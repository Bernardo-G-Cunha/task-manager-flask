from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import bcrypt
from app.schemas.user_schema import *
from app.models.user import User
from app.services.auth import *
from app.exceptions import *

#------------------------------------------------------------------------------------------------------------------

auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/', methods=['POST'])
def login():
    login_data = user_login_schema.load(request.get_json())
    access_token = verify_user(login_data)
    return jsonify({"success": True, "data": {"access_token": access_token}}), 200


@auth_bp.route('/signup', methods=['POST'])
def signup():
    signup_data = user_signup_schema.load(request.get_json())
    create_user(signup_data)
    return jsonify({"success": True, "message": "Successfully signed up"}), 201