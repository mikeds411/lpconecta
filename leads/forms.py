from django import forms

from .models import Agendamento, Contato

ESPECIALIDADES = [
    "Psicologia", "Odontologia", "Fisioterapia", "Nutrição", "Enfermagem", "Fonoaudiologia",
    "Educação Física", "Farmácia", "Biomedicina", "Serviço Social", "Terapia Ocupacional", "Pedagogia",
]


class LgpdMixin(forms.Form):
    consentimento_lgpd = forms.BooleanField(required=True, error_messages={
        "required": "É preciso aceitar a Política de Privacidade."})
    # Campo invisível: robôs costumam preenchê-lo, pessoas não.
    site = forms.CharField(required=False)

    def is_bot(self):
        return bool(self.data.get("site"))


class AgendamentoForm(LgpdMixin, forms.ModelForm):
    especialidade = forms.ChoiceField(choices=[(e, e) for e in ESPECIALIDADES])
    periodo = forms.ChoiceField(choices=[("Manhã", "Manhã"), ("Tarde", "Tarde")])

    class Meta:
        model = Agendamento
        fields = ["nome", "whatsapp", "especialidade", "periodo", "consentimento_lgpd"]

    def clean_whatsapp(self):
        v = self.cleaned_data["whatsapp"]
        if len([c for c in v if c.isdigit()]) < 10:
            raise forms.ValidationError("Informe o WhatsApp com DDD.")
        return v


class ContatoForm(LgpdMixin, forms.ModelForm):
    class Meta:
        model = Contato
        fields = ["nome", "email", "telefone", "mensagem", "consentimento_lgpd"]
