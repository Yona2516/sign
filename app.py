import asyncio
import websockets
import cv2
import numpy as np
import torch
from collections import deque
import mediapipe as mp
import base64
import json
from model.model import SignLanguageLSTM
from dataset_loader import SignDataset

dataset = SignDataset()
label_names = dataset.label_encoder.classes_
model = SignLanguageLSTM(input_size=225, hidden_size=128, output_size=len(label_names))
model.load_state_dict(torch.load("model/lstm_model.pt"))
model.eval()

mp_pose = mp.solutions.pose.Pose()
mp_hands = mp.solutions.hands.Hands()
sequence = deque(maxlen=30)

async def predict_and_send(websocket):
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pose_result = mp_pose.process(rgb)
        hands_result = mp_hands.process(rgb)

        def extract(results_pose, results_hands):
            points = []
            if results_pose.pose_landmarks:
                for lm in results_pose.pose_landmarks.landmark:
                    points.extend([lm.x, lm.y, lm.z])
            else:
                points.extend([0]*99)

            full_hand = []
            if results_hands.multi_hand_landmarks:
                for hand in results_hands.multi_hand_landmarks[:2]:
                    for lm in hand.landmark:
                        full_hand.extend([lm.x, lm.y, lm.z])
            full_hand += [0]*(126 - len(full_hand))
            points.extend(full_hand)
            return points

        keypoints = extract(pose_result, hands_result)
        sequence.append(keypoints)

        label = "..."  # default
        if len(sequence) == 30:
            with torch.no_grad():
                inp = torch.tensor([sequence], dtype=torch.float32)
                pred = model(inp).argmax(dim=1).item()
                label = label_names[pred]

        # Encode image to base64
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        # Send JSON with label and image
        message = json.dumps({
            "label": label,
            "image": jpg_as_text
        })

        await websocket.send(message)

        # Optional: display locally
        cv2.imshow("Real-Time Sign Translator", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

async def main():
    async with websockets.serve(predict_and_send, "localhost", 8765):
        print("WebSocket server started at ws://localhost:8765")
        await asyncio.Future()

asyncio.run(main())
