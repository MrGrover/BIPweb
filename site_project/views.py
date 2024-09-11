from rest_framework.response import Response
from rest_framework import status, generics
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

