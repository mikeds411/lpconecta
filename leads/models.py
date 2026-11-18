import secrets

from django.db import models


class Base(models.Model):
    criado_em = models.DateTimeField("recebido em", auto_now_add=True)
    consentimento_lgpd = models.BooleanField("aceitou a política (LGPD)", default=False)
    ip = models.GenericIPAddressField("IP", null=True, blank=True)
    user_agent = models.CharField("navegador", max_length=300, blank=True)
    origem = models.CharField("página de origem", max_length=300, blank=True)

    class Meta:
        abstract = True
        ordering = ["-criado_em"]


class Agendamento(Base):
    class Status(models.TextChoices):
        NOVO = "novo", "Novo"
        CONTATADO = "contatado", "Contatado"
        CONFIRMADO = "confirmado", "Confirmado"
        CANCELADO = "cancelado", "Cancelado"

    protocolo = models.CharField(max_length=12, unique=True, editable=False)
    nome = models.CharField(max_length=150)
    whatsapp = models.CharField(max_length=30)
    especialidade = models.CharField(max_length=80)
    periodo = models.CharField("período", max_length=20)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NOVO)
    observacoes = models.TextField("observações internas", blank=True)

    class Meta(Base.Meta):
        verbose_name = "agendamento"
        verbose_name_plural = "agendamentos"

    def save(self, *args, **kwargs):
        if not self.protocolo:
            self.protocolo = "CS-" + secrets.token_hex(3).upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.protocolo} — {self.nome}"


class Contato(Base):
    nome = models.CharField(max_length=150)
    email = models.EmailField("e-mail")
    telefone = models.CharField(max_length=30, blank=True)
    mensagem = models.TextField()
    respondido = models.BooleanField(default=False)

    class Meta(Base.Meta):
        verbose_name = "mensagem de contato"
        verbose_name_plural = "mensagens de contato"

    def __str__(self):
        return f"{self.nome} <{self.email}>"


class CliqueWhatsApp(models.Model):
    """Um clique em "Falar no WhatsApp". Não guarda IP nem dados pessoais."""

    CLINICAS = [
        ("medicina", "Medicina"), ("enfermagem", "Enfermagem"), ("nutricao", "Nutrição"),
        ("odontologia", "Odontologia"), ("fisioterapia", "Fisioterapia"), ("psicologia", "Psicologia"),
        ("estetica", "Estética"), ("veterinaria", "Medicina Veterinária"), ("geral", "Número geral"),
    ]
    LOCAIS = [
        ("cartao", "Cartão da clínica"), ("rodape", "Rodapé"), ("flutuante", "Botão flutuante"),
    ]

    criado_em = models.DateTimeField("quando", auto_now_add=True, db_index=True)
    clinica = models.CharField("clínica", max_length=20, choices=CLINICAS)
    local = models.CharField("onde clicou", max_length=12, choices=LOCAIS)
    dispositivo = models.CharField(max_length=10, choices=[("celular", "Celular"), ("computador", "Computador")])
    origem = models.CharField("veio de", max_length=120, blank=True, help_text="Site que trouxe a pessoa (vazio = acesso direto).")

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "clique no WhatsApp"
        verbose_name_plural = "cliques no WhatsApp"

    def __str__(self):
        return f"{self.get_clinica_display()} — {self.criado_em:%d/%m/%Y %H:%M}"
