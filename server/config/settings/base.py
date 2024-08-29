"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
from decouple import config, Csv

SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())


# Application definition

INSTALLED_APPS = [
    "daphne",
    "users",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    # Local apps
    "chat",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = "config.urls"
AUTH_USER_MODEL = "users.User"

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

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USERNAME"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOSTNAME"),
        "PORT": config("DB_PORT", cast=int),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

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

# Celery
CELERY_BROKER_URL = config("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = config("REDIS_BACKEND")


# Django Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [config("REDIS_BACKEND")],
        },
    },
}


# ANA Core config
LLAMA_API_URL = config("LLAMA_API_URL")


# Prompts
FUNCTIONALITY_CLF_PROMPT_PATH = os.path.join(
    BASE_DIR, r"core/static/prompts/v1/functionality_template.txt"
)
GREETING_PROMPT = os.path.join(BASE_DIR, r"core/static/prompts/v1/greet_template.txt")
INTENT_PROMPT_PATH = os.path.join(
    BASE_DIR, r"core/static/prompts/v1/intent_template.txt"
)
CONTEXT_PROMPT_PATH = os.path.join(
    BASE_DIR, r"core/static/prompts/v1/context_extraction_template.txt"
)
QUESTION_CATEGORIZATION_PROMPT_PATH = os.path.join(
    BASE_DIR, r"core/static/prompts/v1/question_categories_template.txt"
)
WEATHER_PROMPT_PATH = os.path.join(
    BASE_DIR, r"core/static/prompts/v1/weather_template.txt"
)
BOOK_NAME_PROMPT_PATH = os.path.join(
    BASE_DIR, r"core/static/prompts/v1/book_details_template.txt"
)
CREATE_JOKE_PROMPT_PATH = os.path.join(
    BASE_DIR, r"core/static/prompts/v1/joke_prompt.txt"
)
OTHER_INQUIRY_PROMPT_PATH = os.path.join(
    BASE_DIR, r"core/static/prompts/v1/other_inquiry_template.txt"
)
TIMING_REQ_PROMPT_PATH = os.path.join(
    BASE_DIR, r"core/static/prompts/v1/timing_request_categories_template.txt"
)

BOOKS_ROOT_DIR = r"core/static/books"
# Instructions
EVENT_EXTRACTION_INSTRUCTION_PATH = os.path.join(
    BASE_DIR, r"core/static/instructions/event_extraction.txt"
)

# Responses
HELP_RESPONSE_PATH = os.path.join(BASE_DIR, r"core/static/responses/help_response.txt")

CALENDAR_CREDS_PATH = os.path.join(BASE_DIR, r"core/static/credentials.json")
TEMP_TOKEN_PATH = os.path.join(BASE_DIR, r"core/static/token.pkl")

# Union of prompts
V1_PROMPTS = [
    FUNCTIONALITY_CLF_PROMPT_PATH,
    GREETING_PROMPT,
    INTENT_PROMPT_PATH,
    CONTEXT_PROMPT_PATH,
    QUESTION_CATEGORIZATION_PROMPT_PATH,
    WEATHER_PROMPT_PATH,
    BOOK_NAME_PROMPT_PATH,
    CREATE_JOKE_PROMPT_PATH,
    OTHER_INQUIRY_PROMPT_PATH,
    TIMING_REQ_PROMPT_PATH,
]

V2_PROMPTS = [
    "core/static/prompts/v2/ana_v2_answer.txt",
    "core/static/prompts/v2/ana_v2_ask.txt",
    "core/static/prompts/v2/ana_v2_functions.txt",
    "core/static/prompts/v2/ana_v2_book_verify.txt",
]
