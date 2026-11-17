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
import altair as alt

baseURL = "https://www.freetogame.com/api"
gameID = 0
gameNameList = []
genreByDevDictionary = {}
releaseDateDictionary = {}
label = ""
# st.title("Free-to-Play Game Data")

tab1, tab2 = st.tabs(["Game Info", "Graphs"])

with tab1:
    st.header("Game Info")
    
    baseResponse = requests.get(f"{baseURL}/games")
    for game in baseResponse.json():
        gameNameList.append(game["title"])   
    st.selectbox("Select a game", sorted(gameNameList), key="gameSelect")
    
    gameID = baseResponse.json()[gameNameList.index(st.session_state.gameSelect)]["id"]
    singleGameResponse = requests.get(f"{baseURL}/game?id={gameID}")
    game = singleGameResponse.json()
    st.header(game["title"])
    st.image(game["thumbnail"])
    st.write(game["short_description"])
    st.write(f"**Genre**: {game['genre']}")
    st.write(f"**Platform**: {game['platform']}")
    st.write(f"**Publisher**: {game['publisher']}")
    st.write(f"**Developer**: {game['developer']}")
    st.write(f"**Release Date**: {game['release_date']}")
    try:
        st.markdown("<u>**Minimum System Requirements**:</u>", unsafe_allow_html=True)
        for specType, spec in game['minimum_system_requirements'].items():
            st.write(f"**{specType}**: {spec}")
    except:
        st.write("There are no published minimum game requirements.")
    
    if "showAll" not in st.session_state:
        st.session_state.showAll = -1

    def toggle():
       st.session_state.showAll *= -1
    if st.session_state.showAll == 1:
        label = "Hide Extra Data"
    else:
        label = "Show Extra Data"
    st.button(label, on_click=toggle)
    if st.session_state.showAll == 1:
        st.write(f"**Long Description**: {game['description']}")
        st.write("**In-Game Screenshots**")
        for image in game.get("screenshots", []):
            st.image(image["image"])
        
with tab2:
    st.header("Graphs")

    for game in baseResponse.json():
        gameName = game["title"]
        developer = game["developer"]
        releaseDate = game["release_date"]
        genre = game["genre"].strip()

        if developer not in genreByDevDictionary:
            genreByDevDictionary[developer] = {}

        if genre not in genreByDevDictionary[developer]:
            genreByDevDictionary[developer][genre] = 0

        genreByDevDictionary[developer][genre] += 1

        if developer not in releaseDateDictionary:
            releaseDateDictionary[developer] = []

        releaseDateDictionary[developer].append(releaseDate)
    st.multiselect(
        "Select developers to display",
        sorted(releaseDateDictionary.keys()),
        key="developerSelect"
    )
    st.subheader("Number of Games Released by Each Developer Over Time")

    selectedDevelopers = st.session_state.developerSelect

    if selectedDevelopers:
        releaseDateData = []

        for developer in selectedDevelopers:
            for releaseDate in releaseDateDictionary[developer]:
                releaseDateData.append({
                    "Developer": developer,
                    "Release Date": releaseDate
                })

        releaseDateDF = pd.DataFrame(releaseDateData)

        releaseDateDF["Release Date"] = pd.to_datetime(
            releaseDateDF["Release Date"]
        ).dt.year

        releaseDateDF = releaseDateDF.groupby(
            ["Developer", "Release Date"]
        ).size().reset_index(name="Count")

        releaseDateDF["Count"] = releaseDateDF.groupby(
            "Developer"
        )["Count"].cumsum()

        graph = px.line(
            releaseDateDF,
            x="Release Date",
            y="Count",
            color="Developer",
            markers=True,
            title="Cumulative Number of Games Released by Each Developer"
        )

        st.plotly_chart(graph)
    
    # altair chart for genre distribution by developer
   # Altair chart for genre distribution by developer
    # Altair chart for genre distribution by developer
    st.subheader("Genre Distribution by Developer")

    allGenres = sorted({
        genre
        for developer in genreByDevDictionary
        for genre in genreByDevDictionary[developer]
    })

    selectedGenres = st.multiselect(
        "Select genres to display",
        allGenres,
        key="genreSelect"
    )

    if selectedGenres:
        genreData = []

        for developer in genreByDevDictionary:
            for genre, count in genreByDevDictionary[developer].items():
                if genre in selectedGenres:
                    genreData.append({
                        "Developer": "Other" if count == 1 else developer,
                        "Genre": genre,
                        "Count": count
                    })

        genreDF = pd.DataFrame(genreData)
        
        # genreDF = genreDF.groupby(
        #     ["Developer", "Genre"], as_index=False
        # )["Count"].sum()

        chart = alt.Chart(genreDF).mark_bar().encode(
            x=alt.X("Genre:N", title="Genre"),
            y=alt.Y("Count:Q", title="Number of Games"),
            color=alt.Color(
                "Developer:N",
                title="Developer"
            ),
            tooltip=["Developer", "Genre", "Count"]
        ).properties(
            title="Number of Games by Developer for Selected Genres",
            
        )

        st.altair_chart(chart, use_container_width=True)
            
        
        
        
        
        