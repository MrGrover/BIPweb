from django.contrib.sessions.models import Session
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.utils import timezone

from otp_app.permission import IsAuthenticatedAndVerified
from otp_app.serializers import UserSerializer
from otp_app.models import UserModel
import pyotp



class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"status": "success", 'message': "Registered successfully, please login"},
                                status=status.HTTP_201_CREATED)
            except:
                return Response({"status": "fail", "message": "User with that email already exists"},
                                status=status.HTTP_409_CONFLICT)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        user = authenticate(username=email.lower(), password=password)

        if user is None:
            return Response({"status": "fail", "message": "Incorrect email or password"},
                            status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({"status": "fail", "message": "Incorrect email or password"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(user)
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"status": "success", "firstname": serializer.data['first_name'],
                         "lastname": serializer.data['last_name'], "email": serializer.data['email'],
                         "token": token.key})


class LogoutView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    def post(self, request):
        if request.user.is_authenticated:
            session_id = request.COOKIES.get('sessionid')
            if not session_id:
                return Response({"message": "Сессия не найдена."})
            # Находим сессию по session_id
            session = Session.objects.get(session_key=session_id)
            # Проверяем, не истекла ли сессия
            if session.expire_date < timezone.now():
                return Response({"message": "Сессия истекла."})
            # Получаем данные сессии
            session_data = session.get_decoded()
            # Извлекаем user_id из данных сессии
            user_id = session_data.get('_auth_user_id')
            user = UserModel.objects.filter(id=user_id).first()
            if user is None:
                return Response({"status": "fail", "message": f"No user with Id: {user_id} found"},
                                status=status.HTTP_404_NOT_FOUND)
            user.otp_verified = False
            user.save()
            serializer = self.serializer_class(user)
            try:
                token = Token.objects.get(user=request.user)
                token.delete()
            except Token.DoesNotExist:
                pass
            logout(request)
            return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

class GenerateOTP(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    def post(self, request):
        data = request.data
        #можно убрать эти запросы
        user_id = data.get('user_id', None)
        email = data.get('email', None)
        # проверка что зашел user
        user = UserModel.objects.filter(id=user_id).first()
        if user == None:
            return Response({"status": "fail", "message": f"No user with Id: {user_id} found"},
                            status=status.HTTP_404_NOT_FOUND)

        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
            name=email.lower(), issuer_name="codevoweb.com")

        user.otp_auth_url = otp_auth_url
        user.otp_base32 = otp_base32
        user.otp_mode = True
        user.save()
        # добавить ссылку на ввод далее
        return Response({'base32': otp_base32, "otpauth_url": otp_auth_url})


class VerifyOTP(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

    def post(self, request):
        data = request.data
        user_id = data.get('user_id', None)
        otp_token = data.get('otp_token', None)

        # Проверка наличия пользователя
        user = UserModel.objects.filter(id=user_id).first()
        if user is None:
            return Response({"status": "fail", "message": f"No user with Id: {user_id} found"},
                            status=status.HTTP_404_NOT_FOUND)

        # Проверка наличия секретного ключа для OTP
        if not user.otp_base32 and user.otp_mode:
            return Response({"status": "fail", "message": "OTP is not enabled for this user"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверка правильности введённого OTP
        totp = pyotp.TOTP(user.otp_base32)
        if not totp.verify(otp_token):
            return Response({"status": "fail", "message": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        # Верификация прошла успешно
        user.otp_verified = True
        user.save()

        # Возвращаем обновленные данные пользователя
        serializer = self.serializer_class(user)
        return Response({'otp_verified': True, "user": serializer.data}, status=status.HTTP_200_OK)


class DisableOTP(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    permission_classes = [IsAuthenticatedAndVerified]

    def post(self, request):
        print(request.user)
        data = request.data
        user_id = data.get('user_id', None)
        user = UserModel.objects.filter(id=user_id).first()
        if user is None:
            return Response({"status": "fail", "message": f"No user with Id: {user_id} found"},
                            status=status.HTTP_404_NOT_FOUND)

        user.otp_mode = False
        user.otp_verified = False
        user.otp_base32 = None
        user.otp_auth_url = None
        user.save()
        serializer = self.serializer_class(user)

        return Response({'otp_disabled': True, 'user': serializer.data})
