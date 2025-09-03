import streamlit as st
import pandas as pd
import plotly.express as px

#st.set_page_config(page_title = "Résultats")
st.title("Résultats")


# ------------------------------
# Page 2 - Résultats
# ------------------------------

df_communes = pd.read_csv(f"processed/data/pop_iso_communes_final.csv", engine="python")

#df_communes

def plot_charts_population_between_interval(df_communes, minimum=0, maximum=100_000_000):
	cols = df_communes.columns[10:]
	df_select = df_communes[
		(df_communes["population"] >= minimum) & (df_communes["population"] < maximum)
	]

	df_chart = pd.DataFrame(columns=["type", "transport", "temps", "pourcentage"])
	for i, col in enumerate(cols):
		df_chart.loc[i] = col.split('_') + [df_select[col].sum()/df_select["population"].sum()]
	df_chart["temps"] = df_chart["temps"].apply(int) // 60



	# st.write(df_select[["DCOE_L_LIB", "population"]].sort_values(by=["population"], ascending=False))

	df_chart["maximum"] = maximum
	return df_chart


df_chart_1 = plot_charts_population_between_interval(df_communes, minimum=100_000)
df_chart_2 = plot_charts_population_between_interval(df_communes, minimum=50_000, maximum=100_000)
df_chart_3 = plot_charts_population_between_interval(df_communes, minimum=10_000, maximum=50_000)
df_chart_4 = plot_charts_population_between_interval(df_communes, minimum=5_000, maximum=10_000)
df_chart_5 = plot_charts_population_between_interval(df_communes, minimum=1_000, maximum=5_000)
df_chart_6 = plot_charts_population_between_interval(df_communes, maximum=1_000)

liste_df_charts = [df_chart_1, df_chart_2, df_chart_3, df_chart_4, df_chart_5, df_chart_6]


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


for df, tab in zip(liste_df_charts, liste_tabs):

	fig = px.line(
		df[df["type"]=="bakery"], 
		x="temps", y="pourcentage", color="transport", markers=True
	)
	tab.plotly_chart(fig)

	fig = px.line(
		df[df["type"]=="supermarket"], 
		x="temps", y="pourcentage", color="transport", markers=True
	)
	tab.plotly_chart(fig)


df_chart_test = pd.DataFrame()
l = []
for df_chart in liste_df_charts:
	l.append(
			 df_chart[
						(df_chart["type"]=="supermarket") & 
						(df_chart["transport"]=="cycling-electric")
					 ]
			)

df_chart_test = pd.concat(l)

df_chart_test["maximum"] = df_chart_test["maximum"].apply(str)

fig = px.bar(
		df_chart_test, 
		x="temps", y="pourcentage", color="maximum", barmode="group",
	)
st.plotly_chart(fig)


