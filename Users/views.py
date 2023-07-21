from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from Users.models import User
from Users.serializers import UserSignUpSerializer, UserSignInSerializer, ChangePasswordSerializer, \
    UserProfileSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class UserSignUpView(APIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        ser_data = UserSignUpSerializer(data=request.data)
        if ser_data.is_valid():
            user = User.objects.create_user(
                ser_data.validated_data['email'],
                ser_data.validated_data['fullname'],
                ser_data.validated_data['password'],
            )
            token, created = Token.objects.get_or_create(user=user)
            result = {'token': 'Token ' + token.key, 'userId': user.id}
            return Response({
                'msg': 'successfully logged in !!',
                'code': status.HTTP_200_OK,
                'data': result
            }, status=status.HTTP_200_OK)
        return Response({
            'msg': ser_data.errors,
            'code': status.HTTP_400_BAD_REQUEST,
            'data': ''
        }, status=status.HTTP_400_BAD_REQUEST)


class UserSignInView(APIView):
    serializer_class = UserSignInSerializer

    def post(self, request):
        ser_data = UserSignInSerializer(data=request.data)
        if ser_data.is_valid():
            user = ser_data.validated_data
            token, created = Token.objects.get_or_create(user=user)
            result = {'token': 'Token ' + token.key, 'userId': user.id}
            return Response({
                'msg': 'successfully logged in !!',
                'code': status.HTTP_200_OK,
                'data': result
            }, status=status.HTTP_200_OK)
        return Response({
            'msg': ser_data.errors,
            'code': status.HTTP_400_BAD_REQUEST,
            'data': ''
        }, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        user = request.user
        if serializer.is_valid():
            new_pass = serializer.validated_data['new_password']
            user.set_password(new_pass)
            user.save()
            response = {
                'code': status.HTTP_200_OK,
                'msg': 'password updated successfully',
                'data': ''
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response({
            'msg': serializer.errors,
            'code': status.HTTP_400_BAD_REQUEST,
            'data': ''
        }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    lookup_field = 'id'  # نام فیلد در مدل که برای جستجو استفاده می‌شود
    lookup_url_kwarg = 'user_id'
