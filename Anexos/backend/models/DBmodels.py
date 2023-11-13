class Aulas:
    def __init__(self, AulaID, Nombre, Ubicacion):
        self.AulaID = AulaID
        self.Nombre = Nombre
        self.Ubicacion = Ubicacion

class Estudiantes:
    def __init__(self, EstudianteID, Nombre, Apellido, CorreoElectronico, AzureB2C_ID):
        self.EstudianteID = EstudianteID
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.CorreoElectronico = CorreoElectronico
        self.AzureB2C_ID = AzureB2C_ID

class OtrosUsuarios:
    def __init__(self, UsuarioID, Nombre, Apellido, CorreoElectronico, AzureB2C_ID, Rol):
        self.UsuarioID = UsuarioID
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.CorreoElectronico = CorreoElectronico
        self.AzureB2C_ID = AzureB2C_ID
        self.Rol = Rol

class Profesores:
    def __init__(self, ProfesorID, Nombre, Apellido, CorreoElectronico, AzureB2C_ID):
        self.ProfesorID = ProfesorID
        self.Nombre = Nombre
        self.Apellido = Apellido
        self.CorreoElectronico = CorreoElectronico
        self.AzureB2C_ID = AzureB2C_ID

class Cursos:
    def __init__(self, CursoID, Nombre, Descripcion, ProfesorID):
        self.CursoID = CursoID
        self.Nombre = Nombre
        self.Descripcion = Descripcion
        self.ProfesorID = ProfesorID

class DatosVideo:
    def __init__(self, VideoID, AulaID, FechaHora, RutaArchivo):
        self.VideoID = VideoID
        self.AulaID = AulaID
        self.FechaHora = FechaHora
        self.RutaArchivo = RutaArchivo

class EventosIdentificacion:
    def __init__(self, EventoID, VideoID, Tiempo, EstudianteID, ProfesorID, TipoEvento):
        self.EventoID = EventoID
        self.VideoID = VideoID
        self.Tiempo = Tiempo
        self.EstudianteID = EstudianteID
        self.ProfesorID = ProfesorID
        self.TipoEvento = TipoEvento

class Inscripciones:
    def __init__(self, InscripcionID, EstudianteID, CursoID):
        self.InscripcionID = InscripcionID
        self.EstudianteID = EstudianteID
        self.CursoID = CursoID

class Transcripciones:
    def __init__(self, TranscripcionID, VideoID, Texto):
        self.TranscripcionID = TranscripcionID
        self.VideoID = VideoID
        self.Texto = Texto

class Clases:
    def __init__(self, ClaseID, CursoID, FechaHora, Ubicacion, Nombre):
        self.ClaseID = ClaseID
        self.CursoID = CursoID
        self.FechaHora = FechaHora
        self.Ubicacion = Ubicacion
        self.Nombre = Nombre

class CursoProfesores:
    def __init__(self, CursoProfesorID, CursoID, ProfesorID):
        self.CursoProfesorID = CursoProfesorID
        self.CursoID = CursoID
        self.ProfesorID = ProfesorID

class Estadisticas:
    def __init__(self, EstadisticaID, ClaseID, EstudianteID, PorcentajeAsistencia, PorcentajeParticipacion):
        self.EstadisticaID = EstadisticaID
        self.ClaseID = ClaseID
        self.EstudianteID = EstudianteID
        self.PorcentajeAsistencia = PorcentajeAsistencia
        self.PorcentajeParticipacion = PorcentajeParticipacion

class Participacion:
    def __init__(self, ParticipacionID, EstudianteID, ClaseID, TipoParticipacion, Detalles, Timestamp):
        self.ParticipacionID = ParticipacionID
        self.EstudianteID = EstudianteID
        self.ClaseID = ClaseID
        self.TipoParticipacion = TipoParticipacion
        self.Detalles = Detalles
        self.Timestamp = Timestamp

class Asistencia:
    def __init__(self, AsistenciaID, EstudianteID, ClaseID, HoraEntrada, HoraSalida):
        self.AsistenciaID = AsistenciaID
        self.EstudianteID = EstudianteID
        self.ClaseID = ClaseID
        self.HoraEntrada = HoraEntrada
        self.HoraSalida = HoraSalida
