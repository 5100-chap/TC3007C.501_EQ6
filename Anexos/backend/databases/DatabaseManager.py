import pymssql
from config import varConfig
from models import DBmodels


class DatabaseManager:
    def __init__(self):
        self.conn = pymssql.connect(
            server=varConfig.DBserver,
            user=varConfig.DBuser,
            password=varConfig.DBpassword,
            database=varConfig.DBname,
        )
        self.cursor = self.conn.cursor()

    def can_register(self, admin_role, user_role):
        hierarchy = {"Dueño": 5, "Admin": 4, "Mod": 3, "Profesor": 2, "Alumno": 1}
        return hierarchy.get(admin_role, 0) > hierarchy.get(user_role, 0)

    def register_user(self, admin_id, user_data, user_role):
        # Verificar si el administrador tiene permiso para registrar este rol
        self.cursor.execute(
            "SELECT * FROM OtrosUsuarios WHERE UsuarioID = ?", (admin_id,)
        )
        admin = self.cursor.fetchone()
        if admin and self.can_register(admin[5], user_role):
            # Crear el nuevo usuario según el rol
            if user_role == "Estudiante":
                query = "INSERT INTO Estudiantes (Nombre, Apellido, CorreoElectronico, AzureB2C_ID) VALUES (?, ?, ?, ?)"
                params = (
                    user_data["Nombre"],
                    user_data["Apellido"],
                    user_data["CorreoElectronico"],
                    user_data["AzureB2C_ID"],
                )
            elif user_role == "Profesor":
                query = "INSERT INTO Profesores (Nombre, Apellido, CorreoElectronico, AzureB2C_ID) VALUES (?, ?, ?, ?)"
                params = (
                    user_data["Nombre"],
                    user_data["Apellido"],
                    user_data["CorreoElectronico"],
                    user_data["AzureB2C_ID"],
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
                self.cursor.execute(query, params)
                self.conn.commit()
                return self.cursor.lastrowid
            except Exception as e:
                print(f"Error al ejecutar la query: {query}")
                print(f"Error: {e}")
                self.conn.rollback()
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
            self.cursor.execute(query, params)
            self.conn.commit()
            return user_id
        except Exception as e:
            print(f"Error al ejecutar la query: {query}")
            print(f"Error: {e}")
            self.conn.rollback()
            return None

    def delete_user(self, user_id, user_role):
        if user_role == "Estudiante":
            query = f"DELETE FROM Estudiante WHERE EstudianteID = {user_id}"
        elif user_role == "Profesor":
            query = f"DELETE FROM Profesor WHERE ProfesorID = {user_id}"
        else:
            query = f"DELETE FROM OtrosUsuarios WHERE UsuarioID = {user_id}"
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            print(f"Error al ejecutar la query: {query}")
            print(f"Error: {e}")
            self.conn.rollback()

    def get_user_role(self, email):
        query = f"SELECT Rol FROM OtrosUsuarios WHERE CorreoElectronico = '{email}'"
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        if user:
            return user[0]
        else:
            raise Exception("Usuario no encontrado")
