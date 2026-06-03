"""Tests du module Forum."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.forum.models import Forum, Sujet, Message

User = get_user_model()


class ForumTestCase(TestCase):
    """Tests des forums communautaires."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.login(email='test@example.com', password='testpass123')
        
        self.forum = Forum.objects.create(
            metier='pilote_de_ligne',
            nom='Forum Pilote de Ligne',
            actif=True,
            ordre=1
        )

    def test_forum_index_200(self):
        """La page d'accueil du forum doit retourner 200."""
        response = self.client.get(reverse('forum:index'))
        self.assertEqual(response.status_code, 200)

    def test_forum_metier_200(self):
        """La page d'un forum par métier doit retourner 200."""
        response = self.client.get(
            reverse('forum:metier', kwargs={'metier': 'pilote_de_ligne'})
        )
        self.assertEqual(response.status_code, 200)

    def test_nouveau_sujet_200(self):
        """La page de création d'un nouveau sujet doit retourner 200."""
        response = self.client.get(
            reverse('forum:nouveau_sujet', kwargs={'metier': 'pilote_de_ligne'})
        )
        self.assertEqual(response.status_code, 200)

    def test_creer_sujet_post(self):
        """La création d'un nouveau sujet doit réussir."""
        response = self.client.post(
            reverse('forum:nouveau_sujet', kwargs={'metier': 'pilote_de_ligne'}),
            {
                'titre': 'Mon premier sujet',
                'contenu': 'Contenu de mon premier message'
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Sujet.objects.filter(titre='Mon premier sujet').exists())
