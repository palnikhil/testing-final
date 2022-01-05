import cv2
import base64
import numpy as np
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def from_b64(uri):
    '''
        Convert from b64 uri to OpenCV image
        Sample input: 'data:image/jpg;base64,/9j/4AAQSkZJR......'
    '''
    encoded_data = uri.split(',')[1]
    data = base64.b64decode(encoded_data)
    np_arr = np.fromstring(data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def to_b64(img):
    '''
        Convert from OpenCV image to b64 uri
        Sample output: 'data:image/jpg;base64,/9j/4AAQSkZJR......'
    '''
    _, buffer = cv2.imencode('.jpg', img)
    uri = base64.b64encode(buffer).decode('utf-8')
    return f'data:image/jpg;base64,{uri}'

def grayscale(data):
    try:
        img = from_b64(data)
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        # Do some OpenCV Processing
         image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
         image.flags.writeable = False
      
        # Make detection
         results = pose.process(image)
    
        # Recolor back to BGR
         image.flags.writeable = True
         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
         mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )
         
        # End for OpenCV Processing
        
        return to_b64(image)
    except:
        # just in case some process is failed
        # normally, for first connection
        # return the original data
        return data
