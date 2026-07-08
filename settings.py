"""
Configuration Django - Ventoryx Academy
Version corrigée et stabilisée.
"""
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# ============================================================
# CHEMINS DE BASE
# ============================================================
BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / 'instance'
INSTANCE_DIR.mkdir(exist_ok=True)

# ============================================================
# SÉCURITÉ - CLÉ SECRÈTE
# ============================================================
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
if not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY est obligatoire")

# ============================================================
# DEBUG
# ============================================================
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"

# ============================================================
# HÔTES AUTORISÉS
# ============================================================
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ============================================================
# ORIGINES CSRF
# ============================================================
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "https://ventoryx-academy.com").split(",")

# ============================================================
# APPLICATIONS INSTALLÉES
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'django_filters',
    'import_export',
    'corsheaders',
    'axes',
    'auditlog',
    'storages',
    'compressor',
    'anymail',
    'csp',
    # Apps locales
    'apps.core',
    'apps.users',
    'apps.parcours',
    'apps.blog',
    'apps.institution',
    'apps.messaging',
    'apps.audit',
    'apps.forum',
    'apps.gestion',
]

# ============================================================
# MIDDLEWARES
# ============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',
    'apps.audit.middleware.AuditMiddleware',
    'apps.core.middleware.MaintenanceMiddleware',
]

# ============================================================
# ROUTAGE
# ============================================================
ROOT_URLCONF = 'urls'

# ============================================================
# TEMPLATES
# ============================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.site_config',
                'apps.core.context_processors.langue_context',
            ],
        },
    },
]

# ============================================================
# WSGI / ASGI
# ============================================================
WSGI_APPLICATION = 'wsgi.application'
ASGI_APPLICATION = 'asgi.application'

# ============================================================
# BASE DE DONNÉES
# ============================================================
if os.getenv('USE_SQLITE', 'True').lower() == 'true':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': INSTANCE_DIR / 'ventoryx.db',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'ventoryx'),
            'USER': os.getenv('DB_USER', 'ventoryx'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
            'ATOMIC_REQUESTS': True,
            'CONN_MAX_AGE': 600,
        }
    }

# ============================================================
# AUTHENTIFICATION
# ============================================================
AUTH_USER_MODEL = 'users.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
    }
}

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 0.25
AXES_LOCKOUT_PARAMETERS = ['username', 'ip_address']
AXES_RESET_ON_SUCCESS = True

ACCOUNT_SIGNUP_FIELDS = ['username*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = {'username', 'email'}

# ============================================================
# SESSIONS
# ============================================================
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_AGE = 14400
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ============================================================
# FICHIERS & MÉDIAS
# ============================================================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

VAULT_ROOT = MEDIA_ROOT / 'vault'

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        'height': 400,
        'width': '100%',
    },
}

# ============================================================
# CSP (django-csp 4.x format)
# ============================================================
CONTENT_SECURITY_POLICY = {
    'DIRECTIVES': {
        'default-src': ("'self'",),
        'script-src': ("'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"),
        'style-src': ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"),
        'font-src': ("'self'", "https://fonts.gstatic.com", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"),
        'img-src': ("'self'", "data:", "https://images.unsplash.com", "https://images.pexels.com", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com"),
        'connect-src': ("'self'",),
        'frame-src': ("'none'",),
    }
}

# ============================================================
# CACHE
# ============================================================
_REDIS_URL = os.getenv('REDIS_URL', '')
if _REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': _REDIS_URL,
            'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }

# ============================================================
# CELERY
# ============================================================
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Paris'

# ============================================================
# CELERY BEAT
# ============================================================
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'backup-quotidien': {
        'task': 'apps.core.tasks.backup_database',
        'schedule': crontab(hour=3, minute=0),
    },
    'nettoyage-comptes-inactifs': {
        'task': 'apps.core.tasks.nettoyer_comptes_inactifs',
        'schedule': crontab(hour=4, minute=0, day_of_week=1),
    },
    'archivage-messages': {
        'task': 'apps.core.tasks.archiver_messages_traites',
        'schedule': crontab(hour=2, minute=0),
    },
    'relance-inactivite-7j': {
        'task': 'apps.core.tasks.envoyer_relances_inactivite_7j',
        'schedule': crontab(hour=10, minute=0),
    },
    'relance-inactivite-30j': {
        'task': 'apps.core.tasks.envoyer_relances_inactivite_30j',
        'schedule': crontab(hour=10, minute=30),
    },
    'rapport-hebdomadaire-dg': {
        'task': 'apps.core.tasks.envoyer_rapport_hebdomadaire',
        'schedule': crontab(hour=8, minute=0, day_of_week=1),
    },
}

# ============================================================
# EMAILS
# ============================================================
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' if DEBUG else 'anymail.backends.sendgrid.EmailBackend'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@ventoryx-academy.com')

# ============================================================
# PAIEMENT
# ============================================================
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')

# ============================================================
# IA
# ============================================================
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')

# ============================================================
# SÉCURITÉ ADDITIONNELLE
# ============================================================
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# ============================================================
# INTERNATIONALISATION
# ============================================================
LANGUAGE_CODE = 'fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
    ('es', 'Español'),
    ('pt', 'Português'),
    ('ar', 'العربية'),
    ('zh', '中文'),
    ('ru', 'Русский'),
    ('de', 'Deutsch'),
    ('it', 'Italiano'),
    ('ja', '日本語'),
    ('ko', '한국어'),
    ('hi', 'हिन्दी'),
    ('tr', 'Türkçe'),
    ('nl', 'Nederlands'),
    ('sv', 'Svenska'),
]

LOCALE_PATHS = [BASE_DIR / 'locale']

# ============================================================
# DÉPARTEMENTS
# ============================================================
DEPARTMENTS = ['pedagogie', 'technique', 'marketing', 'operations', 'qualite', 'support', 'design']

# ============================================================
# SENTRY
# ============================================================
sentry_dsn = os.getenv('SENTRY_DSN', '')
if sentry_dsn:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment=os.getenv('DJANGO_ENV', 'development'),
    )

# ============================================================
# DIVERS
# ============================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AGE_MINIMUM = 16