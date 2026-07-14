"""Placement drive, interview, and offer views."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import company_required, placement_officer_required, student_required
from accounts.views import create_notification
from jobs.models import Application
from placement.forms import InterviewFeedbackForm, InterviewForm, OfferLetterForm, PlacementDriveForm
from placement.models import Interview, OfferLetter, PlacementDrive


@placement_officer_required
def manage_drives(request):
    drives = PlacementDrive.objects.all()
    return render(request, 'placement/manage_drives.html', {'drives': drives})


@placement_officer_required
def create_drive(request):
    if request.method == 'POST':
        form = PlacementDriveForm(request.POST)
        if form.is_valid():
            drive = form.save(commit=False)
            drive.created_by = request.user
            drive.save()
            form.save_m2m()
            messages.success(request, 'Placement drive created.')
            return redirect('placement:manage_drives')
    else:
        form = PlacementDriveForm()
    return render(request, 'placement/create_drive.html', {'form': form})


@placement_officer_required
def edit_drive(request, pk):
    drive = get_object_or_404(PlacementDrive, pk=pk)
    if request.method == 'POST':
        form = PlacementDriveForm(request.POST, instance=drive)
        if form.is_valid():
            form.save()
            messages.success(request, 'Drive updated.')
            return redirect('placement:manage_drives')
    else:
        form = PlacementDriveForm(instance=drive)
    return render(request, 'placement/edit_drive.html', {'form': form, 'drive': drive})


@company_required
def schedule_interview(request, application_pk):
    application = get_object_or_404(
        Application, pk=application_pk, job__company=request.user.company_profile
    )
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            application.status = 'INTERVIEW_SCHEDULED'
            application.save()
            application.student.placement_status = 'INTERVIEWED'
            application.student.save()
            create_notification(
                application.student.user,
                'Interview Scheduled',
                f'Interview for {application.job.title} on {interview.scheduled_date.strftime("%d %b %Y, %I:%M %p")}',
                'INTERVIEW',
            )
            messages.success(request, 'Interview scheduled.')
            return redirect('jobs:view_applicants', pk=application.job.pk)
    else:
        form = InterviewForm()
    return render(request, 'placement/schedule_interview.html', {
        'form': form, 'application': application,
    })


@student_required
def interview_schedule(request):
    profile = request.user.student_profile
    interviews = Interview.objects.filter(
        application__student=profile
    ).select_related('application', 'application__job', 'application__job__company')
    return render(request, 'placement/interview_schedule.html', {'interviews': interviews})


@company_required
def interview_feedback(request, pk):
    interview = get_object_or_404(
        Interview, pk=pk, application__job__company=request.user.company_profile
    )
    if request.method == 'POST':
        form = InterviewFeedbackForm(request.POST, instance=interview)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback submitted.')
            return redirect('jobs:view_applicants', pk=interview.application.job.pk)
    else:
        form = InterviewFeedbackForm(instance=interview)
    return render(request, 'placement/interview_feedback.html', {
        'form': form, 'interview': interview,
    })


@company_required
def create_offer(request, application_pk):
    application = get_object_or_404(
        Application, pk=application_pk, job__company=request.user.company_profile
    )
    if request.method == 'POST':
        form = OfferLetterForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.application = application
            offer.save()
            application.status = 'OFFERED'
            application.save()
            application.student.placement_status = 'OFFERED'
            application.student.save()
            create_notification(
                application.student.user,
                'Offer Received!',
                f'You received an offer for {application.job.title} - {offer.package_offered}',
                'OFFER',
            )
            messages.success(request, 'Offer letter issued.')
            return redirect('jobs:view_applicants', pk=application.job.pk)
    else:
        form = OfferLetterForm()
    return render(request, 'placement/create_offer.html', {
        'form': form, 'application': application,
    })


@student_required
def respond_offer(request, pk):
    offer = get_object_or_404(
        OfferLetter, pk=pk, application__student=request.user.student_profile
    )
    action = request.GET.get('action')
    if action == 'accept':
        offer.status = 'ACCEPTED'
        offer.application.status = 'OFFER_ACCEPTED'
        offer.application.student.placement_status = 'PLACED'
        offer.application.student.save()
        offer.application.save()
        offer.save()
        messages.success(request, 'Offer accepted! Congratulations!')
    elif action == 'reject':
        offer.status = 'REJECTED'
        offer.application.status = 'OFFER_REJECTED'
        offer.application.save()
        offer.save()
        messages.info(request, 'Offer rejected.')
    return redirect('jobs:my_applications')


@student_required
def download_offer(request, pk):
    offer = get_object_or_404(
        OfferLetter, pk=pk, application__student=request.user.student_profile
    )
    if offer.file:
        from django.http import FileResponse
        return FileResponse(offer.file.open('rb'), as_attachment=True, filename=offer.file.name)
    messages.warning(request, 'No offer letter file available.')
    return redirect('jobs:my_applications')
