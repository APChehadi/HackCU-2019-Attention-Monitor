from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django import forms
from .BokehData import GraphCreation
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.io import show, output_file
from bokeh.layouts import gridplot
from twilio.rest import Client
import numpy as np
import pandas as pd
from random import random

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file, curdoc
from bokeh.layouts import column
from bokeh.models import Button
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import show, output_file
from bokeh.embed import components
from .models import *

account_sid = 'AC107dd89200d937d6c197b15e9ba2b840'
auth_token = '6a6eaf96aadae02d8c45bc364d88eccd'



contextMain = {}


# Create your views here.
######################################     FORMS     ######################################
class UserForm(forms.Form):
    firstname = forms.CharField(max_length = 100)
    lastname = forms.CharField(max_length = 255)
    age = forms.IntegerField()

class StatusForm(forms.Form):
    driving = forms.BooleanField(required = False)

class UpdateForm(forms.Form):
    instantEyeRatio = forms.DecimalField(max_digits = 4, decimal_places = 2)
    overallEyeRatio = forms.DecimalField(max_digits = 4, decimal_places = 2)
    time = forms.IntegerField()


class UpdateDriverForm(forms.Form):
    distTraveled = forms.IntegerField()
    eyeRatio = forms.DecimalField(max_digits=5, decimal_places=2)
    timeSpent = forms.IntegerField()


######################################     RENDERERS     ######################################
#render unique page for a user
@csrf_exempt
def renderUserPage(request, username):

    #user object is the username (should be using id in the url but this is a hackathon, easy to change)
    userObject = User.objects.get(firstname = username)


    #if this page recieves a post request, it will change driving to true
    #if driving is true render a different page, otherwise render the default page
    if request.method == "POST":
        form = StatusForm(request.POST)
        # print(request.POST.get('driving'))
        #only listens to on / off switch
        if form.is_valid():
            #change the state of the driver
            # print(form.cleaned_data['driving'])
            userObject.driving = form.cleaned_data['driving']
            userObject.save()

    if userObject.driving:
        _template = "driving.html"
        eyeRatio, times = returnDriveData(username)

        # touple = returnDriveData(username)
        # h , l = newGraph.defaultCreation()
        # newGraph = GraphCreation(username, touple)
        #
        # script1, div1 = components(l, CDN)
        # script2, div2 = components(h, CDN)
        #
        contextMain = {"NAME":username, "eyeRatio":eyeRatio, "times":times}
    else:
        deleteDriveData(username)
        _template = "notDriving.html"
        lastname, firstname, age, netTimeRatio, netSpeedAverage, drives = returnUserData(username)

        contextMain = {"NAME":firstname, "LAST":lastname, "age":age, "netTimeRatio":netTimeRatio, "netSpeedAverage":netSpeedAverage, "drives":drives}


    #     touple = returnDriveData(username)
    #     newGraph = GraphCreation(username, touple)
    #     h , l = newGraph.defaultCreation()
    #
    #     script1, div1 = components(l, CDN)
    #     script2, div2 = components(h, CDN)
    #
    #
    #     contextMain = {"graph1" : script1, "graph1div" : div1, "graph2":script2, "graph2div" : div2}
    #     print(contextMain)
    #
    #
    template = loader.get_template(_template)
    return HttpResponse(template.render(contextMain))

#update the data for the user
@csrf_exempt
def updateUserData(request, username):
    userObject = User.objects.get(firstname = username)
    instantAverage = -1
    tripAverage = -1
    # print(userObject)
    #listens to an updated average and adds to an array
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            # print("hello")
            instantEyeRatio = form.cleaned_data['instantEyeRatio']
            time = form.cleaned_data['time']
            overallEyeRatio = form.cleaned_data['overallEyeRatio']
            InstRequest.objects.create(username = username,
                    time = time,
                    dataPoint = userObject.dataPoint,
                    drNumber = userObject.drives,
                    eyeRatio = instantEyeRatio)

            userObject.dataPoint += 1

            userObject.save()


    contextMain = {"overallEyeRatio":overallEyeRatio}
    template = "driving.html"
    _template = loader.get_template(template)
    return HttpResponse(_template.render(contextMain))


@csrf_exempt
def twilioReaction(request):
    # print('kajbsf')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='+17205752756',
    body='Alert Driver is distracted',
    to='+13032506161')
    print(message.sid)
    return HttpResponse()



#home page (make an account with post request)
@csrf_exempt
def renderHome(request):
    # print(returnDriveData("James"))

    template = loader.get_template('index.html')

    #for creating a new user
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            _firstname = form.cleaned_data['firstname']
            _lastname = form.cleaned_data['lastname']
            _age = form.cleaned_data['age']
            #netTimeRatio = forms.cleaned_data['netTimeRatio']
            #netSpeedAverage = forms.cleaned_data['netSpeedAverage']
            User.objects.create(firstname = _firstname,
                    lastname = _lastname,
                    age = _age,
                    netTimeRatio = 0,
                    netSpeedAverage = 0,
                    drives = 0,
                    driving = False,
                    dataPoint = 0)
            #create new user name
            # print(_age)
            # print(_firstname)
            # print(_lastname)
    return HttpResponse(template.render(contextMain))




@csrf_exempt
def updateDrive(request, username):
    userObject = User.objects.get(firstname = username)
    distTraveled = 0
    eyeRatio = 0
    timeSpent = 0

    #listens to an updated average and adds to an array (only sent on false post request)
    if request.method == "POST":
        form = UpdateDriverForm(request.POST)
        if form.is_valid():
            _distTraveled = form.cleaned_data['distTraveled']
            _eyeRatio = form.cleaned_data['eyeRatio']
            _timeSpent = form.cleaned_data['timeSpent']

            _id = userObject.drives + 1
            _userTag = username

            #update user
            userObject.netTimeRatio = (float(userObject.netTimeRatio * userObject.drives) + float(_eyeRatio)) / float(userObject.drives + 1)
            userObject.netSpeedAverage = ((float(userObject.netSpeedAverage) * float(userObject.drives)) + (float(_distTraveled) / float(_timeSpent))) / (float(userObject.drives + 1))

            userObject.drives += 1
            userObject.dataPoint = 0

            # InstRequest.objects.filter(username = username).delete()
            userObject.save()


            #create a new drive tied to a user
            Driver.objects.create(distTraveled = _distTraveled,
                                eyeRatio = _eyeRatio,
                                timeSpent = _timeSpent,
                                idVal = _id,
                                userTag = _userTag)
            # print(_distTraveled)
            # print(_eyeRatio)
            # print(_timeSpent)
    return HttpResponse()




@csrf_exempt
def render_twilio(request):
    _template = "twilionode.html"
    template = loader.get_template(_template)
    return HttpResponse(template.render())



def returnDriveData(username):
        times = InstRequest.objects.filter(username = username).order_by('time').values_list('time', flat=True)
        #times = InstRequest.objects.filter(username = username).values_list('time', flat=True)
        times = list(times)

        eyeRatio = InstRequest.objects.filter(username = username).order_by('time').values_list('eyeRatio', flat=True)
        eyeRatio = list(eyeRatio)
        # print(eyeRatio, times)
        return eyeRatio, times


def deleteDriveData(username):
        times = InstRequest.objects.filter(username = username)
        times.delete()


def returnDriverHistoryData(username):
        distTraveled = Driver.objects.filter(userTag = username).order_by('idVal').values_list('distTraveled', flat=True)
        distTraveled = list(distTraveled)

        eyeRatio = Driver.objects.filter(userTag = username).order_by('idVal').values_list('eyeRatio', flat=True)
        eyeRatio = list(eyeRatio)

        timeSpent = Driver.objects.filter(userTag = username).order_by('idVal').values_list('timeSpend', flat=True)
        timeSpent = list(timeSpent)

        return distTraveled, eyeRatio, timeSpent


def returnUserData(username):
        userObject = User.objects.get(firstname = username)
        return userObject.lastname, userObject.firstname, userObject.age, userObject.netTimeRatio, userObject.netSpeedAverage, userObject.drives



class GraphCreation():
    def __init__(self, title, array):
        self.title = title
        self.array = array

    #
    # def readData(self, jsonData):
    #     self.array = [jsonData['time'],jsonData['InstantEyeRatio']]

    #declare self.array

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


def runFunction(request, username):
    eyeRatio = InstRequest.objects.filter(username = username).values_list('eyeRatio', flat=True)
    timeSpent = InstRequest.objects.filter(username = username).values_list('time', flat=True)
    rng = pd.date_range('2018-01-01', periods=30, freq = 'S')
    timeSpent = [float(x) for x in list(timeSpent)]
    eyeRatio = [float(x) for x in list(eyeRatio)]
    i = 0
    for x in range(len(timeSpent)):
        i = i + timeSpent[x]
        timeSpent[x] += i


    # print(timeSpent)
    week = [timeSpent, eyeRatio]
    p1 = GraphCreation("Eye Ratio Tracking", week)
    histo = p1.make_histo('Eye Ratio', 'Frequency')

    lineGraph = p1.make_line_plot("Time", "Eye Ratio")


    output_file('Graphs.html', title="histogram.py example")
    grid = gridplot([histo, lineGraph], ncols=2, plot_width=400, plot_height=400)
    show(grid)




    return HttpResponse()
