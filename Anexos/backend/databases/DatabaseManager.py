import pymssql
import time
from config import varConfig
import threading
import datetime
from collections.abc import Iterable
import contextlib

class DatabaseManager:
    def __init__(self, isFreeDB=False):
        self.conn = None
        self.cursor = None
        self.isFreeDB = isFreeDB
        self.connect()
        
    @contextlib.contextmanager
    def get_db_connection(self):
        conn = pymssql.connect(
            server=varConfig.DBserver,
            user=varConfig.DBuser,
            password=varConfig.DBpassword,
            database=varConfig.DBname,
        )
        try:
            yield conn
        finally:
            conn.close()
        
    #Conexion al sql
    def connect(self):
        for i in range(5):
            try:
                self.conn = pymssql.connect(
                    server=varConfig.DBserver,
                    user=varConfig.DBuser,
                    password=varConfig.DBpassword,
                    database=varConfig.DBname,
                )
                self.cursor = self.conn.cursor()
                break
            except Exception as e:
                print(f"Error al conectar a la base de datos: {e}")
                time.sleep(15)
                if i >= 4:
                    self.isFreeDB = False
        # Verificar si existe un hilo con keep_alive
        for thread in threading.enumerate():
            if thread.name == "keep_alive":
                # Detener el hilo existente
                thread.stop()
        # Iniciar el hilo para ejecutar keep_alive en segundo plano
        threading.Thread(target=self.keep_alive, name="keep_alive").start()

    #Verifica si el usuario tiene permiso para registrar
    def can_register(self, admin_role, user_role):
        hierarchy = {"Dueño": 5, "Admin": 4, "Mod": 3, "Profesor": 2, "Alumno": 1}
        return hierarchy.get(admin_role, 0) > hierarchy.get(user_role, 0)

    # Verifica si el objeto es un iterable pero no una cadena.
    def is_non_string_iterable(self, obj):
        return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))

    # Serializa objetos datetime y time a una cadena de texto.
    def serialize_datetime(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            return obj.strftime("%H:%M:%S")
        return obj
    
    #Funcion para ejecutar una query
    def execute_query(self, query, params=None, fetchone=False):
        with self.get_db_connection() as conn:
            try:
                cursor = conn.cursor()
                isSelect = True if query.lower().startswith("select") else False
                cursor.execute(query, params)
                if isSelect:
                    queryRes = (
                        cursor.fetchone() if fetchone else cursor.fetchall()
                    )
                    # Verificar si hay valores datetime o time en queryRes y serializarlos
                    queryRes = [
                        self.serialize_datetime(item)
                        if isinstance(item, (datetime.datetime, datetime.time))
                        else [
                            self.serialize_datetime(sub_item)
                            if isinstance(sub_item, (datetime.datetime, datetime.time))
                            else sub_item
                            for sub_item in item
                        ]
                        if self.is_non_string_iterable(item)
                        else item
                        for item in queryRes
                    ]
                else:
                    queryRes = cursor.lastrowid if cursor.lastrowid else 0
                conn.commit()
                cursor.close()
                return queryRes
            #Reintenta la query
            except pymssql._pymssql.OperationalError as e:
                error_message = str(e)
                if "severity 9: DBPROCESS is dead or not enabled" in error_message:
                    print("Error al ejecutar la query: " + query)
                    print(e)
                    print("Reintentando conexión...")
                    with self.get_db_connection() as conn:
                        try:
                            cursor = conn.cursor()
                            isSelect = True if query.lower().startswith("select") else False
                            cursor.execute(query, params)
                            if isSelect:
                                queryRes = (
                                    cursor.fetchone()
                                    if fetchone
                                    else cursor.fetchall()
                                )
                                # Verificar si hay valores datetime o time en queryRes y serializarlos
                                queryRes = [
                                    self.serialize_datetime(item)
                                    if isinstance(item, (datetime.datetime, datetime.time))
                                    else [
                                        self.serialize_datetime(sub_item)
                                        if isinstance(
                                            sub_item, (datetime.datetime, datetime.time)
                                        )
                                        else sub_item
                                        for sub_item in item
                                    ]
                                    if self.is_non_string_iterable(item)
                                    else item
                                    for item in queryRes
                                ]
                            else:
                                queryRes = cursor.lastrowid if cursor.lastrowid else 0
                            conn.commit()
                            cursor.close()
                            return queryRes
                        except Exception as e:
                            print("Error al ejecutar la query: " + query)
                            print(e)
                            conn.rollback()
                            cursor.close()
                            raise e
                else:
                    print("Error al ejecutar la query: " + query)
                    print(e)
                    conn.rollback()
                    cursor.close()
                    raise e

    #Consigue a los usuarios dentro de las clases
    def get_user_clases(self, user_id, user_role=None):
        if user_role in ["Dueño", "Admin", "Mod"]:
            query = """SELECT 
                Clases.*, Cursos.Nombre AS NombreCurso, Profesores.Nombre AS NombreProfesor, Profesores.Apellido AS ApellidoProfesor
                FROM Clases
                INNER JOIN Cursos ON Clases.CursoID = Cursos.CursoID
                INNER JOIN Profesores ON Clases.ProfesorID = Profesores.ProfesorID
            """
            params = ()
        elif user_role == "Alumno":
            query = """SELECT 
                    Clases.*,
                    Cursos.Nombre AS NombreCurso,
                    Profesores.Nombre AS NombreProfesor,
                    Profesores.Apellido AS ApellidoProfesor
                FROM 
                    face_n_lean.dbo.Estudiantes
                INNER JOIN 
                    face_n_lean.dbo.Inscripciones ON Estudiantes.EstudianteID = Inscripciones.EstudianteID
                INNER JOIN 
                    face_n_lean.dbo.Clases ON Inscripciones.ClaseID = Clases.ClaseID
                INNER JOIN 
                    face_n_lean.dbo.Cursos ON Clases.CursoID = Cursos.CursoID
                LEFT JOIN 
                    face_n_lean.dbo.Profesores ON Clases.ProfesorID = Profesores.ProfesorID
                LEFT JOIN 
                    face_n_lean.dbo.CursoProfesores ON Clases.ClaseID = CursoProfesores.ClaseID
                LEFT JOIN 
                    face_n_lean.dbo.Profesores AS ProfesoresAdicionales ON CursoProfesores.ProfesorID = ProfesoresAdicionales.ProfesorID
                WHERE 
                    Estudiantes.AzureB2C_ID = %s;
            """
            params = (user_id,)
        elif user_role == "Profesor":
            query = """SELECT 
                    Clases.*, 
                    Cursos.Nombre AS NombreCurso, 
                    Profesores.Nombre AS NombreProfesor, 
                    Profesores.Apellido AS ApellidoProfesor
                FROM 
                    face_n_lean.dbo.Profesores
                INNER JOIN 
                    (SELECT 
                        ClaseID, CursoID, ProfesorID 
                    FROM 
                        face_n_lean.dbo.Clases
                    UNION
                    SELECT 
                        CursoProfesores.ClaseID, Clases.CursoID, CursoProfesores.ProfesorID
                    FROM 
                        face_n_lean.dbo.CursoProfesores
                    INNER JOIN 
                        face_n_lean.dbo.Clases ON CursoProfesores.ClaseID = Clases.ClaseID
                    ) AS ClasesProfesor ON Profesores.ProfesorID = ClasesProfesor.ProfesorID
                INNER JOIN 
                    face_n_lean.dbo.Clases ON ClasesProfesor.ClaseID = Clases.ClaseID
                INNER JOIN 
                    face_n_lean.dbo.Cursos ON Clases.CursoID = Cursos.CursoID
                WHERE 
                    Profesores.AzureB2C_ID = %s
            """
            params = (user_id,)
        else:
            return None

        try:
            return self.execute_query(query, params=params, fetchone=False)
        except Exception as e:
            raise e
    #Consigue el rol del usuario
    def get_user_role(self, oid):
        query = "SELECT Rol FROM OtrosUsuarios WHERE AzureB2C_ID = %s"
        params = (oid,)
        try:
            user = self.execute_query(query, params=params, fetchone=True)
            if user is not None:
                return user[0]
        except Exception as e:

            try:
                query = "SELECT * FROM Profesores WHERE AzureB2C_ID = %s"
                user = self.execute_query(query, params=params, fetchone=True)
                if user is not None:
                    return "Profesor"
            except Exception as e:

                try:
                    query = "SELECT * FROM Estudiantes WHERE AzureB2C_ID = %s"
                    user = self.execute_query(query, params=params, fetchone=True)
                    if user is not None:
                        return "Alumno"
                except Exception as e:
                    raise Exception("Usuario no encontrado: " + e)

    #Consigue a los estudiantes
    def get_students(
        self, allStudents=False, student_id=None, class_id=None, course_id=None
    ):
        if allStudents:
            query = "SELECT * FROM Estudiantes"
            params = None
        elif student_id is not None and student_id is not False:
            query = "SELECT * FROM Estudiantes WHERE AzureB2C_ID = %s"
            params = (student_id,)
        elif class_id is not None and course_id is not None:
            query = "SELECT E.* FROM Estudiantes E INNER JOIN Inscripciones I ON E.EstudianteID = I.EstudianteID INNER JOIN Clases C ON I.ClaseID = C.ClaseID INNER JOIN Cursos CR ON C.CursoID = CR.CursoID WHERE C.Nombre = %s AND CR.Nombre = %s"
            params = (class_id, course_id)
        elif course_id is not None:
            query = "SELECT E.* FROM Estudiantes E INNER JOIN Inscripciones I ON E.EstudianteID = I.EstudianteID INNER JOIN Clases C ON I.ClaseID = C.ClaseID INNER JOIN Cursos CR ON C.CursoID = CR.CursoID WHERE CR.Nombre = %s"
            params = (course_id,)
        else:
            raise Exception(
                "Se debe proporcionar al menos un parámetro para obtener estudiantes"
            )

        try:
            students = self.execute_query(query, params=params)
            return students
        except Exception as e:
            raise e
        
    def get_asistencia_por_clase(self, clase_id):
        query = "SELECT a.*, e.Nombre AS NombreEstudiante, e.Apellido AS ApellidoEstudiante FROM face_n_lean.dbo.Asistencia a INNER JOIN face_n_lean.dbo.Estudiantes e ON a.EstudianteID = e.EstudianteID WHERE a.ClaseID = %s"
        params = (clase_id)

        try:
            return self.execute_query(query, params=params)
        except Exception as e:
            raise e

    #Consigue la participacion de la clase
    def get_participacion_por_clase(self, clase_id):
        query = "SELECT p.*, e.Nombre AS NombreEstudiante, e.Apellido AS ApellidoEstudiante FROM face_n_lean.dbo.Participacion p INNER JOIN face_n_lean.dbo.Estudiantes e ON p.EstudianteID = e.EstudianteID WHERE p.ClaseID = %s"

        params = (clase_id)

        try:
            return self.execute_query(query, params=params)
        except Exception as e:
            raise e

    #Consigue a los profesores
    def get_teachers(
        self, allTeachers=False, teacher_id=None, class_id=None, course_id=None
    ):
        if allTeachers:
            query = "SELECT * FROM Profesores"
            params = None
        elif teacher_id:
            query = "SELECT * FROM Profesores WHERE AzureB2C_ID = %s"
            params = (teacher_id,)
        elif class_id and course_id:
            query = "SELECT P.* FROM Profesores P INNER JOIN CursoProfesores CP ON P.ProfesorID = CP.ProfesorID INNER JOIN Clases C ON CP.ClaseID = C.ClaseID INNER JOIN Cursos CR ON C.CursoID = CR.CursoID WHERE C.Nombre = %s AND CR.Nombre = %s"
            params = (class_id, course_id)
        elif course_id:
            query = "SELECT P.* FROM Profesores P INNER JOIN CursoProfesores CP ON P.ProfesorID = CP.ProfesorID INNER JOIN Clases C ON CP.ClaseID = C.ClaseID INNER JOIN Cursos CR ON C.CursoID = CR.CursoID WHERE CR.Nombre = %s"
            params = (course_id,)
        else:
            raise Exception(
                "Se debe proporcionar al menos un parámetro para obtener profesores"
            )

        try:
            teachers = self.execute_query(query, params=params)
            return teachers
        except Exception as e:
            raise e

    #Consigue a los profesores auxiliares
    def get_aux_profesores_clases(self):
        query = "SELECT P.*, C.ClaseID FROM Profesores P INNER JOIN CursoProfesores CP ON P.ProfesorID = CP.ProfesorID INNER JOIN Clases C ON CP.ClaseID = C.ClaseID"
        try:
            return self.execute_query(query)
        except Exception as e:
            raise e

    # Getter para clases
    def get_clases(self):
        return self.get_user_clases(user_id="id_default", user_role="Admin")

    # Getter para estudiantes
    def get_estudiantes(self):
        return self.get_students(allStudents=True)

    # Getter para profesores
    def get_profesores(self):
        return self.get_teachers(allTeachers=True)

    # Getter para auxProfesores
    def get_auxProfesores(self):
        return self.get_aux_profesores_clases()

    #Registra a los usuarios en la base de datos
    def register_user(self, user_id, user_data, user_role):
        # Verificar si el administrador tiene permiso para registrar este rol
        query = "SELECT * FROM OtrosUsuarios WHERE AzureB2C_ID = %s"
        params = (user_data["Admin_id"],)
        try:
            admin = self.execute_query(query, params=params, fetchone=True)
        except Exception as e:
            try:
                query = "SELECT * FROM Profesores WHERE AzureB2C_ID = %s"
                admin = self.execute_query(query, params=params, fetchone=True)
                if admin is not None and admin != 0:
                    admin[5] = 'Profesor'
            except Exception as e:
                raise e
        if admin and self.can_register(admin[5], user_role):
            # Crear el nuevo usuario según el rol
            if user_role == "Estudiante" or user_role == "Alumno":
                query = "INSERT INTO Estudiantes (Nombre, Apellido, CorreoElectronico, AzureB2C_ID, Matricula) VALUES (%s, %s, %s, %s, %s)"
                params = (
                    user_data["givenName"],
                    user_data["surname"],
                    user_data["identities"][0]["issuerAssignedId"],
                    user_data["AzureB2C_ID"],
                    user_id,
                )
            elif user_role == "Profesor":
                query = "INSERT INTO Profesores (Nombre, Apellido, CorreoElectronico, AzureB2C_ID, Nomina) VALUES (%s, %s, %s, %s, %s)"
                params = (
                    user_data["givenName"],
                    user_data["surname"],
                    user_data["identities"][0]["issuerAssignedId"],
                    user_data["AzureB2C_ID"],
                    user_id,
                )
            else:
                query = "INSERT INTO OtrosUsuarios (Nombre, Apellido, CorreoElectronico, AzureB2C_ID, Rol) VALUES (%s, %s, %s, %s, %s)"
                params = (
                    user_data["givenName"],
                    user_data["surname"],
                    user_data["identities"][0]["issuerAssignedId"],
                    user_data["AzureB2C_ID"],
                    user_role,
                )
            try:
                
                return self.execute_query(query, params)
            except Exception as e:
                raise e
        else:
            raise Exception(
                "El usuario administrador no tiene permiso para registrar este usuario"
            )

    #Actualiza a los usuarios
    def update_user(self, user_id, user_data, user_role):
        if user_role == "Estudiante":
            query = "UPDATE Estudiantes SET Nombre = %s, Apellido = %s, CorreoElectronico = %s, AzureB2C_ID = %s WHERE EstudianteID = %s"
            params = (
                user_data["Nombre"],
                user_data["Apellido"],
                user_data["CorreoElectronico"],
                user_data["AzureB2C_ID"],
                user_id,
            )
        elif user_role == "Profesor":
            query = "UPDATE Profesores SET Nombre = %s, Apellido = %s, CorreoElectronico = %s, AzureB2C_ID = %s WHERE ProfesorID = %s"
            params = (
                user_data["Nombre"],
                user_data["Apellido"],
                user_data["CorreoElectronico"],
                user_data["AzureB2C_ID"],
                user_id,
            )
        else:
            query = "UPDATE OtrosUsuarios SET Nombre = %s, Apellido = %s, CorreoElectronico = %s, AzureB2C_ID = %s, Rol = %s WHERE UsuarioID = %s"
            params = (
                user_data["Nombre"],
                user_data["Apellido"],
                user_data["CorreoElectronico"],
                user_data["AzureB2C_ID"],
                user_role,
                user_id,
            )
        try:
            self.execute_query(query, params)
            return user_id
        except Exception as e:
            return None

    #Elimina a los usuarios
    def delete_user(self, user_id, user_role):
        if user_role == "Estudiante":
            query = "DELETE FROM Estudiantes WHERE EstudianteID = %s"
        elif user_role == "Profesor":
            query = "DELETE FROM Profesores WHERE ProfesorID = %s"
        else:
            query = "DELETE FROM OtrosUsuarios WHERE UsuarioID = %s"
        params = (user_id,)
        try:
            # Verificar si el usuario está presente en otras tablas como clave foránea
            if user_role == "Estudiante":
                check_query = "SELECT * FROM Inscripciones WHERE EstudianteID = %s"
            elif user_role == "Profesor":
                check_query = "SELECT * FROM Clases WHERE ProfesorID = %s"
            else:
                check_query = "SELECT * FROM Clases WHERE ProfesorID = %s OR EXISTS (SELECT * FROM Inscripciones WHERE EstudianteID = %s)"
            check_params = (user_id, user_id)
            check_result = self.execute_query(
                check_query, params=check_params, fetchone=True
            )
            if check_result is not None:
                raise Exception(
                    "No se puede eliminar al usuario porque está presente en otras tablas como clave foránea"
                )
            # Eliminar al usuario
            self.execute_query(query, params)
        except Exception as e:
            raise e
        
    #Sube la foto para los alumnos
    def update_student_photo(self, student_id, photo_url, user_role, user_id=None):
        if user_role in ["Dueño", "Admin", "Mod", "Profesor"]:
            query = "UPDATE Estudiantes SET fotosRostro = %s WHERE AzureB2C_ID = %s"
            params = (photo_url, student_id)
            try:
                self.execute_query(query, params)
                return student_id
            except Exception as e:
                raise e
        elif user_role == "Alumno" and user_id == student_id:
            query = "UPDATE Estudiantes SET fotosRostro = %s WHERE AzureB2C_ID = %s"
            params = (photo_url, student_id)
            try:
                self.execute_query(query, params)
                return student_id
            except Exception as e:
                raise e
        else:
            raise Exception("No tienes permiso para actualizar la foto del estudiante")

    def keep_alive(self):
        query = "SELECT 1"
        while self.isFreeDB == True:
            self.execute_query(query)
            time.sleep(200)
            
    def insert_participacion(self, estudiante_id, clase_id, tipo_participacion, detalles):
        query = """INSERT INTO face_n_lean.dbo.Participacion (EstudianteID, ClaseID, TipoParticipacion, Detalles, [Timestamp])
                    VALUES (%s, %s, %s, %s, GETDATE())"""
        params = (estudiante_id, clase_id, tipo_participacion, detalles)
        
        try:
            self.execute_query(query, params)
        except Exception as e:
            raise e

    def insert_asistencia(self, estudiante_id, clase_id, hora_entrada, hora_salida):
        query = """INSERT INTO face_n_lean.dbo.Asistencia (EstudianteID, ClaseID, HoraEntrada, HoraSalida)
                    VALUES (%s, %s, %s, %s)"""
        params = (estudiante_id, clase_id, hora_entrada, hora_salida)
        
        try:
            self.execute_query(query, params)
        except Exception as e:
            raise e


    def calcular_asistencia_total(self, clase_id):
        query = "SELECT COUNT(*) AS TotalAsistencia FROM face_n_lean.dbo.Inscripciones i INNER JOIN face_n_lean.dbo.Asistencia a ON i.EstudianteID = a.EstudianteID WHERE i.ClaseID = %s"

        params = (clase_id)
        
        try:
            result = self.execute_query(query, params=params, fetchone=True)
            total_asistencia = result[0]
            return total_asistencia
        except Exception as e:
            raise e

    def get_numero_alumnos(self, clase_id):
        query = "SELECT COUNT(*) as NumeroDeAlumnos FROM face_n_lean.dbo.Inscripciones WHERE ClaseID = %s"
        params = (clase_id)
        try:
            result = self.execute_query(query, params=params, fetchone=True)
            numero_alumnos = result[0]
            return numero_alumnos
        except Exception as e:
            raise e
        
    def calcular_dias_habiles(self, clase_id):
        # Obtener las fechas de inicio y fin de la clase
        query_fechas = """SELECT 
        FechaInicio, FechaFin FROM face_n_lean.dbo.Clases WHERE ClaseID = %s
        """
        # Obtener los días de la semana en los que se imparte la clase
        query_dias = """SELECT 
        DiaID FROM face_n_lean.dbo.ClaseDias WHERE ClaseID = %s
        """

        try:
            fechas = self.execute_query(query_fechas, params=(clase_id,), fetchone=True)
            dias_clase = self.execute_query(query_dias, params=(clase_id,))
            
            if not fechas or not dias_clase:
                return 0

            fecha_inicio, fecha_fin = fechas
            dias_habiles = self.calcular_dias_entre_fechas(fecha_inicio, fecha_fin, [d[0] for d in dias_clase])
            return dias_habiles
        except Exception as e:
            raise e

    def calcular_dias_entre_fechas(self, fecha_inicio, fecha_fin, dias_semana):
        """
        Calcula el número de días hábiles entre dos fechas, incluyendo solo los días de la semana especificados.
        :param fecha_inicio: Fecha de inicio (datetime)
        :param fecha_fin: Fecha de fin (datetime)
        :param dias_semana: Lista de enteros representando los días de la semana (1=lunes, 7=domingo)
        :return: Número de días hábiles
        """
        
        # Convertir las fechas de string a datetime
        fecha_inicio = datetime.datetime.fromisoformat(fecha_inicio)
        fecha_fin = datetime.datetime.fromisoformat(fecha_fin)

        # Verificar que la fecha de inicio sea menor o igual a la fecha de fin
        if fecha_inicio > fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior o igual a la fecha de fin.")

        # Contador de días hábiles
        dias_habiles = 0

        # Iterar sobre cada día entre las fechas
        dia_actual = fecha_inicio
        while dia_actual <= fecha_fin:
            # Si el día de la semana del día actual está en los días hábiles, incrementar el contador
            if dia_actual.isoweekday() in dias_semana:
                dias_habiles += 1

            # Avanzar al siguiente día
            dia_actual += datetime.timedelta(days=1)

        return dias_habiles