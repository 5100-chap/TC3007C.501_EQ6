import pymssql
import time
from config import varConfig
from models import DBmodels
import threading


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

    def execute_query(self, query, params=None, fetchone=False):
        try:
            isSelect = True if query.lower().startswith("select") else False
            self.cursor.execute(query, params)
            if isSelect:
                queryRes = self.cursor.fetchone() if fetchone else self.cursor.fetchall()
            else:
                queryRes = 0
            self.conn.commit()
            return queryRes

        except pymssql._pymssql.OperationalError as e:
            error_message = str(e)
            if "severity 9: DBPROCESS is dead or not enabled" in error_message:
                print("Error al ejecutar la query: " + query)
                print("Error: " + e)
                print("Reintentando conexión...")
                self.connect()
                try:
                    isSelect = True if query.lower().startswith("select") else False
                    self.cursor.execute(query, params)
                    if isSelect:
                        queryRes = self.cursor.fetchone() if fetchone else self.cursor.fetchall()
                    else:
                        queryRes = 0
                    self.conn.commit()
                    return queryRes
                except Exception as e:
                    print("Error al ejecutar la query: " + query)
                    print("Error: " + e)
                    self.conn.rollback()
                    raise e
            else:
                print("Error al ejecutar la query: " + query)
                print("Error: " + e)
                raise e

    def register_user(self, user_id, user_data, user_role):
        # Verificar si el administrador tiene permiso para registrar este rol
        query = "SELECT * FROM OtrosUsuarios WHERE AzureB2C_ID = %s"
        params = (user_data["Admin_id"],)
        try:
            admin = self.execute_query(query, params=params, fetchone=True)
        except Exception as e:
            print("Error al ejecutar la query: " + query)
            print("Error: " + e)
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
                print("Error al ejecutar la query: " + query)
                print("Error: " + e)
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
            print("Error al ejecutar la query: " + query)
            print("Error: " + e)
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
            print("Error al ejecutar la query: " + query)
            print("Error: " + e)

    def get_user_role(self, email):
        query = "SELECT Rol FROM OtrosUsuarios WHERE CorreoElectronico = %s"
        params = (email)
        try:
            user = self.execute_query(query, params=params, fetchone=True)
            if user != None:
                return user[0]
            else:
                raise Exception("Usuario no encontrado")
        except Exception as e:
            print("Error al ejecutar la query: " + query)
            print("Error: " + e)
            return None

    def keep_alive(self):
        query = "SELECT 1"
        while self.isFreeDB == True:
            self.execute_query(query)
            time.sleep(200)
