from django.urls import path

from .views import  *

urlpatterns = [
        path('', renderHome, name='home'),
        #handels post requests

        #handels the boolean switch from driving to not driving
        path('users/<str:username>/', renderUserPage),

        #handels  specific data being sent to the user
        path('users/<str:username>/update/', updateUserData),
        path('users/<str:username>/addDrive/', updateDrive),

        ]


#timeSpent
#
