from django.db import models
from django.conf import settings


class MessageContact(models.Model):
    CATEGORIE_CHOICES = [
        ('general', 'Général'),
        ('pedagogie', 'Pédagogie'),
        ('technique', 'Technique'),
        ('marketing', 'Marketing'),
        ('operations', 'Opérations'),
        ('qualite', 'Qualité'),
        ('support', 'Support'),
        ('design', 'Design'),
        ('facturation', 'Facturation'),
    ]

    STATUT_CHOICES = [
        ('non_lu', 'Non lu'),
        ('lu', 'Lu'),
        ('repondu', 'Répondu'),
        ('archive', 'Archivé'),
    ]

    nom = models.CharField(max_length=200)
    email = models.EmailField()
    sujet = models.CharField(max_length=300)
    message = models.TextField()
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES, default='general')
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='non_lu')
    date_envoi = models.DateTimeField(auto_now_add=True)
    reponse = models.TextField(blank=True)
    date_reponse = models.DateTimeField(null=True, blank=True)
    traite_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='messages_traites',
    )

    class Meta:
        verbose_name = 'Message de contact'
        verbose_name_plural = 'Messages de contact'
        ordering = ['-date_envoi']

    def __str__(self):
        return f"{self.nom} — {self.sujet}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('succes', 'Succès'),
        ('avertissement', 'Avertissement'),
        ('erreur', 'Erreur'),
        ('urgence', 'Urgence'),
    ]

    destinataire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    titre = models.CharField(max_length=300)
    message = models.TextField()
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='info')
    lue = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    lien = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Notification'
        ordering = ['-date_creation']

    def __str__(self):
        return f"{self.destinataire} — {self.titre}"
