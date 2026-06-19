from django.core.management.base import BaseCommand
from django.core.files import File
from apps.modules.models import (
    ExamVariant, Section, Module, ModuleStep,
    StepNote, ModuleFile, EvaluationCriteria, UsefulLink
)
import os


class Command(BaseCommand):
    help = 'Загрузка варианта демо-экзамена КОД 1.2 Вариант 7'

    def add_arguments(self, parser):
        parser.add_argument(
            '--resources-path',
            type=str,
            default='',
            help='Путь к папке с ресурсами экзамена'
        )

    def handle(self, *args, **options):
        resources_path = options['resources_path']

        self.stdout.write('Создание варианта экзамена КОД 1.2 Вариант 7...')

        variant, created = ExamVariant.objects.update_or_create(
            code='КОД 1.2',
            variant_number=7,
            defaults={
                'name': 'Система управления конференциями',
                'description': '''Предметная область: Система для организаторов конференций по информационной безопасности.

Система предназначена для различных типов пользователей:
1. Внешние пользователи (не зарегистрированы в системе)
2. Участники - просматривают и изменяют профиль, работают в группах
3. Модераторы - координируют участников в рамках активностей
4. Организаторы - управляют участниками, мероприятиями, добавляют активности
5. Жюри - просматривают информацию об активностях и оценивают участников

Основные сущности: Мероприятие, Активность, Участник, Модератор, Организатор, Жюри, Страна, Город.''',
                'total_time': '6 часов 30 минут',
                'order': 1
            }
        )

        if resources_path:
            self._load_pdf_files(variant, resources_path)

        session1, _ = Section.objects.update_or_create(
            exam_variant=variant,
            session_number=1,
            defaults={
                'name': 'Сессия 1: Проектирование и разработка',
                'description': 'Диаграммы, база данных, desktop-приложение, документация',
                'order': 1
            }
        )

        self._create_task_1(session1)
        self._create_task_2(session1)
        self._create_task_3(session1)
        self._create_task_4(session1, resources_path)
        self._create_task_5(session1, resources_path)
        self._create_task_6(session1)
        self._create_task_7(session1)

        self.stdout.write(self.style.SUCCESS(
            f'Вариант экзамена "{variant}" успешно {"создан" if created else "обновлен"}!'
        ))

    def _load_pdf_files(self, variant, resources_path):
        base_path = os.path.join(resources_path, 'Вариант 7')

        desc_pdf = os.path.join(base_path, 'Описание предметной области.pdf')
        if os.path.exists(desc_pdf):
            with open(desc_pdf, 'rb') as f:
                variant.description_file.save('opisanie_variant7.pdf', File(f), save=True)
            self.stdout.write(f'  Загружен: {desc_pdf}')

        task_pdf = os.path.join(base_path, 'Сессия 1.pdf')
        if os.path.exists(task_pdf):
            with open(task_pdf, 'rb') as f:
                variant.task_file.save('session1_variant7.pdf', File(f), save=True)
            self.stdout.write(f'  Загружен: {task_pdf}')

    def _create_task_1(self, session):
        task, created = Module.objects.update_or_create(
            section=session,
            task_number='1',
            defaults={
                'name': 'Диаграмма прецедентов (Use Case)',
                'description': 'Создание UML диаграммы вариантов использования для системы конференций',
                'task_condition': '''Для согласования процесса разработки с заказчиком Вам необходимо ознакомиться с описанием предметной области и сделать диаграмму прецедентов (Use Case) для основных пользователей системы.

Сохраните файл с диаграммой в форматах .vsdx и .pdf.''',
                'instruction': 'Используйте draw.io, Visio или аналогичный инструмент для создания диаграммы.',
                'duration': '30 минут',
                'max_score': 5,
                'order': 1
            }
        )

        if created:
            self._create_task_1_steps(task)
            self._create_task_1_criteria(task)

    def _create_task_1_steps(self, task):
        step1 = ModuleStep.objects.create(
            module=task, number=1, order=1,
            title='Анализ актёров системы',
            description='''Изучите описание предметной области и определите всех пользователей системы:

1. **Внешний пользователь** - не зарегистрирован, может просматривать мероприятия
2. **Участник** - зарегистрирован, участвует в мероприятиях
3. **Модератор** - координирует участников
4. **Организатор** - управляет мероприятиями и пользователями
5. **Жюри** - оценивает участников''',
            expected_result='Список из 5 актёров системы'
        )
        StepNote.objects.create(
            step=step1, note_type='tip', order=1,
            title='Определение актёра',
            content='Актёр в UML - это внешняя сущность (человек или система), взаимодействующая с системой. Один человек может выступать в разных ролях.'
        )

        step2 = ModuleStep.objects.create(
            module=task, number=2, order=2,
            title='Определение прецедентов для каждого актёра',
            description='''Для каждого актёра определите его действия (прецеденты):

**Внешний пользователь:**
- Просмотр мероприятий
- Фильтрация по направлению/дате
- Переход к авторизации

**Участник:**
- Авторизация
- Просмотр/редактирование профиля
- Регистрация на мероприятие
- Работа в группе

**Модератор:**
- Авторизация
- Регистрация на мероприятие
- Выбор активности для модерации
- Координация участников

**Организатор:**
- Авторизация
- Создание мероприятий
- Управление участниками
- Регистрация жюри/модераторов
- Просмотр отчётов

**Жюри:**
- Авторизация
- Просмотр активностей
- Оценка участников''',
            expected_result='Полный список прецедентов для каждого актёра'
        )

        step3 = ModuleStep.objects.create(
            module=task, number=3, order=3,
            title='Создание диаграммы',
            description='''Откройте draw.io (diagrams.net) или Microsoft Visio:

1. Создайте новый файл
2. Нарисуйте прямоугольник - границу системы (System Boundary)
3. Разместите актёров (человечки) слева от границы
4. Внутри границы разместите прецеденты (эллипсы)
5. Соедините актёров с их прецедентами линиями (Association)
6. Добавьте связи между прецедентами:
   - **<<include>>** - обязательное включение (например, все действия include Авторизация)
   - **<<extend>>** - опциональное расширение

7. Подпишите все элементы''',
            expected_result='Готовая диаграмма Use Case'
        )
        StepNote.objects.create(
            step=step3, note_type='warning', order=1,
            title='Частая ошибка',
            content='Стрелка <<include>> направлена ОТ основного прецедента К включаемому. Стрелка <<extend>> направлена ОТ расширяющего К основному.'
        )
        StepNote.objects.create(
            step=step3, note_type='example', order=2,
            title='Пример include',
            content='"Регистрация на мероприятие" --<<include>>--> "Авторизация" (авторизация всегда требуется)'
        )

        ModuleStep.objects.create(
            module=task, number=4, order=4,
            title='Экспорт диаграммы',
            description='''Сохраните диаграмму в двух форматах:

1. **Для draw.io:**
   - Файл → Экспортировать как → PDF
   - Файл → Сохранить как → .drawio (или File → Export as → VSDX)

2. **Для Visio:**
   - Файл → Сохранить как → .vsdx
   - Файл → Экспорт → PDF

Имена файлов: UseCase_Diagram.vsdx и UseCase_Diagram.pdf''',
            expected_result='Два файла: UseCase_Diagram.vsdx и UseCase_Diagram.pdf'
        )

    def _create_task_1_criteria(self, task):
        EvaluationCriteria.objects.create(
            module=task, order=1, max_score=1,
            name='Полнота актёров',
            description='Все 5 типов пользователей определены как актёры'
        )
        EvaluationCriteria.objects.create(
            module=task, order=2, max_score=2,
            name='Полнота прецедентов',
            description='Основные функции системы отражены для каждого актёра'
        )
        EvaluationCriteria.objects.create(
            module=task, order=3, max_score=1,
            name='Связи между прецедентами',
            description='Корректно использованы include и extend'
        )
        EvaluationCriteria.objects.create(
            module=task, order=4, max_score=1,
            name='Нотация UML',
            description='Диаграмма соответствует стандарту UML'
        )

    def _create_task_2(self, session):
        task, created = Module.objects.update_or_create(
            section=session,
            task_number='2',
            defaults={
                'name': 'Проектирование базы данных (ERD)',
                'description': 'Создание ER-диаграммы в 3 нормальной форме',
                'task_condition': '''На основе задания демонстрационного экзамена Вам необходимо спроектировать ER-диаграмму для информационной системы.

Требования:
- Обязательна 3 нормальная форма с обеспечением ссылочной целостности
- Согласованная осмысленная схема именования
- Создайте необходимые первичные и внешние ключи
- Определите ограничения внешних ключей

ER-диаграмма должна быть представлена в формате .pdf и .vsdx и содержать таблицы, связи между ними, атрибуты и ключи.''',
                'instruction': 'Используйте draw.io, Visio, или специализированный инструмент для ERD.',
                'duration': '45 минут',
                'max_score': 10,
                'order': 2
            }
        )

        if created:
            self._create_task_2_steps(task)
            self._create_task_2_criteria(task)

    def _create_task_2_steps(self, task):
        step1 = ModuleStep.objects.create(
            module=task, number=1, order=1,
            title='Определение сущностей',
            description='''Из описания предметной области выделите основные сущности:

1. **User** (Пользователь) - базовая таблица для всех типов пользователей
2. **Role** (Роль) - роли пользователей (Участник, Модератор, Организатор, Жюри)
3. **Country** (Страна)
4. **City** (Город) - связан со страной
5. **Event** (Мероприятие/Конференция)
6. **Activity** (Активность) - активности в рамках мероприятия
7. **Direction** (Направление) - направления мероприятий
8. **EventRegistration** (Регистрация на мероприятие) - связь User и Event''',
            expected_result='Список из 8+ сущностей'
        )
        StepNote.objects.create(
            step=step1, note_type='tip', order=1,
            title='3 нормальная форма',
            content='Каждый неключевой атрибут должен зависеть только от первичного ключа, а не от других неключевых атрибутов.'
        )

        step2 = ModuleStep.objects.create(
            module=task, number=2, order=2,
            title='Определение атрибутов',
            description='''Для каждой сущности определите атрибуты:

**User:**
- id (PK), id_number, first_name, last_name, patronymic
- gender, email, phone, photo, password
- role_id (FK), city_id (FK), direction_id (FK)

**Event:**
- id (PK), name, description, logo
- date_start, date_end, direction_id (FK)

**Activity:**
- id (PK), name, description
- event_id (FK), moderator_id (FK)

**City:**
- id (PK), name, country_id (FK)

И так далее для остальных сущностей...''',
            expected_result='Полный список атрибутов для каждой сущности'
        )

        step3 = ModuleStep.objects.create(
            module=task, number=3, order=3,
            title='Определение связей',
            description='''Установите связи между сущностями:

- **Country** 1:N **City** (в стране много городов)
- **City** 1:N **User** (в городе много пользователей)
- **Role** 1:N **User** (одна роль у многих пользователей)
- **Direction** 1:N **Event** (направление для мероприятий)
- **Event** 1:N **Activity** (в мероприятии много активностей)
- **User** N:M **Event** (через EventRegistration)
- **User** 1:N **Activity** (модератор активности)

Определите действия при удалении (ON DELETE):
- CASCADE - удалять связанные записи
- SET NULL - устанавливать NULL
- RESTRICT - запрещать удаление''',
            expected_result='Схема связей между сущностями'
        )
        StepNote.objects.create(
            step=step3, note_type='warning', order=1,
            title='Ссылочная целостность',
            content='Внешние ключи должны ссылаться на существующие записи. Определите правила ON DELETE и ON UPDATE.'
        )

        ModuleStep.objects.create(
            module=task, number=4, order=4,
            title='Создание и экспорт диаграммы',
            description='''Создайте ER-диаграмму в выбранном инструменте:

1. Нарисуйте прямоугольники для каждой таблицы
2. Укажите название таблицы в заголовке
3. Перечислите атрибуты с указанием:
   - PK (Primary Key) - первичный ключ
   - FK (Foreign Key) - внешний ключ
4. Соедините таблицы линиями связей
5. Укажите кардинальность (1:1, 1:N, N:M)

Экспортируйте в форматы .vsdx и .pdf''',
            expected_result='Файлы ERD.vsdx и ERD.pdf'
        )

    def _create_task_2_criteria(self, task):
        EvaluationCriteria.objects.create(
            module=task, order=1, max_score=3,
            name='Полнота сущностей',
            description='Все необходимые сущности определены'
        )
        EvaluationCriteria.objects.create(
            module=task, order=2, max_score=3,
            name='Нормализация',
            description='База данных в 3 нормальной форме'
        )
        EvaluationCriteria.objects.create(
            module=task, order=3, max_score=2,
            name='Связи и ключи',
            description='Корректно определены PK, FK и связи'
        )
        EvaluationCriteria.objects.create(
            module=task, order=4, max_score=2,
            name='Именование',
            description='Согласованная схема именования'
        )

    def _create_task_3(self, session):
        task, created = Module.objects.update_or_create(
            section=session,
            task_number='3',
            defaults={
                'name': 'Создание базы данных',
                'description': 'Создание БД и таблиц на сервере',
                'task_condition': '''Для работы приложения вам необходимо создать базу данных. Создайте базу данных, используя предпочтительную платформу, на сервере баз данных, который вам предоставлен.

Создайте таблицы основных сущностей, атрибуты, отношения и необходимые ограничения. В любом случае созданные таблицы должны содержать начальные тестовые данные.''',
                'instruction': 'Используйте SQL Server, MySQL, PostgreSQL или SQLite.',
                'duration': '45 минут',
                'max_score': 10,
                'order': 3
            }
        )

        if created:
            self._create_task_3_steps(task)
            self._create_task_3_criteria(task)

    def _create_task_3_steps(self, task):
        step1 = ModuleStep.objects.create(
            module=task, number=1, order=1,
            title='Создание базы данных',
            description='''Создайте новую базу данных:

**SQL Server:**
```sql
CREATE DATABASE ConferenceDB;
GO
USE ConferenceDB;
```

**MySQL:**
```sql
CREATE DATABASE conference_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE conference_db;
```

**PostgreSQL:**
```sql
CREATE DATABASE conference_db;
\\c conference_db
```''',
            expected_result='База данных создана'
        )

        step2 = ModuleStep.objects.create(
            module=task, number=2, order=2,
            title='Создание таблиц справочников',
            description='''Сначала создайте таблицы без внешних ключей:

```sql
-- Роли пользователей
CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Страны
CREATE TABLE countries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

-- Направления
CREATE TABLE directions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

-- Города (зависит от countries)
CREATE TABLE cities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    country_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);
```''',
            expected_result='Таблицы справочников созданы'
        )

        step3 = ModuleStep.objects.create(
            module=task, number=3, order=3,
            title='Создание основных таблиц',
            description='''Создайте таблицы с внешними ключами:

```sql
-- Пользователи
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_number VARCHAR(20) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    patronymic VARCHAR(100),
    gender ENUM('М', 'Ж') NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    photo VARCHAR(255),
    password VARCHAR(255) NOT NULL,
    role_id INT NOT NULL,
    city_id INT,
    direction_id INT,
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (city_id) REFERENCES cities(id),
    FOREIGN KEY (direction_id) REFERENCES directions(id)
);

-- Мероприятия
CREATE TABLE events (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    logo VARCHAR(255),
    date_start DATE,
    date_end DATE,
    direction_id INT,
    FOREIGN KEY (direction_id) REFERENCES directions(id)
);

-- Активности
CREATE TABLE activities (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    event_id INT NOT NULL,
    moderator_id INT,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (moderator_id) REFERENCES users(id) ON DELETE SET NULL
);
```''',
            expected_result='Основные таблицы созданы'
        )

        ModuleStep.objects.create(
            module=task, number=4, order=4,
            title='Добавление тестовых данных',
            description='''Добавьте начальные данные:

```sql
-- Роли
INSERT INTO roles (name) VALUES
('Участник'), ('Модератор'), ('Организатор'), ('Жюри');

-- Страны
INSERT INTO countries (name) VALUES
('Россия'), ('Казахстан'), ('Беларусь');

-- Направления
INSERT INTO directions (name) VALUES
('Информационная безопасность'), ('Разработка ПО'), ('Сети');

-- Города
INSERT INTO cities (name, country_id) VALUES
('Москва', 1), ('Санкт-Петербург', 1), ('Алматы', 2);

-- Тестовый пользователь
INSERT INTO users (id_number, first_name, last_name, gender, email, password, role_id)
VALUES ('10001', 'Иван', 'Иванов', 'М', 'ivan@test.ru', 'password123', 3);
```''',
            expected_result='Тестовые данные добавлены'
        )

    def _create_task_3_criteria(self, task):
        EvaluationCriteria.objects.create(
            module=task, order=1, max_score=3,
            name='Структура таблиц',
            description='Все таблицы созданы с правильной структурой'
        )
        EvaluationCriteria.objects.create(
            module=task, order=2, max_score=3,
            name='Связи и ключи',
            description='Первичные и внешние ключи настроены корректно'
        )
        EvaluationCriteria.objects.create(
            module=task, order=3, max_score=2,
            name='Ограничения',
            description='NOT NULL, UNIQUE и другие ограничения'
        )
        EvaluationCriteria.objects.create(
            module=task, order=4, max_score=2,
            name='Тестовые данные',
            description='Таблицы содержат начальные данные'
        )

    def _create_task_4(self, session, resources_path):
        task, created = Module.objects.update_or_create(
            section=session,
            task_number='4',
            defaults={
                'name': 'Импорт данных',
                'description': 'Загрузка данных из файлов Excel в базу данных',
                'task_condition': '''Заказчик системы предоставил файлы с данными (с пометкой import в ресурсах) для переноса в новую систему.

Подготовьте данные файлов для импорта и загрузите в разработанную базу данных.''',
                'instruction': 'Используйте SQL Import Wizard или программный импорт.',
                'duration': '60 минут',
                'max_score': 10,
                'order': 4
            }
        )

        if created:
            self._create_task_4_steps(task)
            self._create_task_4_criteria(task)
            if resources_path:
                self._load_task_4_files(task, resources_path)

    def _create_task_4_steps(self, task):
        step1 = ModuleStep.objects.create(
            module=task, number=1, order=1,
            title='Анализ файлов импорта',
            description='''Изучите предоставленные файлы:

1. **Страны_import.xlsx** - список стран
2. **Город_import.xlsx** - список городов
3. **Активности_import.xlsx** - виды активностей
4. **Жюри_import/** - данные жюри + фото
5. **Модераторы_import/** - данные модераторов + фото
6. **Организаторы_import/** - данные организаторов + фото
7. **Участники_import/** - данные участников + фото
8. **Мероприятия_import/** - мероприятия + изображения

Откройте каждый файл и изучите структуру данных.''',
            expected_result='Понимание структуры данных для импорта'
        )
        StepNote.objects.create(
            step=step1, note_type='warning', order=1,
            title='Порядок импорта важен!',
            content='Сначала импортируйте справочники (страны, города), затем основные данные (пользователи, мероприятия).'
        )

        step2 = ModuleStep.objects.create(
            module=task, number=2, order=2,
            title='Подготовка данных',
            description='''Проверьте и подготовьте данные:

1. Убедитесь, что названия колонок соответствуют полям в БД
2. Проверьте форматы данных:
   - Даты в правильном формате
   - Телефоны в едином формате
   - Email валидные
3. Удалите дубликаты
4. Заполните пустые обязательные поля

При необходимости создайте промежуточные таблицы для очистки данных.''',
            expected_result='Данные подготовлены к импорту'
        )

        step3 = ModuleStep.objects.create(
            module=task, number=3, order=3,
            title='Импорт справочников',
            description='''Импортируйте справочные данные:

**Способ 1: SQL Server Import Wizard**
1. ПКМ на базе данных → Tasks → Import Data
2. Выберите источник: Excel
3. Укажите файл и лист
4. Сопоставьте колонки с полями таблицы
5. Выполните импорт

**Способ 2: Программный импорт (Python)**
```python
import pandas as pd
import pymysql

df = pd.read_excel('Страны_import.xlsx')
connection = pymysql.connect(...)

for _, row in df.iterrows():
    cursor.execute(
        "INSERT INTO countries (name) VALUES (%s)",
        (row['Название'],)
    )
connection.commit()
```''',
            expected_result='Справочники импортированы'
        )

        ModuleStep.objects.create(
            module=task, number=4, order=4,
            title='Импорт пользователей и фотографий',
            description='''Импортируйте данные пользователей:

1. Импортируйте данные из Excel
2. Для каждого пользователя:
   - Определите его роль
   - Сопоставьте город с таблицей cities
   - Скопируйте фото в папку приложения
   - Сохраните путь к фото в БД

**Генерация id_number:**
```sql
-- Для жюри: 13XXX
-- Для модераторов: 12XXX
-- Для участников: 11XXX
-- Для организаторов: 10XXX
```

Проверьте корректность импорта запросом:
```sql
SELECT r.name as role, COUNT(*) as count
FROM users u
JOIN roles r ON u.role_id = r.id
GROUP BY r.name;
```''',
            expected_result='Все пользователи импортированы с фотографиями'
        )

    def _create_task_4_criteria(self, task):
        EvaluationCriteria.objects.create(
            module=task, order=1, max_score=3,
            name='Импорт справочников',
            description='Страны, города, направления импортированы'
        )
        EvaluationCriteria.objects.create(
            module=task, order=2, max_score=4,
            name='Импорт пользователей',
            description='Все категории пользователей импортированы'
        )
        EvaluationCriteria.objects.create(
            module=task, order=3, max_score=2,
            name='Фотографии',
            description='Фотографии загружены и привязаны'
        )
        EvaluationCriteria.objects.create(
            module=task, order=4, max_score=1,
            name='Целостность данных',
            description='Связи между таблицами корректны'
        )

    def _load_task_4_files(self, task, resources_path):
        base_path = os.path.join(resources_path, 'Вариант 7', 'Ресурсы')

        files_to_load = [
            ('Cтраны_import.xlsx', 'Страны для импорта', 'document'),
            ('Город_import.xlsx', 'Города для импорта', 'document'),
            ('Активности_import.xlsx', 'Активности для импорта', 'document'),
            ('DataDictionary_Template.xlsx', 'Шаблон словаря данных', 'document'),
        ]

        for filename, description, file_type in files_to_load:
            filepath = os.path.join(base_path, filename)
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    ModuleFile.objects.update_or_create(
                        module=task,
                        name=filename,
                        defaults={
                            'description': description,
                            'file_type': file_type,
                            'order': files_to_load.index((filename, description, file_type))
                        }
                    )
                    mf = ModuleFile.objects.get(module=task, name=filename)
                    mf.file.save(filename, File(f), save=True)
                self.stdout.write(f'  Загружен файл: {filename}')

    def _create_task_5(self, session, resources_path):
        task, created = Module.objects.update_or_create(
            section=session,
            task_number='5',
            defaults={
                'name': 'Data Dictionary (Словарь данных)',
                'description': 'Создание документации по структуре базы данных',
                'task_condition': '''Для диаграммы ER необходимо создать словарь данных – набор информации, описывающий, какой тип данных хранится в базе данных, их формат, структуру и способы использования данных.

Требования:
- Соответствие вашей диаграммы и словаря данных
- Подходящие типы данных, ограничения и форматы
- Отразите ограничения: первичные ключи, внешние ключи, NOT NULL
- Добавьте пояснения к неоднозначным полям

Используйте шаблон DataDictionary_Template.xlsx. Сохраните в формате .xls.''',
                'instruction': 'Откройте шаблон в Excel и заполните для каждой таблицы.',
                'duration': '30 минут',
                'max_score': 5,
                'order': 5
            }
        )

        if created:
            self._create_task_5_steps(task)
            self._create_task_5_criteria(task)

    def _create_task_5_steps(self, task):
        step1 = ModuleStep.objects.create(
            module=task, number=1, order=1,
            title='Изучение шаблона',
            description='''Откройте файл DataDictionary_Template.xlsx.

Структура шаблона:
- **Table Name** - название таблицы
- **Column Name** - название колонки
- **Data Type** - тип данных (INT, VARCHAR, DATE и т.д.)
- **Length** - длина (для строк)
- **Nullable** - может ли быть NULL (Yes/No)
- **Primary Key** - является ли первичным ключом
- **Foreign Key** - является ли внешним ключом
- **References** - на какую таблицу ссылается FK
- **Default** - значение по умолчанию
- **Description** - описание поля''',
            expected_result='Понимание структуры шаблона'
        )

        step2 = ModuleStep.objects.create(
            module=task, number=2, order=2,
            title='Заполнение для каждой таблицы',
            description='''Заполните словарь для всех таблиц. Пример для таблицы users:

| Column | Data Type | Length | Nullable | PK | FK | References | Description |
|--------|-----------|--------|----------|----|----|------------|-------------|
| id | INT | - | No | Yes | No | - | Уникальный идентификатор |
| id_number | VARCHAR | 20 | No | No | No | - | Номер пользователя |
| first_name | VARCHAR | 100 | No | No | No | - | Имя |
| last_name | VARCHAR | 100 | No | No | No | - | Фамилия |
| patronymic | VARCHAR | 100 | Yes | No | No | - | Отчество |
| gender | CHAR | 1 | No | No | No | - | Пол (М/Ж) |
| email | VARCHAR | 255 | No | No | No | - | Email адрес |
| phone | VARCHAR | 20 | Yes | No | No | - | Телефон |
| photo | VARCHAR | 255 | Yes | No | No | - | Путь к фото |
| password | VARCHAR | 255 | No | No | No | - | Хэш пароля |
| role_id | INT | - | No | No | Yes | roles(id) | Роль пользователя |
| city_id | INT | - | Yes | No | Yes | cities(id) | Город |
| direction_id | INT | - | Yes | No | Yes | directions(id) | Направление |''',
            expected_result='Словарь заполнен для таблицы users'
        )
        StepNote.objects.create(
            step=step2, note_type='tip', order=1,
            title='Типы данных',
            content='INT - целые числа, VARCHAR(n) - строки до n символов, TEXT - длинный текст, DATE - дата, DATETIME - дата и время, ENUM - перечисление.'
        )

        ModuleStep.objects.create(
            module=task, number=3, order=3,
            title='Добавление описаний',
            description='''Для каждого поля добавьте понятное описание:

- Что хранится в поле
- Формат данных (например, для телефона: +7(999)-099-90-90)
- Ограничения (например, длина пароля не менее 6 символов)
- Бизнес-правила (например, email должен быть уникальным)

Особое внимание уделите:
- Полям с неочевидным назначением
- Внешним ключам (укажите связь)
- Полям со специальными форматами''',
            expected_result='Все поля имеют описания'
        )

        ModuleStep.objects.create(
            module=task, number=4, order=4,
            title='Сохранение документа',
            description='''Проверьте словарь данных:

1. Все таблицы из ERD включены
2. Все поля каждой таблицы описаны
3. Типы данных соответствуют реальной БД
4. FK правильно указывают на родительские таблицы

Сохраните файл:
- Файл → Сохранить как
- Формат: Excel 97-2003 (.xls)
- Имя: DataDictionary.xls''',
            expected_result='Файл DataDictionary.xls сохранен'
        )

    def _create_task_5_criteria(self, task):
        EvaluationCriteria.objects.create(
            module=task, order=1, max_score=2,
            name='Полнота',
            description='Все таблицы и поля описаны'
        )
        EvaluationCriteria.objects.create(
            module=task, order=2, max_score=2,
            name='Корректность типов',
            description='Типы данных соответствуют БД'
        )
        EvaluationCriteria.objects.create(
            module=task, order=3, max_score=1,
            name='Описания',
            description='Понятные описания для всех полей'
        )

    def _create_task_6(self, session):
        task, created = Module.objects.update_or_create(
            section=session,
            task_number='6',
            defaults={
                'name': 'Разработка desktop-приложения',
                'description': 'Создание приложения на C#/WPF или аналогичной технологии',
                'task_condition': '''Разработайте desktop-приложение со следующим функционалом:

1. **Главное окно** - просмотр мероприятий с фильтрацией по направлению и дате
2. **Авторизация** - вход по IdNumber и Password с CAPTCHA и блокировкой
3. **Окно организатора** - приветствие по имени с учётом времени суток
4. **Регистрация жюри/модераторов** - форма с валидацией''',
                'instruction': 'Используйте C# WPF, Windows Forms или другую desktop-технологию.',
                'duration': '3 часа',
                'max_score': 50,
                'order': 6
            }
        )

        task.steps.all().delete()
        task.criteria.all().delete()
        task.useful_links.all().delete()

        self._create_task_6_steps(task)
        self._create_task_6_criteria(task)
        self.stdout.write(f'  Задание 6 обновлено с подробными инструкциями')

    def _create_task_6_steps(self, task):
        step1 = ModuleStep.objects.create(
            module=task, number=1, order=1,
            title='Создание проекта WPF',
            description='''Создайте новый проект в Visual Studio:

1. **Откройте Visual Studio 2022**
2. **Создайте новый проект:**
   - File → New → Project
   - Выберите "WPF Application" (.NET Framework или .NET 6+)
   - Название проекта: ConferenceApp
   - Расположение: папка вашего решения

3. **Структура проекта:**
```
ConferenceApp/
├── Models/           # Классы данных (User, Event, Activity)
├── Views/            # XAML-окна
│   ├── MainWindow.xaml
│   ├── LoginWindow.xaml
│   ├── OrganizerWindow.xaml
│   └── RegistrationWindow.xaml
├── ViewModels/       # Логика представления (опционально)
├── Services/         # Работа с БД
│   └── DatabaseService.cs
└── Resources/        # Стили, изображения
```

4. **Подключите NuGet-пакеты:**
   - Tools → NuGet Package Manager → Manage NuGet Packages
   - Установите: MySql.Data (или Npgsql для PostgreSQL)

5. **Создайте класс подключения к БД:**
```csharp
public class DatabaseService
{
    private string connectionString = "Server=localhost;Database=conference_db;Uid=root;Pwd=password;";

    public MySqlConnection GetConnection()
    {
        return new MySqlConnection(connectionString);
    }
}
```''',
            expected_result='Проект WPF создан и настроен'
        )
        StepNote.objects.create(
            step=step1, note_type='tip', order=1,
            title='Выбор .NET версии',
            content='Для демо-экзамена рекомендуется .NET Framework 4.7.2 или .NET 6, так как они стабильны и хорошо документированы.'
        )

        step2 = ModuleStep.objects.create(
            module=task, number=2, order=2,
            title='Главное окно системы',
            description='''Создайте главное окно со списком мероприятий.

**MainWindow.xaml - Разметка:**
```xml
<Window x:Class="ConferenceApp.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Система управления конференциями"
        Height="600" Width="900"
        WindowStartupLocation="CenterScreen">
    <Grid>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
        </Grid.RowDefinitions>

        <!-- Панель фильтров -->
        <StackPanel Grid.Row="0" Orientation="Horizontal"
                    Margin="20" Background="#F5F5F5" HorizontalAlignment="Stretch">
            <TextBlock Text="Направление:" VerticalAlignment="Center" Margin="10,0"/>
            <ComboBox x:Name="DirectionFilter" Width="200" Margin="5"
                      SelectionChanged="DirectionFilter_SelectionChanged">
                <ComboBoxItem Content="Все направления" IsSelected="True"/>
            </ComboBox>

            <TextBlock Text="Дата:" VerticalAlignment="Center" Margin="20,0,10,0"/>
            <DatePicker x:Name="DateFilter" Width="150"
                        SelectedDateChanged="DateFilter_SelectedDateChanged"/>

            <Button Content="Сбросить" Margin="20,5" Padding="15,5"
                    Click="ResetFilters_Click"/>

            <Button x:Name="LoginButton" Content="Войти"
                    Margin="20,5" Padding="20,5"
                    Background="#4F46E5" Foreground="White"
                    Click="Login_Click" HorizontalAlignment="Right"/>
        </StackPanel>

        <!-- Список мероприятий -->
        <ListView x:Name="EventsListView" Grid.Row="1" Margin="20,0,20,20"
                  BorderThickness="0">
            <ListView.ItemTemplate>
                <DataTemplate>
                    <Border BorderBrush="#E5E7EB" BorderThickness="1"
                            CornerRadius="8" Margin="5" Padding="15"
                            Background="White">
                        <Grid>
                            <Grid.ColumnDefinitions>
                                <ColumnDefinition Width="80"/>
                                <ColumnDefinition Width="*"/>
                                <ColumnDefinition Width="Auto"/>
                            </Grid.ColumnDefinitions>

                            <Image Source="{Binding LogoPath}"
                                   Width="60" Height="60" Stretch="UniformToFill"/>

                            <StackPanel Grid.Column="1" Margin="15,0">
                                <TextBlock Text="{Binding Name}"
                                           FontSize="16" FontWeight="SemiBold"/>
                                <TextBlock Text="{Binding DirectionName}"
                                           Foreground="#6B7280" Margin="0,5,0,0"/>
                            </StackPanel>

                            <StackPanel Grid.Column="2" VerticalAlignment="Center">
                                <TextBlock Text="{Binding DateStart, StringFormat=dd.MM.yyyy}"
                                           FontSize="14" Foreground="#4F46E5"/>
                            </StackPanel>
                        </Grid>
                    </Border>
                </DataTemplate>
            </ListView.ItemTemplate>
        </ListView>
    </Grid>
</Window>
```

**MainWindow.xaml.cs - Логика:**
```csharp
public partial class MainWindow : Window
{
    private DatabaseService db = new DatabaseService();
    private List<Event> allEvents = new List<Event>();

    public MainWindow()
    {
        InitializeComponent();
        LoadDirections();
        LoadEvents();
    }

    private void LoadDirections()
    {
        using (var conn = db.GetConnection())
        {
            conn.Open();
            var cmd = new MySqlCommand("SELECT id, name FROM directions", conn);
            var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                DirectionFilter.Items.Add(new ComboBoxItem
                {
                    Content = reader.GetString("name"),
                    Tag = reader.GetInt32("id")
                });
            }
        }
    }

    private void LoadEvents()
    {
        allEvents.Clear();
        using (var conn = db.GetConnection())
        {
            conn.Open();
            var cmd = new MySqlCommand(@"
                SELECT e.*, d.name as direction_name
                FROM events e
                LEFT JOIN directions d ON e.direction_id = d.id", conn);
            var reader = cmd.ExecuteReader();
            while (reader.Read())
            {
                allEvents.Add(new Event
                {
                    Id = reader.GetInt32("id"),
                    Name = reader.GetString("name"),
                    DirectionName = reader.IsDBNull(reader.GetOrdinal("direction_name"))
                        ? "" : reader.GetString("direction_name"),
                    DateStart = reader.GetDateTime("date_start"),
                    LogoPath = reader.IsDBNull(reader.GetOrdinal("logo"))
                        ? "pack://application:,,,/Resources/default_event.png"
                        : reader.GetString("logo")
                });
            }
        }
        EventsListView.ItemsSource = allEvents;
    }

    private void ApplyFilters()
    {
        var filtered = allEvents.AsEnumerable();

        // Фильтр по направлению
        if (DirectionFilter.SelectedIndex > 0)
        {
            var selectedItem = (ComboBoxItem)DirectionFilter.SelectedItem;
            var directionId = (int)selectedItem.Tag;
            filtered = filtered.Where(e => e.DirectionId == directionId);
        }

        // Фильтр по дате
        if (DateFilter.SelectedDate.HasValue)
        {
            var date = DateFilter.SelectedDate.Value;
            filtered = filtered.Where(e => e.DateStart.Date == date.Date);
        }

        EventsListView.ItemsSource = filtered.ToList();
    }

    private void Login_Click(object sender, RoutedEventArgs e)
    {
        var loginWindow = new LoginWindow();
        loginWindow.ShowDialog();
    }
}
```''',
            expected_result='Главное окно с фильтрами и списком мероприятий'
        )
        StepNote.objects.create(
            step=step2, note_type='info', order=1,
            title='Модель Event',
            content='''Создайте класс Event в папке Models:

```csharp
public class Event
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Description { get; set; }
    public string LogoPath { get; set; }
    public DateTime DateStart { get; set; }
    public DateTime DateEnd { get; set; }
    public int DirectionId { get; set; }
    public string DirectionName { get; set; }
}
```'''
        )

        step3 = ModuleStep.objects.create(
            module=task, number=3, order=3,
            title='Экран авторизации с CAPTCHA',
            description='''Создайте окно авторизации с CAPTCHA и блокировкой.

**LoginWindow.xaml:**
```xml
<Window x:Class="ConferenceApp.LoginWindow"
        Title="Авторизация" Height="450" Width="400"
        WindowStartupLocation="CenterScreen"
        ResizeMode="NoResize">
    <Grid Margin="30">
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
        </Grid.RowDefinitions>

        <TextBlock Text="Вход в систему" FontSize="24" FontWeight="Bold"
                   HorizontalAlignment="Center" Margin="0,0,0,30"/>

        <!-- ID Number -->
        <StackPanel Grid.Row="1" Margin="0,10">
            <TextBlock Text="ID Number:" Margin="0,0,0,5"/>
            <TextBox x:Name="IdNumberTextBox" Height="35" FontSize="14"
                     Padding="10,5"/>
        </StackPanel>

        <!-- Password -->
        <StackPanel Grid.Row="2" Margin="0,10">
            <TextBlock Text="Пароль:" Margin="0,0,0,5"/>
            <PasswordBox x:Name="PasswordBox" Height="35" FontSize="14"
                         Padding="10,5"/>
        </StackPanel>

        <!-- CAPTCHA -->
        <StackPanel Grid.Row="3" Margin="0,10">
            <TextBlock Text="Введите символы с изображения:" Margin="0,0,0,5"/>
            <Grid>
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="*"/>
                    <ColumnDefinition Width="Auto"/>
                </Grid.ColumnDefinitions>
                <Border BorderBrush="#CCC" BorderThickness="1" Height="50"
                        Background="White">
                    <Canvas x:Name="CaptchaCanvas"/>
                </Border>
                <Button Grid.Column="1" Content="↻" Width="40" Height="50"
                        Margin="5,0,0,0" Click="RefreshCaptcha_Click"
                        FontSize="20"/>
            </Grid>
            <TextBox x:Name="CaptchaTextBox" Height="35" FontSize="14"
                     Padding="10,5" Margin="0,10,0,0"/>
        </StackPanel>

        <!-- Remember me -->
        <CheckBox x:Name="RememberMeCheckBox" Grid.Row="4"
                  Content="Запомнить меня" Margin="0,10"/>

        <!-- Timer (hidden by default) -->
        <TextBlock x:Name="TimerTextBlock" Grid.Row="5"
                   Foreground="Red" FontSize="14"
                   HorizontalAlignment="Center" Visibility="Collapsed"/>

        <!-- Buttons -->
        <StackPanel Grid.Row="6" Orientation="Horizontal"
                    HorizontalAlignment="Center" VerticalAlignment="Bottom"
                    Margin="0,20,0,0">
            <Button Content="Войти" Width="120" Height="40"
                    Background="#4F46E5" Foreground="White"
                    Click="Login_Click" IsDefault="True"/>
            <Button Content="Отмена" Width="120" Height="40"
                    Margin="20,0,0,0" Click="Cancel_Click" IsCancel="True"/>
        </StackPanel>
    </Grid>
</Window>
```

**LoginWindow.xaml.cs:**
```csharp
public partial class LoginWindow : Window
{
    private DatabaseService db = new DatabaseService();
    private string captchaText;
    private int failedAttempts = 0;
    private DispatcherTimer lockTimer;
    private int lockSeconds = 10;

    public User LoggedInUser { get; private set; }

    public LoginWindow()
    {
        InitializeComponent();
        GenerateCaptcha();
        LoadRememberedUser();
    }

    private void GenerateCaptcha()
    {
        // Генерация случайных символов
        const string chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";
        var random = new Random();
        captchaText = new string(Enumerable.Repeat(chars, 4)
            .Select(s => s[random.Next(s.Length)]).ToArray());

        // Отрисовка на Canvas
        CaptchaCanvas.Children.Clear();

        // Добавляем шум (линии)
        for (int i = 0; i < 5; i++)
        {
            var line = new Line
            {
                X1 = random.Next(0, 150),
                Y1 = random.Next(0, 50),
                X2 = random.Next(0, 150),
                Y2 = random.Next(0, 50),
                Stroke = new SolidColorBrush(Color.FromRgb(
                    (byte)random.Next(150, 200),
                    (byte)random.Next(150, 200),
                    (byte)random.Next(150, 200))),
                StrokeThickness = 1
            };
            CaptchaCanvas.Children.Add(line);
        }

        // Добавляем текст
        var textBlock = new TextBlock
        {
            Text = captchaText,
            FontSize = 28,
            FontWeight = FontWeights.Bold,
            Foreground = new SolidColorBrush(Color.FromRgb(50, 50, 50))
        };
        Canvas.SetLeft(textBlock, 30);
        Canvas.SetTop(textBlock, 8);
        CaptchaCanvas.Children.Add(textBlock);
    }

    private void Login_Click(object sender, RoutedEventArgs e)
    {
        // Проверка блокировки
        if (failedAttempts >= 3)
        {
            MessageBox.Show("Система заблокирована. Подождите.",
                "Блокировка", MessageBoxButton.OK, MessageBoxImage.Warning);
            return;
        }

        // Проверка CAPTCHA
        if (CaptchaTextBox.Text.ToUpper() != captchaText)
        {
            HandleFailedAttempt("Неверная CAPTCHA");
            return;
        }

        // Проверка логина/пароля
        using (var conn = db.GetConnection())
        {
            conn.Open();
            var cmd = new MySqlCommand(@"
                SELECT u.*, r.name as role_name
                FROM users u
                JOIN roles r ON u.role_id = r.id
                WHERE u.id_number = @id AND u.password = @pwd", conn);
            cmd.Parameters.AddWithValue("@id", IdNumberTextBox.Text);
            cmd.Parameters.AddWithValue("@pwd", PasswordBox.Password);

            var reader = cmd.ExecuteReader();
            if (reader.Read())
            {
                LoggedInUser = new User
                {
                    Id = reader.GetInt32("id"),
                    IdNumber = reader.GetString("id_number"),
                    FirstName = reader.GetString("first_name"),
                    LastName = reader.GetString("last_name"),
                    Patronymic = reader.IsDBNull(reader.GetOrdinal("patronymic"))
                        ? "" : reader.GetString("patronymic"),
                    Photo = reader.IsDBNull(reader.GetOrdinal("photo"))
                        ? null : reader.GetString("photo"),
                    RoleName = reader.GetString("role_name")
                };

                // Сохранение если "Запомнить меня"
                if (RememberMeCheckBox.IsChecked == true)
                {
                    Properties.Settings.Default.RememberedUser = IdNumberTextBox.Text;
                    Properties.Settings.Default.Save();
                }

                DialogResult = true;
                Close();
            }
            else
            {
                HandleFailedAttempt("Неверный логин или пароль");
            }
        }
    }

    private void HandleFailedAttempt(string message)
    {
        failedAttempts++;
        MessageBox.Show(message, "Ошибка", MessageBoxButton.OK, MessageBoxImage.Error);
        GenerateCaptcha();
        CaptchaTextBox.Clear();

        if (failedAttempts >= 3)
        {
            StartLockTimer();
        }
    }

    private void StartLockTimer()
    {
        lockSeconds = 10;
        TimerTextBlock.Visibility = Visibility.Visible;

        lockTimer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(1) };
        lockTimer.Tick += (s, e) =>
        {
            lockSeconds--;
            TimerTextBlock.Text = $"Повторите через {lockSeconds} сек.";

            if (lockSeconds <= 0)
            {
                lockTimer.Stop();
                TimerTextBlock.Visibility = Visibility.Collapsed;
                failedAttempts = 0;
            }
        };
        lockTimer.Start();
        TimerTextBlock.Text = $"Повторите через {lockSeconds} сек.";
    }
}
```''',
            expected_result='Окно авторизации с CAPTCHA и блокировкой'
        )
        StepNote.objects.create(
            step=step3, note_type='warning', order=1,
            title='Безопасность паролей',
            content='На демо-экзамене можно использовать plain text пароли для простоты. В реальных проектах обязательно используйте хэширование (BCrypt, SHA256)!'
        )
        StepNote.objects.create(
            step=step3, note_type='tip', order=2,
            title='Проверка CAPTCHA',
            content='Используйте ToUpper() для сравнения, чтобы регистр не влиял на результат. Генерируйте новую CAPTCHA при каждой ошибке.'
        )

        step4 = ModuleStep.objects.create(
            module=task, number=4, order=4,
            title='Окно организатора',
            description='''Создайте окно организатора с приветствием.

**OrganizerWindow.xaml:**
```xml
<Window x:Class="ConferenceApp.OrganizerWindow"
        Title="Панель организатора" Height="600" Width="900"
        WindowStartupLocation="CenterScreen">
    <Grid>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto"/>
            <RowDefinition Height="*"/>
        </Grid.RowDefinitions>

        <!-- Шапка с приветствием -->
        <Border Grid.Row="0" Background="#4F46E5" Padding="20">
            <Grid>
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="Auto"/>
                    <ColumnDefinition Width="*"/>
                    <ColumnDefinition Width="Auto"/>
                </Grid.ColumnDefinitions>

                <!-- Фото пользователя -->
                <Border CornerRadius="50" Width="80" Height="80"
                        BorderBrush="White" BorderThickness="3">
                    <Border.Background>
                        <ImageBrush x:Name="UserPhotoBrush" Stretch="UniformToFill"/>
                    </Border.Background>
                </Border>

                <!-- Приветствие -->
                <StackPanel Grid.Column="1" Margin="20,0" VerticalAlignment="Center">
                    <TextBlock x:Name="GreetingText" FontSize="24"
                               Foreground="White" FontWeight="SemiBold"/>
                    <TextBlock x:Name="RoleText" FontSize="14"
                               Foreground="#E0E0E0" Margin="0,5,0,0"/>
                </StackPanel>

                <!-- Кнопка выхода -->
                <Button Grid.Column="2" Content="Выйти"
                        Background="Transparent" Foreground="White"
                        BorderBrush="White" Padding="20,10"
                        Click="Logout_Click"/>
            </Grid>
        </Border>

        <!-- Навигация -->
        <Grid Grid.Row="1" Margin="30">
            <Grid.ColumnDefinitions>
                <ColumnDefinition Width="*"/>
                <ColumnDefinition Width="*"/>
            </Grid.ColumnDefinitions>
            <Grid.RowDefinitions>
                <RowDefinition Height="*"/>
                <RowDefinition Height="*"/>
            </Grid.RowDefinitions>

            <Button Style="{StaticResource NavButtonStyle}"
                    Content="&#x1F4C5;&#x0A;Мероприятия"
                    Click="Events_Click"/>
            <Button Grid.Column="1" Style="{StaticResource NavButtonStyle}"
                    Content="&#x1F465;&#x0A;Участники"
                    Click="Participants_Click"/>
            <Button Grid.Row="1" Style="{StaticResource NavButtonStyle}"
                    Content="&#x2696;&#x0A;Жюри и модераторы"
                    Click="JuryModerators_Click"/>
            <Button Grid.Row="1" Grid.Column="1"
                    Style="{StaticResource NavButtonStyle}"
                    Content="&#x1F464;&#x0A;Мой профиль"
                    Click="Profile_Click"/>
        </Grid>
    </Grid>
</Window>
```

**OrganizerWindow.xaml.cs:**
```csharp
public partial class OrganizerWindow : Window
{
    private User currentUser;

    public OrganizerWindow(User user)
    {
        InitializeComponent();
        currentUser = user;
        SetupGreeting();
        LoadUserPhoto();
    }

    private void SetupGreeting()
    {
        string greeting = GetGreetingByTime();
        string fullName = $"{currentUser.FirstName} {currentUser.Patronymic}";

        GreetingText.Text = $"{greeting}, {fullName}!";
        RoleText.Text = currentUser.RoleName;
    }

    private string GetGreetingByTime()
    {
        int hour = DateTime.Now.Hour;

        if (hour >= 9 && hour <= 11)
            return "Доброе утро";
        else if (hour > 11 && hour <= 18)
            return "Добрый день";
        else
            return "Добрый вечер";
    }

    private void LoadUserPhoto()
    {
        if (!string.IsNullOrEmpty(currentUser.Photo))
        {
            try
            {
                var photoPath = Path.Combine(
                    AppDomain.CurrentDomain.BaseDirectory,
                    "Resources", "Photos", currentUser.Photo);

                if (File.Exists(photoPath))
                {
                    UserPhotoBrush.ImageSource = new BitmapImage(new Uri(photoPath));
                }
                else
                {
                    LoadDefaultPhoto();
                }
            }
            catch
            {
                LoadDefaultPhoto();
            }
        }
        else
        {
            LoadDefaultPhoto();
        }
    }

    private void LoadDefaultPhoto()
    {
        UserPhotoBrush.ImageSource = new BitmapImage(
            new Uri("pack://application:,,,/Resources/default_avatar.png"));
    }

    private void JuryModerators_Click(object sender, RoutedEventArgs e)
    {
        var registrationWindow = new RegistrationWindow();
        registrationWindow.ShowDialog();
    }

    private void Logout_Click(object sender, RoutedEventArgs e)
    {
        var mainWindow = new MainWindow();
        mainWindow.Show();
        this.Close();
    }
}
```

**App.xaml - Стиль кнопок навигации:**
```xml
<Application.Resources>
    <Style x:Key="NavButtonStyle" TargetType="Button">
        <Setter Property="Margin" Value="10"/>
        <Setter Property="FontSize" Value="18"/>
        <Setter Property="Background" Value="White"/>
        <Setter Property="BorderBrush" Value="#E5E7EB"/>
        <Setter Property="BorderThickness" Value="1"/>
        <Setter Property="Template">
            <Setter.Value>
                <ControlTemplate TargetType="Button">
                    <Border Background="{TemplateBinding Background}"
                            BorderBrush="{TemplateBinding BorderBrush}"
                            BorderThickness="{TemplateBinding BorderThickness}"
                            CornerRadius="12">
                        <ContentPresenter HorizontalAlignment="Center"
                                          VerticalAlignment="Center"
                                          TextBlock.TextAlignment="Center"/>
                    </Border>
                </ControlTemplate>
            </Setter.Value>
        </Setter>
        <Style.Triggers>
            <Trigger Property="IsMouseOver" Value="True">
                <Setter Property="Background" Value="#F5F3FF"/>
                <Setter Property="BorderBrush" Value="#4F46E5"/>
            </Trigger>
        </Style.Triggers>
    </Style>
</Application.Resources>
```''',
            expected_result='Окно организатора с приветствием и навигацией'
        )
        StepNote.objects.create(
            step=step4, note_type='info', order=1,
            title='Время приветствия',
            content='''По заданию:
- 9:00-11:00 → "Доброе утро"
- 11:01-18:00 → "Добрый день"
- 18:01-24:00 → "Добрый вечер"'''
        )

        step5 = ModuleStep.objects.create(
            module=task, number=5, order=5,
            title='Форма регистрации пользователей',
            description='''Создайте форму регистрации жюри и модераторов.

**RegistrationWindow.xaml:**
```xml
<Window x:Class="ConferenceApp.RegistrationWindow"
        Title="Регистрация пользователя" Height="700" Width="500"
        WindowStartupLocation="CenterScreen" ResizeMode="NoResize">
    <ScrollViewer VerticalScrollBarVisibility="Auto">
        <StackPanel Margin="30">
            <TextBlock Text="Регистрация нового пользователя"
                       FontSize="20" FontWeight="Bold" Margin="0,0,0,20"/>

            <!-- ID Number (readonly) -->
            <StackPanel Margin="0,5">
                <TextBlock Text="ID Number:"/>
                <TextBox x:Name="IdNumberTextBox" IsReadOnly="True"
                         Background="#F5F5F5" Height="35"/>
            </StackPanel>

            <!-- ФИО -->
            <Grid Margin="0,5">
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="*"/>
                    <ColumnDefinition Width="*"/>
                    <ColumnDefinition Width="*"/>
                </Grid.ColumnDefinitions>
                <StackPanel Margin="0,0,5,0">
                    <TextBlock Text="Фамилия: *"/>
                    <TextBox x:Name="LastNameTextBox" Height="35"/>
                </StackPanel>
                <StackPanel Grid.Column="1" Margin="5,0">
                    <TextBlock Text="Имя: *"/>
                    <TextBox x:Name="FirstNameTextBox" Height="35"/>
                </StackPanel>
                <StackPanel Grid.Column="2" Margin="5,0,0,0">
                    <TextBlock Text="Отчество:"/>
                    <TextBox x:Name="PatronymicTextBox" Height="35"/>
                </StackPanel>
            </Grid>

            <!-- Пол и Роль -->
            <Grid Margin="0,5">
                <Grid.ColumnDefinitions>
                    <ColumnDefinition Width="*"/>
                    <ColumnDefinition Width="*"/>
                </Grid.ColumnDefinitions>
                <StackPanel Margin="0,0,5,0">
                    <TextBlock Text="Пол: *"/>
                    <ComboBox x:Name="GenderComboBox" Height="35">
                        <ComboBoxItem Content="М"/>
                        <ComboBoxItem Content="Ж"/>
                    </ComboBox>
                </StackPanel>
                <StackPanel Grid.Column="1" Margin="5,0,0,0">
                    <TextBlock Text="Роль: *"/>
                    <ComboBox x:Name="RoleComboBox" Height="35"
                              SelectionChanged="RoleComboBox_SelectionChanged">
                        <ComboBoxItem Content="Жюри" Tag="4"/>
                        <ComboBoxItem Content="Модератор" Tag="2"/>
                    </ComboBox>
                </StackPanel>
            </Grid>

            <!-- Email -->
            <StackPanel Margin="0,5">
                <TextBlock Text="Email: *"/>
                <TextBox x:Name="EmailTextBox" Height="35"/>
            </StackPanel>

            <!-- Телефон -->
            <StackPanel Margin="0,5">
                <TextBlock Text="Телефон:"/>
                <TextBox x:Name="PhoneTextBox" Height="35"
                         PreviewTextInput="Phone_PreviewTextInput"
                         Text="+7("/>
            </StackPanel>

            <!-- Направление -->
            <StackPanel Margin="0,5">
                <TextBlock Text="Направление:"/>
                <ComboBox x:Name="DirectionComboBox" Height="35" IsEditable="True"/>
            </StackPanel>

            <!-- Прикрепление к мероприятию -->
            <StackPanel Margin="0,5">
                <CheckBox x:Name="AttachToEventCheckBox"
                          Content="Прикрепить к мероприятию"
                          Checked="AttachToEvent_Changed"
                          Unchecked="AttachToEvent_Changed"/>
                <ComboBox x:Name="EventComboBox" Height="35"
                          IsEnabled="False" Margin="0,5,0,0"/>
            </StackPanel>

            <!-- Фото -->
            <StackPanel Margin="0,5">
                <TextBlock Text="Фото:"/>
                <Grid>
                    <Grid.ColumnDefinitions>
                        <ColumnDefinition Width="*"/>
                        <ColumnDefinition Width="Auto"/>
                    </Grid.ColumnDefinitions>
                    <TextBox x:Name="PhotoPathTextBox" Height="35" IsReadOnly="True"/>
                    <Button Grid.Column="1" Content="Выбрать..." Width="100"
                            Margin="5,0,0,0" Click="SelectPhoto_Click"/>
                </Grid>
                <Image x:Name="PhotoPreview" MaxHeight="150" Margin="0,10,0,0"
                       HorizontalAlignment="Left"/>
            </StackPanel>

            <!-- Пароль -->
            <StackPanel Margin="0,5">
                <TextBlock Text="Пароль: *"/>
                <Grid>
                    <PasswordBox x:Name="PasswordBox" Height="35"
                                 PasswordChanged="Password_Changed"/>
                    <TextBox x:Name="PasswordTextBox" Height="35"
                             Visibility="Collapsed"
                             TextChanged="PasswordText_Changed"/>
                </Grid>
                <TextBlock x:Name="PasswordHint" FontSize="11"
                           Foreground="#6B7280" Margin="0,5,0,0"
                           Text="Мин. 6 символов, заглавные и строчные буквы, цифра, спецсимвол"/>
            </StackPanel>

            <!-- Повтор пароля -->
            <StackPanel Margin="0,5">
                <TextBlock Text="Повтор пароля: *"/>
                <PasswordBox x:Name="ConfirmPasswordBox" Height="35"/>
            </StackPanel>

            <!-- Показать пароль -->
            <CheckBox x:Name="ShowPasswordCheckBox" Content="Показать пароль"
                      Margin="0,5" Checked="ShowPassword_Changed"
                      Unchecked="ShowPassword_Changed"/>

            <!-- Кнопки -->
            <StackPanel Orientation="Horizontal" HorizontalAlignment="Center"
                        Margin="0,20,0,0">
                <Button Content="Сохранить" Width="120" Height="40"
                        Background="#4F46E5" Foreground="White"
                        Click="Save_Click"/>
                <Button Content="Отмена" Width="120" Height="40"
                        Margin="20,0,0,0" Click="Cancel_Click"/>
            </StackPanel>
        </StackPanel>
    </ScrollViewer>
</Window>
```

**RegistrationWindow.xaml.cs (валидация):**
```csharp
public partial class RegistrationWindow : Window
{
    private DatabaseService db = new DatabaseService();
    private string photoPath = "";

    public RegistrationWindow()
    {
        InitializeComponent();
        LoadDirections();
        LoadEvents();
        GenerateIdNumber();
    }

    private void GenerateIdNumber()
    {
        // Жюри: 13XXX, Модераторы: 12XXX
        var prefix = (RoleComboBox.SelectedItem as ComboBoxItem)?.Tag?.ToString() == "4"
            ? "13" : "12";

        using (var conn = db.GetConnection())
        {
            conn.Open();
            var cmd = new MySqlCommand(@"
                SELECT MAX(CAST(SUBSTRING(id_number, 3) AS UNSIGNED))
                FROM users WHERE id_number LIKE @prefix", conn);
            cmd.Parameters.AddWithValue("@prefix", prefix + "%");

            var result = cmd.ExecuteScalar();
            int nextNum = result == DBNull.Value ? 1 : Convert.ToInt32(result) + 1;
            IdNumberTextBox.Text = $"{prefix}{nextNum:D3}";
        }
    }

    private bool ValidatePassword(string password)
    {
        if (password.Length < 6) return false;
        if (!password.Any(char.IsUpper)) return false;
        if (!password.Any(char.IsLower)) return false;
        if (!password.Any(char.IsDigit)) return false;
        if (!password.Any(c => !char.IsLetterOrDigit(c))) return false;
        return true;
    }

    private bool ValidateEmail(string email)
    {
        try
        {
            var addr = new System.Net.Mail.MailAddress(email);
            return addr.Address == email;
        }
        catch
        {
            return false;
        }
    }

    private void Phone_PreviewTextInput(object sender, TextCompositionEventArgs e)
    {
        // Маска: +7(999)-099-90-90
        var textBox = sender as TextBox;
        var text = textBox.Text + e.Text;

        e.Handled = !char.IsDigit(e.Text[0]);

        // Автоформатирование
        if (text.Length == 6) // После +7(XXX
            textBox.Text = text + ")-";
        else if (text.Length == 11) // После +7(XXX)-XXX
            textBox.Text = text + "-";
        else if (text.Length == 14) // После +7(XXX)-XXX-XX
            textBox.Text = text + "-";

        textBox.CaretIndex = textBox.Text.Length;
    }

    private void Save_Click(object sender, RoutedEventArgs e)
    {
        // Валидация
        if (string.IsNullOrWhiteSpace(LastNameTextBox.Text) ||
            string.IsNullOrWhiteSpace(FirstNameTextBox.Text))
        {
            MessageBox.Show("Заполните обязательные поля (ФИО)");
            return;
        }

        if (!ValidateEmail(EmailTextBox.Text))
        {
            MessageBox.Show("Некорректный email");
            return;
        }

        var password = ShowPasswordCheckBox.IsChecked == true
            ? PasswordTextBox.Text : PasswordBox.Password;

        if (!ValidatePassword(password))
        {
            MessageBox.Show("Пароль не соответствует требованиям");
            return;
        }

        if (password != ConfirmPasswordBox.Password)
        {
            MessageBox.Show("Пароли не совпадают");
            return;
        }

        // Сохранение в БД
        SaveUser();
        MessageBox.Show("Пользователь успешно зарегистрирован!");
        DialogResult = true;
        Close();
    }
}
```''',
            expected_result='Форма регистрации с валидацией всех полей'
        )
        StepNote.objects.create(
            step=step5, note_type='important', order=1,
            title='Требования к паролю',
            content='''По заданию пароль должен содержать:
- Минимум 6 символов
- Заглавные буквы (A-Z)
- Строчные буквы (a-z)
- Минимум 1 цифра (0-9)
- Минимум 1 спецсимвол (!@#$%^&* и т.д.)'''
        )
        StepNote.objects.create(
            step=step5, note_type='tip', order=2,
            title='Генерация ID Number',
            content='''По заданию:
- Жюри: 13XXX (например, 13001, 13002)
- Модераторы: 12XXX (например, 12001, 12002)
Получите MAX из БД и добавьте 1.'''
        )

        UsefulLink.objects.update_or_create(
            module=task,
            title='WPF Tutorial - Microsoft Docs',
            defaults={
                'url': 'https://docs.microsoft.com/en-us/dotnet/desktop/wpf/',
                'description': 'Официальная документация WPF от Microsoft',
                'order': 1
            }
        )
        UsefulLink.objects.update_or_create(
            module=task,
            title='XAML Controls Gallery',
            defaults={
                'url': 'https://docs.microsoft.com/en-us/windows/apps/design/controls/',
                'description': 'Галерея элементов управления XAML с примерами',
                'order': 2
            }
        )
        UsefulLink.objects.update_or_create(
            module=task,
            title='MySQL Connector .NET',
            defaults={
                'url': 'https://dev.mysql.com/doc/connector-net/en/',
                'description': 'Документация по подключению C# к MySQL',
                'order': 3
            }
        )

    def _create_task_6_criteria(self, task):
        EvaluationCriteria.objects.create(
            module=task, order=1, max_score=10,
            name='Главное окно',
            description='Просмотр и фильтрация мероприятий'
        )
        EvaluationCriteria.objects.create(
            module=task, order=2, max_score=15,
            name='Авторизация',
            description='CAPTCHA, блокировка, запоминание'
        )
        EvaluationCriteria.objects.create(
            module=task, order=3, max_score=10,
            name='Окно организатора',
            description='Приветствие, фото, навигация'
        )
        EvaluationCriteria.objects.create(
            module=task, order=4, max_score=15,
            name='Регистрация',
            description='Все поля, валидация, сохранение в БД'
        )

    def _create_task_7(self, session):
        task, created = Module.objects.update_or_create(
            section=session,
            task_number='7',
            defaults={
                'name': 'Руководство пользователя',
                'description': 'Создание документации для приложения',
                'task_condition': '''Разработайте руководство пользователя для вашего настольного приложения, которое описывает последовательность действий для выполнения всех функций системы.

Требования:
- Живые примеры и скриншоты вашей системы
- Титульный лист
- Автоматическая нумерация страниц
- Разделение на подразделы с оглавлением
- Ссылки на рисунки
- Нумерованные и маркированные списки

Сохраните в формате Word: Руководство_пользователя_XX.docx (где XX - номер рабочего места).''',
                'instruction': 'Используйте Microsoft Word или аналог.',
                'duration': '45 минут',
                'max_score': 10,
                'order': 7
            }
        )

        if created:
            self._create_task_7_steps(task)
            self._create_task_7_criteria(task)

    def _create_task_7_steps(self, task):
        step1 = ModuleStep.objects.create(
            module=task, number=1, order=1,
            title='Создание структуры документа',
            description='''Создайте документ Word со следующей структурой:

1. **Титульный лист**
   - Название системы
   - "Руководство пользователя"
   - Версия, дата
   - Автор

2. **Оглавление** (автоматическое)

3. **Введение**
   - Назначение системы
   - Требования к ПО

4. **Главное окно**
   - Описание интерфейса
   - Фильтрация мероприятий

5. **Авторизация**
   - Вход в систему
   - CAPTCHA
   - Восстановление доступа

6. **Окно организатора**
   - Описание функций
   - Навигация

7. **Регистрация пользователей**
   - Заполнение формы
   - Требования к паролю''',
            expected_result='Структура документа создана'
        )

        step2 = ModuleStep.objects.create(
            module=task, number=2, order=2,
            title='Добавление скриншотов',
            description='''Для каждого раздела добавьте скриншоты:

1. Сделайте скриншот окна (Win+Shift+S или Print Screen)
2. Вставьте в Word (Ctrl+V)
3. Добавьте подпись:
   - Вставка → Подпись → Вставить название
   - Выберите "Рисунок"
   - Напишите описание

Пример подписи: "Рисунок 1 - Главное окно системы"

Настройте автоматическую нумерацию рисунков для ссылок.''',
            expected_result='Скриншоты добавлены с подписями'
        )
        StepNote.objects.create(
            step=step2, note_type='tip', order=1,
            title='Ссылки на рисунки',
            content='Используйте перекрёстные ссылки: Вставка → Перекрёстная ссылка → Рисунок. Тогда при добавлении новых рисунков нумерация обновится автоматически.'
        )

        step3 = ModuleStep.objects.create(
            module=task, number=3, order=3,
            title='Описание действий',
            description='''Для каждой функции опишите пошаговые действия:

**Пример: Авторизация в системе**

1. На главном окне нажмите кнопку "Войти" (см. Рисунок 1)
2. В открывшемся окне введите:
   - Id Number (ваш идентификатор)
   - Пароль
3. Введите символы с изображения CAPTCHA
4. При необходимости установите флажок "Запомнить меня"
5. Нажмите кнопку "Войти"

**Возможные ошибки:**
- "Неверный логин или пароль" - проверьте правильность данных
- "Неверная CAPTCHA" - введите символы заново
- "Система заблокирована" - подождите 10 секунд

Используйте нумерованные списки для последовательности действий и маркированные для перечислений.''',
            expected_result='Пошаговые инструкции для всех функций'
        )

        ModuleStep.objects.create(
            module=task, number=4, order=4,
            title='Оформление и сохранение',
            description='''Проверьте оформление документа:

1. **Оглавление:**
   - Ссылки → Оглавление → Автособираемое оглавление
   - Обновите перед сохранением

2. **Нумерация страниц:**
   - Вставка → Номер страницы → Внизу страницы
   - Титульный лист без номера

3. **Стили:**
   - Заголовки используют стили "Заголовок 1", "Заголовок 2"
   - Основной текст - "Обычный"

4. **Проверка:**
   - Орфография (F7)
   - Все ссылки работают
   - Рисунки отображаются

Сохраните: Файл → Сохранить как → Руководство_пользователя_XX.docx''',
            expected_result='Готовое руководство пользователя'
        )

    def _create_task_7_criteria(self, task):
        EvaluationCriteria.objects.create(
            module=task, order=1, max_score=2,
            name='Структура документа',
            description='Титульный лист, оглавление, разделы'
        )
        EvaluationCriteria.objects.create(
            module=task, order=2, max_score=3,
            name='Скриншоты',
            description='Актуальные скриншоты с подписями'
        )
        EvaluationCriteria.objects.create(
            module=task, order=3, max_score=3,
            name='Описание функций',
            description='Пошаговые инструкции для всех функций'
        )
        EvaluationCriteria.objects.create(
            module=task, order=4, max_score=2,
            name='Оформление',
            description='Нумерация, списки, ссылки'
        )
