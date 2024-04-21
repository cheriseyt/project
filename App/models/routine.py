# routine.py
from App.database import db
from .user import User 
from .workout import Workout

class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    workouts = db.relationship('Workout', secondary='routine_workout', backref=db.backref('routines', lazy='dynamic'))


    def __init__(self, name, user_id, description):
        self.name = name
        self.user_id = user_id
        self.description = description

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'description': self.description,
            'workouts': [workout.get_json() for workout in self.workouts]
        }
