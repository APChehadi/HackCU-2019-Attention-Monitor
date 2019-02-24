from django.shortcuts import render

from django.http import HttpResponse

from django.template import loader

from django.views.decorators.csrf import csrf_exempt

from .models import *

from django import forms

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
    instantAverage = forms.DecimalField(max_digits = 3, decimal_places = 2)
    overallAverage = forms.DecimalField(max_digits = 3, decimal_places = 2)

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
        print(request.POST.get('driving'))
        #only listens to on / off switch
        if form.is_valid():
            #change the state of the driver
            print(form.cleaned_data['driving'])
            userObject.driving = form.cleaned_data['driving']
            userObject.save()

    if userObject.driving:
        _template = "driving.html"
    else:
        _template = "notDriving.html"

    template = loader.get_template(_template)

    return HttpResponse(template.render(contextMain))


#update the data for the user
@csrf_exempt
def updateUserData(request, username):
    userObject = User.objects.get(firstname = username)
    instantAverage = -1
    tripAverage = -1

    #listens to an updated average and adds to an array
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            instantAverage = form.cleaned_data['instantAverage']
            overallAverage = form.cleaned_data['overallAverage']
            print("is  valid")
        print("Data updated user data")
        print(f"changed data: trip --- {overallAverage} --- instantaneous  --- {instantAverage}")
    template = "driving.html"
    _template = loader.get_template(template)
    return HttpResponse(_template.render())


#home page (make an account with post request)
@csrf_exempt
def renderHome(request):
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
                    driving = False)
            print(_age)
            print(_firstname)
            print(_lastname)
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
            userObject.save()
            #create a new drive tied to a user
            Driver.objects.create(distTraveled = _distTraveled,
                                eyeRatio = _eyeRatio,
                                timeSpent = _timeSpent,
                                idVal = _id,
                                userTag = _userTag)
            print(_distTraveled)
            print(_eyeRatio)
            print(_timeSpent)
    return HttpResponse()
