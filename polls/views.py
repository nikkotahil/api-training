from django.core.serializers import serialize
from rest_framework import generics, permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Question, Choice, Vote
from django.contrib.auth import authenticate
from .serializers import (
    QuestionSerializer, RegisterSerializer, VoteSerializer, UserVotedQuestionSerializer
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


class CreateQuestionView(CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        serializer.save()
        return Response({"message": "Question created successfully"}, status=201)


class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

class QuestionDetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]


class VoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = VoteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vote cast successfully"}, status=201)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVotedQuestionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserVotedQuestionSerializer

    def get_queryset(self):
        votes = Vote.objects.filter(user=self.request.user).values_list('question', flat=True)
        return Question.objects.filter(id__in=votes)
