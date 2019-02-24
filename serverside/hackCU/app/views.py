from django.shortcuts import render

from django.http import HttpResponse

from django.template import loader

from django.views.decorators.csrf import csrf_exempt

from .models import *

from django import forms

contextMain = {}


# Create your views here.

class UserForm(forms.Form):
    firstname = forms.CharField(max_length = 100)
    lastname = forms.CharField(max_length = 255)
    age = forms.IntegerField()


class StatusForm(forms.Form):
    driving = forms.BooleanField(required = False)

class UpdateForm(forms.Form):
    instantAverage = forms.IntegerField()
    tripAverage = forms.IntegerField()


#works
@csrf_exempt
def renderUserPage(request, username):
    
    #user object is the username (should be using id in the url but this is a hackathon, easy to change)
    userObject = User.objects.get(firstname = username)
    
    #if this page recieves a post request, it will change driving to true
    #if driving is true render a different page, otherwise render the default page

    if request.method == "POST":
        form = StatusForm(request.POST)
    print(request.POST.get('driving'))
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



@csrf_exempt
def updateUserData(request, username):
    userObject = User.objects.get(firstname = username)
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            instantAverage = form.cleaned_data['instantAverage']
            tripAverage = form.cleaned_data['tripAverage']
            
        print("Data updated user data")
        print(f"changed data: trip --- {tripAverage} --- instantaneous  --- {instantAverage}")
    template = "driving.html"
    _template = loader.get_template(template)
    return HttpResponse(_template.render())

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



def updateData(request):
    if request.method == "POST":
        form = UpdateForm(request.POST)
        if form.is_valid():
            _
