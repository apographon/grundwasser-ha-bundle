# Grundwasser CSV → Langzeitstatistik

Historische Tagesmittelwerte werden als native Home-Assistant-Langzeitstatistik
für `sensor.grundwasser_poing_d83_m_u_nn` importiert. Sie bleiben dauerhaft
erhalten und werden nicht durch `recorder.purge_keep_days` gelöscht.

## Daten und Aufbereitung

- Amtlicher GKD-Gesamtexport:
  `data/raw/gkd-poing-d83-16268-tageswerte-gesamt.zip`
- Aufbereitung:
  `scripts/prepare-grundwasser-statistics.py`
- Statistik-ID:
  `sensor.grundwasser_poing_d83_m_u_nn`
- Statistiktyp:
  Tagesmittel mit `mean`, `min` und `max`

Aufbereitung erneut ausführen:

```bash
python3 scripts/prepare-grundwasser-statistics.py \
  data/raw/gkd-poing-d83-16268-tageswerte-gesamt/grundwasser-gwo \
  data/statistics-import
```

Das Script übernimmt amtliche Werte ab 2018 und interpoliert ausschließlich
Lücken von höchstens sieben Tagen linear. Die Originaldateien bleiben
unverändert. Die abgeleitete CSV kennzeichnet jeden ergänzten Wert mit
`interpolated`.

## Import

Die Dateien `data/statistics-import/import-*.json` sind Payloads für den
Home-Assistant-WebSocket-Befehl `recorder/import_statistics`. Der Import wird
über die Home-Assistant-API ausgeführt, nicht durch direkte Änderungen an
`home-assistant_v2.db`.

Die Dashboard-Karte verwendet anschließend:

```yaml
statistics:
  type: mean
  period: day
  align: start
```

Der aktuelle REST-Sensor besitzt `state_class: measurement`. Home Assistant
führt seine Langzeitstatistik daher nach dem historischen Import automatisch
weiter.

## Prüfung

Mit `recorder/get_statistics_during_period` beziehungsweise der Statistik-
Historie müssen für 2018–2026 neun Jahreszeilen vorhanden sein. Der
GKD-Import vom 26.07.2026 enthält 3.127 Tageswerte ab 2018, davon 15
transparent gekennzeichnete Interpolationen.

Das vollständige Protokoll des ausgeführten Imports einschließlich Quelle,
Prüfsumme, Interpolationstagen, HA-Metadaten und Verifikation steht in
[import-protokoll-2026-07-26.md](import-protokoll-2026-07-26.md).

## Veralteter Recorder-Import

`scripts/import-grundwasser-csv-to-recorder.py` bleibt nur für Altinstallationen
erhalten. Dieser Weg schreibt Rohzustände direkt in SQLite; sie werden später
gepurgt und erfordern einen unnötig großen `purge_keep_days`-Wert. Für neue
Importe nicht mehr verwenden.
