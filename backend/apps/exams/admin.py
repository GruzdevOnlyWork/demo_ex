from django.contrib import admin
from .models import Category, Question, Answer, Test, TestAttempt, UserAnswer


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    min_num = 2


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'questions_count']
    list_editable = ['order']
    search_fields = ['name']

    def questions_count(self, obj):
        return obj.questions.count()
    questions_count.short_description = 'Вопросов'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['short_text', 'category', 'question_type', 'points', 'is_active']
    list_filter = ['category', 'question_type', 'is_active']
    search_fields = ['text']
    inlines = [AnswerInline]

    def short_text(self, obj):
        return obj.text[:80] + '...' if len(obj.text) > 80 else obj.text
    short_text.short_description = 'Текст вопроса'


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title', 'questions_count', 'time_limit', 'passing_score', 'is_active']
    list_filter = ['is_active', 'categories']
    search_fields = ['title']
    filter_horizontal = ['categories']


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'status', 'score', 'max_score', 'percentage_display', 'started_at']
    list_filter = ['status', 'test']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['user', 'test', 'score', 'max_score', 'started_at', 'finished_at']

    def percentage_display(self, obj):
        return f"{obj.percentage}%"
    percentage_display.short_description = 'Процент'


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct', 'points_earned']
    list_filter = ['is_correct']
