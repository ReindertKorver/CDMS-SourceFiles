class DomainType:
    def __init__(self, value):
        self.value=value
    value=None
    def __str__(self):
     return self.value
    def validate(self):
         return True