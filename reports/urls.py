"""Reports URL configuration."""
from django.urls import path

from reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_home, name='reports_home'),
    path('placement/', views.placement_report, name='placement_report'),
    path('applications/', views.application_report, name='application_report'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('export/students/', views.export_students_csv, name='export_students'),
    path('export/applications/', views.export_applications_csv, name='export_applications'),
    path('export/placement/', views.export_placement_csv, name='export_placement'),
]
