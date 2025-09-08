import streamlit as st
#import pandas as pd
import plotly.express as px

def create_line_chart(df, labels, titre, kwargs={}):

	fig = px.line(
		df, x="temps", y="pourcentage", labels=labels, markers=True, **kwargs,
	)
	fig.update_layout(
		title_text=titre,
		yaxis_tickformat='.2%',
	)
	return fig

def create_bar_chart(df, labels, titre, kwargs={}):

	fig = px.bar(
		df, x="temps", y="pourcentage", labels=labels, barmode="group", **kwargs,
	)
	fig.update_layout(
		title_text=titre,
		yaxis_tickformat='.2%',
		)
	return fig