from django.core.management.base import BaseCommand
from apps.modules.models import (
    ExamVariant, Section, Module, ModuleFile,
    ModuleStep, StepImage, StepNote, EvaluationCriteria,
    UsefulLink, UserModuleProgress
)
from apps.exams.models import Category, Question, Answer, Test, TestAttempt, UserAnswer


class Command(BaseCommand):
    help = 'Удаление всех тестовых данных (варианты, модули, вопросы, тесты)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--yes',
            action='store_true',
            help='Пропустить подтверждение'
        )
        parser.add_argument(
            '--keep-tests',
            action='store_true',
            help='Не удалять тесты, вопросы и ответы (Category, Question, Answer, Test)'
        )

    def handle(self, *args, **options):
        keep_tests = options['keep_tests']

        if not options['yes']:
            scope = 'варианты экзаменов и модули (тесты сохранены)' if keep_tests else 'ВСЕ варианты, модули, тесты и вопросы'
            self.stdout.write(self.style.WARNING(
                f'ВНИМАНИЕ: Это удалит {scope}!'
            ))
            confirm = input('Введите "yes" для подтверждения: ')
            if confirm.lower() != 'yes':
                self.stdout.write('Отменено.')
                return

        self.stdout.write('Удаление данных...')

        counts = {}

        if not keep_tests:
            counts.update({
                'UserAnswer': UserAnswer.objects.count(),
                'TestAttempt': TestAttempt.objects.count(),
                'Test': Test.objects.count(),
                'Answer': Answer.objects.count(),
                'Question': Question.objects.count(),
                'Category': Category.objects.count(),
            })

        counts.update({
            'UserModuleProgress': UserModuleProgress.objects.count(),
            'UsefulLink': UsefulLink.objects.count(),
            'EvaluationCriteria': EvaluationCriteria.objects.count(),
            'StepNote': StepNote.objects.count(),
            'StepImage': StepImage.objects.count(),
            'ModuleStep': ModuleStep.objects.count(),
            'ModuleFile': ModuleFile.objects.count(),
            'Module': Module.objects.count(),
            'Section': Section.objects.count(),
            'ExamVariant': ExamVariant.objects.count(),
        })

        if not keep_tests:
            UserAnswer.objects.all().delete()
            TestAttempt.objects.all().delete()
            Test.objects.all().delete()
            Answer.objects.all().delete()
            Question.objects.all().delete()
            Category.objects.all().delete()

        UserModuleProgress.objects.all().delete()
        UsefulLink.objects.all().delete()
        EvaluationCriteria.objects.all().delete()
        StepNote.objects.all().delete()
        StepImage.objects.all().delete()
        ModuleStep.objects.all().delete()
        ModuleFile.objects.all().delete()
        Module.objects.all().delete()
        Section.objects.all().delete()
        ExamVariant.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Удалено:'))
        for model, count in counts.items():
            if count > 0:
                self.stdout.write(f'  {model}: {count}')

        if keep_tests:
            self.stdout.write(self.style.WARNING('Тесты, вопросы и ответы сохранены (--keep-tests).'))
        self.stdout.write(self.style.SUCCESS('База данных очищена. Пользователи сохранены.'))
