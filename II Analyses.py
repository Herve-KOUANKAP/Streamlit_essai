import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd
from shapely.geometry import Point
#from streamlit_html_exporter import StreamlitHTMLExporter
#import cartiflette.s3 as s3


st.title("Analyse des bases de données")

st.markdown("## 1. Analyse de la base Caractéristique")

## Lecture de la base
caracts = pd.read_csv("caract.csv", delimiter=";")

## Labelisation des colonnes
for var in caracts.columns:
    try : 
        labels = pd.read_excel("descriptif_variables.xlsx", sheet_name=var, header=None)
        label_dict = dict(zip(labels[0], labels[1]))
        caracts[var] = caracts[var].replace(label_dict)
    except :
        pass

## Variable "lum"
##Suppression des lignes avec valeur manquante ()

caracts = caracts[~caracts["lum"].isin([-1])]
caracts = caracts[~caracts["int"].isin([-1])]
caracts = caracts[~caracts["atm"].isin([" Non renseigné"])]
caracts = caracts[~caracts["col"].isin([" Non renseigné"])]

caracts["long"] = caracts["long"].str.replace(",", ".").astype(float)
caracts["lat"] = caracts["lat"].str.replace(",", ".").astype(float)

st.markdown("**L’analyse de cette base de données permet de mieux comprendre les circonstances et la fréquence des préjudices corporels résultant d’accidents de la circulation.**")

# Afficher la base caractéristique
st.dataframe(caracts.head())

st.markdown("### 1.1. Analyse de la fréquence d'accidents en fonction de la luminosité")

lum_counts = caracts["lum"].value_counts().reset_index()
lum_counts.columns = ["Lumière", "Nombre"]

# Création du diagramme en camembert
fig1 = px.pie(
    lum_counts, 
    names='Lumière',   
    values="Nombre",
    title="Répartition des accidents avec dommages corporels selon la luminosité",   
    hole=0.7
)

# Personnalisation du layout
fig1.update_layout(
    title_x=0.5,  # Centre le titre horizontalement
    title_y=0.95, # Ajuste la position verticale du titre si nécessaire
    title_font=dict(size=20, family="Arial", color="black"),  # Style du titre
    plot_bgcolor="white",  # Fond blanc pour le graphique
    paper_bgcolor="white",  # Fond du papier (autour du graphique)
    margin=dict(t=50, b=50, l=50, r=50),  # Ajoute des marges autour du graphique pour mieux définir le cadre
    showlegend=True,  # Afficher la légende
    legend=dict(
        x=1.05,  # Positionne la légende à droite du graphique (au-delà du côté droit)
        y=0.5,   # Centre la légende verticalement (à 50% de la hauteur)
        xanchor='left',  # Ancre la légende à la gauche de sa position
        yanchor='middle',  # Ancre la légende au milieu de la position verticale
        bgcolor='white',  # Fond de la légende blanc
        bordercolor='black',  # Bordure noire autour de la légende
        borderwidth=1  # Largeur de la bordure de la légende
    )
)

# Affichage du graphique
st.plotly_chart(fig1)

# commentaire
st.markdown("""
- La majorité des accidents de circulation entraînant des dommages corporels se produisent en plein jour.
- Cela pourrait s'expliquer par une intensité de trafic plus élevée durant la journée, en raison des trajets domicile-travail, des livraisons et des activités personnelles.
""")

st.markdown("### 1.2. Analyse de la fréquence d'accidents en fonction de la situation géographique")


# Fonction pour créer le graphique en camembert
def create_pie_chart(data, names_col, values_col, title):
    chart = px.pie(
        data, 
        names=names_col,   
        values=values_col,    
        title=title,
        hole=0.7
    )
    chart.update_layout(
        title_x=0.5,  
        title_y=0.95, 
        title_font=dict(size=20, family="Arial", color="black"),  
        plot_bgcolor="white",  
        paper_bgcolor="white",  
        margin=dict(t=50, b=50, l=50, r=50),  
        showlegend=True,  
        legend=dict(
            x=1.05,  
            y=0.5,   
            xanchor='left',  
            yanchor='middle',  
            bgcolor='white',  
            bordercolor='black',  
            borderwidth=1  
        )
    )
    return chart

# Fonction pour créer le graphique en barre
def create_bar_chart(data, x_col, y_col, title):
    chart = px.bar(
        data,
        x=x_col,     
        y=y_col,  
        title=title,
        orientation="h"  
    )
    chart.update_layout(
        title_x=0.5,  
        title_y=0.95, 
        title_font=dict(size=20, family="Arial", color="black"),  
        plot_bgcolor="white",  
        paper_bgcolor="white",  
        margin=dict(t=50, b=50, l=50, r=50),  
        showlegend=True,  
        legend=dict(
            x=1.05,  
            y=0.5,   
            xanchor='left',  
            yanchor='middle',  
            bgcolor='white',  
            bordercolor='black',  
            borderwidth=1  
        )
    )
    return chart

# Sélecteur pour choisir le graphique à afficher
#st.markdown("**Choisissez le grapique à afficher")
chart_option = st.selectbox(
    "Choisissez un graphique à afficher:",
    ["Répartition des accidents par localisation", 
     "Accidents par type d'intersection", 
     "Accidents par conditions atmosphériques", 
     "Accidents par luminosité et conditions atmosphériques", 
     "Accidents par type de collision"]
)

# Création des différents graphiques
if chart_option == "Répartition des accidents par localisation":
    agg_counts = caracts["agg"].value_counts().reset_index()
    agg_counts.columns = ["Localisation", "Nombre"] 
    fig = create_pie_chart(agg_counts, "Localisation", "Nombre", "Répartition des accidents avec dommages corporels selon la localisation")
    st.plotly_chart(fig)

elif chart_option == "Accidents par type d'intersection":
    int_counts = caracts["int"].value_counts().reset_index()
    int_counts.columns = ["Intersection", "Nombre"]
    int_counts = int_counts.sort_values(by="Nombre", ascending=True)
    fig = create_bar_chart(int_counts, "Nombre", "Intersection", "Nombre d'accidents avec dommages corporels en fonction du type d'intersection")
    st.plotly_chart(fig)

elif chart_option == "Accidents par conditions atmosphériques":
    atm_counts = caracts["atm"].value_counts().reset_index()
    atm_counts.columns = ["Conditions atmosphériques", "Nombre"]
    atm_counts = atm_counts.sort_values(by="Nombre", ascending=True)
    fig = create_bar_chart(atm_counts, "Nombre", "Conditions atmosphériques", "Nombre d'accidents de la circulation avec dommages corporels en fonction des conditions atmosphériques")
    st.plotly_chart(fig)

elif chart_option == "Accidents par luminosité et conditions atmosphériques":
    atm_lum_counts = caracts[["atm", "lum"]].value_counts().reset_index()
    atm_lum_counts.columns = ["Luminosité", "Conditions atmosphériques", "Nombre"]
    fig = px.scatter(
        atm_lum_counts,
        x="Luminosité",                     
        y="Conditions atmosphériques",              
        size="Nombre",            
        color="Nombre",                 
        title="Nombre d'accidents avec dégâts corporels en fonction de la luminosité et des conditions météorologiques",
        labels={"Luminosité": "Luminosité", "Conditions atmosphériques": "Conditions atmosphériques"}
    )
    fig.update_traces(textposition='top center')
    fig.update_layout(
        xaxis=dict(title="Luminosité", gridcolor='lightgrey'),
        yaxis=dict(title="Conditions météorologiques", gridcolor='lightgrey'),
        plot_bgcolor="white"
    )
    st.plotly_chart(fig)

elif chart_option == "Accidents par type de collision":
    col_counts = caracts["col"].value_counts().reset_index()
    col_counts.columns = ["Collision", "Nombre"]
    col_counts = col_counts.sort_values(by="Nombre", ascending=True)
    fig = create_bar_chart(col_counts, "Nombre", "Collision", "Nombre d'accidents de la circulation avec dommages corporels en fonction du type de collision")
    st.plotly_chart(fig)

st.markdown("### 1.3. Analyse saisonnière")

mois_counts = caracts["mois"].value_counts().reset_index()
mois_counts.columns = ["mois", "Nombre"]
mois_counts = mois_counts.sort_values(by="Nombre", ascending=True)

mois_counts["mois"] = pd.Categorical(
    mois_counts["mois"],
    categories=["janvier", "février", "mars", "avril", "mai", "juin", 
                "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
    ordered=True
)

#mois_counts = mois_counts.sort_values(by="mois")

# Création du graphique
fig2 = px.bar(
    mois_counts,
    x="mois",     
    y="Nombre",   # Colonne contenant les catégories
    title="Nombre d'accidents de la circulation avec dommages corporels par mois",  # Titre du graphique
    orientation="v"  # Barres verticales
)

# Personnalisation du layout
fig2.update_layout(
    title_x=0.5,  # Centre le titre horizontalement
    title_y=0.95, # Ajuste la position verticale du titre si nécessaire
    title_font=dict(size=20, family="Arial", color="black"),  # Style du titre
    plot_bgcolor="white",  # Fond blanc pour le graphique
    paper_bgcolor="white",  # Fond du papier (autour du graphique)
    margin=dict(t=50, b=50, l=50, r=50),  # Ajoute des marges autour du graphique pour mieux définir le cadre
    showlegend=True,  # Afficher la légende
    legend=dict(
        x=1.05,  # Positionne la légende à droite du graphique (au-delà du côté droit)
        y=0.5,   # Centre la légende verticalement (à 50% de la hauteur)
        xanchor='left',  # Ancre la légende à la gauche de sa position
        yanchor='middle',  # Ancre la légende au milieu de la position verticale
        bgcolor='white',  # Fond de la légende blanc
        bordercolor='black',  # Bordure noire autour de la légende
        borderwidth=1  # Largeur de la bordure de la légende
    )
)

st.plotly_chart(fig2)

