import streamlit as st
import pandas as pd
import plotly.express as px

import geopandas as gpd
from shapely import wkt
import folium

st.title("Carte interactive par département")

commerce_map = {
    0: "bakery",
    1: "supermarket",
    2: "convenience",
    3: "post-office",
    4: "pharmacy",
}
commerce_map_bouton = {
    0: "🥖 Boulangeries",
    1: "🛒 Supermarchés",
    2: "🏪 Supérettes",
    3: "📮 Bureaux de poste",
    4: "💊 Pharmacies",
}
transport_map = {
    0: "driving-car",
    1: "cycling-electric",
    2: "cycling-regular",
}
transport_map_bouton = {
    0: "🚗 Voiture",
    1: "🔋Vélo électrique ",
    2: "🚲 Vélo",
}
temps_map_bouton = {
    0: "5",
    1: "10",
    2: "15",
    3: "20",
    4: "25",
    5: "30",
}


# ------------------------------
# Fonctions
# ------------------------------

def chargement_isochrone(df):
    """Fonction qui transforme les données brutes en format GeoPandas."""

    df['geometry'] = df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, crs='epsg:4326')
    return gdf


# ------------------------------
# Présentation des données
# ------------------------------

# Boutons
selection_commerce = st.segmented_control(
    "Type de commerce",
    options=commerce_map_bouton.keys(),
    format_func=lambda option: commerce_map_bouton[option],
    selection_mode="single",
    default=0,
)
selection_transport = st.segmented_control(
    "Type de transport",
    options=transport_map_bouton.keys(),
    format_func=lambda option: transport_map_bouton[option],
    selection_mode="single",
    default=0,
)
selection_temps = st.segmented_control(
    "Intervalle de temps (minutes)",
    options=temps_map_bouton.keys(),
    format_func=lambda option: temps_map_bouton[option],
    selection_mode="single",
    default=0,
)

commerce = commerce_map[selection_commerce]
transport = transport_map[selection_transport]
temps = str((selection_temps + 1)*300)

# Chargement des données
df = pd.read_csv("processed/data/pop_iso_communes_final.csv", engine="python")
gdf = chargement_isochrone(df)

options = st.selectbox(
    "Barre de recherche",
    df["Nom_departement"].unique(),
    placeholder="Sélectionnez un département...",
)

# Affichage des données
column_select = commerce + "_" + transport + "_" + temps

gdf = gdf[gdf["Nom_departement"] == options]
gdf["pourcentage"] = round((gdf[column_select] / gdf["population"])*100, 2)
gdf = gdf.loc[:, ["geometry", "Nom_commune", "population_2022", "pourcentage"]]
gdf = gdf.rename(columns={"Nom_commune":"commune"})

carte = gdf.explore(column="pourcentage", 
                    style_kwds={"fillOpacity":0.3},
                    highlight_kwds={"fillOpacity":0.6},
                    legend_kwds={"max_labels":5},
                    min_zoom=5,
                    max_zoom=15,
                    cmap='coolwarm_r',
                    vmin=0,
                    vmax=1,
                    )
st.components.v1.html(folium.Figure().add_child(carte).render(), height=480, width=800)