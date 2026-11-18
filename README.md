# Conecta Saúde

Site das Clínicas-Escola da UNICEPLAC em Django, pronto para a Vercel.
Os formulários de **agendamento** e **contato** gravam no banco, e você vê tudo no painel em `/painel/` (com filtro, busca, mudança de status e exportação para CSV/Excel).

## Rodar no seu computador

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py createsuperuser
.venv\Scripts\python manage.py runserver
```

Site: http://localhost:8000 · Painel: http://localhost:8000/painel/

## Publicar na Vercel

1. **Suba o código para o GitHub** e importe o repositório em vercel.com → *Add New → Project*.
2. **Crie o banco**: no projeto da Vercel, aba *Storage* → *Create Database* → **Neon (Postgres)**. Ela cria a variável `DATABASE_URL` sozinha.
3. **Variáveis de ambiente** (*Settings → Environment Variables*):
   | Nome | Valor |
   |---|---|
   | `SECRET_KEY` | um texto longo e aleatório (`python -c "import secrets;print(secrets.token_urlsafe(50))"`) |
   | `DEBUG` | `0` |
   | `WHATSAPP_NUMBER` | número da equipe só com dígitos, ex. `5581996236811` |
   | `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` | só se usar domínio próprio, ex. `conectasaude.com.br` / `https://conectasaude.com.br` |
4. **Crie as tabelas no banco de produção** (uma vez, e de novo sempre que mudar os modelos). No seu PC, com a `DATABASE_URL` copiada da Vercel:
   ```powershell
   $env:DATABASE_URL="postgres://..."; .venv\Scripts\python manage.py migrate; .venv\Scripts\python manage.py createsuperuser
   ```
5. Faça o deploy. Pronto: `https://seu-projeto.vercel.app/painel/`.

## Onde mexer

- `templates/index.html` — a página (textos, especialidades, depoimentos, FAQ ficam no `<script>` no fim).
- `leads/models.py` — quais dados são guardados.
- `leads/forms.py` — validação e lista de especialidades aceitas.
- `leads/admin.py` — o painel.

## LGPD

Os formulários só são aceitos com o checkbox de consentimento marcado, e o registro guarda data, IP e navegador como prova do aceite. Antes de ir ao ar, troque os textos ilustrativos das páginas *Política de Privacidade*, *Termos* e *LGPD* (objeto `INFO` em `templates/index.html`) por textos revisados.
