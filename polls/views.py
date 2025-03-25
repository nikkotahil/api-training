from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Question, Choice, Vote
from django.contrib.auth import authenticate
from .serializers import (
    QuestionSerializer, RegisterSerializer
)
from django.contrib.auth import get_user_model

User = get_user_model()


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful",
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "user_type": user.user_type,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {"message": "User registered successfully!", "user": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CreateQuestionView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        question_text = request.data.get('question_text')
        choices = request.data.get('choices', [])

        if not question_text or not choices:
            return Response({"error": "Question and choices are required"}, status=400)

        question = Question.objects.create(question_text=question_text)
        for choice_text in choices:
            Choice.objects.create(question=question, choice_text=choice_text)

        return Response({"message": "Question created successfully"}, status=201)


class VoteView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user = request.user
        question_id = request.data.get('question_id')
        choice_id = request.data.get('choice_id')

        try:
            question = Question.objects.get(id=question_id)
            choice = Choice.objects.get(id=choice_id, question=question)
        except (Question.DoesNotExist, Choice.DoesNotExist):
            return Response({"error": "Invalid question or choice"}, status=400)

        if Vote.objects.filter(user=user, question=question).exists():
            return Response({"error": "You have already voted on this question"}, status=400)

        Vote.objects.create(user=user, question=question, choice=choice)
        choice.votes += 1
        choice.save()

        return Response({"message": "Vote cast successfully"}, status=201)


class UserVotedQuestionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        voted_questions = Question.objects.filter(vote__user=request.user).distinct()
        serializer = QuestionSerializer(voted_questions, many=True)
        return Response(serializer.data)
