import os
from flask import Blueprint, request, make_response, render_template, redirect, url_for, Response, jsonify, session

auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/')
def index():
    return render_template('index.html')


@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
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
           


