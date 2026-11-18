import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conecta.settings")

application = get_wsgi_application()
# A Vercel procura uma variável chamada `app`.
app = application
