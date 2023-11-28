-- DROP SCHEMA dbo;

CREATE SCHEMA dbo;
-- face_n_lean.dbo.Aulas definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.Aulas;

CREATE TABLE face_n_lean.dbo.Aulas (
	AulaID nvarchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	Nombre nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	Ubicacion nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CONSTRAINT PK__Aulas__A8529A182DE02582 PRIMARY KEY (AulaID)
);


-- face_n_lean.dbo.Cursos definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.Cursos;

CREATE TABLE face_n_lean.dbo.Cursos (
	CursoID int NOT NULL,
	Nombre nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Descripcion nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CONSTRAINT PK__Cursos__7E023A37E981413F PRIMARY KEY (CursoID)
);


-- face_n_lean.dbo.DiasDeLaSemana definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.DiasDeLaSemana;

CREATE TABLE face_n_lean.dbo.DiasDeLaSemana (
	DiaID int NOT NULL,
	NombreDia nvarchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CONSTRAINT PK__DiasDeLa__ED194D9691763FDE PRIMARY KEY (DiaID)
);


-- face_n_lean.dbo.Estudiantes definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.Estudiantes;

CREATE TABLE face_n_lean.dbo.Estudiantes (
	EstudianteID int IDENTITY(1,1) NOT NULL,
	Nombre nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Apellido nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CorreoElectronico nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	AzureB2C_ID uniqueidentifier NOT NULL,
	Matricula nvarchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	fotosRostro varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CONSTRAINT PK__Estudian__6F7683380BFADED7 PRIMARY KEY (EstudianteID),
	CONSTRAINT UQ__Estudian__531402F3E304C615 UNIQUE (CorreoElectronico),
	CONSTRAINT UQ__Estudian__Matricula UNIQUE (Matricula)
);


-- face_n_lean.dbo.OtrosUsuarios definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.OtrosUsuarios;

CREATE TABLE face_n_lean.dbo.OtrosUsuarios (
	UsuarioID int IDENTITY(1,1) NOT NULL,
	Nombre nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	Apellido nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	CorreoElectronico nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	AzureB2C_ID uniqueidentifier NULL,
	Rol nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	CONSTRAINT PK_Usuarios PRIMARY KEY (UsuarioID),
	CONSTRAINT UQ_CorreoElectronico_Usuarios UNIQUE (CorreoElectronico)
);


-- face_n_lean.dbo.Profesores definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.Profesores;

CREATE TABLE face_n_lean.dbo.Profesores (
	ProfesorID int IDENTITY(1,1) NOT NULL,
	Nombre nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Apellido nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CorreoElectronico nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	AzureB2C_ID uniqueidentifier NULL,
	Nomina nvarchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CONSTRAINT PK__Profesor__4DF3F028A3E43F72 PRIMARY KEY (ProfesorID),
	CONSTRAINT UQ__Profesor__531402F368C6AE33 UNIQUE (CorreoElectronico),
	CONSTRAINT UQ__Profesor__Nomina UNIQUE (Nomina)
);


-- face_n_lean.dbo.Clases definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.Clases;

CREATE TABLE face_n_lean.dbo.Clases (
	ClaseID int NOT NULL,
	CursoID int NOT NULL,
	Ubicacion nvarchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	Nombre nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	FechaInicio datetime2 NULL,
	FechaFin datetime2 NULL,
	HoraInicio time NULL,
	HoraFin time NULL,
	ProfesorID int NULL,
	CONSTRAINT PK__Clases__F54296B3A2A71AC0 PRIMARY KEY (ClaseID),
	CONSTRAINT FK_Clases_Aulas FOREIGN KEY (Ubicacion) REFERENCES face_n_lean.dbo.Aulas(AulaID),
	CONSTRAINT FK_Clases_Profesores FOREIGN KEY (ProfesorID) REFERENCES face_n_lean.dbo.Profesores(ProfesorID),
	CONSTRAINT FK__Clases__CursoID__571DF1D5 FOREIGN KEY (CursoID) REFERENCES face_n_lean.dbo.Cursos(CursoID)
);


-- face_n_lean.dbo.CursoProfesores definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.CursoProfesores;

CREATE TABLE face_n_lean.dbo.CursoProfesores (
	CursoProfesorID int NOT NULL,
	ProfesorID int NULL,
	ClaseID int NULL,
	CONSTRAINT PK__CursoPro__FA0B9F4BC23E062B PRIMARY KEY (CursoProfesorID),
	CONSTRAINT FK__CursoProf__Clase__1AD3FDA4 FOREIGN KEY (ClaseID) REFERENCES face_n_lean.dbo.Clases(ClaseID),
	CONSTRAINT FK__CursoProf__Profe__1BC821DD FOREIGN KEY (ProfesorID) REFERENCES face_n_lean.dbo.Profesores(ProfesorID)
);


-- face_n_lean.dbo.DatosVideo definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.DatosVideo;

CREATE TABLE face_n_lean.dbo.DatosVideo (
	VideoID int NOT NULL,
	AulaID nvarchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	FechaHora datetime NOT NULL,
	RutaArchivo nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	CONSTRAINT PK__DatosVid__BAE5124AA3DE1F97 PRIMARY KEY (VideoID),
	CONSTRAINT FK__DatosVide__AulaI__6A30C649 FOREIGN KEY (AulaID) REFERENCES face_n_lean.dbo.Aulas(AulaID)
);


-- face_n_lean.dbo.Estadisticas definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.Estadisticas;

CREATE TABLE face_n_lean.dbo.Estadisticas (
	EstadisticaID int NOT NULL,
	ClaseID int NOT NULL,
	EstudianteID int NOT NULL,
	PorcentajeAsistencia float NOT NULL,
	PorcentajeParticipacion float NOT NULL,
	CONSTRAINT PK__Estadist__5E78B5ECD1EADFE9 PRIMARY KEY (EstadisticaID),
	CONSTRAINT FK__Estadisti__Clase__74AE54BC FOREIGN KEY (ClaseID) REFERENCES face_n_lean.dbo.Clases(ClaseID),
	CONSTRAINT FK__Estadisti__Estud__75A278F5 FOREIGN KEY (EstudianteID) REFERENCES face_n_lean.dbo.Estudiantes(EstudianteID)
);


-- face_n_lean.dbo.EventosIdentificacion definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.EventosIdentificacion;

CREATE TABLE face_n_lean.dbo.EventosIdentificacion (
	EventoID int NOT NULL,
	VideoID int NOT NULL,
	Tiempo datetime2 NOT NULL,
	EstudianteID int NULL,
	ProfesorID int NULL,
	TipoEvento nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	CONSTRAINT PK__EventosI__1EEB59015BB167E8 PRIMARY KEY (EventoID),
	CONSTRAINT FK__EventosId__Estud__6E01572D FOREIGN KEY (EstudianteID) REFERENCES face_n_lean.dbo.Estudiantes(EstudianteID),
	CONSTRAINT FK__EventosId__Profe__6EF57B66 FOREIGN KEY (ProfesorID) REFERENCES face_n_lean.dbo.Profesores(ProfesorID),
	CONSTRAINT FK__EventosId__Video__6D0D32F4 FOREIGN KEY (VideoID) REFERENCES face_n_lean.dbo.DatosVideo(VideoID)
);


-- face_n_lean.dbo.Inscripciones definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.Inscripciones;

CREATE TABLE face_n_lean.dbo.Inscripciones (
	InscripcionID int NOT NULL,
	EstudianteID int NOT NULL,
	ClaseID int NULL,
	CONSTRAINT PK__Inscripc__16831699D3825EE9 PRIMARY KEY (InscripcionID),
	CONSTRAINT FK__Inscripci__ClaseID FOREIGN KEY (ClaseID) REFERENCES face_n_lean.dbo.Clases(ClaseID),
	CONSTRAINT FK__Inscripci__Estud__160F4887 FOREIGN KEY (EstudianteID) REFERENCES face_n_lean.dbo.Estudiantes(EstudianteID)
);


-- face_n_lean.dbo.Participacion definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.Participacion;

CREATE TABLE face_n_lean.dbo.Participacion (
	ParticipacionID int IDENTITY(1,1) NOT NULL,
	EstudianteID int NOT NULL,
	ClaseID int NOT NULL,
	TipoParticipacion nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	Detalles nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	[Timestamp] datetime NULL,
	CONSTRAINT PK__Particip__5815A09D6DF9D6A7 PRIMARY KEY (ParticipacionID),
	CONSTRAINT FK__Participa__Clase__59063A47 FOREIGN KEY (ClaseID) REFERENCES face_n_lean.dbo.Clases(ClaseID),
	CONSTRAINT FK__Participa__Estud__59FA5E80 FOREIGN KEY (EstudianteID) REFERENCES face_n_lean.dbo.Estudiantes(EstudianteID)
);


-- face_n_lean.dbo.Transcripciones definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.Transcripciones;

CREATE TABLE face_n_lean.dbo.Transcripciones (
	TranscripcionID int NOT NULL,
	VideoID int NOT NULL,
	Texto nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	CONSTRAINT PK__Transcri__B5BF735D31CBCFD5 PRIMARY KEY (TranscripcionID),
	CONSTRAINT FK__Transcrip__Video__71D1E811 FOREIGN KEY (VideoID) REFERENCES face_n_lean.dbo.DatosVideo(VideoID)
);


-- face_n_lean.dbo.Asistencia definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.Asistencia;

CREATE TABLE face_n_lean.dbo.Asistencia (
	AsistenciaID int IDENTITY(1,1) NOT NULL,
	EstudianteID int NOT NULL,
	ClaseID int NOT NULL,
	HoraEntrada datetime2 NOT NULL,
	HoraSalida datetime2 NOT NULL,
	CONSTRAINT PK__Asistenc__72710F45AF9A6D66 PRIMARY KEY (AsistenciaID),
	CONSTRAINT FK__Asistenci__Clase__5535A963 FOREIGN KEY (ClaseID) REFERENCES face_n_lean.dbo.Clases(ClaseID),
	CONSTRAINT FK__Asistenci__Estud__5629CD9C FOREIGN KEY (EstudianteID) REFERENCES face_n_lean.dbo.Estudiantes(EstudianteID)
);


-- face_n_lean.dbo.ClaseDias definition

-- Drop table

-- DROP TABLE face_n_lean.dbo.ClaseDias;

CREATE TABLE face_n_lean.dbo.ClaseDias (
	ClaseID int NOT NULL,
	DiaID int NOT NULL,
	CONSTRAINT PK__ClaseDia__8B93026AAD378519 PRIMARY KEY (ClaseID,DiaID),
	CONSTRAINT FK__ClaseDias__Clase__6D0D32F4 FOREIGN KEY (ClaseID) REFERENCES face_n_lean.dbo.Clases(ClaseID),
	CONSTRAINT FK__ClaseDias__DiaID__6E01572D FOREIGN KEY (DiaID) REFERENCES face_n_lean.dbo.DiasDeLaSemana(DiaID)
);
