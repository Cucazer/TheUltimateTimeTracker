from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from enum import Enum, auto

import models as m

engine = create_engine("sqlite:///data/test.db", echo=True)
m.Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

try:
    active_task = session.query(m.TimeEntry).filter(m.TimeEntry.end_time == None).one().task
except:
    active_task = "none"


class ChoiceWheel(Widget):
    class Mode(Enum):
        Categories = auto()
        Tasks = auto()

    def __init__(self, *args, **kwargs):
        super(ChoiceWheel, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.init_ui, 0)
    
    def init_ui(self, dt=0):
        self.choice_buttons = [self.ids.button0, self.ids.button1, self.ids.button2, self.ids.button3, self.ids.button4]
        self.mode = self.Mode.Categories
        self.update_choice_buttons(session.query(m.Category).all())

    def update_choice_buttons(self, names):
        for i in range(min(len(names), len(self.choice_buttons))):
            self.choice_buttons[i].text = names[i].name
            self.choice_buttons[i].disabled = False
        for i in range(len(names), len(self.choice_buttons)):
            self.choice_buttons[i].text = ""
            self.choice_buttons[i].disabled = True
        if len(names) < len(self.choice_buttons):
            self.ids.more.disabled = True

    def on_button_click(self, button):
        if self.mode == self.Mode.Categories:
            category = session.query(m.Category).filter(m.Category.name == button.text).first()
            self.update_choice_buttons(category.tasks)
            self.mode = self.Mode.Tasks

            # task_name_edit = self.ids.task_name
            # task_name_edit.disabled = False
            # task_name_edit.focus = True
            # task_name_edit.text = "New task..."
            # task_name_edit.select_all()
        elif self.mode == self.Mode.Tasks:
            pass
        else:
            pass

    def on_more_button_click(self, button):
        pass

class MainForm(Widget):
    def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        Clock.schedule_once(self.init_ui, 0)
    
    def init_ui(self, dt=0):
        self.ids.current_task.text = f"Current task: {str(active_task)}"

    def create_new_task(self):
        task_name_edit = self.ids.choice_wheel.ids.task_name
        task_name_edit.disabled = False
        task_name_edit.focus = True
        task_name_edit.text = "New category..."
        task_name_edit.select_all()

        cw = self.ids.choice_wheel
        cw.mode = cw.Mode.Categories
        cw.update_choice_buttons(session.query(m.Category).all())

    def generate_plot(self):
        tasks = session.query(m.Task).all()

        import plotter
        plotter.generate_basic_plot(tasks)

class TheUltimateTimeTrackerApp(App):
    def build(self):
        return MainForm()


if __name__ == '__main__':
    TheUltimateTimeTrackerApp().run()
