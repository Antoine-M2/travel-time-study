import streamlit as st

page_1 = st.Page("pages/page_1.py", title="Accueil", icon="🏠")
page_2 = st.Page("pages/page_2.py", title="Résultats", icon="📊")
page_3 = st.Page("pages/page_3.py", title="Chercher des communes", icon="🔍")
#page_4 = st.Page("pages/page_4.py", title="Carte interactive", icon="🌎")

pg = st.navigation([page_1, page_2, page_3])	


pg.run()

