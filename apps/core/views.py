from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for monitoring"""
    return JsonResponse({"status": "ok"})

@require_http_methods(["GET"])
def index(request):
    """Home page"""
    return render(request, 'index.html')