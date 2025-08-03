from __future__ import print_function
from flask import redirect, url_for, render_template, flash, request, session, make_response, jsonify
from fitness import app, db, bcrypt
from fitness.forms import SignInForm, SignUpForm, itemForm, calorieForm, CalorieWorkoutForm, UserProfileForm
from fitness.database import User, Post, load_user, UserData, Todo, Exercise, WorkoutHistory, WorkoutExercise
from flask_login import current_user, login_user, current_user, logout_user, login_required
from fitness import nix
from fitness.createplan import *
from time import time
from datetime import date, datetime
import json
import sys
import os


# Get the user database for routes
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}


# Default route
@app.route("/")
def index():
    db.create_all()
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


# Protected route for user id and user consumed
@app.route("/protected")
def protected():
    return str(current_user.id)
    return str(current_user.consumed)


# Route for home page
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

# Route for log out direction which is home page
@app.route("/logout")
@login_required
def logout():
    session.pop('fname')
    session.pop('id')
    logout_user()
    return redirect(url_for("home"))


# Route of user after they logged in
@app.route("/user")
@login_required
def user():
    total, monthly_calories, perk, achievement = calculate_workout()
    return render_template('user_dashboard.html', total=total, monthly_calories=monthly_calories, perk=perk,
                            achievement=achievement)

# Route for user profile page
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UserProfileForm(original_email=current_user.email)
    if form.validate_on_submit():
        # Verify current password
        if bcrypt.check_password_hash(current_user.password, form.current_password.data):
            # Update user information
            current_user.fname = form.first_name.data
            current_user.lname = form.last_name.data
            current_user.email = form.email.data
            
            # Update password if provided
            if form.new_password.data:
                current_user.password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            
            # Update session
            session['fname'] = current_user.fname
            
            db.session.commit()
            flash('Your profile has been updated successfully!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Current password is incorrect!', 'danger')
    
    elif request.method == 'GET':
        form.first_name.data = current_user.fname
        form.last_name.data = current_user.lname
        form.email.data = current_user.email
    
    total, monthly_calories, perk, achievement = calculate_workout()
    return render_template('profile.html', form=form, total=total, monthly_calories=monthly_calories, 
                         perk=perk, achievement=achievement)

#Route to contact page 
@app.route("/contact")
def contact():
    return render_template("contact.html")


# Route for cardio workout
@app.route("/cardio", methods=['GET', 'POST'])
@login_required
def cardio():
    form = CalorieWorkoutForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=session['id']).first()
        user_data = UserData(cardio=int(form.cardio_wo.data), user_id=session['id'])
        db.session.add(user_data)
        db.session.commit()
        return redirect(url_for('cardio'))
    total, monthly_calories, perk, achievement = calculate_workout()
    return render_template('cardio.html', form=form, total=total, monthly_calories=monthly_calories, perk=perk,
                            achievement=achievement)


# Route for strength workout
@app.route("/strength")
@login_required
def strength():
    total, monthly_calories, perk, achievement = calculate_workout()
    return render_template('strength.html', total=total, monthly_calories=monthly_calories, perk=perk, achievement=achievement)


# Route for clothes shopping
@app.route("/clothes")
@login_required
def clothes():
    total, monthly_calories, perk, achievement = calculate_workout()
    return render_template('clothes.html', total=total, monthly_calories=monthly_calories, perk=perk, achievement=achievement)


# Route for equipment shopping
@app.route("/equipment")
@login_required
def gift():
    total, monthly_calories, perk, achievement = calculate_workout()
    return render_template('equipment.html', total=total, monthly_calories=monthly_calories, perk=perk,
                            achievement=achievement)


# Route for supplement shopping
@app.route("/supplement")
@login_required
def supplement():
    total, monthly_calories, perk, achievement = calculate_workout()
    return render_template('supplement.html', total=total, monthly_calories=monthly_calories, perk=perk,
                        achievement=achievement)


# Sign up function for user with fields
# and store them database
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fname=form.first_name.data, lname=form.last_name.data, email=form.email.data,
                    password=hash_password, user_perk=250, consumed=0, burned=0, calories=0)
        db.session.add(user)
        db.session.commit()
        flash(f'Thank you for signing up with us', 'success')
        return redirect(url_for('signin'))
    return render_template('signup.html', title='Register', form=form)


# Sign up function for user with fields
# and query input information to database
# if the input match, the user will log in.
# Otherwise, error message will display
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            session['id'] = user.id
            session['fname'] = user.fname
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('signin.html', form=form)


@login_required
def calculate_workout():
    achievement_max = 1500
    get_all = UserData.query.filter_by(user_id=session['id']).all()
    total_cardio = 0
    total_strength = 0
    total_cardio_m = 0
    total_strength_m = 0
    now = date.today()
    day = now.strftime("%d")
    month = now.strftime("%m")
    for item in get_all:
        # Get the daily calories
        day1 = item.date.strftime("%d")
        if item.cardio is not None and day == day1:
            total_cardio = total_cardio + item.cardio
        if item.strength is not None and day == day1:
            total_strength = total_strength + item.strength
        # Get the monthly calories
        month1 = item.date.strftime("%m")
        if item.cardio is not None and month == month1:
            total_cardio_m = total_cardio_m + item.cardio
        if item.strength is not None and month == month1:
            total_strength_m = total_strength_m + item.strength
    total = total_strength + total_cardio
    monthly_calories = total_strength_m + total_cardio_m
    user = User.query.filter_by(id=session['id']).first()
    perk = user.user_perk
    achievement = int((total / achievement_max) * 100)
    if achievement > 100:
        achievement = 100
        perk += 50
    user.user_perk += perk
    return total, monthly_calories, perk, achievement

@app.route('/pomodoroTimer')
@login_required
def pomodoroTimer():
    title = 'Workout Timer'
    return render_template("pomodoroTimer.html", title=title)

@app.route("/delete")
@login_required
def delete():
    session.pop('fname')
    session.pop('id')
    logout_user()
    flash('Your account is deleted', 'error')
    return redirect("/signin")


@app.route("/todolist")
@login_required
def todoList():
    todo_list = Todo.query.all()
    return render_template("todolist.html", todo_list=todo_list)

@app.route("/add", methods=["POST"])
@login_required
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todoList"))

@app.route("/update/<int:todo_id>")
@login_required
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todoList"))

@app.route("/delete/<int:todo_id>")
@login_required
def deletetodo(todo_id):   
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todoList"))

@app.route("/admin")
def workoutplan():
    total, monthly_calories, perk, achievement = calculate_workout()
    return render_template('tracker.html', total=total, monthly_calories=monthly_calories, perk=perk, achievement=achievement)

# Exercise Library Routes
@app.route("/exercises")
@login_required
def exercise_library():
    """Display all exercises with filtering options"""
    category = request.args.get('category', '')
    muscle_group = request.args.get('muscle_group', '')
    difficulty = request.args.get('difficulty', '')
    
    # Build query with filters
    query = Exercise.query
    
    if category:
        query = query.filter(Exercise.category == category)
    if muscle_group:
        query = query.filter(Exercise.muscle_group.contains(muscle_group))
    if difficulty:
        query = query.filter(Exercise.difficulty == difficulty)
    
    exercises = query.order_by(Exercise.name).all()
    
    # Get unique values for filter dropdowns
    categories = db.session.query(Exercise.category).distinct().all()
    muscle_groups = db.session.query(Exercise.muscle_group).distinct().all()
    difficulties = db.session.query(Exercise.difficulty).distinct().all()
    
    return render_template('exercise_library.html', 
                        exercises=exercises,
                        categories=[c[0] for c in categories if c[0]],
                        muscle_groups=[m[0] for m in muscle_groups if m[0]],
                        difficulties=[d[0] for d in difficulties if d[0]],
                        current_filters={'category': category, 'muscle_group': muscle_group, 'difficulty': difficulty})

@app.route("/exercise/<int:exercise_id>")
@login_required
def exercise_detail(exercise_id):
    """Display detailed information about a specific exercise"""
    exercise = Exercise.query.get_or_404(exercise_id)
    return render_template('exercise_detail.html', exercise=exercise)

@app.route("/exercises/search")
@login_required
def exercise_search():
    """Search exercises by name or description"""
    query = request.args.get('q', '')
    if query:
        exercises = Exercise.query.filter(
            (Exercise.name.contains(query)) | 
            (Exercise.description.contains(query)) |
            (Exercise.muscle_group.contains(query))
        ).order_by(Exercise.name).all()
    else:
        exercises = []
    
    return render_template('exercise_search.html', exercises=exercises, query=query)

# Workout history routes

@app.route("/workout-history")
@login_required
def workout_history():
    """Display user's workout history with statistics"""
    # Get user's workout history
    workouts = WorkoutHistory.query.filter_by(user_id=current_user.id).order_by(WorkoutHistory.date_completed.desc()).all()
    
    # Calculate statistics
    total_workouts = len(workouts)
    total_calories = sum(w.calories_burned or 0 for w in workouts)
    total_duration = sum(w.duration_minutes or 0 for w in workouts)
    
    # Get recent workouts (last 10)
    recent_workouts = workouts[:10]
    
    # Get workout types distribution
    workout_types = {}
    for workout in workouts:
        workout_type = workout.workout_type
        workout_types[workout_type] = workout_types.get(workout_type, 0) + 1
    
    return render_template('workout_history.html', 
                        workouts=recent_workouts,
                        total_workouts=total_workouts,
                        total_calories=total_calories,
                        total_duration=total_duration,
                        workout_types=workout_types)

@app.route("/workout/<int:workout_id>")
@login_required
def workout_detail(workout_id):
    """Display detailed information about a specific workout"""
    workout = WorkoutHistory.query.get_or_404(workout_id)
    
    # Ensure user can only view their own workouts
    if workout.user_id != current_user.id:
        flash('You can only view your own workouts.', 'danger')
        return redirect(url_for('workout_history'))
    
    return render_template('workout_detail.html', workout=workout)

@app.route("/set-workout", methods=['GET', 'POST'])
@login_required
def set_workout():
    """Set a new workout"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            # Create new workout
            workout = WorkoutHistory(
                user_id=current_user.id,
                workout_name=data.get('workout_name', 'Custom Workout'),
                workout_type=data.get('workout_type', 'mixed'),
                duration_minutes=data.get('duration_minutes'),
                calories_burned=data.get('calories_burned'),
                notes=data.get('notes', '')
            )
            
            db.session.add(workout)
            db.session.flush()  # Get the workout ID
            
            # Add exercises to workout
            exercises_data = data.get('exercises', [])
            for i, exercise_data in enumerate(exercises_data):
                workout_exercise = WorkoutExercise(
                    workout_id=workout.id,
                    exercise_id=exercise_data.get('exercise_id'),
                    sets=exercise_data.get('sets'),
                    reps=exercise_data.get('reps'),
                    weight=exercise_data.get('weight'),
                    duration_seconds=exercise_data.get('duration_seconds'),
                    distance=exercise_data.get('distance'),
                    calories=exercise_data.get('calories'),
                    order=i + 1
                )
                db.session.add(workout_exercise)
            
            db.session.commit()
            
            # Update user's burned calories
            if workout.calories_burned:
                current_user.burned = (current_user.burned or 0) + workout.calories_burned
                current_user.calories = (current_user.consumed or 0) - current_user.burned
                db.session.commit()
            
            return jsonify({'success': True, 'workout_id': workout.id})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'error': str(e)})
    
    # GET request - show form
    exercises = Exercise.query.order_by(Exercise.name).all()
    return render_template('set_workout.html', exercises=exercises)

@app.route("/api/exercises")
@login_required
def api_exercises():
    """API endpoint to get exercises for AJAX requests"""
    category = request.args.get('category', '')
    muscle_group = request.args.get('muscle_group', '')
    
    query = Exercise.query
    
    if category:
        query = query.filter(Exercise.category == category)
    if muscle_group:
        query = query.filter(Exercise.muscle_group.contains(muscle_group))
    
    exercises = query.order_by(Exercise.name).all()
    
    return jsonify([{
        'id': ex.id,
        'name': ex.name,
        'category': ex.category,
        'muscle_group': ex.muscle_group,
        'difficulty': ex.difficulty,
        'equipment': ex.equipment,
        'calories_per_minute': ex.calories_per_minute
    } for ex in exercises])

# NEW: Admin route to populate exercise database (for initial setup)
@app.route("/admin/populate-exercises")
@login_required
def populate_exercises():
    """Populate the exercise database with sample exercises"""
    # Check if exercises already exist
    if Exercise.query.first():
        flash('Exercise database already populated!', 'info')
        return redirect(url_for('exercise_library'))
    
    # Sample exercises data
    sample_exercises = [
        # Strength exercises
        {
            'name': 'Push-ups',
            'description': 'A classic bodyweight exercise that targets chest, shoulders, and triceps.',
            'category': 'strength',
            'muscle_group': 'chest, shoulders, triceps',
            'difficulty': 'beginner',
            'equipment': 'none',
            'instructions': '1. Start in a plank position\n2. Lower your body until your chest nearly touches the floor\n3. Push back up to the starting position',
            'calories_per_minute': 8
        },
        {
            'name': 'Squats',
            'description': 'A fundamental lower body exercise that targets quads, hamstrings, and glutes.',
            'category': 'strength',
            'muscle_group': 'legs, glutes',
            'difficulty': 'beginner',
            'equipment': 'none',
            'instructions': '1. Stand with feet shoulder-width apart\n2. Lower your body as if sitting back into a chair\n3. Keep your chest up and knees behind toes\n4. Return to standing position',
            'calories_per_minute': 10
        },
        {
            'name': 'Pull-ups',
            'description': 'An upper body exercise that targets back and biceps.',
            'category': 'strength',
            'muscle_group': 'back, biceps',
            'difficulty': 'intermediate',
            'equipment': 'pull-up bar',
            'instructions': '1. Hang from a pull-up bar with hands shoulder-width apart\n2. Pull your body up until your chin is over the bar\n3. Lower back down with control',
            'calories_per_minute': 12
        },
        # Cardio exercises
        {
            'name': 'Running',
            'description': 'A high-intensity cardiovascular exercise that improves endurance.',
            'category': 'cardio',
            'muscle_group': 'legs, cardiovascular',
            'difficulty': 'beginner',
            'equipment': 'none',
            'instructions': '1. Start with a light warm-up\n2. Maintain good posture with chest up\n3. Land midfoot and keep a steady pace',
            'calories_per_minute': 15
        },
        {
            'name': 'Jumping Jacks',
            'description': 'A full-body cardio exercise that gets your heart rate up quickly.',
            'category': 'cardio',
            'muscle_group': 'full body',
            'difficulty': 'beginner',
            'equipment': 'none',
            'instructions': '1. Start standing with feet together and arms at sides\n2. Jump feet apart while raising arms overhead\n3. Jump back to starting position',
            'calories_per_minute': 10
        },
        # Flexibility exercises
        {
            'name': 'Downward Dog',
            'description': 'A yoga pose that stretches the entire body and improves flexibility.',
            'category': 'flexibility',
            'muscle_group': 'full body',
            'difficulty': 'beginner',
            'equipment': 'none',
            'instructions': '1. Start on hands and knees\n2. Lift hips up and back, forming an inverted V\n3. Press heels toward the ground',
            'calories_per_minute': 3
        },
        {
            'name': 'Child\'s Pose',
            'description': 'A relaxing yoga pose that stretches the back and hips.',
            'category': 'flexibility',
            'muscle_group': 'back, hips',
            'difficulty': 'beginner',
            'equipment': 'none',
            'instructions': '1. Kneel on the floor with big toes touching\n2. Sit back on heels and fold forward\n3. Extend arms forward and rest forehead on floor',
            'calories_per_minute': 2
        }
    ]
    
    # Add exercises to database
    for exercise_data in sample_exercises:
        exercise = Exercise(**exercise_data)
        db.session.add(exercise)
    
    try:
        db.session.commit()
        flash(f'Successfully added {len(sample_exercises)} exercises to the database!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error populating exercises: {str(e)}', 'danger')
    
    return redirect(url_for('exercise_library'))

