import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
from database import KneeExercise
from sqlalchemy.orm import sessionmaker 
from sqlalchemy import create_engine

def opendb():
    engine = create_engine('sqlite:///db.sqlite3')
    Session = sessionmaker(bind=engine)
    sess = Session()
    return sess

def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def start_knee_excercise(campos=0):
    cap = cv2.VideoCapture(0)

    # Curl counter variables
    counter = 0 
    stage = None

    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            frame = cv2.flip(frame,1)
            frame = cv2.resize(frame, (0,0), fx=2, fy=2)
            # Recolor image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
        
            # Make detection
            results = pose.process(image)
        
            # Recolor back to BGR
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark
            
                # Get coordinates
                hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                
                ankle_coords = tuple(np.multiply(ankle, [640, 480]).astype(int))
                cv2.putText(image, str(ankle_coords), ankle_coords ,cv2.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 1, cv2.LINE_AA)
                # Curl counter logic
                if ankle_coords[1] < 350 and ankle_coords[1] > 300:
                    stage = "up"
                elif ankle_coords[1] > 450 and stage =='up':
                    stage="down"
                    counter +=1
                    print(counter,stage)
                    db = opendb()
                    entry = db.query(KneeExercise).filter(KneeExercise.user_id == 1).first()
                    if entry:
                        entry.count=counter
                        print('updated')
                    db.commit()
                    db.close()
                 
                
            except Exception as e:
                pass 
                print(e)
            
            # Render curl counter
            # Setup status box
            cv2.rectangle(image, (0,0), (250,73), (245,117,16), -1)
            
            # Rep data
            cv2.putText(image, 'REPS', (15,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
            
            # Stage data
            cv2.putText(image, 'STAGE', (85,12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)
            cv2.putText(image, stage, 
                        (85,60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
            
            
            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                    mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                    )               
            
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    start_knee_excercise()