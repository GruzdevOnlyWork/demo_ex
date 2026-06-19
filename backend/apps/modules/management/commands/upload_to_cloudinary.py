from django.core.management.base import BaseCommand
from django.core.files import File
from apps.modules.models import ExamVariant, ModuleFile
import os


class Command(BaseCommand):
    help = 'Перезагрузка PDF файлов в Cloudinary'

    def handle(self, *args, **options):
        self.stdout.write('Проверка настроек Cloudinary...')

        cloudinary_url = os.getenv('CLOUDINARY_URL')
        if not cloudinary_url:
            self.stdout.write(self.style.ERROR(
                'CLOUDINARY_URL не настроен! Добавьте переменную окружения.'
            ))
            return

        self.stdout.write(self.style.SUCCESS('Cloudinary настроен корректно'))

        self.stdout.write('\nОбработка вариантов экзаменов...')
        variants = ExamVariant.objects.all()

        for variant in variants:
            self.stdout.write(f'  Вариант: {variant}')

            if variant.description_file:
                try:
                    old_name = variant.description_file.name
                    self.stdout.write(f'    description_file: {old_name}')

                    url = variant.description_file.url
                    if url.startswith('http') and 'cloudinary' in url:
                        self.stdout.write(self.style.SUCCESS(f'      Уже в Cloudinary: {url[:80]}...'))
                    else:
                        self.stdout.write(f'      URL: {url}')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'      Ошибка: {e}'))

            if variant.task_file:
                try:
                    old_name = variant.task_file.name
                    self.stdout.write(f'    task_file: {old_name}')

                    url = variant.task_file.url
                    if url.startswith('http') and 'cloudinary' in url:
                        self.stdout.write(self.style.SUCCESS(f'      Уже в Cloudinary: {url[:80]}...'))
                    else:
                        self.stdout.write(f'      URL: {url}')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'      Ошибка: {e}'))

        self.stdout.write('\nОбработка файлов модулей...')
        module_files = ModuleFile.objects.all()

        for mf in module_files:
            try:
                url = mf.file.url
                status = 'Cloudinary' if ('cloudinary' in url) else 'Локальный'
                self.stdout.write(f'  {mf.name}: {status}')
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  {mf.name}: Ошибка - {e}'))

        self.stdout.write(self.style.SUCCESS('\nПроверка завершена!'))
        self.stdout.write('\nЕсли файлы отображаются как "Локальный", выполните:')
        self.stdout.write('  python manage.py load_exam_variant7 --resources-path=/path/to/resources')
