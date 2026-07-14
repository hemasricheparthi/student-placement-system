"""
Authentication and user management views.
"""
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy

from accounts.decorators import admin_required, get_dashboard_url, placement_officer_required
from accounts.forms import (
    AnnouncementForm,
    CompanyRegistrationForm,
    CustomLoginForm,
    DepartmentForm,
    ProfileUpdateForm,
    SkillForm,
    StudentRegistrationForm,
)
from accounts.models import Announcement, CustomUser, Department, Notification, Skill


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return get_dashboard_url(self.request.user)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'


def home_redirect(request):
    """Redirect to appropriate page based on auth status."""
    if request.user.is_authenticated:
        return redirect(get_dashboard_url(request.user))
    return redirect('dashboard:home')


def student_register(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_url(request.user))
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('accounts:login')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/student_register.html', {'form': form})


def company_register(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_url(request.user))
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company registered! Awaiting verification. Please login.')
            return redirect('accounts:login')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'accounts/company_register.html', {'form': form})


def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})


def notifications_list(request):
    notifications_qs = request.user.notifications.all()
    notifications_qs.filter(is_read=False).update(is_read=True)
    return render(request, 'accounts/notifications.html', {
        'notifications': notifications_qs,
    })


@admin_required
def manage_users(request):
    users = CustomUser.objects.all()
    role = request.GET.get('role')
    search = request.GET.get('search')
    if role:
        users = users.filter(role=role)
    if search:
        users = users.filter(username__icontains=search) | users.filter(email__icontains=search)
    return render(request, 'accounts/manage_users.html', {'users': users})


@admin_required
def toggle_user_active(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if user != request.user:
        user.is_active = not user.is_active
        user.save()
        messages.success(request, f'User {user.username} {"activated" if user.is_active else "deactivated"}.')
    return redirect('accounts:manage_users')


@admin_required
def manage_departments(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added.')
            return redirect('accounts:manage_departments')
    else:
        form = DepartmentForm()
    departments = Department.objects.all()
    return render(request, 'accounts/manage_departments.html', {
        'form': form, 'departments': departments,
    })


@admin_required
def manage_skills(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill added.')
            return redirect('accounts:manage_skills')
    else:
        form = SkillForm()
    skills = Skill.objects.all()
    return render(request, 'accounts/manage_skills.html', {'form': form, 'skills': skills})


@placement_officer_required
def manage_announcements(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.created_by = request.user
            announcement.save()
            messages.success(request, 'Announcement published.')
            return redirect('accounts:manage_announcements')
    else:
        form = AnnouncementForm()
    announcements = Announcement.objects.all()
    return render(request, 'accounts/manage_announcements.html', {
        'form': form, 'announcements': announcements,
    })


def create_notification(user, title, message, notification_type='INFO', link=''):
    """Helper to create notifications."""
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        notification_type=notification_type,
        link=link,
    )
