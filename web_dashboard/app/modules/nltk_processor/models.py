import sys
import os
from pathlib import Path

# Add the exercise path to Python path
project_root = Path(__file__).parent.parent.parent.parent.parent
exercise_path = project_root / "exercises" / "ex01_nltk_text_processor"
sys.path.insert(0, str(exercise_path))

from filter import Filter
from processing import Processing

class NLTKTextProcessor:
    
    @staticmethod
    def process_text(input_text):
        if not input_text or not input_text.strip():
            return []
        
        try:
            filtered = Filter.create(input_text).date().number().result()
            process = Processing.create(filtered)
            tokens = process.split().unique(space=True, count=True).tag().sort(by="alpha", reverse=False).result()
            return tokens
        except Exception as e:
            print(f"Error processing text: {e}")
            return []
    
    @staticmethod
    def format_tokens_for_display(tokens):
        if not tokens:
            return []
        
        formatted = []
        for token_data in tokens:
            if len(token_data) == 3:
                token, tag, count = token_data
                formatted.append({
                    'token': str(token),
                    'tag': str(tag),
                    'count': int(count)
                })
            elif len(token_data) == 2:
                token, count = token_data
                formatted.append({
                    'token': str(token),
                    'tag': 'N/A',
                    'count': int(count)
                })
        
        return formatted 