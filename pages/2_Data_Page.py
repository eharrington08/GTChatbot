# Lab 3: API data page
# TODO: Rename this file to fit your page. Keep the number at the front, since it sets the
#       page's order in the sidebar (for example, 2_Pokedex.py).
#
# This page shows data from your API, processed with your own Python code. No AI on this page.
# It should have:
#   - at least 2 meaningful user inputs (for example st.selectbox, st.text_input, st.slider)
#   - at least 2 dynamic visuals that change based on the user's input: charts, displays of
#     images, or other visualizations (see the example website for examples!)

import requests
import streamlit as st

baseURL = "https://www.freetogame.com/api"


# st.title("Free-to-Play Game Data")

tab1, tab2 = st.tabs(["Game Info", "Graphs"])

with tab1:
    st.header("Game Info")  
    gameID = st.slider(0, 500)
    response = requests.get(f"{baseURL}/game?id={gameID}")
    