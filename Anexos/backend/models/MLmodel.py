import os
from models.faceClass import FaceClass
from models.postureClass import PostureClass
import cv2
import os
import datetime
import urllib.request
import time

class MLmodel:
    def __init__(self, db_manager):
        """
        Constructor de la clase MLmodel.

        Parámetros:
        - db_manager: objeto que maneja la conexión con la base de datos.
        """
        self.posture_class = PostureClass()
        self.db_manager = db_manager
        self.estudiantes_foto = {}
        self.estudiantes = self.db_manager.get_estudiantes()
        self.clases = self.db_manager.get_clases()
        self.asistencias = None
        self.participaciones = None
        
        # Añadir estructuras para acumular métricas
        self.total_face_metrics = {
            "true_positives": 0, "true_negatives": 0, 
            "false_positives": 0, "false_negatives": 0, 
            "precision": [], "recall": [], "f1_score": []
        }
        self.total_posture_metrics = {
            "true_positives": 0, "true_negatives": 0, 
            "false_positives": 0, "false_negatives": 0, 
            "precision": [], "recall": [], "f1_score": []
        }


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
        
    def update_metrics(self, total_metrics, new_metrics):
        """
        Actualiza las métricas totales con las nuevas métricas.

        Parámetros:
        - total_metrics: diccionario con las métricas totales.
        - new_metrics: diccionario con las nuevas métricas a agregar.
        """
        for key in total_metrics:
            if key in ["precision", "recall", "f1_score"]:
                total_metrics[key].append(new_metrics[key])
            else:
                total_metrics[key] += new_metrics[key]
                    
    def calculate_final_metrics(self, metrics):
        """
        Calcula las métricas finales a partir de las métricas acumuladas.

        Parámetros:
        - metrics: diccionario con las métricas acumuladas.

        Retorna:
        - final_metrics: diccionario con las métricas finales calculadas.
        """
        final_metrics = {}
        for key, values in metrics.items():
            if isinstance(values, list):
                final_metrics[key] = sum(values) / len(values) if values else 0
            else:
                final_metrics[key] = values
        return final_metrics
    
    def print_final_metrics(self):
        """
        Imprime las métricas finales de detección de rostros y posturas.
        """
        # Calcular métricas finales para rostros
        final_face_metrics = self.calculate_final_metrics(self.total_face_metrics)
        print("Final Face Detection Metrics:")
        for metric, value in final_face_metrics.items():
            print(f"{metric}: {value}")

        # Calcular métricas finales para posturas
        final_posture_metrics = self.calculate_final_metrics(self.total_posture_metrics)
        print("Final Posture Detection Metrics:")
        for metric, value in final_posture_metrics.items():
            print(f"{metric}: {value}")



    def agregar_participaciones(self, selected_course=None):
        """
        Agrega las participaciones de los estudiantes en las clases.

        Parámetros:
        - selected_course: identificador del curso seleccionado (opcional).

        Retorna:
        - participaciones_registradas: número de participaciones registradas.
        """
        participaciones_registradas = 0
        clases_dict = {clase[0]: clase for clase in self.clases}
        for estudiante_id, hora_participacion_str in self.participaciones.items():
            hora_participacion = datetime.datetime.strptime(
                hora_participacion_str, "%H:%M:%S"
            ).time()
            clases_a_procesar = [clases_dict[selected_course]] if selected_course is not None else self.clases
            for clase in clases_a_procesar:
                clase_id = clase[0]
                if selected_course is not None and clase_id != selected_course:
                    continue
                hora_inicio = datetime.datetime.strptime(clase[6], "%H:%M:%S").time()
                hora_fin = datetime.datetime.strptime(clase[7], "%H:%M:%S").time()
                fecha_inicio = datetime.datetime.strptime(
                    clase[4], "%Y-%m-%dT%H:%M:%S"
                ).date()
                fecha_fin = datetime.datetime.strptime(
                    clase[5], "%Y-%m-%dT%H:%M:%S"
                ).date()

                if (
                    fecha_inicio <= datetime.date.today() <= fecha_fin
                    and hora_inicio <= hora_participacion <= hora_fin
                ):
                    estudiante = next(
                        (est for est in self.estudiantes if est[-2] == estudiante_id),
                        None,
                    )
                    if estudiante:
                        estudianteid = estudiante[0]
                        self.db_manager.insert_participacion(
                            estudianteid,
                            clase_id,
                            "Alzada de mano",
                            "Captada en camara en vivo",
                        )
                        participaciones_registradas += 1
        return participaciones_registradas

    def procesar_y_registrar_asistencias(self, selected_course= None):
        """
        Procesa y registra las asistencias de los estudiantes en las clases.

        Parámetros:
        - selected_course: identificador del curso seleccionado (opcional).

        Retorna:
        - nuevas_asistencias_reg: número de nuevas asistencias registradas.
        """
        nuevas_asistencias_reg = 0
        clases_dict = {clase[0]: clase for clase in self.clases}
        # Leer y filtrar el archivo de texto para obtener asistencias ya registradas
        txt_file_path = os.path.join(self.face_dir, "asistencias_registradas.txt")
        asistencias_registradas = set()
        if os.path.exists(txt_file_path):
            with open(txt_file_path, "r") as file:
                for line in file:
                    partes = line.split(", ")
                    estudiante_id_registrado = partes[0]
                    clase_id_registrado = partes[2].split(": ")[1]
                    fecha_registrada = partes[3].split(": ")[1].strip()

                    asistencias_registradas.add(
                        (estudiante_id_registrado, clase_id_registrado, fecha_registrada)
                    )
                    
        # Procesar asistencias
        for estudiante_id, hora_asistencia_str in self.asistencias:
            hora_asistencia = datetime.datetime.strptime(
                hora_asistencia_str, "%H:%M:%S"
            ).time()
            clases_a_procesar = [clases_dict[selected_course]] if selected_course is not None else self.clases
            for clase in clases_a_procesar:
                (
                    clase_id,
                    curso_id,
                    _,
                    _,
                    fecha_inicio_str,
                    fecha_fin_str,
                    hora_inicio_str,
                    hora_fin_str,
                ) = clase[:8]
                if selected_course is not None and clase_id != selected_course:
                    continue
                fecha_inicio = datetime.datetime.strptime(
                    fecha_inicio_str, "%Y-%m-%dT%H:%M:%S"
                ).date()
                fecha_fin = datetime.datetime.strptime(
                    fecha_fin_str, "%Y-%m-%dT%H:%M:%S"
                ).date()
                hora_inicio = datetime.datetime.strptime(
                    hora_inicio_str, "%H:%M:%S"
                ).time()
                hora_fin = datetime.datetime.strptime(hora_fin_str, "%H:%M:%S").time()
                if (
                    fecha_inicio <= datetime.date.today() <= fecha_fin
                    and hora_inicio <= hora_asistencia <= hora_fin
                    and (estudiante_id, str(clase_id), str(datetime.date.today()))
                    not in asistencias_registradas
                ):
                    estudiante = next(
                        (est for est in self.estudiantes if est[-2] == estudiante_id),
                        None,
                    )
                    if estudiante:
                        estudianteid = estudiante[0]
                        fecha_actual = datetime.datetime.now()
                        dia_asistencia = datetime.datetime.combine(
                            fecha_actual.date(), hora_asistencia
                        )
                        self.db_manager.insert_asistencia(
                            estudianteid,
                            clase_id,
                            dia_asistencia.strftime("%Y-%m-%d %H:%M:%S"),
                            fecha_actual.strftime("%Y-%m-%d %H:%M:%S"),
                        )
                        nuevas_asistencias_reg += 1

                        # Agregar la nueva asistencia al archivo de texto
                        with open(txt_file_path, "a") as file:
                            file.write(
                                f"{estudiante_id}, CursoID: {curso_id}, ClaseID: {clase_id}, Fecha: {datetime.date.today()}\n"
                            )
        return nuevas_asistencias_reg

    def process_video(self, video):
        """
        Procesa un video y realiza la detección de rostros y posturas.

        Parámetros:
        - video: ruta del archivo de video a procesar.
        """
        frame_count = 0
        cap = cv2.VideoCapture(video)
        start_time = time.time()
        previous_labels = []
        previous_poses = {}  # Inicializar como un diccionario vacío
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break
            frame_count += 1
            # ... Procesamiento del frame ...

            total_time = time.time() - start_time
            fps = frame_count / total_time
            print(f"Tiempo total de procesamiento: {total_time} segundos, FPS: {fps}")

            frame = cv2.flip(frame, 1)

            face_locations, labels = self.face_class.recognize_faces(frame)
            
            metrics_face = self.face_class.calculate_detection_metrics(labels)
            self.update_metrics(self.total_face_metrics, metrics_face)
            
            self.face_class.register_attendance(labels)
            frame = self.face_class.draw_faces(frame, face_locations, labels)
            
            current_poses = self.posture_class.get_participations_metrics()
            # Calcula las métricas de participación
            image_drawn = self.posture_class.detect_arms(frame, labels)
            # Llamada a la función de métricas
            metrics_pose = self.posture_class.calculate_participation_metrics(current_poses, previous_poses)
            self.update_metrics(self.total_posture_metrics, metrics_pose)
            
            metrics = {**metrics_face, **metrics_pose}
            # Imprimir las métricas
            for metric, value in metrics.items():
                print(f"{metric}: {value}")

            previous_poses = current_poses.copy()

            cv2.imshow("Frame", image_drawn)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                self.print_final_metrics()
                break

        cap.release()
        cv2.destroyAllWindows()

    def process_image(self, image, rol, submit=False, selected_course=None):
        """
        Procesa una imagen y realiza el reconocimiento de rostros.

        Parámetros:
        - image: imagen de entrada en formato OpenCV (ndarray de NumPy).
        - rol: rol del usuario que realiza el procesamiento.
        - submit: indica si se debe enviar el resultado a la base de datos (opcional).
        - selected_course: identificador del curso seleccionado (opcional).
        """
        # Asumimos que 'image' es una imagen de OpenCV (un ndarray de NumPy)

        # Paso 1: Reconocimiento de Rostros
        # ...
        face_locations, labels = self.face_class.recognize_faces(image)
        self.face_class.register_attendance(labels)
        image_with_faces = self.face_class.draw_faces(image, face_locations, labels)

        # Paso 2: Detección de Posturas
        image_with_posture = self.posture_class.detect_arms(image_with_faces, labels) if rol != 'Alumno' else {}

        # Paso 3: Preparar los resultados
        # Aquí puedes incluir cualquier información adicional que quieras devolver,
        # como estadísticas, etiquetas de rostros detectados, etc.

        if submit:
            # Llamada para que suba todo a la base de datos
            self.participaciones = self.posture_class.get_participations() if rol != 'Alumno' else 0
            self.asistencias = self.face_class.get_attendance_label()
            num_part = self.agregar_participaciones(selected_course) if rol != 'Alumno' else 0
            num_asis = self.procesar_y_registrar_asistencias(selected_course)
            results = {
                "is_finished": True,
                "detected_faces": num_part,
                "detected_participants": num_asis,
            }
            return image_with_posture if rol != 'Alumno' else image_with_faces, results
        else:
            # Devolver la imagen procesada y los resultados
            return image_with_posture if rol != 'Alumno' else image_with_faces, {
                "is_finished": False,
                "detected_faces": 0,
                "detected_participants": 0
            }
