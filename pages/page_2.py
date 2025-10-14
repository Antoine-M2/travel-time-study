import streamlit as st
import pandas as pd
import plotly.express as px

from streamlit.delta_generator import DeltaGenerator

from utilities import *

pd.options.mode.copy_on_write = True

st.title("Résultats généraux")

# ------------------------------
# Fonctions
# ------------------------------

@st.cache_data
def load_data(url:str) -> pd.DataFrame():
	"""Fonction chargeant les données en dataframe Pandas."""
	return pd.read_csv(url, engine="python")

def create_button(nom:str, mapping:dict, default:int=0) -> "DeltaGenerator":
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
st.header("Résultats pour toute la France métropolitaine")
# ------------------------------

# Chargement du dataframe
df_communes = load_data("processed/data/pop_iso_communes_final.csv")


# Bouton
selection_presentation = create_button("Présentation", presentation_map_bouton)
selection_commerce = create_button("Type de commerce", commerce_map_bouton)

# Création du dataframe
df_chart = population_charts(df_communes)

# Affichage des données
labels = {
	"temps":"Temps de trajet (en min)",
	"pourcentage":"Pourcentage",
	"transport_label":"Transport"
}

commerce_legend = commerce_map_legend[selection_commerce]
titre = f"Part de la population habitant à X minutes ou moins " \
		f"d'{commerce_legend}"
st.markdown(f"**{titre}**")

commerce = commerce_map[selection_commerce]
df_select = df_chart[df_chart["type"]==commerce]
kwargs = {"color":"transport_label"}

if selection_presentation == 0:
	fig = create_line_chart(df_select, labels, kwargs)
elif selection_presentation == 1:
	fig = create_bar_chart(df_select, labels, kwargs)
st.plotly_chart(fig)


# ------------------------------
st.header("Résultats par taille de communes")
# ------------------------------

# Bouton
selection_presentation = create_button("Présentation", presentation_map_bouton)
selection_commerce = create_button("Type de commerce", commerce_map_bouton)

# Création des dataframes
liste_df_charts = []
for i in range(7):
	df_chart = population_charts(df_communes, densite=i+1)
	liste_df_charts.append(df_chart)

# Affichage des données
liste_tabs = st.tabs(
		[
			"Grands centres urbains",
			"Centres urbains intermédiaires",
			"Petites villes",
			"Ceintures urbaines",
			"Bourgs ruraux",
			"Rural à habitat dispersé",
			"Rural à habitat très dispersé",
		]
)

labels = {
	"temps":"Temps de trajet (en min)",
	"pourcentage":"Pourcentage",
	"transport_label":"Transport"
}
commerce_legend = commerce_map_legend[selection_commerce]
titre = f"Part de la population habitant à X minutes ou moins " \
		f"d'{commerce_legend}"

for df, tab in zip(liste_df_charts, liste_tabs):

	commerce = commerce_map[selection_commerce]
	df_select = df[df["type"]==commerce]

	tab.markdown(f"**{titre}**")

	if selection_presentation == 0:
		fig = create_line_chart(df_select, labels, kwargs)
	elif selection_presentation == 1:
		fig = create_bar_chart(df_select, labels, kwargs)
	tab.plotly_chart(fig)

# ------------------------------
st.header("Résultats par type de transport")
# ------------------------------

# Boutons
selection_presentation = create_button("Présentation", presentation_map_bouton, default=1)
selection_commerce = create_button("Type de commerce", commerce_map_bouton)
selection_transport = create_button("Type de transport", transport_map_bouton)

# Création du dataframe
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
	"max_pop":"Population",
}
mapping = {
	1:"Grands centres urbains",
	2:"Centres urbains intermédiaires",
	3:"Petites villes",
	4:"Ceintures urbaines",
	5:"Bourgs ruraux",
	6:"Rural à habitat dispersé",
	7:"Rural à habitat très dispersé",
}
df_select["densite"] = df_select["densite"].map(mapping)

commerce_legend = commerce_map_legend[selection_commerce]
transport_legend = transport_map_legend[selection_transport]

titre = f"Part de la population habitant à X minutes ou moins " \
		f"d'{commerce_legend} {transport_legend}"
st.markdown(f"**{titre}**")

kwargs = {"color":"densite"}

if selection_presentation == 0:
	fig = create_line_chart(df_select, labels, kwargs)
elif selection_presentation == 1:
	fig = create_bar_chart(df_select, labels, kwargs)
st.plotly_chart(fig)
