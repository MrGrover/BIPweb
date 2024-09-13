from django.shortcuts import render
from rest_framework import generics

from otp_app.models import get_user_id
from otp_app.permission import IsAuthenticatedAndVerified
from .models import Survey
from .serializers import SurveySerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import SurveyAnswer
from .serializers import SurveyAnswerSerializer


class SurveyDetailView(generics.RetrieveAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = [IsAuthenticatedAndVerified]


class SubmitSurveyView(generics.CreateAPIView):
    serializer_class = SurveyAnswerSerializer
    permission_classes = [IsAuthenticatedAndVerified]

    def post(self, request, *args, **kwargs):
        user_id = get_user_id(request)
        print('user_id: ', user_id)
        data = request.data

        # Пройдем по каждому вопросу и сохраним ответы
        answers = data.get('answers', [])
        for answer in answers:
            serializer = self.get_serializer(data={
                'user': user_id,
                'question': answer['question_id'],
                'answer_text': answer['answer_text']
            })
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "success", "message": "Survey submitted successfully."}, status=status.HTTP_201_CREATED)

