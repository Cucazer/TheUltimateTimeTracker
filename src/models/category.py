from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    tasks = relationship("Task", back_populates="category")

    """docstring for Category."""
        
    def __iter__(self):
        return iter([self.id, self.name])

    def __str__(self):
        return f"{self.name}"