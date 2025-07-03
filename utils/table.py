class TableFormatter:
    
    @staticmethod
    def format_text(text, max_length, suffix="..."):
        text_str = str(text)
        if len(text_str) > max_length:
            return text_str[:max_length-len(suffix)] + suffix
        return text_str
    
    @staticmethod
    def print_header(columns):
        if len(columns) == 1:
            width = columns[0][1]
            print(f"┌{'─' * (width + 2)}┐")
            print(f"│ {columns[0][0]:^{width}} │")
            print(f"├{'─' * (width + 2)}┤")
        elif len(columns) == 2:
            w1, w2 = columns[0][1], columns[1][1]
            print(f"┌{'─' * (w1 + 2)}┬{'─' * (w2 + 2)}┐")
            print(f"│ {columns[0][0]:^{w1}} │ {columns[1][0]:^{w2}} │")
            print(f"├{'─' * (w1 + 2)}┼{'─' * (w2 + 2)}┤")
        elif len(columns) == 3:
            w1, w2, w3 = columns[0][1], columns[1][1], columns[2][1]
            print(f"┌{'─' * (w1 + 2)}┬{'─' * (w2 + 2)}┬{'─' * (w3 + 2)}┐")
            print(f"│ {columns[0][0]:^{w1}} │ {columns[1][0]:^{w2}} │ {columns[2][0]:^{w3}} │")
            print(f"├{'─' * (w1 + 2)}┼{'─' * (w2 + 2)}┼{'─' * (w3 + 2)}┤")
    
    @staticmethod
    def print_footer(columns):
        if len(columns) == 1:
            width = columns[0][1]
            print(f"└{'─' * (width + 2)}┘")
        elif len(columns) == 2:
            w1, w2 = columns[0][1], columns[1][1]
            print(f"└{'─' * (w1 + 2)}┴{'─' * (w2 + 2)}┘")
        elif len(columns) == 3:
            w1, w2, w3 = columns[0][1], columns[1][1], columns[2][1]
            print(f"└{'─' * (w1 + 2)}┴{'─' * (w2 + 2)}┴{'─' * (w3 + 2)}┘")
    
    @staticmethod
    def print_row(data, columns):
        if len(columns) == 1:
            width = columns[0][1]
            text = TableFormatter.format_text(data[0], width)
            print(f"│ {text:<{width}} │")
        elif len(columns) == 2:
            w1, w2 = columns[0][1], columns[1][1]
            text1 = TableFormatter.format_text(data[0], w1)
            text2 = str(data[1])
            if len(data) > 2 and isinstance(data[1], str):
                text2 = TableFormatter.format_text(data[1], w2)
                print(f"│ {text1:<{w1}} │ {text2:<{w2}} │")
            else:
                print(f"│ {text1:<{w1}} │ {text2:>{w2}} │")
        elif len(columns) == 3:
            w1, w2, w3 = columns[0][1], columns[1][1], columns[2][1]
            text1 = TableFormatter.format_text(data[0], w1)
            text2 = TableFormatter.format_text(data[1], w2)
            text3 = str(data[2])
            print(f"│ {text1:<{w1}} │ {text2:<{w2}} │ {text3:>{w3}} │") 