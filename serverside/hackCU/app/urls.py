from django.urls import path

from .views import  *
from .apps import updateUserData

urlpatterns = [
        path('', renderHome, name='home'),
        #handels post requests

        #handels the boolean switch from driving to not driving
        path('users/<str:username>/', renderUserPage),

        #handels  specific data being sent to the user
        path('users/<str:username>/update/', updateUserData),
        path('users/<str:username>/addDrive/', updateDrive),
        #path('users/<str:username>/stats/', updateUserData),

        ]


#timeSpent
#
