# Arquitectura y Tecnologías a Utilizar en el Proyecto

## Diagrama de Arquitectura del Proyecto
<img src="./Diagrama%20de%20arquitectura.png" alt="Diagrama de Flujo que ejemplifica las etapas del proyecto" width="400">

### General
En este proyecto se planea utilizar diversas tecnologías en la nube, todas respaldadas por Azure, un proveedor de servicios en la nube altamente reconocido por su fiabilidad. Los servicios estarán conectados a una API que facilitará la comunicación entre la página web y la base de datos. La base de datos es de tipo relacional SQL, permitiendo almacenar y relacionar datos, por ejemplo, los alumnos que asistieron a un curso, la hora de registro de asistencia, y el curso al que asistieron, entre otros.

La entrada de datos esencial para el funcionamiento de la aplicación es el acceso a una cámara de video para registrar la asistencia de los alumnos y capturar otros datos relevantes según los requerimientos del proyecto. Estos datos son procesados por el backend para su almacenamiento, permitiendo al usuario realizar diversas consultas para verificar la información requerida por el docente. Principalmente, se busca verificar la asistencia de los alumnos. Se contempla la utilización de modelos de visión computacional de inteligencia artificial preentrenados para identificar las acciones y los rostros de los alumnos, cumpliendo así con los objetivos fundamentales del proyecto.

El frontend, desarrollado en React, proporcionará una interfaz interactiva para acceder y visualizar los datos procesados. El backend, desarrollado en Python y alojado en Azure Functions, gestionará la lógica de procesamiento de datos, la interacción con la base de datos, el almacenamiento en blob, y la autenticación de usuarios.

La incorporación de Big Data en este proyecto es crucial debido a la naturaleza y el volumen de los datos que serán procesados. Los datos de video en tiempo real provenientes de múltiples aulas son inherentemente grandes y requieren un procesamiento y análisis eficiente para extraer información valiosa. Además, la integración con plataformas de aprendizaje y la generación automática de informes y estadísticas sugiere una acumulación continua de datos que eventualmente podría escalar a un nivel que justifique una infraestructura de Big Data.

En cuanto al almacenamiento y manejo de datos, se propone un modelo híbrido que integra bases de datos relacionales y almacenamiento en blob para manejar diferentes tipos de datos de manera eficiente.

## Modelo de Almacenamiento y Manejo de Datos:

### Función de la Base de Datos SQL
* Almacenamiento de metadatos y datos estructurados como información de usuarios, asistencia, horarios de clases, entre otros. Además, permitirá relacionar la información de los usuarios con los videos procesados y almacenados en el Blob Storage mediante IDs únicos.

### Función del Blob Storage:

* Almacenamiento de datos no estructurados como los videos procesados, los cuales tendrán referencias (IDs) que serán almacenadas en la base de datos relacional para acceder a los videos correspondientes.
