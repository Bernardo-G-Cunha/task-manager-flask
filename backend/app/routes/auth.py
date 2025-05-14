import os
from flask import Blueprint, request, make_response, render_template, redirect, url_for, Response, jsonify, session
from sqlalchemy.exc import NoResultFound, MultipleResultsFound
from app.extensions import bcrypt
from app.schemas.user_schema import UserSchema
from app.models.user import User
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__, template_folder='templates')

user_schema = UserSchema()

@auth_bp.route('/', methods=['POST'])
def login():
    try:
        data = user_schema.load(request.get_json())
        email = data['email']
        password = data['password']

    except ValidationError as err:
        return jsonify({"error": err.messsages}), 400

    except Exception as err:
        return jsonify({"error": str(err)}), 500

    user = User.query.filter_by(email=email).first()
    
    if not(email == user.email) or not(bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))):
        return jsonify({"error": "Invalid credentials"}), 401
    
    #-------------------------------------------------------------------------
    #Generate token with JWT