"""
Django settings for location_indexing project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%mo6c6j3xa%no%v@3^&$-=267%8*lp(bi_di&4-z^&4t@)%p7&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'accounts',#user log-in and registration app
    'sorl.thumbnail',#image manipulation
	'haystack',#search optimazition
    
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',#Tagging app
    'pata_keja',#Our main app
    'django.contrib.admin',
	
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'location_indexing.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'location_indexing.wsgi.application'


# Database connection to Mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS':{
			'read_default_file':'/home/sammy/Dropbox/location_indexing/db_auth.conf',
		},
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Nairobi'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL='/photos/'
MEDIA_ROOT=os.path.join(BASE_DIR, 'photos/')
LOGIN_REDIRECT_URL=reverse_lazy('myboard')
LOGIN_URL=reverse_lazy('accounts:login')
LOGOUT_URL=reverse_lazy('accounts:logout')
#allows using our customized user models to edit profile and log-in with email or username
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'accounts.emailauth.EmailAuthBackend',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

HOUSES_PER_PAGE = 12
#This for more efficient searching of the database using Solr Apache engine which requires haystack
HAYSTACK_CONNECTIONS={
	'default':{
		'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
		'URL': 'http://127.0.0.1:8983/solr/location_indexing'
	},
}