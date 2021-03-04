#!/usr/bin/python
import os
import sys
import csv
import random
import datetime
#import dateutil
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base

import category as c
import task as t
import time_entry as te

if __name__ == "__main__":
    conn = sqlite3.connect("data/test.db")
    cur = conn.cursor()

    engine = create_engine("sqlite:///data/test.db", echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # initialize categories and tasks
    categories = []
    categories_csv = "data/categories.csv"

    tasks = []
    tasks_csv = "data/tasks.csv"

    time_entries = []
    time_entries_csv = "data/time_entries.csv"

    # if time_entries:
    #     active_task = next(iter([x for x in tasks if x.id == time_entries[-1].task_id]), t.Task(0,0,"test"))
    # else:
    #     active_task = t.Task(0,0,"test")
    try:
        active_task = session.query(te.TimeEntry).filter(te.TimeEntry.end_time == None).one().task
    except:
        active_task = "none"

    start_time = datetime.datetime.now()

    while True:
        print(f"\nCurrent task: {active_task}")
        ans = input("Would you like to (c)reate new task or (s)witch to another task or (g)enerate plot or e(x)it? ")
        if ans == "c" or ans == "create":
            # category (subcategory)
            print(f"0 - New category")
            categories = session.query(c.Category).all()
            for i in range(1, len(categories)+1):
                print(f"{i} - {categories[i-1]}")
            ans = int(input())
            if ans == 0:
                name = input("New category name: ")
                category = c.Category(name = name)
                session.add(category)
            else:
                category = categories[ans-1]
            
            # task name
            name = input("New task name: ")
            category.tasks.append(t.Task(name = name))
            
            session.commit()

        elif ans == "s" or ans == "switch":
            # print categories (and subcategories)
            print("Pick a category:")

            categories = session.query(c.Category).all()
            for i in range(len(categories)):
                print(f"{i} - {categories[i]}")
            category = categories[int(input())]

            # print tasks
            print("Pick a task:")

            for i in range(len(category.tasks)):
                print(f"{i} - {category.tasks[i]}")
            task = category.tasks[int(input())]

            # create time entry
            try:
                unfinished_time_entry = session.query(te.TimeEntry).filter(te.TimeEntry.end_time == None).one()
                unfinished_time_entry.end_time = datetime.datetime.now()
            except:
                pass
            session.add(te.TimeEntry(task = task, start_time = datetime.datetime.now()))   
            session.commit()          

            active_task = task
        elif ans == "g" or ans == "generate":
            import matplotlib.pyplot as plt
            import numpy as np

            plt.rcdefaults()
            fig, ax = plt.subplots()

            # Example data
            y_pos = np.arange(len(tasks))
            performance = [sum([y.get_duration() for y in time_entries if y.task_id == x.id], datetime.timedelta()) for x in tasks]

            ax.barh(y_pos, [x.seconds for x in performance], align='center', color='green')
            #ax.yaxis_date()
            #ax.yaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
            ax.set_yticks(y_pos)
            ax.set_yticklabels([x.name for x in tasks])
            ax.invert_yaxis()  # labels read top-to-bottom
            ax.set_xlabel('Time (s)')
            ax.set_title('How much time did you spend on tasks?')

            plt.show()
        elif ans == "x" or ans == "exit":
            conn.close()
            sys.exit(0)
        else:
            print("Invalid input")