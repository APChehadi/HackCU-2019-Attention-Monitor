import numpy as np
import scipy.special
import pandas as pd
from random import random

<<<<<<< HEAD
=======
from bokeh.models import Button
>>>>>>> a9801e41202392496766b35e742b2b9338658966
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file, curdoc
from bokeh.layouts import column
from bokeh.models import Button
<<<<<<< HEAD
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import show, output_file
from bokeh.embed import components

class GraphCreation():
    def __init__(self, title, array):
        self.title = title
        self.array = array
    def readData(self, jsonData):
        self.array = [jsonData['time'],jsonData['InstantEyeRatio']]
    #This function creates the visualization of the Histogram
    def make_histo(self, xTitle, yTitle):
        #Creates the mathmatical information for the histogram
        hist, edges = np.histogram(self.array[1], density=False, bins=10)
        p = figure(title=self.title, background_fill_color="#fafafa") #Creates base of graph
        #Creates the rectangles for the histogram
        #Left is all boundries except for the last one
        #Right is all boundries except the first
        p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="navy", line_color="white", alpha=0.5)

        #signifies where the y starts
        p.y_range.start = 0
        p.xaxis.axis_label = xTitle
        p.yaxis.axis_label = yTitle 
        p.grid.grid_line_color="white"
        return p
    def make_line_plot(self, xTitle, yTitle):
        #Creates a line plot based on time
        linePlot = figure(title=self.title, x_axis_type="datetime", plot_width=800, plot_height=500)
        #the x data should be formated in date time format
        x = self.array[0]
        #Y would be some thing like eyeRatio
        y = self.array[1]
        linePlot.xaxis.axis_label = xTitle
        linePlot.yaxis.axis_label = yTitle 
        linePlot.line(x,y)
        linePlot.circle(x,y, size=7)
        return linePlot
    def defaultCreation(self):
        histo = self.make_histo('Eye Ratio', 'Frequency')
        lineGraph = self.make_line_plot("Time", "Eye Ratio")
        return (histo,lineGraph)
if __name__ == "__main__":

    p1 = GraphCreation("Eye Ratio Tracking", week)
    histo = p1.make_histo('Eye Ratio', 'Frequency')

    lineGraph = p1.make_line_plot("Time", "Eye Ratio")
    

    output_file('Graphs.html', title="histogram.py example")
    grid = gridplot([histo, lineGraph], ncols=2, plot_width=400, plot_height=400)
    show(grid)


=======


#This function creates the visualization of the Histogram
def make_histo(title, array, x):
    #Creates the mathmatical information for the histogram
    hist, edges = np.histogram(eyeRatios, density=False, bins=10)
    p = figure(title=title, background_fill_color="#fafafa") #Creates base of graph
    #Creates the rectangles for the histogram
    #Left is all boundries except for the last one
    #Right is all boundries except the first
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="navy", line_color="white", alpha=0.5)

    #signifies where the y starts
    p.y_range.start = 0
    p.xaxis.axis_label = 'Eye Ratio'
    p.yaxis.axis_label = 'Frequency'
    p.grid.grid_line_color="white"
    return p
def make_line_plot(title, data):
    #Creates a line plot based on time
    linePlot = figure(title=title, x_axis_type="datetime", plot_width=800, plot_height=500)
    #the x data should be formated in date time format
    x = data[0]
    #Y would be some thing like eyeRatio
    y = data[1]
    linePlot.line(x,y)
    linePlot.circle(x,y, size=7)
    return linePlot



eyeRatios = np.random.random_sample(30)
rng = pd.date_range('2018-01-01', periods=30, freq='S')

week = [rng, eyeRatios]
p1 = make_histo("Eye Ratio Tracking", eyeRatios, eyeRatios)

p2 = make_line_plot("Eye Ratio Tracking", week)
output_file('histogram.html', title="histogram.py example")



# add a text renderer to our plot (no data yet)
r = linePlot.circle(x=[], y=[])


ds = r.data_source

# create a callback that will add a number in a random location
def callback():

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    new_data['x'] = ds.data['x'] + [random()*70 + 15]
    new_data['y'] = ds.data['y'] + [random()*70 + 15]
    ds.data = new_data


# add a button widget and configure with the call back
button = Button(label="Press Me")
button.on_click(callback)

# # put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p2))

>>>>>>> a9801e41202392496766b35e742b2b9338658966

