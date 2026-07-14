"""Context processor for notifications in navbar."""


def notifications(request):
    """Inject unread notification count into all templates."""
    if request.user.is_authenticated:
        unread_count = request.user.notifications.filter(is_read=False).count()
        recent_notifications = request.user.notifications.filter(is_read=False)[:5]
        return {
            'unread_notification_count': unread_count,
            'recent_notifications': recent_notifications,
        }
    return {
        'unread_notification_count': 0,
        'recent_notifications': [],
    }
