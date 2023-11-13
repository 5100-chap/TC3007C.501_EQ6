import pymssql
import time
from config import varConfig
from models import DBmodels


class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
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

    def can_register(self, admin_role, user_role):
        hierarchy = {"Dueño": 5, "Admin": 4, "Mod": 3, "Profesor": 2, "Alumno": 1}
        return hierarchy.get(admin_role, 0) > hierarchy.get(user_role, 0)

    def execute_query(self, query, params=None, fetchone=False):
        try:
            self.cursor.execute(query, params)
            if fetchone:
                queryRes = self.cursor.fetchone()
            else:
                queryRes = self.cursor.fetchall()
            self.conn.commit()
            return queryRes
        except pymssql._pymssql.OperationalError as e:
            print(f"Error al ejecutar la query: {query}")
            print(f"Error: {e}")
            print("Reintentando conexión...")
            self.connect()
            try:
                self.cursor.execute(query, params)
                self.conn.commit()
                if fetchone:
                    return self.cursor.fetchone()
                else:
                    return self.cursor.fetchall()
            except Exception as e:
                print(f"Error al ejecutar la query: {query}")
                print(f"Error: {e}")
                self.conn.rollback()
                return None

    def register_user(self, admin_id, user_data, user_role):
        # Verificar si el administrador tiene permiso para registrar este rol
        self.cursor.execute(
            "SELECT * FROM OtrosUsuarios WHERE UsuarioID = ?", (admin_id,)
        )
        admin = self.cursor.fetchone()
        if admin and self.can_register(admin[5], user_role):
            # Crear el nuevo usuario según el rol
            if user_role == "Estudiante":
                query = "INSERT INTO Estudiantes (Nombre, Apellido, CorreoElectronico, AzureB2C_ID, Matricula) VALUES (?, ?, ?, ?, ?)"
                params = (
                    user_data["Nombre"],
                    user_data["Apellido"],
                    user_data["CorreoElectronico"],
                    user_data["AzureB2C_ID"],
                    user_data["Matricula"],
                )
            elif user_role == "Profesor":
                query = "INSERT INTO Profesores (Nombre, Apellido, CorreoElectronico, AzureB2C_ID, Nomina) VALUES (?, ?, ?, ?, ?)"
                params = (
                    user_data["Nombre"],
                    user_data["Apellido"],
                    user_data["CorreoElectronico"],
                    user_data["AzureB2C_ID"],
                    user_data["Nomina"],
                )
            else:
                query = "INSERT INTO OtrosUsuarios (Nombre, Apellido, CorreoElectronico, AzureB2C_ID, Rol) VALUES (?, ?, ?, ?, ?)"
                params = (
                    user_data["Nombre"],
                    user_data["Apellido"],
                    user_data["CorreoElectronico"],
                    user_data["AzureB2C_ID"],
                    user_role,
                )
            try:
                self.execute_query(query, params)
                return self.cursor.lastrowid
            except Exception as e:
                print(f"Error al ejecutar la query: {query}")
                print(f"Error: {e}")
                return None
        else:
            raise Exception(
                "El usuario administrador no tiene permiso para registrar este usuario"
            )

    def update_user(self, user_id, user_data, user_role):
        if user_role == "Estudiante":
            query = "UPDATE Estudiantes SET Nombre = ?, Apellido = ?, CorreoElectronico = ?, AzureB2C_ID = ? WHERE EstudianteID = ?"
            params = (
                user_data["Nombre"],
                user_data["Apellido"],
                user_data["CorreoElectronico"],
                user_data["AzureB2C_ID"],
                user_id,
            )
        elif user_role == "Profesor":
            query = "UPDATE Profesores SET Nombre = ?, Apellido = ?, CorreoElectronico = ?, AzureB2C_ID = ? WHERE ProfesorID = ?"
            params = (
                user_data["Nombre"],
                user_data["Apellido"],
                user_data["CorreoElectronico"],
                user_data["AzureB2C_ID"],
                user_id,
            )
        else:
            query = "UPDATE OtrosUsuarios SET Nombre = ?, Apellido = ?, CorreoElectronico = ?, AzureB2C_ID = ?, Rol = ? WHERE UsuarioID = ?"
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
            print(f"Error al ejecutar la query: {query}")
            print(f"Error: {e}")
            return None

    def delete_user(self, user_id, user_role):
        if user_role == "Estudiante":
            query = f"DELETE FROM Estudiante WHERE EstudianteID = {user_id}"
        elif user_role == "Profesor":
            query = f"DELETE FROM Profesor WHERE ProfesorID = {user_id}"
        else:
            query = f"DELETE FROM OtrosUsuarios WHERE UsuarioID = {user_id}"
        try:
            self.execute_query(query)
        except Exception as e:
            print(f"Error al ejecutar la query: {query}")
            print(f"Error: {e}")

    def get_user_role(self, email):
        query = "SELECT Rol FROM OtrosUsuarios WHERE CorreoElectronico = %s"
        params = (email,)
        try:
            user = self.execute_query(query, params=params, fetchone=True)
            if user != None:
                return user[0]
            else:
                raise Exception("Usuario no encontrado")
        except Exception as e:
            print(f"Error al ejecutar la query: {query}")
            print(f"Error: {e}")
            return None
