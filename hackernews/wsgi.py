"""
WSGI config for hackernews project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from decouple import config
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackernews.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('settings', default='hackernews.settings.development'))

application = get_wsgi_application()
