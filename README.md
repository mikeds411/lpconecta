# Conecta Saúde

Site das Clínicas-Escola da UNICEPLAC em Django, pronto para a Vercel.
Cada clique em **"Falar no WhatsApp"** (por clínica, rodapé e botão flutuante) é registrado no banco, e você vê tudo no painel em `/painel/` → *Cliques no WhatsApp*, com filtros por clínica, data e aparelho e exportação para CSV/Excel. Não guardamos IP nem dados pessoais dos visitantes.

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
   | `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` | só se usar domínio próprio, ex. `conectasaude.com.br` / `https://conectasaude.com.br` |
4. **Crie as tabelas no banco de produção** (uma vez, e de novo sempre que mudar os modelos). No seu PC, com a `DATABASE_URL` copiada da Vercel:
   ```powershell
   $env:DATABASE_URL="postgres://..."; .venv\Scripts\python manage.py migrate; .venv\Scripts\python manage.py createsuperuser
   ```
5. Faça o deploy. Pronto: `https://seu-projeto.vercel.app/painel/`.

## Onde mexer

- `templates/index.html` — os textos da página (clínicas, passos, depoimentos, FAQ, rodapé).
- `static/landing/js/config.js` — **números de WhatsApp** (geral e de cada clínica; vazio = usa o geral).
- `static/landing/css/styles.css` — visual e animações.
- `static/landing/js/main.js` — menu mobile e item ativo do menu na rolagem.
- `static/landing/js/track.js` — contagem dos cliques no WhatsApp.
- `static/img/` — logo, favicon. Para a foto do hero: salve em `static/landing/assets/hero-photo.jpg`, descomente `--hero-photo` no topo do `styles.css` e remova o bloco `.honey` do `index.html`.
- `leads/` — banco de dados e painel.

Sempre que mudar `leads/models.py`: rode `makemigrations` aqui e `migrate` no banco do Neon.

## LGPD

A contagem de cliques não guarda dados pessoais (só clínica, local do clique, celular/computador e o site de origem). Os links de Política de Privacidade, Termos e LGPD no rodapé ainda apontam para o próprio rodapé: falta criar essas páginas com textos revisados.

O backend ainda tem os endpoints de agendamento e contato (`/api/agendamento/`, `/api/contato/`) e as telas no painel, prontos caso a página volte a ter formulário.
