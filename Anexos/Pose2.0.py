

import cv2
import mediapipe as mp

# Inicializar el módulo MediaPipe para la detección de manos
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

# Inicializar la captura de video (puedes cambiar '0' por el nombre del archivo de video si quieres procesar un video)
cap = cv2.VideoCapture(0)

# Configurar el modelo de MediaPipe para la detección de hombros, brazos y cara
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

    while cap.isOpened():
        ret, frame = cap.read()

        # Convertir la imagen a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Realizar la detección
        results = holistic.process(image=gray)

        # Dibujar los puntos en la cara, hombros y brazos
        if results.pose_landmarks:
            
            # Dibujar los puntos del cuerpo
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

        # Mostrar el resultado
        cv2.imshow('MediaPipe Holistic', frame)

        # Salir si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Liberar la captura y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
