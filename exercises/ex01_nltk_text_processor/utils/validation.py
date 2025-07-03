class Validator:
    
    @staticmethod
    def is_valid_text(text):
        return text is not None and isinstance(text, str) and len(text.strip()) > 0
    
    @staticmethod
    def is_valid_tokens(tokens):
        return tokens is not None and hasattr(tokens, '__iter__') and len(tokens) > 0
    
    @staticmethod
    def validate_sort_criteria(by):
        return by in ['alpha', 'count']
    
    @staticmethod
    def validate_language(language):
        from .language import LanguageUtils
        return language in LanguageUtils.SUPPORTED_LANGUAGES.values()
    
    @staticmethod
    def check_library_availability(libs):
        missing = []
        for lib_name, available in libs.items():
            if not available:
                missing.append(lib_name)
        return missing 