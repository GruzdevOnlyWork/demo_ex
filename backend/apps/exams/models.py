from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Question(models.Model):
    QUESTION_TYPES = [
        ('single', 'Один ответ'),
        ('multiple', 'Несколько ответов'),
        ('text', 'Текстовый ответ'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions', verbose_name='Категория')
    text = models.TextField('Текст вопроса')
    question_type = models.CharField('Тип вопроса', max_length=20, choices=QUESTION_TYPES, default='single')
    points = models.PositiveIntegerField('Баллы', default=1)
    explanation = models.TextField('Пояснение к ответу', blank=True, help_text='Показывается после ответа')
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['category', 'id']

    def __str__(self):
        return f"{self.category.name}: {self.text[:50]}..."


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='Вопрос')
    text = models.CharField('Текст ответа', max_length=500)
    is_correct = models.BooleanField('Правильный', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['order']

    def __str__(self):
        return f"{self.text[:50]} ({'✓' if self.is_correct else '✗'})"


class Test(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    categories = models.ManyToManyField(Category, related_name='tests', verbose_name='Категории', blank=True)
    questions_count = models.PositiveIntegerField('Количество вопросов', default=20, help_text='Сколько вопросов выбрать из категорий')
    time_limit = models.PositiveIntegerField('Время (минуты)', default=60, help_text='0 = без ограничения')
    passing_score = models.PositiveIntegerField('Проходной балл (%)', default=70)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class TestAttempt(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
        ('timeout', 'Время вышло'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attempts', verbose_name='Пользователь')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='attempts', verbose_name='Тест')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='in_progress')
    score = models.PositiveIntegerField('Набрано баллов', default=0)
    max_score = models.PositiveIntegerField('Максимум баллов', default=0)
    started_at = models.DateTimeField('Начат', auto_now_add=True)
    finished_at = models.DateTimeField('Завершен', null=True, blank=True)

    class Meta:
        verbose_name = 'Попытка'
        verbose_name_plural = 'Попытки'
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.user.username} - {self.test.title} ({self.status})"

    @property
    def percentage(self):
        if self.max_score == 0:
            return 0
        return round(self.score / self.max_score * 100)

    @property
    def is_passed(self):
        return self.percentage >= self.test.passing_score


class UserAnswer(models.Model):
    attempt = models.ForeignKey(TestAttempt, on_delete=models.CASCADE, related_name='user_answers', verbose_name='Попытка')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    selected_answers = models.ManyToManyField(Answer, blank=True, verbose_name='Выбранные ответы')
    text_answer = models.TextField('Текстовый ответ', blank=True)
    is_correct = models.BooleanField('Правильно', default=False)
    points_earned = models.PositiveIntegerField('Получено баллов', default=0)

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'
        unique_together = ['attempt', 'question']

    def __str__(self):
        return f"Ответ на: {self.question.text[:30]}..."
