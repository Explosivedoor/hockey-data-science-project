import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
st.write('''<style>

[data-testid="column"] {
    width: calc(33.3333% - 1rem) !important;
    flex: 1 1 calc(33.3333% - 1rem) !important;
    min-width: calc(33% - 1rem) !important;
}
</style>''', unsafe_allow_html=True)
conn = sqlite3.connect("C:\\Users\\Johnny\\source\\repos\Hockey program v2\\Hockey program v2\\test.db")
conn2 = sqlite3.connect("C:\\Users\\Johnny\\source\\repos\Hockey program v2\\Hockey program v2\\KIHF2.db")
cursor = conn.cursor()
cursor2 = conn2.cursor()
st.title("KIHF Stats 2023-2024")
st.caption("Stats may be inncorrect due to limitations of the ingest software (eg. number change during season)")
tab1, tab2= st.tabs([ "Team Stats", "Game Scoresheet Look Up"])
with tab2:
    
    
    
    df = pd.read_sql_query(f"SELECT * FROM KIHF", conn)
    choice = st.selectbox("Pick A Team",(df['team_name']), index=None,
    placeholder="Pick A Team")
    if choice == None:
        pass
    else:
        choice = df[df['team_name'] == choice]
        team = choice.iloc[0,1]
        st.write(team)
        
        
        df3 = pd.read_sql_query(f"SELECT * FROM game WHERE team_a = '{team}' OR  team_b = '{team}'", conn2)
        st.write(df3)
        st.dataframe(df3.drop(["date", "location"], axis=1), hide_index = True)
        selected_game = st.selectbox("Select a Game",df3['game_no'])
        
        game_no = df3[df3['game_no'] == selected_game]
       
        game_stats = df3[df3['game_no'] == selected_game]
       
        game_no = game_no.iloc[0,0]
        df3 = pd.read_sql_query(f"SELECT * FROM '{game_no}' ", conn)
        
        col1,col2= st.columns(2)
        col1.header(game_stats.iloc[0,1])
        col2.metric("Goals",game_stats.iloc[0,2])
        col2.metric("Goals",game_stats.iloc[0,4])
        col1.header(game_stats.iloc[0,3])

        col1, col2 = st.columns(2)    
        score_sheet_on = col1.toggle("See Score Sheet")
        if score_sheet_on:

            on = col2.toggle("Performance Players only")
            goalie_on = col2.toggle("Goalies Only")

            if not on and not goalie_on:   
                st.header("Score Sheet")
                other_team_name = df3.loc[df3['team_name'] != team, 'team_name'].unique()[0]
                st.write(f"{other_team_name}")
                st.dataframe(df3[~((df3['team_name'] == team))].drop(["team_name"], axis=1), hide_index = True)
                st.write(f"{team}")
                st.dataframe(df3[((df3['team_name'] == team))].drop(["team_name"], axis=1), hide_index = True)
            elif on and not goalie_on:
                
                performance_players = df3[~((df3['goal'] == 0) & (df3['assist'] == 0) & (df3['pim'] == 0))]
                other_team_name = df3.loc[df3['team_name'] != team, 'team_name'].unique()[0]

                st.header("Performance Players")
                #st.dataframe(performance_players.drop(["saves",'mip','ga'], axis=1), hide_index = True)
                st.write(f"{other_team_name}")
                st.dataframe(performance_players[~((performance_players['team_name'] == team))].drop(["team_name"], axis=1), hide_index = True)
                st.write(f"{team}")
                st.dataframe(performance_players[((performance_players['team_name'] == team))].drop(["team_name"], axis=1), hide_index = True)
                #goalies only
                st.header("Goalies")
                st.dataframe(df3.dropna().drop(["goal",'position'], axis=1), hide_index = True)
            if goalie_on and on or not on and goalie_on:
                on = True
                st.header("Goalies")
                st.dataframe(df3.dropna().drop(["goal",'position'], axis=1), hide_index = True)

    __ ="""
    else:




        date=st.date_input("Look Up Game By Date",format="MM-DD-YYYY")
        
        date = str(int(date.month)) + "-" + str(int(date.day)) + "-" + str(int(date.year))
        df3 = pd.read_sql_query(f"SELECT * FROM game WHERE date = '{date}'", conn2)


        df3= df3.drop(["date"], axis=1)
        df3 = df3.rename(columns={"game_no":"Game #", "team_a": "Team A", "team_a_score":"Team A Score","team_b":"Team B", "team_b_score":"Team B Score","location":"Rink" } )
        #prevents from throwing error when no game
        if df3.empty:
            st.write("No Games Found on This Date")
        else:
            st.dataframe(df3, hide_index = True)
            #test on 2-22-2024, here because sometimes 2 games on same day
            if df3.shape[0] > 1:
                selected_game = st.selectbox("Select a Game",df3['Game #'])
                game_no = df3[df3['Game #'] == selected_game]
                
                game_no = game_no.iloc[0,0]
                
            else:
                game_no = df3.iloc[0,0]

        
            #try condition because of forfits 
            try:
                df3 = pd.read_sql_query(f"SELECT * FROM '{game_no}' ", conn)
            
                col1, col2 = st.columns(2)    
                score_sheet_on = col1.toggle("See Score Sheet")
                if score_sheet_on:

                    on = col2.toggle("Performance Players only")
                    goalie_on = col2.toggle("Goalies Only")

                    if not on:   
                        st.header("Score Sheet")
                        st.write(df3)
                    elif on and not goalie_on:
                        columns_to_check = ['goal', 'assist', 'pim','ga']
                        performance_players = df3[~((df3['goal'] == 0) & (df3['assist'] == 0) & (df3['pim'] == 0))]


                        st.header("Performance Players")
                        st.dataframe(performance_players.drop(["saves",'mip','ga'], axis=1), hide_index = True)
                        #goalies only
                        st.header("Goalies")
                        st.dataframe(df3.dropna().drop(["goal",'position'], axis=1), hide_index = True)
                    if goalie_on and on:
                        on = True
                        st.header("Goalies")
                        st.dataframe(df3.dropna().drop(["goal",'position'], axis=1), hide_index = True)
            except:
                st.write("No Game was Held")
            """
    with tab1:
        ###############################################################################################################################################
        
        col1, col2 = st.columns(2)

        div = col1.selectbox("Select a Division", (1,2,3,4,5))

        df = pd.read_sql_query(f"SELECT * FROM KIHF WHERE division = {div}", conn)
        
        df = df.rename(columns={"team_name":"Team Name", "goal": "Goals", "assist":"Assists","wins":"Wins", "losses":"Losses","sog":"SOG","ga":"GA",'ties':'Ties',"pim":'PIM','sa':'SA' } )
        df = df.drop(["division"], axis=1)

        div_on = col1.toggle("See Division Standings")
        if div_on:
            st.write(f"Division {div} Standings")
            st.dataframe(df.sort_values('Wins', ascending=False), hide_index = True)
       




        #ranking thing
        team ={}
        for i,y in enumerate(df.iterrows()):
            
            team_name = df.iloc[i,0]             
            points = df.iloc[i,2]*3+df.iloc[i,4]
            team[team_name] = points
            
        ranking = sorted(team.items(),key=lambda item: item[1], reverse=True)
        ranked ={}

        rank = 1  # Start ranking from 1
        for key, value in ranking:
            ranked[key] = rank  # Assign the rank to the corresponding key
            rank += 1



        choice = col2.selectbox("Pick A Team",(df['Team Name']))

        choice = df[df['Team Name'] == choice]
        team = choice.iloc[0,0]
        df3 = pd.read_sql_query(f"SELECT * FROM game WHERE team_a = '{team}' OR  team_b = '{team}'", conn2)
        game_outcomes = col2.toggle("See Games Played")
        if game_outcomes:
            st.write("Games Played")
            st.dataframe(df3)

        rank = ranked[team] 

        wins = choice.iloc[0,2]
        losses = choice.iloc[0,3]
        ties = choice.iloc[0,4]
        sog = choice.iloc[0,5]
        ga = choice.iloc[0,6]
        pim = choice.iloc[0,7]
        sa = choice.iloc[0,8]

        st.header(f"#{rank} {team} ")

        col1, col2, col3 = st.columns(3)




        col1.metric("Wins",wins) 
        col2.metric("Ties",ties) 
        col3.metric("Losses",losses) 
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Shots on Goal",sog) 
        col2.metric("Goals Agaisnt",ga) 
        col3.metric("Penalty Minutes",pim) 
        col4.metric("Shots Agaisnt",sa) 

        #circle plt
        labels = ["Wins", "Ties","Losses"]
        sizes = [wins, ties, losses]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        row_height = 35  # Approximate height per row in pixels
        height = min(500, row_height * len(df))  # Max height of 500 pixels
        #st.pyplot(fig1)
        tab1, tab2= st.tabs(["Team View", "Player View"])
        df2 = pd.read_sql_query(f"SELECT * FROM '{team}'", conn)
        df2 = df2.drop(["team_name"], axis=1)

        df2 = df2[["position","number","player_name",
        
        
        "goal",
        "assist",
        "pim",
        
        "saves",
        "mip",
        "ga",
        "sa"
        ]]
        df2 = df2.rename(columns={"player_name":"Player Name", "goal": "Goals", "assist":"Assists" } )
        with tab1:
            st.dataframe(df2.sort_values('Goals', ascending=False), hide_index= True, use_container_width = True, height=550)
            
                
            
                

                
        with tab2:
            player = st.selectbox("Pick A Player",(df2['Player Name']), placeholder="Pick A Player")
            
            player_df = df2[df2['Player Name'] == player]
            st.header(f"#{player_df.iloc[0,1]} {player} {player_df.iloc[0,0]} ")
            #st.write(player_df)
            if player_df.iloc[0,0] == "G":
                gaa = round(((player_df.iloc[0,8]*45)/player_df.iloc[0,7]),2)
                svp = str(round((player_df.iloc[0,6]/player_df.iloc[0,9]*100),2)) + "%"
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Saves",player_df.iloc[0,6]) 
                col3.metric("Goals Agaisnt",int(player_df.iloc[0,8])) 
                col4.metric("Minutes Played",player_df.iloc[0,7]) 
                col2.metric("Shots Agaisnt",player_df.iloc[0,9]) 
                col1.metric("Save Percentage",  svp )
                col2.metric("Goals Agaisnt Average",gaa)
                col3.metric("Penalty Minutes",player_df.iloc[0,5]) 
            else:
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Goals",player_df.iloc[0,3]) 
                col2.metric("Assists",int(player_df.iloc[0,4])) 
                col3.metric("Points",int((player_df.iloc[0,3])+int(player_df.iloc[0,4])) ) 
                col4.metric("Penalty Minutes",player_df.iloc[0,5]) 
                

            
            

    # Connect to your database


    __ ="""
    col1, col2, col3, col4, col5 = st.columns(5)
        col1.write("Player Number")
        col2.write("Playe Name")
        col3.write("Goals")
        col4.write("Assists")
        col5.write("Penalty Minutes") 
        for i,y in enumerate(df2.iterrows()):
            col1, col2, col3, col4, col5  = st.columns(5)
            col1.text(df2.iloc[i][1])
            col2.write(df2.iloc[i][0])
            col3.text(df2.iloc[i][2])
            col4.text(df2.iloc[i][3])
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()


    # Search for the string in all columns of all tables
    search_string = '富士通RED BULLETS'
    for table in tables:
        table_name = table[0]
        cursor.execute(f'PRAGMA table_info("{table_name}")')
        columns = cursor.fetchall()
        for column in columns:
            column_name = column[1]
            query = f'SELECT * FROM "{table_name}" WHERE "{column_name}" LIKE ?'
            cursor.execute(query, ('%' + search_string + '%',))
            results = cursor.fetchall()
            if results:
                print(f"Found in table {table_name}, column {column_name}")
                print(results)

    conn.close()
    """