class Display:
    
    @staticmethod
    def table(tokens, count=True):
        """Display tokens in a table format
        
        Args:
            tokens: List of tuples (token, count)
            show_count: If True, show count column. If False, show only tokens
        """
        if not tokens:
            print("No tokens to display")
            return
        
        if count:
            print("┌─────────────────────────┬────────┐")
            print("│         Token           │ Count  │")
            print("├─────────────────────────┼────────┤")
            
            for token, count in tokens:
                token_str = str(token)
                if len(token_str) > 23:
                    token_str = token_str[:20] + "..."
                
                print(f"│ {token_str:<23} │ {count:>6} │")
            
            print("└─────────────────────────┴────────┘")
        else:
            print("┌─────────────────────────────────┐")
            print("│             Token               │")
            print("├─────────────────────────────────┤")
            
            for token, count in tokens:
                token_str = str(token)
                if len(token_str) > 31:
                    token_str = token_str[:28] + "..."
                
                print(f"│ {token_str:<31} │")
            
            print("└─────────────────────────────────┘")
        
        print(f"Total unique tokens: {len(tokens)}") 