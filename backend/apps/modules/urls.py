from django.urls import path
from .views import (
    SectionListView, SectionDetailView,
    ModuleListView, ModuleDetailView,
    StartModuleView, UpdateProgressView, CompleteModuleView,
    MyModuleProgressView, SectionsWithModulesView
)

urlpatterns = [
    path('sections/', SectionListView.as_view(), name='section-list'),
    path('sections/with-modules/', SectionsWithModulesView.as_view(), name='sections-with-modules'),
    path('sections/<int:pk>/', SectionDetailView.as_view(), name='section-detail'),
    path('', ModuleListView.as_view(), name='module-list'),
    path('<int:pk>/', ModuleDetailView.as_view(), name='module-detail'),
    path('<int:module_id>/start/', StartModuleView.as_view(), name='start-module'),
    path('<int:module_id>/progress/', UpdateProgressView.as_view(), name='update-progress'),
    path('<int:module_id>/complete/', CompleteModuleView.as_view(), name='complete-module'),
    path('my-progress/', MyModuleProgressView.as_view(), name='my-progress'),
]
