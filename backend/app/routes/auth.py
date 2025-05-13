import os
from flask import Blueprint, request, make_response, render_template, redirect, url_for, Response, jsonify, session
from app.extensions import bcrypt
from app.schemas.user_schema import UserSchema
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__, template_folder='templates')

user_schema = UserSchema()

@auth_bp.route('/', methods=['POST'])
def login():
    try:
        data = user_schema.load(request.get_json())
        username = data['username']
        password = data['password']

    except ValidationError as vali_err:
        return jsonify({"error": vali_err.messsage}), 400

    except Exception as error:
        return jsonify({"error": error.message}), 500
    
    hashed_password = bcrypt.generate_password_hash(password)

    # Pegar valor no db
    isUsername = True
    isPassword = True
    isUser = (isUsername and isPassword)

    if isUser == True:
        session['username'] = username
        return redirect(url_for('tasks'))
    else:
        if not isUser:
            response = jsonify({'Error': 'Invalid User'})
            return response, 404 
        else:
            response = jsonify({'Error': 'Wrong Password'})
            return response, 401
           


