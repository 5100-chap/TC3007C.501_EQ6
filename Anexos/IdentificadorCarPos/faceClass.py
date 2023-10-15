import face_recognition

class FaceClass:
    def __init__(self, student_image_path):
        self.student_image = face_recognition.load_image_file(student_image_path)
        self.student_encoding = face_recognition.face_encodings(self.student_image)[0]

    def recognize_faces(self, frame):
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        labels = []
        for encoding in face_encodings:
            matches = face_recognition.compare_faces([self.student_encoding], encoding)
            label = "Desconocido"
            if True in matches:
                label = "Estudiante"
            labels.append(label)
        return face_locations, labels
