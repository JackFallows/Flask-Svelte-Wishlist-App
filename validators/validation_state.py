class ValidationState():
    def __init__(self, is_valid = True):
        self.is_valid = is_valid
        self.failures = {}
    
    def add_failure_if(self, condition: bool, property: str, reason: str):
        if condition:
            self.is_valid = False
            self.failures[property] = reason
            
        return self
    
    def as_dict(self):
        return {
            "is_valid": self.is_valid,
            "failures": self.failures
        }
