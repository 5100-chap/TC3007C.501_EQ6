#IMPORTAR RECURSOS NECESARIOS.
import cv2
import mediapipe as mp

#INICIAR SISTEMA DE DETECCIÓN.
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#INICIAR CAMARA
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    #COMPROBAR ENTRADA
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue
    #CONVERTIR IMAGEN A RGB
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    #DIBUJAR PUNTOS DE DETECCIÓN
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        #print("HAND LANDMARKS: ",hand_landmarks)
        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
