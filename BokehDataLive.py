import random
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource


def make_doc(doc):
    #Defines format for data
    dataFormat = {
        "Time": [],
        "EyeR": [],
    }
    #Establishes the dict that new data will be added to
    source = ColumnDataSource(dataFormat)

    ##THIS IS THE FUNCTION THAT SHOULD TAKE IN THE Avg EyeR of last 20sec and Time
    ##Function describes how new data will be added
    # def update(eyeRatio, time):
    #     #Format for new data
    #     newData = {
    #         "Time": [eyeRatio],
    #         "EyeR": [time],
    #     }
    #     #Append new data to og source
    #     source.stream(newData)


    #PROOF OF CONCEPT
    # def update():
    #     #Format for new data
    #     newData = {
    #         "Time": [random.random()],
    #         "EyeR": [random.random()],
    #     }
    #     #Append new data to og source
    #     source.stream(newData)






    #calls the update every 100 ms 
    doc.add_periodic_callback(update, 100)

    #Creates the actual graphs
    linePlot = figure(title="Eye Tracking", plot_width=800, plot_height=500)
    #Creates circles
    linePlot.circle(x='Time', y='EyeR', source=source)
    #Creates line connections between points
    linePlot.line(x='Time', y='EyeR', source=source)
    #making it the root means the page updates any times the figure changes
    doc.add_root(linePlot)
apps = {'/': Application(FunctionHandler(make_doc))}
server = Server(apps, port=5001)
server.start()

