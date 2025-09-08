import streamlit as st

import pathlib
import sys

# This adds the path of the …/pages folder
# to the PYTHONPATH variable
# Source : https://www.isticktoit.net/?p=2499
sys.path.append(str(pathlib.Path().absolute()).split("/pages")[0] + "/pages")

page_1 = st.Page("pages/page_1.py", title="Présentation du projet")
page_2 = st.Page("pages/page_2.py", title="Résultats")
page_3 = st.Page("pages/page_3.py", title="Comparer des communes")
#page_4 = st.Page("pages/page_4.py", title="Carte interactive")

pg = st.navigation([page_1, page_2, page_3])	


pg.run()

