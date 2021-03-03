from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    """docstring for Category."""
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
    def __iter__(self):
        return iter([self.id, self.name])

    def __str__(self):
        return f"{self.name}"