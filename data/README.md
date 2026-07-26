# Grundwasser-Daten

Dieser Ordner trennt unveränderte amtliche Rohdaten von abgeleiteten
Importdateien.

## `raw/`

Amtlicher Gesamtexport des Gewässerkundlichen Dienstes Bayern (GKD) für:

- Messstelle: **POING D 83**
- Messstellen-Nr.: **16268**
- Messgröße: Grundwasserstand oberes Stockwerk
- Werteart: Tagesmittelwerte
- Abruf: 26.07.2026
- Quelle:
  <https://www.gkd.bayern.de/de/grundwasser/oberesstockwerk/inn/poing-d-83-16268/download>

Archiv:

`raw/gkd-poing-d83-16268-tageswerte-gesamt.zip`

SHA-256:

`430c2b6b4870c11b04a797fbf91a7392b81d422312ad6c628815e98a78103344`

Die Dateien in `raw/` werden nicht bearbeitet. Leere amtliche Messwerte bleiben
dort leer.

## `statistics-import/`

Reproduzierbar erzeugte Ableitungen für Home Assistant:

- `grundwasser-poing-d83-statistics.csv`: lesbare Kontroll- und Auditdatei
- `import-*.json`: WebSocket-Payloads für `recorder/import_statistics`

Die CSV-Spalte `quality` unterscheidet:

- `official`: unverändert aus dem GKD-Export
- `interpolated`: linear ergänzte Lücke von höchstens sieben Tagen

Aktueller Bestand:

- Zeitraum: 01.01.2018 bis 24.07.2026
- 3.127 Tageswerte
- 3.112 amtliche Werte
- 15 interpolierte Werte

Die Ableitungen können jederzeit mit
`scripts/prepare-grundwasser-statistics.py` neu erzeugt werden.
