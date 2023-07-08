from django.urls import path,include
from .views import *

app_name = 'Users'

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user_signup'),
    path('signin/', UserSignInView.as_view(), name='user_signin'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

]
