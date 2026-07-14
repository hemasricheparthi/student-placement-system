"""Placement URL configuration."""
from django.urls import path

from placement import views

app_name = 'placement'

urlpatterns = [
    path('drives/', views.manage_drives, name='manage_drives'),
    path('drives/create/', views.create_drive, name='create_drive'),
    path('drives/<int:pk>/edit/', views.edit_drive, name='edit_drive'),
    path('interviews/', views.interview_schedule, name='interview_schedule'),
    path('interview/<int:pk>/feedback/', views.interview_feedback, name='interview_feedback'),
    path('interview/schedule/<int:application_pk>/', views.schedule_interview, name='schedule_interview'),
    path('offer/create/<int:application_pk>/', views.create_offer, name='create_offer'),
    path('offer/<int:pk>/respond/', views.respond_offer, name='respond_offer'),
    path('offer/<int:pk>/download/', views.download_offer, name='download_offer'),
]
