#!/usr/bin/env python3
"""
Study Projects Manager
Utility script for managing multiple exercises and the web dashboard
"""

import os
import sys
import subprocess
from pathlib import Path
from shared.utils import ProjectUtils, ExerciseTemplate

class StudyProjectManager:
    
    def __init__(self):
        self.root = ProjectUtils.get_project_root()
        
    def list_exercises(self):
        """List all available exercises"""
        exercises = ProjectUtils.list_exercises()
        print("\n📚 Available Exercises:")
        print("=" * 40)
        
        if not exercises:
            print("No exercises found.")
            return
            
        for i, exercise in enumerate(exercises, 1):
            print(f"{i:2d}. {exercise}")
        
        print("\n💻 Web Dashboard: web_dashboard/")
        print("=" * 40)
    
    def run_exercise(self, exercise_name):
        """Run a specific exercise"""
        exercise_path = self.root / "exercises" / exercise_name
        
        if not exercise_path.exists():
            print(f"❌ Exercise '{exercise_name}' not found!")
            return False
        
        main_file = exercise_path / "main.py"
        if not main_file.exists():
            print(f"❌ main.py not found in '{exercise_name}'!")
            return False
        
        print(f"🚀 Running {exercise_name}...")
        try:
            # Change to exercise directory and run
            original_cwd = os.getcwd()
            os.chdir(exercise_path)
            subprocess.run([sys.executable, "main.py"], check=True)
            os.chdir(original_cwd)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running exercise: {e}")
            return False
        except KeyboardInterrupt:
            print("\n⏹️ Exercise interrupted by user")
            return False
        finally:
            os.chdir(original_cwd)
    
    def start_web_dashboard(self):
        """Start the web dashboard"""
        dashboard_path = self.root / "web_dashboard"
        
        if not dashboard_path.exists():
            print("❌ Web dashboard not found!")
            return False
        
        run_file = dashboard_path / "run.py"
        if not run_file.exists():
            print("❌ run.py not found in web dashboard!")
            return False
        
        print("🌐 Starting Web Dashboard...")
        print("📍 URL: http://localhost:5000")
        print("⏹️  Press Ctrl+C to stop")
        
        try:
            original_cwd = os.getcwd()
            os.chdir(dashboard_path)
            subprocess.run([sys.executable, "run.py"], check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error starting dashboard: {e}")
            return False
        except KeyboardInterrupt:
            print("\n⏹️ Dashboard stopped by user")
            return False
        finally:
            os.chdir(original_cwd)
    
    def create_exercise(self, exercise_name, exercise_title):
        """Create a new exercise from template"""
        if not exercise_name.startswith("ex"):
            # Auto-generate exercise number
            existing = ProjectUtils.list_exercises()
            numbers = []
            for ex in existing:
                if ex.startswith("ex") and "_" in ex:
                    try:
                        num = int(ex.split("_")[0][2:])
                        numbers.append(num)
                    except ValueError:
                        continue
            
            next_num = max(numbers, default=0) + 1
            exercise_name = f"ex{next_num:02d}_{exercise_name}"
        
        exercise_dir = ExerciseTemplate.create_exercise_structure(exercise_name, exercise_title)
        print(f"✅ Created exercise: {exercise_name}")
        print(f"📁 Location: {exercise_dir}")
        return exercise_dir
    
    def interactive_menu(self):
        """Interactive menu for project management"""
        while True:
            print("\n" + "="*50)
            print("📚 STUDY PROJECTS MANAGER")
            print("="*50)
            print("1. 📋 List exercises")
            print("2. 🚀 Run exercise")
            print("3. 🌐 Start web dashboard")
            print("4. ➕ Create new exercise")
            print("5. ❌ Exit")
            print("="*50)
            
            choice = input("Select option (1-5): ").strip()
            
            if choice == "1":
                self.list_exercises()
            
            elif choice == "2":
                exercises = ProjectUtils.list_exercises()
                if not exercises:
                    print("❌ No exercises available!")
                    continue
                
                print("\nAvailable exercises:")
                for i, ex in enumerate(exercises, 1):
                    print(f"{i}. {ex}")
                
                try:
                    idx = int(input("Select exercise number: ")) - 1
                    if 0 <= idx < len(exercises):
                        self.run_exercise(exercises[idx])
                    else:
                        print("❌ Invalid selection!")
                except ValueError:
                    print("❌ Please enter a number!")
            
            elif choice == "3":
                self.start_web_dashboard()
            
            elif choice == "4":
                name = input("Exercise name (without ex prefix): ").strip()
                title = input("Exercise title: ").strip()
                if name and title:
                    self.create_exercise(name, title)
                else:
                    print("❌ Name and title are required!")
            
            elif choice == "5":
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice!")

def main():
    """Main function"""
    manager = StudyProjectManager()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "list":
            manager.list_exercises()
        
        elif command == "run":
            if len(sys.argv) > 2:
                manager.run_exercise(sys.argv[2])
            else:
                print("❌ Please specify exercise name!")
        
        elif command == "web":
            manager.start_web_dashboard()
        
        elif command == "create":
            if len(sys.argv) > 3:
                manager.create_exercise(sys.argv[2], sys.argv[3])
            else:
                print("❌ Usage: python project_manager.py create <name> <title>")
        
        else:
            print("❌ Unknown command!")
            print("Usage: python project_manager.py [list|run|web|create]")
    
    else:
        # Interactive mode
        manager.interactive_menu()

if __name__ == "__main__":
    main() 