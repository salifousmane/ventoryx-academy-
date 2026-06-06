"""Décorateurs RBAC."""
from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def dg_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_dg:
            raise PermissionDenied('Réservé au Directeur Général.')
        if request.user.otp_required and not request.session.get('otp_verified'):
            return redirect('users:otp_verify')
        return view_func(request, *args, **kwargs)
    return wrapper


def coordinateur_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_coordinateur and not request.user.is_dg:
            raise PermissionDenied('Réservé aux coordinateurs.')
        # Validation secondaire pour actions critiques
        if request.session.get('action_critique') and not request.session.get('validation_secondaire'):
            return redirect('users:validation_secondaire')
        return view_func(request, *args, **kwargs)
    return wrapper


def gestionnaire_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_gestionnaire and not request.user.is_coordinateur and not request.user.is_dg:
            raise PermissionDenied('Réservé aux gestionnaires.')
        return view_func(request, *args, **kwargs)
    return wrapper


def abonnement_requis(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.abonnement_actif:
            return redirect('core:premium')
        return view_func(request, *args, **kwargs)
    return wrapper


def departement_requis(departement):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_dg:
                return view_func(request, *args, **kwargs)
            if request.user.departement != departement:
                raise PermissionDenied('Département non autorisé.')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
