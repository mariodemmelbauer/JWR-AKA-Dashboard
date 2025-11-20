import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import numpy as np
import os
import re
import ast
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Konfiguration der Seite
st.set_page_config(
    page_title="AKA Teams Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Mode CSS
st.markdown("""
<style>
    .stApp {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .main-header {
        font-size: 2.5rem;
        color: #00ff88;
        text-align: center;
        margin-bottom: 2rem;
    }
    .team-card {
        background-color: #2d2d2d;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #3d3d3d;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        margin: 0.5rem 0;
    }
    .stSelectbox > div > div {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    .stSelectbox label {
        color: #ffffff;
    }
    .stSidebar {
        background-color: #1a1a1a;
    }
    .stSidebar .stMarkdown {
        color: #ffffff;
    }
    .stSidebar .stMetric {
        background-color: #2d2d2d;
        border-radius: 8px;
        padding: 1rem;
    }
    .stSidebar .stMetric > div {
        color: #ffffff;
    }
    .stSidebar .stMetric > div > div {
        color: #00ff88;
    }
</style>
""", unsafe_allow_html=True)

# Dark Mode CSS bereits oben definiert

def extract_goals_and_assists_from_file(file_path: str) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    """
    Extrahiert Goals und Assists aus einer Python-Datei.
    Sucht nach Zeilen mit 'goals = [...]' und 'assists = [...]'
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Regex-Pattern für goals und assists
        goals_pattern = r'goals\s*=\s*\[(.*?)\]'
        assists_pattern = r'assists\s*=\s*\[(.*?)\]'
        
        goals_match = re.search(goals_pattern, content, re.DOTALL)
        assists_match = re.search(assists_pattern, content, re.DOTALL)
        
        goals = []
        assists = []
        
        if goals_match:
            goals_str = goals_match.group(1).strip()
            if goals_str:
                # Parse die Liste von Tupeln
                try:
                    goals = ast.literal_eval(f'[{goals_str}]')
                except:
                    # Fallback: manuell parsen
                    goals = parse_coordinates(goals_str)
        
        if assists_match:
            assists_str = assists_match.group(1).strip()
            if assists_str:
                try:
                    assists = ast.literal_eval(f'[{assists_str}]')
                except:
                    assists = parse_coordinates(assists_str)
        
        return goals, assists
    
    except Exception as e:
        st.warning(f"Fehler beim Lesen der Datei {file_path}: {str(e)}")
        return [], []

def parse_coordinates(coord_str: str) -> List[Tuple[int, int]]:
    """
    Parst Koordinaten aus einem String.
    Behandelt verschiedene Formate wie (x,y), (x, y), etc.
    """
    coordinates = []
    # Entferne Leerzeichen und teile bei Kommas
    coord_str = coord_str.replace(' ', '')
    
    # Finde alle Tupel-Pattern
    pattern = r'\((\d+(?:\.\d+)?),(\d+(?:\.\d+)?)\)'
    matches = re.findall(pattern, coord_str)
    
    for match in matches:
        try:
            x = int(float(match[0]))
            y = int(float(match[1]))
            coordinates.append((x, y))
        except ValueError:
            continue
    
    return coordinates

def extract_additional_info_from_file(file_path: str) -> str:
    """
    Extrahiert zusätzliche Informationen aus dem plt.title() einer Python-Datei.
    Sucht nach Zeilen wie plt.title("U18 - Gegentore\n 2 Elfmeter n.b.")
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Regex-Pattern für plt.title() mit zusätzlichen Informationen
        title_pattern = r'plt\.title\(".*?\\n\s*(.*?)"\)'
        match = re.search(title_pattern, content, re.DOTALL)
        
        if match:
            additional_info = match.group(1).strip()
            # Entferne führende/trailing Leerzeichen und Zeilenumbrüche
            additional_info = additional_info.replace('\n', ' ').strip()
            return additional_info
        
        return ""
    
    except Exception as e:
        return ""

def get_file_modification_times(base_path: str = ".") -> str:
    """
    Erstellt einen String mit den Modifikationszeiten aller relevanten Dateien.
    Wird als Cache-Key verwendet, um automatisch zu erkennen, wenn Dateien geändert wurden.
    """
    teams = ["U15", "U16", "U18", "JWR", "Profis"]
    modification_times = []
    
    for team in teams:
        if team == "JWR":
            # Spezielle Behandlung für JWR
            team_folder = os.path.join(base_path, team)
            if os.path.exists(team_folder):
                eigene_tore_file = os.path.join(team_folder, "EigeneToreJWR.py")
                gegentore_file = os.path.join(team_folder, "GegentoreJWR.py")
                
                if os.path.exists(eigene_tore_file):
                    mod_time = os.path.getmtime(eigene_tore_file)
                    modification_times.append(f"{team}_eigene_{mod_time}")
                
                if os.path.exists(gegentore_file):
                    mod_time = os.path.getmtime(gegentore_file)
                    modification_times.append(f"{team}_gegentore_{mod_time}")
        else:
            team_folder = os.path.join(base_path, team)
            if os.path.exists(team_folder):
                # Prüfe EigeneTore und Gegentore Dateien
                eigene_tore_file = os.path.join(team_folder, f"EigeneTore{team}.py")
                gegentore_file = os.path.join(team_folder, f"Gegentore{team}.py")
                
                if os.path.exists(eigene_tore_file):
                    mod_time = os.path.getmtime(eigene_tore_file)
                    modification_times.append(f"{team}_eigene_{mod_time}")
                
                if os.path.exists(gegentore_file):
                    mod_time = os.path.getmtime(gegentore_file)
                    modification_times.append(f"{team}_gegentore_{mod_time}")
    
    return "_".join(modification_times)

def load_team_data_from_files(base_path: str = ".") -> Dict[str, Dict[str, Any]]:
    """
    Lädt alle Team-Daten automatisch aus den Dateien im AKA-Ordner.
    """
    teams_data = {}
    
    # Definiere die verfügbaren Teams und deren Ordner
    teams = ["U15", "U16", "U18", "JWR", "Profis"]
    
    for team in teams:
        if team == "JWR":
            # Spezielle Behandlung für JWR
            team_folder = os.path.join(base_path, team)
            
            if not os.path.exists(team_folder):
                st.warning(f"Team-Ordner {team_folder} nicht gefunden!")
                continue
            
            # Lade eigene Tore
            eigene_tore_file = os.path.join(team_folder, "EigeneToreJWR.py")
            eigene_goals, eigene_assists = extract_goals_and_assists_from_file(eigene_tore_file)
            eigene_additional_info = extract_additional_info_from_file(eigene_tore_file)
            
            # Lade Gegentore
            gegentore_file = os.path.join(team_folder, "GegentoreJWR.py")
            gegentore_goals, gegentore_assists = extract_goals_and_assists_from_file(gegentore_file)
            gegentore_additional_info = extract_additional_info_from_file(gegentore_file)
        else:
            team_folder = os.path.join(base_path, team)
            
            if not os.path.exists(team_folder):
                st.warning(f"Team-Ordner {team_folder} nicht gefunden!")
                continue
            
            # Lade eigene Tore
            eigene_tore_file = os.path.join(team_folder, f"EigeneTore{team}.py")
            eigene_goals, eigene_assists = extract_goals_and_assists_from_file(eigene_tore_file)
            eigene_additional_info = extract_additional_info_from_file(eigene_tore_file)
            
            # Lade Gegentore
            gegentore_file = os.path.join(team_folder, f"Gegentore{team}.py")
            gegentore_goals, gegentore_assists = extract_goals_and_assists_from_file(gegentore_file)
            gegentore_additional_info = extract_additional_info_from_file(gegentore_file)
        
        # Erstelle Team-Datenstruktur
        teams_data[team] = {
        "eigene_tore": {
                "goals": eigene_goals,
                "assists": eigene_assists,
                "title": f"{team} - Eigene Tore",
                "additional_info": eigene_additional_info
        },
        "gegentore": {
                "goals": gegentore_goals,
                "assists": gegentore_assists,
                "title": f"{team} - Gegentore",
                "additional_info": gegentore_additional_info
            }
        }
    
    return teams_data

# Lade Team-Daten automatisch
@st.cache_data(ttl=300)  # Cache für 5 Minuten, aber wird durch Datei-Änderungen invalidiert
def get_teams_data(file_modification_key: str):
    """Lädt die Team-Daten mit Caching für bessere Performance."""
    return load_team_data_from_files()

# Datenstrukturen für alle Teams (wird automatisch aktualisiert)
# TEAMS_DATA wird jetzt in main() geladen mit automatischer Datei-Erkennung

def count_goals_in_dashed_zones(goals):
    """Zählt Tore in den gestrichelten Zonen und gibt Prozentsätze zurück, getrennt nach goldenen und roten Zonen"""
    total_goals = len(goals)
    if total_goals == 0:
        return {
            'goldene_zone': 0,  # x: 25-43, y: 84-100 (goldene Zone)
            'rote_zone': 0,     # x: 25-43, y: 75-84 (rote Zone)
            'zone2': 0,  # x: 14-25, y: 75-84 (links oben)
            'zone3': 0,  # x: 43-54, y: 75-84 (rechts oben)
            'zone4': 0,  # x: 0-14, y: 75-90 (links unten)
            'zone5': 0,  # x: 54-68, y: 75-90 (rechts unten)
            'zone6': 0,  # x: 14-25, y: 84-100 (links oben erweitert)
            'zone7': 0,  # x: 43-54, y: 84-100 (rechts oben erweitert)
            'restliches_spielfeld': 0,  # Alle Tore außerhalb der gestrichelten Zonen
            'total': 0
        }
    
    goldene_zone_count = 0  # x: 25-43, y: 84-100 (goldene Zone)
    rote_zone_count = 0      # x: 25-43, y: 75-84 (rote Zone)
    zone2_count = 0  # x: 14-25, y: 75-84 (links oben)
    zone3_count = 0  # x: 43-54, y: 75-84 (rechts oben)
    zone4_count = 0  # x: 0-14, y: 75-90 (links unten)
    zone5_count = 0  # x: 54-68, y: 75-90 (rechts unten)
    zone6_count = 0  # x: 14-25, y: 84-100 (links oben erweitert)
    zone7_count = 0  # x: 43-54, y: 84-100 (rechts oben erweitert)
    restliches_spielfeld_count = 0  # Alle Tore außerhalb der gestrichelten Zonen
    
    for goal in goals:
        x, y = goal
        in_dashed_zone = False
        
        # Prüfe, ob das Tor in einer gestrichelten Zone liegt (y >= 75)
        if y >= 75:
            # Goldene Zone: zentral oben (x: 25-43, y: 84-100)
            if 25 <= x <= 43 and 84 <= y <= 100:
                goldene_zone_count += 1
                in_dashed_zone = True
            # Rote Zone: zentral oben (x: 25-43, y: 75-84)
            elif 25 <= x <= 43 and 75 <= y < 84:
                rote_zone_count += 1
                in_dashed_zone = True
            # Zone 2: links oben (zwischen x=14 und x=25, unterhalb y=84)
            elif 14 <= x < 25 and 75 <= y <= 84:
                zone2_count += 1
                in_dashed_zone = True
            # Zone 3: rechts oben (zwischen x=43 und x=54, unterhalb y=84)
            elif 43 < x <= 54 and 75 <= y <= 84:
                zone3_count += 1
                in_dashed_zone = True
            # Zone 4: links unten (zwischen x=0 und x=14)
            elif 0 <= x < 14 and 75 <= y <= 90:
                zone4_count += 1
                in_dashed_zone = True
            # Zone 5: rechts unten (zwischen x=54 und x=68)
            elif 54 < x <= 68 and 75 <= y <= 90:
                zone5_count += 1
                in_dashed_zone = True
            # Zone 6: links oben erweitert (zwischen x=14 und x=25, oberhalb y=84)
            elif 14 <= x < 25 and 84 < y <= 100:
                zone6_count += 1
                in_dashed_zone = True
            # Zone 7: rechts oben erweitert (zwischen x=43 und x=54, oberhalb y=84)
            elif 43 < x <= 54 and 84 < y <= 100:
                zone7_count += 1
                in_dashed_zone = True
        
        # Wenn das Tor nicht in einer gestrichelten Zone liegt, zähle es zum restlichen Spielfeld
        if not in_dashed_zone:
            restliches_spielfeld_count += 1
    
    return {
        'goldene_zone': (goldene_zone_count / total_goals * 100) if total_goals > 0 else 0,
        'rote_zone': (rote_zone_count / total_goals * 100) if total_goals > 0 else 0,
        'zone2': (zone2_count / total_goals * 100) if total_goals > 0 else 0,
        'zone3': (zone3_count / total_goals * 100) if total_goals > 0 else 0,
        'zone4': (zone4_count / total_goals * 100) if total_goals > 0 else 0,
        'zone5': (zone5_count / total_goals * 100) if total_goals > 0 else 0,
        'zone6': (zone6_count / total_goals * 100) if total_goals > 0 else 0,
        'zone7': (zone7_count / total_goals * 100) if total_goals > 0 else 0,
        'restliches_spielfeld': (restliches_spielfeld_count / total_goals * 100) if total_goals > 0 else 0,
        'total': total_goals
    }

def draw_field(team, goal_type, teams_data):
    """Zeichnet das Spielfeld mit den entsprechenden Toren und Assists"""
    # Dark Mode für Matplotlib
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 12))
    ax.set_facecolor('#1a1a1a')  # Dunkler Hintergrund
    ax.set_xlim(0, 68)  # Spielfeldbreite (m)
    ax.set_ylim(0, 100)  # Spielfeldtiefe (m)
    
    # SV Ried Logo als Hintergrund einfügen (falls vorhanden)
    logo_path = "C:\\Temp\\SV_Ried.png"
    if os.path.exists(logo_path):
        try:
            logo = mpimg.imread(logo_path)
            ax.imshow(logo, extent=[0, 68, 0, 100], alpha=0.05)
        except:
            pass  # Logo wird ignoriert falls es nicht geladen werden kann
    
    # Spielfeldlinien hinzufügen
    ax.plot([0, 68], [50, 50], '#00ff88', linestyle="-", zorder=5, linewidth=2)  # Mittellinie
    mittelkreis = patches.Circle((34, 50), 9, edgecolor='#00ff88', facecolor='none', linewidth=2)  # Mittelkreis
    ax.add_patch(mittelkreis)

    # Gestrichelte Linien hinzufügen
    ax.plot([43, 43], [100, 75], '#00ff88', linestyle="--", linewidth=2)  # Erste gestrichelte Linie
    ax.plot([25, 25], [100, 75], '#00ff88', linestyle="--", linewidth=2)  # Zweite gestrichelte Linie
    ax.plot([43, 54, 54], [100, 84, 75], '#00ff88', linestyle="--", linewidth=2)  # Dritte gestrichelte Linie
    ax.plot([25, 14, 14], [100, 84, 75], '#00ff88', linestyle="--", linewidth=2)  # Vierte gestrichelte Linie
    ax.plot([14, 0], [90, 90], '#00ff88', linestyle="--", linewidth=2)  # Neue horizontale Linie links
    ax.plot([54, 68], [90, 90], '#00ff88', linestyle="--", linewidth=2)  # Neue horizontale Linie rechts

    # Fünfmeterraum hinzufügen (5m tief, 18m breit)
    fuenfmeter_oben = patches.Rectangle((25, 100), 18, -5, edgecolor='#00ff88', facecolor='none', linewidth=2)
    ax.add_patch(fuenfmeter_oben)

    fuenfmeter_unten = patches.Rectangle((25, 0), 18, 5, edgecolor='#00ff88', facecolor='none', linewidth=2)
    ax.add_patch(fuenfmeter_unten)

    # Sechzehnmeterraum hinzufügen (16m tief, 40m breit)
    sechzehn_oben = patches.Rectangle((14, 100), 40, -16, edgecolor='#00ff88', facecolor='none', linewidth=2)
    ax.add_patch(sechzehn_oben)

    sechzehn_unten = patches.Rectangle((14, 0), 40, 16, edgecolor='#00ff88', facecolor='none', linewidth=2)
    ax.add_patch(sechzehn_unten)

    # Goldene Zone im oberen Strafraum (zwischen Torlinie, 5m Raum und 16m Linie)
    goldene_zone_oben = patches.Rectangle((25, 100), 18, -16, edgecolor='none', facecolor='gold', alpha=0.3)
    ax.add_patch(goldene_zone_oben)

    # Rote Zone mit 5m Raum Breite (18m) unterhalb der goldenen Zone bis zur gestrichelten Linie (y=75)
    # Gleiche Breite wie 5m Raum: x von 25 bis 43 (18m breit), y von 75 bis 84 (16m Linie)
    rote_zone_zentral = patches.Rectangle((25, 75), 18, 9, edgecolor='none', facecolor='red', alpha=0.3)
    ax.add_patch(rote_zone_zentral)

    # Elfmeterpunkte hinzufügen
    ax.scatter(34, 89, color='#00ff88', marker='o')  # Elfmeterpunkt oben
    ax.scatter(34, 11, color='#00ff88', marker='o')  # Elfmeterpunkt unten

    # Halbkreise um die Elfmeterpunkte
    halbkreis_oben = patches.Arc((34, 89), 18, 18, angle=0, theta1=215, theta2=325, edgecolor='#00ff88', linewidth=2)
    ax.add_patch(halbkreis_oben)

    halbkreis_unten = patches.Arc((34, 11), 18, 18, angle=0, theta1=35, theta2=145, edgecolor='#00ff88', linewidth=2)
    ax.add_patch(halbkreis_unten)

    # Daten für das ausgewählte Team und Tor-Typ abrufen
    team_data = teams_data[team][goal_type]
    goals = team_data["goals"]
    assists = team_data["assists"]
    title = team_data["title"]

    # Tore markieren (Farbe abhängig vom Tor-Typ)
    if goal_type == "eigene_tore":
        # Eigene Tore: grün-schwarz
        for i, goal in enumerate(goals):
            ax.scatter(goal[0], goal[1], color='#00ff00', edgecolors='#000000', marker='o', s=50, 
                      label='Tor' if i == 0 else "", zorder=10)
    else:
        # Gegentore: rot-weiß
        for i, goal in enumerate(goals):
            ax.scatter(goal[0], goal[1], color='#ff4444', edgecolors='#ffffff', marker='o', s=50, 
                      label='Tor' if i == 0 else "", zorder=10)

    # Assists markieren (gelbe Quadrate)
    for i, assist in enumerate(assists):
        ax.scatter(assist[0], assist[1], color='#ffaa00', marker='s', s=30, 
                  label='Assist' if i == 0 else "", zorder=10)

    # Verbindungslinien zwischen Assist und Tor (Passwege)
    for i in range(min(len(goals), len(assists))):
        ax.plot([assists[i][0], goals[i][0]], [assists[i][1], goals[i][1]], 
                '#ffffff', linestyle="--", alpha=0.5, linewidth=1)

    # Berechne Prozentsätze für gestrichelte Zonen
    zone_percentages = count_goals_in_dashed_zones(goals)
    
    # Zeige Prozentsätze in den gestrichelten Zonen (leicht transparent)
    # Goldene Zone: zentral oben (x: 25-43, y: 84-100) - ganz oben positioniert
    if zone_percentages['goldene_zone'] > 0:
        ax.text(34, 100, f"{zone_percentages['goldene_zone']:.1f}%", 
                ha='center', va='center', fontsize=12, fontweight='bold',
                color='#ffd700', alpha=0.8, 
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.6, edgecolor='#ffd700', linewidth=1))
    
    # Rote Zone: zentral oben (x: 25-43, y: 75-84) - ganz unten positioniert
    if zone_percentages['rote_zone'] > 0:
        ax.text(34, 75, f"{zone_percentages['rote_zone']:.1f}%", 
                ha='center', va='center', fontsize=12, fontweight='bold',
                color='#ff4444', alpha=0.8, 
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.6, edgecolor='#ff4444', linewidth=1))
    
    # Zone 2: links oben (x: 14-25, y: 75-84)
    if zone_percentages['zone2'] > 0:
        ax.text(19.5, 79.5, f"{zone_percentages['zone2']:.1f}%", 
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='none'))
    
    # Zone 3: rechts oben (x: 43-54, y: 75-84)
    if zone_percentages['zone3'] > 0:
        ax.text(48.5, 79.5, f"{zone_percentages['zone3']:.1f}%", 
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='none'))
    
    # Zone 4: links unten (x: 0-14, y: 75-90)
    if zone_percentages['zone4'] > 0:
        ax.text(7, 82.5, f"{zone_percentages['zone4']:.1f}%", 
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='none'))
    
    # Zone 5: rechts unten (x: 54-68, y: 75-90)
    if zone_percentages['zone5'] > 0:
        ax.text(61, 82.5, f"{zone_percentages['zone5']:.1f}%", 
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='none'))
    
    # Zone 6: links oben erweitert (x: 14-25, y: 84-100)
    if zone_percentages['zone6'] > 0:
        ax.text(19.5, 92, f"{zone_percentages['zone6']:.1f}%", 
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='none'))
    
    # Zone 7: rechts oben erweitert (x: 43-54, y: 84-100)
    if zone_percentages['zone7'] > 0:
        ax.text(48.5, 92, f"{zone_percentages['zone7']:.1f}%", 
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='none'))
    
    # Restliches Spielfeld: Alle Tore außerhalb der gestrichelten Zonen
    if zone_percentages['restliches_spielfeld'] > 0:
        ax.text(34, 55, f"{zone_percentages['restliches_spielfeld']:.1f}%", 
                ha='center', va='center', fontsize=12, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='#ffffff', linewidth=1))

    # Legende
    ax.legend(loc="lower left", fontsize=10, framealpha=0.8)

    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("Spielfeldbreite (m)", fontsize=12)
    plt.ylabel("Spielfeldtiefe (m)", fontsize=12)
    
    # Achsenbeschriftungen entfernen für sauberes Aussehen
    ax.set_xticks([])
    ax.set_yticks([])
    
    return fig

def draw_all_teams_field(goal_type, teams_data):
    """Zeichnet ein Spielfeld mit allen Toren aller Teams für einen bestimmten Tor-Typ"""
    # Dark Mode für Matplotlib
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 12))
    ax.set_facecolor('#1a1a1a')  # Dunkler Hintergrund
    ax.set_xlim(0, 68)  # Spielfeldbreite (m)
    ax.set_ylim(0, 100)  # Spielfeldtiefe (m)
    
    # SV Ried Logo als Hintergrund einfügen (falls vorhanden)
    logo_path = "C:\\Temp\\SV_Ried.png"
    if os.path.exists(logo_path):
        try:
            logo = mpimg.imread(logo_path)
            ax.imshow(logo, extent=[0, 68, 0, 100], alpha=0.05)
        except:
            pass  # Logo wird ignoriert falls es nicht geladen werden kann
    
    # Spielfeldlinien hinzufügen (gleiche wie in draw_field)
    ax.plot([0, 68], [50, 50], '#00ff88', linestyle="-", zorder=5, linewidth=2)  # Mittellinie
    mittelkreis = patches.Circle((34, 50), 9, edgecolor='#00ff88', facecolor='none', linewidth=2)  # Mittelkreis
    ax.add_patch(mittelkreis)

    # Gestrichelte Linien hinzufügen
    ax.plot([43, 43], [100, 75], '#00ff88', linestyle="--", linewidth=2)  # Erste gestrichelte Linie
    ax.plot([25, 25], [100, 75], '#00ff88', linestyle="--", linewidth=2)  # Zweite gestrichelte Linie
    ax.plot([43, 54, 54], [100, 84, 75], '#00ff88', linestyle="--", linewidth=2)  # Dritte gestrichelte Linie
    ax.plot([25, 14, 14], [100, 84, 75], '#00ff88', linestyle="--", linewidth=2)  # Vierte gestrichelte Linie
    ax.plot([14, 0], [90, 90], '#00ff88', linestyle="--", linewidth=2)  # Neue horizontale Linie links
    ax.plot([54, 68], [90, 90], '#00ff88', linestyle="--", linewidth=2)  # Neue horizontale Linie rechts

    # Fünfmeterraum hinzufügen (5m tief, 18m breit)
    fuenfmeter_oben = patches.Rectangle((25, 100), 18, -5, edgecolor='#00ff88', facecolor='none', linewidth=2)
    ax.add_patch(fuenfmeter_oben)

    fuenfmeter_unten = patches.Rectangle((25, 0), 18, 5, edgecolor='#00ff88', facecolor='none', linewidth=2)
    ax.add_patch(fuenfmeter_unten)

    # Sechzehnmeterraum hinzufügen (16m tief, 40m breit)
    sechzehn_oben = patches.Rectangle((14, 100), 40, -16, edgecolor='#00ff88', facecolor='none', linewidth=2)
    ax.add_patch(sechzehn_oben)

    sechzehn_unten = patches.Rectangle((14, 0), 40, 16, edgecolor='#00ff88', facecolor='none', linewidth=2)
    ax.add_patch(sechzehn_unten)

    # Goldene Zone im oberen Strafraum (zwischen Torlinie, 5m Raum und 16m Linie)
    goldene_zone_oben = patches.Rectangle((25, 100), 18, -16, edgecolor='none', facecolor='gold', alpha=0.3)
    ax.add_patch(goldene_zone_oben)

    # Rote Zone mit 5m Raum Breite (18m) unterhalb der goldenen Zone bis zur gestrichelten Linie (y=75)
    # Gleiche Breite wie 5m Raum: x von 25 bis 43 (18m breit), y von 75 bis 84 (16m Linie)
    rote_zone_zentral = patches.Rectangle((25, 75), 18, 9, edgecolor='none', facecolor='red', alpha=0.3)
    ax.add_patch(rote_zone_zentral)

    # Elfmeterpunkte hinzufügen
    ax.scatter(34, 89, color='#00ff88', marker='o')  # Elfmeterpunkt oben
    ax.scatter(34, 11, color='#00ff88', marker='o')  # Elfmeterpunkt unten

    # Halbkreise um die Elfmeterpunkte
    halbkreis_oben = patches.Arc((34, 89), 18, 18, angle=0, theta1=215, theta2=325, edgecolor='#00ff88', linewidth=2)
    ax.add_patch(halbkreis_oben)

    halbkreis_unten = patches.Arc((34, 11), 18, 18, angle=0, theta1=35, theta2=145, edgecolor='#00ff88', linewidth=2)
    ax.add_patch(halbkreis_unten)

    # Sammle alle Tore aller Teams
    all_goals = []
    all_assists = []
    
    # Bestimme Farben basierend auf Tor-Typ (wie bei einzelnen Teams)
    if goal_type == "eigene_tore":
        goal_color = '#00ff00'  # Grün für eigene Tore
        goal_edge = '#000000'   # Schwarz für eigene Tore
    else:
        goal_color = '#ff4444'  # Rot für Gegentore
        goal_edge = '#ffffff'   # Weiß für Gegentore
    
    assist_color = '#ffaa00'    # Gelb für alle Assists
    
    for i, (team, team_data) in enumerate(teams_data.items()):
        goals = team_data[goal_type]["goals"]
        assists = team_data[goal_type]["assists"]
        
        # Tore mit einheitlicher Farbe markieren (basierend auf Tor-Typ)
        for j, goal in enumerate(goals):
            ax.scatter(goal[0], goal[1], color=goal_color, edgecolors=goal_edge, marker='o', s=50, 
                      label=f'{team} Tor' if j == 0 else "", zorder=10)
            all_goals.append(goal)
        
        # Assists mit einheitlicher Farbe markieren
        for j, assist in enumerate(assists):
            ax.scatter(assist[0], assist[1], color=assist_color, marker='s', s=30, 
                      label=f'{team} Assist' if j == 0 else "", zorder=10)
            all_assists.append(assist)

    # Verbindungslinien zwischen Assist und Tor (Passwege)
    for i in range(min(len(all_goals), len(all_assists))):
        ax.plot([all_assists[i][0], all_goals[i][0]], [all_assists[i][1], all_goals[i][1]], 
                '#ffffff', linestyle="--", alpha=0.5, linewidth=1)

    # Berechne Prozentsätze für gestrichelte Zonen (nur Tore)
    zone_percentages = count_goals_in_dashed_zones(all_goals)
    
    # Zeige Prozentsätze in den gestrichelten Zonen (leicht transparent)
    # Goldene Zone: zentral oben (x: 25-43, y: 84-100) - ganz oben positioniert
    if zone_percentages['goldene_zone'] > 0:
        ax.text(34, 100, f"{zone_percentages['goldene_zone']:.1f}%", 
                ha='center', va='center', fontsize=12, fontweight='bold',
                color='#ffd700', alpha=0.8, 
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.6, edgecolor='#ffd700', linewidth=1))
    
    # Rote Zone: zentral oben (x: 25-43, y: 75-84) - ganz unten positioniert
    if zone_percentages['rote_zone'] > 0:
        ax.text(34, 75, f"{zone_percentages['rote_zone']:.1f}%", 
                ha='center', va='center', fontsize=12, fontweight='bold',
                color='#ff4444', alpha=0.8, 
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.6, edgecolor='#ff4444', linewidth=1))
    
    # Zone 2: links oben (x: 14-25, y: 75-84)
    if zone_percentages['zone2'] > 0:
        ax.text(19.5, 79.5, f"{zone_percentages['zone2']:.1f}%", 
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='none'))
    
    # Zone 3: rechts oben (x: 43-54, y: 75-84)
    if zone_percentages['zone3'] > 0:
        ax.text(48.5, 79.5, f"{zone_percentages['zone3']:.1f}%", 
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='none'))
    
    # Zone 4: links unten (x: 0-14, y: 75-90)
    if zone_percentages['zone4'] > 0:
        ax.text(7, 82.5, f"{zone_percentages['zone4']:.1f}%", 
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='none'))
    
    # Zone 5: rechts unten (x: 54-68, y: 75-90)
    if zone_percentages['zone5'] > 0:
        ax.text(61, 82.5, f"{zone_percentages['zone5']:.1f}%", 
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='none'))
    
    # Zone 6: links oben erweitert (x: 14-25, y: 84-100)
    if zone_percentages['zone6'] > 0:
        ax.text(19.5, 92, f"{zone_percentages['zone6']:.1f}%", 
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='none'))
    
    # Zone 7: rechts oben erweitert (x: 43-54, y: 84-100)
    if zone_percentages['zone7'] > 0:
        ax.text(48.5, 92, f"{zone_percentages['zone7']:.1f}%", 
                ha='center', va='center', fontsize=11, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='none'))
    
    # Restliches Spielfeld: Alle Tore außerhalb der gestrichelten Zonen
    if zone_percentages['restliches_spielfeld'] > 0:
        ax.text(34, 55, f"{zone_percentages['restliches_spielfeld']:.1f}%", 
                ha='center', va='center', fontsize=12, fontweight='bold',
                color='#ffffff', alpha=0.7,
                bbox=dict(boxstyle='round', facecolor='#000000', alpha=0.5, edgecolor='#ffffff', linewidth=1))

    # Legende
    ax.legend(loc="lower left", fontsize=8, framealpha=0.8)

    goal_type_display = "Eigene Tore" if goal_type == "eigene_tore" else "Gegentore"
    plt.title(f"Alle Teams - {goal_type_display}", fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("Spielfeldbreite (m)", fontsize=12)
    plt.ylabel("Spielfeldtiefe (m)", fontsize=12)
    
    # Achsenbeschriftungen entfernen für sauberes Aussehen
    ax.set_xticks([])
    ax.set_yticks([])
    
    return fig

def count_goals_in_zone(goals, zone_name):
    """Zählt Tore in einer spezifischen Zone"""
    count = 0
    for goal in goals:
        x, y = goal
        if zone_name == "Goldene Zone":
            if 25 <= x <= 43 and 84 <= y <= 100:
                count += 1
        elif zone_name == "Rote Zone":
            if 25 <= x <= 43 and 75 <= y < 84:
                count += 1
        elif zone_name == "Zone 2":
            if 14 <= x < 25 and 75 <= y <= 84:
                count += 1
        elif zone_name == "Zone 3":
            if 43 < x <= 54 and 75 <= y <= 84:
                count += 1
        elif zone_name == "Zone 4":
            if 0 <= x < 14 and 75 <= y <= 90:
                count += 1
        elif zone_name == "Zone 5":
            if 54 < x <= 68 and 75 <= y <= 90:
                count += 1
        elif zone_name == "Zone 6":
            if 14 <= x < 25 and 84 < y <= 100:
                count += 1
        elif zone_name == "Zone 7":
            if 43 < x <= 54 and 84 < y <= 100:
                count += 1
        elif zone_name == "Restliches Spielfeld":
            # Alle Tore außerhalb der gestrichelten Zonen
            in_zone = False
            if y >= 75:
                if (25 <= x <= 43 and 84 <= y <= 100) or \
                   (25 <= x <= 43 and 75 <= y < 84) or \
                   (14 <= x < 25 and 75 <= y <= 84) or \
                   (43 < x <= 54 and 75 <= y <= 84) or \
                   (0 <= x < 14 and 75 <= y <= 90) or \
                   (54 < x <= 68 and 75 <= y <= 90) or \
                   (14 <= x < 25 and 84 < y <= 100) or \
                   (43 < x <= 54 and 84 < y <= 100):
                    in_zone = True
            if not in_zone:
                count += 1
    return count

def create_zone_preview(zone_name):
    """Erstellt eine kleine Spielfeld-Visualisierung mit der markierten Zone"""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(4, 6))
    ax.set_facecolor('#1a1a1a')
    ax.set_xlim(0, 68)
    ax.set_ylim(0, 100)
    
    # Spielfeldlinien
    ax.plot([0, 68], [50, 50], '#00ff88', linestyle="-", zorder=5, linewidth=1.5)
    mittelkreis = patches.Circle((34, 50), 9, edgecolor='#00ff88', facecolor='none', linewidth=1.5)
    ax.add_patch(mittelkreis)
    
    # Gestrichelte Linien
    ax.plot([43, 43], [100, 75], '#00ff88', linestyle="--", linewidth=1.5)
    ax.plot([25, 25], [100, 75], '#00ff88', linestyle="--", linewidth=1.5)
    ax.plot([43, 54, 54], [100, 84, 75], '#00ff88', linestyle="--", linewidth=1.5)
    ax.plot([25, 14, 14], [100, 84, 75], '#00ff88', linestyle="--", linewidth=1.5)
    ax.plot([14, 0], [90, 90], '#00ff88', linestyle="--", linewidth=1.5)
    ax.plot([54, 68], [90, 90], '#00ff88', linestyle="--", linewidth=1.5)
    
    # Fünfmeterraum
    fuenfmeter_oben = patches.Rectangle((25, 100), 18, -5, edgecolor='#00ff88', facecolor='none', linewidth=1.5)
    ax.add_patch(fuenfmeter_oben)
    
    # Sechzehnmeterraum
    sechzehn_oben = patches.Rectangle((14, 100), 40, -16, edgecolor='#00ff88', facecolor='none', linewidth=1.5)
    ax.add_patch(sechzehn_oben)
    
    # Markiere die ausgewählte Zone
    if zone_name == "Goldene Zone":
        zone_rect = patches.Rectangle((25, 84), 18, 16, edgecolor='#ffd700', facecolor='#ffd700', alpha=0.5, linewidth=2)
        ax.add_patch(zone_rect)
    elif zone_name == "Rote Zone":
        zone_rect = patches.Rectangle((25, 75), 18, 9, edgecolor='#ff4444', facecolor='#ff4444', alpha=0.5, linewidth=2)
        ax.add_patch(zone_rect)
    elif zone_name == "Zone 2":
        zone_rect = patches.Rectangle((14, 75), 11, 9, edgecolor='#ffaa00', facecolor='#ffaa00', alpha=0.5, linewidth=2)
        ax.add_patch(zone_rect)
    elif zone_name == "Zone 3":
        zone_rect = patches.Rectangle((43, 75), 11, 9, edgecolor='#ffaa00', facecolor='#ffaa00', alpha=0.5, linewidth=2)
        ax.add_patch(zone_rect)
    elif zone_name == "Zone 4":
        zone_rect = patches.Rectangle((0, 75), 14, 15, edgecolor='#ffaa00', facecolor='#ffaa00', alpha=0.5, linewidth=2)
        ax.add_patch(zone_rect)
    elif zone_name == "Zone 5":
        zone_rect = patches.Rectangle((54, 75), 14, 15, edgecolor='#ffaa00', facecolor='#ffaa00', alpha=0.5, linewidth=2)
        ax.add_patch(zone_rect)
    elif zone_name == "Zone 6":
        zone_rect = patches.Rectangle((14, 84), 11, 16, edgecolor='#ffaa00', facecolor='#ffaa00', alpha=0.5, linewidth=2)
        ax.add_patch(zone_rect)
    elif zone_name == "Zone 7":
        zone_rect = patches.Rectangle((43, 84), 11, 16, edgecolor='#ffaa00', facecolor='#ffaa00', alpha=0.5, linewidth=2)
        ax.add_patch(zone_rect)
    elif zone_name == "Restliches Spielfeld":
        # Markiere den Rest des Spielfelds (alles außerhalb der gestrichelten Zonen)
        # Zeichne einen Rahmen um den nicht markierten Bereich
        ax.add_patch(patches.Rectangle((0, 0), 68, 75, edgecolor='#888888', facecolor='#888888', alpha=0.3, linewidth=2))
        # Markiere auch Bereiche oberhalb y=90 außerhalb der Zonen
        ax.add_patch(patches.Rectangle((0, 90), 14, 10, edgecolor='#888888', facecolor='#888888', alpha=0.3, linewidth=2))
        ax.add_patch(patches.Rectangle((54, 90), 14, 10, edgecolor='#888888', facecolor='#888888', alpha=0.3, linewidth=2))
    
    ax.set_title(zone_name, fontsize=12, fontweight='bold', color='#00ff88', pad=10)
    ax.set_xticks([])
    ax.set_yticks([])
    
    plt.tight_layout()
    return fig

def create_zone_comparison_chart(teams_data, zone_name, goal_type):
    """Erstellt ein Balkendiagramm für den Vergleich der Teams in einer Zone"""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor('#1a1a1a')
    
    teams = list(teams_data.keys())
    goal_counts = []
    total_goals = []
    percentages = []
    
    goal_type_key = "eigene_tore" if goal_type == "Eigene Tore" else "gegentore"
    
    for team in teams:
        goals = teams_data[team][goal_type_key]["goals"]
        zone_goals = count_goals_in_zone(goals, zone_name)
        total = len(goals)
        percentage = (zone_goals / total * 100) if total > 0 else 0
        
        goal_counts.append(zone_goals)
        total_goals.append(total)
        percentages.append(percentage)
    
    # Erstelle Balkendiagramm - Farbe abhängig vom Tor-Typ
    bar_color = '#ff4444' if goal_type == "Gegentore" else '#00ff88'  # Rot für Gegentore, Grün für eigene Tore
    bars = ax.bar(teams, goal_counts, color=bar_color, alpha=0.8, edgecolor='#ffffff', linewidth=1.5)
    
    # Füge Prozentwerte über den Balken hinzu
    for i, (bar, count, total, pct) in enumerate(zip(bars, goal_counts, total_goals, percentages)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{count}\n({pct:.1f}%)',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='#ffffff')
    
    ax.set_xlabel('Teams', fontsize=12, color='#ffffff')
    ax.set_ylabel('Anzahl Tore', fontsize=12, color='#ffffff')
    ax.set_title(f'{zone_name} - {goal_type} Vergleich', fontsize=14, fontweight='bold', color='#00ff88', pad=20)
    ax.tick_params(colors='#ffffff')
    ax.grid(True, alpha=0.3, color='#00ff88')
    
    plt.tight_layout()
    return fig

def create_all_zones_overview_chart(teams_data, goal_type):
    """Erstellt ein Übersichtsdiagramm für alle Zonen aller Teams"""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_facecolor('#1a1a1a')
    
    teams = list(teams_data.keys())
    zones = ["Goldene Zone", "Rote Zone", "Zone 2", "Zone 3", "Zone 4", "Zone 5", "Zone 6", "Zone 7", "Restliches Spielfeld"]
    
    goal_type_key = "eigene_tore" if goal_type == "Eigene Tore" else "gegentore"
    
    # Berechne Daten für jede Zone
    zone_data = {}
    for zone in zones:
        zone_data[zone] = []
        for team in teams:
            goals = teams_data[team][goal_type_key]["goals"]
            zone_goals = count_goals_in_zone(goals, zone)
            total = len(goals)
            percentage = (zone_goals / total * 100) if total > 0 else 0
            zone_data[zone].append(percentage)
    
    # Erstelle gruppiertes Balkendiagramm
    x = np.arange(len(teams))
    width = 0.1
    colors = ['#ffd700', '#ff4444', '#ffaa00', '#ff8800', '#ff6600', '#ff4400', '#ff2200', '#ff0000', '#888888']
    
    for i, (zone, color) in enumerate(zip(zones, colors)):
        offset = (i - len(zones)/2) * width + width/2
        bars = ax.bar(x + offset, zone_data[zone], width, label=zone, color=color, alpha=0.8, edgecolor='#ffffff', linewidth=0.5)
    
    ax.set_xlabel('Teams', fontsize=12, color='#ffffff')
    ax.set_ylabel('Prozent (%)', fontsize=12, color='#ffffff')
    ax.set_title(f'Alle Zonen - {goal_type} Übersicht', fontsize=14, fontweight='bold', color='#00ff88', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(teams, color='#ffffff')
    ax.legend(loc='upper left', fontsize=8, framealpha=0.8)
    ax.tick_params(colors='#ffffff')
    ax.grid(True, alpha=0.3, color='#00ff88', axis='y')
    
    plt.tight_layout()
    return fig

def main():
    # Header mit ForzaRied Logo
    logo_path = "ForzaRied.png"
    if os.path.exists(logo_path):
        col1, col2 = st.columns([1, 4])
        with col1:
            st.image(logo_path, width=80)
        with col2:
            st.markdown('<h1 class="main-header">🟢⚫ AKA Teams Dashboard</h1>', unsafe_allow_html=True)
    else:
        st.markdown('<h1 class="main-header">🟢⚫ AKA Teams Dashboard</h1>', unsafe_allow_html=True)
    
    
    # Lade aktuelle Daten mit automatischer Datei-Erkennung
    file_modification_key = get_file_modification_times()
    current_teams_data = get_teams_data(file_modification_key)
    
    # Zeige Daten-Status
    if not current_teams_data:
        st.error("❌ Keine Team-Daten gefunden! Bitte überprüfen Sie den Pfad zu den Team-Dateien.")
        return
    
    # Sidebar für Auswahl
    
    # Ansichts-Auswahl ganz oben
    view_options = ["Spielfeld-Ansicht", "Zonen-Vergleich"]
    if "view_selection" not in st.session_state:
        st.session_state.view_selection = "Spielfeld-Ansicht"
    
    selected_view = st.sidebar.selectbox(
        "Ansicht auswählen:",
        view_options,
        index=view_options.index(st.session_state.view_selection) if st.session_state.view_selection in view_options else 0,
        key="view_selector"
    )
    st.session_state.view_selection = selected_view
    
    st.sidebar.markdown("---")
    
    # Zone-Auswahl (wird später am Ende der Sidebar angezeigt, aber hier initialisiert)
    zone_options = ["Goldene Zone", "Rote Zone"]
    if "zone_selection" not in st.session_state:
        st.session_state.zone_selection = "Goldene Zone"
    
    # Initialisiere Session State für persistente Auswahl
    if 'team1_selection' not in st.session_state:
        st.session_state.team1_selection = "Alle Teams"
    if 'goal_type1_selection' not in st.session_state:
        st.session_state.goal_type1_selection = "Eigene Tore"
    
    # Erste Auswahl
    team_options = ["Alle Teams"] + list(current_teams_data.keys())
    goal_options = ["Eigene Tore", "Gegentore"]
    
    # Sichere Index-Bestimmung für Team 1
    try:
        team1_index = team_options.index(st.session_state.team1_selection)
    except ValueError:
        team1_index = 0  # Fallback zu "Alle Teams"
        st.session_state.team1_selection = "Alle Teams"
    
    # Sichere Index-Bestimmung für Goal Type 1
    try:
        goal_type1_index = goal_options.index(st.session_state.goal_type1_selection)
    except ValueError:
        goal_type1_index = 0  # Fallback zu "Eigene Tore"
        st.session_state.goal_type1_selection = "Eigene Tore"
    
    team1 = st.sidebar.selectbox(
        "Team 1:",
        options=team_options,
        index=team1_index,
        key="team1"
    )
    
    goal_type1 = st.sidebar.selectbox(
        "Tor-Typ:",
        options=goal_options,
        index=goal_type1_index,
        key="goal_type1"
    )
    
    # Aktualisiere Session State
    st.session_state.team1_selection = team1
    st.session_state.goal_type1_selection = goal_type1
    
    # Automatische Team 2 Auswahl basierend auf Team 1
    # Team 2 soll immer das gleiche Team wie Team 1 sein
    default_team2 = team1
    
    # Automatische Tor-Typ Auswahl für Team 2
    if goal_type1 == "Eigene Tore":
        # Wenn Team 1 "Eigene Tore" hat, wähle "Gegentore" für Team 2
        default_goal_type2 = "Gegentore"
    else:
        # Wenn Team 1 "Gegentore" hat, wähle "Eigene Tore" für Team 2
        default_goal_type2 = "Eigene Tore"
    
    # Team 2 wird immer automatisch basierend auf Team 1 gesetzt
    # Ignoriere Session State für Team 2, da es sich automatisch anpassen soll
    team2_index = team_options.index(default_team2)
    goal_type2_index = goal_options.index(default_goal_type2)
    
    # Aktualisiere Session State für Team 2 mit den automatischen Werten
    st.session_state.team2_selection = default_team2
    st.session_state.goal_type2_selection = default_goal_type2
    
    # Zweite Auswahl
    team2 = st.sidebar.selectbox(
        "Team 2:",
        options=team_options,
        index=team2_index,
        key="team2"
    )
    
    goal_type2 = st.sidebar.selectbox(
        "Tor-Typ:",
        options=goal_options,
        index=goal_type2_index,
        key="goal_type2"
    )
    
    # Validierung: Verhindere identische Teams mit gleichen Tor-Typen
    if team1 == team2 and goal_type1 == goal_type2:
        # Nur wenn beide Teams identisch sind UND den gleichen Tor-Typ haben, ändere Team 2 automatisch
        if goal_type1 == "Eigene Tore":
            goal_type2 = "Gegentore"
        else:
            goal_type2 = "Eigene Tore"
        
        # Aktualisiere die Auswahl
        goal_type2_index = goal_options.index(goal_type2)
        st.session_state.goal_type2_selection = goal_type2
    
    # Aktualisiere Session State für Team 2
    st.session_state.team2_selection = team2
    st.session_state.goal_type2_selection = goal_type2
    
    # Goldene Zone Berechnung und Anzeige basierend auf Team-Auswahl
    def count_goals_in_golden_zone(goals):
        """Zählt Tore in der goldenen Zone (x: 25-43, y: 84-100)"""
        golden_zone_goals = 0
        for goal in goals:
            x, y = goal
            if 25 <= x <= 43 and 84 <= y <= 100:
                golden_zone_goals += 1
        return golden_zone_goals
    
    def count_assists_in_red_zone(assists):
        """Zählt Assists in der roten Zone (x: 25-43, y: 75-84)"""
        red_zone_assists = 0
        for assist in assists:
            x, y = assist
            if 25 <= x <= 43 and 75 <= y <= 84:
                red_zone_assists += 1
        return red_zone_assists
    
    # Berechne Goldene Zone und Rote Zone Daten für das ausgewählte Team
    if team1 == "Alle Teams":
        # Für "Alle Teams" sammle alle Tore und Assists aller Teams
        all_eigene_goals = []
        all_gegentore_goals = []
        all_eigene_assists = []
        all_gegentore_assists = []
        for team in current_teams_data.keys():
            all_eigene_goals.extend(current_teams_data[team]["eigene_tore"]["goals"])
            all_gegentore_goals.extend(current_teams_data[team]["gegentore"]["goals"])
            all_eigene_assists.extend(current_teams_data[team]["eigene_tore"]["assists"])
            all_gegentore_assists.extend(current_teams_data[team]["gegentore"]["assists"])
        
        team_eigene_golden = count_goals_in_golden_zone(all_eigene_goals)
        team_gegentore_golden = count_goals_in_golden_zone(all_gegentore_goals)
        team_eigene_total = len(all_eigene_goals)
        team_gegentore_total = len(all_gegentore_goals)
        
        # Rote Zone Assists
        team_eigene_red = count_assists_in_red_zone(all_eigene_assists)
        team_gegentore_red = count_assists_in_red_zone(all_gegentore_assists)
        team_eigene_assists_total = len(all_eigene_assists)
        team_gegentore_assists_total = len(all_gegentore_assists)
        team_name = "Alle Teams"
    else:
        # Für einzelnes Team
        team_eigene_data = current_teams_data[team1]["eigene_tore"]
        team_gegentore_data = current_teams_data[team1]["gegentore"]
        
        team_eigene_golden = count_goals_in_golden_zone(team_eigene_data["goals"])
        team_gegentore_golden = count_goals_in_golden_zone(team_gegentore_data["goals"])
        team_eigene_total = len(team_eigene_data["goals"])
        team_gegentore_total = len(team_gegentore_data["goals"])
        
        # Rote Zone Assists
        team_eigene_red = count_assists_in_red_zone(team_eigene_data["assists"])
        team_gegentore_red = count_assists_in_red_zone(team_gegentore_data["assists"])
        team_eigene_assists_total = len(team_eigene_data["assists"])
        team_gegentore_assists_total = len(team_gegentore_data["assists"])
        team_name = team1
    
    # Berechne Prozentsätze für Goldene Zone
    team_eigene_percent = (team_eigene_golden / team_eigene_total * 100) if team_eigene_total > 0 else 0
    team_gegentore_percent = (team_gegentore_golden / team_gegentore_total * 100) if team_gegentore_total > 0 else 0
    
    # Berechne Prozentsätze für Rote Zone
    team_eigene_red_percent = (team_eigene_red / team_eigene_assists_total * 100) if team_eigene_assists_total > 0 else 0
    team_gegentore_red_percent = (team_gegentore_red / team_gegentore_assists_total * 100) if team_gegentore_assists_total > 0 else 0
    
    # Konvertiere Anzeige-Text zurück zu internen Werten
    goal_type1_internal = "eigene_tore" if goal_type1 == "Eigene Tore" else "gegentore"
    goal_type2_internal = "eigene_tore" if goal_type2 == "Eigene Tore" else "gegentore"
    
    # Zone-Auswahl (für Berechnung)
    selected_zone = zone_options[zone_options.index(st.session_state.zone_selection)] if st.session_state.zone_selection in zone_options else "Goldene Zone"
    
    def get_team_data(team_name, goal_type_internal):
        """Hilfsfunktion um Team-Daten zu holen, auch für 'Alle Teams'"""
        if team_name == "Alle Teams":
            # Sammle alle Daten aller Teams für den gewählten Tor-Typ
            all_goals = []
            all_assists = []
            for team in current_teams_data.keys():
                all_goals.extend(current_teams_data[team][goal_type_internal]["goals"])
                all_assists.extend(current_teams_data[team][goal_type_internal]["assists"])
            return {"goals": all_goals, "assists": all_assists}
        else:
            return current_teams_data[team_name][goal_type_internal]
    
    # Vergleichsdaten laden
    if team1 == "Alle Teams":
        # Sammle alle Tore aller Teams für den gewählten Tor-Typ
        all_goals1 = []
        for team in current_teams_data.keys():
            all_goals1.extend(current_teams_data[team][goal_type1_internal]["goals"])
        data1 = {"goals": all_goals1}
    else:
        data1 = current_teams_data[team1][goal_type1_internal]
    
    if team2 == "Alle Teams":
        # Sammle alle Tore aller Teams für den gewählten Tor-Typ
        all_goals2 = []
        for team in current_teams_data.keys():
            all_goals2.extend(current_teams_data[team][goal_type2_internal]["goals"])
        data2 = {"goals": all_goals2}
    else:
        data2 = current_teams_data[team2][goal_type2_internal]
    
    goals1_count = len(data1["goals"])
    goals2_count = len(data2["goals"])
    
    # Vergleich anzeigen mit zusätzlichen Informationen direkt darunter
    # Team 1
    st.sidebar.markdown(f"**{team1} {goal_type1}:** {goals1_count}")
    if team1 != "Alle Teams":
        # Sichere Extraktion der zusätzlichen Informationen für Team 1
        team1_eigene_info = current_teams_data[team1]["eigene_tore"].get("additional_info", "")
        team1_gegentore_info = current_teams_data[team1]["gegentore"].get("additional_info", "")
        
        # Zeige zusätzliche Informationen für Team 1 basierend auf dem Tor-Typ
        if goal_type1 == "Eigene Tore" and team1_eigene_info:
            st.sidebar.markdown(f"{team1_eigene_info}")
        elif goal_type1 == "Gegentore" and team1_gegentore_info:
            st.sidebar.markdown(f"{team1_gegentore_info}")
    
    # Team 2
    st.sidebar.markdown(f"**{team2} {goal_type2}:** {goals2_count}")
    if team2 != "Alle Teams":
        # Sichere Extraktion der zusätzlichen Informationen für Team 2
        team2_eigene_info = current_teams_data[team2]["eigene_tore"].get("additional_info", "")
        team2_gegentore_info = current_teams_data[team2]["gegentore"].get("additional_info", "")
        
        # Zeige zusätzliche Informationen für Team 2 basierend auf dem Tor-Typ
        if goal_type2 == "Eigene Tore" and team2_eigene_info:
            st.sidebar.markdown(f"{team2_eigene_info}")
        elif goal_type2 == "Gegentore" and team2_gegentore_info:
            st.sidebar.markdown(f"{team2_gegentore_info}")
    else:
        # Für "Alle Teams" sammle und kumuliere alle zusätzlichen Informationen
        all_eigene_infos = []
        all_gegentore_infos = []
        
        for team in current_teams_data.keys():
            eigene_info = current_teams_data[team]["eigene_tore"].get("additional_info", "")
            gegentore_info = current_teams_data[team]["gegentore"].get("additional_info", "")
            
            if eigene_info:
                all_eigene_infos.append(eigene_info)
            if gegentore_info:
                all_gegentore_infos.append(gegentore_info)
        
        # Kumulierte Anzeige für Eigene Tore (nur wenn vorhanden)
        if all_eigene_infos:
            st.sidebar.markdown(f"**Eigene Tore:** Alle Teams - {' '.join(all_eigene_infos)}")
        
        # Kumulierte Anzeige für Gegentore (nur wenn vorhanden)
        if all_gegentore_infos:
            st.sidebar.markdown(f"**Gegentore:** Alle Teams - {' '.join(all_gegentore_infos)}")
    
    # Zone-Auswahl und Beschriftung nur bei Spielfeld-Ansicht anzeigen
    selected_zone = zone_options[zone_options.index(st.session_state.zone_selection)] if st.session_state.zone_selection in zone_options else "Goldene Zone"
    zone_placeholder = st.sidebar.empty()
    
    if selected_view == "Spielfeld-Ansicht":
        # Zusätzlicher Abstand
        st.sidebar.markdown("")
        st.sidebar.markdown("---")
        st.sidebar.markdown("")
        
        # Zone-Auswahl (ganz unten im Menü)
        selected_zone = st.sidebar.selectbox(
            "Zone auswählen:",
            zone_options,
            index=zone_options.index(st.session_state.zone_selection) if st.session_state.zone_selection in zone_options else 0,
            key="zone_selector"
        )
        
        # Aktualisiere Session State
        st.session_state.zone_selection = selected_zone
        
        # Dynamischer Zone Header
        if selected_zone == "Goldene Zone":
            st.sidebar.markdown("### 🏆 Goldene Zone")
        else:
            st.sidebar.markdown("### 🔴 Rote Zone")
        
        # Platzhalter für Zone Daten (wird direkt danach aktualisiert)
        zone_placeholder = st.sidebar.empty()
        
        # Aktualisiere Zone Daten basierend auf Auswahl (erneut berechnen mit aktualisiertem selected_zone)
    if selected_zone == "Goldene Zone":
        # Goldene Zone - zeige Daten der beiden ausgewählten Teams
        # Hole Daten für Team 1
        team1_data = get_team_data(team1, goal_type1_internal)
        team1_golden_goals = count_goals_in_golden_zone(team1_data["goals"])
        team1_total_goals = len(team1_data["goals"])
        team1_golden_percent = (team1_golden_goals / team1_total_goals * 100) if team1_total_goals > 0 else 0
        
        # Hole Daten für Team 2
        team2_data = get_team_data(team2, goal_type2_internal)
        team2_golden_goals = count_goals_in_golden_zone(team2_data["goals"])
        team2_total_goals = len(team2_data["goals"])
        team2_golden_percent = (team2_golden_goals / team2_total_goals * 100) if team2_total_goals > 0 else 0
        
        zone_text = f"**{team1} {goal_type1}:**\n"
        zone_text += f"{team1_golden_goals} Tore von {team1_total_goals} Toren ({team1_golden_percent:.1f}%)\n\n"
        zone_text += f"**{team2} {goal_type2}:**\n"
        zone_text += f"{team2_golden_goals} Tore von {team2_total_goals} Toren ({team2_golden_percent:.1f}%)"
    else:  # Rote Zone - zeige Daten der beiden ausgewählten Teams
        # Hole Daten für Team 1
        team1_data = get_team_data(team1, goal_type1_internal)
        team1_red_assists = count_assists_in_red_zone(team1_data["assists"])
        team1_total_assists = len(team1_data["assists"])
        team1_red_percent = (team1_red_assists / team1_total_assists * 100) if team1_total_assists > 0 else 0
        
        # Hole Daten für Team 2
        team2_data = get_team_data(team2, goal_type2_internal)
        team2_red_assists = count_assists_in_red_zone(team2_data["assists"])
        team2_total_assists = len(team2_data["assists"])
        team2_red_percent = (team2_red_assists / team2_total_assists * 100) if team2_total_assists > 0 else 0
        
        zone_text = f"**{team1} {goal_type1}:**\n"
        zone_text += f"{team1_red_assists} Assists von {team1_total_assists} Assists ({team1_red_percent:.1f}%)\n\n"
        zone_text += f"**{team2} {goal_type2}:**\n"
        zone_text += f"{team2_red_assists} Assists von {team2_total_assists} Assists ({team2_red_percent:.1f}%)"
    
    # Zone-Daten nur bei Spielfeld-Ansicht anzeigen
    if selected_view == "Spielfeld-Ansicht":
        zone_placeholder.markdown(zone_text)
    
    # Hauptinhalt basierend auf ausgewählter Ansicht
    if selected_view == "Spielfeld-Ansicht":
        # Spielfelder basierend auf Team-Vergleich
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"### {team1} - {goal_type1}")
            if team1 == "Alle Teams":
                # Zeige alle Tore aller Teams auf einem Spielfeld
                fig1 = draw_all_teams_field(goal_type1_internal, current_teams_data)
            else:
                fig1 = draw_field(team1, goal_type1_internal, current_teams_data)
            st.pyplot(fig1, use_container_width=True)
        
        with col2:
            st.markdown(f"### {team2} - {goal_type2}")
            if team2 == "Alle Teams":
                # Zeige alle Tore aller Teams auf einem Spielfeld
                fig2 = draw_all_teams_field(goal_type2_internal, current_teams_data)
            else:
                fig2 = draw_field(team2, goal_type2_internal, current_teams_data)
            st.pyplot(fig2, use_container_width=True)
    
    elif selected_view == "Zonen-Vergleich":
        # Zone-Auswahl für Diagramm
        zone_names = ["Goldene Zone", "Rote Zone", "Zone 2", "Zone 3", "Zone 4", "Zone 5", "Zone 6", "Zone 7", "Restliches Spielfeld"]
        selected_zone_for_chart = st.selectbox(
            "Zone für Vergleich auswählen:",
            zone_names,
            key="zone_chart_selector"
        )
        
        # Tor-Typ Auswahl für Diagramm
        goal_type_for_chart = st.selectbox(
            "Tor-Typ für Vergleich:",
            ["Eigene Tore", "Gegentore"],
            key="goal_type_chart_selector"
        )
        
        # Zeige kleine Spielfeld-Grafik mit markierter Zone
        col_preview, col_chart = st.columns([1, 2])
        
        with col_preview:
            st.markdown("### Zone-Vorschau")
            zone_preview_fig = create_zone_preview(selected_zone_for_chart)
            st.pyplot(zone_preview_fig, use_container_width=True)
        
        with col_chart:
            # Erstelle und zeige Diagramm
            chart_fig = create_zone_comparison_chart(current_teams_data, selected_zone_for_chart, goal_type_for_chart)
            st.pyplot(chart_fig, use_container_width=True)
    
    # Footer
    st.markdown("---")

if __name__ == "__main__":
    main()
