"""Accounts URL configuration."""
from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/student/', views.student_register, name='student_register'),
    path('register/company/', views.company_register, name='company_register'),
    path('profile/', views.profile_view, name='profile'),
    path('notifications/', views.notifications_list, name='notifications'),
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('manage/users/', views.manage_users, name='manage_users'),
    path('manage/users/<int:pk>/toggle/', views.toggle_user_active, name='toggle_user'),
    path('manage/departments/', views.manage_departments, name='manage_departments'),
    path('manage/skills/', views.manage_skills, name='manage_skills'),
    path('manage/announcements/', views.manage_announcements, name='manage_announcements'),
]
