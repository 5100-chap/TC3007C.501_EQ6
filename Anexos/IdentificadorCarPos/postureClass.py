import cv2
import mediapipe as mp
import time


class PostureClass:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()
        self.ongoing_events = (
            {}
        )  # Añadir un diccionario para mantener los eventos de levantamiento de brazo

    def detect_arms(self, frame, labels):
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
                # Convertir las coordenadas normalizadas a coordenadas de píxeles
                image_h, image_w, _ = frame.shape
                x = int(landmark.x * image_w)
                y = int(landmark.y * image_h)
                # Dibujar un círculo en cada landmark de interés
                cv2.circle(image_drawn, (x, y), 5, (0, 255, 0), -1)

        return image_drawn

    def process_arm_raise_events(self, landmarks, labels):
        # Verificar si la mano está levantada
        right_wrist = landmarks[15]
        left_wrist = landmarks[16]
        right_elbow = landmarks[11]
        left_elbow = landmarks[12]
        hand_raised = (right_wrist.y < right_elbow.y) or (left_wrist.y < left_elbow.y)

        # Actualizar el diccionario de eventos de levantamiento de brazo
        for label in labels:
            if hand_raised:
                if label not in self.ongoing_events:
                    self.ongoing_events[
                        label
                    ] = time.time()  # Guardar el tiempo inicial del evento
            elif label in self.ongoing_events:
                del self.ongoing_events[
                    label
                ]  # Eliminar el evento si la mano ya no está levantada

        # Verificar la duración de los eventos de levantamiento de brazo
        current_time = time.time()
        for label, start_time in list(self.ongoing_events.items()):
            if current_time - start_time > 4:
                print(f"{label} participó a las {time.strftime('%H:%M:%S')}")
                del self.ongoing_events[label]  # El
