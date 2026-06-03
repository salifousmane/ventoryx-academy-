"""
Vues parcours : sélection, accueil, cours, test, test global.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.utils import timezone
from .models import Parcours, ModuleParcours, CoursItem, ProgressionUtilisateur, Question, Reponse
from apps.core.notifications import (
    certificat_delivre, test_global_reussi, quiz_reussi, quiz_echoue
)


@login_required
def selection_metier(request):
    metiers = Parcours.objects.filter(actif=True).order_by('ordre')
    for metier in metiers:
        progressions = ProgressionUtilisateur.objects.filter(user=request.user, parcours=metier)
        total = metier.total_cours
        termine = progressions.filter(termine=True).count()
        metier.progression = int((termine / max(total, 1)) * 100) if total > 0 else 0
        metier.total_cours = total
        metier.total_tests = metier.total_quiz

    return render(request, 'parcours/selection_metier.html', {
        'page_title': 'Sélection du parcours',
        'metiers': metiers,
    })


@login_required
def accueil_parcours(request, metier):
    parcours = get_object_or_404(Parcours, metier=metier, actif=True)
    modules = ModuleParcours.objects.filter(parcours=parcours, actif=True).order_by('numero')

    if not parcours.gratuit and not parcours.premium:
        if not request.user.abonnement_actif:
            return redirect('core:premium')
    if parcours.premium:
        try:
            sub = request.user.subscription
            if not sub.est_active() or sub.plan_type not in ['annuel', 'bienvenue_annuel']:
                return redirect('core:premium')
        except Exception:
            return redirect('core:premium')

    module_precedent_termine = True
    for module in modules:
        items = module.items.filter(actif=True)
        total = items.count()
        termine = ProgressionUtilisateur.objects.filter(
            user=request.user, parcours=parcours, module=module, termine=True
        ).count()
        module.progression = int((termine / max(total, 1)) * 100) if total > 0 else 0
        module.debloque = module_precedent_termine
        if module.progression < 100:
            module_precedent_termine = False

    test_global_debloque = all(m.progression >= 100 for m in modules)

    return render(request, 'parcours/accueil_parcours.html', {
        'page_title': parcours.nom,
        'metier': metier,
        'parcours': parcours,
        'modules': modules,
        'test_global_debloque': test_global_debloque,
    })


@login_required
def cours(request, metier, module_num, cours_num):
    parcours = get_object_or_404(Parcours, metier=metier, actif=True)
    module = get_object_or_404(ModuleParcours, parcours=parcours, numero=module_num, actif=True)
    cours_item = get_object_or_404(CoursItem, module=module, numero=cours_num, type='cours', actif=True)

    if module_num > 1:
        module_precedent = ModuleParcours.objects.get(parcours=parcours, numero=module_num - 1)
        progression_precedente = ProgressionUtilisateur.objects.filter(
            user=request.user, parcours=parcours, module=module_precedent
        )
        if progression_precedente.filter(termine=True).count() < module_precedent.items.filter(actif=True).count():
            return redirect('parcours:accueil_parcours', metier=metier)

    progression, _ = ProgressionUtilisateur.objects.get_or_create(
        user=request.user, parcours=parcours, module=module, item=cours_item
    )

    cours_precedent = CoursItem.objects.filter(
        module=module, type='cours', numero__lt=cours_num, actif=True
    ).order_by('-numero').first()

    cours_suivant = CoursItem.objects.filter(
        module=module, type='cours', numero__gt=cours_num, actif=True
    ).order_by('numero').first()

    test_suivant = None
    if not cours_suivant:
        test_suivant = CoursItem.objects.filter(
            module=module, type='test', actif=True
        ).order_by('numero').first()

    return render(request, 'parcours/cours.html', {
        'page_title': cours_item.titre,
        'metier': metier,
        'parcours': parcours,
        'module': module,
        'cours': cours_item,
        'cours_precedent': cours_precedent,
        'cours_suivant': cours_suivant,
        'test_suivant': test_suivant,
        'progression': progression,
    })


@login_required
def test(request, metier, module_num, test_num):
    parcours = get_object_or_404(Parcours, metier=metier, actif=True)
    module = get_object_or_404(ModuleParcours, parcours=parcours, numero=module_num, actif=True)
    test_item = get_object_or_404(CoursItem, module=module, numero=test_num, type='test', actif=True)

    # Vérifier que tous les cours du module sont terminés
    cours_module = module.items.filter(type='cours', actif=True)
    for c in cours_module:
        if not ProgressionUtilisateur.objects.filter(
            user=request.user, parcours=parcours, module=module, item=c, termine=True
        ).exists():
            messages.warning(request, 'Terminez tous les cours avant de passer le test.')
            return redirect('parcours:accueil_parcours', metier=metier)

    deja_reussi = ProgressionUtilisateur.objects.filter(
        user=request.user, parcours=parcours, module=module, item=test_item, termine=True
    ).exists()

    derniere = ProgressionUtilisateur.objects.filter(
        user=request.user, parcours=parcours, module=module, item=test_item
    ).order_by('-date_modification').first()

    questions = test_item.questions.prefetch_related('reponses').order_by('ordre')

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for i, question in enumerate(questions):
            if question.type == 'qcm_simple' or question.type == 'vrai_faux':
                reponse_id = request.POST.get(f'question_{i}')
                if reponse_id:
                    try:
                        reponse = question.reponses.get(id=reponse_id)
                        if reponse.est_correcte:
                            score += 1
                    except Reponse.DoesNotExist:
                        pass

            elif question.type == 'qcm_multiple':
                reponses_ids = request.POST.getlist(f'question_{i}')
                bonnes = set(question.reponses.filter(est_correcte=True).values_list('id', flat=True))
                donnees = set(int(r) for r in reponses_ids if r.isdigit())
                if donnees == bonnes:
                    score += 1

            elif question.type == 'texte_trous':
                reponse_texte = request.POST.get(f'question_{i}', '').strip().lower()
                attendu = question.reponse_texte.strip().lower()
                if reponse_texte == attendu:
                    score += 1

            elif question.type == 'reorganisation':
                ordre_donne = request.POST.get(f'question_{i}', '')
                if ordre_donne:
                    try:
                        donnees = [int(x) for x in ordre_donne.split(',') if x.isdigit()]
                        correctes = list(question.reponses.order_by('position_correcte').values_list('id', flat=True))
                        if donnees == correctes:
                            score += 1
                    except (ValueError, IndexError):
                        pass

        score_pct = int((score / max(total, 1)) * 100)
        reussi = score_pct >= 70

        progression, _ = ProgressionUtilisateur.objects.get_or_create(
            user=request.user, parcours=parcours, module=module, item=test_item
        )
        progression.tentatives += 1
        if reussi:
            progression.termine = True
            quiz_reussi(request.user, test_item.titre, score_pct)
        else:
            quiz_echoue(request.user, test_item.titre, score_pct)
        progression.score = max(progression.score, score_pct)
        progression.save()

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'score': score_pct,
                'reussi': reussi,
                'total': total,
                'bonnes_reponses': score,
            })

    return render(request, 'parcours/test.html', {
        'page_title': test_item.titre,
        'metier': metier,
        'parcours': parcours,
        'module': module,
        'test': test_item,
        'questions': questions,
        'deja_reussi': deja_reussi,
        'derniere_progression': derniere,
    })


@login_required
def test_global(request, metier):
    parcours = get_object_or_404(Parcours, metier=metier, actif=True)
    modules = ModuleParcours.objects.filter(parcours=parcours, actif=True)

    test_global_debloque = True
    modules_valides = []
    for module in modules:
        total = module.items.filter(actif=True).count()
        termine = ProgressionUtilisateur.objects.filter(
            user=request.user, parcours=parcours, module=module, termine=True
        ).count()
        if termine >= total:
            modules_valides.append(module)
        else:
            test_global_debloque = False

    test_global_item = CoursItem.objects.filter(
        module__parcours=parcours, type='test', actif=True
    ).first()

    deja_reussi = False
    derniere_progression = None
    questions = []

    if test_global_item:
        deja_reussi = ProgressionUtilisateur.objects.filter(
            user=request.user, parcours=parcours, item=test_global_item, termine=True
        ).exists()
        derniere_progression = ProgressionUtilisateur.objects.filter(
            user=request.user, parcours=parcours, item=test_global_item
        ).order_by('-date_modification').first()
        questions = test_global_item.questions.prefetch_related('reponses').order_by('ordre')

        if request.method == 'POST' and test_global_debloque:
            score = 0
            total = questions.count()
            for i, question in enumerate(questions):
                if question.type in ['qcm_simple', 'vrai_faux']:
                    reponse_id = request.POST.get(f'question_{i}')
                    if reponse_id:
                        try:
                            if question.reponses.get(id=reponse_id).est_correcte:
                                score += 1
                        except Reponse.DoesNotExist:
                            pass
                elif question.type == 'qcm_multiple':
                    reponses_ids = request.POST.getlist(f'question_{i}')
                    bonnes = set(question.reponses.filter(est_correcte=True).values_list('id', flat=True))
                    donnees = set(int(r) for r in reponses_ids if r.isdigit())
                    if donnees == bonnes:
                        score += 1
                elif question.type == 'texte_trous':
                    reponse_texte = request.POST.get(f'question_{i}', '').strip().lower()
                    if reponse_texte == question.reponse_texte.strip().lower():
                        score += 1
                elif question.type == 'reorganisation':
                    ordre_donne = request.POST.get(f'question_{i}', '')
                    if ordre_donne:
                        try:
                            donnees = [int(x) for x in ordre_donne.split(',') if x.isdigit()]
                            correctes = list(question.reponses.order_by('position_correcte').values_list('id', flat=True))
                            if donnees == correctes:
                                score += 1
                        except (ValueError, IndexError):
                            pass

            score_pct = int((score / max(total, 1)) * 100)
            reussi = score_pct >= 70

            progression, _ = ProgressionUtilisateur.objects.get_or_create(
                user=request.user, parcours=parcours, item=test_global_item
            )
            progression.tentatives += 1
            if reussi:
                progression.termine = True
            progression.score = max(progression.score, score_pct)
            progression.save()

            # Générer le certificat si réussi
            if reussi:
                from apps.institution.models import Certificat
                import hashlib

                if not Certificat.objects.filter(user=request.user, parcours=parcours.nom).exists():
                    numero = f'VTX-{timezone.now().strftime("%Y%m%d")}-{request.user.id:04d}'
                    chaine = f'{numero}-{request.user.get_full_name()}-{timezone.now()}'
                    hash_sha = hashlib.sha256(chaine.encode()).hexdigest()

                    certificat = Certificat.objects.create(
                        numero_serie=numero,
                        full_name=request.user.get_full_name(),
                        parcours=parcours.nom,
                        user=request.user,
                        hash_verification=hash_sha,
                    )
                    certificat_delivre(request.user, parcours.nom, numero, hash_sha)
                    test_global_reussi(request.user, parcours.nom, score_pct)
                else:
                    test_global_reussi(request.user, parcours.nom, score_pct)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'score': score_pct,
                    'reussi': reussi,
                    'total': total,
                    'bonnes_reponses': score,
                })

    return render(request, 'parcours/test_global.html', {
        'page_title': f'Test Global — {parcours.nom}',
        'metier': metier,
        'parcours': parcours,
        'questions': questions,
        'deja_reussi': deja_reussi,
        'derniere_progression': derniere_progression,
        'test_global_debloque': test_global_debloque,
        'modules_valides': modules_valides,
    })


@login_required
def terminer_cours(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        item_id = data.get('item_id')
        try:
            progression = ProgressionUtilisateur.objects.get(user=request.user, item_id=item_id)
            progression.termine = True
            progression.save()
            return JsonResponse({'ok': True})
        except ProgressionUtilisateur.DoesNotExist:
            return JsonResponse({'ok': False, 'error': 'Non trouvé'})
    return JsonResponse({'ok': False})
