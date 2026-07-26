# Situation-Alias (UI vs REST)

## Problem

Home Assistant kann dem REST-Sensor `Grundwasser Poing D83 Situation` einen Suffix anhängen (`_2`, `_3`, …), wenn der Entity-Name in der Registry schon belegt war.

Beispiel Live-Stand (Poing):

| Rolle | Entity-ID |
|-------|-----------|
| REST-Quelle (NID) | `sensor.grundwasser_poing_d83_situation_3` |
| Neuinstallation (typisch) | `sensor.grundwasser_poing_d83_situation` (ohne Suffix) |

Dashboard-Tiles mit hardcodiertem `_3` brechen nach Restore/Neuaufsetzen.

## Lösung

Template-Sensor in `integration/grundwasser_helpers.yaml`:

| Entity | Rolle |
|--------|-------|
| `sensor.grundwasser_poing_d83_situation(_N)` | REST-Quelle — liefert die NID-Daten |
| `sensor.grundwasser_poing_d83_situation_anzeige` | **UI-Alias** — stabiler Name für Tile / Automations |

Der Alias:

- spiegelt den Zustand der REST-Quelle
- wählt automatisch eine Entity `sensor.grundwasser_poing_d83_situation` oder `…_situation_N` mit gültigem State
- setzt Attribut `source_entity` auf die gewählte Quelle

**Beide Sensoren parallel nutzbar:** REST für Historie/Debugging, Alias für Dashboard.

## Was sich ändert / was nicht

| | Auswirkung |
|--|------------|
| REST-Sensor | unverändert (bleibt `_3` oder wie vorhanden) |
| Neuer Template-Sensor | additiv — eine Entity mehr in der Liste |
| Historie | bleibt am REST-Sensor; Alias hat History erst ab Einrichtung |
| Tile | muss `…_situation_anzeige` verwenden |
| Deploy | `grundwasser_helpers.yaml` nach `integrations/` → Neustart |

## Dateien

| Datei | Inhalt |
|-------|--------|
| `integration/grundwasser_helpers.yaml` | Template-Alias |
| `ui/tile-grundwasser-situation.yaml` | Tile auf Alias |
| [ENTITY-IDS.md](../ENTITY-IDS.md) | Live-IDs inkl. `source_entity` |

## Nach Deploy prüfen

1. `sensor.grundwasser_poing_d83_situation_anzeige` hat Wert (`kein Niedrigwasser` / `niedrig` / `Niedrigwasser`)
2. Attribut `source_entity` zeigt z. B. `sensor.grundwasser_poing_d83_situation_3`
3. Dashboard-Tile im **UI-Storage** auf den Alias umstellen (Deploy aktualisiert Lovelace-UI-Storage **nicht**)
