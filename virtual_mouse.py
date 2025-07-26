import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

click_threshold = 30  # Distance between fingers to click

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Mirror the camera
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for hand_landmark in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmark, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmark.landmark
            index_finger = landmarks[8]
            thumb = landmarks[4]

            # Convert to screen coordinates
            x = int(index_finger.x * screen_w)
            y = int(index_finger.y * screen_h)
            pyautogui.moveTo(x, y)

            # Click gesture
            thumb_x = int(thumb.x * screen_w)
            thumb_y = int(thumb.y * screen_h)
            distance = ((thumb_x - x)**2 + (thumb_y - y)**2)**0.5
            if distance < click_threshold:
                pyautogui.click()
                pyautogui.sleep(0.5)

    cv2.imshow("Virtual Mouse", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
