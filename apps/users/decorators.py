from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


def dg_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not request.user.is_dg:
            return HttpResponseForbidden('Accès réservé à la Direction Générale.')
        return func(request, *args, **kwargs)
    return wrapper


def coordinateur_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not (request.user.is_coordinateur or request.user.is_dg):
            return HttpResponseForbidden('Accès réservé aux coordinateurs.')
        return func(request, *args, **kwargs)
    return wrapper


def gestionnaire_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not (request.user.is_gestionnaire or request.user.is_coordinateur or request.user.is_dg):
            return HttpResponseForbidden('Accès réservé aux gestionnaires.')
        return func(request, *args, **kwargs)
    return wrapper
