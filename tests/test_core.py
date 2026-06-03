"""Tests de base pour Ventoryx Academy - Module Core."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CoreViewsTestCase(TestCase):
    """Tests des vues principales du module Core."""

    def setUp(self):
        self.client = Client()

    def test_index_200(self):
        """La page d'accueil doit retourner 200."""
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)

    def test_faq_200(self):
        """La page FAQ doit retourner 200."""
        response = self.client.get(reverse('core:faq'))
        self.assertEqual(response.status_code, 200)

    def test_contact_200(self):
        """La page contact doit retourner 200."""
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)

    def test_a_propos_200(self):
        """La page À propos doit retourner 200."""
        response = self.client.get(reverse('core:a_propos'))
        self.assertEqual(response.status_code, 200)

    def test_premium_200(self):
        """La page des abonnements doit retourner 200."""
        response = self.client.get(reverse('core:premium'))
        self.assertEqual(response.status_code, 200)

    def test_health_200(self):
        """L'endpoint health doit retourner 200 avec status ok."""
        response = self.client.get(reverse('core:health'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'ok'})

    def test_centre_aide_200(self):
        """La page centre d'aide doit retourner 200."""
        response = self.client.get(reverse('core:centre_aide'))
        self.assertEqual(response.status_code, 200)

    def test_support_technique_200(self):
        """La page support technique doit retourner 200."""
        response = self.client.get(reverse('core:support_technique'))
        self.assertEqual(response.status_code, 200)

    def test_temoignages_200(self):
        """La page témoignages doit retourner 200."""
        response = self.client.get(reverse('core:temoignages'))
        self.assertEqual(response.status_code, 200)

    def test_verification_certificat_200(self):
        """La page vérification certificat doit retourner 200."""
        response = self.client.get(reverse('core:verification_certificat'))
        self.assertEqual(response.status_code, 200)

    def test_programme_metier_200(self):
        """Les pages programme par métier doivent retourner 200."""
        metiers = ['pilote_de_ligne', 'personnel_navigant', 'controleur_aerien', 
                   'technicien_aeronautique', 'ingenieur_aeronautique', 
                   'mecanicien_avion', 'agent_escale', 'formation_avancee']
        for metier in metiers:
            response = self.client.get(
                reverse('core:programme_metier', kwargs={'metier': metier})
            )
            self.assertEqual(response.status_code, 200, f'Erreur pour {metier}')

    def test_programme_metier_404(self):
        """Un métier inconnu doit retourner 404."""
        response = self.client.get(
            reverse('core:programme_metier', kwargs={'metier': 'metier_inconnu'})
        )
        self.assertEqual(response.status_code, 404)

    def test_page_legale_cgu_200(self):
        """La page CGU doit retourner 200."""
        response = self.client.get(
            reverse('core:page_legale', kwargs={'type_page': 'cgu'})
        )
        self.assertEqual(response.status_code, 200)

    def test_page_legale_confidentialite_200(self):
        """La page confidentialité doit retourner 200."""
        response = self.client.get(
            reverse('core:page_legale', kwargs={'type_page': 'confidentialite'})
        )
        self.assertEqual(response.status_code, 200)

    def test_page_legale_mentions_200(self):
        """La page mentions légales doit retourner 200."""
        response = self.client.get(
            reverse('core:page_legale', kwargs={'type_page': 'mentions_legales'})
        )
        self.assertEqual(response.status_code, 200)

    def test_page_legale_404(self):
        """Un type de page légal inconnu doit retourner 404."""
        response = self.client.get(
            reverse('core:page_legale', kwargs={'type_page': 'type_inconnu'})
        )
        self.assertEqual(response.status_code, 404)


class LegalPagesTestCase(TestCase):
    """Tests des pages légales statiques."""

    def setUp(self):
        self.client = Client()

    def test_cgu_content(self):
        """La page CGU doit contenir les articles essentiels."""
        response = self.client.get(
            reverse('core:page_legale', kwargs={'type_page': 'cgu'})
        )
        self.assertContains(response, 'Conditions Générales d\'Utilisation')
        self.assertContains(response, 'Article 1')
        self.assertContains(response, 'Article 35')

    def test_confidentialite_content(self):
        """La page confidentialité doit mentionner le RGPD."""
        response = self.client.get(
            reverse('core:page_legale', kwargs={'type_page': 'confidentialite'})
        )
        self.assertContains(response, 'Politique de confidentialité')
        self.assertContains(response, 'RGPD')

    def test_mentions_legales_content(self):
        """La page mentions légales doit contenir les informations requises."""
        response = self.client.get(
            reverse('core:page_legale', kwargs={'type_page': 'mentions_legales'})
        )
        self.assertContains(response, 'Mentions légales')
        self.assertContains(response, 'Hébergement')


class CoreMiddlewareTestCase(TestCase):
    """Tests des middlewares du module Core."""

    def setUp(self):
        self.client = Client()

    def test_security_headers_present(self):
        """Les en-têtes de sécurité doivent être présents."""
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(response.get('X-Frame-Options'), 'DENY')
        self.assertIsNotNone(response.get('Referrer-Policy'))


class ChatbotAPITestCase(TestCase):
    """Tests de l'API Chatbot."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.login(email='test@example.com', password='testpass123')

    def test_chatbot_api_requires_auth(self):
        """L'API chatbot doit nécessiter une authentification."""
        self.client.logout()
        response = self.client.post(
            reverse('core:chatbot_api'),
            {'question': 'Test question'},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_chatbot_api_post_only(self):
        """L'API chatbot doit accepter uniquement POST."""
        response = self.client.get(reverse('core:chatbot_api'))
        self.assertEqual(response.status_code, 405)

    def test_chatbot_api_empty_question(self):
        """Une question vide doit retourner un message d'erreur."""
        response = self.client.post(
            reverse('core:chatbot_api'),
            {'question': ''},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('reponse', response.json())
