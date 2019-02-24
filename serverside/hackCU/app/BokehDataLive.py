import random
from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers.function import FunctionHandler
from bokeh.plotting import figure, ColumnDataSource
from django.shortcuts import render
from bokeh.resources import CDN
from bokeh.embed import components
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django import forms

@csrf_exempt
def update(time, eyeR):
    newData = {
        "Time": [time],
        "EyeR": [eyeR],
    }
    #Append new data to og source
    print('loafojsdbfpqadf')
    return newData


class ChangeForm(forms.Form):
    overallAverage = forms.DecimalField(max_digits = 3, decimal_places = 2)
    time = forms.IntegerField()

@csrf_exempt
def make_doc(request):
    #Defines format for data
    dataFormat = {
        "Time": [],
        "EyeR": [],
    }
    #Establishes the dict that new data will be added to
    source = ColumnDataSource(dataFormat)
    newData = {
        "Time": [0],
        "EyeR": [0],
    }
    ##THIS IS THE FUNCTION THAT SHOULD TAKE IN THE Avg EyeR of last 20sec and Time
    ##Function describes how new data will be added
    if request.method == "POST":
        form = ChangeForm(request.POST)
        print(request.POST.get('time'))
        #only listens to on / off switch
        if form.is_valid():
            #change the state of the driver
            print(form.cleaned_data['time'])
            time = form.cleaned_data['time']
            eyeR = form.cleaned_data['overallAverage']
            newData = update(time, eyeR)
    #calls the update every 100 ms
    #doc.add_periodic_callback(update, 100)
    print(newData['Time'])
    source.stream(newData)

    #Creates the actual graphs
    linePlot = figure(title="Eye Tracking", plot_width=800, plot_height=500)
    #Creates circles
    linePlot.circle(x='Time', y='EyeR', source=source)
    #Creates line connections between points
    linePlot.line(x='Time', y='EyeR', source=source)
    #making it the root means the page updates any times the figure changes
    #doc.add_root(linePlot)
    script, div = components(linePlot, CDN)

    return render(request, "simple_chart.html", {"the_script" : script, "the_div": div})

'''
apps = {'/': Application(FunctionHandler(make_doc))}
server = Server(apps, port=5001)
server.start()
'''
