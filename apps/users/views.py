from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def login_view(request):
    """User login"""
    return render(request, 'auth/login.html')

@require_http_methods(["GET", "POST"])
def register_view(request):
    """User registration"""
    return render(request, 'auth/register.html')

@require_http_methods(["GET", "POST"])
def forgot_password_view(request):
    """Forgot password"""
    return render(request, 'auth/forgot_password.html')