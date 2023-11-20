import pymssql
import time
from config import varConfig
import threading
import datetime
from collections.abc import Iterable
class DatabaseManager:
    def __init__(self, isFreeDB=False):
        self.conn = None
        self.cursor = None
        self.isFreeDB = isFreeDB
        self.connect()

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

    def can_register(self, admin_role, user_role):
        hierarchy = {"Dueño": 5, "Admin": 4, "Mod": 3, "Profesor": 2, "Alumno": 1}
        return hierarchy.get(admin_role, 0) > hierarchy.get(user_role, 0)
    
    #Verifica si el objeto es un iterable pero no una cadena.
    def is_non_string_iterable(self, obj):
        return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))
    
    # Serializa objetos datetime y time a una cadena de texto.
    def serialize_datetime(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, datetime.time):
            return obj.strftime('%H:%M:%S')
        return obj

    def execute_query(self, query, params=None, fetchone=False):
        try:
            isSelect = True if query.lower().startswith("select") else False
            self.cursor.execute(query, params)
            if isSelect:
                queryRes = self.cursor.fetchone() if fetchone else self.cursor.fetchall()
                # Verificar si hay valores datetime o time en queryRes y serializarlos
                queryRes = [self.serialize_datetime(item) if isinstance(item, (datetime.datetime, datetime.time)) 
                else [self.serialize_datetime(sub_item) if isinstance(sub_item, (datetime.datetime, datetime.time)) else sub_item for sub_item in item] 
                if self.is_non_string_iterable(item) else item for item in queryRes]
            else:
                queryRes = 0
            self.conn.commit()
            return queryRes

        except pymssql._pymssql.OperationalError as e:
            error_message = str(e)
            if "severity 9: DBPROCESS is dead or not enabled" in error_message:
                print("Error al ejecutar la query: " + query)
                print(e)
                print("Reintentando conexión...")
                self.connect()
                try:
                    isSelect = True if query.lower().startswith("select") else False
                    self.cursor.execute(query, params)
                    if isSelect:
                        queryRes = self.cursor.fetchone() if fetchone else self.cursor.fetchall()
                        # Verificar si hay valores datetime o time en queryRes y serializarlos
                        queryRes = [self.serialize_datetime(item) if isinstance(item, (datetime.datetime, datetime.time)) 
                        else [self.serialize_datetime(sub_item) if isinstance(sub_item, (datetime.datetime, datetime.time)) else sub_item for sub_item in item] 
                        if self.is_non_string_iterable(item) else item for item in queryRes]
                    else:
                        queryRes = 0
                    self.conn.commit()
                    return queryRes
                except Exception as e:
                    print("Error al ejecutar la query: " + query)
                    print(e)
                    self.conn.rollback()
                    raise e
            else:
                print("Error al ejecutar la query: " + query)
                print(e)
                self.conn.rollback()
                raise e



    def get_user_clases(self, user_id, user_role = None):
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

    def register_user(self, user_id, user_data, user_role):
        # Verificar si el administrador tiene permiso para registrar este rol
        query = "SELECT * FROM OtrosUsuarios WHERE AzureB2C_ID = %s"
        params = (user_data["Admin_id"],)
        try:
            admin = self.execute_query(query, params=params, fetchone=True)
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
                self.execute_query(query, params)
                return self.cursor.lastrowid
            except Exception as e:
                raise e
        else:
            raise Exception(
                "El usuario administrador no tiene permiso para registrar este usuario"
            )

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

    def delete_user(self, user_id, user_role):
        if user_role == "Estudiante":
            query = "DELETE FROM Estudiante WHERE EstudianteID = %s"
        elif user_role == "Profesor":
            query = "DELETE FROM Profesor WHERE ProfesorID = %s"
        else:
            query = "DELETE FROM OtrosUsuarios WHERE UsuarioID = %s"
        params = (user_id,)
        try:
            self.execute_query(query, params)
        except Exception as e:
            raise e

    def get_user_role(self, oid):
        query = "SELECT Rol FROM OtrosUsuarios WHERE AzureB2C_ID = %s"
        params = (oid,)
        try:
            user = self.execute_query(query, params=params, fetchone=True)
            if user is not None:
                return user[0]
            else:
                query = "SELECT * FROM Profesores WHERE AzureB2C_ID = %s"
                user = self.execute_query(query, params=params, fetchone=True)
                if user is not None:
                    return 'Profesor'
                else:
                    query = "SELECT * FROM Estudiantes WHERE AzureB2C_ID = %s"
                    user = self.execute_query(query, params=params, fetchone=True)
                    if user is not None:
                        return 'Alumno'
                    else:
                        raise Exception("Usuario no encontrado")
        except Exception as e:
            raise e

    def get_students(self, allStudents=False, student_id=None, class_id=None, course_id=None):
        if allStudents:
            query = "SELECT * FROM Estudiantes"
            params = None
        elif student_id:
            query = "SELECT * FROM Estudiantes WHERE AzureB2C_ID = %s"
            params = (student_id,)
        elif class_id and course_id:
            query = "SELECT E.* FROM Estudiantes E INNER JOIN Inscripciones I ON E.EstudianteID = I.EstudianteID INNER JOIN Clases C ON I.ClaseID = C.ClaseID INNER JOIN Cursos CR ON C.CursoID = CR.CursoID WHERE C.Nombre = %s AND CR.Nombre = %s"
            params = (class_id, course_id)
        elif course_id:
            query = "SELECT E.* FROM Estudiantes E INNER JOIN Inscripciones I ON E.EstudianteID = I.EstudianteID INNER JOIN Clases C ON I.ClaseID = C.ClaseID INNER JOIN Cursos CR ON C.CursoID = CR.CursoID WHERE CR.Nombre = %s"
            params = (course_id,)
        else:
            raise Exception("Se debe proporcionar al menos un parámetro para obtener estudiantes")
        
        try:
            students = self.execute_query(query, params=params)
            return students
        except Exception as e:
            raise e

    def update_student_photo(self, student_id, photo_url, user_role, user_id = None):
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
