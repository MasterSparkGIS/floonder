from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from auth.auth import IsMember
from generic_serializers.serializers import ResponseSerializer
from users.models import User
from users.serializers.serializers import UserSerializer


class JWTObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        token['email'] = user.email
        token['id'] = user.id
        return token


class JwtObtain(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            raise NotFound('User does not exist!')

        if not user.active:
            raise ValidationError({
                'email': ['User is not active']
            })

        if not user.check_password(request.data.get('password')):
            raise ValidationError({
                'password': ['Password is incorrect']
            })

        response = super().post(request, *args, **kwargs)

        response.data['email'] = user.email
        response.data['id'] = user.id

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': response.data,
            'error': None,
        })

        return Response(serializer.data)


class RefreshToken(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        serializer = ResponseSerializer({
            'code': 200,
            'status': 'success',
            'recordsTotal': 1,
            'data': response.data,
            'error': None,
        })

        return Response(serializer.data)


class RegisterViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsMember]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            raise ValidationError(serializer.errors)

        self.perform_create(serializer)

        resp = ResponseSerializer({
            'code': 201,
            'status': 'success',
            'recordsTotal': 1,
            'data': {
                "message": "User created successfully"
            },
            'error': None,
        })

        return Response(resp.data)
