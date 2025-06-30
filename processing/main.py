import re
from typing import List, Tuple
from collections import Counter

class Processing:
    def __init__(self, text: str = None):
        self.text = text
        self.tokens = None
        self.unique_tokens = None
        self.spaced_text = None
    
    @classmethod
    def create(cls, text: str):
        return cls(text)
    
    def split(self):
        if self.text is not None:
            pattern = r'\[NUMBER\]|\[DATE\]|[a-zA-Z]+|\d+|[^\w\s]|\s+'
            self.tokens = re.findall(pattern, self.text)
        
        return self
    
    def unique(self, count=False, space=False):
        if self.tokens is not None:
            # Filter out spaces if space=False
            filtered_tokens = self.tokens
            if not space:
                filtered_tokens = [token for token in self.tokens if not token.isspace()]
            
            token_counts = Counter(filtered_tokens)
            if count:
                self.unique_tokens = [(token, count) for token, count in token_counts.items()]
            else:
                self.unique_tokens = list(token_counts.keys())
        
        return self
    
    def spacing(self):
        # Work with whatever data we have: unique_tokens, tokens, or text
        source_data = None
        
        if self.unique_tokens is not None:
            # If unique_tokens is tuples, extract just the values
            if self.unique_tokens and isinstance(self.unique_tokens[0], tuple):
                source_data = [token for token, count in self.unique_tokens]
            else:
                source_data = self.unique_tokens
        elif self.tokens is not None:
            source_data = self.tokens
        elif self.text is not None:
            # Split text first
            pattern = r'\[NUMBER\]|\[DATE\]|[a-zA-Z]+|\d+|[^\w\s]'
            source_data = re.findall(pattern, self.text)
        
        if source_data:
            # Add spaces between tokens, but handle punctuation smartly
            result = []
            for i, token in enumerate(source_data):
                if i > 0:
                    # Don't add space before punctuation
                    if not re.match(r'^[^\w\[\]]+$', token):
                        result.append(' ')
                result.append(token)
            
            self.spaced_text = ''.join(result)
        
        return self
    
    def result(self):
        # Always return tuple format
        if self.spaced_text is not None:
            # Convert spaced text to tuple with single element
            return (self.spaced_text,)
        elif self.unique_tokens is not None:
            # If already tuples, return as is; if list, convert to tuples
            if self.unique_tokens and isinstance(self.unique_tokens[0], tuple):
                return tuple(self.unique_tokens)
            else:
                # Convert list to tuple of single-element tuples
                return tuple((token,) for token in self.unique_tokens)
        elif self.tokens is not None:
            # Convert tokens list to tuple of single-element tuples
            return tuple((token,) for token in self.tokens)
        else:
            # Return original text as single-element tuple
            return (self.text,)
    
    def __str__(self):
        if self.spaced_text is not None:
            return self.spaced_text
        elif self.unique_tokens is not None:
            return str(self.unique_tokens)
        elif self.tokens is not None:
            return str(self.tokens)
        return self.text or "" 