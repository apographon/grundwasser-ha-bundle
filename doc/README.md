# Dokumentation (`doc/`)

Projekt-Doku für **grundwasser-bundle**. Konvention im HAss-Umfeld: immer **`doc/`** (Singular), nicht `docs/`.

| Datei | Thema |
|-------|--------|
| [deploy.md](deploy.md) | Deploy nach Live, Verifikation, Dashboard-Checkliste |
| [situation-alias.md](situation-alias.md) | Stabiler UI-Sensor `…_situation_anzeige` vs. REST mit Suffix |
| [csv-import.md](csv-import.md) | Historische CSV → permanente Langzeitstatistik |
| [import-protokoll-2026-07-26.md](import-protokoll-2026-07-26.md) | Quelle, Aufbereitung, Import und HA-Verifikation |
| [session-2026-05.md](session-2026-05.md) | Stand der Session (Alias, Deploy, offene Punkte) |

Dashboard-Quellen: `../ui/` enthält Tile, Jahresvergleich aller Jahre in
einer Grafik und den 365-Tage-Verlauf. Das Live-Dashboard läuft im
UI-Storage-Modus; Änderungen aus dem Dashboard-Editor müssen bewusst nach
`ui/` zurückgeführt werden.

Related (außerhalb des Bundles):

| Datei | Thema |
|-------|--------|
| [../ENTITY-IDS.md](../ENTITY-IDS.md) | Live Entity-IDs |
| [../../home-assistant-config/doc/ssh-from-mac.md](../../home-assistant-config/doc/ssh-from-mac.md) | SSH Mac → HA (Stand, Grenzen) |
