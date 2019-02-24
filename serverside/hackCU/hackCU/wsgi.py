"""
WSGI config for hackCU project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os, sys


sys.path.append('/home/theo/Documents/projects/Website/HackCU-2019-Attention-Monitor/serverside')
sys.path.append('/home/theo/Documents/projects/Website/HackCU-2019-Attention-Monitor/serverside/hackCU')


sys.path.append('/home/theo/Documents/projects/Website/HackCU-2019-Attention-Monitor/serverside/hackCU/hackCU')


from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hackCU.settings')

application = get_wsgi_application()
