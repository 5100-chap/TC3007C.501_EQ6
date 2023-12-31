import cv2
import mediapipe as mp
import time


class PostureClass:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()
        self.ongoing_events = {}
        self.transition_duration = 2  # Duración de la transición en segundos
        self.transition_start_time = 0  # Tiempo de inicio de la transición
        self.use_cuda = cv2.cuda.getCudaEnabledDeviceCount() > 0
        self.participations = {}
        self.participations_metrics = {}

    def detect_arms(self, frame, labels):
        """
        Detecta los brazos en un frame y devuelve la imagen con los brazos resaltados.

        Parámetros:
        - frame: Frame de la imagen en formato BGR.
        - labels: Lista de etiquetas de los eventos.

        Retorna:
        - image_drawn: Imagen con los brazos resaltados.
        """
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(image_rgb)
        image_drawn = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)    

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark
            # Verificar si alguien tiene la mano levantada y actualizar el diccionario de eventos
            # Procesar eventos de levantamiento de brazo
            self.process_arm_raise_events(landmarks, labels)
            # Indices de los landmarks para los codos y muñecas
            arm_indices = [11, 12, 13, 14, 15, 16]
            for index in arm_indices:
                landmark = landmarks[index]
                image_h, image_w, _ = frame.shape
                x = int(landmark.x * image_w)
                y = int(landmark.y * image_h)

                if self.is_transition_in_progress():
                    progress = self.get_transition_progress()
                    color = self.interpolate_color((0, 255, 0), (0, 165, 255), progress)
                else:
                    color = (0, 255, 0)
                    cv2.circle(image_drawn, (x, y), 5, color, -1)

        return image_drawn

    def process_arm_raise_events(self, landmarks, labels):
        """
        Procesa los eventos de levantamiento de brazo.

        Parámetros:
        - landmarks: Lista de landmarks de las posturas detectadas.
        - labels: Lista de etiquetas de los eventos.
        """
        # Verificar si la mano está levantada
        right_wrist = landmarks[15]
        left_wrist = landmarks[16]
        right_elbow = landmarks[11]
        left_elbow = landmarks[12]
        hand_raised = (right_wrist.y < right_elbow.y) or (left_wrist.y < left_elbow.y)

        # Actualizar el diccionario de eventos de levantamiento de brazo
        for label in labels:
            if hand_raised:
                self.participations_metrics[label] = hand_raised
                if label not in self.ongoing_events:
                    self.ongoing_events[label] = time.time()
                    self.transition_start_time = time.time()  # Iniciar la transición
            elif label in self.ongoing_events:
                del self.ongoing_events[label]

        # Verificar la duración de los eventos de levantamiento de brazo
        current_time = time.time()
        for label, start_time in list(self.ongoing_events.items()):
            if current_time - start_time > 5 and label != "Desconocido":
                self.participations[label] = time.strftime(
                    "%H:%M:%S", time.localtime(current_time)
                )  # Guarda el tiempo de asistencia
                participation = f"{label} participó a las {time.strftime('%H:%M:%S')}"
                print(participation)
                del self.ongoing_events[label]

    def is_transition_in_progress(self):
        """
        Verifica si hay una transición en progreso.

        Retorna:
        - Booleano que indica si hay una transición en progreso.
        """
        return time.time() - self.transition_start_time < self.transition_duration

    def get_transition_progress(self):
        """
        Obtiene el progreso de la transición.

        Retorna:
        - Progreso de la transición en un valor entre 0 y 1.
        """
        elapsed_time = time.time() - self.transition_start_time
        return elapsed_time / self.transition_duration

    def interpolate_color(self, color_start, color_end, progress):
        """
        Interpola un color entre dos colores base.

        Parámetros:
        - color_start: Color inicial en formato RGB.
        - color_end: Color final en formato RGB.
        - progress: Progreso de la interpolación en un valor entre 0 y 1.

        Retorna:
        - Color interpolado en formato RGB.
        """
        r = int(color_start[0] + (color_end[0] - color_start[0]) * progress)
        g = int(color_start[1] + (color_end[1] - color_start[1]) * progress)
        b = int(color_start[2] + (color_end[2] - color_start[2]) * progress)
        return (r, g, b)

    def calculate_participation_metrics(self, current_labels, previous_labels):
        """
        Calcula las métricas de participación.

        Parámetros:
        - current_labels: Diccionario de etiquetas actuales de los eventos.
        - previous_labels: Diccionario de etiquetas anteriores de los eventos.

        Retorna:
        - Diccionario con las métricas de participación.
        """
        consistent_detections = 0
        true_positives = 0
        true_negatives = 0
        false_positives = 0
        false_negatives = 0

        for label in current_labels:
            if label in previous_labels:
                if current_labels[label] == previous_labels[label]:
                    consistent_detections += 1
                    if current_labels[label]:
                        true_positives += 1
                    else:
                        true_negatives += 1
                else:
                    if current_labels[label]:
                        false_positives += 1
                    else:
                        false_negatives += 1
            else:
                if current_labels[label]:
                    false_positives += 1
                else:
                    false_negatives += 1

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0
        )
        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0
        )
        f1_score = (
            2 * (precision * recall) / (precision + recall)
            if (precision + recall) > 0
            else 0
        )

        return {
            "consistent_detections": consistent_detections,
            "true_positives": true_positives,
            "true_negatives": true_negatives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "precision": precision,
            "recall": recall,
            "f1_score": f1_score,
        }

    def get_participations(self):
        """
        Obtiene las participaciones y reinicia el diccionario.

        Retorna:
        - Diccionario con las participaciones.
        """
        res = self.participations
        self.participations = {}
        return res

    def get_participations_metrics(self):
        return self.participations_metrics
