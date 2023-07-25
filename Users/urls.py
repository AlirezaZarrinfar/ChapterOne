from django.urls import path,include
from .views import *

app_name = 'Users'

urlpatterns = [
    path('signup/', UserSignUpView.as_view(), name='user_signup'),
    path('signin/', UserSignInView.as_view(), name='user_signin'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('getprofile/<int:user_id>/', UserProfileView.as_view(), name='getprofile'),
    path('profile/update/', UserProfileEditView.as_view(), name='update-profile'),
    path('profile/search/', UserSearchView.as_view(), name='user-search'),

]
