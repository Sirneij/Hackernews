"""
ASGI config for hackernews project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from decouple import config
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackernews.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', config('settings', default='hackernews.settings.development'))

application = get_asgi_application()
