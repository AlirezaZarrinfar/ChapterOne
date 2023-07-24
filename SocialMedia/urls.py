from SocialMedia.views import *
from django.urls import path,include

app_name = 'SocialMedia'

urlpatterns = [
    path('getbooks/', GetBooksView.as_view(), name='books_get'),
    path('rate-books/', RateBookView.as_view(), name='books_rate'),
    path('toggle-favorite-book/', ToggleFavoriteBookView.as_view(), name='books_favorite'),
    path('get-favorite-books/<int:user_id>', FavoriteBooksListView.as_view(), name='favorite_books_list'),
    path('toggle-follow/', ToggleFollowView.as_view(), name='toggle_follow'),
    path('followers/<int:user_id>/', FollowersView.as_view(), name='followers'),
    path('followings/<int:user_id>/', FollowingView.as_view(), name='following'),
    path('comments/add/', CreateCommentView.as_view(), name='add_comment'),
    path('comment/get/<int:book_id>/', GetCommentsView.as_view(), name='book-comments'),
    path('authors/<int:book_id>', GetAuthorView.as_view(), name='author-filter'),
    path('books-by-author/<int:author_id>/', GetBooksByAuthorView.as_view(), name='books-by-author'),
    path('books/rating/<int:book_id>', GetBookRatingView.as_view(), name='book_rating'),
    path('rating/count/<int:book_id>', GetRatingCountView.as_view(), name='rating_count'),

]
