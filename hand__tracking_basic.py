import cv2
import mediapipe as mp
import time
import pyautogui as py
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

ctime = 0
ptime = 0
# You need to download 'hand_landmarker.task' from Google's website
base_options = python.BaseOptions(model_asset_path="Hand_guesture_controlled_gaming\hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,  # Good for webcams
)

cap = cv2.VideoCapture(0)
jump=0
'''
option = input("Run? y/n: ")
if option=='n':
    sys.exit()
'''
    
time.sleep(1)
with vision.HandLandmarker.create_from_options(options) as landmarker:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        
        h, w, c = frame.shape

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        frame = cv2.flip(frame, 1)
        #THE PROCESSING LOGIC

        # 1) Convert OpenCV BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 2). Wrap it in a MediaPipe Image object
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # 3) Get a timestamp in milliseconds
        timestamp_ms = int(time.time() * 1000)

        # 4) Perform detection
        result = landmarker.detect_for_video(mp_image, timestamp_ms)
        list_lm = []
        if result.hand_landmarks:
            i = -1
            flag = 0
            
            #DRAWING points
            for hand_landmarks in result.hand_landmarks:
                # Loop through each of the 21 landmarks
                for landmark in hand_landmarks:
                    i += 1
                    # Convert normalized (0.0 to 1.0) to pixel coordinates
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    
                    #use this for analyzing the position of the points to build your own control system check 21 landmarks.png file in the repo
                    #print(f"Lm No.={i}, X={int(landmark.x * w)},Y={int(landmark.y * h)}") 

                    # Draw a small green circle on each point
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                #EXAMPLE index finger tip (no.8), check 21 landmarks.png file to know the index no. of any finger.
                index = hand_landmarks[8]
                ix, iy = int(index.x* w), int(index.y * h)

                #EXAMPLE
                # DINO CONTROLS 
                
                if iy < h * 0.4:  # Top 40% of screen
                    if jump == 0:
                        jump = 1
                        py.press("space")
                    cv2.putText(
                        frame,
                        "JUMP!",
                        (w // 2 - 50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5,
                        (0, 0, 255),
                        3,
                    )
                else:
                    jump = 0
                
                                                           
        # Draw a visual line for the jump boundary
        cv2.line(frame, (0, int(h * 0.4)), (w, int(h * 0.4)), (0, 150, 255), 1)        
           

        cv2.putText(frame,str(int(fps)),(500, 400),cv2.FONT_HERSHEY_PLAIN,2, (255, 255, 255),2,)
        
        # SHOW THE FRAME
        cv2.imshow("Hand Tracking", frame)
        #print("fps=", fps)
        if cv2.waitKey(1) & 0xFF == ord("k"):
            break

cap.release()
cv2.destroyAllWindows()

print("done")
