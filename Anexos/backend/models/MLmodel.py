import os
from models.faceClass import FaceClass
from models.postureClass import PostureClass
import cv2

class MLmodel:
    def __init__(self, db_manager):
        self.posture_class = PostureClass()
        self.db_manager = db_manager

        # Obtener la ruta absoluta del archivo actual
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Unir la ruta actual con la carpeta "faces"
        faces_dir = os.path.join(current_dir, "faces")

        self.face_class = FaceClass(faces_dir)

    def process_video(self, video):
        cap = cv2.VideoCapture(video)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            frame = cv2.flip(frame, 1)
            orig = frame.copy()

            face_locations, labels = self.face_class.recognize_faces(frame)
            self.face_class.register_attendance(labels)
            
            frame = self.face_class.draw_faces(frame, face_locations, labels)
            image_drawn = self.posture_class.detect_arms(frame, labels)

            cv2.imshow("Frame", image_drawn)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
        
    def process_image(self, image):
        # Asumimos que 'image' es una imagen de OpenCV (un ndarray de NumPy)

        # Paso 1: Reconocimiento de Rostros
        face_locations, labels = self.face_class.recognize_faces(image)
        self.face_class.register_attendance(labels)
        image_with_faces = self.face_class.draw_faces(image, face_locations, labels)

        # Paso 2: Detección de Posturas
        image_with_posture = self.posture_class.detect_arms(image_with_faces, labels)

        # Paso 3: Preparar los resultados
        # Aquí puedes incluir cualquier información adicional que quieras devolver,
        # como estadísticas, etiquetas de rostros detectados, etc.
        results = {
            "detected_faces": len(face_locations),
            "detected_labels": labels,
            # ... otros resultados ...
        }

        # Devolver la imagen procesada y los resultados
        return image_with_posture, results