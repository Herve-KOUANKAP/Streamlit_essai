# Importation de la librairie
import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Multipage App"
)

st.title("Analyse des accidents corporels de la circulation routière")
st.sidebar.success("Select a page above.")
#st.markdown("# Titre principal avec Markdown")
st.markdown("#### Challenge Data Visualisation en Actuariat 2024")
st.markdown("##### ENSAE'STAT")

st.header("Introduction")
st.markdown("Dans le domaine de l'asurance automobile, l'évaluation des risques repose non seulement sur la fréquence des sinistres, mais aussi sur leur gravité, \
c'est-à-dire des dommages causés. En utilisant les données des accidents corporels de la route, en particulier la variable de gravité des accidents, il est possible \
 de mieux comprendre les différents niveaux de risques auxquels un assureur peut être confronté. L’objectif est de mettre en lumière des patterns spécifiques qui permettent \
d’optimiser les offres d’assurance en fonction de la probabilité d’un sinistre et de la sévérité des conséquences, afin d’offrir une couverture plus adaptée et de réduire les \
coûts liés aux indemnités. ")
st.markdown("Pour notre cette étude nous disposons de quatre (04) bases de données annueldisponibles et accessibles sur le site https://data.gouv.fr : \
Caractéristiques, Lieux, Véhicules et Usagers. Nous nous focaliserons sur les données de l'année 2023.")



# Importation des bases
caracts = pd.read_csv("caract.csv", delimiter=";")
lieux = pd.read_csv("lieux.csv", delimiter=";")
usagers = pd.read_csv("usagers.csv", delimiter=";")
vehicules = pd.read_csv("vehicules.csv", delimiter=";")

# Labélisation des colonnes

bases = [caracts, lieux, usagers, vehicules]
for base in bases :
    for var in base.columns:
        try :
            labels = pd.read_excel("descriptif_variables.xlsx", sheet_name=var, header=None)
            label_dict = dict(zip(labels[0], labels[1]))
            base[var] = base[var].replace(label_dict)
        except :
            pass

# Afficher la base usagers
#st.dataframe(usagers.head())


