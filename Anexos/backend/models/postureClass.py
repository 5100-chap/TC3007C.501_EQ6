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
                    self.ongoing_events[label] = time.time()
                    self.transition_start_time = time.time()  # Iniciar la transición
            elif label in self.ongoing_events:
                del self.ongoing_events[label]

        # Verificar la duración de los eventos de levantamiento de brazo
        current_time = time.time()
        for label, start_time in list(self.ongoing_events.items()):
            if current_time - start_time > 4 and label != "Desconocido":
                print(f"{label} participó a las {time.strftime('%H:%M:%S')}")
                del self.ongoing_events[label]

    def is_transition_in_progress(self):
        return time.time() - self.transition_start_time < self.transition_duration

    def get_transition_progress(self):
        elapsed_time = time.time() - self.transition_start_time
        return elapsed_time / self.transition_duration

    def interpolate_color(self, color_start, color_end, progress):
        r = int(color_start[0] + (color_end[0] - color_start[0]) * progress)
        g = int(color_start[1] + (color_end[1] - color_start[1]) * progress)
        b = int(color_start[2] + (color_end[2] - color_start[2]) * progress)
        return (r, g, b)
