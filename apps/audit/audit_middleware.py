"""Middleware d'audit automatique."""
from .models import AuditLog


def _get_ip(request):
    """Récupère l'adresse IP réelle du client."""
    x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded:
        return x_forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')


class AuditMiddleware:
    """Middleware enregistrant automatiquement certaines actions dans l'audit."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Enregistrer les actions d'écriture (POST, PUT, PATCH, DELETE)
        if request.user.is_authenticated and request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            # Éviter la surcharge pour les actions fréquentes
            if not request.path.startswith('/api/chatbot/'):
                AuditLog.objects.create(
                    utilisateur=request.user,
                    action=f'methode_{request.method.lower()}',
                    objet=request.path,
                    description=f'Méthode: {request.method} sur {request.path}',
                    ip_address=_get_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
                )

        # Enregistrer les erreurs HTTP
        if response.status_code in [403, 404, 500]:
            gravite = 'avertissement'
            if response.status_code == 500:
                gravite = 'critique'
            
            AuditLog.objects.create(
                utilisateur=request.user if request.user.is_authenticated else None,
                action='erreur',
                gravite=gravite,
                objet=f'HTTP {response.status_code} - {request.path}',
                ip_address=_get_ip(request),
            )

        return response
