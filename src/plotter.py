import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as ticker
import datetime

def format_func(x, pos):
    hours = int(x//3600)
    minutes = int((x%3600)//60)
    seconds = int(x%60)

    return "{:d}:{:02d}".format(hours, minutes)
    # return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)

def generate_basic_plot(tasks):
    plt.rcdefaults()
    fig, ax = plt.subplots()

    # Example data
    y_pos = np.arange(len(tasks))
    performance = [sum([y.get_duration() for y in x.time_entries], datetime.timedelta()) for x in tasks]

    formatter = FuncFormatter(format_func)
    ax.barh(y_pos, [x.seconds for x in performance], align='center', color='green')
    ax.xaxis.set_major_formatter(formatter)
    # this locates y-ticks at the hours
    #ax.xaxis.set_major_locator(ticker.MultipleLocator(base=3600))
    # this ensures each bar has a 'date' label
    #ax.yaxis.set_major_locator(ticker.MultipleLocator(base=1))
    ax.set_yticks(y_pos)
    ax.set_yticklabels([x.name for x in tasks])
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Time')
    ax.set_title('How much time did you spend on tasks?')

    plt.show()