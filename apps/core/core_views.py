"""
Vues principales.
"""
import json
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit
from django.core.cache import cache
from django.utils import translation
from django.conf import settings
from apps.core.models import PageStatique, DocumentVault
from apps.core.ai import chatbot, _filtrer_question, _filtrer_reponse
from apps.core.translation import LANGUES
from apps.institution.models import Candidature, OffreEmploi, Certificat
from apps.audit.models import AuditLog
from apps.messaging.models import MessageContact

logger = logging.getLogger(__name__)


def health(request):
    return JsonResponse({'status': 'ok'})


def changer_langue(request, langue):
    if langue in LANGUES:
        translation.activate(langue)
        request.session['_language'] = langue
        request.session['langue'] = langue
        response = redirect(request.META.get('HTTP_REFERER', 'core:index'))
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, langue, max_age=365*24*60*60)
        return response
    return redirect('core:index')


def index(request):
    return render(request, 'index.html', {'page_title': 'Accueil'})


@login_required
def tableau_de_bord(request):
    user = request.user
    if user.is_dg:
        return redirect('users:dashboard_dg')
    elif user.is_coordinateur:
        return redirect('users:dashboard_coordinateur', departement=user.departement)
    elif user.is_gestionnaire:
        return redirect('users:dashboard_gestionnaire', departement=user.departement)
    else:
        return redirect('users:dashboard_etudiant')


def faq(request):
    return render(request, 'pages/support/faq.html', {'page_title': 'FAQ'})


def centre_aide(request):
    return render(request, 'pages/support/centre_aide.html', {'page_title': "Centre d'aide"})


def support_technique(request):
    return render(request, 'pages/support/support_technique.html', {'page_title': 'Support technique'})


def telechargement(request):
    if request.user.is_authenticated:
        try:
            if request.user.subscription.est_active() and request.user.subscription.plan_type in ['annuel', 'bienvenue_annuel']:
                documents = DocumentVault.objects.filter(est_confidentiel=False)
                return render(request, 'pages/support/telechargement.html', {'documents': documents, 'page_title': 'Téléchargements'})
        except Exception:
            pass
    messages.warning(request, "Le téléchargement est réservé aux abonnés Annuels.")
    return redirect('core:premium')


def temoignages(request):
    return render(request, 'pages/support/temoignages.html', {'page_title': 'Témoignages'})


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@csrf_protect
def contact(request):
    if request.method == 'POST':
        if request.POST.get('website'):
            messages.error(request, 'Erreur lors de l\'envoi.')
            return redirect('core:contact')

        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        category = request.POST.get('category', 'general')
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and email and subject and message_text:
            # Créer le message
            msg = MessageContact.objects.create(
                nom=name,
                email=email,
                sujet=subject,
                message=message_text,
                categorie=category,
            )
            messages.success(request, 'Votre message a été envoyé avec succès. Nous vous répondrons sous 48h.')
            
            # Envoyer un seul email au DG
            from apps.core.tasks import envoyer_notification_contact
            envoyer_notification_contact.delay(name, email, category, subject, message_text)
        else:
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')

    return render(request, 'pages/support/contact.html', {'page_title': 'Contact'})


def blog(request):
    try:
        from apps.blog.views import index as blog_index
        return blog_index(request)
    except ImportError:
        return render(request, 'pages/support/blog.html', {'articles': [], 'articles_recents': [], 'page_title': 'Blog'})


@login_required
@require_http_methods(["POST"])
def chatbot_api(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'reponse': 'Requête invalide.'}, status=400)
    question = data.get('question', '').strip()
    cours = data.get('cours', '')

    if not question:
        return JsonResponse({'reponse': 'Veuillez poser une question.'})

    ip = request.META.get('REMOTE_ADDR', '')

    bloquee, motif = _filtrer_question(question)
    if bloquee:
        AuditLog.objects.create(
            utilisateur=request.user, action='chatbot_bloque',
            gravite='critique', objet=f'Question bloquée: {question[:100]}',
            description=motif, ip_address=ip,
        )
        return JsonResponse({'reponse': "Cette question ne peut pas être traitée.", 'bloque': True})

    key = f'chatbot_quota_{request.user.id}'
    count = cache.get(key, 0)
    
    is_premium = False
    try:
        if request.user.subscription.est_active() and request.user.subscription.plan_type in ['annuel', 'bienvenue_annuel']:
            is_premium = True
    except Exception:
        pass
    
    if not is_premium and count >= 10:
        return JsonResponse({'reponse': "Limite quotidienne de 10 questions atteinte.", 'quota': True})
    
    cache.set(key, count + 1, 86400)

    langue = request.session.get('langue', 'fr')
    reponse, erreur = chatbot(question, langue, cours)

    reponse_bloquee, reponse_finale = _filtrer_reponse(reponse)
    if reponse_bloquee:
        AuditLog.objects.create(
            utilisateur=request.user, action='chatbot_reponse_bloquee',
            gravite='critique', objet=f'Réponse bloquée', ip_address=ip,
        )
        reponse_finale = "Je ne peux pas répondre à cette question."

    AuditLog.objects.create(
        utilisateur=request.user, action='chatbot',
        objet=f'Q: {question[:100]}', ip_address=ip,
    )

    return JsonResponse({'reponse': reponse_finale})


def programme(request):
    return redirect('core:index')


def programme_metier(request, metier):
    templates = {
        'pilote_de_ligne': 'pages/Academie/programme_pilote_de_ligne.html',
        'personnel_navigant': 'pages/Academie/programme_pnc.html',
        'ingenieur_aeronautique': 'pages/Academie/programme_ingenieur_aeronautique.html',
        'controleur_aerien': 'pages/Academie/programme_controleur_aerien.html',
        'technicien_aeronautique': 'pages/Academie/programme_technicien_aeronautique.html',
        'mecanicien_avion': 'pages/Academie/programme_mecanicien_avion.html',
        'agent_escale': 'pages/Academie/programme_agent_escale.html',
        'formation_avancee': 'pages/Academie/programme_formation_avancee.html',
    }
    template = templates.get(metier)
    if not template:
        raise Http404('Programme non trouvé.')
    titres = {
        'pilote_de_ligne': 'Pilote de Ligne',
        'personnel_navigant': 'Personnel Navigant Commercial (PNC)',
        'ingenieur_aeronautique': 'Ingénieur Aéronautique',
        'controleur_aerien': 'Contrôleur Aérien',
        'technicien_aeronautique': 'Technicien Aéronautique',
        'mecanicien_avion': 'Mécanicien Avion',
        'agent_escale': "Agent d'Escale",
        'formation_avancee': 'Formation Avancée Premium',
    }
    return render(request, template, {'page_title': titres.get(metier, metier.replace('_', ' ').title())})


def a_propos(request):
    page = PageStatique.objects.filter(type_page='a_propos', archive=False).first()
    return render(request, 'pages/a_propos.html', {'page_title': 'À propos', 'page': page})


def carriere(request):
    offres = OffreEmploi.objects.filter(statut='publiee').order_by('-date_publication')
    return render(request, 'pages/recrutement/carriere.html', {'page_title': 'Carrières', 'offres': offres})


@ratelimit(key='ip', rate='3/m', method='POST', block=True)
@csrf_protect
def postuler(request, offre_id=None):
    offre = None
    if offre_id:
        offre = get_object_or_404(OffreEmploi, id=offre_id, statut='publiee')

    if request.method == 'POST':
        if request.POST.get('website'):
            messages.error(request, 'Erreur.')
            return redirect('core:carriere')

        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        email = request.POST.get('email', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        message_text = request.POST.get('message', '').strip()
        poste = request.POST.get('poste', offre.titre if offre else 'Candidature spontanée')

        if nom and prenom and email:
            Candidature.objects.create(
                poste=poste, nom=nom, prenom=prenom,
                email=email, telephone=telephone, message=message_text,
            )
            messages.success(request, 'Candidature envoyée avec succès.')
            return redirect('core:carriere')
        else:
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')

    return render(request, 'pages/recrutement/postuler.html', {'page_title': 'Postuler', 'offre': offre})


@login_required
def espace_candidat(request):
    candidatures = Candidature.objects.filter(email=request.user.email).order_by('-date_soumission')
    return render(request, 'pages/recrutement/espace_candidat.html', {'page_title': 'Espace candidat', 'candidatures': candidatures})


def premium(request):
    from apps.users.models import User
    total_inscrits = User.objects.count()
    places_restantes = max(0, 3 - total_inscrits)
    return render(request, 'pages/entreprise/premium.html', {
        'page_title': 'Abonnements Premium',
        'places_bienvenue_restantes': places_restantes if places_restantes > 0 else 0,
    })


def partenariats(request):
    return render(request, 'pages/entreprise/partenariats.html', {'page_title': 'Partenariats'})


def verification_certificat(request):
    certificat = None
    erreur = None
    numero_recherche = ''
    hash_recherche = ''

    if request.method == 'POST':
        mode = request.POST.get('mode', 'numero')
        if mode == 'numero':
            numero_recherche = request.POST.get('numero_serie', '').strip()
            if numero_recherche:
                try:
                    certificat = Certificat.objects.get(numero_serie=numero_recherche)
                    if certificat.statut == 'revoke':
                        erreur = 'revoke'
                        certificat = None
                except Certificat.DoesNotExist:
                    erreur = 'non_trouve'
        elif mode == 'hash':
            hash_recherche = request.POST.get('hash_verification', '').strip()
            if hash_recherche:
                try:
                    certificat = Certificat.objects.get(hash_verification=hash_recherche)
                    if certificat.statut == 'revoke':
                        erreur = 'revoke'
                        certificat = None
                except Certificat.DoesNotExist:
                    erreur = 'non_trouve'

    return render(request, 'pages/utilisateur/verification_certificat.html', {
        'page_title': 'Vérification de certificat',
        'certificat': certificat,
        'erreur': erreur,
        'numero_recherche': numero_recherche,
        'hash_recherche': hash_recherche,
    })


def page_legale(request, type_page):
    types_valides = ['cgu', 'confidentialite', 'mentions_legales', 'cookies', 'accessibilite']
    if type_page not in types_valides:
        raise Http404('Page légale non trouvée.')

    page = PageStatique.objects.filter(type_page=type_page, archive=False, approuve_par_dg=True).first()

    if page and page.est_publicable():
        return render(request, 'pages/legal/page_legale.html', {'page_title': page.titre, 'page': page})

    template_map = {
        'cgu': 'pages/legal/cgu.html',
        'confidentialite': 'pages/legal/confidentialite.html',
        'mentions_legales': 'pages/legal/mentions_legales.html',
    }
    template = template_map.get(type_page)
    if template:
        return render(request, template, {'page_title': type_page.replace('_', ' ').title()})

    raise Http404('Page non trouvée.')


@login_required
def servir_fichier_vault(request, fichier_id):
    document = get_object_or_404(DocumentVault, id=fichier_id)

    if not request.user.is_dg and document.proprietaire != request.user:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied('Accès non autorisé.')

    AuditLog.objects.create(
        utilisateur=request.user,
        action='acces_vault',
        objet=f'Document {document.nom}',
        ip_address=request.META.get('REMOTE_ADDR', ''),
    )

    with document.fichier.open('rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{document.nom}"'
        return response


def get_gestion_context(request, departement):
    from apps.messaging.models import MessageContact
    dg_messages = MessageContact.objects.filter(categorie=departement).order_by('-date_envoi')[:10]
    return {'dg_messages': dg_messages}


@login_required
def pedagogie_contenu(request):
    context = get_gestion_context(request, 'pedagogie')
    context.update({'page_title': 'Pédagogie & Contenu'})
    return render(request, 'pages/institution/pedagogie_contenu.html', context)


@login_required
def developpement_technique(request):
    context = get_gestion_context(request, 'technique')
    context.update({'page_title': 'Développement & Technique'})
    return render(request, 'pages/institution/developpement_technique.html', context)


@login_required
def marketing_communication(request):
    context = get_gestion_context(request, 'marketing')
    context.update({'page_title': 'Marketing & Communication'})
    return render(request, 'pages/institution/marketing_communication.html', context)


@login_required
def operations_logistique(request):
    context = get_gestion_context(request, 'operations')
    context.update({'page_title': 'Opérations & Logistique'})
    return render(request, 'pages/institution/operations_logistique.html', context)


@login_required
def qualite_innovation(request):
    context = get_gestion_context(request, 'qualite')
    context.update({'page_title': 'Qualité & Innovation'})
    return render(request, 'pages/institution/qualite_innovation.html', context)


@login_required
def support_administration(request):
    context = get_gestion_context(request, 'support')
    context.update({'page_title': 'Support & Administration'})
    return render(request, 'pages/institution/support_administration.html', context)


@login_required
def design_experience_utilisateur(request):
    context = get_gestion_context(request, 'design')
    context.update({'page_title': 'Design & Expérience Utilisateur'})
    return render(request, 'pages/institution/design_experience_utilisateur.html', context)


def recherche(request):
    q = request.GET.get('q', '').strip()
    resultats = []
    if q:
        from apps.blog.models import Article
        from apps.parcours.models import Parcours
        articles = Article.objects.filter(titre__icontains=q, statut='publie')[:5]
        parcours_list = Parcours.objects.filter(nom__icontains=q)[:5]
        resultats = list(articles) + list(parcours_list)
    return render(request, 'pages/recherche.html', {'page_title': 'Recherche', 'q': q, 'resultats': resultats})


def offline(request):
    return render(request, 'offline.html', {'page_title': 'Hors ligne'})


def api_blog_recent(request):
    try:
        from apps.blog.models import Article
        articles = Article.objects.filter(publie=True).order_by('-date_publication')[:4]
        data = [{'title': a.titre, 'slug': a.slug, 'excerpt': getattr(a, 'extrait', ''), 'date': str(a.date_publication)} for a in articles]
    except Exception:
        data = []
    return JsonResponse({'articles': data})


def api_temoignages_recent(request):
    return JsonResponse({'temoignages': []})


@require_http_methods(["GET", "POST"])
def api_newsletter(request):
    import json as _json
    from django.views.decorators.csrf import csrf_exempt
    if request.method == 'GET':
        return JsonResponse({'status': 'ok'})
    try:
        body = _json.loads(request.body)
        email = body.get('email', '').strip()
    except Exception:
        email = request.POST.get('email', '').strip()
    if email:
        return JsonResponse({'success': True, 'message': 'Inscription confirmée ! Merci.'})
    return JsonResponse({'success': False, 'message': 'Email invalide.'}, status=400)


@require_http_methods(["GET", "POST"])
def set_language_api(request):
    import json as _json
    try:
        body = _json.loads(request.body)
        langue = body.get('langue', 'fr')
    except Exception:
        langue = 'fr'
    if langue in ['fr', 'en', 'es', 'ar', 'zh', 'pt', 'de', 'it', 'ru', 'ja', 'ko', 'nl', 'pl', 'tr', 'hi']:
        translation.activate(langue)
        request.session['langue'] = langue
        response = JsonResponse({'success': True})
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, langue, max_age=365*24*60*60)
        return response
    return JsonResponse({'success': False}, status=400)


def handler403(request, exception=None):
    return render(request, 'errors/403.html', status=403)


def handler404(request, exception=None):
    return render(request, 'errors/404.html', status=404)


def handler429(request, exception=None):
    return render(request, 'errors/429.html', status=429)


def handler500(request):
    return render(request, 'errors/500.html', status=500)


def maintenance(request):
    return render(request, 'errors/maintenance.html', status=503)
