from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Question, Choice, Vote


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "username", "first_name", "last_name", "user_type", "is_staff", "is_active")
    list_filter = ("user_type", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name")
    ordering = ("id",)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question_text", "pub_date")
    search_fields = ("question_text",)
    list_filter = ("pub_date",)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "choice_text", "question", "votes")
    search_fields = ("choice_text",)
    list_filter = ("question",)


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "question", "choice")
    search_fields = ("user__username", "question__question_text")
    list_filter = ("question", "user")
