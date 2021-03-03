#!/usr/bin/python
import os
import sys
import csv
import random
import datetime
#import dateutil
import sqlite3
from sqlalchemy import create_engine

import category as c
import task as t
import time_entry as te

if __name__ == "__main__":
    conn = sqlite3.connect("data/test.db")
    cur = conn.cursor()

    engine = create_engine("sqlite:///data/test.db", echo=True)
    c.Base.metadata.create_all(engine)

    # initialize categories and tasks
    categories = []
    categories_csv = "data/categories.csv"
    if os.path.exists(categories_csv):
        with open(categories_csv, "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                categories.append(c.Category(row[0], row[1]))

    tasks = []
    tasks_csv = "data/tasks.csv"
    if os.path.exists(tasks_csv):
        with open(tasks_csv, "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                tasks.append(t.Task(row[0], row[1], row[2]))

    time_entries = []
    time_entries_csv = "data/time_entries.csv"
    if os.path.exists(time_entries_csv):
        with open(time_entries_csv, "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                time_entries.append(te.TimeEntry(row[0], row[1], row[2]))

    if time_entries:
        active_task = next(iter([x for x in tasks if x.id == time_entries[-1].task_id]), t.Task(0,0,"test"))
    else:
        active_task = t.Task(0,0,"test")

    start_time = datetime.datetime.now()

    while True:
        print(f"\nCurrent task: {active_task}")
        ans = input("Would you like to (c)reate new task or (s)witch to another task or (g)enerate plot or e(x)it? ")
        if ans == "c" or ans == "create":
            # category (subcategory)
            print(f"0 - New category")
            for i in range(1, len(categories)+1):
                print(f"{i} - {categories[i-1]}")
            ans = int(input())
            if ans == 0:
                name = input("New category name: ")
                category = c.Category(random.randint(0, 1000), name)

                cur.execute("INSERT INTO category (name) VALUES (?)", [name])

                with open(categories_csv, "a") as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow(category)
                categories.append(category)
            else:
                category = categories[ans-1]
            
            # task name
            name = input("New task name: ")
            task = t.Task(random.randint(0, 1000), category.id, name)

            cur.execute("INSERT INTO task (category_id, name) VALUES (last_insert_rowid(),?)", [name])

            with open(tasks_csv, "a") as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow(task)
            tasks.append(task)

            conn.commit()

        elif ans == "s" or ans == "switch":
            # print categories (and subcategories)
            print("Pick a category:")

            cur.execute("SELECT * FROM category")
            for (id, name) in cur.fetchall():
                print(f"{id} - {name}")

            for i in range(len(categories)):
                print(f"{i} - {categories[i]}")
            category_id = int(input())
            category = categories[category_id]

            # print tasks
            print("Pick a task:")

            cur.execute("SELECT id, name FROM task WHERE category_id = ?", [category_id])
            for (id, name) in cur.fetchall():
                print(f"{id} - {name}")

            category_tasks = [x for x in tasks if x.category_id == category.id]
            for i in range(len(category_tasks)):
                print(f"{i} - {category_tasks[i]}")
            task = category_tasks[int(input())]

            # create time entry
            if time_entries:
                time_entries[-1].end_time = datetime.datetime.now()
            time_entries.append(te.TimeEntry(task.id, datetime.datetime.now()))
            with open(time_entries_csv, "w") as file:
                csv_writer = csv.writer(file)
                for time_entry in time_entries:
                    csv_writer.writerow(time_entry)                

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