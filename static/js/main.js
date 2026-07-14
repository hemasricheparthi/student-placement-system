/**
 * Placement Portal - Main JavaScript utilities
 */

document.addEventListener('DOMContentLoaded', function () {
    initAlertDismiss();
    initConfirmActions();
    initMatchBars();
    initTooltips();
});

/** Auto-dismiss success alerts after 5 seconds */
function initAlertDismiss() {
    document.querySelectorAll('.alert-success.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            var closeBtn = alert.querySelector('.btn-close');
            if (closeBtn) closeBtn.click();
        }, 5000);
    });
}

/** Confirm destructive actions (delete, reject) */
function initConfirmActions() {
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            var message = el.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });
}

/** Animate match percentage bars on page load */
function initMatchBars() {
    document.querySelectorAll('.match-bar-fill[data-width]').forEach(function (bar) {
        var width = bar.getAttribute('data-width');
        bar.style.width = '0%';
        requestAnimationFrame(function () {
            bar.style.width = width + '%';
        });
    });
}

/** Initialize Bootstrap tooltips */
function initTooltips() {
    if (typeof bootstrap !== 'undefined') {
        document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
            new bootstrap.Tooltip(el);
        });
    }
}

/** Get CSS class for match percentage */
function getMatchClass(percentage) {
    if (percentage >= 70) return 'high';
    if (percentage >= 40) return 'medium';
    return 'low';
}

/** Format date string for display */
function formatDate(dateStr) {
    if (!dateStr) return '';
    var d = new Date(dateStr);
    return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
}
