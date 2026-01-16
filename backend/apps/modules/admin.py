from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Section, Module, ModuleFile, ModuleStep,
    StepImage, StepNote, EvaluationCriteria, UserModuleProgress
)


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ['name', 'order', 'duration', 'max_score', 'is_active']
    show_change_link = True


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'modules_count_display', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    search_fields = ['name', 'description']
    list_filter = ['is_active']
    inlines = [ModuleInline]

    def modules_count_display(self, obj):
        return obj.modules_count
    modules_count_display.short_description = 'Модулей'


class ModuleFileInline(admin.TabularInline):
    model = ModuleFile
    extra = 1
    fields = ['name', 'file', 'file_type', 'description', 'order']


class StepImageInline(admin.TabularInline):
    model = StepImage
    extra = 1
    fields = ['image', 'caption', 'order', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Превью'


class StepNoteInline(admin.TabularInline):
    model = StepNote
    extra = 1
    fields = ['note_type', 'title', 'content', 'order']


class ModuleStepInline(admin.StackedInline):
    model = ModuleStep
    extra = 1
    fields = ['number', 'title', 'description', 'expected_result', 'order']
    ordering = ['order', 'number']


class EvaluationCriteriaInline(admin.TabularInline):
    model = EvaluationCriteria
    extra = 1
    fields = ['name', 'description', 'max_score', 'order']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'section', 'order', 'duration', 'max_score', 'steps_count', 'files_count', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['section', 'is_active']
    search_fields = ['name', 'description', 'instruction']
    inlines = [ModuleFileInline, ModuleStepInline, EvaluationCriteriaInline]

    fieldsets = (
        ('Основное', {
            'fields': ('section', 'name', 'description', 'order', 'is_active')
        }),
        ('Детали', {
            'fields': ('instruction', 'duration', 'max_score')
        }),
    )

    def steps_count(self, obj):
        return obj.steps.count()
    steps_count.short_description = 'Шагов'

    def files_count(self, obj):
        return obj.files.count()
    files_count.short_description = 'Файлов'


@admin.register(ModuleStep)
class ModuleStepAdmin(admin.ModelAdmin):
    list_display = ['module', 'number', 'title', 'images_count', 'notes_count']
    list_filter = ['module__section', 'module']
    search_fields = ['title', 'description']
    inlines = [StepImageInline, StepNoteInline]

    def images_count(self, obj):
        return obj.images.count()
    images_count.short_description = 'Изображений'

    def notes_count(self, obj):
        return obj.notes.count()
    notes_count.short_description = 'Заметок'


@admin.register(StepImage)
class StepImageAdmin(admin.ModelAdmin):
    list_display = ['step', 'caption', 'order', 'image_preview', 'uploaded_at']
    list_filter = ['step__module__section', 'step__module']
    search_fields = ['caption']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Превью'


@admin.register(StepNote)
class StepNoteAdmin(admin.ModelAdmin):
    list_display = ['step', 'note_type', 'title', 'order']
    list_filter = ['note_type', 'step__module']
    search_fields = ['title', 'content']


@admin.register(ModuleFile)
class ModuleFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'module', 'file_type', 'file_size', 'uploaded_at']
    list_filter = ['file_type', 'module__section', 'module']
    search_fields = ['name', 'description']


@admin.register(EvaluationCriteria)
class EvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ['name', 'module', 'max_score', 'order']
    list_filter = ['module__section', 'module']
    search_fields = ['name', 'description']
    list_editable = ['max_score', 'order']


@admin.register(UserModuleProgress)
class UserModuleProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'module', 'status', 'current_step', 'started_at', 'completed_at']
    list_filter = ['status', 'module__section', 'module']
    search_fields = ['user__username', 'user__email', 'module__name']
    readonly_fields = ['started_at', 'completed_at']
