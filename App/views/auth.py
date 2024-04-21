from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies, create_access_token
from sqlalchemy.exc import IntegrityError
from.index import index_views

from App.controllers import (
    login,
    get_workouts,
    create_user,
    get_workout_ID,
    create_routine,
    get_routines,
    get_routine_id,
    remove_workout_from_routine,
    add_workout_to_routine,
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')


'''
Page/Action Routes
'''    
@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@auth_views.route('/identify', methods=['GET'])
@jwt_required()
def identify_page():
    return render_template('message.html', title="Identify", message=f"You are logged in as {current_user.id} - {current_user.username}")
    

@auth_views.route('/login', methods=['POST'])
def login_action():
    data = request.form
    token = login(data['username'], data['password'])
    response = redirect(url_for('auth_views.homepage'))
    if not token:
        flash('Bad username or password given'), 401
        response = redirect(request.referrer)
    else:
        flash('Login Successful')
        set_access_cookies(response, token) 
    return response

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    response = redirect(url_for('auth_views.index')) 
    flash("Logged Out!")
    unset_jwt_cookies(response)
    return response

@auth_views.route('/homepage', methods=['GET'])
@auth_views.route('/homepage/<int:workout_id>', methods=["GET"])
@jwt_required()
def homepage(workout_id=1):
    workouts = get_workouts()
    selected_workout = get_workout_ID(workout_id)
    username = current_user.username
    return render_template('Homepage.html', workouts=workouts, selected_workout=selected_workout, username=username)

@auth_views.route('/Signup', methods=['GET'])
def Signup():
    return render_template('Signup.html')

@auth_views.route("/Signup", methods=['POST'])
def signup_action():
  try:
    username = request.form['username']
    password = request.form['password']
    user = create_user(username=username, password=password)
    flash('Account created')
    response = redirect(url_for('auth_views.homepage'))
    token = create_access_token(identity=username)
    set_access_cookies(response, token)
    return response

  except IntegrityError:
    flash('Username already exists')
    response = redirect(url_for('auth_views.Signup'))
    return response


@auth_views.route('/routines')
@jwt_required() 
def routines():
    username = current_user.username
    all_routines = get_routines(current_user.id)
    return render_template('routines.html', routines=all_routines,username=username)

@auth_views.route('/remove_workout_from_routine/<int:routine_id>/<int:workout_id>', methods=['POST'])
@jwt_required()
def remove_workout_from_routine_view(routine_id, workout_id):
    success = remove_workout_from_routine(routine_id, workout_id)
    if success:
        flash('success')
    else:
        flash('error')
    return redirect(url_for('auth_views.routines'))

@auth_views.route('/add_workout_to_routine/<int:routine_id>/<int:workout_id>', methods=['POST'])
@jwt_required()
def add_workout_to_routine_view(routine_id, workout_id):
    success = add_workout_to_routine(routine_id, workout_id)
    if success:
        flash('success')
    else:
        flash('error')
    return redirect(url_for('auth_views.routines'))

@auth_views.route('/view_workouts/<int:routine_id>')
@jwt_required()
def view_workouts(routine_id):
    routine_id = get_routine_id(current_user.id, routine_id)
    workouts = get_workouts()  
    return render_template('viewWorkouts.html', routine_id=routine_id, workouts=workouts)


@auth_views.route('/create_routine', methods=['GET', 'POST'])
@jwt_required()
def createRoutines_action():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        workout_ids = request.form['workout_ids'].split(',') 
        routine = create_routine(name, description, current_user.id, workout_ids)
        flash('Routine created successfully!')
        return redirect(url_for('auth_views.routines', routine_id=routine.id))

    workouts = get_workouts()
    return render_template('createRoutine.html', workouts=workouts) 

@auth_views.route('/')
def index():
    return render_template('index.html')


'''
API Routes
'''

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = login(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  response = jsonify(access_token=token) 
  set_access_cookies(response, token)
  return response

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})

@auth_views.route('/api/logout', methods=['GET'])
def logout_api():
    response = jsonify(message="Logged Out!")
    unset_jwt_cookies(response)
    return response