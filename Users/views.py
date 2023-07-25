from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from Users.models import User
from Users.serializers import UserSignUpSerializer, UserSignInSerializer, ChangePasswordSerializer, \
    UserProfileSerializer, UpdateUserProfileSerializer, UserSearchSerializer
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

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        obj = queryset.filter(id=user_id).first()
        return obj

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            response_data = {
                "data": {},
                "msg": "User not found.",
                "code": status.HTTP_404_NOT_FOUND
            }
        else:
            serializer = self.get_serializer(instance)
            response_data = {
                "data": serializer.data,
                "msg": "User data retrieved successfully.",
                "code": status.HTTP_200_OK
            }

        return Response(response_data, status=response_data["code"])


class UserProfileEditView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserProfileSerializer
    def put(self, request):
        user = request.user
        serializer = UpdateUserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                "data": serializer.data,
                "msg": "User edited successfully.",
                "code": status.HTTP_200_OK
            }
            return Response(response_data)
        response_data = {
            "data": [],
            "msg": serializer.errors,
            "code": status.HTTP_400_BAD_REQUEST
        }
        return Response(response_data, status=400)


class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSearchSerializer
    def post(self, request):
        serializer = UserSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        full_name = serializer.validated_data.get('full_name')
        email = serializer.validated_data.get('email')

        users = User.objects.all()

        if full_name:
            users = users.filter(full_name__icontains=full_name)

        if email:
            users = users.filter(email__icontains=email)

        serializer = UserProfileSerializer(users, many=True)
        if len(serializer.data) != 0 :
            return Response({
                'data' : serializer.data,
                'msg' : 'User Found Successfully !!',
                'code' : status.HTTP_200_OK
            } ,status=status.HTTP_200_OK)
        return Response({
            'data': [],
            'msg': 'User not Found !!',
            'code': status.HTTP_404_NOT_FOUND
        }, status=status.HTTP_404_NOT_FOUND)

