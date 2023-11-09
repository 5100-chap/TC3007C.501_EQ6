from flask import Flask, request, jsonify
from auth.AzureADManager import AzureADManager
from auth.authManager import AuthManager

#Variables globales
url = "http://localhost:5000"
app = Flask(__name__)
azure_ad_manager = AzureADManager()
auth_manager = AuthManager(url)


@app.route("/register", methods=["POST"])
def register():
    user_data = request.json
    response = azure_ad_manager.register_user(user_data)
    if response.status_code == 201:
        return jsonify(response.json()), 201
    else:
        return jsonify(response.json()), response.status_code


@app.route("/update_user/<user_id>", methods=["PATCH"])
def update_user(user_id):
    update_data = request.json
    response = azure_ad_manager.update_user(user_id, update_data)
    if response.status_code == 204:
        return jsonify({"message": "User updated successfully"}), 204
    else:
        return jsonify(response.json()), response.status_code


@app.route("/delete_user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    response = azure_ad_manager.delete_user(user_id)
    if response.status_code == 204:
        return jsonify({"message": "User deleted successfully"}), 204
    else:
        return jsonify(response.json()), response.status_code


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
