# Importprotokoll – 26.07.2026

## Ziel

Wiederherstellung des Jahresvergleichs 2018–2026, nachdem ältere
Recorder-Rohzustände durch einen kleineren `purge_keep_days`-Wert gelöscht
worden waren. Die Historie wurde als permanente Home-Assistant-
Langzeitstatistik importiert.

## Quelle

| Feld | Wert |
|------|------|
| Herausgeber | Bayerisches Landesamt für Umwelt / GKD Bayern |
| Messstelle | POING D 83 |
| Messstellen-Nr. | 16268 |
| Messgröße | Grundwasserstand oberes Stockwerk |
| Einheit | m ü. NN |
| Werteart | Tagesmittelwerte |
| GKD-Datenbestand | 01.11.1988 bis 25.07.2026 |
| Letzter gültiger Wert im Export | 24.07.2026 |
| Download | 26.07.2026 |
| Lizenz | Creative Commons Namensnennung 4.0 International |

Archiv:
`data/raw/gkd-poing-d83-16268-tageswerte-gesamt.zip`

SHA-256:
`430c2b6b4870c11b04a797fbf91a7392b81d422312ad6c628815e98a78103344`

## Aufbereitung

Ausgeführt mit:

```bash
python3 scripts/prepare-grundwasser-statistics.py \
  data/raw/gkd-poing-d83-16268-tageswerte-gesamt/grundwasser-gwo \
  data/statistics-import
```

Regeln:

1. Importbeginn ist der 01.01.2018.
2. Amtliche Werte werden ohne numerische Veränderung übernommen.
3. Nur geschlossene Lücken von höchstens sieben aufeinanderfolgenden Tagen
   werden linear zwischen dem vorherigen und nächsten amtlichen Wert ergänzt.
4. Längere oder nicht beidseitig begrenzte Lücken werden nicht interpoliert.
5. Interpolierte Werte werden in der Audit-CSV mit `quality=interpolated`
   gekennzeichnet.
6. Die Rohdateien werden niemals verändert.

Interpoliert wurden:

| Jahr | Tage |
|------|------|
| 2018 | 11.–12.03. und 03.–05.11. |
| 2021 | 03.–04.08. und 04.–08.10. |
| 2023 | 21.–23.11. |

Ergebnis: 3.127 Tageswerte, davon 15 interpoliert.

## Home-Assistant-Import

| Feld | Wert |
|------|------|
| HA-Version beim Import | 2026.7.4 |
| Statistik-ID | `sensor.grundwasser_poing_d83_m_u_nn` |
| Quelle | `recorder` |
| Einheit / Einheitenklasse | `m` / `distance` |
| Mittelwerttyp | arithmetisch (`mean_type: 1`) |
| Summenstatistik | nein |
| WebSocket-Befehl | `recorder/import_statistics` |
| Blockgröße | 750 Datensätze |
| Blöcke | 5 |

Pro Tag wurden `mean`, `min` und `max` mit dem Tagesmittelwert belegt. Das ist
korrekt, weil jeder Importdatensatz bereits genau einen amtlichen
Tagesmittelwert repräsentiert.

Der Import erfolgte in die bestehende Sensor-Statistik. Dadurch werden aktuelle
und zukünftige Werte des Sensors mit `state_class: measurement` automatisch in
derselben Statistik fortgeführt.

Eine zunächst zum Test angelegte externe Statistik
`grundwasser:poing_d83_m_u_nn` wurde nach erfolgreicher Übernahme mit
`recorder/clear_statistics` vollständig entfernt.

## Verifikation

Nach dem Import ergab die Jahresabfrage für
`sensor.grundwasser_poing_d83_m_u_nn` genau neun Statistikperioden:
2018 bis 2026.

Zusätzlich geprüft:

- Metadaten: `mean_type=1`, `has_sum=false`, Einheit `m`,
  Einheitenklasse `distance`
- Dashboard: neun Reihen 2018–2026
- Dashboard-Datenquelle: tägliche Langzeitstatistik (`mean`, `day`, `start`)
- Live-Dashboard-Schreibvorgang: erfolgreich gespeichert und erneut gelesen
- Temporäre externe Statistik: nicht mehr vorhanden

## Purge-Verhalten

`recorder.purge_keep_days` betrifft Recorder-Rohzustände und
Kurzzeitstatistiken. Die importierten Langzeitstatistiken bleiben erhalten.
Eine künstlich große Aufbewahrungsdauer ist für diese Grafik nicht mehr nötig.

## Dashboard-Änderung

Die Jahresvergleichskarte enthält nun:

```yaml
all_series_config:
  statistics:
    type: mean
    period: day
    align: start
```

Diese Änderung wurde sowohl im Live-Dashboard als auch in
`ui/apex-grundwasser-card.yaml` vorgenommen.
