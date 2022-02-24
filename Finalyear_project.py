##########################Importing libraries required for the program #############################
import face_recognition
import cv2
import numpy as np
from time import sleep
from tkinter import *
from PIL import Image
from tkinter import messagebox




########################## Declare the RFID numbers of the Users ####################################
#SALONIid=xxxxxxxxxx
#NAYANid=xxxxxxxxxxx
DEVid = 419969722853
syspass = "dev"


########################## Scan the RFID Card ########################################################
def RFID():                      
    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522
    global id
    reader = SimpleMFRC522()
    id, text = reader.read()
    if id==DEVid:      #check if the id is of dev or not
        #print(id)
        GPIO.cleanup()
        messagebox.showinfo( "Car Security system", "Welcome Dev Joshi")
        sleep(0.5)
        root.destroy()
        
   
#################################### Function used if REPORT button is pressed ##########################   
def report():
    import urllib.request
    import urllib.parse
                 
    def sendSMS(apikey, numbers, sender, message):
        data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,'message' : message, 'DEv': sender})
        data = data.encode('utf-8')
        request = urllib.request.Request("https://api.textlocal.in/send/?")
        f = urllib.request.urlopen(request, data)
        fr = f.read()
        return(fr)
                 
    resp =  sendSMS('PhNzii9Muu4-IoJJZSXG6hYxSkIsRZ7mCqcYWnBHlx', '917990277613','JimsAutos', 'Error reported please call this product id')
    print (resp)
    messagebox.showinfo( "Car Security system", "You will receive a call shortly\n Sorry for the inconvenience")


############################ Function to termiante the system after checking the password #####################################################
def Terminate():
    password = pwordEL.get()
    if password == syspass:
        rootB = Tk()
        rootB.geometry("300x100")
        kill = Label (rootB, text = "Disabling this car system")
        sleep(1)
        sys.exit('System Disabled by the owner')
        rootA.destroy()
        rootB.destroy()
        root.destroy()
    else:
        messagebox.showwarning( "Car Security system", "Invalid Password!!!!! \n Please try again!!")
        
        
    
    
###########################  Function to show GUI of the button Disable the system ##########################################
def Disable():
    import sys
    global pwordEL
    rootA = Tk()
    intruction = Label(rootA, text='Please Login\n') 
    intruction.grid(sticky=E)
    pwordL = Label(rootA, text=' Insert Password: ')
    pwordL.grid(row=1, sticky=W)
    pwordEL = Entry(rootA, show='*')
    pwordEL.grid(row=1, column=1)
    loginB = Button(rootA, text='Disable', command=Terminate) 
    loginB.grid(columnspan=2, sticky=W)
    rootA.mainloop()


    

################################# Function for the GUI shown in the starting ###############################################    
def GUI():
    global root
    root = Tk()    
    root.wm_title("Car Security system")
    root.geometry("300x250")
    label_2=Label(text="Car security dashboard", bg="white", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    label_1= Label(root, text= "Place Your RFID card on the receiver ").pack()
    Label(text="").pack()
    button_1= Button(root,text="Start Scanning", command = RFID,bg= "white", fg = "green").pack()
    Label(text="").pack()
    button_2= Button(root,text="Report Error ", command = report,bg= "white", fg = "blue").pack()
    Label(text="").pack()
    button_3= Button(root,text="Disable System", command = Disable,bg= "white", fg = "red").pack()
    root.mainloop()
GUI()


###################################### Function to send message about who is driving the car ###################################
def message(face_names):
    
    if face_names==['DevJoshi']:
        name = face_names[0]
    elif face_names ==['SaloniShah']:
        name = face_names[0]
    elif face_names==['NayanParmar']:
        name = face_names[0]
    elif face_names==[Unknown]:
        name = face_names[0]
    import urllib.request
    import urllib.parse
    import time

    localtime = time.asctime( time.localtime(time.time()) )
                    
                     
    def sendSMS(apikey, numbers, sender, message):
        data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
                            'message' : message, 'DEv': sender})
        data = data.encode('utf-8')
        request = urllib.request.Request("https://api.textlocal.in/send/?")
        f = urllib.request.urlopen(request, data)
        fr = f.read()
        return(fr)
                     
    resp =  sendSMS('PhNzii9Muu4-IoJJZSXG6hYxSkIsRZ7mCqcYWnBHlx', '917990277613',
                        'JimsAutos', str(name)+' is driving the car on'+str(localtime))
    print (resp)
    print(str(name)+' is driving the car on '+str(localtime))
        
    
############################################################################################
###########################code for face recognition started##############################

print("[INFO]..........face recognition started") 
# start your webcam
video_capture = cv2.VideoCapture(0)

# load the picture whose face has to be recognised.
Dev_image = face_recognition.load_image_file("/home/pi/photos/dev.jpg")
Dev_face_encoding = face_recognition.face_encodings(Dev_image)[0]

# Load a second picture whose face has to be recognised
saloni_image = face_recognition.load_image_file("/home/pi/photos/saloni.JPG")
saloni_face_encoding = face_recognition.face_encodings(saloni_image)[0]

# Load the third picture whose face has to be recognised
nayan_image = face_recognition.load_image_file("/home/pi/photos/nayan.jpg")
nayan_face_encoding = face_recognition.face_encodings(nayan_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    Dev_face_encoding,
    saloni_face_encoding,
    nayan_face_encoding
    ]
known_face_names = [
    "DevJoshi",
    "SaloniShah",
    "NayanParmar"
    ]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
dev=1
saloni=1
nayan=1
unkown=1
#######################################################################################
################infinite loop to recognise face in the frame of the camera############
while True:
        
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    #Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)
            #print(face_names)
            ###################Recognise if there is another face and contact the owner about the driver###### 
            if id==DEVid and face_names==['DevJoshi'] and dev==1:
                message(face_names)
                dev=0
                    
                   
            elif id==DEVid and face_names==['SaloniShah'] and saloni==1:
                message(face_names)
                saloni=0
                
                
            elif id==DEVid and face_names==['NayanParmar'] and nayan==1:
                message(face_names)
                nayan=0
                
                
            elif id==DEVid and face_names==['Unkown']and unkown==1:
                message(face_names)
                unknown=0
    
            
            


    process_this_frame = not process_this_frame
    
    
   
    
        # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

            # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        

        # Display the resulting image
    cv2.imshow('Video', frame)
    
    
    
    
        # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        video_capture.release()
        cv2.destroyAllWindows()
       
        

    # Release handle to the webcam

root.mainloop()





