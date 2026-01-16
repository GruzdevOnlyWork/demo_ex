from django.urls import path
from .views import (
    CategoryListView, TestListView, StartTestView,
    AttemptQuestionsView, SubmitAnswerView, FinishTestView,
    AttemptResultView, MyAttemptsView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('tests/', TestListView.as_view(), name='test-list'),
    path('tests/<int:test_id>/start/', StartTestView.as_view(), name='start-test'),
    path('attempts/', MyAttemptsView.as_view(), name='my-attempts'),
    path('attempts/<int:attempt_id>/questions/', AttemptQuestionsView.as_view(), name='attempt-questions'),
    path('attempts/<int:attempt_id>/submit/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('attempts/<int:attempt_id>/finish/', FinishTestView.as_view(), name='finish-test'),
    path('attempts/<int:pk>/result/', AttemptResultView.as_view(), name='attempt-result'),
]
