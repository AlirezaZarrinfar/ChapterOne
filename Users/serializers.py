from rest_framework import serializers


class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    fullname = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True)
