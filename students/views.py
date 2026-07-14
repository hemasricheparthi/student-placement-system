"""Student views."""
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import placement_officer_required, student_required
from accounts.views import create_notification
from jobs.resume_matcher import extract_skills_from_text, extract_text_from_pdf
from students.forms import (
    CertificationForm,
    ProjectForm,
    ResumeUploadForm,
    StudentProfileForm,
    StudentSearchForm,
)
from students.models import Certification, Project, Resume, StudentProfile


@student_required
def student_dashboard_data(request):
    """Redirect handled by dashboard app."""
    return redirect('dashboard:student_dashboard')


@student_required
def profile_edit(request):
    profile = request.user.student_profile
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('students:profile')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'students/profile.html', {
        'form': form,
        'profile': profile,
        'certifications': profile.certifications.all(),
        'projects': profile.projects.all(),
        'resumes': profile.resumes.all(),
    })


@student_required
def add_certification(request):
    profile = request.user.student_profile
    if request.method == 'POST':
        form = CertificationForm(request.POST)
        if form.is_valid():
            cert = form.save(commit=False)
            cert.student = profile
            cert.save()
            messages.success(request, 'Certification added.')
            return redirect('students:profile')
    else:
        form = CertificationForm()
    return render(request, 'students/add_certification.html', {'form': form})


@student_required
def add_project(request):
    profile = request.user.student_profile
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = profile
            project.save()
            messages.success(request, 'Project added.')
            return redirect('students:profile')
    else:
        form = ProjectForm()
    return render(request, 'students/add_project.html', {'form': form})


@student_required
def upload_resume(request):
    profile = request.user.student_profile
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Deactivate previous resumes
            profile.resumes.update(is_active=False)
            resume = form.save(commit=False)
            resume.student = profile
            resume.is_active = True

            # Extract text and skills from PDF
            if resume.file:
                text = extract_text_from_pdf(resume.file.path)
                resume.extracted_text = text
                from accounts.models import Skill
                known_skills = list(Skill.objects.values_list('name', flat=True))
                profile_skill_names = list(profile.skills.values_list('name', flat=True))
                all_skills = known_skills + profile_skill_names
                resume.extracted_skills = extract_skills_from_text(text, set(all_skills))
            resume.save()
            messages.success(request, 'Resume uploaded and analyzed successfully.')
            return redirect('students:profile')
    else:
        form = ResumeUploadForm()
    return render(request, 'students/upload_resume.html', {'form': form})


@student_required
def placement_statistics(request):
    profile = request.user.student_profile
    applications = profile.applications.all()
    stats = {
        'total_applications': applications.count(),
        'shortlisted': applications.filter(status='SHORTLISTED').count(),
        'interviews': applications.filter(status='INTERVIEW_SCHEDULED').count(),
        'offers': applications.filter(status__in=['OFFERED', 'OFFER_ACCEPTED']).count(),
        'placed': profile.placement_status == 'PLACED',
    }
    return render(request, 'students/placement_statistics.html', {
        'stats': stats,
        'applications': applications,
        'profile': profile,
    })


@placement_officer_required
def student_list(request):
    form = StudentSearchForm(request.GET)
    students = StudentProfile.objects.select_related('user', 'department').all()

    if form.is_valid():
        search = form.cleaned_data.get('search')
        department = form.cleaned_data.get('department')
        min_cgpa = form.cleaned_data.get('min_cgpa')
        skill = form.cleaned_data.get('skill')
        status = form.cleaned_data.get('placement_status')

        if search:
            students = students.filter(
                Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
                | Q(enrollment_no__icontains=search)
            )
        if department:
            students = students.filter(department=department)
        if min_cgpa:
            students = students.filter(cgpa__gte=min_cgpa)
        if skill:
            students = students.filter(skills=skill)
        if status:
            students = students.filter(placement_status=status)

    paginator = Paginator(students, 10)
    page = request.GET.get('page')
    students_page = paginator.get_page(page)

    return render(request, 'students/student_list.html', {
        'students': students_page,
        'form': form,
    })


@placement_officer_required
def verify_student(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    student.is_profile_verified = not student.is_profile_verified
    student.save()
    status = 'verified' if student.is_profile_verified else 'unverified'
    messages.success(request, f'Student profile {status}.')
    create_notification(
        student.user,
        'Profile Verification Update',
        f'Your profile has been {status} by the placement officer.',
        'INFO',
    )
    return redirect('students:student_list')


@placement_officer_required
def student_detail(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})
