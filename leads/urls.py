from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/agendamento/", views.agendamento, name="api-agendamento"),
    path("api/contato/", views.contato, name="api-contato"),
    path("api/clique/", views.clique, name="api-clique"),
]
