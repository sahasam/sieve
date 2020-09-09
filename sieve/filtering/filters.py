#filters.py


class BaseFilter :
    def __init__ (self, regex, output):
        self.regex = regex
        self.output = output
    
class MultithreadedFilter (BaseFilter) :
    def __init__ (self, regex, output):
        super.__init__(regex, output)
        
