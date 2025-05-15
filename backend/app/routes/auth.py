from flask import Blueprint, request, jsonify
from sqlalchemy.orm.exc import NoResultFound
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from app.extensions import bcrypt
from app.schemas.user_schema import UserSchema
from app.models.user import User
from app.services.auth import verify_user

#------------------------------------------------------------------------------------------------------------------

auth_bp = Blueprint('auth', __name__, template_folder='templates')

user_schema = UserSchema()

@auth_bp.route('/', methods=['POST'])
def login():
    #Gets request's data
    try:
        data = user_schema.load(request.get_json())
        user = verify_user(data['email'], data['password'])

    except ValidationError as err:
        return jsonify({"error": err.messsages}), 400
    
    except ValueError as err:
        return jsonify({"error": str(err)}), 401

    except Exception as err:
        return jsonify({"error": str(err)}), 500

    #Generates JWT token for valid users
    access_token = create_access_token(identity=user.id)

    return jsonify({"access_token": access_token}), 200