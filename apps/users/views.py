from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .models import User, Subscription


@csrf_protect
def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if not all([first_name, last_name, email, password]):
            messages.error(request, 'Tous les champs sont obligatoires.')
            return render(request, 'auth/register.html', {'page_title': 'Inscription'})

        if password != password2:
            messages.error(request, 'Les mots de passe ne correspondent pas.')
            return render(request, 'auth/register.html', {'page_title': 'Inscription'})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Un compte avec cet email existe déjà.')
            return render(request, 'auth/register.html', {'page_title': 'Inscription'})

        if User.objects.filter(username=email).exists():
            messages.error(request, 'Un compte avec cet identifiant existe déjà.')
            return render(request, 'auth/register.html', {'page_title': 'Inscription'})

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Bienvenue {first_name} ! Votre compte a été créé.')
            return redirect('core:index')
        except Exception as e:
            messages.error(request, f'Erreur lors de la création du compte.')
            return render(request, 'auth/register.html', {'page_title': 'Inscription'})

    return render(request, 'auth/register.html', {'page_title': 'Inscription'})


@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=email, password=password)
        if user is None:
            user = authenticate(request, username=email, email=email, password=password)

        if user is not None and user.is_active:
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            next_url = request.GET.get('next', '')
            if next_url:
                return redirect(next_url)
            return redirect('core:tableau_de_bord')
        else:
            messages.error(request, 'Email ou mot de passe incorrect.')

    return render(request, 'auth/login.html', {'page_title': 'Connexion'})


def logout_view(request):
    logout(request)
    messages.success(request, 'Vous avez été déconnecté.')
    return redirect('core:index')


@csrf_protect
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email and User.objects.filter(email=email).exists():
            messages.success(request, 'Un email de réinitialisation vous a été envoyé.')
        else:
            messages.success(request, 'Si un compte existe, un email a été envoyé.')
    return render(request, 'auth/forgot_password.html', {'page_title': 'Mot de passe oublié'})


@csrf_protect
def reset_password(request, uidb64, token):
    return render(request, 'auth/reset_password.html', {'page_title': 'Réinitialiser le mot de passe'})


def otp_verify(request):
    return render(request, 'auth/opt.html', {'page_title': 'Vérification OTP'})


def validation_secondaire(request):
    return render(request, 'auth/validation_secondaire.html', {'page_title': 'Validation secondaire'})


def google_login(request):
    try:
        from allauth.socialaccount.providers.google.views import oauth2_login
        return oauth2_login(request)
    except Exception:
        from django.contrib import messages
        messages.error(request, "La connexion Google n'est pas encore configurée. Veuillez utiliser email + mot de passe.")
        return redirect('users:login')


def google_callback(request):
    try:
        from allauth.socialaccount.providers.google.views import oauth2_callback
        return oauth2_callback(request)
    except Exception:
        return redirect('users:login')


@login_required
def dashboard_redirect(request):
    return redirect('core:tableau_de_bord')


@login_required
def dashboard_dg(request):
    from apps.users.models import User, Subscription
    from apps.messaging.models import MessageContact, Notification
    from apps.institution.models import Candidature, Certificat

    context = {
        'page_title': 'Tableau de bord DG',
        'total_utilisateurs': User.objects.count(),
        'messages_recents': MessageContact.objects.filter(statut='non_lu').count(),
        'candidatures_recentes': Candidature.objects.filter(statut='soumise').count(),
        'certificats_delivres': Certificat.objects.count(),
    }
    return render(request, 'admin/dg.html', context)


@login_required
def dashboard_coordinateur(request, departement):
    from apps.messaging.models import MessageContact

    context = {
        'page_title': f'Dashboard Coordinateur — {departement.title()}',
        'departement': departement,
        'messages_recents': MessageContact.objects.filter(categorie=departement, statut='non_lu').count(),
    }

    templates = {
        'pedagogie': 'admin/coordinateur_pedagogie.html',
        'marketing': 'admin/coordinateur_ marketing.html',
        'technique': 'admin/coordinateur_technique.html',
        'operations': 'admin/coordonnateur_operations.html',
    }
    template = templates.get(departement, 'admin/gestionnaire.html')
    return render(request, template, context)


@login_required
def dashboard_gestionnaire(request, departement):
    context = {
        'page_title': f'Dashboard Gestionnaire — {departement.title()}',
        'departement': departement,
    }
    return render(request, 'admin/gestionnaire.html', context)


@login_required
def dashboard_etudiant(request):
    from apps.parcours.models import ProgressionUtilisateur
    progressions = ProgressionUtilisateur.objects.filter(user=request.user).select_related('parcours')
    context = {
        'page_title': 'Mon tableau de bord',
        'progressions': progressions,
    }
    return render(request, 'admin/gestionnaire.html', context)


@login_required
def checkout(request):
    return render(request, 'pages/entreprise/checkout.html', {'page_title': 'Abonnement'})


@login_required
def create_checkout_session(request):
    return JsonResponse({'error': 'Stripe non configuré'}, status=400)


@login_required
def payment_success(request):
    return render(request, 'pages/entreprise/paiement_success.html', {'page_title': 'Paiement réussi'})


@login_required
def payment_cancel(request):
    return render(request, 'pages/entreprise/paiment_cancel.html', {'page_title': 'Paiement annulé'})


@csrf_protect
def stripe_webhook(request):
    return HttpResponse(status=200)
