"""
Role-based access decorators and mixins.
"""
from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


def role_required(*roles):
    """Decorator to restrict view access to specific user roles."""
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            user = request.user
            if user.is_superuser or user.role in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, 'You do not have permission to access this page.')
            raise PermissionDenied
        return wrapper
    return decorator


def admin_required(view_func):
    return role_required('ADMIN')(view_func)


def placement_officer_required(view_func):
    return role_required('ADMIN', 'PLACEMENT_OFFICER')(view_func)


def student_required(view_func):
    return role_required('STUDENT')(view_func)


def company_required(view_func):
    return role_required('COMPANY')(view_func)


def get_dashboard_url(user):
    """Return the appropriate dashboard URL based on user role."""
    from django.urls import reverse
    role_urls = {
        'ADMIN': 'dashboard:admin_dashboard',
        'PLACEMENT_OFFICER': 'dashboard:officer_dashboard',
        'STUDENT': 'dashboard:student_dashboard',
        'COMPANY': 'dashboard:company_dashboard',
    }
    url_name = role_urls.get(user.role, 'dashboard:home')
    return reverse(url_name)
