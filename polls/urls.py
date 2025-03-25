from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, LoginView,
    CreateQuestionView, VoteView, UserVotedQuestionsView
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-question/', CreateQuestionView.as_view(), name='create_question'),
    path('vote/', VoteView.as_view(), name='vote'),
    path('user-voted-questions/', UserVotedQuestionsView.as_view(), name='user_voted_questions'),
]
