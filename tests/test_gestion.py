"""Tests du module Gestion (départements, tâches)."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.gestion.models import Tache

User = get_user_model()


class GestionTestCase(TestCase):
    """Tests des vues de gestion des départements."""

    def setUp(self):
        self.client = Client()
        
        # Créer un coordinateur
        self.coord_user = User.objects.create_user(
            email='coord@test.com',
            password='testpass123',
            first_name='Coord',
            last_name='Test'
        )
        self.coord_user.is_coordinateur = True
        self.coord_user.role = 'coordinateur'
        self.coord_user.departement = 'pedagogie'
        self.coord_user.save()
        
        self.client.login(email='coord@test.com', password='testpass123')

    def test_pedagogie_creer_module(self):
        """La création d'un module doit réussir."""
        from apps.parcours.models import Parcours
        
        parcours = Parcours.objects.create(
            metier='pilote_de_ligne',
            nom='Pilote de Ligne',
            actif=True,
            ordre=1
        )
        
        response = self.client.post(
            reverse('gestion:pedagogie_creer_module'),
            {
                'titre': 'Nouveau module',
                'parcours_id': parcours.id,
                'description': 'Description du module'
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_technique_creer_tache(self):
        """La création d'une tâche technique doit réussir."""
        response = self.client.post(
            reverse('gestion:technique_creer_tache'),
            {
                'titre': 'Tâche technique',
                'description': 'Description de la tâche',
                'priorite': 'haute'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tache.objects.filter(titre='Tâche technique').exists())
