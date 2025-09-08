import streamlit as st
import pandas as pd
import plotly.express as px

from utilities import *

#import numpy as np

st.title("Comparer des communes")

commerce_map = {
    0: "bakery",
    1: "supermarket",
}
commerce_map_bouton = {
    0: "🥖 Boulangeries",
    1: "🛒 Supermarchés",
}
commerce_map_legend = {
    0: "une boulangerie",
    1: "un supermarché",
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
transport_map_legend = {
    0: "en voiture",
    1: "à vélo électrique",
    2: "à vélo",
}
presentation_map_bouton = {
    0: "📈 Courbes",
    1: "📊 Barres",
}


# ------------------------------
# Fonctions
# ------------------------------

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

@st.cache_data
def load_data(url):
	df_communes = pd.read_csv(url, engine="python")
	#Création d'un nom unique (nom commune + département)
	col = df_communes["DCOE_L_LIB"] + " (" + df_communes["DDEP_C_COD"] + ")"
	df_communes.insert(0, 'nom', col)

	return df_communes


# ------------------------------
# Présentation des données
# ------------------------------

df = load_data("processed/data/pop_iso_communes_final.csv")

options = st.multiselect(
	"Barre de recherche",
	df["nom"],
	placeholder="Chercher des communes...",
	max_selections=6)

if options:

	# ------------------------------
	st.header("Résultats par communes")
	# ------------------------------

	selection_presentation = create_button("Présentation", presentation_map_bouton)
	selection_commerce = create_button("Type de commerce", commerce_map_bouton)

	labels = {
	"temps":"Temps de trajet (en min)",
	"pourcentage":"Pourcentage",
	"transport_label":"Transport"
	}

	commerce_legend = commerce_map_legend[selection_commerce]
	titre = f"Part de la population habitant à X minutes ou moins " \
			f"d'{commerce_legend}"

	liste_tabs = st.tabs(options)

	for option, tab in zip(options, liste_tabs):

		df_option = df[df["nom"].isin([option])]
		df_chart = population_charts_between_interval(df_option)

		tab.write(f"Population de la commune: {int(df_option["population"].iloc[0])}")

		commerce = commerce_map[selection_commerce]
		df_select = df_chart[df_chart["type"]==commerce]
		kwargs = {"color":"transport_label"}

		if selection_presentation == 0:
			fig = create_line_chart(df_select, labels, titre, kwargs)
		elif selection_presentation == 1:
			fig = create_bar_chart(df_select, labels, titre, kwargs)
		tab.plotly_chart(fig)


	# ------------------------------
	st.header("Résultats par type de transport")
	# ------------------------------

	# Boutons
	selection_presentation = create_button("Présentation", presentation_map_bouton, default=1)
	selection_commerce = create_button("Type de commerce", commerce_map_bouton)
	selection_transport = create_button("Type de transport", transport_map_bouton)

	# Création du dataframe
	liste_df_charts = []
	for option in options:
		df_option = df[df["nom"].isin([option])]
		df_chart = population_charts_between_interval(df_option)
		df_chart["nom"] = str(df_option["nom"].iloc[0])
		liste_df_charts.append(df_chart)

	df_charts = pd.concat(liste_df_charts)
	commerce, transport = commerce_map[selection_commerce], transport_map[selection_transport]
	df_select = df_charts[
							(df_charts["type"]==commerce) & 
	 						(df_charts["transport"]==transport)
	 					 ]

	# Affichage des données
	labels = {
		"temps":"Temps de trajet (en min)",
		"pourcentage":"Pourcentage",
		"nom":"Communes",
	}

	commerce_legend = commerce_map_legend[selection_commerce]
	transport_legend = transport_map_legend[selection_transport]

	titre = f"Part de la population habitant à X minutes ou moins " \
			f"d'{commerce_legend} {transport_legend}"
	kwargs = {"color":"nom"}

	if selection_presentation == 0:
		fig = create_line_chart(df_select, labels, titre, kwargs)
	elif selection_presentation == 1:
		fig = create_bar_chart(df_select, labels, titre, kwargs)
	st.plotly_chart(fig)