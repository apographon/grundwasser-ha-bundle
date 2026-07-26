# Grundwasser – Deploy auf Live-HA

Schritt-für-Schritt für **Messstelle Poing D 83**. Voraussetzung: Live-Config unter `/Volumes/config` (oder `HA_CONFIG_DEST`).

## Was wohin gehört

| Artefakt | Im Repo | Auf Live | Automatisch im Dashboard? |
|----------|---------|----------|---------------------------|
| `integration/grundwasser.yaml` | ✓ | `integrations/grundwasser.yaml` | — (Package, kein UI) |
| `integration/grundwasser_helpers.yaml` | ✓ | `integrations/grundwasser_helpers.yaml` | — (Template-Alias für Tile) |
| `scripts/import-grundwasser-csv-to-recorder.py` | ✓ | `/config/` (Projektroot) | — |
| `ui/*.yaml` | ✓ | `ui/` (versionierte Referenzkopien) | **Nein** — manuell oder per Lovelace-API |
| Dashboard-Karten | UI-Storage auf Live | nur auf Live | Ja, aber **nicht** via Sync |

**Wichtig:** Dateien unter `ui/` sind **Lovelace-Snippets**, keine HA-Packages. Niemals nach `integrations/` kopieren (Slug-Fehler wie bei EON). Das Live-Dashboard läuft im **UI-Storage-Modus**; Änderungen im Dashboard-Editor werden deshalb nicht automatisch in dieses Bundle zurückgeschrieben.

Entity-IDs: **[ENTITY-IDS.md](../ENTITY-IDS.md)**. Situation-Alias: **[situation-alias.md](situation-alias.md)**.

---

## Deploy (Integration + Hilfsdateien)

Aus dem Bundle-Root:

```bash
./scripts/deploy-grundwasser.sh          # Dry-Run (Standard)
./scripts/deploy-grundwasser.sh --run    # Kopieren nach Live
```

Umgebungsvariablen (optional):

- `HA_CONFIG_DEST=/pfad/zur/config` — Ziel (Default: `/Volumes/config`)
- `GRUNDWASSER_SOURCE=/pfad/zum/bundle` — Quelle (Default: Bundle-Root)

### Alternative: gesamter HA-Sync

```bash
cd /Users/oli/HAss/home-assistant-config
./scripts/sync-to-live.sh          # Dry-Run
./scripts/sync-to-live.sh --run
```

Das Bundle-Script ist schmaler: nur Grundwasser-Dateien, ohne `configuration.yaml` oder andere Projekte.

---

## Nach dem Deploy: Verifikation

### 1. Config prüfen + Neustart

Die `ha`-CLI funktioniert **nicht** zuverlässig per `ssh ha "ha …"` (API-Token). Stattdessen:

**Einstellungen → Add-ons → Terminal & SSH → Terminal öffnen**, dann:

```bash
ha core check
ha core restart
```

Oder Neustart über **Einstellungen → System**.

SSH-Stand und Grenzen: [home-assistant-config/doc/ssh-from-mac.md](../../home-assistant-config/doc/ssh-from-mac.md).

### 2. Sensoren prüfen

**Entwicklerwerkzeuge → Zustände** — nach `grundwasser_poing` filtern.

| Prüfung | Erwartung |
|--------|-----------|
| `sensor.grundwasser_poing_d83_m_u_nn` | Zahl ~500–520, nicht `unavailable` |
| `sensor.grundwasser_poing_d83_m_u_gelande` | Zahl, nicht `unavailable` |
| `sensor.grundwasser_poing_d83_situation_anzeige` | `kein Niedrigwasser`, `niedrig` oder `Niedrigwasser` |
| Attribut `source_entity` am Alias | zeigt REST-Quelle (z. B. `…_situation_3`) |

### 3. Log (nur Kritisches)

**Einstellungen → System → Protokolle:**

- `nid.bayern.de` + `ERROR` / `Timeout`
- `grundwasser` + `failed` / `invalid`

### 4. Dashboard (manuell)

Sync legt **keine** Karten im UI-Storage an. Checkliste:

- [ ] ApexCharts-Karte (`ui/apex-grundwasser-card.yaml`)
- [ ] Verlauf (`ui/apex-grundwasser-verlauf-card.yaml`)
- [ ] Mobile Swipe-Ansicht (`ui/apex-grundwasser-mobile-swipe-card.yaml`)
- [ ] Situation-Tile — Entity: `sensor.grundwasser_poing_d83_situation_anzeige`

---

## CSV-Import (optional)

Nicht Teil von `deploy-grundwasser.sh`. Siehe [csv-import.md](csv-import.md).

Vor Import: `recorder.purge_keep_days` in der Live-`configuration.yaml` ggf. erhöhen.

---

## Typische Fehler

| Symptom | Ursache | Lösung |
|---------|---------|--------|
| Package `apex-grundwasser-card` failed | UI-YAML in `integrations/` | Nur Packages in `integrations/` |
| Situation-Tile grau/leer | Alias `unavailable` oder REST tot | `source_entity` / NID prüfen |
| Chart ohne Historie | `purge_keep_days` zu klein | Vor Import erhöhen |
| Deploy schreibt nichts | Volume nicht gemountet | `/Volumes/config` oder `HA_CONFIG_DEST` |
| `ha …` per SSH: API token | User `hassio` ohne Supervisor-Token | Web-Terminal nutzen |
