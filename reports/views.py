"""
Reports and CSV export views.
"""
import csv

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render

from accounts.decorators import admin_required, placement_officer_required
from jobs.models import Application, Job
from placement.models import PlacementDrive
from students.models import StudentProfile


@placement_officer_required
def reports_home(request):
    return render(request, 'reports/reports_home.html')


@placement_officer_required
def placement_report(request):
    students = StudentProfile.objects.select_related('user', 'department').all()
    placed = students.filter(placement_status='PLACED').count()
    total = students.count()
    dept_breakdown = {}
    for student in students:
        dept = student.department.name if student.department else 'Unknown'
        if dept not in dept_breakdown:
            dept_breakdown[dept] = {'total': 0, 'placed': 0}
        dept_breakdown[dept]['total'] += 1
        if student.placement_status == 'PLACED':
            dept_breakdown[dept]['placed'] += 1

    return render(request, 'reports/placement_report.html', {
        'students': students,
        'placed_count': placed,
        'total_count': total,
        'placement_rate': round(placed / total * 100, 1) if total else 0,
        'dept_breakdown': dept_breakdown,
    })


@placement_officer_required
def application_report(request):
    applications = Application.objects.select_related(
        'student', 'student__user', 'job', 'job__company'
    ).all()
    status_counts = {}
    for app in applications:
        status_counts[app.status] = status_counts.get(app.status, 0) + 1

    return render(request, 'reports/application_report.html', {
        'applications': applications,
        'status_counts': status_counts,
        'total': applications.count(),
    })


@placement_officer_required
def export_students_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students_report.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Enrollment No', 'Name', 'Department', 'CGPA', 'Backlogs',
        'Placement Status', 'Verified', 'Email',
    ])
    for student in StudentProfile.objects.select_related('user', 'department'):
        writer.writerow([
            student.enrollment_no,
            student.full_name,
            student.department.name if student.department else '',
            student.cgpa,
            student.backlogs,
            student.get_placement_status_display(),
            'Yes' if student.is_profile_verified else 'No',
            student.user.email,
        ])
    return response


@placement_officer_required
def export_applications_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="applications_report.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Student', 'Enrollment', 'Job', 'Company', 'Status',
        'Match %', 'Applied Date',
    ])
    for app in Application.objects.select_related('student', 'job', 'job__company'):
        writer.writerow([
            app.student.full_name,
            app.student.enrollment_no,
            app.job.title,
            app.job.company.company_name,
            app.get_status_display(),
            app.match_percentage,
            app.applied_at.strftime('%Y-%m-%d'),
        ])
    return response


@placement_officer_required
def export_placement_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="placement_report.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Enrollment No', 'Name', 'Department', 'CGPA', 'Placement Status',
        'Company', 'Package',
    ])
    for student in StudentProfile.objects.select_related('user', 'department'):
        placed_app = student.applications.filter(status='OFFER_ACCEPTED').first()
        company = placed_app.job.company.company_name if placed_app else ''
        package = placed_app.offer_letter.package_offered if placed_app and hasattr(placed_app, 'offer_letter') else ''
        writer.writerow([
            student.enrollment_no,
            student.full_name,
            student.department.name if student.department else '',
            student.cgpa,
            student.get_placement_status_display(),
            company,
            package,
        ])
    return response


@admin_required
def analytics_view(request):
    from dashboard.views import get_dashboard_stats
    stats = get_dashboard_stats()
    jobs_by_company = (
        Job.objects.values('company__company_name')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )
    return render(request, 'reports/analytics.html', {
        'stats': stats,
        'jobs_by_company': list(jobs_by_company),
    })
