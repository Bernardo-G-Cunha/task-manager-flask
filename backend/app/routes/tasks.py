from flask import Blueprint, request, render_template, url_for

tasks = Blueprint('tasks', __name__, template_folder='templates')


@tasks.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        return render_template('tasks.html')

    if request.method == 'POST':
        
        print() 
       
    return

@tasks.route('/tasks/create')
def create_task():
    
    return

@tasks.route('/tasks/edit', methods=['GET', 'PUT'])
def edit_task():

    return
