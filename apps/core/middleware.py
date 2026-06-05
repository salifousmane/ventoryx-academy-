from django.shortcuts import render
from django.conf import settings


class MaintenanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            from apps.core.models import SiteConfig
            config = SiteConfig.objects.filter(pk=1).first()
            if config and config.maintenance_mode:
                if not request.user.is_authenticated or not getattr(request.user, 'is_dg', False):
                    if not request.path.startswith('/admin'):
                        return render(request, 'errors/maintenance.html', status=503)
        except Exception:
            pass

        response = self.get_response(request)
        return response
