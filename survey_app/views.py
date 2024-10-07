from django.shortcuts import render
from rest_framework import generics

from otp_app.models import get_user_id
from otp_app.permission import IsAuthenticatedAndVerified
from .MLApi import get_model_answer
from .models import Survey
from .serializers import SurveySerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import SurveyAnswer
from .serializers import SurveyAnswerSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import SurveyAnswer, SurveyQuestion
from .serializers import SurveyAnswerSerializer


class SurveyDetailView(generics.RetrieveAPIView):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer


def parse_answer(question_id, answer):
    print(question_id, answer)
    if question_id == 1:
        if int(answer) in range(20, 66):
            #print('proba')
            return answer
        else:
            #print('proba')
            return 20
    elif question_id == 2:
        if answer.lower() in ('мужской', 'женский'):
            return answer.lower()
        else:
            #print('proba')
            return 'мужской'
    else:
        if answer.lower() in ('да', 'нет'):
            return answer.lower()


class SubmitSurveyView(generics.GenericAPIView):
    serializer_class = SurveyAnswerSerializer

    def post(self, request, *args, **kwargs):
        user = request.user  # Текущий пользователь
        data = request.data

        # Получаем ответы из запроса
        answers = data.get('answers', [])

        # Проходим по каждому вопросу
        for answer_data in answers:
            question_id = answer_data['question_id']
            answer_text = parse_answer(question_id, answer_data['answer_text'])

            # Ищем вопрос
            question = SurveyQuestion.objects.get(id=question_id)

            # Проверяем, существует ли уже ответ на этот вопрос для данного пользователя
            existing_answer = SurveyAnswer.objects.filter(user=user, question=question).first()

            if existing_answer:
                # Если ответ существует, обновляем его
                existing_answer.answer_text = answer_text
                existing_answer.save()
            else:
                # Если ответа нет, создаём новый
                SurveyAnswer.objects.create(
                    user=user,
                    question=question,
                    answer_text=answer_text
                )

        return Response({"status": "success", "message": "Survey answers submitted successfully."},
                        status=status.HTTP_200_OK)


class SurveyResultsView(generics.GenericAPIView):
    def get(self, request, survey_id, *args, **kwargs):
        user = request.user
        survey = get_object_or_404(Survey, id=survey_id)

        # Получаем все вопросы опроса
        questions = survey.questions.all()
        questions_data = []

        answer_for_ml = []

        # Для каждого вопроса находим ответ пользователя
        for question in questions:
            user_answer = SurveyAnswer.objects.filter(user=user, question=question).first()
            question_data = {
                'question': question.text,
                'answer': user_answer.answer_text if user_answer else "No answer"
            }
            answer_for_ml.append(user_answer.answer_text if user_answer else "No answer")
            questions_data.append(question_data)
        #print(answer_for_ml)
        survey_result = get_model_answer(answer_for_ml)
        if survey_result:
            result_text = "Модель предсказывает, что пациент болен диабетом (Positive)."
        else:
            result_text = "Модель предсказывает, что пациент НЕ болен диабетом (Negative)."
        return Response({
            'survey': survey.name,
            'description': survey.description,
            'questions': questions_data,
            'result': result_text
        })
