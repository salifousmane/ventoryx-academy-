from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .models import Task, Campaign, Ticket

@require_http_methods(["GET"])
def task_list(request):
    """List tasks"""
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'admin/gestion_tasks.html', {'tasks': tasks})

@require_http_methods(["GET"])
def ticket_list(request):
    """List support tickets"""
    tickets = Ticket.objects.all()
    return render(request, 'admin/gestion_tickets.html', {'tickets': tickets})