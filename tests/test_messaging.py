"""Tests du module Messaging (messages, notifications)."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.messaging.models import MessageContact, Notification

User = get_user_model()


class MessagingTestCase(TestCase):
    """Tests des messages et notifications."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.login(email='test@example.com', password='testpass123')

    def test_contact_form_submit(self):
        """L'envoi d'un message de contact doit réussir."""
        response = self.client.post(
            reverse('core:contact'),
            {
                'name': 'Jean Dupont',
                'email': 'jean@example.com',
                'category': 'general',
                'subject': 'Question sur la formation',
                'message': 'Bonjour, j\'ai une question...'
            }
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(MessageContact.objects.filter(email='jean@example.com').exists())

    def test_newsletter_subscription(self):
        """L'inscription à la newsletter doit réussir."""
        response = self.client.post(
            reverse('messaging:newsletter'),
            {'email': 'newsletter@example.com'}
        )
        self.assertEqual(response.status_code, 200)

    def test_notifications_api(self):
        """L'API des notifications doit retourner les notifications de l'utilisateur."""
        Notification.objects.create(
            destinataire=self.user,
            type='info',
            titre='Notification test',
            message='Ceci est un test'
        )
        
        response = self.client.get(reverse('messaging:notifications'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('notifications', data)
        self.assertGreaterEqual(len(data['notifications']), 1)
