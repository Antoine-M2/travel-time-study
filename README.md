# travel-time-study

L'application streamlit est en ligne via ce lien :
https://comparaison-trajets-voiture-velo.streamlit.app/

#### Introduction
 
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

Les données ne concernent pour l'instant que les communes de France 
métropolitaine, et seulement les supermarchés et les boulangeries.

#### Construction de la base de données

En amont de ce site, j'ai créé la base de données grâce à des algorithmes,
des données open source et une application open source.

Pour construire cette base de données, il faut d'abord calculer des isochrones.
Une isochrone permet de déterminer quelle zone géographique est atteignable 
en un temps donné selon un mode de déplacement.

Nous allons répéter ce processus pour chaque commerce en France métropolitaine, 
et fusionner les isochrones. On obtient une carte isochrone pour chaque mode de transport 
et chaque intervalle de temps.

En recoupant les cartes isochrones obtenues avec la carte de la répartition 
de la population, on obtient le pourcentage de la population étant à 
5/10/15/20/25/30 minutes d'au moins un commerce selon le type de transport.

Enfin, on recoupe une nouvelle fois les cartes isochrones et les cartes de la répartition
de la population avec la carte des communes.
Cela nous permet d'avoir des résultats par commune, et de mieux comprendre la différence
des temps de trajet en voiture et à vélo selon la taille de la commune.
Le même processus est répété pour chaque type de commerce.

#### Base de données et applications open source utilisées

Les isochrones ont été calculés grâce à une instance locale 
d'[OpenRouteService](https://openrouteservice.org/).

La liste des commerces en France métropolitaine est issue de la base de données 
d'[OpenStreetMap via Opendatasoft](https://public.opendatasoft.com/explore/dataset/osm-france-shop-craft-office/information/).

La répartition de la population sur le territoire français est issue du jeu de données 
[GHSL "Gloval Human Settlement Layer"](https://human-settlement.emergency.copernicus.eu/dataToolsOverview.php).

La base de données comportant les coordonnées des communes provient de
l'[ADEME](https://data-interne.ademe.fr/datasets/geo-contours-communes).
