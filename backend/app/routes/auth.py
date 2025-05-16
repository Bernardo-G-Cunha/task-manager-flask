from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from app.extensions import bcrypt
from app.schemas.user_schema import UserSchema
from app.models.user import User
from app.services.auth import *
from app.exceptions.auth_exceptions import *

#------------------------------------------------------------------------------------------------------------------

auth_bp = Blueprint('auth', __name__, template_folder='templates')

user_schema = UserSchema()

@auth_bp.route('/', methods=['POST'])
def login():
    data = user_schema.load(request.get_json())
    user = verify_user(data['email'], data['password'])

    access_token = create_access_token(identity=user.id)

    return jsonify({"access_token": access_token}), 200


@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = user_schema.load(request.get_json())
    create_user(data['username'], data['email'], data['password'])

    return jsonify({"message": "Successfully signed up"}), 200