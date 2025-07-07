import cv2
import os
import numpy as np
import mediapipe as mp
from collections import deque

SEQUENCE_LENGTH = 30
SAVE_DIR = "dataset"
GESTURE = ("kuharisha")    # Change this for each sign

mp_pose = mp.solutions.pose.Pose()
mp_hands = mp.solutions.hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
sequence = deque(maxlen=SEQUENCE_LENGTH)
saved_count = 0
hands_detected = False

if not os.path.exists(os.path.join(SAVE_DIR, GESTURE)):
    os.makedirs(os.path.join(SAVE_DIR, GESTURE))

def extract_landmarks(results_pose, results_hands):
    landmarks = []

    if results_pose.pose_landmarks:
        for lm in results_pose.pose_landmarks.landmark:
            landmarks.extend([lm.x, lm.y, lm.z])
    else:
        landmarks.extend([0] * 99)

    hand_landmarks = [results_hands.multi_hand_landmarks] if results_hands.multi_hand_landmarks else []
    hands = hand_landmarks[0] if hand_landmarks else []

    full_hand = []
    for h in hands[:2]:
        for lm in h.landmark:
            full_hand.extend([lm.x, lm.y, lm.z])
    full_hand += [0] * (126 - len(full_hand))

    landmarks.extend(full_hand)
    return landmarks

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results_pose = mp_pose.process(img_rgb)
    results_hands = mp_hands.process(img_rgb)

    keypoints = extract_landmarks(results_pose, results_hands)
    hands_present = results_hands.multi_hand_landmarks is not None

    if hands_present or hands_detected:
        hands_detected = True
        sequence.append(keypoints)

        if len(sequence) == SEQUENCE_LENGTH:
            np.save(os.path.join(SAVE_DIR, GESTURE, f"{saved_count}.npy"), np.array(sequence))
            saved_count += 1
            sequence.clear()
            print(f"[✓] Saved sequence {saved_count}")

    cv2.imshow("Collecting", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
