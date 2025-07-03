try:
    from langdetect import detect
    from nltk.stem import SnowballStemmer
    LANGUAGE_LIBS_AVAILABLE = True
except ImportError:
    LANGUAGE_LIBS_AVAILABLE = False

class LanguageUtils:
    SUPPORTED_LANGUAGES = {
        'en': 'english', 'es': 'spanish', 'fr': 'french', 'de': 'german',
        'it': 'italian', 'pt': 'portuguese', 'ru': 'russian', 'ar': 'arabic',
        'da': 'danish', 'nl': 'dutch', 'fi': 'finnish', 'hu': 'hungarian',
        'no': 'norwegian', 'ro': 'romanian', 'sv': 'swedish', 'tr': 'turkish'
    }
    
    @staticmethod
    def detect_language(text, default='english'):
        if not LANGUAGE_LIBS_AVAILABLE or len(text) <= 2:
            return default
        try:
            detected = detect(text)
            return LanguageUtils.SUPPORTED_LANGUAGES.get(detected, default)
        except:
            return default
    
    @staticmethod
    def stem_word(word, language='english'):
        if not LANGUAGE_LIBS_AVAILABLE:
            return word
        try:
            stemmer = SnowballStemmer(language)
            return stemmer.stem(word)
        except:
            return word 