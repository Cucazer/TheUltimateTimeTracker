import datetime
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class TimeEntry(Base):
    """docstring for TimeEntry."""
    __tablename__ = "time_entries"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    start_time = Column(String)
    end_time = Column(String)

    task = relationship("Task", back_populates="time_entries")

    # def __init__(self, task_id, start_time, end_time=None):
    #     self.task_id = task_id

    #     if start_time and type(start_time) is str:
    #         self.start_time = datetime.datetime.fromisoformat(start_time)
    #     else:
    #         self.start_time = start_time

    #     if end_time and type(end_time) is str:
    #         self.end_time = datetime.datetime.fromisoformat(end_time)
    #     else:
    #         self.end_time = end_time
        
    def __iter__(self):
        return iter([self.task_id, self.start_time, self.end_time])

    def get_duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        # unfinished task
        return datetime.timedelta() # should be datetime.now