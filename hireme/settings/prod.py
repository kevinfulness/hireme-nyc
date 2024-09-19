from .common import *

DEBUG = True

ALLOWED_HOSTS = [
    'hireme-nyc-500432b446dc.herokuapp.com',
    '.hireme.nyc',
    'hireme.nyc',
]


DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True, default=os.environ['HEROKU_POSTGRESQL_PUCE_URL'])
}
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'

#if 'ENGINE' in DATABASES['default'] and 'postgres' in DATABASES['default']['ENGINE']:
#    DATABASES['default']['OPTIONS'] = {'sslmode': 'require'}

django_heroku.settings(locals())

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


AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_REGION_NAME = 'us-east-2'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERITY = True
AWS_QUERYSTRING_AUTH = False

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_LOCATION = 'static'
STATIC_URL = 'https://hireme-image.s3.us-east-2.amazonaws.com/static/'

# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_LOCATION = 'media'
MEDIA_URL = 'https://hireme-image.s3.us-east-2.amazonaws.com/media/'
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_UPLOAD_PREFIX = 'https://hireme-image.s3.us-east-2.amazonaws.com/'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'