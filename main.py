import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Disable PyAutoGUI failsafe for smoother operation
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()

cap = cv2.VideoCapture(1)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

while True:
    success, img = cap.read()
    if not success:
        print("Error: Could not read from camera")
        break
        
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                lm_list.append((int(lm.x * w), int(lm.y * h)))

            if len(lm_list) >= 9:  # Ensure we have enough landmarks
                x, y = lm_list[8]  # index fingertip
                screen_x = np.interp(x, (0, w), (0, screen_w))
                screen_y = np.interp(y, (0, h), (0, screen_h))
                pyautogui.moveTo(screen_x, screen_y)

                # Click gesture (thumb and index close)
                if len(lm_list) >= 5:  # Ensure thumb landmark exists
                    thumb_x, thumb_y = lm_list[4]
                    dist = np.hypot(thumb_x - x, thumb_y - y)
                    if dist < 40:
                        pyautogui.click()
                        cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Vision Cursor", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()