#!/usr/bin/env bash
set -euo pipefail

# =====================================================================
# Supreme lab deploy - laptop git HEAD -> lab server (192.168.1.105)
#
# Same idea as audaxEMR's deploy_patch.sh, cut down for one box:
#
#   * diffs from the deployed/<ip> tag, so only what changed is pushed
#   * lab/settings.py NEVER ships - the server's copy holds the real
#     DB password and secret key; git's copy deliberately does not
#   * migrations are synced as whole directories (append-only), and the
#     SERVER says whether migrate is needed
#   * a pg_dump of the live database is taken before anything is written
#   * manage.py check runs on the server before migrate and before reload
#   * gunicorn is reloaded with HUP (graceful, no sudo needed - it runs as
#     sadmin), not restarted
#   * a full-tree checksum sweep must come back clean before it tags
#
# Usage:   ./deploy.sh            (asks before every step that writes)
#          ./deploy.sh --check    (read-only: what would ship, and is the
#                                  server in sync with deployed/<ip>?)
# =====================================================================

HOST="192.168.1.105"
USER_="sadmin"
RPATH="/home/sadmin/supreme_lab"
REMOTE="${USER_}@${HOST}"
TAG="deployed/${HOST}"

# What ships. lab/ is here for urls.py/wsgi.py; settings.py is filtered out.
DEPLOY_DIRS=(results theme lab)
NEVER_SHIP='^lab/(settings|local_settings)\.py$'

CHECK_ONLY=0; [[ "${1:-}" == "--check" ]] && CHECK_ONLY=1

cd "$(git rev-parse --show-toplevel)"

CTL="/tmp/.supreme_ssh_$$"
SSH_OPTS=(-o ControlMaster=auto -o "ControlPath=$CTL" -o ControlPersist=10m)
cleanup() { ssh "${SSH_OPTS[@]}" -O exit "$REMOTE" 2>/dev/null || true; }
trap cleanup EXIT
rsh() { ssh "${SSH_OPTS[@]}" "$REMOTE" "$@"; }
rsy() { rsync -e "ssh ${SSH_OPTS[*]}" "$@"; }
rvenv() { rsh "cd '$RPATH' && source venv/bin/activate && $1"; }
ask() { read -rp "    $1 Type 'yes': " a; [[ "$a" == "yes" ]] || { echo "Aborted - nothing further was written."; exit 1; }; }

tracked_deployables() {
  git ls-files -- "${DEPLOY_DIRS[@]}" | grep -Ev "$NEVER_SHIP" | grep -Ev '__pycache__|\.pyc$'
}

# Tracked files whose CONTENT differs on the server (checksums, not mtimes).
server_diff_list() {
  local out
  if ! out=$(tracked_deployables | rsy -rcin --files-from=- ./ "${REMOTE}:${RPATH}/" 2>/dev/null); then
    echo "__COULD_NOT_COMPARE__"; return 0
  fi
  awk 'substr($1,2,1)=="f" {print $2}' <<<"$out"
}

echo "==> [0] Connecting to $REMOTE ..."
rsh -o ConnectTimeout=8 "test -d '$RPATH'" || { echo "Can't reach $REMOTE or $RPATH is missing. Stop."; exit 1; }
if ! ssh -o BatchMode=yes -o ConnectTimeout=5 "$REMOTE" true 2>/dev/null; then
  echo "    (no SSH key - you were asked for the password once. To stop that: ssh-copy-id $REMOTE)"
fi

# --- 1. local hygiene ----------------------------------------------------
echo "==> [1] Local checks ..."
if [[ -n "$(git status --porcelain -- "${DEPLOY_DIRS[@]}")" ]]; then
  echo "    Uncommitted changes in deployable dirs - rsync sends WORKING files:"
  git status --short -- "${DEPLOY_DIRS[@]}" | sed 's/^/      /'
  [[ $CHECK_ONLY == 1 ]] || ask "Deploy them anyway?"
fi
UNTRACKED=$(git ls-files --others --exclude-standard -- "${DEPLOY_DIRS[@]}" | grep -Ev '__pycache__|\.pyc$' || true)
if [[ -n "$UNTRACKED" ]]; then
  echo "    Untracked files in deployable dirs (these will NOT ship - commit them):"
  echo "$UNTRACKED" | sed 's/^/      /'
  [[ $CHECK_ONLY == 1 ]] || ask "Continue without them?"
fi

# --- 2. what changed since the last deploy -------------------------------
echo "==> [2] Changes since $TAG ..."
git rev-parse -q --verify "$TAG" >/dev/null || { echo "    No $TAG tag. Tag the commit the server is running first."; exit 1; }
echo "    Server was last deployed at $(git rev-parse --short "$TAG"): $(git log -1 --format=%s "$TAG" | cut -c1-70)"

CHANGED=(); DELETED=()
while IFS= read -r f; do [[ -n "$f" ]] && CHANGED+=("$f"); done < <(
  git diff --name-only --diff-filter=ACMR "$TAG" HEAD -- "${DEPLOY_DIRS[@]}" | grep -Ev "$NEVER_SHIP" | grep -v '/migrations/' || true)
while IFS= read -r f; do [[ -n "$f" ]] && DELETED+=("$f"); done < <(
  git diff --name-only --diff-filter=D "$TAG" HEAD -- "${DEPLOY_DIRS[@]}" | grep -Ev "$NEVER_SHIP" || true)
NEW_MIGRATIONS=$(git diff --name-only --diff-filter=A "$TAG" HEAD -- '*/migrations/*.py' || true)

echo "    files to push (${#CHANGED[@]}):";  printf '      %s\n' "${CHANGED[@]:-<none>}"
echo "    files to delete (${#DELETED[@]}):"; printf '      %s\n' "${DELETED[@]:-<none>}"
echo "    new migrations:"; if [[ -n "$NEW_MIGRATIONS" ]]; then sed 's/^/      /' <<<"$NEW_MIGRATIONS"; else echo "      <none>"; fi

# A file deleted from git but still on disk is almost always an accident.
for f in "${DELETED[@]:-}"; do
  if [[ -n "$f" && -e "$f" ]]; then
    echo "    STOP: $f is marked deleted in git but still exists here. Re-add it or remove it locally."; exit 1
  fi
done

# requirements.txt never ships. Compare it with what the server venv really has.
MISSING_PKGS=$(comm -23 <(grep -v '^\s*#' requirements.txt | sed '/^\s*$/d' | tr 'A-Z_' 'a-z-' | sort -u) \
                        <(rvenv "pip freeze" 2>/dev/null | tr 'A-Z_' 'a-z-' | sort -u) || true)
if [[ -n "$MISSING_PKGS" ]]; then
  echo "    NOTE: requirements.txt has packages the server venv lacks - install by hand:"
  sed 's/^/      /' <<<"$MISSING_PKGS"
  echo "      (ssh $REMOTE \"cd $RPATH && venv/bin/pip install -r requirements.txt\" after pushing it)"
fi

# --- 3. static files -----------------------------------------------------
# nginx serves $RPATH/static/ (collectstatic output, owned by www-data), NOT
# the app static dirs. Pushing theme/static/... alone changes nothing users
# see; collectstatic does. Only flag files whose SERVED copy would change.
NEED_COLLECTSTATIC=()
for f in "${CHANGED[@]:-}"; do
  [[ "$f" == */static/* ]] || continue
  served="static/${f#*/static/}"
  if ! rsh "cmp -s '$RPATH/$served' -" < "$f" 2>/dev/null; then NEED_COLLECTSTATIC+=("$served"); fi
done
if [[ ${#NEED_COLLECTSTATIC[@]} -gt 0 ]]; then
  echo "    STATIC: these SERVED files would change and need collectstatic:"
  printf '      %s\n' "${NEED_COLLECTSTATIC[@]}"
  echo "    $RPATH/static is owned by www-data, so once, on the server, run:"
  echo "      sudo chown -R $USER_:www-data $RPATH/static"
fi

if [[ $CHECK_ONLY == 1 ]]; then
  echo "==> [check] Checksum sweep: tracked files that differ between HEAD and the server"
  STALE=$(server_diff_list)
  if [[ -z "$STALE" ]]; then
    echo "    None - the server matches HEAD."
  else
    sed 's/^/      /' <<<"$STALE"
    if git diff --quiet "$TAG" HEAD -- "${DEPLOY_DIRS[@]}"; then
      echo "    HEAD == $TAG, so these were edited ON THE SERVER by hand. Pull them into git before deploying."
    fi
  fi
  exit 0
fi

# --- 3b. the test suite must pass before anything touches the server --------
echo "==> [3b] Running the test suite locally (about a minute) ..."
TEST_LOG=$(mktemp /tmp/supreme_tests.XXXXXX)
if venv/bin/python manage.py test results --debug-mode --noinput >"$TEST_LOG" 2>&1; then
  grep -E '^Ran ' "$TEST_LOG" | sed 's/^/      /'
  echo "    All tests passed."
  rm -f "$TEST_LOG"
else
  grep -E '^(FAIL|ERROR):|^Ran |^FAILED' "$TEST_LOG" | sed 's/^/      /'
  echo "    TESTS FAILED - nothing was sent to the server. Full output: $TEST_LOG"
  exit 1
fi

ask "Back up the server and push?"

# --- 4. backups ----------------------------------------------------------
STAMP=$(date +%F_%H%M)
echo "==> [4] Backing up the live database and the files about to change ..."
rsh "mkdir -p ~/backups"
# Reads the DB credentials from the SERVER's settings.py - none live in this script.
rvenv "DJANGO_SETTINGS_MODULE=lab.settings python - <<'PY'
import os, subprocess, django
django.setup()
from django.conf import settings
d = settings.DATABASES['default']
out = os.path.expanduser('~/backups/supreme_db_${STAMP}.dump')
subprocess.run(['pg_dump', '-Fc', '-h', d['HOST'] or 'localhost', '-U', d['USER'], '-f', out, d['NAME']],
               env=dict(os.environ, PGPASSWORD=d['PASSWORD']), check=True)
print('    database ->', out, os.path.getsize(out) // 1024, 'KB')
PY"
rsh "cd '$RPATH' && tar -czf ~/backups/supreme_code_${STAMP}.tar.gz --exclude=venv --exclude=supreme --exclude=node_modules --exclude=static --exclude=__pycache__ ." \
  && echo "    code     -> ~/backups/supreme_code_${STAMP}.tar.gz (whole tree before this deploy)"
echo "    Old backups are never deleted by this script - prune ~/backups by hand now and then."

# --- 5. push ---------------------------------------------------------------
echo "==> [5] Pushing ..."
if [[ ${#CHANGED[@]} -gt 0 ]]; then
  rsy -azR --itemize-changes "${CHANGED[@]}" "${REMOTE}:${RPATH}/" | sed 's/^/      /'
fi
if [[ ${#DELETED[@]} -gt 0 ]]; then
  printf '%s\n' "${DELETED[@]}" | rsh "cd '$RPATH' && xargs -r -d '\n' rm -fv" | sed 's/^/      /'
fi
MIGDIRS=(); for d in "${DEPLOY_DIRS[@]}"; do [[ -d "$d/migrations" ]] && MIGDIRS+=("$d/migrations"); done
rsy -azR --exclude='__pycache__' "${MIGDIRS[@]}" "${REMOTE}:${RPATH}/"

# --- 6. check, then migrate --------------------------------------------------
echo "==> [6] manage.py check on the server ..."
if ! rvenv "python manage.py check" ; then
  echo "    CHECK FAILED - the running app is untouched (gunicorn still has the old code loaded)."
  echo "    Fix and redeploy, or restore: tar -xzf ~/backups/supreme_code_${STAMP}.tar.gz -C $RPATH"
  exit 1
fi
PENDING=$(rvenv "python manage.py showmigrations --plan | grep -c '^\[ \]' || true")
if [[ "$PENDING" != "0" ]]; then
  echo "    $PENDING migration(s) pending on the server:"
  rvenv "python manage.py showmigrations --plan | grep '^\[ \]'" | sed 's/^/      /'
  ask "Run migrate now?"
  rvenv "python manage.py migrate" | sed 's/^/      /'
else
  echo "    No migrations pending."
fi

echo "==> [6b] Catalogue check (is every requestable test in Admin -> Generic tests?) ..."
if CAT_OUT=$(rvenv "python manage.py check_catalogue" 2>&1); then
  sed 's/^/      /' <<<"$CAT_OUT"
else
  sed 's/^/      /' <<<"$CAT_OUT"
  echo "    WARNING: the tests listed above CANNOT be requested until their catalogue rows"
  echo "    are fixed in Admin. The code is fine; this is data on the server. Continuing."
fi

if [[ ${#NEED_COLLECTSTATIC[@]} -gt 0 ]]; then
  echo "==> collectstatic ..."
  rvenv "python manage.py collectstatic --noinput" | tail -2 | sed 's/^/      /' \
    || echo "    collectstatic FAILED (ownership?) - see the sudo chown line above, then rerun it on the server."
fi

# --- 7. reload ---------------------------------------------------------------
echo "==> [7] Reloading gunicorn (graceful HUP) ..."
rsh 'M=$(pgrep -u '"$USER_"' -o -f "gunicorn.*lab.wsgi") && kill -HUP "$M" && echo "      HUP sent to master $M"'
sleep 3
CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "http://${HOST}/login/" || echo "000")
echo "    http://${HOST}/login/ -> $CODE"
[[ "$CODE" == "200" ]] || { echo "    Site is NOT answering 200. Check: ssh $REMOTE 'journalctl -u gunicorn -n 50'"; exit 1; }

# --- 8. verify, then tag -------------------------------------------------------
echo "==> [8] Verifying every tracked file now matches the server ..."
STALE=$(server_diff_list)
if [[ -z "$STALE" ]]; then
  git tag -f "$TAG" HEAD >/dev/null
  echo "    Clean. Tagged $TAG -> $(git rev-parse --short HEAD)."
else
  echo "    NOT tagging - these still differ on the server:"; sed 's/^/      /' <<<"$STALE"
  exit 1
fi
echo "Done."
