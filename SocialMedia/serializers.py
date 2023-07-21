from rest_framework import serializers
from rest_framework.generics import get_object_or_404

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


from rest_framework import serializers
from .models import Book, Comment


class CreateCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True,
                                              default=serializers.CurrentUserDefault())
    book_id = serializers.IntegerField(required=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'created_at', 'parent_comment', 'book_id')


class GetCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.full_name')
    replies = serializers.SerializerMethodField()

    def get_replies(self, obj):
        replies = Comment.objects.filter(parent_comment=obj.id)
        serializer = GetCommentSerializer(replies, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'created_at', 'replies')


class GetAuthorSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    full_name = serializers.CharField(max_length=100, required=False)
    book_id = serializers.IntegerField(required=False, write_only=True)
    biography = serializers.CharField(read_only=True)
    birth_date = serializers.DateField(read_only=True)
    country = serializers.CharField(max_length=100)
    image = serializers.CharField(max_length=100)


class GetBookRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('user', 'book', 'rating')