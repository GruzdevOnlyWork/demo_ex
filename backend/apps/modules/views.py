from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Section, Module, UserModuleProgress
from .serializers import (
    SectionListSerializer, SectionDetailSerializer,
    ModuleListSerializer, ModuleDetailSerializer,
    UserModuleProgressSerializer, UpdateProgressSerializer
)


class SectionListView(generics.ListAPIView):
    queryset = Section.objects.filter(is_active=True)
    serializer_class = SectionListSerializer
    permission_classes = [permissions.IsAuthenticated]


class SectionDetailView(generics.RetrieveAPIView):
    queryset = Section.objects.filter(is_active=True)
    serializer_class = SectionDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class ModuleListView(generics.ListAPIView):
    serializer_class = ModuleListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Module.objects.filter(is_active=True).select_related('section')
        section_id = self.request.query_params.get('section')
        if section_id:
            queryset = queryset.filter(section_id=section_id)
        return queryset


class ModuleDetailView(generics.RetrieveAPIView):
    queryset = Module.objects.filter(is_active=True).prefetch_related(
        'steps__notes', 'steps__images', 'files', 'criteria'
    )
    serializer_class = ModuleDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class StartModuleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, is_active=True)

        progress, created = UserModuleProgress.objects.get_or_create(
            user=request.user,
            module=module,
            defaults={
                'status': 'in_progress',
                'started_at': timezone.now()
            }
        )

        if not created and progress.status == 'not_started':
            progress.status = 'in_progress'
            progress.started_at = timezone.now()
            progress.save()

        return Response(UserModuleProgressSerializer(progress).data)


class UpdateProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, is_active=True)

        progress, created = UserModuleProgress.objects.get_or_create(
            user=request.user,
            module=module
        )

        serializer = UpdateProgressSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        if 'status' in data:
            progress.status = data['status']
            if data['status'] == 'in_progress' and not progress.started_at:
                progress.started_at = timezone.now()
            elif data['status'] == 'completed':
                progress.completed_at = timezone.now()

        if 'current_step' in data:
            progress.current_step = data['current_step']

        if 'notes' in data:
            progress.notes = data['notes']

        progress.save()

        return Response(UserModuleProgressSerializer(progress).data)


class CompleteModuleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, module_id):
        module = get_object_or_404(Module, id=module_id, is_active=True)

        progress, created = UserModuleProgress.objects.get_or_create(
            user=request.user,
            module=module
        )

        progress.status = 'completed'
        progress.completed_at = timezone.now()
        progress.save()

        return Response(UserModuleProgressSerializer(progress).data)


class MyModuleProgressView(generics.ListAPIView):
    serializer_class = UserModuleProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserModuleProgress.objects.filter(
            user=self.request.user
        ).select_related('module')


class SectionsWithModulesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sections = Section.objects.filter(is_active=True).prefetch_related('modules')

        data = []
        for section in sections:
            section_data = SectionListSerializer(section).data
            section_data['modules'] = ModuleListSerializer(
                section.modules.filter(is_active=True),
                many=True,
                context={'request': request}
            ).data
            data.append(section_data)

        return Response(data)
