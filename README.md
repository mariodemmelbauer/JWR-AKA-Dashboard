# AKA Teams Dashboard

Ein interaktives Streamlit Dashboard für die Analyse von Fußball-Statistiken der AKA Teams (U15, U16, U18).

## Features

- **Spielfeld-Visualisierung**: Interaktive Darstellung von Toren und Assists auf einem Fußballfeld
- **Team-Vergleich**: Vergleich zwischen verschiedenen Teams und Tor-Typen
- **Goldene Zone**: Analyse der Tore in der goldenen Zone (Strafraum)
- **Rote Zone**: Analyse der Assists in der roten Zone (zentraler Bereich)
- **Dynamische Daten**: Automatische Aktualisierung bei Dateiänderungen
- **Dark Mode**: Moderne, benutzerfreundliche Oberfläche

## Installation

1. Repository klonen:
```bash
git clone <repository-url>
cd aka-dashboard
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

3. Dashboard starten:
```bash
streamlit run aka_dashboard.py
```

## Verwendung

1. **Team-Auswahl**: Wähle zwei Teams für den Vergleich aus
2. **Tor-Typ**: Wähle zwischen "Eigene Tore" und "Gegentore"
3. **Zone-Auswahl**: Wähle zwischen "Goldene Zone" und "Rote Zone"
4. **Visualisierung**: Das Dashboard zeigt die Statistiken und das Spielfeld

## Datenstruktur

Das Dashboard erwartet folgende Ordnerstruktur:

```
.
├── U15/
│   ├── EigeneToreU15.py
│   └── GegentoreU15.py
├── U16/
│   ├── EigeneToreU16.py
│   └── GegentoreU16.py
├── U18/
│   ├── EigeneToreU18.py
│   └── GegentoreU18.py
└── aka_dashboard.py
```

## Dateiformat

Die Python-Dateien müssen folgende Struktur haben:

```python
# Beispiel: EigeneToreU15.py
goals = [(x1, y1), (x2, y2), ...]  # Koordinaten der Tore
assists = [(x1, y1), (x2, y2), ...]  # Koordinaten der Assists

plt.title("U15 - Eigene Tore\n Zusätzliche Informationen")
```

## Streamlit Cloud Deployment

1. Repository zu GitHub hochladen
2. Bei [Streamlit Cloud](https://share.streamlit.io) anmelden
3. Neues App erstellen
4. Repository auswählen
5. Hauptdatei: `aka_dashboard.py`
6. Deploy!

## Technische Details

- **Framework**: Streamlit
- **Visualisierung**: Matplotlib
- **Caching**: Automatische Cache-Invalidierung bei Dateiänderungen
- **Responsive Design**: Funktioniert auf Desktop und Mobile

## Lizenz

Dieses Projekt ist für interne Verwendung der AKA Teams bestimmt.