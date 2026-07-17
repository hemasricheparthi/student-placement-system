"""
Dashboard views with statistics and Chart.js data.
"""
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import redirect, render
from django.utils import timezone
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

from accounts.decorators import (
    admin_required,
    company_required,
    get_dashboard_url,
    placement_officer_required,
    student_required,
)
from accounts.models import Announcement, CustomUser, Department
from companies.models import CompanyProfile
from jobs.models import Application, Job
from placement.models import Interview, PlacementDrive
from students.models import StudentProfile


def get_dashboard_stats():
    """Aggregate statistics for dashboards."""
    total_students = StudentProfile.objects.count()
    placed_students = StudentProfile.objects.filter(placement_status='PLACED').count()
    unplaced_students = total_students - placed_students
    placement_percentage = (placed_students / total_students * 100) if total_students else 0

    return {
        'total_students': total_students,
        'total_companies': CompanyProfile.objects.filter(is_verified=True).count(),
        'total_jobs': Job.objects.filter(status='OPEN').count(),
        'total_applications': Application.objects.count(),
        'placement_percentage': round(placement_percentage, 1),
        'students_placed': placed_students,
        'students_unplaced': unplaced_students,
        'upcoming_drives': PlacementDrive.objects.filter(
            status='UPCOMING', drive_date__gte=timezone.now().date()
        ).count(),
    }


def home(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_url(request.user))
    return redirect('accounts:login')

def about(request):
    return render(request, 'dashboard/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_body = request.POST.get('message', '').strip()

        if name and email and subject and message_body:
            try:
                send_mail(
                    subject=f'[Placement Portal Contact] {subject}',
                    message=f'From: {name} <{email}>\n\n{message_body}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_RECEIVER_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
            except Exception:
                messages.error(request, 'Sorry, something went wrong while sending your message. Please try again later or email us directly.')
        else:
            messages.error(request, 'Please fill in all fields.')

        return redirect('dashboard:contact')

    return render(request, 'dashboard/contact.html')


@login_required
def dashboard_redirect(request):
    return redirect(get_dashboard_url(request.user))


@admin_required
def admin_dashboard(request):
    stats = get_dashboard_stats()
    dept_stats = (
        StudentProfile.objects
        .values('department__name')
        .annotate(count=Count('id'), placed=Count('id', filter=Q(placement_status='PLACED')))
        .order_by('-count')[:10]
    )
    monthly_apps = (
        Application.objects
        .extra(select={'month': "strftime('%%Y-%%m', applied_at)"})
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')[:12]
    )
    recent_users = CustomUser.objects.order_by('-created_at')[:10]
    return render(request, 'dashboard/admin_dashboard.html', {
        'stats': stats,
        'dept_stats': json.dumps(list(dept_stats)),
        'monthly_apps': json.dumps(list(monthly_apps)),
        'recent_users': recent_users,
    })


@placement_officer_required
def officer_dashboard(request):
    stats = get_dashboard_stats()
    pending_verifications = StudentProfile.objects.filter(is_profile_verified=False).count()
    pending_companies = CompanyProfile.objects.filter(is_verified=False).count()
    upcoming_drives = PlacementDrive.objects.filter(status='UPCOMING')[:5]
    recent_applications = Application.objects.select_related(
        'student', 'job', 'job__company'
    ).order_by('-applied_at')[:10]
    return render(request, 'dashboard/officer_dashboard.html', {
        'stats': stats,
        'pending_verifications': pending_verifications,
        'pending_companies': pending_companies,
        'upcoming_drives': upcoming_drives,
        'recent_applications': recent_applications,
    })


@student_required
def student_dashboard(request):
    profile = request.user.student_profile
    applications = profile.applications.select_related('job', 'job__company').order_by('-applied_at')[:5]
    upcoming_interviews = Interview.objects.filter(
        application__student=profile,
        status='SCHEDULED',
        scheduled_date__gte=timezone.now(),
    ).select_related('application__job')[:5]
    eligible_count = Job.objects.filter(
        status='OPEN', min_cgpa__lte=profile.cgpa
    ).count()
    return render(request, 'dashboard/student_dashboard.html', {
        'profile': profile,
        'applications': applications,
        'upcoming_interviews': upcoming_interviews,
        'eligible_count': eligible_count,
    })


@company_required
def company_dashboard(request):
    company = request.user.company_profile
    jobs = company.jobs.all()
    total_applicants = Application.objects.filter(job__company=company).count()
    recent_applications = Application.objects.filter(
        job__company=company
    ).select_related('student', 'job').order_by('-applied_at')[:10]
    return render(request, 'dashboard/company_dashboard.html', {
        'company': company,
        'jobs': jobs,
        'total_applicants': total_applicants,
        'recent_applications': recent_applications,
        'open_jobs': jobs.filter(status='OPEN').count(),
    })
