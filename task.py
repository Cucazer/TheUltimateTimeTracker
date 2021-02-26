import datetime

class Task(object):
    """docstring for Task."""
    def __init__(self, name):
        super(Task, self).__init__()
        self.name = name
        self.start = datetime.datetime()
        self.finish = datetime.datetime()
        self.to_be_done_by = datetime.datetime()
        self.to_be_tracked_by = datetime.datetime()
        self.karma_done_rate = 5
        self.karma_tracked_rate = 2
        #self.category = Category()
        