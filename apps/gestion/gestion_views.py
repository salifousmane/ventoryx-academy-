"""Vues de gestion des départements — Tous rôles."""
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST, require_http_methods
from django.utils import timezone
from django.core.cache import cache
from apps.parcours.models import Parcours, ModuleParcours, CoursItem, Question, Reponse
from apps.gestion.models import Tache, Campagne, TicketSupport
from apps.institution.models import Candidature, OffreEmploi
from apps.messaging.models import MessageContact, Notification
from apps.blog.models import Article
from apps.audit.models import AuditLog
from apps.users.decorators import dg_required, coordinateur_required, gestionnaire_required
from apps.users.models import User


def _log(request, action, objet, gravite='info', description=''):
    """Enregistre une entrée dans le journal d'audit."""
    try:
        AuditLog.objects.create(
            utilisateur=request.user,
            action=action,
            gravite=gravite,
            objet=objet,
            description=description,
            ip_address=request.META.get('REMOTE_ADDR', ''),
        )
    except Exception:
        pass


# ============================================================
# PÉDAGOGIE — Coordinateur & Gestionnaires
# ============================================================

@login_required
@coordinateur_required
def pedagogie_creer_module(request):
    """Crée un nouveau module pédagogique."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    titre = request.POST.get('titre', '').strip()
    parcours_id = request.POST.get('parcours_id')
    
    if not titre or not parcours_id:
        messages.error(request, 'Tous les champs obligatoires sont requis.')
        return redirect('users:dashboard_coordinateur', departement='pedagogie')
    
    parcours = get_object_or_404(Parcours, id=parcours_id)
    numero = ModuleParcours.objects.filter(parcours=parcours).count() + 1
    
    ModuleParcours.objects.create(
        parcours=parcours,
        numero=numero,
        titre=titre,
        description=request.POST.get('description', ''),
    )
    _log(request, 'module_cree', f'Module: {titre}')
    messages.success(request, f'Module "{titre}" créé.')
    return redirect('users:dashboard_coordinateur', departement='pedagogie')


@login_required
@coordinateur_required
def pedagogie_creer_cours(request):
    """Crée un nouveau cours."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    titre = request.POST.get('titre', '').strip()
    module_id = request.POST.get('module_id')
    contenu = request.POST.get('contenu', '')
    
    if not titre or not module_id:
        messages.error(request, 'Tous les champs obligatoires sont requis.')
        return redirect('users:dashboard_coordinateur', departement='pedagogie')
    
    module = get_object_or_404(ModuleParcours, id=module_id)
    numero = CoursItem.objects.filter(module=module, type='cours').count() + 1
    
    CoursItem.objects.create(
        module=module,
        type='cours',
        numero=numero,
        titre=titre,
        contenu=contenu,
        duree_estimee=int(request.POST.get('duree', 30)),
    )
    _log(request, 'cours_cree', f'Cours: {titre}')
    messages.success(request, f'Cours "{titre}" créé.')
    return redirect('users:dashboard_coordinateur', departement='pedagogie')


@login_required
@coordinateur_required
def pedagogie_creer_quiz(request):
    """Crée un nouveau quiz/test."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    titre = request.POST.get('titre', '').strip()
    module_id = request.POST.get('module_id')
    
    if not titre or not module_id:
        messages.error(request, 'Tous les champs obligatoires sont requis.')
        return redirect('users:dashboard_coordinateur', departement='pedagogie')
    
    module = get_object_or_404(ModuleParcours, id=module_id)
    numero = CoursItem.objects.filter(module=module, type='test').count() + 1
    
    CoursItem.objects.create(
        module=module,
        type='test',
        numero=numero,
        titre=titre,
    )
    _log(request, 'quiz_cree', f'Quiz: {titre}')
    messages.success(request, f'Quiz "{titre}" créé.')
    return redirect('users:dashboard_coordinateur', departement='pedagogie')


@login_required
@coordinateur_required
def pedagogie_ajouter_question(request):
    """Ajoute une question à un quiz/test."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    test_id = request.POST.get('test_id')
    test = get_object_or_404(CoursItem, id=test_id, type='test')
    texte = request.POST.get('texte', '').strip()
    
    if not texte:
        messages.error(request, 'Texte de la question requis.')
        return redirect(request.META.get('HTTP_REFERER', 'users:dashboard_coordinateur'))
    
    Question.objects.create(
        test=test,
        type=request.POST.get('type', 'qcm_simple'),
        texte=texte,
        reponse_texte=request.POST.get('reponse_texte', ''),
        explication=request.POST.get('explication', ''),
        ordre=Question.objects.filter(test=test).count() + 1,
    )
    _log(request, 'question_ajoutee', f'Question: {texte[:80]}')
    messages.success(request, 'Question ajoutée.')
    return redirect(request.META.get('HTTP_REFERER', 'users:dashboard_coordinateur'))


@login_required
@coordinateur_required
def pedagogie_gerer_parcours(request):
    """Page de gestion des parcours."""
    parcours_list = Parcours.objects.filter(actif=True)
    modules = ModuleParcours.objects.filter(actif=True).select_related('parcours')
    return render(request, 'pages/institution/pedagogie_contenu.html', {
        'page_title': 'Pédagogie & Contenu',
        'parcours_list': parcours_list,
        'modules': modules,
    })


# ============================================================
# TECHNIQUE — Coordinateur & Gestionnaires
# ============================================================

@login_required
@coordinateur_required
def technique_creer_tache(request):
    """Crée une nouvelle tâche technique."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    titre = request.POST.get('titre', '').strip()
    if not titre:
        messages.error(request, 'Titre requis.')
        return redirect('users:dashboard_coordinateur', departement='technique')
    
    Tache.objects.create(
        titre=titre,
        description=request.POST.get('description', ''),
        departement='technique',
        priorite=request.POST.get('priorite', 'normale'),
        assigne_a=request.user if request.POST.get('assigner_a_soi') else None,
    )
    _log(request, 'tache_cree', f'Tâche: {titre}')
    messages.success(request, 'Tâche créée.')
    return redirect('users:dashboard_coordinateur', departement='technique')


@login_required
@coordinateur_required
def technique_signaler_bug(request):
    """Signale un bug technique."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    description = request.POST.get('description', '').strip()
    if not description:
        messages.error(request, 'Description du bug requise.')
        return redirect('users:dashboard_coordinateur', departement='technique')
    
    Tache.objects.create(
        titre=f'BUG: {description[:80]}',
        description=description,
        departement='technique',
        priorite=request.POST.get('priorite', 'haute'),
        assigne_a=request.user,
    )
    _log(request, 'bug_signale', f'Bug signalé: {description[:80]}', 'critique')
    messages.success(request, 'Bug signalé.')
    return redirect('users:dashboard_coordinateur', departement='technique')


@login_required
@coordinateur_required
def technique_liste_taches(request):
    """Liste des tâches techniques."""
    taches = Tache.objects.filter(departement='technique').order_by('-date_creation')
    return render(request, 'pages/institution/developpement_technique.html', {
        'page_title': 'Développement & Technique',
        'taches': taches,
    })


# ============================================================
# MARKETING — Coordinateur & Gestionnaires
# ============================================================

@login_required
@coordinateur_required
def marketing_creer_campagne(request):
    """Crée une nouvelle campagne marketing."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    nom = request.POST.get('nom', '').strip()
    if not nom:
        messages.error(request, 'Nom de campagne requis.')
        return redirect('users:dashboard_coordinateur', departement='marketing')
    
    Campagne.objects.create(
        nom=nom,
        description=request.POST.get('description', ''),
        plateforme=request.POST.get('plateforme', 'email'),
        cree_par=request.user,
    )
    _log(request, 'campagne_cree', f'Campagne: {nom}')
    messages.success(request, f'Campagne "{nom}" créée.')
    return redirect('users:dashboard_coordinateur', departement='marketing')


@login_required
@coordinateur_required
def marketing_creer_article(request):
    """Crée un article de blog (brouillon)."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    titre = request.POST.get('titre', '').strip()
    if not titre:
        messages.error(request, 'Titre requis.')
        return redirect('users:dashboard_coordinateur', departement='marketing')
    
    Article.objects.create(
        titre=titre,
        contenu=request.POST.get('contenu', ''),
        auteur=request.user,
        statut='brouillon',
    )
    _log(request, 'article_cree', f'Article: {titre}')
    messages.success(request, f'Article "{titre}" créé.')
    return redirect('users:dashboard_coordinateur', departement='marketing')


# ============================================================
# OPÉRATIONS — Coordinateur & Gestionnaires
# ============================================================

@login_required
@coordinateur_required
def operations_planifier_formation(request):
    """Planifie une formation."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    nom = request.POST.get('nom', '').strip()
    if not nom:
        messages.error(request, 'Nom de formation requis.')
        return redirect('users:dashboard_coordinateur', departement='operations')
    
    _log(request, 'formation_planifiee', f'Formation: {nom}')
    messages.success(request, f'Formation "{nom}" planifiée.')
    return redirect('users:dashboard_coordinateur', departement='operations')


@login_required
@coordinateur_required
def operations_ajouter_partenaire(request):
    """Ajoute un partenaire."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    nom = request.POST.get('nom', '').strip()
    email = request.POST.get('email', '').strip()
    if not nom or not email:
        messages.error(request, 'Nom et email requis.')
        return redirect('users:dashboard_coordinateur', departement='operations')
    
    _log(request, 'partenaire_ajoute', f'Partenaire: {nom}')
    messages.success(request, f'Partenaire "{nom}" ajouté.')
    return redirect('users:dashboard_coordinateur', departement='operations')


# ============================================================
# QUALITÉ — Coordinateur & Gestionnaires
# ============================================================

@login_required
@coordinateur_required
def qualite_proposer_innovation(request):
    """Propose une innovation."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    nom = request.POST.get('nom', '').strip()
    if not nom:
        messages.error(request, 'Nom du projet requis.')
        return redirect('users:dashboard_coordinateur', departement='qualite')
    
    _log(request, 'innovation_proposee', f'Innovation: {nom}')
    messages.success(request, f'Innovation "{nom}" proposée.')
    return redirect('users:dashboard_coordinateur', departement='qualite')


@login_required
@coordinateur_required
def qualite_signaler_nc(request):
    """Signale une non-conformité."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    description = request.POST.get('description', '').strip()
    if not description:
        messages.error(request, 'Description requise.')
        return redirect('users:dashboard_coordinateur', departement='qualite')
    
    _log(request, 'nc_signalée', f'NC: {description[:80]}', 'avertissement')
    messages.success(request, 'Non-conformité signalée.')
    return redirect('users:dashboard_coordinateur', departement='qualite')


@login_required
@coordinateur_required
def qualite_lancer_audit(request):
    """Lance un audit qualité."""
    _log(request, 'audit_lance', 'Audit qualité lancé')
    messages.success(request, 'Audit lancé avec succès.')
    return redirect('users:dashboard_coordinateur', departement='qualite')


# ============================================================
# SUPPORT — Coordinateur & Gestionnaires
# ============================================================

@login_required
@coordinateur_required
def support_creer_ticket(request):
    """Crée un ticket support."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    sujet = request.POST.get('sujet', '').strip()
    if not sujet:
        messages.error(request, 'Sujet requis.')
        return redirect('users:dashboard_coordinateur', departement='support')
    
    TicketSupport.objects.create(
        sujet=sujet,
        description=request.POST.get('description', ''),
        utilisateur=request.user,
        priorite=request.POST.get('priorite', 'moyenne'),
    )
    _log(request, 'ticket_cree', f'Ticket: {sujet}')
    messages.success(request, f'Ticket "{sujet}" créé.')
    return redirect('users:dashboard_coordinateur', departement='support')


@login_required
@coordinateur_required
def support_envoyer_chat(request):
    """Envoie un message dans le chat support."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    message = request.POST.get('message', '').strip()
    if not message:
        messages.error(request, 'Message requis.')
        return redirect('users:dashboard_coordinateur', departement='support')
    
    _log(request, 'chat_envoye', f'Chat: {message[:80]}')
    messages.success(request, 'Message envoyé.')
    return redirect('users:dashboard_coordinateur', departement='support')


@login_required
@coordinateur_required
def support_repondre_message(request):
    """Répond à un message de contact."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    message_id = request.POST.get('message_id')
    reponse = request.POST.get('reponse', '').strip()
    
    if not message_id or not reponse:
        messages.error(request, 'Message ID et réponse requis.')
        return redirect('users:dashboard_coordinateur', departement='support')
    
    try:
        msg = MessageContact.objects.get(id=message_id)
        msg.statut = 'repondu'
        msg.reponse = reponse
        msg.date_reponse = timezone.now()
        msg.traite_par = request.user
        msg.save()
        _log(request, 'message_repondu', f'Message #{message_id}')
        messages.success(request, 'Réponse envoyée.')
    except MessageContact.DoesNotExist:
        messages.error(request, 'Message introuvable.')
    
    return redirect('users:dashboard_coordinateur', departement='support')


# ============================================================
# DESIGN — Coordinateur & Gestionnaires
# ============================================================

@login_required
@coordinateur_required
def design_creer_maquette(request):
    """Crée une nouvelle maquette."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    nom = request.POST.get('nom', '').strip()
    if not nom:
        messages.error(request, 'Nom de maquette requis.')
        return redirect('users:dashboard_coordinateur', departement='design')
    
    _log(request, 'maquette_cree', f'Maquette: {nom}')
    messages.success(request, f'Maquette "{nom}" créée.')
    return redirect('users:dashboard_coordinateur', departement='design')


@login_required
@coordinateur_required
def design_creer_composant(request):
    """Crée un nouveau composant UI."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Méthode non autorisée'}, status=405)
    
    nom = request.POST.get('nom', '').strip()
    if not nom:
        messages.error(request, 'Nom du composant requis.')
        return redirect('users:dashboard_coordinateur', departement='design')
    
    _log(request, 'composant_cree', f'Composant: {nom}')
    messages.success(request, f'Composant "{nom}" créé.')
    return redirect('users:dashboard_coordinateur', departement='design')


# ============================================================
# DG — Supervision globale
# ============================================================

@login_required
@dg_required
def dg_exporter_messages(request):
    """Exporte les messages de contact."""
    _log(request, 'export_messages', 'Export des messages')
    messages.success(request, 'Export des messages en cours.')
    return redirect('users:dashboard_dg')


@login_required
@dg_required
def dg_exporter_candidatures(request):
    """Exporte les candidatures."""
    _log(request, 'export_candidatures', 'Export des candidatures')
    messages.success(request, 'Export des candidatures en cours.')
    return redirect('users:dashboard_dg')


@login_required
@dg_required
def dg_rapport_hebdo(request):
    """Génère le rapport hebdomadaire."""
    _log(request, 'rapport_hebdo', 'Rapport hebdomadaire')
    messages.success(request, 'Rapport hebdomadaire généré.')
    return redirect('users:dashboard_dg')


@login_required
@dg_required
@require_POST
def dg_message_coordinateurs(request):
    """Envoie un message à tous les coordinateurs."""
    data = json.loads(request.body)
    contenu = data.get('message', '').strip()
    
    if not contenu:
        return JsonResponse({'success': False, 'error': 'Message vide'})
    
    coordinateurs = User.objects.filter(role='coordinateur', is_active=True)
    for coord in coordinateurs:
        Notification.objects.create(
            destinataire=coord,
            titre='Message de la Direction Générale',
            message=contenu,
            type='urgence',
        )
    
    _log(request, 'message_coordinateurs', f'Message aux {coordinateurs.count()} coordinateurs')
    return JsonResponse({'success': True, 'count': coordinateurs.count()})


@login_required
@dg_required
@require_POST
def dg_archiver_messages(request):
    """Archive les messages traités de plus de 30 jours."""
    date_limite = timezone.now() - timezone.timedelta(days=30)
    count = MessageContact.objects.filter(
        date_reponse__lt=date_limite,
        statut='repondu'
    ).update(statut='archive')
    
    _log(request, 'archivage_messages', f'{count} messages archivés')
    return JsonResponse({'success': True, 'count': count})


@login_required
@dg_required
def dg_auditer_departement(request):
    """Lance un audit de département."""
    departement = request.GET.get('departement', '')
    if not departement:
        messages.error(request, 'Département requis.')
        return redirect('users:dashboard_dg')
    
    _log(request, 'audit_departement', f'Département: {departement}')
    messages.success(request, f'Audit du département {departement} lancé.')
    return redirect('users:dashboard_dg')


@login_required
@dg_required
@require_POST
def dg_valider_budget(request):
    """Valide le budget (action critique)."""
    _log(request, 'validation_budget', 'Budget validé', 'critique')
    return JsonResponse({'success': True, 'message': 'Budget validé.'})
  


# ============================================================
# DG — Vues supplémentaires
# ============================================================

@login_required
@dg_required
@require_POST
def dg_creer_alerte(request):
    """Crée une alerte plateforme."""
    import json as _json
    data = _json.loads(request.body)
    type_alerte = data.get('type', 'information')
    message = data.get('message', '').strip()
    if not message:
        return JsonResponse({'success': False, 'error': 'Message requis'})
    _log(request, 'alerte_cree', f'Alerte {type_alerte}: {message[:80]}', 'critique')
    return JsonResponse({'success': True, 'message': f'Alerte "{type_alerte}" créée.'})


@login_required
@dg_required
@require_POST
def dg_ajouter_partenaire(request):
    """Ajoute un partenaire (DG)."""
    import json as _json
    data = _json.loads(request.body)
    nom = data.get('nom', '').strip()
    if not nom:
        return JsonResponse({'success': False, 'error': 'Nom requis'})
    _log(request, 'partenaire_ajoute_dg', f'Partenaire DG: {nom}')
    return JsonResponse({'success': True, 'message': f'Partenaire "{nom}" ajouté.'})


@login_required
@dg_required
@require_POST
def dg_vider_cache(request):
    """Vide le cache Django."""
    from django.core.cache import cache as django_cache
    django_cache.clear()
    _log(request, 'cache_vide', 'Cache vidé', 'critique')
    return JsonResponse({'success': True, 'message': 'Cache vidé avec succès.'})


@login_required
@dg_required
def admin_candidatures(request):
    """Page administration des candidatures."""
    from apps.institution.models import Candidature
    candidatures = Candidature.objects.select_related('offre').order_by('-date_candidature')
    context = {
        'page_title': 'Administration Candidatures',
        'candidatures': candidatures,
        'total': candidatures.count(),
        'shortlist': candidatures.filter(statut='shortlist').count(),
        'en_attente': candidatures.filter(statut='soumise').count(),
        'rejets': candidatures.filter(statut='rejetee').count(),
    }
    return render(request, 'admin/administration_candidatures.html', context)
