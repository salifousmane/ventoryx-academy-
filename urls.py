"""
Configuration des URLs principales.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os

_sw_js_path = os.path.join(settings.BASE_DIR, 'static', 'js', 'sw.js')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sw.js', serve, {'path': 'js/sw.js', 'document_root': settings.BASE_DIR / 'static'}),
]

urlpatterns += i18n_patterns(
    path('', include('apps.core.urls')),
    path('auth/', include('apps.users.urls')),
    path('parcours/', include('apps.parcours.urls')),
    path('blog/', include('apps.blog.urls')),
    path('institution/', include('apps.institution.urls')),
    path('forum/', include('apps.forum.urls')),
    path('messaging/', include('apps.messaging.urls')),
    path('audit/', include('apps.audit.urls')),
    path('gestion/', include('apps.gestion.urls')),
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
