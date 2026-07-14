"""Students URL configuration."""
from django.urls import path

from students import views

app_name = 'students'

urlpatterns = [
    path('profile/', views.profile_edit, name='profile'),
    path('certification/add/', views.add_certification, name='add_certification'),
    path('project/add/', views.add_project, name='add_project'),
    path('resume/upload/', views.upload_resume, name='upload_resume'),
    path('statistics/', views.placement_statistics, name='placement_statistics'),
    path('list/', views.student_list, name='student_list'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('<int:pk>/verify/', views.verify_student, name='verify_student'),
]
