import cv2
import mediapipe as mp
import time
import pyautogui as py
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

ctime = 0
ptime = 0

#download 'hand_landmarker.task' from Google's website or I'll link it in github
base = python.BaseOptions(model_asset_path="Hand_guesture_controlled_gaming\hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base,
    running_mode=vision.RunningMode.VIDEO)

# "Game Controls"
print("\n\tGAME CONTROLS [HILL CLIMB RACING] \n1.Palm : Accelarate \n2.Fist : Brake  \n3.Index Finger : Neutral\n4.'k' : exit \n")
cap = cv2.VideoCapture(0) #to capture the webcam.

time.sleep(1)

with vision.HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        success, frame = cap.read() #returns each frame
        if not success: #if no more frames
            break
        
        h, w, c = frame.shape #returns height, width and color channels of the frame/Video

        #just to calculate fps
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        #flipping the frame, try executing without this and you'll know why we need this
        frame = cv2.flip(frame, 1)
    
        # 1. Convert OpenCV BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 2. Wrap it in a MediaPipe Image object
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        # 3. Get a timestamp in milliseconds
        timestamp_ms = int(time.time() * 1000)
        # 4. Perform detection
        result = landmarker.detect_for_video(mp_image, timestamp_ms)
        
        if result.hand_landmarks:
            i = -1
            flag = 0
            
            #LANDMARKS
            for hand_landmarks in result.hand_landmarks:
                # Loop through each of the 21 landmarks
                for landmark in hand_landmarks:
                    i += 1
                    # Convert normalized (0.0 to 1.0) to pixel coordinates
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    # print(f"Lm No.={i}, X={int(landmark.x * w)},Y={int(landmark.y * h)}") #to print position of each landmarks, needed sometimes to analyze the movements of fingers

                    # Draw a small green circle on each point
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                # wrist
                wrist = hand_landmarks[0]
                wx, wy = int(wrist.x * w), int(wrist.y* h)
                #index finger
                index = (hand_landmarks[8].x, hand_landmarks[8].y)
                ix, iy = int(index[0]* w), int(index[1] * h)
                # middle finger
                middle = hand_landmarks[12]
                mx, my = int(middle.x * w), int(middle.y * h)
                
                separation_wm = abs(wy-my)  # distance btween middle finger and wrist
                
                # HILL CLIMB RACING CONTROLS 
                #flag=0 -> nothing, flag=1 -> Accelaration, flag=2 ->BRAKE, flag=3 -> Neutral
                
                cv2.line(frame, (wx, wy), (mx, my), (255, 150, 12), 2)
                #print("Sep", separation)

                if separation_wm >= 120:
                    if flag != 1:
                        flag = 1
                        py.keyUp("left")
                        py.keyDown("right")
                        cv2.putText(frame,"gas!",(w // 2 - 50, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 255, 0),2,)

                elif separation_wm < 120 and iy > h * 0.5:
                    if flag != 2:
                        flag = 2
                        py.keyUp("right")
                        py.keyDown("left")
                        cv2.putText(frame,"brake!",(w // 2 - 50, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255),2,)

                elif iy < h * 0.4 and separation_wm <120:
                    if flag != 3:
                        flag = 3
                        py.keyUp("right")
                        py.keyUp("left")
                        cv2.putText(frame,"neutral!",(w // 2 - 50, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 150, 200),2,)       
                
        cv2.putText(frame,str(int(fps)),(500, 400),cv2.FONT_HERSHEY_PLAIN,2, (255, 255, 255),2,)
        #print("fps=", fps)
        
        # SHOW THE FRAME
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord("k"): #click 'k' to quit
            break

cap.release()
cv2.destroyAllWindows()

print("done")
