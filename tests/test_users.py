"""Tests du module Users (authentification, RBAC, abonnements)."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class UserRegistrationTestCase(TestCase):
    """Tests d'inscription des utilisateurs."""

    def setUp(self):
        self.client = Client()

    def test_register_page_200(self):
        """La page d'inscription doit retourner 200."""
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_valid_data(self):
        """Une inscription avec données valides doit réussir."""
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean.dupont@example.com',
            'nationality': 'Française',
            'date_naissance': '1990-01-01',
            'password1': 'MotDePasseTresLong123!',
            'password2': 'MotDePasseTresLong123!',
            'accepte_cgu': 'on',
            'accepte_confidentialite': 'on',
            'accepte_mentions': 'on',
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(email='jean.dupont@example.com').exists())

    def test_register_invalid_email(self):
        """Une inscription avec email invalide doit échouer."""
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'email_invalide',
            'nationality': 'Française',
            'date_naissance': '1990-01-01',
            'password1': 'MotDePasseTresLong123!',
            'password2': 'MotDePasseTresLong123!',
            'accepte_cgu': 'on',
            'accepte_confidentialite': 'on',
            'accepte_mentions': 'on',
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='email_invalide').exists())

    def test_register_age_minimum(self):
        """Une inscription avec âge < 16 ans doit échouer."""
        data = {
            'first_name': 'Jean',
            'last_name': 'Dupont',
            'email': 'jean.minor@example.com',
            'nationality': 'Française',
            'date_naissance': '2015-01-01',
            'password1': 'MotDePasseTresLong123!',
            'password2': 'MotDePasseTresLong123!',
            'accepte_cgu': 'on',
            'accepte_confidentialite': 'on',
            'accepte_mentions': 'on',
        }
        response = self.client.post(reverse('users:register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='jean.minor@example.com').exists())


class UserLoginTestCase(TestCase):
    """Tests de connexion des utilisateurs."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_login_page_200(self):
        """La page de connexion doit retourner 200."""
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_valid_credentials(self):
        """Une connexion avec identifiants valides doit réussir."""
        response = self.client.post(reverse('users:login'), {
            'username': 'test@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard

    def test_login_invalid_credentials(self):
        """Une connexion avec identifiants invalides doit échouer."""
        response = self.client.post(reverse('users:login'), {
            'username': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email ou mot de passe incorrect')


class RBACDecoratorsTestCase(TestCase):
    """Tests des décorateurs RBAC (dg_required, coordinateur_required)."""

    def setUp(self):
        self.client = Client()
        
        # Création des utilisateurs avec différents rôles
        self.dg_user = User.objects.create_user(
            email='dg@test.com',
            password='testpass123',
            first_name='DG',
            last_name='Test'
        )
        self.dg_user.is_dg = True
        self.dg_user.role = 'dg'
        self.dg_user.save()
        
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
        
        self.normal_user = User.objects.create_user(
            email='normal@test.com',
            password='testpass123',
            first_name='Normal',
            last_name='User'
        )

    def test_dg_dashboard_access_granted(self):
        """Le DG doit avoir accès à son dashboard."""
        self.client.login(email='dg@test.com', password='testpass123')
        response = self.client.get(reverse('users:dashboard_dg'))
        self.assertEqual(response.status_code, 200)

    def test_dg_dashboard_access_denied_for_normal_user(self):
        """Un utilisateur normal ne doit pas avoir accès au dashboard DG."""
        self.client.login(email='normal@test.com', password='testpass123')
        response = self.client.get(reverse('users:dashboard_dg'))
        self.assertEqual(response.status_code, 403)

    def test_coord_dashboard_access_granted(self):
        """Le coordinateur doit avoir accès à son dashboard."""
        self.client.login(email='coord@test.com', password='testpass123')
        response = self.client.get(
            reverse('users:dashboard_coordinateur', kwargs={'departement': 'pedagogie'})
        )
        self.assertEqual(response.status_code, 200)


class SubscriptionTestCase(TestCase):
    """Tests des abonnements et offres de bienvenue."""

    def setUp(self):
        self.client = Client()

    def test_welcome_offer_tier_1(self):
        """Le premier utilisateur doit recevoir l'offre bienvenue tier 1 (365j)."""
        from apps.users.models import Subscription
        
        user1 = User.objects.create_user(
            email='user1@test.com',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        
        # Vérifier que l'abonnement bienvenue a été créé
        self.assertTrue(Subscription.objects.filter(user=user1).exists())
        sub = Subscription.objects.get(user=user1)
        self.assertEqual(sub.plan_type, 'bienvenue_annuel')
        self.assertTrue(sub.end_date > timezone.now() + timedelta(days=360))

    def test_welcome_offer_tier_2(self):
        """Les 2e et 3e utilisateurs doivent recevoir l'offre tier 2 (30j)."""
        from apps.users.models import Subscription
        
        # Créer un premier utilisateur (tier 1)
        User.objects.create_user(
            email='user1@test.com', password='testpass123',
            first_name='User', last_name='One'
        )
        
        # Créer un deuxième utilisateur (tier 2)
        user2 = User.objects.create_user(
            email='user2@test.com', password='testpass123',
            first_name='User', last_name='Two'
        )
        
        sub2 = Subscription.objects.get(user=user2)
        self.assertEqual(sub2.plan_type, 'bienvenue_mensuel')
        self.assertTrue(sub2.end_date > timezone.now() + timedelta(days=25))
        
        # Créer un troisième utilisateur (tier 2 aussi)
        user3 = User.objects.create_user(
            email='user3@test.com', password='testpass123',
            first_name='User', last_name='Three'
        )
        
        sub3 = Subscription.objects.get(user=user3)
        self.assertEqual(sub3.plan_type, 'bienvenue_mensuel')
