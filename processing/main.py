import re
from typing import List, Tuple
from collections import Counter

try:
    import nltk
    from nltk.stem import SnowballStemmer
    from langdetect import detect
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

class Processing:
    def __init__(self, text: str = None):
        self.text = text
        self.tokens = None
        self.unique_tokens = None
        self.spaced_text = None
        self.sorted = False
        self.stemmed = False
    
    @classmethod
    def create(cls, text: str):
        return cls(text)
    
    def split(self):
        if self.text is not None:
            pattern = r'\[NUMBER\]|\[DATE\]|[a-zA-Z]+|\d+|[^\w\s]|\s+'
            self.tokens = re.findall(pattern, self.text)
        
        return self
    
    def unique(self, count=False, space=False):
        # If we already have unique_tokens (e.g., after stemming), work with them
        if self.unique_tokens is not None:
            # Check if unique_tokens contains tuples (token, count) or just tokens
            if self.unique_tokens and isinstance(self.unique_tokens[0], tuple):
                # Extract tokens from tuples for re-counting
                source_tokens = [token for token, _ in self.unique_tokens]
            else:
                # Already just tokens
                source_tokens = self.unique_tokens
                
            # Filter out spaces if space=False
            if not space:
                source_tokens = [token for token in source_tokens if not str(token).isspace()]
            
            # Recount tokens
            token_counts = Counter(source_tokens)
            if count:
                self.unique_tokens = [(token, count) for token, count in token_counts.items()]
            else:
                self.unique_tokens = list(token_counts.keys())
                
        elif self.tokens is not None:
            # Original logic for when working with raw tokens
            filtered_tokens = self.tokens
            if not space:
                filtered_tokens = [token for token in self.tokens if not token.isspace()]
            
            token_counts = Counter(filtered_tokens)
            if count:
                self.unique_tokens = [(token, count) for token, count in token_counts.items()]
            else:
                self.unique_tokens = list(token_counts.keys())
        
        return self
    
    def sort(self, by="alpha", reverse=False):
        """Sort tokens by different criteria
        
        Args:
            by: Sort criteria - "alpha" (alphabetical), "count" (by count if available)
            reverse: If True, sort in descending order
        """
        if self.unique_tokens is not None:
            if self.unique_tokens and isinstance(self.unique_tokens[0], tuple):
                # Sorting tuples (token, count)
                if by == "count":
                    self.unique_tokens = sorted(self.unique_tokens, key=lambda x: x[1], reverse=reverse)
                else:  # by == "alpha"
                    self.unique_tokens = sorted(self.unique_tokens, key=lambda x: str(x[0]).lower(), reverse=reverse)
            else:
                # Sorting just tokens
                self.unique_tokens = sorted(self.unique_tokens, key=lambda x: str(x).lower(), reverse=reverse)
        elif self.tokens is not None:
            # Sorting regular tokens
            self.tokens = sorted(self.tokens, key=lambda x: str(x).lower(), reverse=reverse)
        
        self.sorted = True
        return self
    
    def stem(self, auto_detect=True, language="english"):
        """Apply Snowball Stemmer to tokens with language detection
        
        Args:
            auto_detect: If True, automatically detect language for each token
            language: Default language to use if auto_detect is False
        """
        if not NLTK_AVAILABLE:
            print("Warning: NLTK and langdetect are required for stemming. Please install requirements.txt")
            return self
        
        # Supported languages by Snowball Stemmer
        supported_languages = {
            'en': 'english', 'es': 'spanish', 'fr': 'french', 'de': 'german',
            'it': 'italian', 'pt': 'portuguese', 'ru': 'russian', 'ar': 'arabic',
            'da': 'danish', 'nl': 'dutch', 'fi': 'finnish', 'hu': 'hungarian',
            'no': 'norwegian', 'ro': 'romanian', 'sv': 'swedish', 'tr': 'turkish'
        }
        
        def detect_and_stem(token_str):
            # Skip special tokens and non-alphabetic tokens
            if not re.match(r'^[a-zA-Z]+$', token_str):
                return token_str
            
            try:
                if auto_detect and len(token_str) > 2:  # Need minimum length for detection
                    detected_lang = detect(token_str)
                    lang = supported_languages.get(detected_lang, language)
                else:
                    lang = language
                
                stemmer = SnowballStemmer(lang)
                return stemmer.stem(token_str)
            except:
                # If detection or stemming fails, return original token
                return token_str
        
        if self.unique_tokens is not None:
            if self.unique_tokens and isinstance(self.unique_tokens[0], tuple):
                # Process tuples (token, count)
                self.unique_tokens = [(detect_and_stem(token), count) for token, count in self.unique_tokens]
            else:
                # Process just tokens
                self.unique_tokens = [detect_and_stem(token) for token in self.unique_tokens]
        elif self.tokens is not None:
            # Process regular tokens
            self.tokens = [detect_and_stem(token) for token in self.tokens]
        
        self.stemmed = True
        return self
    
    def spacing(self):
        source_data = None
        
        if self.unique_tokens is not None:
            if self.unique_tokens and isinstance(self.unique_tokens[0], tuple):
                source_data = [token for token, count in self.unique_tokens]
            else:
                source_data = self.unique_tokens
        elif self.tokens is not None:
            source_data = self.tokens
        elif self.text is not None:
            pattern = r'\[NUMBER\]|\[DATE\]|[a-zA-Z]+|\d+|[^\w\s]'
            source_data = re.findall(pattern, self.text)
        
        if source_data:
            result = []
            for i, token in enumerate(source_data):
                if i > 0:
                    if not re.match(r'^[^\w\[\]]+$', token):
                        result.append(' ')
                result.append(token)
            
            self.spaced_text = ''.join(result)
        
        return self
    
    def result(self):
        if self.spaced_text is not None:
            return (self.spaced_text,)
        elif self.unique_tokens is not None:
            if self.unique_tokens and isinstance(self.unique_tokens[0], tuple):
                return tuple(self.unique_tokens)
            else:
                return tuple((token,) for token in self.unique_tokens)
        elif self.tokens is not None:
            return tuple((token,) for token in self.tokens)
        else:
            return (self.text,)
    
    def __str__(self):
        if self.spaced_text is not None:
            return self.spaced_text
        elif self.unique_tokens is not None:
            return str(self.unique_tokens)
        elif self.tokens is not None:
            return str(self.tokens)
        return self.text or "" 