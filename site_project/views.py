from rest_framework.response import Response
from rest_framework import status, generics

from otp_app.permission import IsAuthenticatedAndVerified
from otp_app.serializers import UserSerializer
from otp_app.models import UserModel

from django.contrib.sessions.models import Session
from django.utils import timezone

class HomeView(generics.ListAPIView):
    def get(self, request):
        user = request.user  # Получение пользователя из запроса
        if user.is_authenticated:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({'detail': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


        #return Response({"status": "success", "message": "home page", "session_id": request.session.session_key})

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request  # Добавляем 'request' в контекст
        return context

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)