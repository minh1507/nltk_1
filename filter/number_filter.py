import re
from typing import List

class NumberFilter:
    
    @staticmethod
    def detect(text: str) -> List[str]:
        number_patterns = [
            r'\b\d+\.\d+\b', 
            r'\b\d+,\d+\b',   
            r'\b\d+\b'        
        ]
        
        found_numbers = []
        
        for pattern in number_patterns:
            matches = re.findall(pattern, text)
            found_numbers.extend(matches)
        
        return found_numbers

    @staticmethod
    def replace(text: str, numbers: List[str]) -> str:
        modified_text = text
        
        for number in numbers:
            modified_text = modified_text.replace(number, "[NUMBER]")
        
        return modified_text

    @staticmethod
    def run(input_text: str) -> str:
        detected_numbers = NumberFilter.detect(input_text)
        modified_text = NumberFilter.replace(input_text, detected_numbers)
        
        return modified_text 