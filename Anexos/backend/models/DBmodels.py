from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import varConfig

Base = declarative_base()

# Definición del modelo Estudiante
class Estudiante(Base):
    __tablename__ = 'Estudiantes'
    EstudianteID = Column(Integer, primary_key=True)
    Nombre = Column(String)
    Apellido = Column(String)
    CorreoElectronico = Column(String)
    AzureB2C_ID = Column(String)

# Definición del modelo Aula
class Aula(Base):
    __tablename__ = 'Aulas'
    AulaID = Column(Integer, primary_key=True)
    Nombre = Column(String, nullable=False)
    Ubicacion = Column(String)
    
# Definición del modelo OtrosUsuarios
class OtrosUsuarios(Base):
    __tablename__ = 'OtrosUsuarios'
    UsuarioID = Column(Integer, primary_key=True)
    Nombre = Column(String, nullable=False)
    Apellido = Column(String, nullable=False)
    CorreoElectronico = Column(String, unique=True, nullable=False)
    AzureB2C_ID = Column(String)
    Rol = Column(String, nullable=False)

# Definición del modelo Profesor
class Profesor(Base):
    __tablename__ = 'Profesores'
    ProfesorID = Column(Integer, primary_key=True)
    Nombre = Column(String)
    Apellido = Column(String)
    CorreoElectronico = Column(String, unique=True)
    AzureB2C_ID = Column(String)

# Definición del modelo Curso
class Curso(Base):
    __tablename__ = 'Cursos'
    CursoID = Column(Integer, primary_key=True)
    Nombre = Column(String)
    Descripcion = Column(String)
    ProfesorID = Column(Integer, ForeignKey('Profesores.ProfesorID'))
    profesor = relationship("Profesor", back_populates="cursos")

# Definición del modelo DatosVideo
class DatosVideo(Base):
    __tablename__ = 'DatosVideo'
    VideoID = Column(Integer, primary_key=True)
    AulaID = Column(Integer, ForeignKey('Aulas.AulaID'))
    FechaHora = Column(DateTime)
    RutaArchivo = Column(String)
    aula = relationship("Aula", back_populates="videos")

# Definición del modelo EventosIdentificacion
class EventosIdentificacion(Base):
    __tablename__ = 'EventosIdentificacion'
    EventoID = Column(Integer, primary_key=True)
    VideoID = Column(Integer, ForeignKey('DatosVideo.VideoID'))
    Tiempo = Column(DateTime)
    EstudianteID = Column(Integer, ForeignKey('Estudiantes.EstudianteID'))
    ProfesorID = Column(Integer, ForeignKey('Profesores.ProfesorID'))
    TipoEvento = Column(String)
    estudiante = relationship("Estudiante", back_populates="eventos_identificacion")
    profesor = relationship("Profesor", back_populates="eventos_identificacion")
    video = relationship("DatosVideo", back_populates="eventos_identificacion")

# Definición del modelo Transcripciones
class Transcripciones(Base):
    __tablename__ = 'Transcripciones'
    TranscripcionID = Column(Integer, primary_key=True)
    VideoID = Column(Integer, ForeignKey('DatosVideo.VideoID'))
    Texto = Column(String)
    video = relationship("DatosVideo", back_populates="transcripciones")

# Definición del modelo Clases
class Clases(Base):
    __tablename__ = 'Clases'
    ClaseID = Column(Integer, primary_key=True)
    CursoID = Column(Integer, ForeignKey('Cursos.CursoID'))
    FechaHora = Column(DateTime)
    Ubicacion = Column(String)
    Nombre = Column(String)
    curso = relationship("Curso", back_populates="clases")

# Definición del modelo Estadisticas
class Estadisticas(Base):
    __tablename__ = 'Estadisticas'
    EstadisticaID = Column(Integer, primary_key=True)
    ClaseID = Column(Integer, ForeignKey('Clases.ClaseID'))
    EstudianteID = Column(Integer, ForeignKey('Estudiantes.EstudianteID'))
    PorcentajeAsistencia = Column(Float)
    PorcentajeParticipacion = Column(Float)
    estudiante = relationship("Estudiante", back_populates="estadisticas")
    clase = relationship("Clases", back_populates="estadisticas")

# Definición del modelo Participacion
class Participacion(Base):
    __tablename__ = 'Participacion'
    ParticipacionID = Column(Integer, primary_key=True)
    EstudianteID = Column(Integer, ForeignKey('Estudiantes.EstudianteID'))
    ClaseID = Column(Integer, ForeignKey('Clases.ClaseID'))
    TipoParticipacion = Column(String)
    Detalles = Column(String)
    Timestamp = Column(DateTime)
    estudiante = relationship("Estudiante", back_populates="participaciones")
    clase = relationship("Clases", back_populates="participaciones")

# Definición del modelo Asistencia
class Asistencia(Base):
    __tablename__ = 'Asistencia'
    AsistenciaID = Column(Integer, primary_key=True)
    EstudianteID = Column(Integer, ForeignKey('Estudiantes.EstudianteID'))
    ClaseID = Column(Integer, ForeignKey('Clases.ClaseID'))
    HoraEntrada = Column(DateTime)
    HoraSalida = Column(DateTime)
    estudiante = relationship("Estudiante", back_populates="asistencias")
    clase = relationship("Clases", back_populates="asistencias")
