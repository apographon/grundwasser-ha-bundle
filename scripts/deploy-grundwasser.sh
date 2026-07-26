#!/usr/bin/env bash
# Deploy Grundwasser-Bundle → Live-HA (nur Projektdateien).
#
# Kopiert:
#   integration/grundwasser.yaml         → integrations/grundwasser.yaml
#   integration/grundwasser_helpers.yaml → integrations/grundwasser_helpers.yaml
#   scripts/import-grundwasser-csv-to-recorder.py → config-Root
#   ui/*.yaml                     → ui/ (Referenz; Dashboard manuell)
#
# Kopiert NICHT ins Lovelace-UI-Storage — siehe doc/deploy.md
#
# Nutzung:
#   ./scripts/deploy-grundwasser.sh          # dry-run (Default)
#   ./scripts/deploy-grundwasser.sh --run    # kopieren
#
# Nach --run: ha core check && ha core restart (siehe doc/deploy.md)

set -euo pipefail

BUNDLE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE="${GRUNDWASSER_SOURCE:-$BUNDLE_ROOT}"
DEST="${HA_CONFIG_DEST:-/Volumes/config}"

DRY=(--dry-run -v)
if [[ "${1:-}" == "--run" ]]; then
  DRY=(-v)
fi

if [[ ! -f "$SOURCE/integration/grundwasser.yaml" ]]; then
  echo "Error: Bundle not found (missing integration/grundwasser.yaml): $SOURCE" >&2
  exit 1
fi

if [[ ! -d "$DEST" ]]; then
  echo "Error: Destination not found (volume mounted?): $DEST" >&2
  echo "Override: HA_CONFIG_DEST=/path/to/config $0" >&2
  exit 1
fi

if [[ ! -w "$DEST" ]]; then
  echo "Error: Destination not writable: $DEST" >&2
  exit 1
fi

echo "=============================================="
echo "  Deploy: Grundwasser → Live HA"
echo "=============================================="
echo "  Source:      $SOURCE"
echo "  Destination: $DEST"
if [[ "${#DRY[@]}" -gt 1 ]]; then
  echo "  Mode:        DRY RUN"
else
  echo "  Mode:        RUN"
fi
echo "=============================================="
echo ""
echo "Hinweis: ui/*.yaml landen nur als Referenz unter ui/."
echo "         Dashboard-Karten im UI-Storage manuell pflegen (doc/deploy.md)."
echo ""

mkdir -p "$DEST/integrations" "$DEST/ui"

echo "--- integration/grundwasser.yaml → integrations/grundwasser.yaml"
rsync -a "${DRY[@]}" \
  "$SOURCE/integration/grundwasser.yaml" \
  "$DEST/integrations/grundwasser.yaml"

echo ""
echo "--- integration/grundwasser_helpers.yaml → integrations/grundwasser_helpers.yaml"
rsync -a "${DRY[@]}" \
  "$SOURCE/integration/grundwasser_helpers.yaml" \
  "$DEST/integrations/grundwasser_helpers.yaml"

echo ""
echo "--- import script → config root"
rsync -a "${DRY[@]}" \
  "$SOURCE/scripts/import-grundwasser-csv-to-recorder.py" \
  "$DEST/import-grundwasser-csv-to-recorder.py"

echo ""
echo "--- ui/*.yaml → ui/ (Referenz)"
rsync -a "${DRY[@]}" \
  --include='*.yaml' \
  --exclude='*' \
  "$SOURCE/ui/" \
  "$DEST/ui/"

echo ""
if [[ "${#DRY[@]}" -gt 1 ]]; then
  echo "Dry run complete. Apply: $0 --run"
  echo "Then: ha core check && ha core restart"
  echo "Verify: doc/deploy.md"
else
  echo "Done. Next steps:"
  echo "  1. ha core check"
  echo "  2. ha core restart"
  echo "  3. Sensoren prüfen (doc/deploy.md)"
  echo "  4. Dashboard-Karten ggf. manuell aktualisieren"
fi
