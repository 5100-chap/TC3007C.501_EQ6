import face_recognition
import os
import cv2
import time


class FaceClass:
    def __init__(self, student_images_folder_path):
        self.student_encodings = []
        self.student_labels = []
        self.face_counts = (
            {}
        )  # Añade un diccionario para contar las veces que se ve una cara
        self.face_first_seen = (
            {}
        )  # Añade un diccionario para registrar la primera vez que se ve una cara
        self.attendance_recorded = (
            {}
        )  # Añade un diccionario para llevar un registro de las personas a las que se les ha tomado asistencia

        # Deteccion de caras en imagenes de referencia
        for filename in os.listdir(student_images_folder_path):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = os.path.join(student_images_folder_path, filename)
                student_image = face_recognition.load_image_file(image_path)

                try:
                    student_encoding = face_recognition.face_encodings(student_image)[0]
                    self.student_encodings.append(student_encoding)
                    self.student_labels.append(filename.split(".")[0])
                except IndexError:
                    print(
                        f"No se pudo encontrar una cara en {filename}. Ignorando esta imagen."
                    )

    # Funcion para reconocer caras
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

    # Funcion para dibujar los recuadros para las caras
    def draw_faces(self, frame, face_locations, labels):
        for (top, right, bottom, left), label in zip(face_locations, labels):
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            cv2.putText(
                frame,
                label,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 0, 0),
                2,
            )
        return frame

    # Registra asistencia
    def register_attendance(self, labels):
        current_time = time.time()
        for label in labels:
            if label != "Desconocido":
                # Verifica si ya se ha tomado asistencia para esta persona
                if self.attendance_recorded.get(label, False):
                    continue  # Si ya se ha tomado asistencia, salta al siguiente ciclo

                if label not in self.face_counts:
                    self.face_counts[label] = 1
                    self.face_first_seen[label] = current_time
                else:
                    self.face_counts[label] += 1

                # Verifica si se han cumplido las condiciones para marcar la asistencia
                if self.face_counts[label] >= 6 or (
                    current_time - self.face_first_seen[label] >= 10
                ):
                    print(
                        f"{label} asistió a las {time.strftime('%H:%M:%S', time.localtime(current_time))}."
                    )
                    self.attendance_recorded[
                        label
                    ] = True  # Marca que se ha tomado asistencia para esta persona
                    # Elimina los registros para liberar memoria
                    del self.face_counts[label]
                    del self.face_first_seen[label]
