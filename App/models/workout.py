from App.database import db

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.Integer)
    difficulty = db.Column(db.String(50))
    calories_burned = db.Column(db.Integer)
    muscle_group = db.Column(db.String(100))
    image = db.Column(db.String(255))
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'))

    def __init__(self, name, description, duration, difficulty, calories_burned, muscle_group, image):
        self.name = name
        self.description = description
        self.duration = duration
        self.difficulty = difficulty
        self.calories_burned = calories_burned
        self.muscle_group = muscle_group
        self.image = image

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'duration': self.duration,
            'difficulty': self.difficulty,
            'calories_burned': self.calories_burned,
            'muscle_group': self.muscle_group,
            'image': self.image
        }
