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
gameID = 0
gameNameList = []
# st.title("Free-to-Play Game Data")

tab1, tab2 = st.tabs(["Game Info", "Graphs"])

with tab1:
    st.header("Game Info")
    baseResponse = requests.get(f"{baseURL}/games")
    for game in baseResponse.json():
        gameName = game["title"]
        gameNameList.append(gameName)
    st.selectbox("Select a game", sorted(gameNameList), key="gameSelect")
    gameID = baseResponse.json()[gameNameList.index(st.session_state.gameSelect)]["id"]
    singleGameResponse = requests.get(f"{baseURL}/game?id={gameID}")
    st.header(singleGameResponse.json()["title"])
    st.image(singleGameResponse.json()["thumbnail"])
    st.write(singleGameResponse.json()["short_description"])
    st.write(f"Genre: {singleGameResponse.json()['genre']}")
    st.write(f"Platform: {singleGameResponse.json()['platform']}")
    st.write(f"Publisher: {singleGameResponse.json()['publisher']}")
    st.write(f"Developer: {singleGameResponse.json()['developer']}")
    st.write(f"Release Date: {singleGameResponse.json()['release_date']}")
    st.write(f"Minimum System Requirements: {singleGameResponse.json()['minimum_system_requirements']}")  
    