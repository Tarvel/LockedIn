"""
WSGI config for lockedin project.

It exposes the WSGI callable as a module-level variable named ``application``.
Vercel uses this file as the serverless function entry point.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lockedin.settings')

application = get_wsgi_application()

# Vercel expects the handler to be named `app`
app = application
