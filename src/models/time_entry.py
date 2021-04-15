import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class TimeEntry(Base):
    """docstring for TimeEntry."""
    __tablename__ = "time_entries"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'))
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    task = relationship("Task", back_populates="time_entries")
        
    def __iter__(self):
        return iter([self.task_id, self.start_time, self.end_time])

    def get_duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        # unfinished task
        return datetime.timedelta() # should be datetime.now