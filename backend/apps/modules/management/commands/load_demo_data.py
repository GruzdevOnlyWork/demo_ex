from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.exams.models import Category, Question, Answer, Test
from apps.modules.models import (
    Section, Module, ModuleStep, StepNote, EvaluationCriteria
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Загрузка демо-данных для подготовки к экзамену КОД 1.2'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка данных...')

        # Создаем суперпользователя
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                first_name='Администратор'
            )
            self.stdout.write(self.style.SUCCESS('Создан суперпользователь: admin / admin123'))

        # Создаем тестового студента
        if not User.objects.filter(username='student').exists():
            User.objects.create_user(
                username='student',
                email='student@example.com',
                password='student123',
                first_name='Иван',
                last_name='Петров',
                group='ИС-21'
            )
            self.stdout.write(self.style.SUCCESS('Создан студент: student / student123'))

        # ============== РАЗДЕЛЫ И МОДУЛИ ==============
        self.stdout.write('Создание разделов и модулей...')

        # Раздел A: Проектирование
        section_a, _ = Section.objects.get_or_create(
            name='Модуль A: Проектирование программного обеспечения',
            defaults={
                'description': 'Анализ требований, проектирование архитектуры и базы данных',
                'order': 1
            }
        )

        # Модуль A1: Анализ требований
        module_a1, created = Module.objects.get_or_create(
            section=section_a,
            name='A1: Анализ требований и техническое задание',
            defaults={
                'description': 'Изучение методов сбора и анализа требований, составление ТЗ',
                'instruction': '''В этом модуле вы научитесь:
- Анализировать бизнес-требования заказчика
- Выделять функциональные и нефункциональные требования
- Составлять техническое задание по ГОСТ
- Создавать диаграммы вариантов использования (Use Case)''',
                'duration': '3 часа',
                'max_score': 20,
                'order': 1
            }
        )

        if created:
            # Шаги модуля A1
            step1 = ModuleStep.objects.create(
                module=module_a1,
                number=1,
                title='Изучение предметной области',
                description='''Внимательно прочитайте описание предметной области из задания.
Выделите основных участников системы (актёров) и их цели.
Определите основные бизнес-процессы, которые должна автоматизировать система.''',
                expected_result='Список актёров и их целей, перечень бизнес-процессов',
                order=1
            )
            StepNote.objects.create(
                step=step1,
                note_type='tip',
                title='Совет',
                content='Используйте маркеры для выделения ключевых слов в тексте задания: существительные часто указывают на сущности данных, глаголы - на функции системы.',
                order=1
            )
            StepNote.objects.create(
                step=step1,
                note_type='important',
                title='Важно',
                content='Не пропускайте неявные требования! Если в задании говорится "система учёта заказов", подразумевается создание, редактирование, удаление и просмотр заказов.',
                order=2
            )

            step2 = ModuleStep.objects.create(
                module=module_a1,
                number=2,
                title='Составление списка требований',
                description='''Разделите требования на функциональные (что система должна делать) и нефункциональные (как система должна работать).

Функциональные требования:
- Авторизация пользователей
- CRUD операции для основных сущностей
- Формирование отчётов
- Поиск и фильтрация данных

Нефункциональные требования:
- Производительность
- Безопасность
- Удобство использования''',
                expected_result='Структурированный список функциональных и нефункциональных требований',
                order=2
            )
            StepNote.objects.create(
                step=step2,
                note_type='example',
                title='Пример функционального требования',
                content='FR-001: Система должна позволять администратору создавать учётные записи пользователей с указанием ФИО, логина, пароля и роли.',
                order=1
            )

            step3 = ModuleStep.objects.create(
                module=module_a1,
                number=3,
                title='Создание диаграммы Use Case',
                description='''Создайте диаграмму вариантов использования в нотации UML:

1. Определите актёров (пользователей системы)
2. Определите варианты использования (функции)
3. Установите связи между актёрами и функциями
4. Добавьте связи include и extend при необходимости''',
                expected_result='Диаграмма Use Case в формате PNG или встроенная в документ',
                order=3
            )
            StepNote.objects.create(
                step=step3,
                note_type='info',
                title='Инструменты',
                content='Рекомендуемые инструменты: draw.io, PlantUML, StarUML, Visual Paradigm. На экзамене обычно доступен draw.io.',
                order=1
            )
            StepNote.objects.create(
                step=step3,
                note_type='warning',
                title='Частая ошибка',
                content='Не путайте актёра "Система" с внешними системами. Актёр - это всегда внешняя сущность по отношению к разрабатываемой системе.',
                order=2
            )

            # Критерии оценивания A1
            EvaluationCriteria.objects.create(
                module=module_a1,
                name='Полнота анализа требований',
                description='Все требования из задания выявлены и классифицированы',
                max_score=5,
                order=1
            )
            EvaluationCriteria.objects.create(
                module=module_a1,
                name='Корректность диаграммы Use Case',
                description='Диаграмма соответствует нотации UML, все актёры и связи указаны верно',
                max_score=5,
                order=2
            )
            EvaluationCriteria.objects.create(
                module=module_a1,
                name='Оформление документации',
                description='Документ оформлен аккуратно, структурирован',
                max_score=5,
                order=3
            )
            EvaluationCriteria.objects.create(
                module=module_a1,
                name='Соответствие ГОСТ',
                description='ТЗ соответствует требованиям ГОСТ 19.201-78',
                max_score=5,
                order=4
            )

        # Модуль A2: Проектирование БД
        module_a2, created = Module.objects.get_or_create(
            section=section_a,
            name='A2: Проектирование базы данных',
            defaults={
                'description': 'Создание ER-диаграммы и нормализация базы данных',
                'instruction': '''В этом модуле вы научитесь:
- Выделять сущности и атрибуты из требований
- Определять связи между сущностями
- Создавать ER-диаграмму
- Проводить нормализацию до 3НФ''',
                'duration': '2 часа',
                'max_score': 25,
                'order': 2
            }
        )

        if created:
            step1 = ModuleStep.objects.create(
                module=module_a2,
                number=1,
                title='Выделение сущностей',
                description='''Проанализируйте требования и выделите основные сущности:

1. Найдите существительные в описании предметной области
2. Определите, какие из них являются самостоятельными сущностями
3. Для каждой сущности определите атрибуты
4. Выделите первичные ключи''',
                expected_result='Список сущностей с атрибутами и первичными ключами',
                order=1
            )
            StepNote.objects.create(
                step=step1,
                note_type='tip',
                content='Типичные сущности для бизнес-приложений: Пользователь, Роль, Заказ, Товар, Клиент, Сотрудник, Документ, Категория.',
                order=1
            )

            step2 = ModuleStep.objects.create(
                module=module_a2,
                number=2,
                title='Определение связей',
                description='''Установите связи между сущностями:

- Один-к-одному (1:1) - редко используется
- Один-ко-многим (1:N) - самый распространённый тип
- Многие-ко-многим (M:N) - требует промежуточной таблицы

Определите обязательность связей (может ли FK быть NULL).''',
                expected_result='Список связей с указанием типа и обязательности',
                order=2
            )
            StepNote.objects.create(
                step=step2,
                note_type='example',
                title='Пример связи M:N',
                content='Заказ содержит много Товаров, Товар может быть в разных Заказах. Создаём таблицу OrderItems (order_id, product_id, quantity, price).',
                order=1
            )

            step3 = ModuleStep.objects.create(
                module=module_a2,
                number=3,
                title='Создание ER-диаграммы',
                description='''Создайте ER-диаграмму в нотации "воронья лапка" (Crow's Foot):

1. Нарисуйте прямоугольники для каждой сущности
2. Укажите атрибуты внутри прямоугольников
3. Отметьте первичные ключи (PK) и внешние ключи (FK)
4. Соедините сущности линиями связей
5. Укажите кардинальность на концах линий''',
                expected_result='ER-диаграмма в графическом формате',
                order=3
            )
            StepNote.objects.create(
                step=step3,
                note_type='warning',
                title='Проверьте',
                content='Убедитесь, что все связи M:N разбиты на две связи 1:N через промежуточную таблицу.',
                order=1
            )

            # Критерии
            EvaluationCriteria.objects.create(module=module_a2, name='Корректность сущностей', description='Все необходимые сущности выделены, атрибуты определены верно', max_score=8, order=1)
            EvaluationCriteria.objects.create(module=module_a2, name='Корректность связей', description='Типы связей определены правильно, M:N декомпозированы', max_score=8, order=2)
            EvaluationCriteria.objects.create(module=module_a2, name='Нормализация', description='База данных приведена минимум к 3НФ', max_score=5, order=3)
            EvaluationCriteria.objects.create(module=module_a2, name='Оформление диаграммы', description='Диаграмма читаема, использована правильная нотация', max_score=4, order=4)

        # Раздел B: Разработка
        section_b, _ = Section.objects.get_or_create(
            name='Модуль B: Разработка программного обеспечения',
            defaults={
                'description': 'Реализация серверной и клиентской части приложения',
                'order': 2
            }
        )

        # Модуль B1: Backend разработка
        module_b1, created = Module.objects.get_or_create(
            section=section_b,
            name='B1: Разработка серверной части (Backend)',
            defaults={
                'description': 'Создание REST API, работа с базой данных, аутентификация',
                'instruction': '''В этом модуле вы реализуете:
- Структуру проекта на выбранном фреймворке
- Модели данных и миграции
- REST API endpoints
- Аутентификацию и авторизацию
- Валидацию данных''',
                'duration': '4 часа',
                'max_score': 35,
                'order': 1
            }
        )

        if created:
            step1 = ModuleStep.objects.create(
                module=module_b1,
                number=1,
                title='Инициализация проекта',
                description='''Создайте структуру проекта:

Django:
```
django-admin startproject config .
python manage.py startapp api
```

Или другой фреймворк по заданию (FastAPI, Flask, Express).

Настройте подключение к базе данных в settings.py''',
                expected_result='Рабочий проект с настроенным подключением к БД',
                order=1
            )
            StepNote.objects.create(
                step=step1,
                note_type='important',
                content='На экзамене база данных уже создана. Проверьте параметры подключения в задании!',
                order=1
            )

            step2 = ModuleStep.objects.create(
                module=module_b1,
                number=2,
                title='Создание моделей данных',
                description='''Создайте модели на основе ER-диаграммы:

```python
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
```

Выполните миграции:
```
python manage.py makemigrations
python manage.py migrate
```''',
                expected_result='Созданные модели, применённые миграции',
                order=2
            )

            step3 = ModuleStep.objects.create(
                module=module_b1,
                number=3,
                title='Реализация API endpoints',
                description='''Создайте REST API для CRUD операций:

- GET /api/items/ - список
- GET /api/items/{id}/ - детали
- POST /api/items/ - создание
- PUT /api/items/{id}/ - обновление
- DELETE /api/items/{id}/ - удаление

Используйте сериализаторы для валидации и преобразования данных.''',
                expected_result='Работающие API endpoints',
                order=3
            )
            StepNote.objects.create(
                step=step3,
                note_type='tip',
                content='Django REST Framework: используйте ModelSerializer и ModelViewSet для быстрой реализации CRUD.',
                order=1
            )

            step4 = ModuleStep.objects.create(
                module=module_b1,
                number=4,
                title='Аутентификация',
                description='''Реализуйте систему аутентификации:

Для JWT:
```python
from rest_framework_simplejwt.views import TokenObtainPairView
path('api/token/', TokenObtainPairView.as_view())
```

Защитите endpoints с помощью permissions.''',
                expected_result='Работающая аутентификация, защищённые endpoints',
                order=4
            )

            # Критерии
            EvaluationCriteria.objects.create(module=module_b1, name='Структура проекта', description='Проект организован логично, код разделён по модулям', max_score=5, order=1)
            EvaluationCriteria.objects.create(module=module_b1, name='Модели данных', description='Модели соответствуют ER-диаграмме, связи настроены', max_score=8, order=2)
            EvaluationCriteria.objects.create(module=module_b1, name='API endpoints', description='Все необходимые endpoints реализованы и работают', max_score=12, order=3)
            EvaluationCriteria.objects.create(module=module_b1, name='Аутентификация', description='Реализована безопасная аутентификация', max_score=5, order=4)
            EvaluationCriteria.objects.create(module=module_b1, name='Качество кода', description='Код читаем, следует стандартам', max_score=5, order=5)

        # Модуль B2: Frontend
        module_b2, created = Module.objects.get_or_create(
            section=section_b,
            name='B2: Разработка клиентской части (Frontend)',
            defaults={
                'description': 'Создание пользовательского интерфейса, работа с API',
                'instruction': '''В этом модуле вы реализуете:
- Структуру frontend приложения
- Компоненты пользовательского интерфейса
- Взаимодействие с REST API
- Формы и валидацию
- Маршрутизацию''',
                'duration': '4 часа',
                'max_score': 30,
                'order': 2
            }
        )

        if created:
            step1 = ModuleStep.objects.create(
                module=module_b2,
                number=1,
                title='Создание проекта',
                description='''Инициализируйте frontend проект:

Vue.js:
```
npm create vite@latest frontend -- --template vue
cd frontend && npm install
npm install axios vue-router pinia
```

Настройте proxy для API в vite.config.js''',
                expected_result='Рабочий frontend проект',
                order=1
            )

            step2 = ModuleStep.objects.create(
                module=module_b2,
                number=2,
                title='Создание компонентов',
                description='''Создайте базовые компоненты:

- Layout (шапка, меню, футер)
- Формы ввода данных
- Таблицы для отображения списков
- Карточки для детального просмотра
- Модальные окна

Используйте CSS-фреймворк или собственные стили.''',
                expected_result='Набор переиспользуемых компонентов',
                order=2
            )

            step3 = ModuleStep.objects.create(
                module=module_b2,
                number=3,
                title='Интеграция с API',
                description='''Настройте взаимодействие с backend:

```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: '/api'
})

// Добавьте interceptor для токена
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```''',
                expected_result='Работающее взаимодействие frontend и backend',
                order=3
            )
            StepNote.objects.create(
                step=step3,
                note_type='warning',
                content='Не забудьте обработать ошибки API (401, 403, 404, 500) и показать пользователю понятные сообщения.',
                order=1
            )

            # Критерии
            EvaluationCriteria.objects.create(module=module_b2, name='Структура приложения', description='Код организован по компонентам, используется роутинг', max_score=5, order=1)
            EvaluationCriteria.objects.create(module=module_b2, name='Пользовательский интерфейс', description='UI удобен, адаптивен, соответствует макету', max_score=10, order=2)
            EvaluationCriteria.objects.create(module=module_b2, name='Работа с API', description='Данные корректно загружаются и отправляются', max_score=10, order=3)
            EvaluationCriteria.objects.create(module=module_b2, name='Валидация форм', description='Формы валидируются, ошибки отображаются', max_score=5, order=4)

        # ============== КАТЕГОРИИ И ВОПРОСЫ ДЛЯ ТЕСТОВ ==============
        self.stdout.write('Создание категорий и вопросов...')

        # Категория: SQL
        cat_sql, _ = Category.objects.get_or_create(
            name='SQL и базы данных',
            defaults={'description': 'Вопросы по SQL, проектированию БД', 'order': 1}
        )

        # Вопросы SQL
        q1, created = Question.objects.get_or_create(
            category=cat_sql,
            text='Какой SQL-оператор используется для выборки данных из таблицы?',
            defaults={'question_type': 'single', 'points': 1}
        )
        if created:
            Answer.objects.create(question=q1, text='SELECT', is_correct=True, order=1)
            Answer.objects.create(question=q1, text='GET', is_correct=False, order=2)
            Answer.objects.create(question=q1, text='FETCH', is_correct=False, order=3)
            Answer.objects.create(question=q1, text='RETRIEVE', is_correct=False, order=4)

        q2, created = Question.objects.get_or_create(
            category=cat_sql,
            text='Какой тип связи требует создания промежуточной таблицы?',
            defaults={'question_type': 'single', 'points': 1}
        )
        if created:
            Answer.objects.create(question=q2, text='Один-к-одному', is_correct=False, order=1)
            Answer.objects.create(question=q2, text='Один-ко-многим', is_correct=False, order=2)
            Answer.objects.create(question=q2, text='Многие-ко-многим', is_correct=True, order=3)

        q3, created = Question.objects.get_or_create(
            category=cat_sql,
            text='Выберите операторы, которые относятся к DDL (Data Definition Language):',
            defaults={'question_type': 'multiple', 'points': 2}
        )
        if created:
            Answer.objects.create(question=q3, text='CREATE', is_correct=True, order=1)
            Answer.objects.create(question=q3, text='SELECT', is_correct=False, order=2)
            Answer.objects.create(question=q3, text='ALTER', is_correct=True, order=3)
            Answer.objects.create(question=q3, text='INSERT', is_correct=False, order=4)
            Answer.objects.create(question=q3, text='DROP', is_correct=True, order=5)

        q4, created = Question.objects.get_or_create(
            category=cat_sql,
            text='Что означает аббревиатура CRUD?',
            defaults={'question_type': 'single', 'points': 1}
        )
        if created:
            Answer.objects.create(question=q4, text='Create, Read, Update, Delete', is_correct=True, order=1)
            Answer.objects.create(question=q4, text='Copy, Rename, Undo, Delete', is_correct=False, order=2)
            Answer.objects.create(question=q4, text='Connect, Request, Upload, Download', is_correct=False, order=3)

        q5, created = Question.objects.get_or_create(
            category=cat_sql,
            text='Какая нормальная форма требует, чтобы все неключевые атрибуты зависели только от первичного ключа?',
            defaults={'question_type': 'single', 'points': 2}
        )
        if created:
            Answer.objects.create(question=q5, text='1НФ', is_correct=False, order=1)
            Answer.objects.create(question=q5, text='2НФ', is_correct=True, order=2)
            Answer.objects.create(question=q5, text='3НФ', is_correct=False, order=3)
            Answer.objects.create(question=q5, text='НФБК', is_correct=False, order=4)

        # Категория: Python/Django
        cat_python, _ = Category.objects.get_or_create(
            name='Python и Django',
            defaults={'description': 'Вопросы по Python, Django, DRF', 'order': 2}
        )

        q6, created = Question.objects.get_or_create(
            category=cat_python,
            text='Какой декоратор Django REST Framework делает view доступным без аутентификации?',
            defaults={'question_type': 'single', 'points': 1}
        )
        if created:
            Answer.objects.create(question=q6, text='@api_view', is_correct=False, order=1)
            Answer.objects.create(question=q6, text='@permission_classes([AllowAny])', is_correct=True, order=2)
            Answer.objects.create(question=q6, text='@public', is_correct=False, order=3)
            Answer.objects.create(question=q6, text='@no_auth', is_correct=False, order=4)

        q7, created = Question.objects.get_or_create(
            category=cat_python,
            text='Какой HTTP метод используется для создания нового ресурса в REST API?',
            defaults={'question_type': 'single', 'points': 1}
        )
        if created:
            Answer.objects.create(question=q7, text='GET', is_correct=False, order=1)
            Answer.objects.create(question=q7, text='POST', is_correct=True, order=2)
            Answer.objects.create(question=q7, text='PUT', is_correct=False, order=3)
            Answer.objects.create(question=q7, text='PATCH', is_correct=False, order=4)

        q8, created = Question.objects.get_or_create(
            category=cat_python,
            text='Какой класс Django используется для определения структуры таблицы в базе данных?',
            defaults={'question_type': 'single', 'points': 1}
        )
        if created:
            Answer.objects.create(question=q8, text='models.Model', is_correct=True, order=1)
            Answer.objects.create(question=q8, text='forms.Form', is_correct=False, order=2)
            Answer.objects.create(question=q8, text='views.View', is_correct=False, order=3)
            Answer.objects.create(question=q8, text='serializers.Serializer', is_correct=False, order=4)

        q9, created = Question.objects.get_or_create(
            category=cat_python,
            text='Выберите правильные утверждения о Django ORM:',
            defaults={'question_type': 'multiple', 'points': 2}
        )
        if created:
            Answer.objects.create(question=q9, text='ORM позволяет работать с БД без написания SQL', is_correct=True, order=1)
            Answer.objects.create(question=q9, text='filter() возвращает один объект', is_correct=False, order=2)
            Answer.objects.create(question=q9, text='get() вызывает исключение если объект не найден', is_correct=True, order=3)
            Answer.objects.create(question=q9, text='all() сразу загружает все данные в память', is_correct=False, order=4)

        # Категория: JavaScript/Vue
        cat_js, _ = Category.objects.get_or_create(
            name='JavaScript и Vue.js',
            defaults={'description': 'Вопросы по JS, Vue.js, frontend', 'order': 3}
        )

        q10, created = Question.objects.get_or_create(
            category=cat_js,
            text='Какой хук жизненного цикла Vue 3 вызывается после монтирования компонента?',
            defaults={'question_type': 'single', 'points': 1}
        )
        if created:
            Answer.objects.create(question=q10, text='onBeforeMount', is_correct=False, order=1)
            Answer.objects.create(question=q10, text='onMounted', is_correct=True, order=2)
            Answer.objects.create(question=q10, text='onCreated', is_correct=False, order=3)
            Answer.objects.create(question=q10, text='onReady', is_correct=False, order=4)

        q11, created = Question.objects.get_or_create(
            category=cat_js,
            text='Какая функция Vue 3 Composition API используется для создания реактивной переменной?',
            defaults={'question_type': 'single', 'points': 1}
        )
        if created:
            Answer.objects.create(question=q11, text='reactive()', is_correct=False, order=1)
            Answer.objects.create(question=q11, text='ref()', is_correct=True, order=2)
            Answer.objects.create(question=q11, text='data()', is_correct=False, order=3)
            Answer.objects.create(question=q11, text='state()', is_correct=False, order=4)

        q12, created = Question.objects.get_or_create(
            category=cat_js,
            text='Какой метод axios используется для отправки POST-запроса?',
            defaults={'question_type': 'single', 'points': 1}
        )
        if created:
            Answer.objects.create(question=q12, text='axios.get()', is_correct=False, order=1)
            Answer.objects.create(question=q12, text='axios.post()', is_correct=True, order=2)
            Answer.objects.create(question=q12, text='axios.send()', is_correct=False, order=3)
            Answer.objects.create(question=q12, text='axios.request()', is_correct=False, order=4)

        # Категория: UML
        cat_uml, _ = Category.objects.get_or_create(
            name='UML и проектирование',
            defaults={'description': 'Вопросы по UML-диаграммам', 'order': 4}
        )

        q13, created = Question.objects.get_or_create(
            category=cat_uml,
            text='Какая UML-диаграмма используется для описания функциональных требований к системе?',
            defaults={'question_type': 'single', 'points': 1}
        )
        if created:
            Answer.objects.create(question=q13, text='Диаграмма классов', is_correct=False, order=1)
            Answer.objects.create(question=q13, text='Диаграмма последовательности', is_correct=False, order=2)
            Answer.objects.create(question=q13, text='Диаграмма вариантов использования', is_correct=True, order=3)
            Answer.objects.create(question=q13, text='Диаграмма состояний', is_correct=False, order=4)

        q14, created = Question.objects.get_or_create(
            category=cat_uml,
            text='Что означает связь "include" на диаграмме Use Case?',
            defaults={'question_type': 'single', 'points': 2}
        )
        if created:
            Answer.objects.create(question=q14, text='Один вариант использования всегда включает другой', is_correct=True, order=1)
            Answer.objects.create(question=q14, text='Один вариант может опционально расширить другой', is_correct=False, order=2)
            Answer.objects.create(question=q14, text='Два варианта использования исключают друг друга', is_correct=False, order=3)

        # ============== ТЕСТЫ ==============
        self.stdout.write('Создание тестов...')

        test1, _ = Test.objects.get_or_create(
            title='Тест: SQL и базы данных',
            defaults={
                'description': 'Проверка знаний по SQL, проектированию и нормализации БД',
                'questions_count': 5,
                'time_limit': 15,
                'passing_score': 60
            }
        )
        test1.categories.add(cat_sql)

        test2, _ = Test.objects.get_or_create(
            title='Тест: Backend разработка',
            defaults={
                'description': 'Вопросы по Python, Django, REST API',
                'questions_count': 5,
                'time_limit': 15,
                'passing_score': 60
            }
        )
        test2.categories.add(cat_python)

        test3, _ = Test.objects.get_or_create(
            title='Тест: Frontend разработка',
            defaults={
                'description': 'Вопросы по JavaScript, Vue.js',
                'questions_count': 5,
                'time_limit': 15,
                'passing_score': 60
            }
        )
        test3.categories.add(cat_js)

        test_full, _ = Test.objects.get_or_create(
            title='Комплексный тест: КОД 1.2',
            defaults={
                'description': 'Полный тест по всем темам демо-экзамена "Программные решения для бизнеса"',
                'questions_count': 15,
                'time_limit': 30,
                'passing_score': 70
            }
        )
        test_full.categories.add(cat_sql, cat_python, cat_js, cat_uml)

        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write('')
        self.stdout.write('Учётные записи:')
        self.stdout.write('  Админ: admin / admin123')
        self.stdout.write('  Студент: student / student123')
        self.stdout.write('')
        self.stdout.write(f'Создано разделов: {Section.objects.count()}')
        self.stdout.write(f'Создано модулей: {Module.objects.count()}')
        self.stdout.write(f'Создано категорий: {Category.objects.count()}')
        self.stdout.write(f'Создано вопросов: {Question.objects.count()}')
        self.stdout.write(f'Создано тестов: {Test.objects.count()}')
