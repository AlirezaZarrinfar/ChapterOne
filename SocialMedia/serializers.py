from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from SocialMedia.models import Book, Rating
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
            raise serializers.ValidationError({'error': 'You have already rated this book.'})

        data['book'] = book
        return data


class ToggleFavoriteBookSerializer(serializers.Serializer):
    book_id = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        book_id = attrs.get('book_id')

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Book not found.")

        attrs['book'] = book
        return attrs

    def update(self, instance, validated_data):
        book = validated_data.get('book')

        if book in instance.favorite_books.all():
            instance.favorite_books.remove(book)
            message = 'Book removed from favorites.'
        else:
            instance.favorite_books.add(book)
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