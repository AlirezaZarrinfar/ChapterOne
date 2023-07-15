from SocialMedia.views import *
from django.urls import path,include

app_name = 'SocialMedia'

urlpatterns = [
    path('getbooks/', GetBooksView.as_view(), name='books_get'),
    path('rate-books/', RateBookView.as_view(), name='books_rate'),
    path('toggle-favorite-book/', ToggleFavoriteBookView.as_view(), name='books_favorite'),
    path('get-favorite-books/', FavoriteBooksListView.as_view(), name='favorite_books_list'),
    path('toggle-follow/', ToggleFollowView.as_view(), name='toggle_follow'),
    path('followers/<int:user_id>/', FollowersView.as_view(), name='followers'),
    path('followings/<int:user_id>/', FollowingView.as_view(), name='following'),

]
