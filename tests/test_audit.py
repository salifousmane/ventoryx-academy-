"""Tests du module Audit (journal immutable)."""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionError
from apps.audit.models import AuditLog

User = get_user_model()


class AuditLogTestCase(TestCase):
    """Tests du journal d'audit."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.client.login(email='test@example.com', password='testpass123')

    def test_audit_log_creation(self):
        """La création d'un log d'audit doit réussir."""
        log = AuditLog.objects.create(
            utilisateur=self.user,
            action='connexion',
            objet='Connexion de test',
            ip_address='127.0.0.1'
        )
        self.assertEqual(AuditLog.objects.count(), 1)
        self.assertEqual(log.action, 'connexion')

    def test_audit_log_immutable_modification(self):
        """La modification d'un log d'audit doit être interdite."""
        log = AuditLog.objects.create(
            utilisateur=self.user,
            action='connexion',
            objet='Connexion de test'
        )
        
        with self.assertRaises(PermissionError):
            log.description = 'Tentative de modification'
            log.save()

    def test_audit_log_immutable_deletion(self):
        """La suppression d'un log d'audit doit être interdite."""
        log = AuditLog.objects.create(
            utilisateur=self.user,
            action='connexion',
            objet='Connexion de test'
        )
        
        with self.assertRaises(PermissionError):
            log.delete()

    def test_audit_log_hash_chain(self):
        """La chaîne de hachage doit être générée automatiquement."""
        log1 = AuditLog.objects.create(
            utilisateur=self.user,
            action='connexion',
            objet='Première connexion'
        )
        
        log2 = AuditLog.objects.create(
            utilisateur=self.user,
            action='deconnexion',
            objet='Déconnexion'
        )
        
        self.assertIsNotNone(log1.hash_precedent)
        self.assertIsNotNone(log2.hash_precedent)
        self.assertNotEqual(log1.hash_precedent, log2.hash_precedent)
