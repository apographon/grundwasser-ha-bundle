# Session-Stand (Mai 2026) – Grundwasser + SSH

Kurzprotokoll: was erledigt ist, was deployed wurde, was offen bleibt.

## Erledigt im Bundle

| Thema | Status |
|-------|--------|
| Canonical source = `grundwasser-bundle/` (`grundwasser/` nur Redirect) | ✓ |
| Doku-Ordner konsequent `doc/` | ✓ |
| `doc/deploy.md` + `scripts/deploy-grundwasser.sh` | ✓ |
| `ENTITY-IDS.md` | ✓ |
| Situation-Alias `…_situation_anzeige` (`grundwasser_helpers.yaml`) | ✓ |
| Tile auf Alias umgestellt | ✓ |
| Deploy nach `/Volumes/config` (`--run`) | ✓ ausgeführt |

## Nach Deploy noch manuell

1. **`ha core check`** und **Neustart** — im **Web-Terminal** (Add-on), nicht per `ssh ha "ha …"` (siehe SSH-Doku)
2. Sensor `…_situation_anzeige` + Attribut `source_entity` prüfen

## Nachtrag Juli 2026

- Dashboard-Badge und Situation-Tile verwenden jetzt
  `sensor.grundwasser_poing_d83_situation_anzeige`.
- Die nur im UI-Storage vorhandenen Karten wurden als versionierte Quellen
  nach `ui/` zurückgeführt:
  - `apex-grundwasser-verlauf-card.yaml`
  - `apex-grundwasser-mobile-swipe-card.yaml`
- Der Desktop-Jahresvergleich dokumentiert nun seine Desktop-Visibility.

## SSH Mac → HA (Kurz)

| | Stand |
|--|--------|
| `ssh ha "whoami"` als `hassio` mit SSH-Key | ✓ funktioniert (ggf. Key-Passphrase) |
| `ssh ha "ha core check"` | ✗ `missing or invalid API token` |
| `ha`-CLI | nur Web-Terminal (Add-on, dort `whoami` = `root`) |

Details: [home-assistant-config/doc/ssh-from-mac.md](../../home-assistant-config/doc/ssh-from-mac.md)

## Bewusst später / anderes Projekt

- Generische Deploy-Pipeline (check → verify → reboot → test) — separates Projekt
- Baseline-Capture der Live-`configuration.yaml` — später
- Punkt „stabile Situation“ war dieses Bundle; generisches HA-Hardening nicht

## Sicherheitshinweis

Während der SSH-Einrichtung stand kurz ein Passwort fälschlich unter `authorized_keys` in der Terminal-Add-on-Config und im Chat. Passwort **ändern** bzw. nur Key-Login nutzen. Niemals Passwörter in Repo-Doku oder `authorized_keys`.
