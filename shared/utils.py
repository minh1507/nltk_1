"""
Shared Utilities for Study Projects
Common functions and helpers used across multiple exercises
"""

import os
import sys
from pathlib import Path

class ProjectUtils:
    """Utility functions for project management"""
    
    @staticmethod
    def get_project_root():
        """Get the root directory of the project"""
        return Path(__file__).parent.parent
    
    @staticmethod
    def get_exercise_path(exercise_name):
        """Get path to specific exercise directory"""
        root = ProjectUtils.get_project_root()
        return root / "exercises" / exercise_name
    
    @staticmethod
    def add_exercise_to_path(exercise_name):
        """Add exercise directory to Python path"""
        exercise_path = ProjectUtils.get_exercise_path(exercise_name)
        if exercise_path.exists():
            sys.path.insert(0, str(exercise_path))
        else:
            raise FileNotFoundError(f"Exercise '{exercise_name}' not found")
    
    @staticmethod
    def list_exercises():
        """List all available exercises"""
        root = ProjectUtils.get_project_root()
        exercises_dir = root / "exercises"
        if exercises_dir.exists():
            return [d.name for d in exercises_dir.iterdir() if d.is_dir()]
        return []

class FileUtils:
    """File and directory utilities"""
    
    @staticmethod
    def ensure_directory(path):
        """Create directory if it doesn't exist"""
        Path(path).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def read_text_file(file_path):
        """Read text file with encoding handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
    
    @staticmethod
    def write_text_file(file_path, content):
        """Write text file with UTF-8 encoding"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

class ExerciseTemplate:
    """Template for creating new exercises"""
    
    @staticmethod
    def create_exercise_structure(exercise_name, exercise_title):
        """Create directory structure for new exercise"""
        root = ProjectUtils.get_project_root()
        exercise_dir = root / "exercises" / exercise_name
        
        # Create directories
        dirs_to_create = [
            exercise_dir,
            exercise_dir / "src",
            exercise_dir / "tests",
            exercise_dir / "data"
        ]
        
        for dir_path in dirs_to_create:
            FileUtils.ensure_directory(dir_path)
        
        # Create basic files
        files_to_create = {
            exercise_dir / "README.md": ExerciseTemplate._readme_template(exercise_name, exercise_title),
            exercise_dir / "main.py": ExerciseTemplate._main_template(),
            exercise_dir / "requirements.txt": "# Add your dependencies here\n",
            exercise_dir / "src" / "__init__.py": "",
            exercise_dir / "tests" / "__init__.py": "",
            exercise_dir / "tests" / "test_main.py": ExerciseTemplate._test_template()
        }
        
        for file_path, content in files_to_create.items():
            FileUtils.write_text_file(file_path, content)
        
        return exercise_dir
    
    @staticmethod
    def _readme_template(exercise_name, exercise_title):
        return f"""# {exercise_title}

## 📋 **Problem Description**

[Describe the problem and objectives here]

## 🎯 **Objectives**

- [ ] Objective 1
- [ ] Objective 2
- [ ] Objective 3

## 🚀 **Usage**

```bash
cd exercises/{exercise_name}
pip install -r requirements.txt
python main.py
```

## 🛠️ **Technologies**

- Python 3.8+
- [Add your technologies here]

## 📈 **Expected Output**

[Describe expected results]
"""
    
    @staticmethod
    def _main_template():
        return '''"""
Main execution script for the exercise
"""

def main():
    """Main function"""
    print("Exercise starting...")
    
    # Add your code here
    
    print("Exercise completed!")

if __name__ == "__main__":
    main()
'''
    
    @staticmethod
    def _test_template():
        return '''"""
Unit tests for the exercise
"""

import unittest

class TestExercise(unittest.TestCase):
    
    def test_placeholder(self):
        """Placeholder test"""
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()
''' 