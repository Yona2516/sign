import cv2
import asyncio
import websockets
import base64
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils

# Open the webcam
cap = cv2.VideoCapture(0)


# WebSocket handler (MUST accept two arguments: websocket and path)
async def send_video(websocket):
    print("Client connected:")
    try:
        while True:
            success, frame = cap.read()
            if not success:
                continue

            # Convert image to RGB for MediaPipe
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(img_rgb)

            # Draw pose landmarks on frame
            if result.pose_landmarks:
                mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Encode image to JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer).decode('utf-8')

            # Send base64 string to the client
            await websocket.send(jpg_as_text)

            # ~30 FPS
            await asyncio.sleep(0.03)

    except websockets.ConnectionClosed:
        print("Client disconnected")


# Start the WebSocket server
async def main():
    print("Starting WebSocket server at ws://localhost:8765")
    async with websockets.serve(send_video, "localhost", 8765):
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
