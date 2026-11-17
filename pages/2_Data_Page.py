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
import plotly.express as px
import pandas as pd

baseURL = "https://www.freetogame.com/api"
gameID = 0
gameNameList = []
genreByDevDictionary = {}
releaseDateDictionary = {}
# st.title("Free-to-Play Game Data")

tab1, tab2 = st.tabs(["Game Info", "Graphs"])

with tab1:
    st.header("Game Info")
    
    baseResponse = requests.get(f"{baseURL}/games")
         
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
    try:
        st.write(f"Minimum System Requirements: {singleGameResponse.json()['minimum_system_requirements']}")  
    except:
        st.write("There are no published minimum game requirements.")
    
with tab2:
    st.header("Graphs")
    
    for game in baseResponse.json():
        gameName = game["title"]
        developer = game["developer"]
        releaseDate = game["release_date"]
        genre = game["genre"]

        if developer not in genreByDevDictionary:
            genreByDevDictionary[developer] = {}

        if genre not in genreByDevDictionary[developer]:
            genreByDevDictionary[developer][genre] = 0

        genreByDevDictionary[developer][genre] += 1
        if developer not in releaseDateDictionary:
            releaseDateDictionary[developer] = []
        releaseDateDictionary[developer].append(releaseDate)  
    # line chart of number of games released by each developer over time
    st.subheader("Number of Games Released by Each Developer Over Time")
    st.multiselect("Select developers to display", sorted(releaseDateDictionary.keys()), key="developerSelect")
    selectedDevelopers = st.session_state.developerSelect
    if selectedDevelopers:
        releaseDateData = []
        for developer in selectedDevelopers:
            for releaseDate in releaseDateDictionary[developer]:
                releaseDateData.append({"Developer": developer, "Release Date": releaseDate})
        releaseDateDF = pd.DataFrame(releaseDateData)
        releaseDateDF["Release Date"] = pd.to_datetime(releaseDateDF["Release Date"])
        releaseDateDF = releaseDateDF.groupby(["Developer", pd.Grouper(key="Release Date", freq="Y")]).size().reset_index(name="Count")
        fig = px.line(releaseDateDF, x="Release Date", y="Count", color="Developer", title="Number of Games Released by Each Developer Over Time")
        st.plotly_chart(fig)
    
    