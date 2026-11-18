import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Agendamento, CliqueWhatsApp, Contato


@admin.action(description="Exportar selecionados para CSV")
def exportar_csv(modeladmin, request, queryset):
    campos = [f.name for f in queryset.model._meta.fields]
    resp = HttpResponse(content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = f'attachment; filename="{queryset.model._meta.model_name}.csv"'
    resp.write("﻿")  # BOM para o Excel abrir acentos corretamente
    w = csv.writer(resp, delimiter=";")
    w.writerow(campos)
    for obj in queryset:
        w.writerow([getattr(obj, c) for c in campos])
    return resp


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ("protocolo", "nome", "whatsapp", "especialidade", "periodo", "status", "criado_em")
    list_filter = ("status", "especialidade", "periodo", "criado_em")
    list_editable = ("status",)
    search_fields = ("protocolo", "nome", "whatsapp")
    readonly_fields = ("protocolo", "criado_em", "consentimento_lgpd", "ip", "user_agent", "origem")
    date_hierarchy = "criado_em"
    actions = [exportar_csv]


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "telefone", "respondido", "criado_em")
    list_filter = ("respondido", "criado_em")
    list_editable = ("respondido",)
    search_fields = ("nome", "email", "mensagem")
    readonly_fields = ("criado_em", "consentimento_lgpd", "ip", "user_agent", "origem")
    date_hierarchy = "criado_em"
    actions = [exportar_csv]


@admin.register(CliqueWhatsApp)
class CliqueWhatsAppAdmin(admin.ModelAdmin):
    list_display = ("criado_em", "clinica", "local", "dispositivo", "origem")
    list_filter = ("clinica", "local", "dispositivo", "criado_em")
    search_fields = ("origem",)
    date_hierarchy = "criado_em"
    actions = [exportar_csv]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
