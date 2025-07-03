import re

class DateFilter:
    
    @staticmethod 
    def run(text: str) -> str:
        patterns = [
            r'\b\d{4}-\d{2}-\d{2}\b',
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',
            r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
            r'\b\d{1,2}-\d{1,2}-\d{4}\b'
        ]
        
        result = text
        for pattern in patterns:
            result = re.sub(pattern, '[DATE]', result)
        
        return result