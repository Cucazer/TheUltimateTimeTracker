import sys
import os
import datetime
import math
import cmath
from enum import Enum, auto

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.properties import ObjectProperty, NumericProperty

from kivymd.app import MDApp
#from kivymd.uix.datatables import MDDataTable
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.snackbar import Snackbar

import config
import models as m
from db_connection import DbConnection, Item

db_connection = DbConnection()

try:
    active_task = db_connection.get(Item.ActiveTask)
except:
    active_task = "none"

class ChoiceButton(ButtonBehavior, Label):
    i = NumericProperty()
    root_pos_x = NumericProperty()
    root_pos_y = NumericProperty()

    def __init__(self, *args, **kwargs):
        super(ChoiceButton, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.init_ui, 0)

    def init_ui(self, dt=0):
        pass

class Separator(Widget):
    i = NumericProperty()
    root_pos_x = NumericProperty()
    root_pos_y = NumericProperty()

class ChoiceWheel(Widget):
    category = ObjectProperty()
    task = ObjectProperty()

    class Mode(Enum):
        Switch = auto()
        Create = auto()
        Select = auto()

    class ItemType(Enum):
        Categories = auto()
        Tasks = auto()

    def __init__(self, *args, **kwargs):
        super(ChoiceWheel, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.init_ui, 0)

        self.touched_button_index = None

    def init_ui(self, dt=0):
        self.choice_buttons = [self.ids.button0, self.ids.button5, self.ids.button1, self.ids.button4, self.ids.button2]
        self.buttons = [self.ids.button0, self.ids.button1, self.ids.button2, self.ids.more, self.ids.button4, self.ids.button5]
        self.mode = self.Mode.Switch
        self.items = self.ItemType.Categories
        self.update_choice_buttons(db_connection.get(Item.Category))

    def update_choice_buttons(self, names, disable = False, page = 0):
        self.button_names = names
        self.page = page
        choice_count = len(self.choice_buttons)
        name_count = len(names) - page * choice_count
        for i in range(min(name_count, choice_count)):
            self.choice_buttons[i].text = names[i + page * choice_count].name.replace(' ', "\n")
            self.choice_buttons[i].disabled = disable
        for i in range(name_count, choice_count):
            self.choice_buttons[i].text = ""
            self.choice_buttons[i].disabled = True

        if len(names) > choice_count:
            self.ids.more.disabled = False
            if name_count < choice_count:
                self.ids.more.text = "Return"
            else:
                self.ids.more.text = "More"
        else:
            self.ids.more.disabled = name_count <= choice_count

    def update_task_edit(self, text = None):
        task_name_edit = self.ids.task_name
        if text:
            task_name_edit.disabled = False
            task_name_edit.focus = True
            task_name_edit.text = text
            Clock.schedule_once(lambda dt: task_name_edit.select_all())
        else:
            task_name_edit.disabled = True
            task_name_edit.text = ""

    def on_touch_down(self, touch):
        local_pos = self.to_local(*touch.pos, True)
        pos = complex(local_pos[0] - self.size[0] / 2, local_pos[1] - self.size[1] / 2)
        r, phi = cmath.polar(pos)
        if r > self.size[0] / 2:
            # outside circle
            return
        #print(f"Local coordinates: {local_pos}, pos: {pos}, polar: {cmath.polar(pos)}")
        converted_deg = (-math.degrees(phi) + 90 + 360) % 360
        self.touched_button_index = int((converted_deg + 30) // 60 % 6)
        #print(f"Converted degrees {converted_deg}, index: {self.touched_button_index}")

    def on_touch_up(self, touch):
        #TODO bug with touchpad: check, whether the same button was touched down and up/disable moving
        if self.touched_button_index is None:
            # touched outside any button
            return

        if self.touched_button_index == 3:
            self.on_more_button_click()
            self.touched_button_index = None
            return

        button = self.buttons[self.touched_button_index]

        if button.disabled:
            self.touched_button_index = None
            return

        if self.items == self.ItemType.Categories:
            self.category = db_connection.get(Item.Category, button.text.replace("\n", " "))

            self.items = self.ItemType.Tasks
            self.update_choice_buttons(self.category.tasks, self.mode == self.Mode.Create)

            if self.mode == self.Mode.Create:
                self.update_task_edit("New task...")
        elif self.items == self.ItemType.Tasks:
            self.task = next(x for x in self.category.tasks if x.name == button.text.replace("\n", " "))
            
            self.update_choice_buttons(db_connection.get(Item.Category))
            self.items = self.ItemType.Categories
            self.mode = self.Mode.Switch
            self.update_task_edit()

            print(f"Category {self.category.name} and task {self.task.name} chosen!")
        else:
            pass

        self.touched_button_index = None

    def on_input_submit(self, input):
        if self.items == self.ItemType.Categories:
            self.category = m.Category(name=input.text)

            self.update_choice_buttons(self.category.tasks, self.mode == self.Mode.Create)
            self.items = self.ItemType.Tasks

            if self.mode == self.Mode.Create:
                self.update_task_edit("New task...")
        elif self.items == self.ItemType.Tasks:
            self.task = m.Task(name=input.text)
            self.category.tasks.append(self.task)
            db_connection.add(self.category)

            self.update_choice_buttons(db_connection.get(Item.Category))
            self.items = self.ItemType.Categories
            self.mode = self.Mode.Switch
            self.update_task_edit()

            print(f"Category {self.category.name} and task {self.task.name} chosen!")
        else:
            pass

    def on_more_button_click(self):
        if (self.page + 1) * len(self.choice_buttons) < len(self.button_names):
            self.update_choice_buttons(self.button_names, page = self.page + 1)
        else:
            self.update_choice_buttons(self.button_names, page = 0)

class MainForm(Widget):
    start_date = ObjectProperty()
    start_time = ObjectProperty()
    end_date = ObjectProperty()
    end_time = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.init_ui, 0)
    
    def init_ui(self, dt=0):
        self.ids.choice_wheel.bind(task = self.on_task_changed)
        self.ids.current_task.text = f"Current task: {str(active_task)}"

    def on_start_date(self, instance, value: datetime.date):
        if value:
            self.change_time_input(self.ids.start_time, value, self.start_time)

    def on_start_time(self, instance, value: datetime.time):
        if value:
            self.change_time_input(self.ids.start_time, self.start_date, value)

    def on_end_date(self, instance, value: datetime.date):
        if value:
            self.change_time_input(self.ids.end_time, value, self.end_time)

    def on_end_time(self, instance, value: datetime.time):
        if value:
            self.change_time_input(self.ids.end_time, self.end_date, value)

    def change_time_input(self, input_widget, date, time):
        if date:
            if date.year != datetime.date.today().year:
                input_widget.text = f"{time.strftime(config.TIME_FORMAT) + ' ' if time else ''}{date.strftime(config.LONG_DATE_FORMAT)}"
            else:
                input_widget.text = f"{time.strftime(config.TIME_FORMAT) + ' ' if time else ''}{date.strftime(config.SHORT_DATE_FORMAT)}"

    def create_new_task(self):
        task_name_edit = self.ids.choice_wheel.ids.task_name
        task_name_edit.disabled = False
        task_name_edit.focus = True
        task_name_edit.text = "New category..."
        task_name_edit.select_all()

        cw = self.ids.choice_wheel
        cw.mode = cw.Mode.Create
        cw.items = cw.ItemType.Categories
        cw.update_choice_buttons(db_connection.get(Item.Category))

    def on_task_changed(self, instance, task):
        if self.ids.choice_wheel.mode == self.ids.choice_wheel.Mode.Switch:
            active_task = task
            self.ids.current_task.text = f"Current task: {str(active_task)}"

            # create time entry
            try:
                unfinished_time_entry = db_connection.get(Item.UnfinishedTimeEntry)
                unfinished_time_entry.end_time = datetime.datetime.now()
            except:
                pass
            db_connection.add(m.TimeEntry(task = task, start_time = datetime.datetime.now()))   
        elif self.ids.choice_wheel.mode == self.ids.choice_wheel.Mode.Select:
            start_time = datetime.datetime.combine(self.start_date, self.start_time)
            end_time = datetime.datetime.combine(self.end_date, self.end_time)
            db_connection.add(m.TimeEntry(task = task, start_time = start_time, end_time = end_time))   
            #TODO increase duration?
            Snackbar(text=f"Activity {task.name} ({task.category.name}) from {start_time} to {end_time} successfully recorded!").show() # change to open() after update
            for widget in [self.ids.start_time, self.ids.end_time]:
                widget.disabled = False
            self.start_date = end_time.date()
            self.start_time = end_time.time()

    def generate_plot(self):
        tasks = db_connection.get(Item.Task)
        
        #TODO separate thread
        import plotter
        plotter.generate_basic_plot(tasks)

    def get_date(self, date):
        if self.grabbed_text_edit == self.ids.start_time:
            self.start_date = date
        else:
            self.end_date = date
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time):
        if self.grabbed_text_edit == self.ids.start_time:
            self.start_time = time
        else:
            self.end_time = time
        self.grabbed_text_edit = None
        if all(x is not None for x in [self.start_date, self.start_time, self.end_date, self.end_time]):
            self.ids.select_task.disabled = False

    def show_date_picker(self, touch):
        if touch.grab_current not in [self.ids.start_time, self.ids.end_time]:
            return
        self.grabbed_text_edit = touch.grab_current
        date_dialog = MDDatePicker(callback=self.get_date, max_date=datetime.date.today())
        date_dialog.open()
        touch.ungrab(self.grabbed_text_edit)
        return True

    def select_task(self):
        cw = self.ids.choice_wheel
        cw.mode = cw.Mode.Select
        cw.items = cw.ItemType.Categories
        cw.update_choice_buttons(db_connection.get(Item.Category))
        for widget in [self.ids.start_time, self.ids.end_time, self.ids.select_task]:
            widget.disabled = True

class TheUltimateTimeTrackerApp(MDApp):
    def build(self):
        return MainForm()


if __name__ == '__main__':
    TheUltimateTimeTrackerApp().run()
