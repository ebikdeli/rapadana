from django.urls import reverse_lazy

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

SITE_ID = 1

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'rest_framework',
    'django_filters',
    'corsheaders',
    'ckeditor',
    'ckeditor_uploader',
    "debug_toolbar",
    'axes',
    'sorl.thumbnail',
    'django_hosts',
    'constance',

    'watchman',
    # 'django_browser_reload',
    'djmoney',

    # 'django_otp',
    # 'django_otp.plugins.otp_static',
    # 'django_otp.plugins.otp_totp',
    # 'django_otp.plugins.otp_email',  # <- if you want email capability.
    # 'two_factor',
    # 'two_factor.plugins.phonenumber',  # <- if you want phone number capability.
    # 'two_factor.plugins.email',  # <- if you want email capability.
    # 'two_factor.plugins.yubikey',  # <- for yubikey capability.

    # 'rest_framework.authtoken',
    # 'taggit',
    # 'django_quill',
    # 'django_countries',
    # 'social_django',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',

    'modelcluster',
    'taggit',

    'home',
    'apps.accounts.apps.AccountsConfig',
    'apps.apis.apps.ApisConfig',
    'apps.core.apps.CoreConfig',
    'apps.blog',
    'apps.services',

    'constance.backends.database',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',

    "debug_toolbar.middleware.DebugToolbarMiddleware",

    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',        # for per site cache
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',     # for per site cache
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # 'django_otp.middleware.OTPMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # 'django_browser_reload.middleware.BrowserReloadMiddleware',

    'wagtail.contrib.redirects.middleware.RedirectMiddleware',

    'django_hosts.middleware.HostsResponseMiddleware',
    'axes.middleware.AxesMiddleware',
]

ROOT_URLCONF = 'rapadana.urls'

# For django_hosts
ROOT_HOSTCONF = 'rapadana.hosts'

DEFAULT_HOST = 'www'

# PARENT_HOST = 'localhost' if settings.DEBUG else 'example.com'

# if settings.DEBUG:
#     MAIN_PORT = 8000
# else:
#     MAIN_PORT = 443 if settings.SECURE_SSL_REDIRECT else 80

# MAIN_PORT = 8000 if settings.DEBUG else 443 if settings.SECURE_SSL_REDIRECT else 80

# MAIN_SCHEME = 'http' if settings.DEBUG else 'https' if settings.SECURE_SSL_REDIRECT else 'http'


# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR, 
                 os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'apps')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_proccessors.get_user_ip_and_session_key',
                # 'social_django.context_processors.backends',
                # 'social_django.context_processors.login_redirect',
                # 'cart.context_processor.cart_context'
            ],
        },
    },
]

WSGI_APPLICATION = 'rapadana.wsgi.application'

# sqlite3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'apadana.sqlite3'),
        # 'NAME': BASE_DIR / 'db.sqlite3',
        'OPTIONS': {
            'timeout': 20,
                    }
    }
}

"""
# postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rapadana_db',
        'USER': 'rapadana_ehsan',
        'PASSWORD': 'Ehsan19921371',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
"""

# Using django memcache for caching
"""
CACHES = {
    'default': {
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 600                                        # cache never expires
    }
}
"""

# for cache per site:

# CACHE_MIDDLEWARE_ALIAS = 'apadana_cache'

# CACHE_MIDDLEWARE_SECONDS = 900

# CACHE_MIDDLEWARE_KEY_PREFIX = 'mem'

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

AUTH_USER_MODEL = 'accounts.User'

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

THOUSAND_SEPARATOR = ','

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
# To deploy on Host:
# STATIC_ROOT = '/home/rapadana/public_html/static'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR),
]

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# To deploy on Host:
# MEDIA_ROOT = '/home/rapadana/public_html/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Login and Logout urls (django two factor authentication override these settings)
# LOGIN_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = reverse_lazy('admin:login')

# LOGIN_URL = '/login/'
LOGIN_URL = 'admin:login'

# LOGOUT_REDIRECT_URL = 'blog:blog_list'
# LOGOUT_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'index'


AUTHENTICATION_BACKENDS = [
    # AxesBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    'axes.backends.AxesBackend',

    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

# django-axes optional config:
# https://django-axes.readthedocs.io/en/latest/4_configuration.html

AXES_FAILURE_LIMIT = 5
AXES_ONLY_USER_FAILURES = True


# We can also use 'reverse_lazy' to handle login and logout urls

# TAGGIT_CASE_INSENSITIVE = True

# Django social authentication settings:

# SOCIAL_AUTH_POSTGRES_JSONFIELD = True     <==> This is soon to be decapitated
# SOCIAL_AUTH_JSONFIELD_ENABLED = True

"""
AUTHENTICATION_BACKENDS = (
    # google oauth2 backend
    'social_core.backends.google.GoogleOAuth2',

    # normal django auth backend
    'django.contrib.auth.backends.ModelBackend',
)
"""

# ID_KEY and SECRET for google
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '696613813066-qi854fm95mv3h7meen44rbqgcel48mbu.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'KM1oanQONJYFvgtT9BVGu9gy'

# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [...]

# SOCIAL_AUTH_URL_NAMESPACE = 'social'    # It's optional, to make a default namespace for our social auth backend

"""
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ]
}
"""

# cors headers settings

CORS_ALLOW_ALL_ORIGINS = True

# CORS_ALLOWED_ORIGINS = ['http://localhost:3030', ]

# CKEditor settings
# each one of three below is acceptable
# CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
# CKEDITOR_BASEPATH = f"{STATIC_URL}ckeditor/ckeditor/"
CKEDITOR_BASEPATH = (os.path.join(STATIC_URL, 'ckeditor', 'ckeditor', '')).replace("\\", "/")		# Works on windows machine
CKEDITOR_UPLOAD_PATH = "uploads/"
# CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'
# CKEDITOR_IMAGE_BACKEND = "pillow"

# CKEditor optional settings
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
        # 'toolbar': 'basic',
        'height': 600,
        'width': 900,
    },
}

# Wagtail settings

WAGTAIL_SITE_NAME = 'Rapadana'

WAGTAILADMIN_BASE_URL = '/wagtail-admin/'

# This is custom setting for features in wagtail text editor
# https://docs.wagtail.org/en/stable/advanced_topics/customisation/page_editing_interface.html
WAGTAIL_EDITOR_FEAUTURES = [
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code',
    'superscript', 'subscript', 'strikethrough', 'blockquote',
]


# django-constance settings
CONSTANCE_CONFIG = {
    'discount': (5, 'Global discount percent'),
}

CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True

# By default django uses 'redis' to store 'constance' variables. to use database we should follow this document:
# https://django-constance.readthedocs.io/en/latest/backends.html#database
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'


# Django two factor authentication
# LOGIN_URL = 'two_factor:login'

# this one is optional
# LOGIN_REDIRECT_URL = 'two_factor:profile'


# django-debug-toolbar settings

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
