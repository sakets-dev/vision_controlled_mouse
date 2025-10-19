import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Disable PyAutoGUI failsafe for smoother operation
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
screen_w, screen_h = pyautogui.size()

# Click detection variables
click_threshold = 40
right_click_threshold = 50
last_click_time = 0
click_cooldown = 0.5  # seconds between clicks

cap = cv2.VideoCapture(0)

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

            if len(lm_list) >= 21:  # Ensure we have all hand landmarks
                # Get key landmarks
                index_tip = lm_list[8]  # index fingertip
                thumb_tip = lm_list[4]  # thumb tip
                middle_tip = lm_list[12]  # middle fingertip
                ring_tip = lm_list[16]  # ring fingertip
                pinky_tip = lm_list[20]  # pinky fingertip
                
                # Move mouse with index finger
                x, y = index_tip
                screen_x = np.interp(x, (0, w), (0, screen_w))
                screen_y = np.interp(y, (0, h), (0, screen_h))
                pyautogui.moveTo(screen_x, screen_y)

                # Calculate distances for gesture detection
                thumb_index_dist = np.hypot(thumb_tip[0] - index_tip[0], thumb_tip[1] - index_tip[1])
                middle_index_dist = np.hypot(middle_tip[0] - index_tip[0], middle_tip[1] - index_tip[1])
                ring_index_dist = np.hypot(ring_tip[0] - index_tip[0], ring_tip[1] - index_tip[1])
                pinky_index_dist = np.hypot(pinky_tip[0] - index_tip[0], pinky_tip[1] - index_tip[1])
                
                current_time = time.time()
                
                # Left click: thumb and index finger close together
                if (thumb_index_dist < click_threshold and 
                    current_time - last_click_time > click_cooldown):
                    pyautogui.click()
                    cv2.circle(img, (x, y), 15, (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, "LEFT CLICK", (x-30, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    last_click_time = current_time
                
                # Right click: index and middle finger close together
                elif (middle_index_dist < click_threshold and 
                      current_time - last_click_time > click_cooldown):
                    pyautogui.rightClick()
                    cv2.circle(img, (x, y), 15, (0, 0, 255), cv2.FILLED)
                    cv2.putText(img, "RIGHT CLICK", (x-40, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    last_click_time = current_time
                
                # Double click: index, middle, and ring finger close together
                elif (middle_index_dist < click_threshold and 
                      ring_index_dist < click_threshold and
                      current_time - last_click_time > click_cooldown):
                    pyautogui.doubleClick()
                    cv2.circle(img, (x, y), 15, (255, 0, 255), cv2.FILLED)
                    cv2.putText(img, "DOUBLE CLICK", (x-50, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                    last_click_time = current_time
                
                # Scroll up: all fingers close together
                elif (thumb_index_dist < click_threshold and 
                      middle_index_dist < click_threshold and
                      ring_index_dist < click_threshold and
                      pinky_index_dist < click_threshold and
                      current_time - last_click_time > click_cooldown):
                    pyautogui.scroll(3)  # Scroll up
                    cv2.circle(img, (x, y), 15, (255, 255, 0), cv2.FILLED)
                    cv2.putText(img, "SCROLL UP", (x-40, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                    last_click_time = current_time
                
                # Visual feedback for gesture detection
                if thumb_index_dist < click_threshold:
                    cv2.circle(img, (x, y), 20, (0, 255, 0), 2)  # Green circle for left click
                if middle_index_dist < click_threshold:
                    cv2.circle(img, (x, y), 20, (0, 0, 255), 2)  # Red circle for right click

            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

    # Add instruction text overlay
    cv2.putText(img, "Gesture Controls:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(img, "Thumb + Index = Left Click", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.putText(img, "Index + Middle = Right Click", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    cv2.putText(img, "Index + Middle + Ring = Double Click", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 1)
    cv2.putText(img, "All Fingers Together = Scroll Up", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
    cv2.putText(img, "Press 'q' to quit", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    cv2.imshow("Vision Cursor", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()