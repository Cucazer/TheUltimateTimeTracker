import datetime
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Task(Base):
    """docstring for Task."""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('categories.id'))
    name = Column(String)

    category = relationship("Category", back_populates="tasks")
    time_entries = relationship("TimeEntry", back_populates="task")

    # def __init__(self, id, category_id, name):
    #     self.id = id
    #     self.category_id = category_id
    #     self.name = name
    #     #self.to_be_done_by = datetime.datetime()
    #     #self.to_be_tracked_by = datetime.datetime()
    #     self.karma_done_rate = 5
    #     self.karma_tracked_rate = 2
    #     #self.category = Category()
        
    def __iter__(self):
        return iter([self.id, self.category_id, self.name])

    def __str__(self):
        return f"{self.name}"