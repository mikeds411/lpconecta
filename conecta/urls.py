from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Conecta Saúde — Painel"
admin.site.site_title = "Conecta Saúde"
admin.site.index_title = "Dados coletados"

urlpatterns = [
    path("painel/", admin.site.urls),
    path("", include("leads.urls")),
]
