from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from auth.AzureADManager import AzureADManager
from auth.authManager import AuthManager
from databases.DatabaseManager import DatabaseManager
from databases.blobManager import BlobManager
from config.varConfig import FLASK_SECRET_KEY
from models.MLmodel import MLmodel
import base64
import numpy as np
import cv2


# Variables globales
url = "http://localhost:5000"
fronturl = "http://localhost:3000"
app = Flask(__name__)
CORS(app, supports_credentials=True)

blob_manager = BlobManager()
db_manager = DatabaseManager(isFreeDB=False)
azure_ad_manager = AzureADManager(db_manager)
auth_manager = AuthManager(url, db_manager, fronturl)
ml_model = MLmodel(db_manager)

app.secret_key = FLASK_SECRET_KEY

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user_id = data.get("userID")
    user_data = data
    user_role = data.get("Rol")

    try:
        response = azure_ad_manager.register_user(user_id, user_data, user_role)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update_user/<user_id>/<user_role>", methods=["PATCH"])
def update_user(user_id, user_role):
    update_data = request.json
    try:
        response = azure_ad_manager.update_user(user_id, update_data, user_role)
        if response.status_code == 204:
            return jsonify({"message": "User updated successfully"}), 204
        else:
            return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/obtain_students_info", methods=["POST"])
def obtain_students_info():
    data = request.json
    allStudents = True if data["type"] == "AllStudentRequest" else False
    try:
        if allStudents:
            response = db_manager.get_students(allStudents=allStudents)
        else:
            response = db_manager.get_students(
                allStudents=allStudents,
                student_id=data["oid"],
                class_id=data["Clase"],
                course_id=data["Curso"],
            )
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/obtain_clases_info", methods=["POST"])
def obtain_clases_info():
    data = request.json
    try:
        response = db_manager.get_user_clases(
            user_id=data["oid"], user_role=data["user_role"]
        )
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/alumnos/foto", methods=["POST"])
def alumnos_foto():
    data = request.form.to_dict()
    file = request.files["file"]
    link = ""

    try:
        rol_extraido = data["Rol"]
        oid_extraido = data["user_oid"]
        link = blob_manager.upload_image(file, file.filename)

        if rol_extraido in ["Admin", "Mod", "Dueño", "Profesor"]:
            # Actualizar la foto del estudiante con el rol extraído
            response = db_manager.update_student_photo(
                student_id=data["oid"], photo_url=link, user_role=rol_extraido
            )
        elif rol_extraido == "Alumno":
            # Actualizar la foto del estudiante con el rol y oid extraídos
            response = db_manager.update_student_photo(
                student_id=data["oid"],
                photo_url=link,
                user_role=rol_extraido,
                user_id=oid_extraido,
            )
        else:
            return jsonify({"error": "Rol inválido"}), 400

        return jsonify(response), 200
    except Exception as e:
        blob_manager.delete_image(link)
        return jsonify({"error": str(e)}), 500


@app.route("/delete_user/<user_id>/<user_role>", methods=["DELETE"])
def delete_user(user_id, user_role):
    try:
        response = azure_ad_manager.delete_user(user_id, user_role)
        if response.status_code == 204:
            return jsonify({"message": "User deleted successfully"}), 204
        else:
            return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/login")
def login():
    return auth_manager.login()


@app.route("/login-redirect")
def login_redirect():
    return auth_manager.login_redirect()


@app.route("/logout")
def logout():
    return auth_manager.logout()


@app.route("/receive_fps_ml", methods=["POST"])
def receive_fps_ml():
    data = request.json
    image_src = data.get("image")
    selected_course = data.get("course")

    try:
        # Decodificar la imagen base64 y convertirla en una matriz de imagen
        image_data = base64.b64decode(image_src.split(",")[1])
        nparr = np.frombuffer(image_data, dtype=np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Guardar la imagen original temporalmente
        #cv2.imwrite("temp_original.jpg", img)

        # Procesar la imagen
        processed_image, results = ml_model.process_image(img)

        # Guardar la imagen procesada temporalmente
        #cv2.imwrite("temp_processed.jpg", processed_image)

        # Codificar la imagen procesada en base64 para la respuesta
        _, buffer = cv2.imencode('.jpg', processed_image)
        jpg_as_text = base64.b64encode(buffer).decode()

        # Eliminar las imágenes temporales
        #os.remove("temp_original.jpg")
        #os.remove("temp_processed.jpg")

        return jsonify({"image": jpg_as_text, "results": results}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True)
    # Importar el módulo necesario

    # ...

    