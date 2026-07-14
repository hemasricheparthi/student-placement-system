"""Companies URL configuration."""
from django.urls import path

from companies import views

app_name = 'companies'

urlpatterns = [
    path('', views.company_list, name='company_list'),
    path('profile/', views.company_profile, name='profile'),
    path('manage/', views.manage_companies, name='manage_companies'),
    path('<int:pk>/', views.company_detail, name='company_detail'),
    path('<int:pk>/verify/', views.verify_company, name='verify_company'),
]
