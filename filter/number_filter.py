import re

class NumberFilter:
    
    @staticmethod
    def run(text: str) -> str:
        patterns = [
            r'\b\d+\.\d+\b',
            r'\b\d+\b'
        ]
        
        result = text
        for pattern in patterns:
            result = re.sub(pattern, '[NUMBER]', result)
        
        return result 