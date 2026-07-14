"""Jobs URL configuration."""
from django.urls import path

from jobs import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('eligible/', views.eligible_jobs, name='eligible_jobs'),
    path('manage/', views.manage_jobs, name='manage_jobs'),
    path('create/', views.create_job, name='create_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('<int:pk>/applicants/', views.view_applicants, name='view_applicants'),
    path('application/<int:pk>/shortlist/', views.shortlist_candidate, name='shortlist'),
    path('application/<int:pk>/reject/', views.reject_candidate, name='reject'),
    path('application/<int:pk>/select/', views.select_candidate, name='select'),
]
