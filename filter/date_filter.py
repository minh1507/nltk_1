import re
from datetime import datetime
from typing import List, Tuple

class DateFilter:
    
    @staticmethod
    def detect(text: str) -> List[Tuple[str, str]]:
        date_patterns = [
            (r'\b\d{4}-\d{2}-\d{2}\b', '%Y-%m-%d'),
            (r'\b\d{1,2}/\d{1,2}/\d{4}\b', '%m/%d/%Y'),
            (r'\b\d{1,2}-\d{1,2}-\d{4}\b', '%m-%d-%Y'),
            (r'\b\d{1,2}/\d{1,2}/\d{4}\b', '%d/%m/%Y'),
            (r'\b\d{1,2}-\d{1,2}-\d{4}\b', '%d-%m-%Y'),
            (r'\b\d{1,2}\.\d{1,2}\.\d{4}\b', '%d.%m.%Y'),
            (r'\b\d{4}/\d{1,2}/\d{1,2}\b', '%Y/%m/%d'),
            (r'\b\d{4}-\d{2}-\d{2}\s+\d{1,2}:\d{2}:\d{2}\b', '%Y-%m-%d %H:%M:%S'),
            (r'\b\d{1,2}/\d{1,2}/\d{4}\s+\d{1,2}:\d{2}\b', '%m/%d/%Y %H:%M'),
        ]
        
        found_dates = []
        
        for pattern, date_format in date_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    parsed_date = datetime.strptime(match, date_format)
                    standardized = parsed_date.strftime('%Y-%m-%d')
                    found_dates.append((match, standardized))
                except ValueError:
                    if date_format in ['%m/%d/%Y', '%d/%m/%Y']:
                        alt_format = '%d/%m/%Y' if date_format == '%m/%d/%Y' else '%m/%d/%Y'
                        try:
                            parsed_date = datetime.strptime(match, alt_format)
                            standardized = parsed_date.strftime('%Y-%m-%d')
                            found_dates.append((match, standardized))
                        except ValueError:
                            pass
        
        return found_dates

    @staticmethod
    def replace(text: str, dates: List[Tuple[str, str]]) -> str:
        modified_text = text
        
        for original_match, _ in dates:
            modified_text = modified_text.replace(original_match, "[DATE]")
        
        return modified_text

    @staticmethod
    def run(input_text: str) -> str:
        detected_dates = DateFilter.detect(input_text)
        modified_text = DateFilter.replace(input_text, detected_dates)
        
        return modified_text