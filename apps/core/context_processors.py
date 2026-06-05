from django.conf import settings


def site_config(request):
    try:
        from apps.core.models import SiteConfig
        config = SiteConfig.objects.filter(pk=1).first()
        return {'site_config': config}
    except Exception:
        return {'site_config': None}


def langue_context(request):
    langue = request.session.get('langue', 'fr')
    return {'langue_active': langue}
