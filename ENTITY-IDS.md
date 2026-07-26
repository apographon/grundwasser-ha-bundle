# Entity-IDs (Live-Stand)

Diese Datei dokumentiert die **tatsächlichen** Entity-IDs auf deiner Home-Assistant-Instanz. Sie ist die Referenz für Debugging und AI-Kontext.

**UI-Karten** verwenden den **Alias** `sensor.grundwasser_poing_d83_situation_anzeige` (stabil, ohne Suffix-Jagen). Hintergrund: [doc/situation-alias.md](doc/situation-alias.md).

**Aktualisieren:** Entwicklerwerkzeuge → Zustände → nach `grundwasser_poing` filtern.

| Beschreibung | Entity-ID auf Live | unique_id (YAML) | Rolle |
|--------------|-------------------|------------------|-------|
| Grundwasserstand m ü. NN | `sensor.grundwasser_poing_d83_m_u_nn` | `grundwasser_poing_d83_m_u_nn` | REST, Chart |
| Grundwasserstand m u. Gelände | `sensor.grundwasser_poing_d83_m_u_gelande` | `grundwasser_poing_d83_m_u_gelande` | REST |
| Situation (REST-Quelle) | `sensor.grundwasser_poing_d83_situation_3` | `grundwasser_poing_d83_situation` | NID-Daten; Suffix instanzabhängig |
| Situation (UI-Alias) | `sensor.grundwasser_poing_d83_situation_anzeige` | `grundwasser_poing_d83_situation_anzeige` | **Tile / Automations** |

Attribut `source_entity` am Alias zeigt, welche REST-Entity gerade gespiegelt wird.

## Wo die IDs verwendet werden

| Datei | Entity |
|-------|--------|
| `ui/apex-grundwasser-card.yaml` | `sensor.grundwasser_poing_d83_m_u_nn` |
| `ui/tile-grundwasser-situation.yaml` | `sensor.grundwasser_poing_d83_situation_anzeige` |
| `scripts/import-grundwasser-csv-to-recorder.py` | `ENTITY_ID` = m ü. NN |
| `integration/grundwasser_helpers.yaml` | Alias (Quelle automatisch) |

## Nach Neuaufsetzen / Restore

1. REST-Sensoren prüfen — Situation kann Suffix `_2`, `_3` haben oder ohne Suffix.
2. Alias `…_situation_anzeige` sollte automatisch die aktive Quelle wählen.
3. `source_entity`-Attribut am Alias prüfen.
4. Tabelle oben (REST-Zeile) bei Bedarf anpassen — **Tile-YAML nicht ändern**.
