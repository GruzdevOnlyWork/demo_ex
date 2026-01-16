from rest_framework import serializers
from .models import Category, Question, Answer, Test, TestAttempt, UserAnswer


class CategorySerializer(serializers.ModelSerializer):
    questions_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'questions_count']

    def get_questions_count(self, obj):
        return obj.questions.filter(is_active=True).count()


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'order']


class AnswerWithCorrectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'order', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'points', 'answers']


class QuestionResultSerializer(serializers.ModelSerializer):
    answers = AnswerWithCorrectSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'question_type', 'points', 'answers', 'explanation']


class TestListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'categories', 'questions_count', 'time_limit', 'passing_score']


class TestDetailSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'title', 'description', 'time_limit', 'questions']

    def get_questions(self, obj):
        attempt = self.context.get('attempt')
        if attempt:
            user_answers = attempt.user_answers.select_related('question').prefetch_related('question__answers')
            questions = [ua.question for ua in user_answers]
            return QuestionSerializer(questions, many=True).data
        return []


class UserAnswerSerializer(serializers.ModelSerializer):
    question = QuestionResultSerializer(read_only=True)
    selected_answers = AnswerWithCorrectSerializer(many=True, read_only=True)

    class Meta:
        model = UserAnswer
        fields = ['id', 'question', 'selected_answers', 'text_answer', 'is_correct', 'points_earned']


class SubmitAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    answer_ids = serializers.ListField(child=serializers.IntegerField(), required=False, default=[])
    text_answer = serializers.CharField(required=False, allow_blank=True, default='')


class TestAttemptSerializer(serializers.ModelSerializer):
    test = TestListSerializer(read_only=True)
    percentage = serializers.ReadOnlyField()
    is_passed = serializers.ReadOnlyField()

    class Meta:
        model = TestAttempt
        fields = ['id', 'test', 'status', 'score', 'max_score', 'percentage', 'is_passed', 'started_at', 'finished_at']


class TestAttemptDetailSerializer(serializers.ModelSerializer):
    test = TestListSerializer(read_only=True)
    user_answers = UserAnswerSerializer(many=True, read_only=True)
    percentage = serializers.ReadOnlyField()
    is_passed = serializers.ReadOnlyField()

    class Meta:
        model = TestAttempt
        fields = ['id', 'test', 'status', 'score', 'max_score', 'percentage', 'is_passed', 'started_at', 'finished_at', 'user_answers']
