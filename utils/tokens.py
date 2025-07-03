from collections import Counter
from .patterns import TokenPatterns

class TokenProcessor:
    
    @staticmethod
    def extract_tokens_from_tuples(unique_tokens):
        if unique_tokens and isinstance(unique_tokens[0], tuple):
            return [token for token, *_ in unique_tokens]
        return unique_tokens
    
    @staticmethod
    def filter_spaces(tokens):
        return [token for token in tokens if not str(token).isspace()]
    
    @staticmethod
    def count_tokens(tokens):
        return Counter(tokens)
    
    @staticmethod
    def create_token_count_pairs(tokens):
        counts = TokenProcessor.count_tokens(tokens)
        return [(token, count) for token, count in counts.items()]
    
    @staticmethod
    def sort_tokens(tokens, by="alpha", reverse=False):
        if not tokens:
            return tokens
            
        if isinstance(tokens[0], tuple):
            if by == "count" and len(tokens[0]) >= 2 and isinstance(tokens[0][1], int):
                return sorted(tokens, key=lambda x: x[1], reverse=reverse)
            else:
                return sorted(tokens, key=lambda x: str(x[0]).lower(), reverse=reverse)
        else:
            return sorted(tokens, key=lambda x: str(x).lower(), reverse=reverse)
    
    @staticmethod
    def determine_data_structure(tokens):
        if not tokens:
            return {'has_tags': False, 'has_count': False}
        
        first_item = tokens[0]
        has_tags = len(first_item) >= 2 and isinstance(first_item[1], str) and not first_item[1].isdigit()
        has_count = len(first_item) == 3 or (len(first_item) == 2 and not has_tags)
        
        return {'has_tags': has_tags, 'has_count': has_count} 