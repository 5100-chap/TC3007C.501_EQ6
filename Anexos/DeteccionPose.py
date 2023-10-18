import cv2
import mediapipe as mp

# Inicializar el módulo Pose de Mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Función para verificar si el brazo está alzado
def is_arm_raised(landmarks):
    shoulder_x = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x
    wrist_y = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y
    hip_y = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y
    
    # Verificar si el brazo está alzado (en este caso, el brazo izquierdo)
    if wrist_y < shoulder_x and wrist_y < hip_y:
        return True
    else:
        return False

# Inicializar la captura de video (0 para la cámara predeterminada)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir la imagen a escala de grises
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    
    # Verificar si el brazo está alzado y mostrar un mensaje en la pantalla
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        if is_arm_raised(landmarks):
            cv2.putText(frame, 'Brazo Alzado', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'Brazo Abajo', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Mostrar el frame con las anotaciones
    cv2.imshow('Brazo Detector', frame)

    # Romper el bucle si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()

    
