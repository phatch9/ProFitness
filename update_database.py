#!/usr/bin/env python3
"""
Database Update Script for ProFitness
This script adds the new Exercise and WorkoutHistory tables to the database.
"""

import os
import sys

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fitness import app, db
from fitness.models import Exercise, WorkoutHistory, WorkoutExercise

def update_database():
    """Update the database with new tables"""
    print("🔄 Updating ProFitness database...")
    
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Check if exercises already exist
            existing_exercises = Exercise.query.count()
            if existing_exercises == 0:
                print("📝 No exercises found. You can populate the database by visiting:")
                print("   http://localhost:8000/admin/populate-exercises")
            else:
                print(f"📊 Found {existing_exercises} exercises in the database.")
            
            print("\n🎉 Database update completed!")
            print("\nNew features available:")
            print("  • Exercise Library: /exercises")
            print("  • Workout History: /workout-history")
            print("  • Log Workout: /log-workout")
            
        except Exception as e:
            print(f"❌ Error updating database: {e}")
            return False
    
    return True

if __name__ == "__main__":
    update_database() 