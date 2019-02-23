from django.shortcuts import render

from django.http import HttpResponse

from django.template import loader

from django.views.decorators.csrf import csrf_exempt

from .models import *


from django import forms


# Create your views here.

class UserForm(forms.Form):
    firstname = forms.CharField(max_length = 100)
    lastname = forms.CharField(max_length = 255)
    age = forms.IntegerField()



contextMain = {}

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
                    netSpeedAverage = 0)        
            print(_age)
            print(_firstname)
            print(_lastname)
    return HttpResponse(template.render(contextMain))


