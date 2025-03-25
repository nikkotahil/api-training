from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView, QuestionListView,
    CreateQuestionView, VoteView, UserVotedQuestionsView,
    QuestionDetailView
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-question/', CreateQuestionView.as_view(), name='create_question'),
    path("questions/", QuestionListView.as_view(), name="question_list"),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('vote/', VoteView.as_view(), name='vote'),
    path('voted-questions/', UserVotedQuestionsView.as_view(), name='user-voted-questions'),
]
