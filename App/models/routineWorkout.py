from App.database import db
from .user import User  
from .workout import Workout

class RoutineWorkout(db.Model):
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'), primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), primary_key=True)