"""Middleware maintenance et sécurité."""


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclure les chemins critiques
        if request.path.startswith('/admin/') or \
           request.path.startswith('/static/') or \
           request.path.startswith('/media/') or \
           request.path == '/health/':
            return self.get_response(request)
        
        try:
            from .models import SiteConfig
            config = SiteConfig.objects.first()
            if config and config.maintenance_mode and not request.user.is_superuser:
                from django.shortcuts import render
                return render(request, 'errors/maintenance.html', status=503)
        except Exception:
            pass
        
        return self.get_response(request)


class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['X-XSS-Protection'] = '1; mode=block'
        return response
