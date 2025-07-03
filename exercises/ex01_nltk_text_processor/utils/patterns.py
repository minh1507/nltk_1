import re

class TokenPatterns:
    SPLIT_PATTERN = r'\[NUMBER\]|\[DATE\]|[a-zA-Z]+|\d+|[^\w\s]|\s+'
    ALPHABETIC = r'^[a-zA-Z]+$'
    SPECIAL_TOKEN = r'^\[.*\]$'
    DIGITS_ONLY = r'^\d+$'
    PUNCTUATION = r'^[^\w\s]+$'
    SPACING_EXCLUDE = r'^[^\w\[\]]+$'
    
    @staticmethod
    def is_alphabetic(text):
        return bool(re.match(TokenPatterns.ALPHABETIC, str(text)))
    
    @staticmethod
    def is_special_token(text):
        return bool(re.match(TokenPatterns.SPECIAL_TOKEN, str(text)))
    
    @staticmethod
    def is_digits_only(text):
        return bool(re.match(TokenPatterns.DIGITS_ONLY, str(text)))
    
    @staticmethod
    def is_punctuation(text):
        return bool(re.match(TokenPatterns.PUNCTUATION, str(text)))
    
    @staticmethod
    def split_tokens(text):
        return re.findall(TokenPatterns.SPLIT_PATTERN, text) 