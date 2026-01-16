from django.db import models
from django.conf import settings


class Section(models.Model):
    name = models.CharField('Название раздела', max_length=200)
    description = models.TextField('Описание', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def modules_count(self):
        return self.modules.filter(is_active=True).count()


class Module(models.Model):
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='modules',
        verbose_name='Раздел'
    )
    name = models.CharField('Название модуля', max_length=200)
    description = models.TextField('Описание', blank=True)
    instruction = models.TextField('Общая инструкция', blank=True, help_text='Общее описание задания модуля')
    duration = models.CharField('Рекомендуемое время', max_length=50, blank=True, help_text='Например: 2 часа')
    max_score = models.PositiveIntegerField('Максимальный балл', default=100)
    order = models.PositiveIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активен', default=True)
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['section', 'order', 'name']

    def __str__(self):
        return f"{self.section.name} - {self.name}"

    @property
    def total_criteria_score(self):
        return sum(c.max_score for c in self.criteria.all())


class ModuleFile(models.Model):
    FILE_TYPES = [
        ('document', 'Документ'),
        ('image', 'Изображение'),
        ('archive', 'Архив'),
        ('video', 'Видео'),
        ('other', 'Другое'),
    ]

    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name='Модуль'
    )
    name = models.CharField('Название файла', max_length=200)
    description = models.TextField('Описание', blank=True)
    file = models.FileField('Файл', upload_to='modules/files/')
    file_type = models.CharField('Тип файла', max_length=20, choices=FILE_TYPES, default='document')
    order = models.PositiveIntegerField('Порядок', default=0)
    uploaded_at = models.DateTimeField('Загружен', auto_now_add=True)

    class Meta:
        verbose_name = 'Файл модуля'
        verbose_name_plural = 'Файлы модулей'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    @property
    def file_size(self):
        try:
            size = self.file.size
            for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} ТБ"
        except:
            return "Неизвестно"


class ModuleStep(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='steps',
        verbose_name='Модуль'
    )
    number = models.PositiveIntegerField('Номер шага')
    title = models.CharField('Заголовок шага', max_length=300)
    description = models.TextField('Описание шага', help_text='Подробное описание того, что нужно сделать')
    expected_result = models.TextField('Ожидаемый результат', blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Шаг модуля'
        verbose_name_plural = 'Шаги модулей'
        ordering = ['module', 'order', 'number']
        unique_together = ['module', 'number']

    def __str__(self):
        return f"Шаг {self.number}: {self.title}"


class StepImage(models.Model):
    step = models.ForeignKey(
        'ModuleStep',
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Шаг'
    )
    image = models.ImageField('Изображение', upload_to='modules/steps/')
    caption = models.CharField('Подпись', max_length=300, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    uploaded_at = models.DateTimeField('Загружено', auto_now_add=True)

    class Meta:
        verbose_name = 'Изображение шага'
        verbose_name_plural = 'Изображения шагов'
        ordering = ['order']

    def __str__(self):
        return f"Изображение для: {self.step.title[:30]}"


class StepNote(models.Model):
    NOTE_TYPES = [
        ('info', 'Информация'),
        ('warning', 'Предупреждение'),
        ('tip', 'Совет'),
        ('important', 'Важно'),
        ('example', 'Пример'),
    ]

    step = models.ForeignKey(
        ModuleStep,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Шаг'
    )
    note_type = models.CharField('Тип заметки', max_length=20, choices=NOTE_TYPES, default='info')
    title = models.CharField('Заголовок', max_length=200, blank=True)
    content = models.TextField('Содержание')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Заметка к шагу'
        verbose_name_plural = 'Заметки к шагам'
        ordering = ['order']

    def __str__(self):
        return f"{self.get_note_type_display()}: {self.title or self.content[:50]}"


class EvaluationCriteria(models.Model):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='criteria',
        verbose_name='Модуль'
    )
    name = models.CharField('Название критерия', max_length=300)
    description = models.TextField('Описание критерия', blank=True)
    max_score = models.PositiveIntegerField('Максимальный балл')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Критерий оценивания'
        verbose_name_plural = 'Критерии оценивания'
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.max_score} балл.)"


class UserModuleProgress(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Не начат'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершен'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='module_progress',
        verbose_name='Пользователь'
    )
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='user_progress',
        verbose_name='Модуль'
    )
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='not_started')
    current_step = models.PositiveIntegerField('Текущий шаг', default=1)
    notes = models.TextField('Личные заметки', blank=True)
    started_at = models.DateTimeField('Начат', null=True, blank=True)
    completed_at = models.DateTimeField('Завершен', null=True, blank=True)

    class Meta:
        verbose_name = 'Прогресс по модулю'
        verbose_name_plural = 'Прогресс по модулям'
        unique_together = ['user', 'module']

    def __str__(self):
        return f"{self.user.username} - {self.module.name} ({self.get_status_display()})"
