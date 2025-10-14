import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------
# Variables communes à toutes les pages
# ------------------------------

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
commerce_map_legend = {
    0: "une boulangerie",
    1: "un supermarché",
    2: "une supérette",
    3: "un bureau de poste",
    4: "une pharmacie",
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

def create_line_chart(df:pd.DataFrame, labels:dict, kwargs:dict={}) -> go.Figure():
	"""Fonction créant un graphique en courbes."""
	fig = px.line(
		df, x="temps", y="pourcentage", labels=labels, markers=True, **kwargs,
	)
	fig.update_layout(
		#title_text=titre,
		yaxis_tickformat='.2%',
		legend = dict(orientation="h", xanchor="center", x=0.5, y=-0.25),
	)
	return fig

def create_bar_chart(df:pd.DataFrame, labels:dict, kwargs:dict={}) -> go.Figure():
	"""Fonction créant un graphique en barres."""
	fig = px.bar(
		df, x="temps", y="pourcentage", labels=labels, barmode="group", **kwargs,
	)
	fig.update_layout(
		#title_text=titre,
		yaxis_tickformat='.2%',
		legend = dict(orientation="h", xanchor="center", x=0.5, y=-0.25),
	)
	return fig

def population_charts(df_communes:pd.DataFrame, densite:int=0) -> pd.DataFrame:
	"""Fonction permettant de transformer les données brutes des communes.

	Elle permet de transformer les données afin d'obtenir un nouveau tableau 
	contenant le  pourcentage de population pour chaque paramètre : type de commerce,
	type de transport et intervalle de temps.

	Args:
		df_communes: La base de données à transformer.
		densite: Densité de la commune (1 = le plus dense, 7 = le moins dense)
	
	Returns:
		df_chart : Le tableau de données transformé.

	"""
	if densite == 0:
		df_select = df_communes
	else:
		df_select = df_communes[df_communes["DENS7"] == densite]

	cols = df_select.columns[df_select.columns.str.contains("driving-car|cycling-electric|cycling-regular")]
	df_chart = pd.DataFrame(columns=["type", "transport", "temps", "pourcentage"])
	for i, col in enumerate(cols):
		df_chart.loc[i] = col.split('_') + [df_select[col].sum()/df_select["population"].sum()]
	df_chart["temps"] = df_chart["temps"].apply(int) // 60

	mapping_order = {
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
	df_chart["densite"] = densite
	return df_chart