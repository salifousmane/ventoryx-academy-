from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import AuditLog

@login_required
@require_http_methods(["GET"])
def audit_journal(request):
    """View audit log"""
    logs = AuditLog.objects.all()[:1000]  # Last 1000 entries
    return render(request, 'audit/journal.html', {'logs': logs})