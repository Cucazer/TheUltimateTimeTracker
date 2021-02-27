import datetime

class Task(object):
    """docstring for Task."""
    def __init__(self, id, category_id, name):
        self.id = id
        self.category_id = category_id
        self.name = name
        #self.to_be_done_by = datetime.datetime()
        #self.to_be_tracked_by = datetime.datetime()
        self.karma_done_rate = 5
        self.karma_tracked_rate = 2
        #self.category = Category()
        
    def __iter__(self):
        return iter([self.id, self.category_id, self.name])

    def __str__(self):
        return f"{self.name}"