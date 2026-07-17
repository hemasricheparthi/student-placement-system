"""Job and application views."""
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.decorators import company_required, student_required
from accounts.models import Skill
from accounts.views import create_notification
from jobs.forms import ApplicationForm, JobForm, JobSearchForm
from jobs.models import Application, Job
from jobs.resume_matcher import process_resume_match
from students.models import Resume


def job_list(request):
    """Public job listings with search and filters."""
    form = JobSearchForm(request.GET)
    jobs = Job.objects.filter(status='OPEN').select_related('company')

    if form.is_valid():
        search = form.cleaned_data.get('search')
        company = form.cleaned_data.get('company')
        min_cgpa = form.cleaned_data.get('min_cgpa')
        skill = form.cleaned_data.get('skill')
        job_type = form.cleaned_data.get('job_type')

        if search:
            jobs = jobs.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        if company:
            jobs = jobs.filter(company__company_name__icontains=company)
        if min_cgpa:
            jobs = jobs.filter(min_cgpa__lte=min_cgpa)
        if skill:
            jobs = jobs.filter(required_skills=skill)
        if job_type:
            jobs = jobs.filter(job_type=job_type)

    paginator = Paginator(jobs, 10)
    page = request.GET.get('page')
    jobs_page = paginator.get_page(page)

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs_page,
        'form': form,
    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False
    application = None
    if request.user.is_authenticated and request.user.is_student:
        application = Application.objects.filter(
            student=request.user.student_profile, job=job
        ).first()
        has_applied = application is not None

    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'has_applied': has_applied,
        'application': application,
    })


@student_required
def eligible_jobs(request):
    """Show jobs the student is eligible for."""
    profile = request.user.student_profile
    jobs = Job.objects.filter(
        status='OPEN',
        last_date_to_apply__gte=timezone.now().date(),
        min_cgpa__lte=profile.cgpa,
        max_backlogs__gte=profile.backlogs,
    ).select_related('company')

    if profile.department:
        jobs = jobs.filter(
            Q(eligible_departments=profile.department) | Q(eligible_departments__isnull=True)
        ).distinct()

    applied_job_ids = profile.applications.values_list('job_id', flat=True)

    return render(request, 'jobs/eligible_jobs.html', {
        'jobs': jobs,
        'applied_job_ids': list(applied_job_ids),
        'profile': profile,
    })


@student_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk, status='OPEN')
    profile = request.user.student_profile

    if not job.is_open:
        messages.error(request, 'The application deadline for this job has passed.')
        return redirect('jobs:job_detail', pk=pk)


    if Application.objects.filter(student=profile, job=job).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('jobs:job_detail', pk=pk)

    # Check eligibility
    if profile.cgpa < job.min_cgpa:
        messages.error(request, f'Minimum CGPA required: {job.min_cgpa}')
        return redirect('jobs:job_detail', pk=pk)
    if profile.backlogs > job.max_backlogs:
        messages.error(request, f'Maximum backlogs allowed: {job.max_backlogs}')
        return redirect('jobs:job_detail', pk=pk)

    active_resume = profile.resumes.filter(is_active=True).first()
    if not active_resume:
        messages.error(request, 'Please upload a resume before applying.')
        return redirect('students:upload_resume')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            # Smart Resume Match
            known_skills = list(Skill.objects.values_list('name', flat=True))
            profile_skills = list(profile.skills.values_list('name', flat=True))
            all_skills = known_skills + profile_skills

            match_data = process_resume_match(
                active_resume.file.path, job, all_skills
            )

            application = form.save(commit=False)
            application.student = profile
            application.job = job
            application.resume = active_resume
            application.match_percentage = match_data['match_percentage']
            application.matched_skills = match_data['matched_skills']
            application.missing_skills = match_data['missing_skills']
            application.suggested_skills = match_data['suggested_skills']
            application.save()

            profile.placement_status = 'APPLIED'
            profile.save()

            create_notification(
                job.company.user,
                'New Application',
                f'{profile.full_name} applied for {job.title} (Match: {match_data["match_percentage"]}%)',
                'APPLICATION',
                f'/jobs/{job.pk}/applicants/',
            )
            messages.success(
                request,
                f'Application submitted! Resume Match: {match_data["match_percentage"]}%'
            )
            return redirect('jobs:my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})


@student_required
def my_applications(request):
    profile = request.user.student_profile
    applications = profile.applications.select_related('job', 'job__company').all()
    paginator = Paginator(applications, 10)
    page = request.GET.get('page')
    apps_page = paginator.get_page(page)
    return render(request, 'jobs/my_applications.html', {'applications': apps_page})


@company_required
def manage_jobs(request):
    company = request.user.company_profile
    jobs = company.jobs.all()
    return render(request, 'jobs/manage_jobs.html', {'jobs': jobs})


@company_required
def create_job(request):
    company = request.user.company_profile
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            form.save_m2m()
            messages.success(request, 'Job posted successfully.')
            return redirect('jobs:manage_jobs')
    else:
        form = JobForm()
    return render(request, 'jobs/create_job.html', {'form': form})


@company_required
def edit_job(request, pk):
    company = request.user.company_profile
    job = get_object_or_404(Job, pk=pk, company=company)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated.')
            return redirect('jobs:manage_jobs')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/edit_job.html', {'form': form, 'job': job})


@company_required
def delete_job(request, pk):
    company = request.user.company_profile
    job = get_object_or_404(Job, pk=pk, company=company)
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job deleted.')
        return redirect('jobs:manage_jobs')
    return render(request, 'jobs/delete_job.html', {'job': job})


@company_required
def view_applicants(request, pk):
    company = request.user.company_profile
    job = get_object_or_404(Job, pk=pk, company=company)
    applications = job.applications.select_related('student', 'student__user').order_by('-match_percentage')
    return render(request, 'jobs/applicants.html', {
        'job': job,
        'applications': applications,
    })


@company_required
def shortlist_candidate(request, pk):
    application = get_object_or_404(
        Application, pk=pk, job__company=request.user.company_profile
    )
    application.status = 'SHORTLISTED'
    application.save()
    application.student.placement_status = 'SHORTLISTED'
    application.student.save()
    create_notification(
        application.student.user,
        'Shortlisted!',
        f'You have been shortlisted for {application.job.title}.',
        'SUCCESS',
    )
    messages.success(request, 'Candidate shortlisted.')
    return redirect('jobs:view_applicants', pk=application.job.pk)


@company_required
def reject_candidate(request, pk):
    application = get_object_or_404(
        Application, pk=pk, job__company=request.user.company_profile
    )
    application.status = 'REJECTED'
    application.save()
    create_notification(
        application.student.user,
        'Application Update',
        f'Your application for {application.job.title} was not selected.',
        'WARNING',
    )
    messages.info(request, 'Candidate rejected.')
    return redirect('jobs:view_applicants', pk=application.job.pk)


@company_required
def select_candidate(request, pk):
    application = get_object_or_404(
        Application, pk=pk, job__company=request.user.company_profile
    )
    application.status = 'SELECTED'
    application.save()
    create_notification(
        application.student.user,
        'Selected!',
        f'Congratulations! You have been selected for {application.job.title}.',
        'SUCCESS',
    )
    messages.success(request, 'Candidate selected.')
    return redirect('jobs:view_applicants', pk=application.job.pk)
