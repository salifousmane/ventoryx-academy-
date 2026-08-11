
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings
from django.db import models
from .models import User, Subscription

logger = logging.getLogger(__name__)

@csrf_protect
@csrf_exempt
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")
        nationality = request.POST.get("nationality", "").strip()
        date_naissance = request.POST.get("date_naissance", "").strip()
        role_souhaite = request.POST.get("role_souhaite", "").strip()

        form_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "nationality": nationality,
            "date_naissance": date_naissance,
            "role_souhaite": role_souhaite,
        }

        if not all([first_name, last_name, email, password]):
            messages.error(request, "Tous les champs obligatoires doivent être remplis.")
            return render(request, "auth/register.html", {"page_title": "Inscription", "form_data": form_data})

        if len(password) < 10:
            messages.error(request, "Le mot de passe doit contenir au moins 10 caractères.")
            return render(request, "auth/register.html", {"page_title": "Inscription", "form_data": form_data})

        if password != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, "auth/register.html", {"page_title": "Inscription", "form_data": form_data})

        if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
            messages.error(request, "Un compte avec cet email existe déjà.")
            return render(request, "auth/register.html", {"page_title": "Inscription", "form_data": form_data})

        try:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            messages.success(request, f"Bienvenue {first_name} ! Votre compte a été créé avec succès.")
            return redirect("users:dashboard_etudiant")
        except Exception:
            messages.error(request, "Une erreur est survenue lors de la création du compte. Veuillez réessayer.")
            return render(request, "auth/register.html", {"page_title": "Inscription", "form_data": form_data})

    return render(request, "auth/register.html", {"page_title": "Inscription", "form_data": {}})

@csrf_protect
@csrf_exempt
def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")

    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=email, password=password)
        if user is None:
            user = authenticate(request, username=email, email=email, password=password)

        if user is not None and user.is_active:
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            next_url = request.GET.get("next", "")
            if next_url:
                return redirect(next_url)

            # Redirection selon le rôle (100% propre, plus de conflit Git)
            if user.role == 'etudiant':
                return redirect("users:dashboard_etudiant")
            elif user.role == 'dg':
                return redirect("users:dashboard_dg")
            elif user.role == 'coordinateur':
                departement = getattr(user, 'departement', 'pedagogie')
                return redirect("users:dashboard_coordinateur", departement=departement)

            # Redirection par défaut (fallback)
            return redirect("core:index")
        else:
            messages.error(request, "Email ou mot de passe incorrect.")

    return render(request, "auth/login.html", {"page_title": "Connexion"})

def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté.")
    return redirect("core:index")

@csrf_protect
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        if email and User.objects.filter(email=email).exists():
            messages.success(request, "Un email de réinitialisation vous a été envoyé.")
        else:
            messages.success(request, "Si un compte existe avec cet email, un lien de réinitialisation a été envoyé.")
    return render(request, "auth/forgot_password.html", {"page_title": "Mot de passe oublié"})

@csrf_protect
def reset_password(request, uidb64, token):
    return render(request, "auth/reset_password.html", {"page_title": "Réinitialiser le mot de passe"})

def otp_verify(request):
    return render(request, "auth/opt.html", {"page_title": "Vérification OTP"})

def validation_secondaire(request):
    return render(request, "auth/validation_secondaire.html", {"page_title": "Validation secondaire"})

def google_login(request):
    try:
        from allauth.socialaccount.providers.google.views import oauth2_login
        return oauth2_login(request)
    except Exception:
        messages.error(request, "La connexion Google n'est pas encore configurée. Veuillez utiliser email + mot de passe.")
        return redirect("users:login")

def google_callback(request):
    try:
        from allauth.socialaccount.providers.google.views import oauth2_callback
        return oauth2_callback(request)
    except Exception:
        return redirect("users:login")

@login_required
def dashboard_redirect(request):
    return redirect("users:dashboard_etudiant")

@login_required
def dashboard_dg(request):
    from apps.users.models import User
    from apps.messaging.models import MessageContact
    from apps.institution.models import Candidature, Certificat
    from apps.gestion.models import Tache, TicketSupport
    from apps.parcours.models import Parcours
    from django.utils import timezone
    from datetime import timedelta

    now = timezone.now()
    last_30 = now - timedelta(days=30)

    context = {
        "page_title": "Tableau de bord DG",
        "total_utilisateurs": User.objects.count(),
        "messages_recents": MessageContact.objects.filter(statut="non_lu").count(),
        "candidatures_recentes": Candidature.objects.filter(statut="soumise").count(),
        "certificats_delivres": Certificat.objects.count(),
        "candidatures_total": Candidature.objects.count(),
        "total_parcours": Parcours.objects.count(),
        "taches_en_cours": Tache.objects.filter(statut="en_cours").count(),
        "tickets_ouverts": TicketSupport.objects.filter(statut="ouvert").count(),
        "nouveaux_utilisateurs": User.objects.filter(date_joined__gte=last_30).count(),
    }
    return render(request, "templates/admin/dg.html", context)

@login_required
def dashboard_coordinateur(request, departement):
    from apps.messaging.models import MessageContact
    from apps.gestion.models import Tache

    context = {
        "page_title": f"Dashboard Coordinateur — {departement.title()}",
        "departement": departement,
        "messages_recents": MessageContact.objects.filter(categorie=departement, statut="non_lu").count(),
        "taches_actives": Tache.objects.filter(departement=departement, statut="en_cours").count(),
        "taches_terminees": Tache.objects.filter(departement=departement, statut="terminee").count(),
    }

    templates = {
        "pedagogie": "admin/coordinateur_pedagogie.html",
        "marketing": "admin/coordinateur_marketing.html",
        "technique": "admin/coordinateur_technique.html",
        "operations": "admin/coordonnateur_operations.html",
        "qualite": "admin/coordinateur_qualite.html",
        "support": "admin/coordinateur_support.html",
        "design": "admin/coordinateur_design.html",
    }
    template = templates.get(departement, "admin/gestionnaire.html")
    return render(request, "templates/" + template, context)

@login_required
def dashboard_gestionnaire(request, departement):
    from apps.messaging.models import MessageContact

    messages_list = MessageContact.objects.filter(categorie=departement).order_by("-date_envoi")[:20]
    total = messages_list.count()
    non_lus = MessageContact.objects.filter(categorie=departement, statut="non_lu").count()
    traites = MessageContact.objects.filter(categorie=departement, statut="repondu").count()

    context = {
        "page_title": f"Dashboard Gestionnaire — {departement.title()}",
        "departement": departement,
        "messages_list": messages_list,
        "total_messages": total,
        "messages_non_lus": non_lus,
        "messages_traites": traites,
    }
    return render(request, "templates/admin/gestionnaire.html", context)

@login_required
def dashboard_etudiant(request):
    from apps.parcours.models import ProgressionUtilisateur, Parcours, CoursItem
    from apps.messaging.models import Notification
    from django.utils import timezone
    from django.db import models

    user = request.user
    all_prog = ProgressionUtilisateur.objects.filter(user=user).select_related('parcours', 'module', 'item')

    parcours_stats = {}
    derniere_date = None
    dernier_item = None

    for prog in all_prog:
        pk = prog.parcours_id
        if pk not in parcours_stats:
            parcours_stats[pk] = {
                'parcours': prog.parcours,
                'cours_termines': 0,
                'total_cours_vus': 0,
                'tests_reussis': 0,
                'total_tests_vus': 0,
                'scores': [],
                'last_date': prog.date_modification,
            }
        s = parcours_stats[pk]
        if prog.item:
            if prog.item.type == 'cours':
                s['total_cours_vus'] += 1
                if prog.termine:
                    s['cours_termines'] += 1
            elif prog.item.type == 'test':
                s['total_tests_vus'] += 1
                if prog.score >= 70:
                    s['tests_reussis'] += 1
                if prog.score:
                    s['scores'].append(prog.score)
        if prog.date_modification > s['last_date']:
            s['last_date'] = prog.date_modification
        if derniere_date is None or prog.date_modification > derniere_date:
            derniere_date = prog.date_modification
            dernier_item = prog.item

    progressions_list = []
    for stat in sorted(parcours_stats.values(), key=lambda x: x['last_date'], reverse=True):
        parc = stat['parcours']
        total_cours_parc = max(parc.total_cours, stat['total_cours_vus']) or 1
        total_tests_parc = max(parc.total_quiz, stat['total_tests_vus'])
        cours_t = stat['cours_termines']
        pourcentage = min(100, int(cours_t / total_cours_parc * 100))
        progressions_list.append({
            'metier': parc.nom,
            'slug': parc.metier,
            'module_actuel': 1,
            'total_modules': parc.modules.count(),
            'pourcentage': pourcentage,
            'cours_termines': cours_t,
            'total_cours': total_cours_parc,
            'tests_reussis': stat['tests_reussis'],
            'total_tests': total_tests_parc,
        })

    cours_total_global = sum(s['total_cours_vus'] for s in parcours_stats.values())
    cours_termines_global = sum(s['cours_termines'] for s in parcours_stats.values())
    tests_reussis_global = sum(s['tests_reussis'] for s in parcours_stats.values())
    tests_total_global = sum(s['total_tests_vus'] for s in parcours_stats.values())
    all_scores = [sc for s in parcours_stats.values() for sc in s['scores']]
    moyenne = int(sum(all_scores) / len(all_scores)) if all_scores else 0

    parcours_actif = None
    if progressions_list:
        try:
            parcours_actif = Parcours.objects.get(metier=progressions_list[0]['slug'])
        except Parcours.DoesNotExist:
            pass

    try:
        certificats = user.certificats.filter(statut='valide').order_by('-date_delivrance')
    except Exception:
        certificats = []

    try:
        notifications = Notification.objects.filter(destinataire=user).order_by('-date_creation')[:10]
        notifications_non_lues = Notification.objects.filter(destinataire=user, lue=False).count()
    except Exception:
        notifications = []
        notifications_non_lues = 0

    abonnement_actif = False
    plan_type = None
    date_fin_abonnement = None
    try:
        sub = user.subscription
        abonnement_actif = sub.est_active()
        plan_type = sub.plan_type
        date_fin_abonnement = sub.date_fin
    except Exception:
        pass

    heures_formation = int(cours_termines_global * 0.5)

    rang_global = ProgressionUtilisateur.objects.filter(termine=True).values('user').distinct().count()
    ma_position = ProgressionUtilisateur.objects.filter(termine=True).values('user').annotate(nb=models.Count('id')).filter(nb__gt=cours_termines_global).count() + 1 if cours_termines_global > 0 else '-'

    try:
        activites_recentes_qs = ProgressionUtilisateur.objects.filter(user=user, termine=True).select_related('item', 'parcours').order_by('-date_modification')[:10]
        activites_recentes = [
            {
                'type': p.item.type if p.item else 'cours',
                'description': f"{p.item.titre} — {p.parcours.nom}" if p.item else p.parcours.nom,
                'date': p.date_modification,
            }
            for p in activites_recentes_qs
        ]
    except Exception:
        activites_recentes = []

    try:
        from apps.parcours.models import Parcours as ParcoursModel
        prog_par_slug = {p['slug']: p['pourcentage'] for p in progressions_list}
        metiers_disponibles = [
            {'nom': parc.nom, 'slug': parc.metier, 'progression': prog_par_slug.get(parc.metier, 0)}
            for parc in ParcoursModel.objects.all().order_by('nom')
        ]
    except Exception:
        metiers_disponibles = []

    context = {
        "page_title": "Mon espace",
        "progressions": progressions_list,
        "parcours_actif": parcours_actif,
        "module_actuel": None,
        "cours_termines": cours_termines_global,
        "cours_total": cours_total_global,
        "tests_reussis": tests_reussis_global,
        "tests_total": tests_total_global,
        "moyenne_generale": moyenne,
        "heures_formation": heures_formation,
        "rang_classement": f"#{ma_position}" if isinstance(ma_position, int) else "-",
        "parcours_actifs": len(parcours_stats),
        "notifications": notifications,
        "notifications_non_lues": notifications_non_lues,
        "messages_non_lus": 0,
        "dernier_cours": dernier_item,
        "prochains_tests": [],
        "certificats": certificats,
        "abonnement_actif": abonnement_actif,
        "plan_type": plan_type,
        "date_fin_abonnement": date_fin_abonnement,
        "activites_recentes": activites_recentes,
        "metiers_disponibles": metiers_disponibles,
        "discussions_recentes": [],
        "recommandations": [],
    }
    return render(request, "templates/pages/utilisateur/dashboard_etudiant.html", context)

@login_required
def checkout(request):
    return render(request, "pages/entreprise/checkout.html", {"page_title": "Abonnement"})

@login_required
@require_POST
def create_checkout_session(request):
    stripe_secret = getattr(settings, 'STRIPE_SECRET_KEY', '')
    if not stripe_secret:
        return JsonResponse({"error": "Le paiement en ligne n'est pas encore disponible. Contactez-nous."}, status=503)

    try:
        import stripe, json as _json
        stripe.api_key = stripe_secret
        body = _json.loads(request.body)
        plan = body.get('plan', 'annuel')
        promo_code = body.get('promo_code', '').strip()

        prices = {
            'mensuel': {'unit_amount': 3900, 'name': 'Abonnement Mensuel'},
            'annuel': {'unit_amount': 32900, 'name': 'Abonnement Annuel'},
        }
        price_data = prices.get(plan, prices['annuel'])

        success_url = request.build_absolute_uri('/auth/paiement/succes/')
        cancel_url = request.build_absolute_uri('/auth/paiement/annulation/')

        session_params = {
            'payment_method_types': ['card'],
            'line_items': [{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': price_data['name']},
                    'unit_amount': price_data['unit_amount'],
                    'recurring': {'interval': 'month' if plan == 'mensuel' else 'year'},
                },
                'quantity': 1,
            }],
            'mode': 'subscription',
            'success_url': success_url + '?session_id={CHECKOUT_SESSION_ID}',
            'cancel_url': cancel_url,
            'customer_email': request.user.email,
            'metadata': {'user_id': request.user.id, 'plan': plan},
        }

        if promo_code:
            try:
                coupons = stripe.PromotionCode.list(code=promo_code, active=True, limit=1)
                if coupons.data:
                    session_params['discounts'] = [{'promotion_code': coupons.data[0].id}]
            except Exception:
                pass

        session = stripe.checkout.Session.create(**session_params)
        return JsonResponse({'url': session.url})
    except Exception as e:
        logger.error(f"Stripe error: {e}")
        return JsonResponse({"error": "Erreur lors de la session de paiement."}, status=500)

@login_required
def payment_success(request):
    return render(request, "pages/entreprise/paiement_success.html", {"page_title": "Paiement réussi"})

@login_required
def payment_cancel(request):
    return render(request, "pages/entreprise/paiment_cancel.html", {"page_title": "Paiement annulé"})

@csrf_exempt
def stripe_webhook(request):
    stripe_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    if not stripe_secret:
        return HttpResponse(status=200)

    try:
        import stripe
        stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
        event = stripe.Webhook.construct_event(payload, sig_header, stripe_secret)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            user_id = session.get('metadata', {}).get('user_id')
            plan = session.get('metadata', {}).get('plan', 'mensuel')
            stripe_customer_id = session.get('customer', '')
            stripe_subscription_id = session.get('subscription', '')

            if user_id:
                from apps.users.models import User, Subscription
                from django.utils import timezone
                from datetime import timedelta
                try:
                    user = User.objects.get(id=user_id)
                    sub, _ = Subscription.objects.get_or_create(user=user)
                    sub.plan_type = plan
                    sub.statut = 'active'
                    sub.stripe_customer_id = stripe_customer_id or ''
                    sub.stripe_subscription_id = stripe_subscription_id or ''
                    sub.date_debut = timezone.now()
                    sub.date_fin = timezone.now() + (timedelta(days=365) if plan == 'annuel' else timedelta(days=30))
                    sub.save()
                    user.abonnement_actif = True
                    user.save(update_fields=['abonnement_actif'])
                except Exception as e:
                    import logging
                    logging.getLogger(__name__).error(f"Webhook user update error: {e}")
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Stripe webhook error: {e}")
        return HttpResponse(status=400)

    return HttpResponse(status=200)

@login_required
def reunion_virtuelle(request):
    context = {"page_title": "Réunion virtuelle"}
    return render(request, "templates/admin/reunion.html", context)

@login_required
@require_POST
def reunion_envoyer_message(request):
    message_text = request.POST.get("message", "").strip()
    if message_text:
        messages.success(request, "Message envoyé dans la réunion.")
    return redirect("users:reunion_virtuelle")

@login_required
def page_equipe(request):
    if request.user.role != "dg":
        messages.error(request, "Accès réservé à la Direction Générale.")
        return redirect("users:dashboard_dg")
    from apps.users.models import User
    membres = User.objects.exclude(role="etudiant").order_by("role", "last_name")
    context = {"page_title": "Notre Équipe", "membres": membres}
    return render(request, "templates/admin/equipe.html", context)

@login_required
def page_rapports_transparence(request):
    if request.user.role != "dg":
        messages.error(request, "Accès réservé à la Direction Générale.")
        return redirect("users:dashboard_dg")
    from apps.audit.models import AuditLog
    from apps.institution.models import Candidature, Certificat
    from apps.users.models import User
    from django.utils import timezone
    from datetime import timedelta

    now = timezone.now()
    logs_recents = AuditLog.objects.order_by("-timestamp")[:50]

    context = {
        "page_title": "Rapports de Transparence",
        "total_utilisateurs": User.objects.count(),
        "total_certificats": Certificat.objects.count(),
        "total_candidatures": Candidature.objects.count(),
        "logs_recents": logs_recents,
        "date_rapport": now,
    }
    return render(request, "templates/admin/rapports_transparence.html", context)

@login_required
def documentation(request):
    context = {"page_title": "Documentation Technique"}
    return render(request, "pages/documentation.html", context)