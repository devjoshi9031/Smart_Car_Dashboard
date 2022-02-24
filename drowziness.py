#Import necessary libraries
from scipy.spatial import distance
from imutils import face_utils
import numpy as np
import time
import dlib
import cv2

##### Minimum threshold value of Eye aspect ratio belo which the driver will be considered as drowsy######################
EYE_ASPECT_RATIO_THRESHOLD = 0.3

####### number of frames after which the system will show error on the screen ##############################
EYE_ASPECT_RATIO_CONSEC_FRAMES = 20

################# variable to count the number of frames for whioch the eye aspect ratio is below threshold#############
COUNTER = 0


################### Function to calculate the eye aspect ratio of the face detceted in the screen ################
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    global ear
    ear = (A+B) / (2*C)
    return ear

#Load face detector and predictor, uses dlib shape predictor file
print("[INFO]..... Loading shape_predictor")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('/home/pi/shape_predictor_68_face_landmarks.dat')

#Extract indexes of facial landmarks for the left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

#Start webcam video capture
video_capture = cv2.VideoCapture(0)

#Give some time for camera to initialize(not required)
time.sleep(2)

while(True):
    #Read each frame and flip it, and convert to grayscale
    ret, frame = video_capture.read()
    frame = cv2.flip(frame,1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Detect facial points through detector function
    faces = detector(gray, 0)
    
    for face in faces:

        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        #Get array of coordinates of leftEye and rightEye
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        #Calculate aspect ratio of both eyes
        leftEyeAspectRatio = eye_aspect_ratio(leftEye)
        rightEyeAspectRatio = eye_aspect_ratio(rightEye)

        eyeAspectRatio = (leftEyeAspectRatio + rightEyeAspectRatio) / 2

        #Use hull to remove convex contour discrepencies and draw eye shape around eyes
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        #Detect if eye aspect ratio is less than threshold
        if(eyeAspectRatio < EYE_ASPECT_RATIO_THRESHOLD):
            COUNTER += 1
            #If no. of frames is greater than threshold frames,
            if COUNTER >= EYE_ASPECT_RATIO_CONSEC_FRAMES:
                #pygame.mixer.music.play(-1)
                cv2.putText(frame,"!!!!!!!!!!!!!!!!!!!!!!ALERT!!!!!!!!!!!!!!!!!",(100,450),cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),2)
                cv2.putText(frame, "Drowziness Alert", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
        else:
            #pygame.mixer.music.stop()
            COUNTER = 0
        cv2.putText(frame, "EAR: {:.2f}".format(ear), (500, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    #Show video feed
    cv2.imshow('Video', frame)
    if(cv2.waitKey(1) & 0xFF == ord('q')):
        break

#Finally when video capture is over, release the video capture and destroyAllWindows
video_capture.release()
cv2.destroyAllWindows()