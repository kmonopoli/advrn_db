import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# Security
SECURE_SSL_REDIRECT = True 
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True


SESSION_SECURITY_EXPIRE_AFTER = 1800
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['data.advirna.com','myhost.local']


# Application definition

INSTALLED_APPS = (
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dapp',
    'dbbackup',
    'session_security',
    'gunicorn',
    'djangosecure',
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',

)

ROOT_URLCONF = 'adv_dj_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
TEMPLATE_CONTEXT_PROCESSORS  = {
    'django.core.context_processors.request',
}


WSGI_APPLICATION = 'adv_dj_proj.wsgi.application'


# Database

DATABASES = {
    'default': {

        'ENGINE':'django.db.backends.mysql',
        'NAME':''
        'USER':''
        'PASSWORD':os.environ.get('DATABASE_PASSWORD'),
        'HOST':'us-cdbr-iron-east-03.cleardb.net',
        'PORT':'',


}
}



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True



STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")


DBBACKUP_BACKUP_DIRECTORY = 'path/to/django_dbbackup'
DBBACKUP_CLEANUP_KEEP = 1
DBBACKUP_CLEANUP_KEEP_MEDIA = 1




EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'username@gmail.com'
EMAIL_HOST_PASSWORD =os.environ.get('EMAIL_PASSWORD')
EMAIL_PORT = 587

