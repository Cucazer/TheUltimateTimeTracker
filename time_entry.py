import datetime

class TimeEntry(object):
    """docstring for TimeEntry."""
    def __init__(self, task_id, start_time, end_time=None):
        self.task_id = task_id
        self.start_time = start_time
        self.end_time = end_time
        
    def __iter__(self):
        return iter([self.task_id, self.start_time, self.end_time])