"""Dashboard URL configuration."""
from django.urls import path

from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('redirect/', views.dashboard_redirect, name='redirect'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('officer/', views.officer_dashboard, name='officer_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('company/', views.company_dashboard, name='company_dashboard'),
]
