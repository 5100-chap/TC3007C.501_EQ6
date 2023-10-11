# Arquitectura y tecnologias a usar en el proyecto

## Diagrama de arquitectura del proyecto
<img src="./Diagrama%20de%20arquitectura.png" alt="Diagrama de Flujo en donde se ejemplifica las etapas del proyecto" width="400">

### General
En este proyecto se tiene pensado usar diversas tecnologias en la nube, todas con el respaldo de Azure, que es un proveedor de servicios en la nube muy reconocido por su fiabilidad, los servicios estaran conectados a una API que permitira la comunicacion entre la pagina web y la base de datos, la cual es una base de datos relacional SQL, que permitira almacenar y relacionar datos de por ejemplo los alumnos que asistieron a un curso, a que hora se registro la aisstencia, en que curso asistieron entre otros.

Nuestros datos de entrada para que la aplicación funcione es el tener acceso a una camara de video en el cual se pueda observar a los diferentes alumnos a registrar su pase de lista y otros diversos datos que puedan tomarse acorde a los requerimientos del reto, estos datos son procesados por el backend para almacenarlos y que estos datos puedan ser usados por el usuario para hacer diversas consultas para verificar datos requeridos por el docente, el principal checar asistencia de los alumnos, se tiene en mente que modelos visión computacional de inteligencia artificial preentrenados ayuden a identificar las acciones y el rostro de los alumnos para cumplir con lo fundamental de este proyecto

El frontend, desarrollado en React, proporcionará una interfaz interactiva para acceder y visualizar los datos procesados.
El backend, desarrollado en Python y alojado en Azure Functions, gestionará la lógica de procesamiento de datos, la interacción con la base de datos y el almacenamiento en blob, y la autenticación de usuarios.

El uso de Big Data en este proyecto es fundamental debido a la naturaleza y volumen de los datos que serán procesados. Los datos de video en tiempo real de múltiples aulas son inherentemente grandes y requieren un procesamiento y análisis eficiente para extraer información valiosa. Además, la integración con plataformas de aprendizaje y la generación automática de informes y estadísticas sugiere una acumulación continua de datos que eventualmente podría escalar a un nivel que justifique una infraestructura de Big Data.

En cuanto al almacenamiento y manejo de datos, se propone un modelo híbrido que integra bases de datos relacionales y almacenamiento en blob para manejar diferentes tipos de datos de manera eficiente.

## Modelo de Almacenamiento y Manejo de Datos:

### Función de la base de datos SQL
* Almacenamiento de metadatos y datos estructurados como información de usuarios, asistencia, horarios de clases, entre otros ademas de relacionar la información de los usuarios con los videos procesados y almacenados en el Blob Storage mediante IDs únicos.

### Función del Blob Storage:

* Almacenamiento de datos no estructurados como los videos procesados los cuales tendran referencia (IDs), las cuales seran almacenadas en la base de datos relacional para acceder a los videos correspondientes.
