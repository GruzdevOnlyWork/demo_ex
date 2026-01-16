from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Prefetch
import random

from .models import Category, Test, TestAttempt, UserAnswer, Question, Answer
from .serializers import (
    CategorySerializer, TestListSerializer, TestDetailSerializer,
    TestAttemptSerializer, TestAttemptDetailSerializer,
    SubmitAnswerSerializer, QuestionSerializer
)


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class TestListView(generics.ListAPIView):
    queryset = Test.objects.filter(is_active=True).prefetch_related('categories')
    serializer_class = TestListSerializer
    permission_classes = [permissions.IsAuthenticated]


class StartTestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, test_id):
        try:
            test = Test.objects.get(id=test_id, is_active=True)
        except Test.DoesNotExist:
            return Response({'error': 'Тест не найден'}, status=status.HTTP_404_NOT_FOUND)

        existing_attempt = TestAttempt.objects.filter(
            user=request.user, test=test, status='in_progress'
        ).first()

        if existing_attempt:
            return Response({
                'attempt_id': existing_attempt.id,
                'message': 'У вас есть незавершенная попытка'
            })

        categories = test.categories.all()
        if categories.exists():
            questions = Question.objects.filter(
                category__in=categories, is_active=True
            ).prefetch_related('answers')
        else:
            questions = Question.objects.filter(is_active=True).prefetch_related('answers')

        questions = list(questions)
        random.shuffle(questions)
        selected_questions = questions[:test.questions_count]

        if not selected_questions:
            return Response({'error': 'Нет доступных вопросов'}, status=status.HTTP_400_BAD_REQUEST)

        max_score = sum(q.points for q in selected_questions)
        attempt = TestAttempt.objects.create(
            user=request.user,
            test=test,
            max_score=max_score
        )

        for question in selected_questions:
            UserAnswer.objects.create(attempt=attempt, question=question)

        return Response({
            'attempt_id': attempt.id,
            'questions_count': len(selected_questions),
            'time_limit': test.time_limit,
            'message': 'Тест начат'
        }, status=status.HTTP_201_CREATED)


class AttemptQuestionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, attempt_id):
        try:
            attempt = TestAttempt.objects.select_related('test').get(
                id=attempt_id, user=request.user
            )
        except TestAttempt.DoesNotExist:
            return Response({'error': 'Попытка не найдена'}, status=status.HTTP_404_NOT_FOUND)

        if attempt.status != 'in_progress':
            return Response({'error': 'Тест уже завершен'}, status=status.HTTP_400_BAD_REQUEST)

        if attempt.test.time_limit > 0:
            elapsed = (timezone.now() - attempt.started_at).total_seconds() / 60
            if elapsed > attempt.test.time_limit:
                attempt.status = 'timeout'
                attempt.finished_at = timezone.now()
                attempt.save()
                return Response({'error': 'Время вышло'}, status=status.HTTP_400_BAD_REQUEST)

        user_answers = attempt.user_answers.select_related('question').prefetch_related(
            'question__answers', 'selected_answers'
        ).order_by('id')

        questions_data = []
        for ua in user_answers:
            q_data = QuestionSerializer(ua.question).data
            q_data['user_answer'] = {
                'selected_answer_ids': list(ua.selected_answers.values_list('id', flat=True)),
                'text_answer': ua.text_answer
            }
            questions_data.append(q_data)

        time_remaining = None
        if attempt.test.time_limit > 0:
            elapsed = (timezone.now() - attempt.started_at).total_seconds()
            time_remaining = max(0, attempt.test.time_limit * 60 - elapsed)

        return Response({
            'test_title': attempt.test.title,
            'questions': questions_data,
            'time_remaining': time_remaining
        })


class SubmitAnswerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, attempt_id):
        try:
            attempt = TestAttempt.objects.get(
                id=attempt_id, user=request.user, status='in_progress'
            )
        except TestAttempt.DoesNotExist:
            return Response({'error': 'Попытка не найдена или завершена'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubmitAnswerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question_id = serializer.validated_data['question_id']
        answer_ids = serializer.validated_data.get('answer_ids', [])
        text_answer = serializer.validated_data.get('text_answer', '')

        try:
            user_answer = UserAnswer.objects.get(attempt=attempt, question_id=question_id)
        except UserAnswer.DoesNotExist:
            return Response({'error': 'Вопрос не найден в этом тесте'}, status=status.HTTP_404_NOT_FOUND)

        user_answer.text_answer = text_answer
        user_answer.selected_answers.set(answer_ids)
        user_answer.save()

        return Response({'status': 'ok'})


class FinishTestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, attempt_id):
        try:
            attempt = TestAttempt.objects.get(
                id=attempt_id, user=request.user, status='in_progress'
            )
        except TestAttempt.DoesNotExist:
            return Response({'error': 'Попытка не найдена или уже завершена'}, status=status.HTTP_404_NOT_FOUND)

        total_score = 0
        user_answers = attempt.user_answers.select_related('question').prefetch_related(
            'question__answers', 'selected_answers'
        )

        for ua in user_answers:
            question = ua.question
            is_correct = False
            points = 0

            if question.question_type in ['single', 'multiple']:
                correct_ids = set(question.answers.filter(is_correct=True).values_list('id', flat=True))
                selected_ids = set(ua.selected_answers.values_list('id', flat=True))
                is_correct = correct_ids == selected_ids
            elif question.question_type == 'text':
                correct_answer = question.answers.filter(is_correct=True).first()
                if correct_answer:
                    is_correct = ua.text_answer.strip().lower() == correct_answer.text.strip().lower()

            if is_correct:
                points = question.points
                total_score += points

            ua.is_correct = is_correct
            ua.points_earned = points
            ua.save()

        attempt.score = total_score
        attempt.status = 'completed'
        attempt.finished_at = timezone.now()
        attempt.save()

        return Response({
            'score': attempt.score,
            'max_score': attempt.max_score,
            'percentage': attempt.percentage,
            'is_passed': attempt.is_passed,
            'passing_score': attempt.test.passing_score
        })


class AttemptResultView(generics.RetrieveAPIView):
    serializer_class = TestAttemptDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TestAttempt.objects.filter(user=self.request.user).select_related('test').prefetch_related(
            'user_answers__question__answers',
            'user_answers__selected_answers'
        )


class MyAttemptsView(generics.ListAPIView):
    serializer_class = TestAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TestAttempt.objects.filter(user=self.request.user).select_related('test')
