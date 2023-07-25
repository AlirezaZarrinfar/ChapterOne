from django.contrib.auth import authenticate
from jsonschema.exceptions import ValidationError
from rest_framework import serializers
from rest_framework import status
from rest_framework.fields import CurrentUserDefault

from Users.models import User


class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    fullname = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if not User.validate_password(password):
            password_validations = [
                "Password must be at least 8 characters long.",
                "Password must contain at least one uppercase letter and one lowercase letter.",
            ]
            raise serializers.ValidationError(detail={'error': password_validations})
        user = User.objects.filter(email=email)
        if user:
            raise serializers.ValidationError(detail={'error': 'your email already exists !'})
        return attrs


class UserSignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({'error': 'email or password is wrong'})
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        request = self.context['request']
        old_pass = attrs.get('old_password')
        if not request.user.check_password(old_pass):
            raise serializers.ValidationError(detail={'error': 'old password is incorrect !!'})
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'date_joined', 'following_num', 'followers_num']

class UpdateUserProfileSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=True)

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.save()
        return instance

class UserSearchSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False , allow_null=True , allow_blank=True)
    email = serializers.CharField(required=False , allow_null=True , allow_blank=True)