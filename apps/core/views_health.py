"""
Health check endpoint pour monitoring et load balancer
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db import connection

@require_http_methods(["GET"])
def health_check(request):
    """
    Endpoint pour vérifier la santé de l'application
    Utilisé par Fly.io et les load balancers
    """
    try:
        # Vérifier la connexion à la base de données
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat(),
            'app': 'ventoryx-academy',
            'version': '1.0.0'
        }, status=200)
    
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=503)
