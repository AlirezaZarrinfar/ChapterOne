from django.urls import path
from .views import *

app_name = 'Users'

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user_signup')
]
