from rest_framework import serializers
from .models import (
    Section, Module, ModuleFile, ModuleStep,
    StepImage, StepNote, EvaluationCriteria, UserModuleProgress
)


class StepImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = StepImage
        fields = ['id', 'image', 'image_url', 'caption', 'order']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class StepNoteSerializer(serializers.ModelSerializer):
    note_type_display = serializers.CharField(source='get_note_type_display', read_only=True)

    class Meta:
        model = StepNote
        fields = ['id', 'note_type', 'note_type_display', 'title', 'content', 'order']


class ModuleStepSerializer(serializers.ModelSerializer):
    images = StepImageSerializer(many=True, read_only=True)
    notes = StepNoteSerializer(many=True, read_only=True)

    class Meta:
        model = ModuleStep
        fields = ['id', 'number', 'title', 'description', 'expected_result', 'order', 'images', 'notes']


class ModuleFileSerializer(serializers.ModelSerializer):
    file_type_display = serializers.CharField(source='get_file_type_display', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = ModuleFile
        fields = ['id', 'name', 'description', 'file', 'file_url', 'file_type', 'file_type_display', 'file_size', 'order', 'uploaded_at']

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class EvaluationCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EvaluationCriteria
        fields = ['id', 'name', 'description', 'max_score', 'order']


class ModuleListSerializer(serializers.ModelSerializer):
    section_name = serializers.CharField(source='section.name', read_only=True)
    steps_count = serializers.SerializerMethodField()
    files_count = serializers.SerializerMethodField()
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = [
            'id', 'name', 'description', 'section', 'section_name',
            'duration', 'max_score', 'order', 'steps_count', 'files_count',
            'user_progress'
        ]

    def get_steps_count(self, obj):
        return obj.steps.count()

    def get_files_count(self, obj):
        return obj.files.count()

    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            progress = obj.user_progress.filter(user=request.user).first()
            if progress:
                return {
                    'status': progress.status,
                    'current_step': progress.current_step
                }
        return None


class ModuleDetailSerializer(serializers.ModelSerializer):
    section_name = serializers.CharField(source='section.name', read_only=True)
    steps = ModuleStepSerializer(many=True, read_only=True)
    files = ModuleFileSerializer(many=True, read_only=True)
    criteria = EvaluationCriteriaSerializer(many=True, read_only=True)
    total_criteria_score = serializers.ReadOnlyField()
    user_progress = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = [
            'id', 'name', 'description', 'instruction', 'section', 'section_name',
            'duration', 'max_score', 'order', 'total_criteria_score',
            'steps', 'files', 'criteria', 'user_progress',
            'created_at', 'updated_at'
        ]

    def get_user_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            progress = obj.user_progress.filter(user=request.user).first()
            if progress:
                return UserModuleProgressSerializer(progress).data
        return None


class SectionListSerializer(serializers.ModelSerializer):
    modules_count = serializers.ReadOnlyField()

    class Meta:
        model = Section
        fields = ['id', 'name', 'description', 'order', 'modules_count']


class SectionDetailSerializer(serializers.ModelSerializer):
    modules = ModuleListSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'description', 'order', 'modules']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['modules'] = ModuleListSerializer(
            instance.modules.filter(is_active=True),
            many=True,
            context=self.context
        ).data
        return data


class UserModuleProgressSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    module_name = serializers.CharField(source='module.name', read_only=True)

    class Meta:
        model = UserModuleProgress
        fields = [
            'id', 'module', 'module_name', 'status', 'status_display',
            'current_step', 'notes', 'started_at', 'completed_at'
        ]
        read_only_fields = ['started_at', 'completed_at']


class UpdateProgressSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=UserModuleProgress.STATUS_CHOICES, required=False)
    current_step = serializers.IntegerField(required=False, min_value=1)
    notes = serializers.CharField(required=False, allow_blank=True)
