#!/usr/bin/env bash
# FEDCO Theme installer
set -euo pipefail
SITE="${1:-}"
APP_PATH="${2:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}"

if [[ -z "$SITE" ]]; then echo "Usage: ./install.sh <site-name> [path]"; exit 1; fi
if [[ ! -f "sites/common_site_config.json" ]]; then
  echo "ERROR: run from your frappe-bench directory."; exit 1
fi

[[ -d "apps/fedco_theme" ]] || bench get-app fedco_theme "$APP_PATH"
bench --site "$SITE" install-app fedco_theme
bench build --app fedco_theme
bench --site "$SITE" clear-cache
bench --site "$SITE" clear-website-cache
bench restart || echo "  (bench restart skipped — restart your processes manually)"

cat <<'DONE'

============================================================
 FEDCO Theme installed.

 Hard-refresh your browser (Ctrl-Shift-R) — CSS is cached.

 Logo and favicon are applied automatically where those
 fields were blank. Override at: Website Settings > Brand.
============================================================
DONE
