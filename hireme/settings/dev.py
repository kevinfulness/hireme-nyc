from .common import *

DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_LOCATION = 'static'
STATIC_URL = 'static/'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_LOCATION = 'media'
MEDIA_URL = 'media/'
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_UPLOAD_PREFIX = ''
# Use local file storage for development
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
# DEFAULT_FILE_STORAGE = 'hireme.storage_backends.PublicMediaStorage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
