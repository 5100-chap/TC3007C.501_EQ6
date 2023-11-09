from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import varConfig
from models import DBmodels as models

engine = create_engine(varConfig.AZURE_SQL_CONNECTION_STRING)
Session = sessionmaker(bind=engine)

class DatabaseManager:
    def __init__(self):
        self.session = Session()

    def register_user(self, user_data, role):
        if role == "Estudiante":
            new_user = models.Estudiante(**user_data)
            self.session.add(new_user)
        # Lógica para otros roles...
        self.session.commit()

    # Más métodos para manejar la base de datos
    # ...