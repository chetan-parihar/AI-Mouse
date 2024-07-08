import cv2 
import mediapipe as mp
import pyautogui as gui
import numpy as np

cam=cv2.VideoCapture(0)
object=mp.solutions.hands.Hands(False,2,.8,.8)
mpDraw=mp.solutions.drawing_utils

gui.FAILSAFE = False
temp=[]
dis_x,dis_y=0,0

while True:
    myHands=[]
    ret,frame=cam.read()

    frame= cv2.flip(frame,1)

    height,width,_=frame.shape
    
    frameRGB=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=object.process(frameRGB)
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    #rectangle_1
    rectangle_p1_x,rectangle_p1_y=200,100
    rectangle_p2_x,rectangle_p2_y=400,250
    first_rect_speed=23


    cv2.rectangle(frame,(rectangle_p1_x,rectangle_p1_y),(rectangle_p2_x,rectangle_p2_y),(255,0,0),2)
    # cv2.rectangle(frame,(70,70),(430,330),(255,0,255),2)
    

    if results.multi_hand_landmarks!=None:
        for handLandMark in results.multi_hand_landmarks:
            myHand=[]
            # mpDraw.draw_landmarks(frame,handLandMark,mp.solutions.hands.HAND_CONNECTIONS)
            for Landmark in handLandMark.landmark:
                myHand.append((int(Landmark.x*width),int(Landmark.y*height)))

            finger_x,finger_y=myHand[8][0],myHand[8][1]
            mouse_x,mouse_y=gui.position()
            cv2.circle(frame,(finger_x,finger_y),5,(0,55,225),-9)
            
            cv2.circle(frame,(myHand[10][0],myHand[10][1]),5,(0,55,225),-9)
            cv2.circle(frame,(myHand[4][0],myHand[4][1]),5,(0,55,225),-9)
            
            distance_click=abs(myHand[10][0]-myHand[4][0])

            temp.append((finger_x,finger_y))
            
            if len(temp)>=2:
                dis_x=temp[1][0]-temp[0][0]
                dis_y=temp[1][1]-temp[0][1]
            # print(dis_x,dis_y)

            if finger_x>rectangle_p1_x and finger_y>rectangle_p1_y and finger_x<rectangle_p2_x and finger_y<rectangle_p2_y:
                mouse_x=mouse_x+dis_x
                mouse_y=mouse_y+dis_y
            if finger_x<rectangle_p1_x and finger_y<rectangle_p1_y:
                mouse_x=mouse_x-first_rect_speed
                mouse_y=mouse_y-first_rect_speed
            if finger_x>rectangle_p2_x and finger_y<rectangle_p1_y:
                mouse_x=mouse_x+first_rect_speed
                mouse_y=mouse_y-first_rect_speed
            if finger_x>rectangle_p2_x and finger_y>rectangle_p2_y:
                mouse_x=mouse_x+first_rect_speed
                mouse_y=mouse_y+first_rect_speed
            if finger_x<rectangle_p1_x and finger_y>rectangle_p2_y:
                mouse_x=mouse_x-first_rect_speed
                mouse_y=mouse_y+first_rect_speed
            if finger_y<rectangle_p1_y:
                mouse_y=mouse_y-first_rect_speed
                mouse_x=mouse_x
            if finger_x>rectangle_p2_x:
                mouse_x=mouse_x+first_rect_speed
                mouse_y=mouse_y
            if finger_y>rectangle_p2_y:
                mouse_y=mouse_y+first_rect_speed
                mouse_x=mouse_x
            if finger_x<rectangle_p1_x:
                mouse_x=mouse_x-first_rect_speed
                mouse_y=mouse_y

            if len(temp)>3:
                temp.pop(0)
            # print(distance_click)
            if distance_click<45:
                gui.click(mouse_x,mouse_y)

            gui.moveTo(mouse_x,mouse_y)
            myHands.append(myHand)
    

    cv2.imshow("frame",frame)
    if cv2.waitKey(1) & 0xff==ord("q"):
        break

#frame=480 640
#screen= 1920 x 1080
# mouse_pos_x=(480/1920)*myHand[8][0]
# mouse_pos_y=(640/1080)*myHand[8][1]   

video=cv2.VideoCapture(0)
a=0
while True:
    a=a+1
    check, frame= video.read()

    # Converting the input frame to grayscale
    gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   

    # Fliping the image as said in question
    gray_flip = cv2.flip(gray,1)

