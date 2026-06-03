from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Forum, SousForum, Sujet, Message
from apps.users.decorators import gestionnaire_required


def index(request):
    """Page d'accueil du forum - liste tous les forums."""
    forums = Forum.objects.filter(actif=True).prefetch_related('sous_forums').order_by('ordre')
    
    # Ajouter des statistiques pour chaque forum
    for forum in forums:
        forum.total_sujets = forum.sujets.count()
        forum.total_messages = sum(s.total_reponses for s in forum.sujets.all())
    
    context = {
        'forums': forums,
        'page_title': 'Forum communautaire',
    }
    return render(request, 'forum/forum_principal.html', context)


def metier(request, metier):
    """Forum d'un métier spécifique."""
    forum = get_object_or_404(Forum, metier=metier, actif=True)
    sujets = forum.sujets.select_related('auteur').order_by('-est_epingle', '-date_dernier_message')
    
    context = {
        'forum': forum,
        'sujets': sujets,
        'page_title': forum.nom,
    }
    return render(request, 'forum/forum_metier.html', context)


def sous_forum(request, metier, slug):
    """Sous-forum spécifique."""
    forum = get_object_or_404(Forum, metier=metier, actif=True)
    sous_forum_obj = get_object_or_404(SousForum, forum=forum, slug=slug, actif=True)
    sujets = sous_forum_obj.sujets.select_related('auteur').order_by('-est_epingle', '-date_dernier_message')
    
    context = {
        'forum': forum,
        'sous_forum': sous_forum_obj,
        'sujets': sujets,
        'page_title': f"{sous_forum_obj.nom} - {forum.nom}",
    }
    return render(request, 'forum/sous_forum.html', context)


def sujet(request, metier, sujet_id):
    """Affiche un sujet et ses messages."""
    sujet_obj = get_object_or_404(
        Sujet.objects.select_related('forum', 'auteur'),
        id=sujet_id, forum__metier=metier
    )
    
    # Incrémenter les vues
    sujet_obj.total_vues += 1
    sujet_obj.save(update_fields=['total_vues'])
    
    messages_list = sujet_obj.messages.select_related('auteur').order_by('date_creation')
    
    context = {
        'sujet': sujet_obj,
        'messages': messages_list,
        'page_title': sujet_obj.titre,
    }
    return render(request, 'forum/sujet.html', context)


@login_required
def nouveau_sujet(request, metier, slug=None):
    """Créer un nouveau sujet."""
    forum = get_object_or_404(Forum, metier=metier, actif=True)
    sous_forum_obj = None
    
    if slug:
        sous_forum_obj = get_object_or_404(SousForum, forum=forum, slug=slug, actif=True)
    
    if request.method == 'POST':
        titre = request.POST.get('titre', '').strip()
        contenu = request.POST.get('contenu', '').strip()
        
        if titre and contenu:
            sujet_obj = Sujet.objects.create(
                forum=forum,
                sous_forum=sous_forum_obj,
                titre=titre,
                auteur=request.user,
                contenu=contenu,
            )
            # Le premier message est le contenu du sujet
            Message.objects.create(
                sujet=sujet_obj,
                auteur=request.user,
                contenu=contenu,
            )
            messages.success(request, 'Votre sujet a été créé avec succès.')
            return redirect('forum:sujet', metier=metier, sujet_id=sujet_obj.id)
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')
    
    context = {
        'forum': forum,
        'sous_forum': sous_forum_obj,
        'page_title': 'Nouveau sujet',
    }
    return render(request, 'forum/nouveau_sujet.html', context)


@login_required
@require_POST
def repondre_sujet(request, sujet_id):
    """Ajoute une réponse à un sujet (API)."""
    sujet_obj = get_object_or_404(Sujet, id=sujet_id)
    
    if sujet_obj.est_ferme:
        return JsonResponse({'error': 'Ce sujet est fermé'}, status=400)
    
    contenu = request.POST.get('contenu', '').strip()
    if not contenu:
        return JsonResponse({'error': 'Message vide'}, status=400)
    
    message = Message.objects.create(
        sujet=sujet_obj,
        auteur=request.user,
        contenu=contenu,
    )
    
    return JsonResponse({
        'success': True,
        'message': {
            'id': message.id,
            'auteur': message.auteur.get_full_name(),
            'contenu': message.contenu,
            'date': message.date_creation.strftime('%d/%m/%Y à %H:%M'),
        }
    })


@login_required
@gestionnaire_required
def epingler_sujet(request, sujet_id):
    """Épingle ou désépingle un sujet."""
    sujet_obj = get_object_or_404(Sujet, id=sujet_id)
    sujet_obj.est_epingle = not sujet_obj.est_epingle
    sujet_obj.save()
    return JsonResponse({'success': True, 'epingle': sujet_obj.est_epingle})


@login_required
@gestionnaire_required
def fermer_sujet(request, sujet_id):
    """Ferme ou rouvre un sujet."""
    sujet_obj = get_object_or_404(Sujet, id=sujet_id)
    sujet_obj.est_ferme = not sujet_obj.est_ferme
    sujet_obj.save()
    return JsonResponse({'success': True, 'ferme': sujet_obj.est_ferme})
