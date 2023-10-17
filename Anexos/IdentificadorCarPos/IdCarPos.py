import cv2
from faceClass import FaceClass
from postureClass import PostureClass

def main():
    face_class = FaceClass("Anexos/IdentificadorCarPos/Imagenes/")
    posture_class = PostureClass()
    
    cap = cv2.VideoCapture(0)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        face_locations, labels = face_class.recognize_faces(frame)
        for (top, right, bottom, left), label in zip(face_locations, labels):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, label, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        
        arm_frame = posture_class.detect_arms(frame)
        
        cv2.imshow('Frame', arm_frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
