import cv2
import pyautogui
import mediapipe as mp
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
x1=x2=y1=y2=0
webcam = cv2.VideoCapture(0)
while webcam.isOpened():
    r,f = webcam.read()
    height,width,x=f.shape
    f = cv2.cvtColor(f,cv2.COLOR_BGR2RGB)
    result = hands.process(f)
    f = cv2.cvtColor(f,cv2.COLOR_RGB2BGR)
    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            mpDraw.draw_landmarks(f,handLms,mpHands.HAND_CONNECTIONS)
            if handLms:
                for id, landmark in enumerate(handLms.landmark):
                    x=int(landmark.x*width)
                    y=int(landmark.y*height)
                    if id ==4:
                        x1=x
                        y1=y
                    if id ==8:
                        x2=x
                        y2=y
                        dist =((x2-x1)**2 + (y2-y1)**2)**(0.5)//4
                        if dist >30:
                            pyautogui.press("volumeup")
                            cv2.putText(f,"Volume UP",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),4)
                        else:
                            pyautogui.press("volumedown")
                            cv2.putText(f,"Volume DOWN",(50,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),4)
                        print(dist)
                        cv2.line(f,(x1,y1),(x2,y2),(0,0,255),4)
    if r== True:
        cv2.flip(f,1)
        cv2.imshow("gesture volume control",f)
        if cv2.waitKey(25) & 0xff == ord("q"):
            break
    else:
        break
webcam.release()
cv2.destroyAllWindows()