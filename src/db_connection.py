import sys
import os
from enum import Enum, auto

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
print("In module products __package__, __name__ ==", __package__, __name__)
from models import *

class Item(Enum):
    ActiveTask = auto()
    Category = auto()
    Task = auto()
    UnfinishedTimeEntry = auto()

class DbConnection():
    
    def __init__(self):
        self.db_file_path = os.path.join(config.ROOT_DIR, "testdata", "example.db")
        if len(sys.argv) > 1:
            self.db_file_path = sys.argv[1]
        self.engine = create_engine(f"sqlite:///{self.db_file_path}", echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def get(self, item:Item, name = None):
        if item is Item.ActiveTask:
            return self.session.query(TimeEntry).filter(TimeEntry.end_time == None).one().task
        elif item is Item.Category:
            if name:
                return self.session.query(Category).filter(Category.name == name).first()
            else:
                return self.session.query(Category).all()
        elif item is Item.Task:
            return self.session.query(Task).all()
        elif item is Item.UnfinishedTimeEntry:
            return self.session.query(TimeEntry).filter(TimeEntry.end_time == None).one()

    def add(self, new_object):
        self.session.add(new_object)   
        self.session.commit()