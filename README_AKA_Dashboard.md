# AKA Teams Dashboard

Ein interaktives Streamlit Dashboard für die Analyse der AKA Teams (U15, U16, U18) mit Eigene Tore und Gegentore Visualisierung.

## 🚀 Installation

1. **Python Dependencies installieren:**
   ```bash
   pip install -r requirements_aka.txt
   ```

2. **Dashboard starten:**
   - **Option 1:** Doppelklick auf `AKA_Dashboard.bat`
   - **Option 2:** Manuell über Terminal:
     ```bash
     streamlit run aka_dashboard.py
     ```

## 📊 Features

### Team-Auswahl
- **U15** - Jugendteam U15
- **U16** - Jugendteam U16  
- **U18** - Jugendteam U18

### Statistik-Typen
- **Eigene Tore** - Tore die das Team erzielt hat
- **Gegentore** - Tore die das Team erhalten hat

### Visualisierung
- **Spielfeld-Darstellung** mit korrekten Maßen (68m x 100m)
- **Tor-Positionen** als rote Kreise markiert
- **Assist-Positionen** als gelbe Quadrate markiert
- **Passwege** als gestrichelte Linien zwischen Assists und Toren
- **Interaktive Sidebar** mit Team- und Statistik-Auswahl
- **Live-Statistiken** (Anzahl Tore und Assists)

## 🎯 Verwendung

1. **Team auswählen** in der linken Sidebar
2. **Statistik-Typ wählen** (Eigene Tore oder Gegentore)
3. **Spielfeld betrachten** mit allen Tor- und Assist-Positionen
4. **Details einsehen** in der rechten Spalte

## 📁 Dateien

- `aka_dashboard.py` - Haupt-Dashboard Anwendung
- `requirements_aka.txt` - Python Dependencies
- `AKA_Dashboard.bat` - Batch-Datei zum Starten
- `README_AKA_Dashboard.md` - Diese Dokumentation

## 🔧 Anpassungen

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

- Das Dashboard lädt automatisch das SV Ried Logo als Hintergrund (falls vorhanden unter `C:\Temp\SV_Ried.png`)
- Alle Koordinaten sind in Metern angegeben
- (0,0) entspricht der linken unteren Ecke des Spielfelds
- Das Dashboard läuft standardmäßig auf `http://localhost:8501`
