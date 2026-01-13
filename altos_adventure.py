import cv2
import mediapipe as mp
import time
import pyautogui as py
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pygame as pg

pg.mixer.init()
ctime = 0
ptime = 0
# --- 1. SETUP ---
# You need to download 'hand_landmarker.task' from Google's website
base_options = python.BaseOptions(model_asset_path="Hand_guesture_controlled_gaming\hand_landmarker.task")
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.VIDEO,  # Good for webcams
)

 
# "Game Controls"
print("\n\tGAME CONTROLS [ALTO'S ADVENTURE]\nPinch -> thumb and index finger: \nPinch = Jump (single click) \nPinch for long time = backflip (Long press)\n'k' : exit \n")

s1=cv2.imread("Hand_guesture_controlled_gaming\sdk1.jpg")
s2=cv2.imread("Hand_guesture_controlled_gaming\sdk2.webp")
s2= cv2.resize(s2,(500,544))
s3=cv2.imread("Hand_guesture_controlled_gaming\sdk3.jpg")
s4=cv2.imread("Hand_guesture_controlled_gaming\sdk4.jpg")
s5=cv2.imread("Hand_guesture_controlled_gaming\sdk5.jpg")
s6=cv2.imread("Hand_guesture_controlled_gaming\sdk6.jpeg")
s7=cv2.imread("Hand_guesture_controlled_gaming\sdk7.jpeg")
s8=cv2.imread("Hand_guesture_controlled_gaming\sdk8.jpeg")
#s9=cv2.imread("Hand_guesture_controlled_gaming\sdk9.gif")
s10=cv2.imread("Hand_guesture_controlled_gaming\sdk10.gif")

cap = cv2.VideoCapture(0)
play=0
pg.mixer.music.load("Hand_guesture_controlled_gaming\EsDeeKid & Rico Ace - Phantom.mp3")

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
        
        #PROCESSING LOGIC
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
            
            #DRAWING LM points
            for hand_landmarks in result.hand_landmarks:
                # Loop through each of the 21 landmarks
                for landmark in hand_landmarks:
                    i += 1
                    # Convert normalized (0.0 to 1.0) to pixel coordinates
                    x = int(landmark.x * frame.shape[1])
                    y = int(landmark.y * frame.shape[0])
                    # print(f"Lm No.={i}, X={int(landmark.x * w)},Y={int(landmark.y * h)}")

                    # Draw a small green circle on each point
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
                    
                #thumb
                thumb = (hand_landmarks[4].x,hand_landmarks[4].y)
                tx,ty = int(thumb[0]*w), int(thumb[1]*h)
                
                #index
                index = (hand_landmarks[8].x, hand_landmarks[8].y)
                ix, iy = int(index[0]* w), int(index[1] * h)

                '''
                #Uncomment this if you wanna try esdeekid part 
                # middle
                middle = (hand_landmarks[12].x, hand_landmarks[12].y)
                mx, my = int(middle[0] * w), int(middle[1] * h)
                # pinky
                pinky = (hand_landmarks[20].x, hand_landmarks[20].y)
                px, pyy = int(pinky[0] * w), int(pinky[1] * h)
                
                separation_wm = abs(wy-my)  # distance btween middle finger and wrist
                sep_wp = math.dist(wrist,pinky)
                #print("Sep pinky and wrist = ",sep_wp)
                '''

                #ALTO'S ADVENTURE CONTROLS
                
                ti = ix-tx
                if ti<12:
                    if flag!=1:
                        flag=1
                        py.keyDown("space")
                        cv2.putText(frame,"click!",(w // 2 - 50, 50),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0, 150, 200),3,)
                else:
                    py.keyUp("space")
                    
                    
                '''
                #EsDeeKID
                
                if sep_wp<0.15 and separation_wm>120:
                    #cv2.putText(frame,"OK!",(w // 2, h//2),cv2.FONT_HERSHEY_SIMPLEX,2,(0, 225, 0),3)
                    if play!=1:
                        
                        play=1
                        pg.mixer.music.play(loops=0, start=14)
                        time.sleep(0.5)
                        print("NOW MUSIC")
                        cv2.imshow("Esdeekid5",s5)
                        time.sleep(0.01)
                        cv2.imshow("Esdeekid6",s6)
                        time.sleep(0.01)
                        cv2.imshow("Esdeekid7",s7)
                        time.sleep(0.01)
                        cv2.imshow("Esdeekid8",s8)
                        time.sleep(0.01)
                        cv2.imshow("Esdeekid1",s2)
                        time.sleep(0.01)
                        cv2.imshow("Esdeekid2",s1)
                        time.sleep(0.01)
                        cv2.imshow("Esdeekid4",s4)
                        time.sleep(0.01)
                        #cv2.imshow("Esdeekid9",s9)
                        cv2.imshow("Esdeekid3",s3)
                        time.sleep(0.01)
                        cv2.imshow("Esdeekid10",s10)
                        
                else:
                    if play!=0:
                        print("NOt playing music")
                        play=0
                    ''' 
                                                  
        # Draw a visual line for the jump boundary
        #cv2.line(frame, (0, int(h * 0.4)), (w, int(h * 0.4)), (0, 150, 255), 1)        
                
        cv2.putText(frame,str(int(fps)),(500, 400),cv2.FONT_HERSHEY_PLAIN,2, (255, 255, 255),2,)
        
        # SHOW THE FRAME
        cv2.imshow("Hand Tracking", frame)
        #print("fps=", fps)
        if cv2.waitKey(1) & 0xFF == ord("k"):
            break

cap.release()
cv2.destroyAllWindows()

print("done")
