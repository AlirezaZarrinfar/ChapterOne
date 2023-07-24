from django.shortcuts import get_object_or_404
from rest_framework import serializers

from SocialMedia.models import Book, Rating, Comment, Author, FavoriteBook
from Users.models import User


class GetBooksSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    search = serializers.CharField(write_only=True)
    name = serializers.CharField()
    release_date = serializers.DateField()
    genres = serializers.CharField()
    description = serializers.CharField()
    image = serializers.CharField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)


class RateBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(write_only=True)
    rating = serializers.IntegerField(write_only=True, max_value=5, min_value=1)

    def validate(self, data):
        book_id = data.get('book_id')
        rating = data.get('rating')

        if not rating:
            raise serializers.ValidationError({'error': 'Rating value is required.'})

        book = Book.objects.filter(pk=book_id).first()
        if not book:
            raise serializers.ValidationError({'error': 'book does not exist.'})
        # Check if the user has already rated the book
        user = self.context['request'].user
        existing_rating = Rating.objects.filter(user=user, book=book).first()
        if existing_rating:
            data['book'] = book
            data['existing_rating'] = existing_rating
            return data

        data['book'] = book
        data['existing_rating'] = None
        return data


class ToggleFavoriteBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(write_only=True)
    status = serializers.CharField()

    def validate(self, attrs):
        book_id = attrs.get('book_id')
        status = attrs.get('status')
        if status not in ('خوانده شده', 'درحال خواندن', 'برای خواندن'):
            raise serializers.ValidationError("Invalid Input.")
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found.")

        attrs['book'] = book
        return attrs

    def update(self, instance, validated_data):
        book = validated_data.get('book')
        status = validated_data.get('status')
        if book in instance.favorite_books.all():
            instance.favorite_books.remove(book)
            message = 'Book removed from favorites.'
        else:
            favoritebook = FavoriteBook.objects.create(user=instance, book=book, status=status)
            favoritebook.save()
            message = 'Book added to favorites.'

        return message


class FavoriteBooksListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'release_date', 'description', 'genres', 'image', 'average_rating']
        read_only_fields = ['id', 'name', 'release_date', 'description', 'genres', 'image', 'average_rating']


class ToggleFollowSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with the provided ID does not exist.')

        return user

    def toggle_follow(self, user):
        current_user = self.context['request'].user
        if user in current_user.following.all():
            current_user.following.remove(user)
            current_user.following_num -= 1
            user.followers_num -= 1
            current_user.save()
            user.save()
            return 'unfollowed'
        else:
            current_user.following.add(user)
            current_user.following_num += 1
            user.followers_num += 1
            current_user.save()
            user.save()
            return 'followed'


class FollowSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
class CreateCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True,
                                              default=serializers.CurrentUserDefault())
    book_id = serializers.IntegerField(required=True)
    parent_comment_id = serializers.IntegerField(required=False)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'created_at', 'parent_comment_id', 'book_id')

    def validate_book_id(self, value):
        try:
            book = Book.objects.get(pk=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found.")
        return value

    def validate_parent_comment_id(self, value):
        if value:
            try:
                parent_comment = Comment.objects.get(pk=value)
            except Comment.DoesNotExist:
                raise serializers.ValidationError("Parent comment not found.")
        return value

    def create(self, validated_data):
        book_id = validated_data.pop('book_id')
        parent_comment_id = validated_data.pop('parent_comment_id', None)
        book = Book.objects.get(pk=book_id)
        parent_comment = None
        if parent_comment_id:
            parent_comment = Comment.objects.get(pk=parent_comment_id)
        request = self.context['request']
        comment = Comment.objects.create(book=book, parent_comment=parent_comment, user=request.user, **validated_data)
        return comment

class GetAuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    full_name = serializers.CharField(max_length=100, required=False)
    book_id = serializers.IntegerField(required=False, write_only=True)
    biography = serializers.CharField(read_only=True)
    birth_date = serializers.DateField(read_only=True)
    country = serializers.CharField(max_length=100)
    image = serializers.CharField(max_length=100)
class GetBookRatingSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    book_id = serializers.IntegerField(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    def validate_book_id(self, book_id):
        try:
            book = Book.objects.get(id=book_id)
            return book_id
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found.")

    def validate(self, temp):
        data = self.initial_data
        book_id = data['book_id']
        user_id = data['user_id']

        try:
            book = Book.objects.get(id=book_id)
            user = User.objects.get(id=user_id)
            rating = Rating.objects.get(book=book, user=user)
            data['rating'] = rating.rating
            return data
        except (Book.DoesNotExist, User.DoesNotExist, Rating.DoesNotExist):
            raise serializers.ValidationError("Rating not found.")


class GetRatingCountSerializer(serializers.Serializer):
    count = serializers.IntegerField(read_only=True)

    def validate_book_id(self, value):
        book = Book.objects.filter(id=value).first()
        if not book:
            raise serializers.ValidationError("Book does not found !!")
        return value

    def validate(self, data):
        book_id = self.initial_data['book_id']
        rates = Rating.objects.filter(book_id=book_id)
        if not rates:
            raise serializers.ValidationError("Rates does not found !!")
        return data


class GetCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.full_name')
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'created_at', 'replies')

    def get_replies(self, instance):
        replies = Comment.objects.filter(parent_comment=instance.id)
        serializer = GetCommentSerializer(replies, many=True)
        return serializer.data

    def to_representation(self, instance):
        response_data = {
            "id": instance.id,
            "user": instance.user.full_name,
            "text": instance.text,
            "created_at": instance.created_at,
            "replies": self.get_replies(instance),
        }
        return response_data