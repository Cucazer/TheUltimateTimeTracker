#!/usr/bin/python
import os
import sys
import csv
import random
import datetime
#import dateutil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models as m

if __name__ == "__main__":
    data_dir = "../data"
    engine = create_engine(f"sqlite:///{data_dir}/test.db", echo=True)
    m.Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        active_task = session.query(m.TimeEntry).filter(m.TimeEntry.end_time == None).one().task
    except:
        active_task = "none"

    start_time = datetime.datetime.now()

    while True:
        print(f"\nCurrent task: {active_task}")
        ans = input("Would you like to (c)reate new task or (s)witch to another task or (g)enerate plot or e(x)it? ")
        if ans == "c" or ans == "create":
            # category (subcategory)
            print(f"0 - New category")
            categories = session.query(m.Category).all()
            for i in range(1, len(categories)+1):
                print(f"{i} - {categories[i-1]}")
            ans = int(input())
            if ans == 0:
                name = input("New category name: ")
                category = m.Category(name = name)
                session.add(category)
            else:
                category = categories[ans-1]
            
            # task name
            name = input("New task name: ")
            category.tasks.append(m.Task(name = name))
            
            session.commit()

        elif ans == "s" or ans == "switch":
            # print categories (and subcategories)
            print("Pick a category:")

            categories = session.query(m.Category).all()
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
                unfinished_time_entry = session.query(m.TimeEntry).filter(m.TimeEntry.end_time == None).one()
                unfinished_time_entry.end_time = datetime.datetime.now()
            except:
                pass
            session.add(m.TimeEntry(task = task, start_time = datetime.datetime.now()))   
            session.commit()          

            active_task = task
        elif ans == "g" or ans == "generate":
            tasks = session.query(m.Task).all()

            import plotter
            plotter.generate_basic_plot(tasks)
        elif ans == "x" or ans == "exit":
            session.close()
            sys.exit(0)
        else:
            print("Invalid input")