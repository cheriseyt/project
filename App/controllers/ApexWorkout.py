from App.models import Workout
from App.database import db
import csv

def create_workouts():
    with open('/workspace/project/App/ApexWorkouts.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            new_workout = Workout(
                name=row['name'],
                description=row['description'],
                duration=int(row['duration']),
                difficulty=row['difficulty'],
                calories_burned=int(row['calories_burned']),
                muscle_group=row['muscle_group'],
                image=row['image']
                
            )
            db.session.add(new_workout)
    db.session.commit()
    return Workout

def get_workouts():
    return Workout.query.all()

def get_workout_ID(workout_id):
    return Workout.query.get(workout_id)