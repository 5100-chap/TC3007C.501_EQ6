import cv2
import os
import face_recognition
import mediapipe as mp

# Inicializar la captura de video
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Detector facial
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Inicializar el modelo de MediaPipe para la detección de hombros, brazos y cara
holistic = mp.solutions.holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Inicializar el módulo MediaPipe para la detección de manos y rostros
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic


# Rutas de las imágenes de los rostros conocidos
imageFacesPath = "C:/Users/usuario/Documents/GitHub/hand-deteccion/faces"

# Codificar los rostros conocidos
facesEncodings = []
facesNames = []
for file_name in os.listdir(imageFacesPath):
    image = cv2.imread(os.path.join(imageFacesPath, file_name))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Intentar encontrar rostros en la imagen
    face_locations = face_recognition.face_locations(image)
    if face_locations:
        # Codificar el primer rostro encontrado en la imagen
        f_coding = face_recognition.face_encodings(image, known_face_locations=[face_locations[0]])[0]
        facesEncodings.append(f_coding)
        facesNames.append(file_name.split(".")[0])
    else:
        print(f"No se encontraron rostros en {file_name}")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    orig = frame.copy()

    # Detección facial con Haar cascades
    faces = faceClassif.detectMultiScale(frame, 1.1, 5)

    for (x, y, w, h) in faces:
        face = orig[y:y + h, x:x + w]
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        
        # Intentar encontrar rostros en el cuadro actual
        face_locations = face_recognition.face_locations(face)
        if face_locations:
            # Codificar el primer rostro encontrado en el cuadro actual
            actual_face_encoding = face_recognition.face_encodings(face, known_face_locations=[face_locations[0]])[0]
            result = face_recognition.compare_faces(facesEncodings, actual_face_encoding)

            if True in result:
                index = result.index(True)
                name = facesNames[index]
                color = (125, 220, 0)
            else:
                name = "Desconocido"
                color = (50, 50, 255)

            cv2.rectangle(frame, (x, y + h), (x + w, y + h + 30), color, -1)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, name, (x, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Detección de hombros, brazos y cara con MediaPipe
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = holistic.process(image=gray)

    if results.pose_landmarks:
        # Dibujar los puntos del cuerpo
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

    # Mostrar el resultado
    cv2.imshow("Frame", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
