import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs


import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

import cv2 # type: ignore
import mediapipe as mp # type: ignore

import mediapipe as mp
from utils import overlay_transparent


image_path = os.path.join("ar-face-filters","assets", "sunglasses.png")
# Load filter image
sunglasses = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)


mp_drawing = mp.solutions.drawing_utils #accesses the drawing utilities
mp_face_detect = mp.solutions.face_mesh #accesses the face mesh solution in MediaPipe. Use to initialize the model



d_spec = mp_drawing.DrawingSpec(color = (255, 0, 0), thickness = 1, circle_radius=1)

video = cv2.VideoCapture(0) #creates a video capture object to access the default camera (0 = primary webcam)
#video is the object used to read frames from the webcam

with mp_face_detect.FaceMesh(min_detection_confidence= 0.5, min_tracking_confidence = 0.5) as face_mesh:

    while True:
        ret,image=video.read() #Reads a single frame from the webcam
        #ret is a boolean, True if the frame is read correctly
        #image contains the actual frame (image) captured from the webcam

        image = cv2.flip(image, 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # convert frames into rgb

        # making more accurecy
        image.flags.writeable = False 
        output = face_mesh.process(image) # process the image
        # print(output)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # convert frames into bgr
        if output.multi_face_landmarks:
            for face_landmarks in output.multi_face_landmarks:
                ih, iw, _ = image.shape

                # Get eye positions
                left_eye = face_landmarks.landmark[33]
                right_eye = face_landmarks.landmark[263]

                x1 = int(left_eye.x * iw)
                y1 = int(left_eye.y * ih)
                x2 = int(right_eye.x * iw)
                y2 = int(right_eye.y * ih)

                w = int(1.5 * abs(x2 - x1))
                h = int(w * 0.4)
                x = x1 - int(w * 0.25)
                y = y1 - int(h * 0.5)

                image = overlay_transparent(image, sunglasses, x, y, (w, h))

        cv2.imshow("AR Face Filter", image) #cv2.imshow() shows the image in a real-time window. Face detection is the title of the window

        k=cv2.waitKey(1)
        if k==ord('n'):
            break
        elif cv2.getWindowProperty("AR Face Filter", cv2.WND_PROP_VISIBLE) < 1:
            break

    video.release() #Releases the webcam so it's no longer being used by your program
    cv2.destroyAllWindows() #Closes all OpenCV windows created during the program