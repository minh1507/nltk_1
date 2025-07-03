from .date_filter import DateFilter
from .number_filter import NumberFilter

class Filter:
    def __init__(self, text: str = None):
        self.text = text
    
    @classmethod
    def create(cls, text: str):
        return cls(text)
    
    def date(self):
        if self.text is not None:
            self.text = DateFilter.run(self.text)
        return self
    
    def number(self):
        if self.text is not None:
            self.text = NumberFilter.run(self.text)
        return self
    
    def result(self):
        return self.text
    
    def __str__(self):
        return self.text or "" 