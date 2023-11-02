import cv2
from faceClass import FaceClass
from postureClass import PostureClass

def main():
    # Inicialización de clases
    face_class = FaceClass('Anexos/IdentificadorCarPos/Imagenes/')
    posture_class = PostureClass()
    # tracking_class = TrackingClass()  # Si decides implementarla

    # Captura de video
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break

        frame = cv2.flip(frame, 1)
        orig = frame.copy()

        # Reconocimiento facial y registro de asistencia
        face_locations, labels = face_class.recognize_faces(frame)
        face_class.register_attendance(labels)
        
        # Dibuja rectángulos y etiquetas
        frame = face_class.draw_faces(frame, face_locations, labels)

        # Detección de manos levantadas
        image_drawn = posture_class.detect_arms(frame)
        # ... (código para procesar la detección de manos levantadas)

        # Seguimiento de personas
        # tracked_objects = tracking_class.update_trackers(frame, face_locations)
        # ... (código para procesar objetos rastreados)

        # Mostrar el resultado
        cv2.imshow("Frame", image_drawn)
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
