import streamlit as st
import pandas as pd
import plotly.express as px

from utilities import *

st.title("Résultats")

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
    0: "📈 Lignes",
    1: "📊 Barres",
}

@st.cache_data
def load_data(url):
	return pd.read_csv(url, engine="python")

df_communes = load_data("processed/data/pop_iso_communes_final.csv")


# ------------------------------
# Fonctions
# ------------------------------

def create_button(nom, mapping, default=0):

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


def population_charts_between_interval(df_communes, minimum=0, maximum=100_000_000):
	cols = df_communes.columns[10:]
	df_select = df_communes[
		(df_communes["population"] >= minimum) & (df_communes["population"] < maximum)
	]

	df_chart = pd.DataFrame(columns=["type", "transport", "temps", "pourcentage"])
	for i, col in enumerate(cols):
		df_chart.loc[i] = col.split('_') + [df_select[col].sum()/df_select["population"].sum()]
	df_chart["temps"] = df_chart["temps"].apply(int) // 60

	# st.write(df_select[["DCOE_L_LIB", "population"]].sort_values(by=["population"], ascending=False))

	#
	mapping_order= {
	    "driving-car"      : 0,
	    "cycling-electric" : 1,
	    "cycling-regular"  : 2,
	}
	df_chart = df_chart.sort_values(by="transport", key=lambda col: col.map(mapping_order))
	df_chart = df_chart.sort_values(by="temps")

	mapping = {
		"driving-car":     "Voiture", 
		"cycling-electric":"Vélo électrique",
		"cycling-regular": "Vélo"
	}
	df_chart["transport_label"] = df_chart["transport"].map(mapping)
	df_chart["maximum"] = maximum
	return df_chart


# ------------------------------
st.header("Résultats pour toute la France métropolitaine")
# ------------------------------

# Bouton
selection_presentation = create_button("Présentation", presentation_map_bouton)
selection_commerce = create_button("Type de commerce", commerce_map_bouton)

# Création du dataframe
df_chart = population_charts_between_interval(df_communes)

# Affichage des données
labels = {
	"temps":"Temps de trajet (en min)",
	"pourcentage":"Pourcentage",
	"transport_label":"Transport"
}

commerce_legend = commerce_map_legend[selection_commerce]
titre = f"Part de la population habitant à X minutes ou moins " \
		f"d'{commerce_legend}"

commerce = commerce_map[selection_commerce]
df_select = df_chart[df_chart["type"]==commerce]
kwargs = {"color":"transport_label"}

if selection_presentation == 0:
	fig = create_line_chart(df_select, labels, titre, kwargs)
elif selection_presentation == 1:
	fig = create_bar_chart(df_select, labels, titre, kwargs)
st.plotly_chart(fig)


# ------------------------------
st.header("Résultats par taille de communes")
# ------------------------------

# Bouton
selection_presentation = create_button("Présentation", presentation_map_bouton)
selection_commerce = create_button("Type de commerce", commerce_map_bouton)

# Création des dataframes
df_chart_1 = population_charts_between_interval(df_communes, minimum=100_000)
df_chart_2 = population_charts_between_interval(df_communes, minimum=50_000, maximum=100_000)
df_chart_3 = population_charts_between_interval(df_communes, minimum=10_000, maximum=50_000)
df_chart_4 = population_charts_between_interval(df_communes, minimum=5_000, maximum=10_000)
df_chart_5 = population_charts_between_interval(df_communes, minimum=1_000, maximum=5_000)
df_chart_6 = population_charts_between_interval(df_communes, maximum=1_000)
liste_df_charts = [df_chart_1, df_chart_2, df_chart_3, df_chart_4, df_chart_5, df_chart_6]

# Affichage des données
liste_tabs = st.tabs(
		[
			"100 000+ hab.",
			"50 000 - 99 999 hab.",
			"10 000 - 49 999 hab.",
			"5 000 - 9 999 hab.",
			"1 000 - 4 999 hab.",
			"Moins de 1 000 hab.",
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

	if selection_presentation == 0:
		fig = create_line_chart(df_select, labels, titre, kwargs)
	elif selection_presentation == 1:
		fig = create_bar_chart(df_select, labels, titre, kwargs)
	tab.plotly_chart(fig)


# ------------------------------
st.subheader("Sélectionnez l'intervalle")
# ------------------------------

intervalle = st.slider("Sélectionnez un intervalle de population :", 
						0, 100_000, (2_000, 50_000), step=50)

# Bouton
selection_presentation = create_button("Présentation", presentation_map_bouton)
selection_commerce = create_button("Type de commerce", commerce_map_bouton)

# Création du dataframe
df_chart = population_charts_between_interval(df_communes, 
											  minimum=intervalle[0], maximum=intervalle[1])

# Affichage des données
labels = {
	"temps":"Temps de trajet (en min)",
	"pourcentage":"Pourcentage",
	"transport_label":"Transport"
}

commerce_legend = commerce_map_legend[selection_commerce]
titre = f"Part de la population habitant à X minutes ou moins " \
		f"d'{commerce_legend}"

commerce = commerce_map[selection_commerce]
df_select = df_chart[df_chart["type"]==commerce]

if selection_presentation == 0:
	fig = create_line_chart(df_select, labels, titre, kwargs)
elif selection_presentation == 1:
	fig = create_bar_chart(df_select, labels, titre, kwargs)
st.plotly_chart(fig)


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
	1_000      :"Moins de 1 000 hab.",
	5_000      :"1 000 - 4 999 hab.",
	10_000     :"5 000 - 9 999 hab.",
	50_000     :"10 000 - 49 999 hab.",
	100_000    :"50 000 - 99 999 hab.",
	100_000_000:"100 000+ hab.",
}
df_select["max_pop"] = df_select["maximum"].map(mapping)

commerce_legend = commerce_map_legend[selection_commerce]
transport_legend = transport_map_legend[selection_transport]

titre = f"Part de la population habitant à X minutes ou moins " \
		f"d'{commerce_legend} {transport_legend}"
kwargs = {"color":"max_pop"}

if selection_presentation == 0:
	fig = create_line_chart(df_select, labels, titre, kwargs)
elif selection_presentation == 1:
	fig = create_bar_chart(df_select, labels, titre, kwargs)
st.plotly_chart(fig)
