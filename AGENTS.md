# AGENTS.md

## Stack

- Django 5.2, Python 3.10+, SQLite, Pillow, python-dotenv
- `venv/` at repo root — activate before manage.py commands

## Setup & Commands

```sh
source venv/bin/activate
cp .env.example .env                  # first time only — edit SECRET_KEY/DEBUG
python manage.py migrate              # creates db.sqlite3
python manage.py createsuperuser      # needed for dashboard/admin access
python manage.py runserver            # dev server at http://127.0.0.1:8000
python manage.py makemigrations       # after model changes
```

## Architecture

- Project config `oficina/` (settings, urls, wsgi, asgi, context_processors.py)
- Single app `servico/` registered as `'servico'` in INSTALLED_APPS
- **4 models**: `Cliente`, `Servico`, `HistoricoStatus`, `ServicoOferta`
  - `Servico` status: `aguardando` / `em_andamento` / `servico_concluido`
  - Payment status auto-set via `Servico.save()` (pendente/parcial/pago)
  - `Servico.previsao_entrega` defaults to now+4d if null
  - `HistoricoStatus` logs every status change
  - `ServicoOferta` = "serviços" cards on homepage
- Templates: `base_templates/global/base.html`, `servico/templates/servico/{partials,pages,dashboard}/`
- Static sources: `servico/static/servico/` and `base_static/` (collects into `static/` which is gitignored)
- Media: `media/` (gitignored, served via `urlpatterns += static()` in dev)
- Settings loaded from `.env` (`SECRET_KEY`, `DEBUG`)
- WhatsApp number in `settings.WHATSAPP_NUMBER`, via `oficina.context_processors.whatsapp`
- `ALLOWED_HOSTS = ['0.0.0.0', '*']`, `LANGUAGE_CODE = 'pt-BR'`

## Routes

| Path | View | Auth |
|---|---|---|
| `/` | `home` | public |
| `/acompanhar/` | `acompanhar` (lookup by CPF/phone) | public |
| `/dashboard/` | `dashboard_home` | staff only (redirects to `/admin/login/`) |
| `/dashboard/servicos/`, `/dashboard/clientes/`, etc. | CRUD views | staff only |
| `/admin/` | Django admin (registers all 4 models) | superuser |

Dashboard views: `@login_required(login_url='/admin/login/')` + `@user_passes_test(staff_check)`.

## Dual-mode site

- **Django version** (`runserver`): full site with DB-driven content
- **Standalone `index.html`** at repo root: static HTML copy, NOT rendered by Django. Its `style.css` and `script.js` are also at root level — separate from Django static files. Form submits via `alert()` mock.
- **GitHub Pages**: `docs/` folder is the static site deployed to Pages — copy of the root files. Configured in repo Settings > Pages > branch `main`, folder `/docs`.

## What's NOT configured

- No tests written (`servico/tests.py` is empty)
- No linter, formatter, type checker, or CI
- `CACHES` uses `DummyCache` (dev only — remove for production)
- `db.sqlite3` and `media/` are gitignored — new clones must run `migrate`
