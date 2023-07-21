from builtins import id

from django.shortcuts import render
from django_filters import filterset
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, generics
from rest_framework.views import APIView
from SocialMedia.models import Book, Rating, Comment, Author
from SocialMedia.serializers import GetBooksSerializer, RateBookSerializer, \
    ToggleFollowSerializer, FollowSerializer, ToggleFavoriteBookSerializer, \
    FavoriteBooksListSerializer, CreateCommentSerializer, GetCommentSerializer, GetAuthorSerializer
from rest_framework.response import Response
from rest_framework import status

from Users.models import User


class GetBookFilterSet(filterset.FilterSet):
    genres = filterset.CharFilter(method='filter_genres')

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'release_date', 'genres']

    def filter_genres(self, queryset, name, value):
        genres_list = value.split(',')
        return queryset.filter(genres__in=genres_list)


class GetBooksView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetBooksSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    queryset = Book.objects.get_queryset()
    filterset_class = GetBookFilterSet
    search_fields = ['name', 'description', 'release_date', 'genres']

    def get(self, request, *args, **kwargs):
        data = super().get(self, request, *args, **kwargs).data
        if len(data) != 0:
            return Response({
                'data': list(data),
                'msg': 'success !!',
                'code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
            'data': [],
            'msg': 'there is no books in the database !!',
            'code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)


class RateBookView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RateBookSerializer

    def post(self, request):
        serializer = RateBookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            rating = serializer.validated_data['rating']
            book = serializer.validated_data['book']
            new_rating = Rating(user=request.user, book=book, rating=rating)
            new_rating.save()

            return Response({
                'data': 'Book rated successfully',
                'msg': 'success !!',
                'code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
            'data': [],
            'msg': serializer.errors,
            'code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)


class ToggleFavoriteBookView(generics.UpdateAPIView):
    serializer_class = ToggleFavoriteBookSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            message = serializer.save()
            return Response({
                'data': [],
                'msg': message,
                'code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
            'data': [],
            'msg': serializer.errors,
            'code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)


class FavoriteBooksListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request,*args,**kwargs):
        userid = self.kwargs['user_id']
        user = User.objects.get(id=userid)
        favorite_books = user.favorite_books
        serializer = FavoriteBooksListSerializer(favorite_books, many=True)
        if serializer.data:
            return Response({
                'data': serializer.data,
                'msg': 'books get successfully !',
                'code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
            'data': [],
            'msg': serializer.errors,
            'code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)


class ToggleFollowView(APIView):
    serializer_class = ToggleFollowSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ToggleFollowSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            message = serializer.toggle_follow(serializer.validated_data['user_id'])
            return Response({
                'data': [],
                'msg': 'user ' + message + ' successful.',
                'code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
            'data': [],
            'msg': serializer.errors,
            'code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)


class FollowersView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            followers = user.followers.all()
            serializer = FollowSerializer(followers, many=True)
            message = 'successfully done !'
            if len(serializer.data) == 0:
                message = 'user does not have followers'
            return Response({
                'data': serializer.data,
                'msg': message,
                'code': status.HTTP_200_OK
            })
        except User.DoesNotExist:
            return Response({
                'data': [],
                'msg': 'user does not exist',
                'code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)


class FollowingView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            following = user.following.all()
            serializer = FollowSerializer(following, many=True)
            message = 'successfully done !'
            if len(serializer.data) == 0:
                message = 'user does not have followings'
            return Response({
                'data': serializer.data,
                'msg': message,
                'code': status.HTTP_200_OK
            })
        except User.DoesNotExist:
            return Response({
                'data': [],
                'msg': 'does not exist',
                'code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)


class CreateCommentView(generics.CreateAPIView):
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]  # Set the permission to IsAuthenticated

    def perform_create(self, serializer):
        book_id = self.request.data.get('book_id')  # Get the book_id from the request data
        book = Book.objects.get(pk=book_id)
        serializer.save(user=self.request.user, book=book)



class GetCommentView(generics.ListAPIView):
    serializer_class = GetCommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return Comment.objects.filter(book=book_id, parent_comment=None)


class GetAuthorView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GetAuthorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    queryset = Author.objects.get_queryset()
    filterset_fields = ['id', 'full_name']
    search_fields = ['full_name']

    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['book_id']
        if book_id != 0:
            book = Book.objects.filter(pk=book_id)
            self.queryset = Author.objects.filter(books_written__in=book)
        data = super().get(self, request, *args, **kwargs).data
        if len(data) != 0:
            return Response({
                'data': list(data),
                'msg': 'success !!',
                'code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        return Response({
            'data': [],
            'msg': 'there is no books in the database !!',
            'code': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)


class GetBooksByAuthorView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, author_id):
        try:
            author = Author.objects.get(id=author_id)
            books = Book.objects.filter(authors__in=[author])
            serializer = GetBooksSerializer(books, many=True)
            return Response({
                'data': serializer.data,
                'msg': 'success !!',
                'code': status.HTTP_200_OK
            }, status=status.HTTP_200_OK)
        except Author.DoesNotExist:
            return Response({
                'data': [],
                'msg': 'Author not found',
                'code': status.HTTP_400_BAD_REQUEST
            }, status=status.HTTP_400_BAD_REQUEST)


