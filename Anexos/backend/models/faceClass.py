import face_recognition
import os
import cv2
import time


class FaceClass:
    def __init__(self, student_images_folder_path):
        """
        Inicializa una instancia de la clase FaceClass.

        Args:
            student_images_folder_path (str): Ruta de la carpeta que contiene las imágenes de referencia de los estudiantes.
        """
        self.student_encodings = []
        self.student_labels = []
        self.face_counts = {}
        self.face_first_seen = {}
        self.attendance_recorded = {}
        self.previous_labels = []

        # Verificar si CUDA está disponible
        self.use_cuda = cv2.cuda.getCudaEnabledDeviceCount() > 0

        # Detección de caras en imágenes de referencia
        for filename in os.listdir(student_images_folder_path):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                image_path = os.path.join(student_images_folder_path, filename)
                student_image = face_recognition.load_image_file(image_path)

                try:
                    student_encoding = face_recognition.face_encodings(student_image)[0]
                    self.student_encodings.append(student_encoding)
                    self.student_labels.append(filename.split(".")[0])
                except IndexError:
                    print(f"No se pudo encontrar una cara en {filename}. Ignorando esta imagen.")
    
    def recognize_faces(self, frame):
        """
        Reconoce las caras en un frame de imagen.

        Args:
            frame (numpy.ndarray): Frame de imagen en formato numpy array.

        Returns:
            tuple: Una tupla que contiene las ubicaciones de las caras detectadas y las etiquetas correspondientes.
        """
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
        self.previous_labels = labels
        return face_locations, labels

    def draw_faces(self, frame, face_locations, labels):
        """
        Dibuja los recuadros alrededor de las caras detectadas en un frame de imagen.

        Args:
            frame (numpy.ndarray): Frame de imagen en formato numpy array.
            face_locations (list): Lista de ubicaciones de las caras detectadas.
            labels (list): Lista de etiquetas correspondientes a las caras detectadas.

        Returns:
            numpy.ndarray: Frame de imagen con los recuadros y etiquetas dibujados.
        """
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

    def register_attendance(self, labels):
        """
        Registra la asistencia de los estudiantes.

        Args:
            labels (list): Lista de etiquetas correspondientes a las caras detectadas.

        Returns:
            None
        """
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
                if self.face_counts[label] >= 16 or (
                    current_time - self.face_first_seen[label] >= 10
                ):
                    self.attendance_recorded[label] = time.strftime('%H:%M:%S', time.localtime(current_time))  # Guarda el tiempo de asistencia
                    print(
                        f"{label} asistió a las {time.strftime('%H:%M:%S', time.localtime(current_time))}."
                    )
                    # Elimina los registros para liberar memoria
                    del self.face_counts[label]
                    del self.face_first_seen[label]

    def get_attendance_label(self):
        """
        Obtiene los datos de asistencia registrados.

        Returns:
            list: Lista de tuplas que contienen la etiqueta del estudiante y el tiempo de asistencia.
        """
        attendance_data = []
        for label, time_attended in self.attendance_recorded.items():
            attendance_data.append((label, time_attended))
        return attendance_data
    
    def calculate_detection_metrics(self, current_labels):
        """
        Calcula las métricas de detección de caras.

        Args:
            current_labels (list): Lista de etiquetas actuales de las caras detectadas.

        Returns:
            dict: Un diccionario que contiene las métricas de detección (verdaderos positivos, verdaderos negativos, falsos positivos, falsos negativos, precisión, recall y f1-score).
        """
        true_positives = 0
        true_negatives = 0
        false_positives = 0
        false_negatives = 0

        for current_label, previous_label in zip(current_labels, self.previous_labels):
            if current_label != "Desconocido":
                if current_label == previous_label:
                    true_positives += 1
                else:
                    false_positives += 1
            else:
                if previous_label != "Desconocido":
                    false_negatives += 1
                else:
                    true_negatives += 1

        # Si el número de etiquetas actuales y previas es diferente
        extra_labels = len(current_labels) - len(self.previous_labels)
        if extra_labels > 0:
            false_positives += extra_labels  # Etiquetas adicionales se consideran como falsos positivos
        elif extra_labels < 0:
            false_negatives -= extra_labels  # Etiquetas faltantes se consideran como falsos negativos

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        return {
            "true_positives": true_positives,
            "true_negatives": true_negatives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
        }