import streamlit as st
import pandas as pd
import plotly.express as px

from utilities import *

#import numpy as np

st.title("Comparer des communes")

presentation_map_bouton = {
    0: "📈 Courbes",
    1: "📊 Barres",
}
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
	"Titre",
	df["nom"],
	max_selections=5)

if options:

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

		commerce = commerce_map[selection_commerce]
		df_select = df_chart[df_chart["type"]==commerce]
		kwargs = {"color":"transport_label"}

		if selection_presentation == 0:
			fig = create_line_chart(df_select, labels, titre, kwargs)
		elif selection_presentation == 1:
			fig = create_bar_chart(df_select, labels, titre, kwargs)
		tab.plotly_chart(fig)