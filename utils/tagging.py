try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from nltk import pos_tag
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

class TaggingUtils:
    PUNCTUATION_TAGS = {
        '.!?': '.', ',;:': ',', '()[]{}': ('LRB', 'RRB'), '\'"': ('``', "''")
    }
    
    @staticmethod
    def get_punctuation_tag(char):
        for chars, tag in TaggingUtils.PUNCTUATION_TAGS.items():
            if char in chars:
                if isinstance(tag, tuple):
                    return tag[0] if char in '([{' else tag[1]
                return tag
        return 'SYM'
    
    @staticmethod
    def get_spacy_model():
        if not SPACY_AVAILABLE:
            return None
        try:
            return spacy.load("en_core_web_sm")
        except OSError:
            try:
                import subprocess
                subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], 
                             capture_output=True, check=True)
                return spacy.load("en_core_web_sm")
            except:
                return None
    
    @staticmethod
    def tag_with_spacy(token, nlp):
        doc = nlp(str(token))
        if doc and len(doc) > 0 and doc[0].tag_:
            return doc[0].tag_
        return 'NN'
    
    @staticmethod
    def tag_with_nltk(tokens):
        if not NLTK_AVAILABLE:
            return [(token, 'NN') for token in tokens]
        try:
            return pos_tag(tokens)
        except:
            return [(token, 'NN') for token in tokens]
    
    @staticmethod
    def fallback_tag(word):
        word_lower = word.lower()
        if word_lower.endswith('ing'):
            return 'VBG'
        elif word_lower.endswith('ed'):
            return 'VBD'
        elif word_lower.endswith('ly'):
            return 'RB'
        elif word_lower.endswith('s') and len(word) > 2:
            return 'NNS'
        return 'NN' 