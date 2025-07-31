#!/usr/bin/env python3
"""
Quick Database Fix for ProFitness
This script creates the new database tables and handles import issues.
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from fitness import app, db
    from fitness.database import Exercise, WorkoutHistory, WorkoutExercise
    print("✅ Successfully imported database models")
except ImportError as e:
    print(f"Import error: {e}")
    print("This might be because the database models haven't been created yet.")
    sys.exit(1)

def fix_database():
    """Create the database tables"""
    print("🔄 Creating database tables...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if exercises exist
            exercise_count = Exercise.query.count()
            print(f"📊 Found {exercise_count} exercises in database")
            
            if exercise_count == 0:
                print("\n💡 To populate with sample exercises, visit:")
                print("   http://localhost:8000/admin/populate-exercises")
            
            print("\n🎉 Database is ready!")
            print("You can now access:")
            print("  • Exercise Library: http://localhost:8000/exercises")
            print("  • Workout History: http://localhost:8000/workout-history")
            
        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            return False
    
    return True

if __name__ == "__main__":
    fix_database() 