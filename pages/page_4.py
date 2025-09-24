import streamlit as st
import pandas as pd
import plotly.express as px

import geopandas as gpd
from shapely import wkt
import folium

from utilities import *

st.title("Carte interactive par département")

# ------------------------------
# Fonctions
# ------------------------------

@st.cache_data
def load_data_geopandas(url):
    """Fonction qui transforme les données brutes en format GeoPandas."""
    df = pd.read_csv("processed/data/pop_iso_communes_final.csv", engine="python")
    df['geometry'] = df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, crs='epsg:4326')
    return gdf

def create_button(nom, mapping, default=0):
    """Fonction créant un bouton d'interface streamlit."""
    try:
        create_button.counter += 1
    except AttributeError:
        create_button.counter = 1

    bouton = st.segmented_control(
        nom,
        options=mapping.keys(),
        format_func=lambda option: mapping[option],
        selection_mode="single",
        key=create_button.counter,
        default=default,
    )

    return bouton


# ------------------------------
# Présentation des données
# ------------------------------

# Boutons
selection_commerce = create_button("Type de commerce", commerce_map_bouton)
selection_transport = create_button("Type de transport", transport_map_bouton)
selection_temps = create_button("Intervalle de temps (minutes)", temps_map_bouton)

commerce = commerce_map[selection_commerce]
transport = transport_map[selection_transport]
temps = str((selection_temps + 1)*300)

# Chargement des données
gdf = load_data_geopandas("processed/data/pop_iso_communes_final.csv")

options = st.selectbox(
    "Barre de recherche",
    gdf["Nom_departement"].unique(),
    placeholder="Sélectionnez un département...",
)

# Affichage des données
column_select = commerce + "_" + transport + "_" + temps

gdf = gdf[gdf["Nom_departement"] == options]

moyenne = round((gdf[column_select].sum()/gdf["population"].sum())*100, 2)
gdf["pourcentage"] = round((gdf[column_select] / gdf["population"])*100, 2)

gdf = gdf.loc[:, ["geometry", "Nom_commune", "population_2022", "pourcentage"]]
gdf = gdf.rename(columns={"Nom_commune":"commune"})


commerce_legend = commerce_map_legend[selection_commerce]
transport_legend = transport_map_legend[selection_transport]
temps_legend = temps_map_bouton[selection_temps]

titre = f"Part de la population habitant à {temps_legend} minutes ou moins " \
        f"d'{commerce_legend} {transport_legend}"
st.markdown(f"**{titre}**")
st.markdown(f"Moyenne du département : {moyenne}%")


carte = gdf.explore(column="pourcentage", 
                    style_kwds={"fillOpacity":0.75},
                    highlight_kwds={"fillOpacity":0.5},
                    legend_kwds={"max_labels":4},
                    min_zoom=5,
                    max_zoom=15,
                    cmap='Spectral',
                    vmin=0,
                    vmax=100,
                    )
st.components.v1.html(folium.Figure().add_child(carte).render(), height=480, width=800)