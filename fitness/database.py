from sqlalchemy import Column, Integer, String,Boolean, DateTime
from datetime import datetime
from fitness import db, login_manager
from flask_login import UserMixin


# Require user login to query data
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User database model with id, first name, last name, email, password and so on
# that store user information
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(60), nullable=False)
    lname = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    ##image_file = db.Column(db.String(20), unique=True, default='avatar.png')
    password = db.Column(db.String(60), nullable=False)
    post_attribute = db.relationship('Post', backref='author', lazy=True)
    user_data = db.relationship('UserData', backref='user_database', lazy=True)
    # NEW: Added relationship to workout history
    workout_history = db.relationship('WorkoutHistory', backref='user', lazy=True)
    user_perk = db.Column(db.Integer, nullable=False)
    consumed = db.Column(db.Integer, nullable=True)
    burned = db.Column(db.Integer, nullable=True)
    calories = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"User('{self.fname}', '{self.lname}','{self.email}')"
        ##return f"User('{self.email}', '{self.image_file}')"


# Posting database model with id, first name, last name, email, password and so on
# that store user posts
class Post(db.Model):
    __searchable__ = ['title', 'content']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.data_posted}')"


class UserData(db.Model):
    dataId = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.today())
    consumed = db.Column(db.Integer, nullable=True)
    burned = db.Column(db.Integer, nullable=True)
    cardio = db.Column(db.Integer, nullable=True)
    strength = db.Column(db.Integer, nullable=True)
    rest = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # user = db.relationship('User', foreign_keys = user_id)

#to do list db
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


# NEW: Exercise Library Model
class Exercise(db.Model):
    __tablename__ = 'Exercise'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=False)  # strength, cardio, flexibility, yoga
    muscle_group = db.Column(db.String(100), nullable=True)  # chest, back, legs, etc.
    difficulty = db.Column(db.String(20), nullable=False)  # beginner, intermediate, advanced
    equipment = db.Column(db.String(100), nullable=True)  # none, dumbbells, barbell, etc.
    instructions = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    calories_per_minute = db.Column(db.Integer, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Exercise('{self.name}', '{self.category}', '{self.difficulty}')"


# NEW: Workout History Model
class WorkoutHistory(db.Model):
    __tablename__ = 'WorkoutHistory'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_name = db.Column(db.String(100), nullable=False)
    workout_type = db.Column(db.String(50), nullable=False)  # cardio, strength, mixed, etc.
    duration_minutes = db.Column(db.Integer, nullable=True)
    calories_burned = db.Column(db.Integer, nullable=True)
    date_completed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    
    # Relationship to workout exercises
    exercises = db.relationship('WorkoutExercise', backref='workout', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"WorkoutHistory('{self.workout_name}', '{self.date_completed}', '{self.calories_burned}')"


# NEW: Workout Exercise Model (for tracking exercises in a workout)
class WorkoutExercise(db.Model):
    __tablename__ = 'WorkoutExercise'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('WorkoutHistory.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)  # in kg/lbs
    duration_seconds = db.Column(db.Integer, nullable=True)  # for timed exercises
    distance = db.Column(db.Float, nullable=True)  # for cardio exercises
    calories = db.Column(db.Integer, nullable=True)
    order = db.Column(db.Integer, nullable=False)  # exercise order in workout
    
    # Relationship to exercise
    exercise = db.relationship('Exercise', backref='workout_exercises')
    
    def __repr__(self):
        return f"WorkoutExercise('{self.exercise_id}', 'Sets: {self.sets}', 'Reps: {self.reps}')"


#create plan db
# class Exercise(db.Model)
#     name= db.Column(db.String(60), nullable=False)


class Plan(db.Model):
    __tablename__='Plan'

    plan_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String(60), nullable=False)
    detail = db.Column(db.String(200))
    rep = db.Column(db.Integer, nullable=False)
    Set = db.Column(db.Integer, nullable=False)
    complete = db.Column(db.Boolean)
    create_date = db.Column(DateTime,default=datetime.now())


if __name__ == '__main__':
    db.create_all()



