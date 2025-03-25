from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Question, Choice, Vote, User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=6, error_messages={
        "min_length": "Password must be at least 6 characters long."
    })
    user_type = serializers.ChoiceField(choices=User.USER_TYPES, default='user')

    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "user_type"]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate_first_name(self, value):
        if len(value.strip()) < 1:
            raise serializers.ValidationError("First name cannot be empty.")
        return value

    def validate_last_name(self, value):
        if len(value.strip()) < 1:
            raise serializers.ValidationError("Last name cannot be empty.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken. Please choose another one.")
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=make_password(validated_data["password"]),
            user_type=validated_data["user_type"]
        )
        return user


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id", "choice_text", "votes"]

    def validate_choice_text(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Choice text cannot be empty.")
        return value


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date", "choices"]

    def get_choices(self, obj):
        return ChoiceSerializer(obj.choices.all(), many=True).data


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'
