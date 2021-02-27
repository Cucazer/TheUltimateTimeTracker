class Category(object):
    """docstring for Category."""
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
    def __iter__(self):
        return iter([self.id, self.name])

    def __str__(self):
        return f"{self.name}"