from kivy.app import App
from kivy.uix.widget import Widget

class ChoiceWheel(Widget):
    pass

class MainForm(Widget):
    pass

class TheUltimateTimeTrackerApp(App):
    def build(self):
        return MainForm()


if __name__ == '__main__':
    TheUltimateTimeTrackerApp().run()
