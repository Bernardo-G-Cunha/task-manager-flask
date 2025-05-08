from flask import Blueprint, request, render_template, url_for, jsonify
from flask import Blueprint, request, make_response, redirect, url_for, Response, jsonify

tasks_bp = Blueprint('tasks', __name__, template_folder='templates')


@tasks_bp.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        return jsonify() #render_template('tasks.html')

    if request.method == 'POST':
        
        print() 
       
    return jsonify()

@tasks_bp.route('/tasks/create', methods=['GET', 'POST'])
def create_task():
    
    return jsonify()

@tasks_bp.route('/tasks/edit', methods=['GET', 'PUT'])
def edit_task():

    return jsonify()
