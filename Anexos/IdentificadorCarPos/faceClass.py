import face_recognition
import os

class FaceClass:
    def __init__(self, student_images_folder_path):
        self.student_encodings = []
        self.student_labels = []
        
        for filename in os.listdir(student_images_folder_path):
            if filename.endswith(".png") or filename.endswith(".jpg"):  # Añade más formatos si es necesario
                image_path = os.path.join(student_images_folder_path, filename)
                student_image = face_recognition.load_image_file(image_path)
                
                try:
                    student_encoding = face_recognition.face_encodings(student_image)[0]
                    self.student_encodings.append(student_encoding)
                    self.student_labels.append(filename.split('.')[0])  # Usar el nombre del archivo como etiqueta
                except IndexError:
                    print(f"No se pudo encontrar una cara en {filename}. Ignorando esta imagen.")

    def recognize_faces(self, frame):
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        labels = []
        
        for encoding in face_encodings:
            matches = face_recognition.compare_faces(self.student_encodings, encoding)
            label = "Desconocido"
            
            if True in matches:
                first_match_index = matches.index(True)
                label = self.student_labels[first_match_index]
            
            labels.append(label)
        
        return face_locations, labels
