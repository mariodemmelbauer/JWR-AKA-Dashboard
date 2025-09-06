# AKA Teams Dashboard

Ein interaktives Streamlit Dashboard für die Analyse der AKA Teams (U15, U16, U18) mit Eigene Tore und Gegentore Visualisierung.

## 🚀 Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mariodemmelbauer-jwr-aka-dashboard.streamlit.app/)

## 📊 Features

### Team-Auswahl
- **U15** - Jugendteam U15
- **U16** - Jugendteam U16  
- **U18** - Jugendteam U18

### Visualisierung
- **Spielfeld-Darstellung** mit korrekten Maßen (68m x 100m)
- **Tor-Positionen** als rote Kreise markiert
- **Assist-Positionen** als orange Quadrate markiert
- **Passwege** als gestrichelte Linien zwischen Assists und Toren
- **Dark Mode Design** mit grünen Akzentfarben
- **Nebeneinander-Anzeige** von Eigene Tore und Gegentore

## 🎯 Verwendung

1. **Team auswählen** in der linken Sidebar
2. **Spielfelder betrachten** mit allen Tor- und Assist-Positionen
3. **Live-Statistiken** in der Sidebar einsehen

## 🔧 Lokale Installation

1. **Repository klonen:**
   ```bash
   git clone https://github.com/mariodemmelbauer/JWR-AKA-Dashboard.git
   cd JWR-AKA-Dashboard
   ```

2. **Dependencies installieren:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Dashboard starten:**
   ```bash
   streamlit run aka_dashboard.py
   ```

## 📁 Projektstruktur

```
JWR-AKA-Dashboard/
├── aka_dashboard.py          # Haupt-Dashboard Anwendung
├── requirements.txt          # Python Dependencies
├── README.md                 # Projekt-Dokumentation
├── ForzaRied.png            # Logo für Sidebar
└── U15/                     # Team-spezifische Daten
    ├── EigeneToreU15.py
    └── GegentoreU15.py
```

## 🌐 Streamlit Cloud Bereitstellung

Das Dashboard kann einfach auf Streamlit Cloud bereitgestellt werden:

1. Gehen Sie zu [share.streamlit.io](https://share.streamlit.io)
2. Verbinden Sie Ihr GitHub Repository
3. Wählen Sie `aka_dashboard.py` als Hauptdatei
4. Deploy!

## 📝 Anpassungen

Die Tor- und Assist-Positionen können in der `TEAMS_DATA` Struktur in `aka_dashboard.py` angepasst werden:

```python
TEAMS_DATA = {
    "U15": {
        "eigene_tore": {
            "goals": [(x1,y1), (x2,y2), ...],  # Tor-Positionen
            "assists": [(x1,y1), (x2,y2), ...], # Assist-Positionen
            "title": "U15 - Eigene Tore"
        },
        # ...
    }
}
```

## 📝 Hinweise

- Alle Koordinaten sind in Metern angegeben
- (0,0) entspricht der linken unteren Ecke des Spielfelds
- Das Dashboard läuft standardmäßig auf `http://localhost:8501`
- Dark Mode Design für bessere Benutzerfreundlichkeit

## 🤝 Beitragen

Fork das Repository und erstellen Sie einen Pull Request für Verbesserungen.

## 📄 Lizenz

Dieses Projekt ist für den internen Gebrauch der AKA Teams bestimmt.

