from django.urls import path

from survey_app.views import SurveyDetailView, SubmitSurveyView

urlpatterns = [
    path('<int:pk>/', SurveyDetailView.as_view(), name='survey_detail'),
    path('submit', SubmitSurveyView.as_view(), name='submit-survey'),
    ]