import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg
import os
from pathlib import Path

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

# Datenstrukturen für alle Teams
TEAMS_DATA = {
    "U15": {
        "eigene_tore": {
            "goals": [(34,89),(42,95)],
            "assists": [(17,100),(52,48)],
            "title": "U15 - Eigene Tore"
        },
        "gegentore": {
            "goals": [(28,95),(34,92),(43,96)],
            "assists": [(34,84),(39,82),(39,83)],
            "title": "U15 - Gegentore"
        }
    },
    "U16": {
        "eigene_tore": {
            "goals": [],
            "assists": [],
            "title": "U16 - Eigene Tore"
        },
        "gegentore": {
            "goals": [(40,90),(38,96),(31,94),(34,83)],
            "assists": [(65,97),(66,76),(64,88),(52,70)],
            "title": "U16 - Gegentore"
        }
    },
    "U18": {
        "eigene_tore": {
            "goals": [],
            "assists": [],
            "title": "U18 - Eigene Tore"
        },
        "gegentore": {
            "goals": [(27,88),(32,93),(37,95)],
            "assists": [(38,81),(28,3),(12,86)],
            "title": "U18 - Gegentore\n 2 Elfmeter n.b."
        }
    }
}

def draw_field(team, goal_type):
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

    # Elfmeterpunkte hinzufügen
    ax.scatter(34, 89, color='#00ff88', marker='o')  # Elfmeterpunkt oben
    ax.scatter(34, 11, color='#00ff88', marker='o')  # Elfmeterpunkt unten

    # Halbkreise um die Elfmeterpunkte
    halbkreis_oben = patches.Arc((34, 89), 18, 18, angle=0, theta1=215, theta2=325, edgecolor='#00ff88', linewidth=2)
    ax.add_patch(halbkreis_oben)

    halbkreis_unten = patches.Arc((34, 11), 18, 18, angle=0, theta1=35, theta2=145, edgecolor='#00ff88', linewidth=2)
    ax.add_patch(halbkreis_unten)

    # Daten für das ausgewählte Team und Tor-Typ abrufen
    team_data = TEAMS_DATA[team][goal_type]
    goals = team_data["goals"]
    assists = team_data["assists"]
    title = team_data["title"]

    # Tore markieren (rote Kreise)
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

    # Legende
    ax.legend(loc="lower left", fontsize=10, framealpha=0.8)

    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.xlabel("Spielfeldbreite (m)", fontsize=12)
    plt.ylabel("Spielfeldtiefe (m)", fontsize=12)
    
    # Achsenbeschriftungen entfernen für sauberes Aussehen
    ax.set_xticks([])
    ax.set_yticks([])
    
    return fig

def main():
    # Header
    st.markdown('<h1 class="main-header">⚽ AKA Teams Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar für Auswahl
    # ForzaRied Logo einfügen
    logo_path = "C:\\Users\\demmelb-ma\\OneDrive\\AKA\\ForzaRied.png"
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=200)
    else:
        st.sidebar.header("📊 Team & Statistik Auswahl")
    
    # Team-Auswahl
    selected_team = st.sidebar.selectbox(
        "🏆 Team auswählen:",
        options=list(TEAMS_DATA.keys()),
        index=0
    )
    
    # Statistik-Typ Auswahl entfernt - beide werden immer angezeigt
    
    # Zusätzliche Informationen in der Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Team Statistiken")
    
    # Alle Teams: Statistiken für beide Tor-Typen anzeigen
    eigene_data = TEAMS_DATA[selected_team]["eigene_tore"]
    gegentore_data = TEAMS_DATA[selected_team]["gegentore"]
    
    st.sidebar.markdown("**Eigene Tore:**")
    st.sidebar.metric("Tore", len(eigene_data["goals"]))
    
    st.sidebar.markdown("**Gegentore:**")
    st.sidebar.metric("Tore", len(gegentore_data["goals"]))
    
    # Hauptinhalt - Alle Teams: Beide Spielfelder nebeneinander anzeigen
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### {selected_team} - Eigene Tore")
        fig_eigene = draw_field(selected_team, "eigene_tore")
        st.pyplot(fig_eigene, use_container_width=True)
    
    with col2:
        st.markdown(f"### {selected_team} - Gegentore")
        fig_gegentore = draw_field(selected_team, "gegentore")
        st.pyplot(fig_gegentore, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        AKA Teams Dashboard - Fußball-Statistiken
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
