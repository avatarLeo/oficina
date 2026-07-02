# AGENTS.md

## Stack

- Django 5.2, Python 3.10, SQLite, Pillow, python-dotenv
- `venv/` at repo root — activate before running manage.py commands

## Commands

```sh
source venv/bin/activate
python manage.py runserver          # dev server at http://127.0.0.1:8000
python manage.py makemigrations     # after model changes
python manage.py migrate            # apply migrations
```

## Architecture

- Project `oficina/`, single app `servico/`
- **4 models**: `Cliente`, `Servico`, `HistoricoStatus`, `ServicoOferta`
  - `Servico` has status (`aguardando` / `em_andamento` / `servico_concluido`) and payment tracking (auto-set via `save()`)
  - `Servico.previsao_entrega` defaults to now+4d if null
  - `HistoricoStatus` logs every status change
  - `ServicoOferta` is the "serviços" cards on the homepage
- Template base: `base_templates/global/base.html`
  - Partials: `servico/templates/servico/partials/*.html`
  - Pages: `servico/templates/servico/pages/*.html` (home, acompanhar)
  - Dashboard: `servico/templates/servico/dashboard/*.html`
- Static (app): `servico/static/servico/css/`, `servico/static/servico/js/`
- Static (global): `base_static/`
- Media: `media/` (served via `urlpatterns += static()` in dev)
- Settings loaded from `.env` (SECRET_KEY, DEBUG)
- WhatsApp number in `settings.WHATSAPP_NUMBER`, exposed via `oficina.context_processors.whatsapp`

## Routes

| Path | View | Auth |
|---|---|---|
| `/` | `home` | public |
| `/acompanhar/` | `acompanhar` (lookup by CPF/phone) | public |
| `/dashboard/` | `dashboard_home` | staff only (redirects to `/admin/login/`) |
| `/dashboard/servicos/`, `/dashboard/clientes/`, etc. | CRUD views | staff only |
| `/admin/` | Django admin (registers all 4 models) | superuser |

Dashboard views use `@login_required(login_url='/admin/login/')` + `@user_passes_test(staff_check)`.

## Dual-mode site

- **Django version** (`runserver`): full site with DB-driven content
- **Standalone `index.html`** at repo root: static HTML copy, NOT rendered by Django. Its `style.css` and `script.js` are also at root level — separate from Django static files.

## Known issues

- `CACHES` uses `DummyCache` (settings.py:81) — dev only, remove for production
- Root `index.html` form submits via `alert()` mock — no real backend
- No tests written (`servico/tests.py` is empty)
- `db.sqlite3` is gitignored — new clones must run `migrate`
