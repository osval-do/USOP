import os, sys, environ
from pathlib import Path


# PATH VARS
BASE_DIR = Path(__file__).resolve().parent.parent


# ENV FILE
# Defaults to local if an environment is not specified
env = environ.Env(DEBUG=(bool, False))
ENVIRONMENT_NAME = env("ENVIRONMENT_NAME", default="local")
environ.Env.read_env(os.path.join(BASE_DIR, "envs", ENVIRONMENT_NAME + ".env"))


# DJANGO
SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env("DEBUG")
if ENVIRONMENT_NAME=="local":
    DEBUG = True
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    # Django base
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Auth https://docs.allauth.org/en/latest/installation/quickstart.html
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.microsoft",
    # Other third party
    "django_celery_results",
    "django_celery_beat",
    "viewflow",
    # Core apps
    "usop.apps.users",
    "usop.apps.services"
    # Custom apps and services
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]
ROOT_URLCONF = "usop.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
SITE_ID = 1
WSGI_APPLICATION = "usop.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {"default": env.db_url("DATABASE_URL", default="sqlite:///db.sqlite3")}


# AUTH setup
AUTH_USER_MODEL = "users.User"
DJANGO_ADMIN_FORCE_ALLAUTH = True
ACCOUNT_ALLOW_REGISTRATION = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_ADAPTER = "usop.apps.users.adapters.AccountAdapter"
ACCOUNT_FORMS = {"signup": "usop.apps.users.forms.UserSignupForm"}
SOCIALACCOUNT_ADAPTER = "usop.apps.users.adapters.SocialAccountAdapter"
SOCIALACCOUNT_FORMS = {"signup": "usop.apps.users.forms.UserSocialSignupForm"}
MFA_SUPPORTED_TYPES = [
    "webauthn",
    "totp",
    "recovery_codes",
]
MFA_PASSKEY_LOGIN_ENABLED = True


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "static/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Authentication
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]


# CELERY
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_BROKER_TRANSPORT_OPTIONS = {
    "visibility_timeout": 3600,
}


# SERVICE DEPLOYMENT SETTINGS
# TODO expmplain in docs this settings
DRY_RUN = env("DRY_RUN", default=False)
DEFAULT_CONTROLLER = env("DEFAULT_CONTROLLER", default="usop.apps.services.controller.ServiceController")
HELM_COMMAND = ["microk8s","helm"]
KUBECTL_COMMAND = ["microk8s","kubectl"]
DEFAULT_NAMESPACE = env("DEFAULT_NAMESPACE", default="usop_default")
