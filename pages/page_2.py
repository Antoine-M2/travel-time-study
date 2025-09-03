import streamlit as st
import pandas as pd
import plotly.express as px

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
    1: "cycling-regular",
    2: "cycling-electric",
}
transport_map_bouton = {
    0: "🚗 Voiture",
    1: "🚲 Vélo",
    2: "🔋Vélo électrique ",
}
transport_map_legend = {
    0: "voiture",
    1: "vélo",
    2: "vélo électrique",
}

# ------------------------------
# Fonctions
# ------------------------------

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

	mapping = {
		"driving-car":     "Voiture", 
		"cycling-regular": "Vélo", 
		"cycling-electric":"Vélo électrique"
	}
	df_chart["transport_label"] = df_chart["transport"].map(mapping)
	df_chart["maximum"] = maximum
	return df_chart


# ------------------------------
st.header("Résultats pour toute la France métropolitaine")
# ------------------------------

# Bouton
selection_commerce = st.segmented_control(
    "Type de commerce",
    options=commerce_map_bouton.keys(),
    format_func=lambda option: commerce_map_bouton[option],
    selection_mode="single",
    default=0,
    key="0",
)

# Création du dataframe
df_communes = pd.read_csv("processed/data/pop_iso_communes_final.csv", engine="python")
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

fig = px.line(
	df_select, x="temps", y="pourcentage", color="transport_label", 
	markers=True, labels=labels,
)
fig.update_layout(
	title_text=titre,
	yaxis_tickformat='.2%'
	)
st.plotly_chart(fig)


# ------------------------------
st.header("Résultats par taille de communes")
# ------------------------------

# Bouton
selection_commerce = st.segmented_control(
    "Type de commerce",
    options=commerce_map_bouton.keys(),
    format_func=lambda option: commerce_map_bouton[option],
    selection_mode="single",
    default=0,
    key="1",
)

# Création des dataframes
df_chart_1 = population_charts_between_interval(df_communes, minimum=100_000)
df_chart_2 = population_charts_between_interval(df_communes, minimum=50_000, maximum=100_000)
df_chart_3 = population_charts_between_interval(df_communes, minimum=10_000, maximum=50_000)
df_chart_4 = population_charts_between_interval(df_communes, minimum=5_000, maximum=10_000)
df_chart_5 = population_charts_between_interval(df_communes, minimum=1_000, maximum=5_000)
df_chart_6 = population_charts_between_interval(df_communes, maximum=1_000)
liste_df_charts = [df_chart_1, df_chart_2, df_chart_3, df_chart_4, df_chart_5, df_chart_6]

# Affichage des données
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
		[
			"100 000+ hab.",
			"50 000 - 99 999 hab.",
			"10 000 - 49 999 hab.",
			"5 000 - 9 999 hab.",
			"1 000 - 4 999 hab.",
			"Moins de 1 000 hab.",
		]
)
liste_tabs = [tab1, tab2, tab3, tab4, tab5, tab6]

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

	fig = px.line(
		df_select, x="temps", y="pourcentage", color="transport_label", 
		markers=True, labels=labels,
	)
	fig.update_layout(
		title_text=titre,
		yaxis_tickformat='.2%'
		)
	tab.plotly_chart(fig)


# ------------------------------
st.header("Résultats par type de transport")
# ------------------------------

# Boutons
selection_commerce = st.segmented_control(
    "Type de commerce",
    options=commerce_map_bouton.keys(),
    format_func=lambda option: commerce_map_bouton[option],
    selection_mode="single",
    default=0,
    key="2",
)

selection_transport = st.segmented_control(
    "Type de transport",
    options=transport_map_bouton.keys(),
    format_func=lambda option: transport_map_bouton[option],
    selection_mode="single",
    default=0,
)

# Création du dataframe
df_charts = pd.concat(liste_df_charts)
commerce, transport = commerce_map[selection_commerce], transport_map[selection_transport]
df_select = df_charts[
						(df_chart["type"]==commerce) & 
 						(df_chart["transport"]==transport)
 					 ]
df_select["maximum"] = df_select["maximum"].apply(str)

# Affichage des données
labels = {
	"temps":"Temps de trajet (en min)",
	"pourcentage":"Pourcentage",
}

fig = px.bar(
		df_select, 
		x="temps", y="pourcentage", color="maximum", barmode="group",
		labels=labels,
	)

commerce_legend = commerce_map_legend[selection_commerce]
transport_legend = transport_map_legend[selection_transport]

titre = f"Part de la population habitant à X minutes ou moins" \
		f"d'{commerce_legend} en {transport_legend}"

fig.update_layout(
	title_text=titre,
	yaxis_tickformat='.2%'
	)
st.plotly_chart(fig)
