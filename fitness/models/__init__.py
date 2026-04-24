"""
Database models for ProFitness
Organized for better maintainability and SOLID principles
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, Enum
from datetime import datetime
from fitness import db, login_manager
from flask_login import UserMixin
import enum


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))


class ExerciseCategory(enum.Enum):
    """Exercise categories"""
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    YOGA = "yoga"


class DifficultyLevel(enum.Enum):
    """Exercise difficulty levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class WorkoutType(enum.Enum):
    """Workout types"""
    CARDIO = "cardio"
    STRENGTH = "strength"
    MIXED = "mixed"
    FLEXIBILITY = "flexibility"
    YOGA = "yoga"


# ============================================================================
# USER MODEL
# ============================================================================
class User(db.Model, UserMixin):
    """User model with profile information and relationships"""
    __tablename__ = 'User'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Fitness stats
    user_perk = db.Column(db.Integer, default=0)
    calories_consumed = db.Column(db.Integer, default=0)
    calories_burned = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workout_history = db.relationship('WorkoutHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    user_stats = db.relationship('UserStats', backref='user', lazy=True, cascade='all, delete-orphan', uselist=False)
    todos = db.relationship('Todo', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"User('{self.first_name} {self.last_name}', '{self.email}')"


# ============================================================================
# EXERCISE MODEL
# ============================================================================
class Exercise(db.Model):
    """Exercise library model"""
    __tablename__ = 'Exercise'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.Enum(ExerciseCategory), nullable=False)
    muscle_group = db.Column(db.String(100), nullable=True)
    difficulty = db.Column(db.Enum(DifficultyLevel), nullable=False)
    equipment = db.Column(db.String(100), nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    video_url = db.Column(db.String(200), nullable=True)
    image_url = db.Column(db.String(200), nullable=True)
    calories_per_minute = db.Column(db.Integer, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', backref='exercise', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"Exercise('{self.name}', {self.category.value}, {self.difficulty.value})"


# ============================================================================
# WORKOUT HISTORY MODEL
# ============================================================================
class WorkoutHistory(db.Model):
    """Track user workouts"""
    __tablename__ = 'WorkoutHistory'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    workout_name = db.Column(db.String(100), nullable=False)
    workout_type = db.Column(db.Enum(WorkoutType), nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=True)
    calories_burned = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    date_completed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    exercises = db.relationship('WorkoutExercise', backref='workout', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"WorkoutHistory('{self.workout_name}', {self.calories_burned}cal)"


# ============================================================================
# WORKOUT EXERCISE MODEL (Join Table)
# ============================================================================
class WorkoutExercise(db.Model):
    """Track exercises within a workout (with detailed metrics)"""
    __tablename__ = 'WorkoutExercise'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('WorkoutHistory.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('Exercise.id'), nullable=False)
    
    # Exercise metrics (flexible - not all fields needed for every exercise)
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)
    distance = db.Column(db.Float, nullable=True)
    calories = db.Column(db.Integer, nullable=True)
    
    # Order within workout
    order = db.Column(db.Integer, nullable=False)
    
    # Timestamp
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"WorkoutExercise(exercise_id={self.exercise_id}, workout_id={self.workout_id})"


# ============================================================================
# USER STATS MODEL (Track daily stats)
# ============================================================================
class UserStats(db.Model):
    """Daily user statistics"""
    __tablename__ = 'UserStats'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False, unique=True)
    
    # Daily totals
    total_workouts = db.Column(db.Integer, default=0)
    total_calories_burned = db.Column(db.Integer, default=0)
    total_calories_consumed = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"UserStats(user_id={self.user_id}, calories_burned={self.total_calories_burned})"


# ============================================================================
# TODO MODEL
# ============================================================================
class Todo(db.Model):
    """Todo/Task list for users"""
    __tablename__ = 'Todo'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Todo('{self.title}', completed={self.completed})"


# ============================================================================
# LEGACY: USER STATS (Keep for backward compatibility during migration)
# ============================================================================
class UserData(db.Model):
    """Legacy daily stats - for backward compatibility"""
    __tablename__ = 'UserData'
    
    dataId = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    consumed = db.Column(db.Integer, nullable=True)
    burned = db.Column(db.Integer, nullable=True)
    cardio = db.Column(db.Integer, nullable=True)
    strength = db.Column(db.Integer, nullable=True)
    rest = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)

    def __repr__(self):
        return f"UserData(date={self.date}, user_id={self.user_id})"
