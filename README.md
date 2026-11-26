# Supreme Diagnostic Laboratories – lab results system

Django 5.0 app running on the lab's LAN server at http://192.168.1.105
(gunicorn behind nginx, PostgreSQL 14). This repo is the source of truth;
the server gets changes only through `./deploy.sh`.

## Everyday workflow

```bash
source venv/bin/activate
python manage.py runserver                       # laptop copy, DB: supreme_lab_dev
python manage.py test results --debug-mode       # whole suite, about a minute
git commit ...
./deploy.sh --check                              # read-only: what would ship, any drift on the server
./deploy.sh                                      # tests -> backup -> push -> migrate -> reload -> verify -> tag
```

`deploy.sh` refuses to touch the server if any test fails. It backs up the live
database and code to `~/backups/` on the server before every push, and those
backups are never deleted automatically, so prune them now and then.

## Things that will bite you

- **`lab/settings.py` never deploys.** The server's copy has the real DB
  password and secret key; git's copy reads them from the environment. Laptop
  DB credentials live in `lab/local_settings.py` (git-ignored). Change server
  settings by hand, on the server.
- **The CSS the lab sees is `static/css/dist/styles.css` on the server**
  (collectstatic output, owned by `www-data`, built Oct 2024). A Tailwind class
  that isn't already in that file does nothing on the live site. Check first:
  `grep -c '\.your-class' static/css/dist/styles.css`. Rebuilding the CSS
  (`cd theme/static_src && npm run build`) changes the look of many pages
  (e.g. some report colours, layouts on the General form), so treat it as a
  deliberate release of its own. collectstatic then needs
  `sudo chown -R sadmin:www-data ~/supreme_lab/static` once.
- **Test requests are found by catalogue NAME** (Admin → Generic tests). Renaming
  a test there breaks SEND REQUEST for it. `python manage.py check_catalogue`
  (run by every deploy) lists any that can't be requested.
- **The server runs DEBUG=True with django_fastdev**, so a template that uses
  a missing variable errors instead of rendering blank. The tests run with
  `--debug-mode` for the same reason.
- **Every page requires login** (wrapped in `results/urls.py`). New routes
  are covered automatically; add a name to `PUBLIC_URL_NAMES` only if it must
  be reachable logged out.
- **Patient age is free text on purpose.** Many patients don't know their age,
  so staff write ADULT / CHILD. The box suggests those, but anything is accepted.

## Where things are

| What | Where |
|---|---|
| Test types, results models | `results/models.py` |
| FBC 2 parameters and reference ranges | `FBC2_PARAMETERS` in `results/models.py` (no migration needed to change a range) |
| Patient folder (all test tabs) | `results/templates/patient/patient_details.html` |
| Printed lab report | `results/templates/report_pdf.html` (xhtml2pdf: never leave a table cell empty; use `&nbsp;`) |
| Tests | `results/tests/` (`base.py` holds the live catalogue and the list of all 33 test types) |
| Deploy | `deploy.sh` (server address and path at the top) |
