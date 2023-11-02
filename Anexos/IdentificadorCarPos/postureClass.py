import cv2
import mediapipe as mp


class PostureClass:
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.pose = self.mp_pose.Pose()

    def detect_arms(self, frame):
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.pose.process(image_rgb)
        image_drawn = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark
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

    def check_hand_raised(self, landmarks):
        # Suponiendo que landmarks[15] y landmarks[16] corresponden a las muñecas derecha e izquierda
        # y landmarks[11] y landmarks[12] corresponden a los codos derecho e izquierdo.
        # Ajusta los índices según la documentación de MediaPipe.
        right_wrist = landmarks[15]
        left_wrist = landmarks[16]
        right_elbow = landmarks[11]
        left_elbow = landmarks[12]

        # Comprobar si alguna muñeca está por encima del codo correspondiente
        hand_raised = (right_wrist.y < right_elbow.y) or (left_wrist.y < left_elbow.y)
        return hand_raised
