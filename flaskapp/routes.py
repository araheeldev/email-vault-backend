from flask import Blueprint, request, jsonify
from .services.auth_service import signup_user, login_user, password_recovery, enable_two_factor, verify_login_2fa, verify_account

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    response = signup_user(data) 
    return jsonify(response)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    response = login_user(data)  
    return jsonify(response)

@auth_bp.route('/password-recovery', methods=['POST'])
def password_recovery_route():
    data = request.json
    response = password_recovery(data)  
    return jsonify(response)

@auth_bp.route('/enable-2fa', methods=['POST'])
def enable_2fa():
    data = request.json
    response = enable_two_factor(data.get('user_id'))  
    return jsonify(response)

@auth_bp.route('/verify-login-2fa', methods=['POST'])
def verify_2fa():
    data = request.json
    response = verify_login_2fa(data)  
    return jsonify(response)

@auth_bp.route('/verify/<user_id>', methods=['GET'])
def verify_account_route(user_id):
    response = verify_account(user_id)  
    return jsonify(response)


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
