#!/usr/bin/python
import os
import csv
import random
import datetime
#import dateutil

import category as c
import task as t
import time_entry as te

if __name__ == "__main__":
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
        ans = input("Would you like to (c)reate new task or (s)witch to another task? ")
        if ans == "c" or ans == "create":
            # category (subcategory)
            print(f"0 - New category")
            for i in range(1, len(categories)+1):
                print(f"{i} - {categories[i-1]}")
            ans = int(input())
            if ans == 0:
                name = input("New category name: ")
                category = c.Category(random.randint(0, 1000), name)
                with open(categories_csv, "a") as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow(category)
                categories.append(category)
            else:
                category = categories[ans-1]
            
            # task name
            name = input("New task name: ")
            task = t.Task(random.randint(0, 1000), category.id, name)
            with open(tasks_csv, "a") as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerow(task)
            tasks.append(task)

        elif ans == "s" or ans == "switch":
            # print categories (and subcategories)
            print("Pick a category:")
            for i in range(len(categories)):
                print(f"{i} - {categories[i]}")
            category = categories[int(input())]

            # print tasks
            print("Pick a task:")
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
        else:
            print("Invalid input")