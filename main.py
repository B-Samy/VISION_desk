import cv2 
import mediapipe as mp 
import mediapipe as mp  
from mediapipe.tasks import python 
from mediapipe.tasks.python import vision
import numpy as np 
import pyautogui


face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

)
cam = cv2.VideoCapture(0)

my_hands = mp.solutions.hands.Hands( max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5)
drawing_utils = mp.solutions.drawing_utils


if not cam.isOpened():
    raise IOError('Cant access webcam')



# for pyautogui : screen widht and height 
screen_width  , screen_height = pyautogui.size()

# for pyautogui pinch func logic 
is_pinch = False


smooth_cursor = 3
prev_x  = 0 
prev_y = 0

while True:
    ret , frame = cam.read()

    
    
    if not ret:
        print('Cant read the video frames')
        break 
    
    
    
    
        
    frame_height , frame_width , _ = frame.shape
    frame = cv2.flip(frame , 1)
    
    rgb = cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb)
    
    hands = output.multi_hand_landmarks
    
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame,hand , mp.solutions.hands.HAND_CONNECTIONS,
            
            landmark_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
            color=(0, 255, 255),  # Red dots
            thickness=1,
            circle_radius=5
            ),
            
            connection_drawing_spec=mp.solutions.drawing_utils.DrawingSpec(
            color=(255, 255,255),  
            thickness=1
            )
            
            )
            landmarks  = hand.landmark
            
            

            

    
            
        index_tip = hand.landmark[8]
        thumb_tip = hand.landmark[4]
        
        middle_tip = hand.landmark[12]
        ring_tip = hand.landmark[16]
        pinky_tip = hand.landmark[20]
        
        index_joint = hand.landmark[6]
        middle_joint = hand.landmark[10]
        ring_joint = hand.landmark[14]
        pinky_joint = hand.landmark[18]
        
        thumb_join = hand.landmark[2]
        
        
        
        
        
        
        
        x = int(index_tip.x * frame_width)
        y = int(index_tip.y * frame_height)
        
        cv2.circle(frame , (x,y) ,15 ,  (255,0,255) , -1)
        print('Fingertips' , x,y)
        

        mouse_x = int(x* screen_width / frame_width)
        mouse_y = int(y* screen_height / frame_height)
        

        
        def pinch_click():
            global is_pinch
            
            
            distance = (
            (thumb_tip.x - index_tip.x)**2 + (thumb_tip.y - index_tip.y)**2
            )**0.5
            if distance < 0.05:
                print('pinch detected')
            
            
            is_pinch_active = distance < 0.05
            
            
            if is_pinch_active:
                print('Pinch activated')
        
            if is_pinch_active and not is_pinch:
                pyautogui.click()
                print('clicked')       
                
            is_pinch = is_pinch_active
        
        
        def thump():
        # for volume increase by using thump up 
        # for volume decrease by using thump down 
        
            is_thump_up = thumb_tip.y  < thumb_join.y 
            is_thump_down =  thumb_tip.y  > thumb_join.y 
        
            if is_thump_up:
                pyautogui.press('volumeup')  
        
            if is_thump_down:
                pyautogui.press('volumedown')
            
        
        def right_click():
            # right click on 2 fingers like V gesture in real life 
            
            two_fingers = (
                index_tip.y <index_joint.y and 
                middle_tip.y < middle_joint.y and 
                ring_tip.y > ring_joint.y and 
                pinky_tip.y > pinky_joint.y 
            )
            
            if two_fingers:
                pyautogui.rightClick()
                print('Right Click occuring!!!')
            
            
        
        is_open_palm = (
            index_tip.y < index_joint.y and 
            middle_tip.y < middle_joint.y and 
            ring_tip.y < ring_joint.y and 
            pinky_tip.y < pinky_joint.y and 
            thumb_tip.x < thumb_join.x
        )
        

        if is_open_palm:
            is_pinch = False
            
            cv2.putText(
                frame , 
                'Paused' , 
                (50,50),
                cv2.FONT_HERSHEY_SIMPLEX , 
                1 , 
                (0,0,255),
                2
            )
            print("PAUSED — cursor movement disabled")
        else:
            current_x = prev_x + (mouse_x - prev_x) / smooth_cursor
            current_y = prev_y + (mouse_y - prev_y ) / smooth_cursor
            
            pyautogui.moveTo(int(current_x), int(current_y))
            
            prev_x = current_x
            prev_y = current_y
            
            pinch_click()
            thump()
            right_click()
            
            


        
    faces = face_cascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5 ,
        minSize=(30,30)
    )    
    
    for(x,y,w,h) in faces:
        cv2.rectangle(
            frame,
            (x,y),
            (x+w , y+h) ,
            (0,255,0),
            2
        )
        
        



    
    cv2.imshow('Displaying video frame ' , frame)
    
    
    key = cv2.waitKey(10)
    
    if key == 27:
        break 
    
cam.release()
cv2.destroyAllWindows()