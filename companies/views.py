"""Company views."""
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import company_required, placement_officer_required
from accounts.views import create_notification
from companies.forms import CompanyProfileForm, CompanySearchForm
from companies.models import CompanyProfile


@company_required
def company_profile(request):
    profile = request.user.company_profile
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company profile updated.')
            return redirect('companies:profile')
    else:
        form = CompanyProfileForm(instance=profile)
    return render(request, 'companies/profile.html', {
        'form': form,
        'profile': profile,
        'jobs': profile.jobs.all()[:5],
    })


def company_list(request):
    """Public company listing."""
    form = CompanySearchForm(request.GET)
    companies = CompanyProfile.objects.filter(is_active=True, is_verified=True)

    if form.is_valid():
        search = form.cleaned_data.get('search')
        industry = form.cleaned_data.get('industry')
        if search:
            companies = companies.filter(company_name__icontains=search)
        if industry:
            companies = companies.filter(industry__icontains=industry)

    paginator = Paginator(companies, 10)
    page = request.GET.get('page')
    companies_page = paginator.get_page(page)

    return render(request, 'companies/company_list.html', {
        'companies': companies_page,
        'form': form,
    })


def company_detail(request, pk):
    company = get_object_or_404(CompanyProfile, pk=pk, is_active=True)
    jobs = company.jobs.filter(status='OPEN')
    return render(request, 'companies/company_detail.html', {
        'company': company,
        'jobs': jobs,
    })


@placement_officer_required
def verify_company(request, pk):
    company = get_object_or_404(CompanyProfile, pk=pk)
    company.is_verified = not company.is_verified
    company.save()
    status = 'verified' if company.is_verified else 'unverified'
    messages.success(request, f'Company {status}.')
    create_notification(
        company.user,
        'Company Verification Update',
        f'Your company profile has been {status}.',
        'INFO',
    )
    return redirect('companies:manage_companies')


@placement_officer_required
def manage_companies(request):
    form = CompanySearchForm(request.GET)
    companies = CompanyProfile.objects.all()

    if form.is_valid():
        search = form.cleaned_data.get('search')
        if search:
            companies = companies.filter(company_name__icontains=search)

    paginator = Paginator(companies, 10)
    page = request.GET.get('page')
    companies_page = paginator.get_page(page)

    return render(request, 'companies/manage_companies.html', {
        'companies': companies_page,
        'form': form,
    })
