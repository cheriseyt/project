from App.database import db
from App.models import Routine, Workout, User


def create_routine(name, description, user_id, workout_ids):
    new_routine = Routine(name=name, description=description, user_id=user_id)
    db.session.add(new_routine)

    for workout_id in workout_ids:
        workout = Workout.query.get(workout_id)
        if workout:
            new_routine.workouts.append(workout)
    
    db.session.commit()
    return new_routine

def get_routine_id(user_id, routine_id):
    routine = Routine.query.filter_by(user_id=user_id, id=routine_id).first()
    if routine:
        return routine.id
    else:
        return None

def remove_workout_from_routine(routine_id, workout_id):
    routine = Routine.query.get(routine_id)
    workout = Workout.query.get(workout_id)
    if routine is None or workout is None:
        return False, "Routine or Workout not found"

    if workout in routine.workouts:
        routine.workouts.remove(workout)
        db.session.commit()
        return True
    else:
        return False

def add_workout_to_routine(routine_id, workout_id):
    routine = Routine.query.get(routine_id)
    workout = Workout.query.get(workout_id)
    if not routine or not workout:
        return False

    if workout not in routine.workouts:
        routine.workouts.append(workout)
        db.session.commit()
        return True
    else:
        return False

def get_routines(user_id):
    return Routine.query.filter_by(user_id=user_id).all()