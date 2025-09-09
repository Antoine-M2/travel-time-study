import streamlit as st
import pandas as pd
import plotly.express as px

import geopandas as gpd
from shapely import wkt
import folium

st.title("Comparaison des moyens de transports individuels pour les trajets quotidiens")


# ------------------------------
# Fonctions
# ------------------------------

def chargement_isochrone(df):
    """Fonction qui transforme les données brutes en format GeoPandas."""
    try:
        chargement_isochrone.counter += 1
    except AttributeError:
        chargement_isochrone.counter = 1

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

    selection_transport = st.segmented_control(
        "Type de transport",
        options=transport_map_bouton.keys(),
        format_func=lambda option: transport_map_bouton[option],
        selection_mode="single",
        key=chargement_isochrone.counter,
        default=0,
    )

    transport = transport_map[selection_transport]

    #Chargement des données
    df['geometry'] = df['geometry'].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, crs='epsg:4326')
    gdf = gdf[gdf["transport"]==transport]
    gdf = gdf[["minutes", "geometry"]]

    return gdf


# ------------------------------
# Sidebar
# ------------------------------

# st.sidebar.write("Accueil")


# ------------------------------
st.header("Introduction")
# ------------------------------

markdown_text = (
"""
Ma principale motivation pour construire ce site et la base de données
l'alimentant était la suivante : 

Les infrastructures de transport, pour les déplacements
du quotidien, sont construites principalement pour les voitures.

Cependant, le vélo devrait être compétitif face à la voiture dans les 
grandes villes (en terme de temps de déplacement pour les trajets du quotidien),
mais quel est l'écart réel d'efficacité entre eux ?
De même, dans les plus petites villes et villages, la voiture devrait être
plus efficace en général que les vélos, mais quel est l'écart réel entre eux ? 

J'ai créé ce site pour pouvoir répondre à ces questions : il permet
de comparer les temps de trajet en voiture ou en vélo 
(avec assistance électrique ou non) lors des trajets du quotidien 
(par exemple pour faire des courses), grâce à des visualisations de données
interactives.

Pour chaque commune, la base de données contient quel pourcentage 
de la population habite à 5, 10, 15, 20, 25 et 30 minutes d'un supermarché 
ou d'une boulangerie, selon le mode de déplacement choisi : voiture, 
vélo et vélo électrique.

Vous pouvez consulter les résultats pour l'ensemble de la population
de France métropolitaine [sur cette page](./page_2).

Vous pouvez aussi chercher dans la base de données des communes pour les 
comparer (jusqu'à 6) [sur cette page](./page_3).

Les données ne concernent pour l'instant que les communes de France 
métropolitaine, et seulement les supermarchés et les boulangeries.
Mais le site sera prochainement mis à jour avec de nouvelles données !
"""
)
st.write(markdown_text)


# ------------------------------
st.header("Construction de la base de données")
# ------------------------------

markdown_text = (
"""
En amont de ce site, j'ai créé la base de données grâce à des algorithmes,
des données open source et une application open source.

Pour construire cette base de données, il faut d'abord calculer des isochrones.
Une isochrone permet de déterminer quelle zone géographique est atteignable 
en un temps donné selon un mode de déplacement.

Ci-dessous, vous pouvez voir un exemple avec les isochrones de 5 à 30 minutes
pour chaque mode de transport, pour le même supermarché :
"""
)
st.write(markdown_text)


# ------------------------------
# Visualisation isochrone
# ------------------------------

df = pd.read_csv("processed/data/exemple_visualisation_1.csv", engine="python")
gdf = chargement_isochrone(df)

geo_point = gdf.loc[gdf["minutes"] == 0, "geometry"]
x, y = float(geo_point.y.iloc[0]), float(geo_point.x.iloc[0])
pad = 0.1
sw, ne = [x - pad, y - pad], [x + pad, y + pad]

carte = gdf.explore(column="minutes", 
                marker_type="marker",
                style_kwds={"fillOpacity":0.15}, 
                legend_kwds={"max_labels":6},
                min_zoom=10,
                max_zoom=15,
                )
carte.fit_bounds([sw, ne])
st.components.v1.html(folium.Figure().add_child(carte).render(), height=480, width=600)


# ------------------------------
# Paragraphe
# ------------------------------

markdown_text = (
"""
On constate que la voiture permet au supermarché d'atteindre une clientèle sur une zone
beaucoup plus large qu'avec le vélo. Mais les supermarchés sont présents partout sur le territoire :
nous allons donc répéter ce processus pour chaque supermarché en France métropolitaine, 
et fusionner les isochrones. On obtient une carte isochrone pour chaque mode de transport 
et chaque intervalle de temps.

En recoupant les cartes isochrones obtenues avec la carte de la répartition 
de la population, on obtient le pourcentage de la population étant à 
5/10/15/20/25/30 minutes d'au moins un supermarché selon le type de transport.

Ci-dessous, vous pouvez voir un exemple avec la carte isochrone des supermarchés
dans le Calvados :
"""
)
st.write(markdown_text)


# ------------------------------
# Visualisation isochrone
# ------------------------------

df = pd.read_csv("processed/data/exemple_visualisation_2.csv", engine="python")
gdf = chargement_isochrone(df)

carte = gdf.explore(column="minutes", 
                marker_type="marker",
                style_kwds={"fillOpacity":0.15}, 
                legend_kwds={"max_labels":5},
                min_zoom=9,
                max_zoom=15,
                )
st.components.v1.html(folium.Figure().add_child(carte).render(), height=480, width=600)


# ------------------------------
# Paragraphe
# ------------------------------

markdown_text = (
"""
Enfin, on recoupe une nouvelle fois les cartes isochrones et les cartes de la répartition
de la population avec la carte des communes.
Cela nous permet d'avoir des résultats par commune, et de mieux comprendre la différence
des temps de trajet en voiture et à vélo selon la taille de la commune.
Le même processus est répété pour les boulangeries.

#### Base de données et applications open source utilisées

Les isochrones ont été calculés grâce à une instance locale 
d'[OpenRouteService](https://openrouteservice.org/).

La liste des commerces en France métropolitaine est issue de la base de données 
d'[OpenStreetMap via Opendatasoft](https://public.opendatasoft.com/explore/dataset/osm-france-shop-craft-office/information/).

La répartition de la population sur le territoire français est issue du jeu de données 
[GHSL "Gloval Human Settlement Layer"](https://human-settlement.emergency.copernicus.eu/dataToolsOverview.php).

La base de données comportant les coordonnées des communes provient de
l'[ADEME](https://data-interne.ademe.fr/datasets/geo-contours-communes).

"""
)

st.write(markdown_text)