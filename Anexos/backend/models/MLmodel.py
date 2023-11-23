import os
from models.faceClass import FaceClass
from models.postureClass import PostureClass
import cv2
import os
import datetime
import urllib.request


class MLmodel:
    def __init__(self, db_manager):
        self.posture_class = PostureClass()
        self.db_manager = db_manager
        self.estudiantes_foto = {}
        self.estudiantes = self.db_manager.get_estudiantes()
        self.clases = self.db_manager.get_clases()
        self.asistencias = None
        self.participaciones = None

        # Obtener la ruta absoluta del archivo actual
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Unir la ruta actual con la carpeta "faces"
        faces_dir = os.path.join(current_dir, "faces")

        # Si no existe la carpeta, creala
        if not os.path.exists(faces_dir):
            os.makedirs(faces_dir)

        for estudiante in self.estudiantes:
            matricula = estudiante[-2]
            imagen_url = estudiante[-1]

            if imagen_url:
                imagen_path = os.path.join(faces_dir, f"{matricula}.jpg")

                # Descargar la imagen y guardarla en la carpeta correspondiente
                urllib.request.urlretrieve(imagen_url, imagen_path)
        # Se crea una instancia de la clase FaceClass
        self.face_class = FaceClass(faces_dir)
        self.face_dir = faces_dir
        
    def agregar_participaciones(self):
        for estudiante_id, hora_participacion_str in self.participaciones.items():
            hora_participacion = datetime.datetime.strptime(hora_participacion_str, "%H:%M:%S").time()
            for clase in self.clases:
                clase_id = clase[0]
                hora_inicio = datetime.datetime.strptime(clase[6], "%H:%M:%S").time()
                hora_fin = datetime.datetime.strptime(clase[7], "%H:%M:%S").time()
                fecha_inicio = datetime.datetime.strptime(clase[4], "%Y-%m-%dT%H:%M:%S").date()
                fecha_fin = datetime.datetime.strptime(clase[5], "%Y-%m-%dT%H:%M:%S").date()

                if fecha_inicio <= datetime.date.today() <= fecha_fin and hora_inicio <= hora_participacion <= hora_fin:
                    estudiante = next((est for est in self.estudiantes if est[-2] == estudiante_id), None)
                    if estudiante:
                        estudianteid = estudiante[0]
                        self.db_manager.insert_participacion(estudianteid, clase_id, "Alzada de mano", "Captada en camara en vivo")
    
    def procesar_y_registrar_asistencias(self):
        # Leer y filtrar el archivo de texto para obtener asistencias ya registradas
        txt_file_path = os.path.join(self.face_dir, "asistencias_registradas.txt")
        asistencias_registradas = set()
        if os.path.exists(txt_file_path):
            with open(txt_file_path, "r") as file:
                for line in file:
                    estudiante_id_registrado, _, clase_id_registrado, _, fecha_registrada = line.split(', ')
                    asistencias_registradas.add((estudiante_id_registrado, clase_id_registrado, fecha_registrada.strip()))

        # Procesar asistencias
        for estudiante_id, hora_asistencia_str in self.asistencias:
            hora_asistencia = datetime.datetime.strptime(hora_asistencia_str, "%H:%M:%S").time()
            for clase in self.clases:
                clase_id, curso_id, _, _, fecha_inicio_str, fecha_fin_str, hora_inicio_str, hora_fin_str = clase[:8]
                fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, "%Y-%m-%dT%H:%M:%S").date()
                fecha_fin = datetime.datetime.strptime(fecha_fin_str, "%Y-%m-%dT%H:%M:%S").date()
                hora_inicio = datetime.datetime.strptime(hora_inicio_str, "%H:%M:%S").time()
                hora_fin = datetime.datetime.strptime(hora_fin_str, "%H:%M:%S").time()

                if (fecha_inicio <= datetime.date.today() <= fecha_fin and 
                    hora_inicio <= hora_asistencia <= hora_fin and
                    (estudiante_id, str(clase_id), str(datetime.date.today())) not in asistencias_registradas):
                    
                    estudiante = next((est for est in self.estudiantes if est[-2] == estudiante_id), None)
                    if estudiante:
                        estudianteid = estudiante[0]
                        
                        self.db_manager.insert_asistencia(estudianteid, clase_id, hora_asistencia_str, hora_asistencia_str)

                        # Agregar la nueva asistencia al archivo de texto
                        with open(txt_file_path, "a") as file:
                            file.write(f"{estudiante_id}, CursoID: {curso_id}, ClaseID: {clase_id}, Fecha: {datetime.date.today()}\n")

    def process_video(self, video):
        cap = cv2.VideoCapture(video)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            frame = cv2.flip(frame, 1)

            face_locations, labels = self.face_class.recognize_faces(frame)
            self.face_class.register_attendance(labels)

            frame = self.face_class.draw_faces(frame, face_locations, labels)
            image_drawn = self.posture_class.detect_arms(frame, labels)

            cv2.imshow("Frame", image_drawn)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    def process_image(self, image, submit=False, selected_course=None):
        # Asumimos que 'image' es una imagen de OpenCV (un ndarray de NumPy)

        # Paso 1: Reconocimiento de Rostros
        face_locations, labels = self.face_class.recognize_faces(image)
        self.face_class.register_attendance(labels)
        image_with_faces = self.face_class.draw_faces(image, face_locations, labels)

        # Paso 2: Detección de Posturas
        image_with_posture = self.posture_class.detect_arms(image_with_faces, labels)

        # Paso 3: Preparar los resultados
        # Aquí puedes incluir cualquier información adicional que quieras devolver,
        # como estadísticas, etiquetas de rostros detectados, etc.
        results = {
            "detected_faces": len(face_locations),
            "detected_labels": labels,
            # ... otros resultados ...
        }

        if submit:
            # Llamada para que suba todo a la base de datos
            self.participaciones = self.posture_class.get_participations()
            self.asistencias = self.face_class.get_attendance_label()
            self.agregar_participaciones()
            self.procesar_y_registrar_asistencias()
            return image_with_posture, results
        else:
            # Devolver la imagen procesada y los resultados
            return image_with_posture, results
