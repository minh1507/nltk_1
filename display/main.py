from utils import TableFormatter, TokenProcessor

class Display:
    
    @staticmethod
    def table(tokens, count=True, tags=False):
        """Display tokens in a table format
        
        Args:
            tokens: List of tuples - can be (token, count), (token, tag), or (token, tag, count)
            count: If True, show count column. If False, show only tokens
            tags: If True, show POS tags column
        """
        if not tokens:
            print("No tokens to display")
            return
        
        structure = TokenProcessor.determine_data_structure(tokens)
        has_tags = structure['has_tags']
        has_count = structure['has_count']
        
        if tags and has_tags:
            if has_count:
                if count:
                    columns = [("Token", 19), ("Tag", 8), ("Count", 6)]
                    TableFormatter.print_header(columns)
                    for token, tag, cnt in tokens:
                        TableFormatter.print_row((token, tag, cnt), columns)
                    TableFormatter.print_footer(columns)
                else:
                    columns = [("Token", 19), ("Tag", 8)]
                    TableFormatter.print_header(columns)
                    for token, tag, cnt in tokens:
                        TableFormatter.print_row((token, tag), columns)
                    TableFormatter.print_footer(columns)
            else:
                columns = [("Token", 19), ("Tag", 8)]
                TableFormatter.print_header(columns)
                for token, tag in tokens:
                    TableFormatter.print_row((token, tag), columns)
                TableFormatter.print_footer(columns)
        else:
            if count and has_count:
                columns = [("Token", 23), ("Count", 6)]
                TableFormatter.print_header(columns)
                for item in tokens:
                    if len(item) == 3:
                        token, tag, cnt = item
                    elif len(item) == 2 and not has_tags:
                        token, cnt = item
                    else:
                        token = item[0]
                        cnt = 1
                    TableFormatter.print_row((token, cnt), columns)
                TableFormatter.print_footer(columns)
            else:
                columns = [("Token", 31)]
                TableFormatter.print_header(columns)
                for item in tokens:
                    token = item[0] if isinstance(item, tuple) else item
                    TableFormatter.print_row((token,), columns)
                TableFormatter.print_footer(columns)
        
        print(f"Total unique tokens: {len(tokens)}") 