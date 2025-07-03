import re
from typing import List, Tuple
from collections import Counter
from utils import TokenPatterns, LanguageUtils, TaggingUtils, TokenProcessor, Validator

try:
    import nltk
    from nltk.stem import SnowballStemmer
    from nltk import pos_tag, word_tokenize
    from langdetect import detect
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

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
            self.tokens = TokenPatterns.split_tokens(self.text)
        return self
    
    def unique(self, count=False, space=False):
        if self.unique_tokens is not None:
            source_tokens = TokenProcessor.extract_tokens_from_tuples(self.unique_tokens)
            
            if not space:
                source_tokens = TokenProcessor.filter_spaces(source_tokens)
            
            if count:
                if self.unique_tokens and isinstance(self.unique_tokens[0], tuple) and len(self.unique_tokens[0]) >= 2:
                    if isinstance(self.unique_tokens[0][1], int):
                        return self
                    elif len(self.unique_tokens[0]) == 3 and isinstance(self.unique_tokens[0][2], int):
                        return self
                
                token_counts = TokenProcessor.count_tokens(source_tokens)
                self.unique_tokens = [(token, count) for token, count in token_counts.items()]
            else:
                self.unique_tokens = list(token_counts.keys()) if 'token_counts' in locals() else list(set(source_tokens))
                
        elif self.tokens is not None:
            filtered_tokens = self.tokens if space else TokenProcessor.filter_spaces(self.tokens)
            token_counts = TokenProcessor.count_tokens(filtered_tokens)
            if count:
                self.unique_tokens = [(token, count) for token, count in token_counts.items()]
            else:
                self.unique_tokens = list(token_counts.keys())
        
        return self
    
    def sort(self, by="alpha", reverse=False):
        if not Validator.validate_sort_criteria(by):
            return self
            
        if self.unique_tokens is not None:
            self.unique_tokens = TokenProcessor.sort_tokens(self.unique_tokens, by, reverse)
        elif self.tokens is not None:
            self.tokens = TokenProcessor.sort_tokens(self.tokens, by, reverse)
        
        self.sorted = True
        return self
    
    def stem(self, auto_detect=True, language="english"):
        if not NLTK_AVAILABLE:
            print("Warning: NLTK and langdetect are required for stemming. Please install requirements.txt")
            return self
        
        def detect_and_stem(token_str):
            if not TokenPatterns.is_alphabetic(token_str):
                return token_str
            
            lang = language
            if auto_detect and len(token_str) > 2:
                lang = LanguageUtils.detect_language(token_str, language)
            
            return LanguageUtils.stem_word(token_str, lang)
        
        if self.unique_tokens is not None:
            if self.unique_tokens and isinstance(self.unique_tokens[0], tuple):
                if len(self.unique_tokens[0]) == 2:
                    self.unique_tokens = [(detect_and_stem(token), count) for token, count in self.unique_tokens]
                elif len(self.unique_tokens[0]) == 3:
                    self.unique_tokens = [(detect_and_stem(token), tag, count) for token, tag, count in self.unique_tokens]
            else:
                self.unique_tokens = [detect_and_stem(token) for token in self.unique_tokens]
        elif self.tokens is not None:
            self.tokens = [detect_and_stem(token) for token in self.tokens]
        
        self.stemmed = True
        return self
    
    def tag(self, include_special=False):
        if not SPACY_AVAILABLE and not NLTK_AVAILABLE:
            print("Warning: spaCy or NLTK is required for POS tagging. Please install requirements.txt")
            return self
        
        nlp = TaggingUtils.get_spacy_model() if SPACY_AVAILABLE else None
        
        def tag_tokens(token_list):
            result = []
            alphabetic_tokens = []
            token_map = {}
            
            for i, token in enumerate(token_list):
                token_str = str(token)
                
                if not include_special and TokenPatterns.is_special_token(token_str):
                    token_map[i] = (token_str, 'SPECIAL')
                elif TokenPatterns.is_alphabetic(token_str):
                    alphabetic_tokens.append((i, token_str))
                    token_map[i] = None
                elif TokenPatterns.is_digits_only(token_str):
                    token_map[i] = (token_str, 'CD')
                elif TokenPatterns.is_punctuation(token_str):
                    tag = TaggingUtils.get_punctuation_tag(token_str)
                    token_map[i] = (token_str, tag)
                else:
                    token_map[i] = (token_str, 'XX')
            
            if alphabetic_tokens:
                if nlp:
                    for i, token_str in alphabetic_tokens:
                        tag = TaggingUtils.tag_with_spacy(token_str, nlp)
                        token_map[i] = (token_str, tag)
                else:
                    words = [token for _, token in alphabetic_tokens]
                    tagged = TaggingUtils.tag_with_nltk(words)
                    for (i, _), (word, tag) in zip(alphabetic_tokens, tagged):
                        token_map[i] = (word, tag)
            
            return [token_map[i] for i in range(len(token_list))]
        
        if self.unique_tokens is not None:
            if self.unique_tokens and isinstance(self.unique_tokens[0], tuple):
                if len(self.unique_tokens[0]) == 2:
                    tokens_only = [token for token, count in self.unique_tokens]
                    tagged_tokens = tag_tokens(tokens_only)
                    self.unique_tokens = [(token, tag, count) for (token, tag), (_, count) in zip(tagged_tokens, self.unique_tokens)]
                elif len(self.unique_tokens[0]) == 3:
                    tokens_only = [token for token, tag, count in self.unique_tokens]
                    tagged_tokens = tag_tokens(tokens_only)
                    self.unique_tokens = [(token, new_tag, count) for (token, new_tag), (_, _, count) in zip(tagged_tokens, self.unique_tokens)]
            else:
                self.unique_tokens = tag_tokens(self.unique_tokens)
        elif self.tokens is not None:
            self.tokens = tag_tokens(self.tokens)
        
        return self
    
    def spacing(self):
        source_data = None
        
        if self.unique_tokens is not None:
            source_data = TokenProcessor.extract_tokens_from_tuples(self.unique_tokens)
        elif self.tokens is not None:
            source_data = self.tokens
        elif self.text is not None:
            source_data = re.findall(r'\[NUMBER\]|\[DATE\]|[a-zA-Z]+|\d+|[^\w\s]', self.text)
        
        if source_data:
            result = []
            for i, token in enumerate(source_data):
                if i > 0 and not re.match(TokenPatterns.SPACING_EXCLUDE, token):
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