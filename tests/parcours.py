"""Tests du module Parcours (formations, cours, quiz, progression)."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.parcours.models import Parcours, ModuleParcours, CoursItem

User = get_user_model()


class ParcoursModelsTestCase(TestCase):
    """Tests des modèles Parcours."""

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        
        # Créer un parcours de test
        self.parcours = Parcours.objects.create(
            metier='pilote_de_ligne',
            nom='Pilote de Ligne',
            gratuit=False,
            actif=True,
            ordre=1
        )
        
        # Créer un module
        self.module = ModuleParcours.objects.create(
            parcours=self.parcours,
            numero=1,
            titre='Module 1',
            actif=True
        )
        
        # Créer un cours
        self.cours = CoursItem.objects.create(
            module=self.module,
            type='cours',
            numero=1,
            titre='Cours 1',
            contenu='<p>Contenu du cours</p>',
            actif=True
        )

    def test_parcours_creation(self):
        """La création d'un parcours doit réussir."""
        self.assertEqual(self.parcours.nom, 'Pilote de Ligne')
        self.assertEqual(self.parcours.total_modules, 1)

    def test_module_creation(self):
        """La création d'un module doit réussir."""
        self.assertEqual(self.module.titre, 'Module 1')
        self.assertEqual(self.module.cours_count, 20)  # Valeur par défaut

    def test_cours_creation(self):
        """La création d'un cours doit réussir."""
        self.assertEqual(self.cours.titre, 'Cours 1')
        self.assertIn('Contenu du cours', self.cours.contenu)


class ParcoursViewsTestCase(TestCase):
    """Tests des vues du module Parcours."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.login(email='test@example.com', password='testpass123')
        
        # Créer un parcours gratuit pour les tests
        self.parcours_gratuit = Parcours.objects.create(
            metier='controleur_aerien',
            nom='Contrôleur Aérien',
            gratuit=True,
            actif=True,
            ordre=1
        )
        
        self.module = ModuleParcours.objects.create(
            parcours=self.parcours_gratuit,
            numero=1,
            titre='Module Test',
            actif=True
        )
        
        self.cours = CoursItem.objects.create(
            module=self.module,
            type='cours',
            numero=1,
            titre='Cours Test',
            contenu='<p>Contenu du test</p>',
            actif=True
        )

    def test_selection_metier_200(self):
        """La page de sélection des métiers doit retourner 200."""
        response = self.client.get(reverse('parcours:selection_metier'))
        self.assertEqual(response.status_code, 200)

    def test_accueil_parcours_200(self):
        """La page d'accueil d'un parcours doit retourner 200."""
        response = self.client.get(
            reverse('parcours:accueil_parcours', kwargs={'metier': 'controleur_aerien'})
        )
        self.assertEqual(response.status_code, 200)

    def test_cours_200(self):
        """La page d'un cours doit retourner 200."""
        response = self.client.get(
            reverse('parcours:cours', kwargs={
                'metier': 'controleur_aerien',
                'module_num': 1,
                'cours_num': 1
            })
        )
        self.assertEqual(response.status_code, 200)

    def test_cours_404_invalid_module(self):
        """Un module invalide doit retourner 404."""
        response = self.client.get(
            reverse('parcours:cours', kwargs={
                'metier': 'controleur_aerien',
                'module_num': 999,
                'cours_num': 1
            })
        )
        self.assertEqual(response.status_code, 404)


class ProgressionTestCase(TestCase):
    """Tests de la progression utilisateur."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.login(email='test@example.com', password='testpass123')
        
        self.parcours = Parcours.objects.create(
            metier='pilote_de_ligne',
            nom='Pilote de Ligne',
            gratuit=False,
            actif=True,
            ordre=1
        )
        
        self.module = ModuleParcours.objects.create(
            parcours=self.parcours,
            numero=1,
            titre='Module Test',
            actif=True
        )
        
        self.cours = CoursItem.objects.create(
            module=self.module,
            type='cours',
            numero=1,
            titre='Cours Test',
            actif=True
        )

    def test_terminer_cours_api(self):
        """L'API de fin de cours doit marquer le cours comme terminé."""
        from apps.parcours.models import ProgressionUtilisateur
        
        response = self.client.post(
            reverse('parcours:terminer_cours'),
            {'item_id': self.cours.id},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        
        progression = ProgressionUtilisateur.objects.filter(
            user=self.user,
            item=self.cours
        ).first()
        self.assertIsNotNone(progression)
        self.assertTrue(progression.termine)
