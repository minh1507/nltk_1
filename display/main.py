class Display:
    
    @staticmethod
    def table(tokens, count=True, show_tags=False):
        """Display tokens in a table format
        
        Args:
            tokens: List of tuples - can be (token, count), (token, tag), or (token, tag, count)
            count: If True, show count column. If False, show only tokens
            show_tags: If True, show POS tags column
        """
        if not tokens:
            print("No tokens to display")
            return
        
        # Determine data structure
        if not tokens:
            return
            
        first_item = tokens[0]
        has_tags = len(first_item) >= 2 and isinstance(first_item[1], str) and not first_item[1].isdigit()
        has_count = len(first_item) == 3 or (len(first_item) == 2 and not has_tags)
        
        if show_tags and has_tags:
            if has_count:
                # (token, tag, count) format
                if count:
                    # Show all three columns
                    print("┌─────────────────────┬──────────┬────────┐")
                    print("│       Token         │   Tag    │ Count  │")
                    print("├─────────────────────┼──────────┼────────┤")
                    
                    for token, tag, cnt in tokens:
                        token_str = str(token)
                        if len(token_str) > 19:
                            token_str = token_str[:16] + "..."
                        
                        tag_str = str(tag)
                        if len(tag_str) > 8:
                            tag_str = tag_str[:5] + "..."
                        
                        print(f"│ {token_str:<19} │ {tag_str:<8} │ {cnt:>6} │")
                    
                    print("└─────────────────────┴──────────┴────────┘")
                else:
                    # Show token and tag only
                    print("┌─────────────────────┬──────────┐")
                    print("│       Token         │   Tag    │")
                    print("├─────────────────────┼──────────┤")
                    
                    for token, tag, cnt in tokens:
                        token_str = str(token)
                        if len(token_str) > 19:
                            token_str = token_str[:16] + "..."
                        
                        tag_str = str(tag)
                        if len(tag_str) > 8:
                            tag_str = tag_str[:5] + "..."
                        
                        print(f"│ {token_str:<19} │ {tag_str:<8} │")
                    
                    print("└─────────────────────┴──────────┘")
            else:
                # (token, tag) format
                print("┌─────────────────────┬──────────┐")
                print("│       Token         │   Tag    │")
                print("├─────────────────────┼──────────┤")
                
                for token, tag in tokens:
                    token_str = str(token)
                    if len(token_str) > 19:
                        token_str = token_str[:16] + "..."
                    
                    tag_str = str(tag)
                    if len(tag_str) > 8:
                        tag_str = tag_str[:5] + "..."
                    
                    print(f"│ {token_str:<19} │ {tag_str:<8} │")
                
                print("└─────────────────────┴──────────┘")
        else:
            # Original format without tags
            if count and has_count:
                # Header with count
                print("┌─────────────────────────┬────────┐")
                print("│         Token           │ Count  │")
                print("├─────────────────────────┼────────┤")
                
                # Data rows with count
                for item in tokens:
                    if len(item) == 3:
                        token, tag, cnt = item
                    elif len(item) == 2 and not has_tags:
                        token, cnt = item
                    else:
                        token = item[0]
                        cnt = 1
                        
                    # Format token with proper padding
                    token_str = str(token)
                    if len(token_str) > 23:
                        token_str = token_str[:20] + "..."
                    
                    print(f"│ {token_str:<23} │ {cnt:>6} │")
                
                # Footer with count
                print("└─────────────────────────┴────────┘")
            else:
                # Header without count
                print("┌─────────────────────────────────┐")
                print("│             Token               │")
                print("├─────────────────────────────────┤")
                
                # Data rows without count
                for item in tokens:
                    if isinstance(item, tuple):
                        token = item[0]
                    else:
                        token = item
                        
                    # Format token with proper padding
                    token_str = str(token)
                    if len(token_str) > 31:
                        token_str = token_str[:28] + "..."
                    
                    print(f"│ {token_str:<31} │")
                
                # Footer without count
                print("└─────────────────────────────────┘")
        
        print(f"Total unique tokens: {len(tokens)}") 