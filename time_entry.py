import datetime

class TimeEntry(object):
    """docstring for TimeEntry."""
    def __init__(self, task_id, start_time, end_time):
        self.task_id = task_id
        self.start_time = start_time
        self.end_time = end_time
        