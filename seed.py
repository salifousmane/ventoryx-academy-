"""
Seed defaults : utilisateurs, parcours, forums, contenus pédagogiques.
Respecte intégralement le manifeste Ventoryx Academy.
"""
import os
import json
from datetime import timedelta
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()
DEFAULT_PASSWORD = os.getenv("VENTORYX_DEFAULT_PWD", "ChangeMe!2026")

# ============================================================
# CONFIGURATION DES 8 MÉTIERS (SEED)
# ============================================================

METIERS = {
    'pilote_de_ligne': {
        'nom': 'Pilote de Ligne',
        'icone': 'fa-plane',
        'gratuit': False,
        'modules': [
            {'numero': 1, 'titre': 'Découverte du cockpit', 'description': 'Instruments de bord, commandes et environnement du poste de pilotage.'},
            {'numero': 2, 'titre': 'Commandes de vol', 'description': 'Manche, palonnier, manette des gaz et surfaces de contrôle.'},
            {'numero': 3, 'titre': 'Décollage et montée', 'description': 'Procédures de décollage, V1/Vr/V2, montée initiale.'},
            {'numero': 4, 'titre': 'Atterrissage et approche', 'description': 'Alignement, pente d\'approche, flare et toucher des roues.'},
        ],
    },
    'personnel_navigant': {
        'nom': 'Personnel Navigant (PNC)',
        'icone': 'fa-user-friends',
        'gratuit': False,
        'modules': [
            {'numero': 1, 'titre': 'Connaissance de la cabine', 'description': 'Environnement cabine, équipements de sécurité.'},
            {'numero': 2, 'titre': 'Procédures normales', 'description': 'Démonstrations de sécurité, service à bord.'},
            {'numero': 3, 'titre': 'Turbulences et incidents', 'description': 'Gestion des turbulences et malaises passagers.'},
            {'numero': 4, 'titre': 'Évacuation d\'urgence', 'description': 'Dépressurisation, atterrissage d\'urgence, évacuation.'},
        ],
    },
    'ingenieur_aeronautique': {
        'nom': 'Ingénieur Aéronautique',
        'icone': 'fa-cogs',
        'gratuit': False,
        'modules': [
            {'numero': 1, 'titre': 'Les forces en vol', 'description': 'Portance, poids, traînée et poussée.'},
            {'numero': 2, 'titre': 'La portance', 'description': 'Aérodynamique, profils d\'aile, génération de portance.'},
            {'numero': 3, 'titre': 'Le décrochage', 'description': 'Phénomène de décrochage, angle critique, récupération.'},
            {'numero': 4, 'titre': 'Optimisation du vol', 'description': 'Masse, altitude, vitesse et consommation.'},
        ],
    },
    'controleur_aerien': {
        'nom': 'Contrôleur Aérien',
        'icone': 'fa-tower-broadcast',
        'gratuit': True,
        'modules': [
            {'numero': 1, 'titre': 'Le radar', 'description': 'Lecture des écrans radar, étiquettes, informations de vol.'},
            {'numero': 2, 'titre': 'Les clairances', 'description': 'Phraséologie et instructions de contrôle.'},
            {'numero': 3, 'titre': 'La séparation', 'description': 'Distances minimales entre aéronefs.'},
            {'numero': 4, 'titre': 'Gestion d\'urgence', 'description': 'Situations d\'urgence, pannes radio, déroutements.'},
        ],
    },
    'technicien_aeronautique': {
        'nom': 'Technicien Aéronautique',
        'icone': 'fa-tools',
        'gratuit': True,
        'modules': [
            {'numero': 1, 'titre': 'Technologie de base', 'description': 'Matériaux, documentation technique, réglementation.'},
            {'numero': 2, 'titre': 'Systèmes avion', 'description': 'Hydraulique, pneumatique, circuits électriques.'},
            {'numero': 3, 'titre': 'Maintenance avionique', 'description': 'Instruments, communication, diagnostic.'},
            {'numero': 4, 'titre': 'Moteurs', 'description': 'Turboréacteurs, turbopropulseurs, maintenance.'},
        ],
    },
    'mecanicien_avion': {
        'nom': 'Mécanicien Avion',
        'icone': 'fa-wrench',
        'gratuit': False,
        'modules': [
            {'numero': 1, 'titre': 'Structures & Cellules', 'description': 'Matériaux, assemblage, réparation.'},
            {'numero': 2, 'titre': 'Systèmes hydrauliques', 'description': 'Pompes, vérins, trains, freins.'},
            {'numero': 3, 'titre': 'Commandes de vol', 'description': 'Gouvernes, câbles, vérins.'},
            {'numero': 4, 'titre': 'Expertise', 'description': 'Diagnostic, inspection, test global.'},
        ],
    },
    'agent_escale': {
        'nom': 'Agent d\'Escale',
        'icone': 'fa-suitcase',
        'gratuit': False,
        'modules': [
            {'numero': 1, 'titre': 'Enregistrement & Bagages', 'description': 'Procédures, systèmes DCS, documents.'},
            {'numero': 2, 'titre': 'Embarquement & Piste', 'description': 'Procédures, coordination, sécurité.'},
            {'numero': 3, 'titre': 'Relation client', 'description': 'Accueil, PMR, situations particulières.'},
            {'numero': 4, 'titre': 'Expertise', 'description': 'Coordination, sûreté, test global.'},
        ],
    },
    'formation_avancee': {
        'nom': 'Formation Avancée Premium',
        'icone': 'fa-crown',
        'gratuit': False,
        'premium': True,
        'modules': [
            {'numero': 1, 'titre': 'Gestion de crise', 'description': 'Situations d\'urgence et gestion du stress.'},
            {'numero': 2, 'titre': 'Leadership et CRM', 'description': 'Communication et travail en équipe.'},
            {'numero': 3, 'titre': 'Sécurité approfondie', 'description': 'Analyse des risques et prévention.'},
            {'numero': 4, 'titre': 'Avionique avancée', 'description': 'Systèmes électroniques de bord.'},
            {'numero': 5, 'titre': 'Management', 'description': 'Gestion d\'équipe et optimisation.'},
            {'numero': 6, 'titre': 'Aviation durable', 'description': 'Carburants alternatifs, environnement.'},
        ],
    },
}

CONTENUS_COURS = {
    'pilote_de_ligne': {
        1: """
        <h2>Le poste de pilotage moderne</h2>
        <p>Le cockpit d'un avion de ligne moderne est organisé autour de plusieurs zones fonctionnelles :</p>
        <ul>
            <li><strong>Le tableau de bord principal</strong> : instruments de vol, navigation et moteurs</li>
            <li><strong>La console centrale</strong> : commandes des moteurs, trains d'atterrissage, volets</li>
            <li><strong>Le toit de cockpit</strong> : panneaux de commandes électriques et systèmes</li>
        </ul>
        <div class="highlight-box">
            <strong>À retenir</strong> : Chaque commande a une fonction précise et son emplacement est standardisé pour faciliter la transition entre différents types d'avions.
        </div>
        """,
        2: """
        <h2>Les commandes de vol principales</h2>
        <p>Le pilote dispose de trois commandes principales :</p>
        <ul>
            <li><strong>Le manche (ou sidestick)</strong> : contrôle le tangage et le roulis</li>
            <li><strong>Le palonnier</strong> : contrôle le lacet (direction)</li>
            <li><strong>La manette des gaz</strong> : contrôle la puissance des moteurs</li>
        </ul>
        """,
    },
    'personnel_navigant': {
        1: """
        <h2>La cabine passagers</h2>
        <p>La cabine est organisée pour accueillir les passagers dans les meilleures conditions de sécurité et de confort.</p>
        <ul>
            <li>Issues de secours : portes et fenêtres de secours</li>
            <li>Équipements de sécurité : gilets de sauvetage, masques à oxygène</li>
            <li>Galley : préparation des repas et boissons</li>
        </ul>
        """,
    },
}


def _ensure_user(email, full_name, role, department=None):
    """Crée un utilisateur s'il n'existe pas."""
    user = User.objects.filter(email=email).first()
    if user:
        return user
    parts = full_name.split()
    first = parts[0] if parts else ''
    last = parts[-1] if len(parts) > 1 else ''
    user = User.objects.create_user(email=email, password=DEFAULT_PASSWORD, first_name=first, last_name=last)
    user.role = role
    user.departement = department
    if role == 'dg':
        user.is_dg = True
        user.is_staff = True
    elif role == 'coordinateur':
        user.is_coordinateur = True
    elif role == 'gestionnaire':
        user.is_gestionnaire = True
    user.is_active = True
    user.save()
    return user


def seed_utilisateurs():
    """Crée tous les utilisateurs par défaut."""
    print('👥 Création des utilisateurs...')
    
    # DG
    _ensure_user('dg@ventoryx-academy.com', 'Directeur Général', 'dg')
    
    # Coordinateurs
    for dept, name in [
        ('pedagogie', 'Coordinateur Pédagogie'), ('technique', 'Coordinateur Technique'),
        ('marketing', 'Coordinateur Marketing'), ('operations', 'Coordinateur Opérations'),
        ('qualite', 'Coordinateur Qualité'), ('support', 'Coordinateur Support'),
        ('design', 'Coordinateur Design'),
    ]:
        _ensure_user(f'coord.{dept}@ventoryx-academy.com', name, 'coordinateur', dept)
    
    # Gestionnaires
    for dept, name in [
        ('pedagogie', 'Gestionnaire Pédagogie'), ('technique', 'Gestionnaire Technique'),
        ('marketing', 'Gestionnaire Marketing'), ('operations', 'Gestionnaire Opérations'),
        ('qualite', 'Gestionnaire Qualité'), ('support', 'Gestionnaire Support'),
        ('design', 'Gestionnaire Design UX'),
    ]:
        _ensure_user(f'gest.{dept}@ventoryx-academy.com', name, 'gestionnaire', dept)
    
    print(f'✅ {User.objects.count()} utilisateurs créés.')


def seed_parcours():
    """Crée tous les parcours et leurs modules."""
    from apps.parcours.models import Parcours, ModuleParcours, CoursItem
    
    print('📚 Création des parcours...')
    
    for metier_key, data in METIERS.items():
        parcours, created = Parcours.objects.get_or_create(
            metier=metier_key,
            defaults={
                'nom': data['nom'],
                'icone': data['icone'],
                'gratuit': data.get('gratuit', False),
                'premium': data.get('premium', False),
                'ordre': list(METIERS.keys()).index(metier_key) + 1,
            }
        )
        
        if created:
            print(f'   📖 Création du parcours : {parcours.nom}')
        
        for mod in data['modules']:
            module, module_created = ModuleParcours.objects.get_or_create(
                parcours=parcours, numero=mod['numero'],
                defaults={'titre': mod['titre'], 'description': mod['description']}
            )
            
            if module_created:
                print(f'      📘 Module {mod["numero"]} : {mod["titre"]}')
                
                # Créer les cours pour ce module (20 cours)
                for i in range(1, 21):
                    titre_cours = f'Cours {i} : {mod["titre"]}'
                    contenu_cours = CONTENUS_COURS.get(metier_key, {}).get(i, f"""
                    <h2>{titre_cours}</h2>
                    <p>Ce cours fait partie du module {mod["titre"]} du parcours {data["nom"]}.</p>
                    <p>Le contenu pédagogique complet sera disponible prochainement.</p>
                    <div class="highlight-box">
                        <strong>Objectif pédagogique :</strong> Maîtriser les fondamentaux de {mod["titre"]}.
                    </div>
                    """)
                    
                    CoursItem.objects.get_or_create(
                        module=module, type='cours', numero=i,
                        defaults={
                            'titre': titre_cours,
                            'contenu': contenu_cours,
                            'duree_estimee': 30,
                        }
                    )
                
                # Créer les quiz pour ce module (4 quiz)
                for i in range(1, 5):
                    CoursItem.objects.get_or_create(
                        module=module, type='test', numero=i,
                        defaults={
                            'titre': f'Quiz {i} : Évaluation du module {mod["numero"]}',
                            'duree_estimee': 15,
                        }
                    )
        
        print(f'   ✅ {parcours.nom} : {parcours.modules.count()} modules, {parcours.total_cours} cours')


def seed_forums():
    """Crée les forums par métier."""
    from apps.forum.models import Forum
    
    print('💬 Création des forums...')
    
    for metier_key, data in METIERS.items():
        forum, created = Forum.objects.get_or_create(
            metier=metier_key,
            defaults={
                'nom': data['nom'],
                'icone': data['icone'],
                'ordre': list(METIERS.keys()).index(metier_key) + 1
            }
        )
        
        if created:
            # Ajouter des gestionnaires au forum
            gestionnaires = User.objects.filter(role='gestionnaire', departement='support')[:2]
            if gestionnaires.exists():
                forum.gestionnaires.set(gestionnaires)
            print(f'   💬 Forum créé : {forum.nom}')
    
    print(f'✅ {Forum.objects.count()} forums créés')


def seed_defaults():
    """Fonction principale de seed."""
    if User.objects.count() > 0:
        print('ℹ️  Utilisateurs déjà existants, seed ignoré.')
        print('   Pour forcer le seed, supprimez la base de données.')
        return
    
    print('🌱 Démarrage du seed...')
    seed_utilisateurs()
    seed_parcours()
    seed_forums()
    print('🎉 Seed terminé !')


if __name__ == '__main__':
    import django
    import os
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    django.setup()
    seed_defaults()
