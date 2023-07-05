from rest_framework.views import APIView
from Users.models import User
from Users.serializers import UserSignUpSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class UserSignUpView(APIView):
    serializer_class = UserSignUpSerializer
    def post(self, request):
        ser_data = UserSignUpSerializer(data=request.data)
        if ser_data.is_valid():
            user = User.objects.create_user(
                ser_data.validated_data['email'],
                ser_data.validated_data['fullname'],
                ser_data.validated_data['password']
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response(token.key)
        return Response(ser_data.errors)
