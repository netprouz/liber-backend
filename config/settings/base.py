import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = 'znf0%dw+9+q8ey-*i)e9g7x+v77e#94&rn*v!%dx+1tshpxke6'

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "django_extensions",
    "phonenumber_field",
    "django_filters",
    "rest_framework_swagger",
    "storages",
    "paycomuz",
    "clickuz",
]

LOCAL_APPS = [
    "main.apps.account.apps.AccountConfig",
    "main.apps.common.apps.CommonConfig",
    "main.apps.category.apps.CategoryConfig",
    "main.apps.book.apps.BookConfig",
    "main.apps.subscription.apps.SubscriptionConfig",
    "main.apps.order.apps.OrderConfig",
    "main.apps.stats.apps.StatsConfig",
    "main.apps.transaction.apps.TransactionConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

AUTH_USER_MODEL = "account.User"

ROOT_URLCONF = "config.urls"

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
            "libraries": {
                "staticfiles": "django.templatetags.static",
            },
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

REST_FRAMEWORK = {
    #"DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
    #    "rest_framework.authentication.BasicAuthentication",
    #    "rest_framework.authentication.SessionAuthentication",
    #    "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "main.apps.common.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        # "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}

DATABASES = {
       "default": {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": os.environ.get("POSTGRES_HOST"),
        "NAME": os.environ.get("POSTGRES_DB"),
        "PORT": os.environ.get("POSTGRES_PORT"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
    }
}

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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MEDIA_URL = "/media/"
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "main", "static_files"),)
MEDIA_ROOT = os.path.join(BASE_DIR, "main", "media/")
STATIC_ROOT = os.path.join(BASE_DIR, "main", "static/")

ONLINE = "online"
PAPER = "paper"
AUDIO = "audio"

PERMANENT = "permanent"
TEMPORARY = "temporary"

SMS_TOKEN = os.environ.get("SMS_TOKEN")
SMS_DOMAIN = os.environ.get("SMS_DOMAIN")

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_FILE_OVERWRITE = os.environ.get("AWS_S3_FILE_OVERWRITE")
DEFAULT_FILE_STORAGE = os.environ.get("DEFAULT_FILE_STORAGE")
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_S3_REGION_NAME = "us-east-1"
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_ALL_ORIGINS = True
PAYCOM_SETTINGS = {
    "KASSA_ID": '6229ec614fed152a1068002a',  # token
    # TODO: TOKEN key was not declared in the docs, find out and remove if needed
    "TOKEN": os.environ.get("MERCHANT_ID"),  # token
    "SECRET_KEY": os.environ.get("MERCHANT_SECRET_KEY"),  # password
    "ACCOUNTS": {"KEY": "order_id"},
}

PAYME_PRICE_HELPER = 100

CLICK_SETTINGS = {
    "service_id": os.environ.get("CLICK_SERVICE_ID"),
    "merchant_id": os.environ.get("CLICK_MERCHANT_ID"),
    "merchant_user_id": os.environ.get("CLICK_MERCHANT_USER_ID"),
    "secret_key": os.environ.get("CLICK_SECRET_KEY"),
}