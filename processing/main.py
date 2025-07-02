import re
from typing import List, Tuple
from collections import Counter

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
    
    def tag(self, include_special=False):
        """Apply POS tagging using spaCy or NLTK as fallback
        
        Args:
            include_special: If True, include special tokens ([NUMBER], [DATE]) in tagging
        """
        if not SPACY_AVAILABLE and not NLTK_AVAILABLE:
            print("Warning: spaCy or NLTK is required for POS tagging. Please install requirements.txt")
            return self
        
        # Initialize spaCy model
        nlp = None
        if SPACY_AVAILABLE:
            try:
                # Try to load English model
                nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("spaCy English model not found. Downloading...")
                try:
                    import subprocess
                    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], 
                                 capture_output=True, check=True)
                    nlp = spacy.load("en_core_web_sm")
                    print("spaCy model downloaded successfully!")
                except:
                    print("Failed to download spaCy model, falling back to NLTK")
                    nlp = None
        
        def tag_tokens_spacy(token_list):
            """Tag tokens using spaCy"""
            if nlp is None:
                return tag_tokens_nltk(token_list)
                
            result = []
            for token in token_list:
                token_str = str(token)
                
                # Handle special tokens
                if not include_special and (token_str.startswith('[') and token_str.endswith(']')):
                    result.append((token_str, 'SPECIAL'))
                elif re.match(r'^[a-zA-Z]+$', token_str):
                    # Use spaCy for alphabetic tokens
                    doc = nlp(token_str)
                    if doc and len(doc) > 0:
                        # Convert spaCy POS tags to Penn Treebank format
                        spacy_tag = doc[0].tag_
                        if spacy_tag:
                            result.append((token_str, spacy_tag))
                        else:
                            result.append((token_str, 'NN'))  # Default
                    else:
                        result.append((token_str, 'NN'))
                elif token_str.isdigit():
                    result.append((token_str, 'CD'))  # Cardinal number
                elif re.match(r'^[^\w\s]+$', token_str):
                    # Punctuation mapping
                    if token_str in '.!?':
                        result.append((token_str, '.'))
                    elif token_str in ',;:':
                        result.append((token_str, ','))
                    elif token_str in '()[]{}':
                        result.append((token_str, '-LRB-' if token_str in '([{' else '-RRB-'))
                    elif token_str in '\'"':
                        result.append((token_str, '``' if token_str == '"' else "''"))
                    else:
                        result.append((token_str, 'SYM'))
                else:
                    result.append((token_str, 'XX'))  # Unknown
            
            return result
        
        def tag_tokens_nltk(token_list):
            """Tag tokens using NLTK (fallback)"""
            # Check for required NLTK data for POS tagging
            tagger_available = True
            if NLTK_AVAILABLE:
                try:
                    nltk.data.find('taggers/averaged_perceptron_tagger')
                except LookupError:
                    try:
                        nltk.download('averaged_perceptron_tagger', quiet=True)
                    except:
                        print("Warning: Could not download POS tagger data, using basic fallback")
                        tagger_available = False
            else:
                tagger_available = False
            
            # Filter tokens for tagging
            taggable_tokens = []
            token_map = {}  # Map original position to token
            
            for i, token in enumerate(token_list):
                token_str = str(token)
                # Skip special tokens unless include_special is True
                if not include_special and (token_str.startswith('[') and token_str.endswith(']')):
                    token_map[i] = (token_str, 'SPECIAL')
                elif re.match(r'^[a-zA-Z]+$', token_str):
                    taggable_tokens.append((len(taggable_tokens), i, token_str))
                    token_map[i] = None  # Will be filled after tagging
                elif token_str.isdigit():
                    token_map[i] = (token_str, 'CD')  # Cardinal number
                elif re.match(r'^[^\w\s]+$', token_str):
                    # Punctuation mapping
                    if token_str in '.!?':
                        token_map[i] = (token_str, '.')
                    elif token_str in ',;:':
                        token_map[i] = (token_str, ',')
                    elif token_str in '()[]{}':
                        token_map[i] = (token_str, '-LRB-' if token_str in '([{' else '-RRB-')
                    elif token_str in '\'"':
                        token_map[i] = (token_str, '``' if token_str == '"' else "''")
                    else:
                        token_map[i] = (token_str, 'SYM')
                else:
                    token_map[i] = (token_str, 'XX')  # Unknown
            
            # Tag alphabetic tokens
            if taggable_tokens:
                words_to_tag = [token for _, _, token in taggable_tokens]
                if tagger_available and NLTK_AVAILABLE:
                    try:
                        tagged_words = pos_tag(words_to_tag)
                        # Fill in the tagged results
                        for (tag_idx, orig_idx, _), (word, tag) in zip(taggable_tokens, tagged_words):
                            token_map[orig_idx] = (word, tag)
                    except:
                        # Fallback if tagging fails
                        for tag_idx, orig_idx, word in taggable_tokens:
                            token_map[orig_idx] = (word, 'NN')  # Default to noun
                else:
                    # Basic fallback tagging without NLTK
                    for tag_idx, orig_idx, word in taggable_tokens:
                        # Simple heuristic-based tagging
                        word_lower = word.lower()
                        if word_lower.endswith('ing'):
                            tag = 'VBG'  # Gerund
                        elif word_lower.endswith('ed'):
                            tag = 'VBD'  # Past tense
                        elif word_lower.endswith('ly'):
                            tag = 'RB'   # Adverb
                        elif word_lower.endswith('s') and len(word) > 2:
                            tag = 'NNS'  # Plural noun
                        else:
                            tag = 'NN'   # Default to noun
                        token_map[orig_idx] = (word, tag)
            
            # Return results in original order
            return [token_map[i] for i in range(len(token_list))]
        
        # Choose tagging method
        if SPACY_AVAILABLE:
            tag_function = tag_tokens_spacy
        else:
            tag_function = tag_tokens_nltk
        
        if self.unique_tokens is not None:
            if self.unique_tokens and isinstance(self.unique_tokens[0], tuple):
                # Handle (token, count) tuples
                tokens_only = [token for token, count in self.unique_tokens]
                tagged_tokens = tag_function(tokens_only)
                # Create new structure: (token, tag, count)
                self.unique_tokens = [(token, tag, orig_count) for (token, tag), (_, orig_count) in zip(tagged_tokens, self.unique_tokens)]
            else:
                # Handle just tokens
                tagged_tokens = tag_function(self.unique_tokens)
                # Create new structure: (token, tag)
                self.unique_tokens = tagged_tokens
        elif self.tokens is not None:
            # Handle regular tokens
            self.tokens = tag_function(self.tokens)
        
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