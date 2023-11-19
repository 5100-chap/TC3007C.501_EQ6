from flask import Flask, request, jsonify
from flask_cors import CORS
from auth.AzureADManager import AzureADManager
from auth.authManager import AuthManager
from databases.DatabaseManager import DatabaseManager
from config.varConfig import FLASK_SECRET_KEY
from models.MLmodel import MLmodel

#Variables globales
url = "http://localhost:5000"
fronturl = "http://localhost:3000"
app = Flask(__name__)
CORS(app, supports_credentials=True)
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


if __name__ == "__main__":
    app.run(debug=True)
