# -*- coding: utf-8 -*-
import sqlite3
import tabula
import pandas as pd
import re
#connects to database
conn = sqlite3.connect('C:\\Users\\Johnny\\source\\repos\\Hockey program v2\\Hockey program v2\\test.db')
cursor = conn.cursor()

list_df = tabula.read_pdf_with_template(
    input_path='D:\\Downloads\\Hockey\\1-2.pdf',
    template_path="D:\\Downloads\\Hockey\\template6.json",
    pages='all',
    
    
)


for index, i in enumerate(list_df):
    print("INDEX IS: " , index, list_df[index])
    




#table creation naming
pattern2 = re.compile(r'^\d+-\d+$')      
if pattern2.match(list_df[0].columns[10]):
    game_no = list_df[0].columns[10]
else:
    game_no = list_df[0].columns[11]


#create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "{}" (
        number INTEGER,
        team_name TEXT,       
        Goal INTEGER ,
        Assist INTEGER,
        pim INTEGER,
        player_name TEXT,
        position TEXT,
        saves INTEGER,
        mip FLOAT,
        ga INTEGER       
    )
'''.format(game_no))

conn.commit()


########################################################################################################################################################
''''''
team_a_name = list_df[1].columns[1]
print("HERE", team_a_name)
print(pd.isna(list_df[2].iat[0, 1]))
#goals and assists, drops empty rows for processing
team_a_ga = list_df[3].dropna()
team_a_roster = list_df[2]
#adds players on the scoresheet to the database
for y in range(len(team_a_roster) ):
    
    #edge case detection for team A
    if pd.isna(list_df[2].iat[0, 1]) or list_df[2].iat[0, 1] in ["(C)", "(A)"]:
        player = list_df[2].iat[y, 0]
        player = player.replace("V", '',).replace("T", '',1).replace("F", '',1).strip()
        player, player_name = player.split(" ",1) 
        position = team_a_roster.iat[y, 2]
        cursor.execute('''
                        INSERT INTO"{}"  (number, team_name, Goal, Assist, pim, player_name, position)
                        VALUES (?,?,0,0,0,?,?)
                        
                    '''.format(game_no), (player,team_a_name ,player_name,position,))
        conn.commit()
        print(player, player_name,position)


     #Normal Condition for A 
    else: 
        player = team_a_roster.iat[y, 1]
        player_name = team_a_roster.iat[y, 2]
        try:
            position = team_a_roster.iat[y, 3]
            player = int(player)
            print("PssssNAME", player_name)
            #replaces V (which is in there for some reason) and replaces it, strips out white space. Next  remove captian and assistant captian marks 
            player_name = player_name.replace("V", '').strip()
            player_name = player_name.replace("(C)", '').strip()
            player_name = player_name.replace("T", '').strip()
            player_name = player_name.replace("(A)", '').strip()
            print("NAME A",player_name)
            cursor.execute('''
                        INSERT INTO "{}"  (number, team_name, Goal, Assist, pim, player_name, position)
                        VALUES (?,?,0,0,0,?,?)
                        
                    '''.format(game_no), (player,team_a_name ,player_name,position,))
            conn.commit()
        except Exception as e:
            print(e)
            continue
   
        






team_b_name = list_df[10].columns[1]
print(team_b_name)
#goals and assists, drops empty rows for processing
team_b_ga = list_df[8].dropna()
print("ga", team_b_ga)
team_b_roster = list_df[9]

#adds players on the scoresheet to the database
print(list_df[9].iat[0, 1]) 
for y in range(len(team_b_roster) ):
    if pd.isna(list_df[9].iat[0, 1]) or list_df[2].iat[0, 1] in ["(C)", "(A)"]:
        player = list_df[9].iat[y, 0]
        player = player.replace("V", '',).replace("T", '',1).replace("F", '',1).strip()
        player, player_name = player.split(" ",1) 
        position = team_b_roster.iat[y, 2]
        cursor.execute('''
                        INSERT INTO "{}" (number, team_name, Goal, Assist, pim, player_name, position)
                        VALUES (?,?,0,0,0,?,?)
                        
                    '''.format(game_no), (player,team_b_name ,player_name,position,))
        conn.commit()
        print("BREEEEEE",player, player_name,position)
    else:    
        player = team_b_roster.iat[y, 0]
        player_name = team_b_roster.iat[y, 1]
        
        try:
            position = team_b_roster.iat[y, 2]
            
            player = int(player)
            #replaces V (which is in there for some reason) and replaces it, strips out white space. Next  remove captian and assistant captian marks 
            player_name = player_name.replace("V", '').strip()
            player_name = player_name.replace("T", '').strip()
            player_name = player_name.replace("(C)", '').strip()
            player_name = player_name.replace("(A)", '').strip()
            print("BREEEEEE",player," ", player_name," ",position)
            cursor.execute('''
                        INSERT INTO "{}"  (number, team_name, Goal, Assist, pim, player_name, position)
                        VALUES (?,?,0,0,0,?,?)
                        
                    '''.format(game_no), (player,team_b_name,player_name,position,))
            conn.commit()
        except Exception as e:
            print(e)
            continue


########################################################################################################################################################
#doto add where = ?    
print(team_a_ga.iat[1, 2])
for x in range(1, len(team_a_ga)):
    
    
    try:
        

    
        cursor.execute('''
                UPDATE "{}" 
                SET Goal = Goal + 1
                WHERE number = ? AND team_name = ?
            '''.format(game_no), (team_a_ga.iat[x, 1],team_a_name,))
        conn.commit()



        try:
            
            
            cursor.execute('''
                UPDATE "{}" 
                SET Assist = Assist + 1
                WHERE number = ? AND team_name = ?
            '''.format(game_no), (team_a_ga.iat[x, 2],team_a_name,))
            conn.commit()

            
            
            cursor.execute('''
                UPDATE "{}" 
                SET Assist = Assist + 1
                WHERE number = ? AND team_name = ?
            '''.format(game_no), (team_a_ga.iat[x, 3],team_a_name,))
            conn.commit()




        except:
            continue
    except Exception as a:
        print(a)
        pass




"""      
##above needs to be done below for team b it seems. 

team_b_name = list_df[10].columns[1]
team_b_ga = list_df[8].dropna()
print("\n")
for x in range(1,len(team_b_ga)):
    
    print("TEAM B: ")
    
    try:
        print("Goal:", team_b_ga.iat[x, 1], "A1:", team_b_ga.iat[x, 2], "A2:", team_b_ga.iat[x, 3])
    except Exception as a:
        print(a)
        pass


"""

########################################################################################################################################################
#GOALIE STATS SECTION
# needs to get to database

# this function cleans data for cells with A:B, for some reason tabula breaks it and has extra whitespace characters in there
def clean_data(cell):
    cell1,cell2 = re.sub(r'\s+', '', cell).strip().split(":")
    return cell1,cell2

def get_sec(time_str):
    """Get seconds from time."""
    m, s = time_str.split(':')
    return 3600 + int(m) * 60 + int(s)

shots_a,shots_b  = clean_data(list_df[14].iat[6, 3])
print("SHOTS A ", shots_a, " SHOTS B ", shots_b)





#use map int on mip 
#GKA1
gka1_saves = int(list_df[13].iat[5, 0])
gka1_number = int(list_df[12].iat[0, 0])
gka1_mip,y = list_df[12].iat[0, 1].split(":")
gka1_ga = int(list_df[12].iat[0, 2])
gka1_mip = int(gka1_mip)
try:
#GKA2
    gka2_saves = int(list_df[13].iat[5, 1])
    gka2_number = int(list_df[12].iat[1, 0])
    gka2_mip,y = list_df[12].iat[1, 1].split(":")
    gka2_ga = int(list_df[12].iat[1, 2])
    gka2_mip = int(gka2_mip)
except:
    pass
#GKB1
gkb1_saves = int(list_df[13].iat[5, 2])
gkb1_number = int(list_df[12].iat[0, 3])
gkb1_mip,y = list_df[12].iat[0, 4].split(":")
gkb1_ga = int(list_df[12].iat[0, 5])
gkb1_mip = int(gkb1_mip)
try:
#GKB2
    gkb2_saves = int(list_df[13].iat[5, 3])
    gka2_number = int(list_df[12].iat[1, 3])
    gka2_mip,y = list_df[12].iat[1, 4].split(":")
    gka2_ga = int(list_df[12].iat[1, 5])
    gka2_mip = int(gka2_mip)
except:
    pass


print(team_b_name, " ", gkb1_number, " ", gkb1_saves)




try:
    cursor.execute('''
    UPDATE "{}"
    SET saves = ?,
        mip = ?,
        ga = ?
    WHERE number = ? AND team_name = ?
'''.format(game_no), (gka1_saves, gka1_mip, gka1_ga, gka1_number, team_a_name))

    conn.commit()
except Exception as e:
    print(e)  



try:
    cursor.execute('''
    UPDATE "{}"
    SET saves = ?,
        mip = ?,
        ga = ?
    WHERE number = ? 
'''.format(game_no), (gkb1_saves, gkb1_mip, gkb1_ga, gkb1_number))

    conn.commit()
except Exception as e:
    print(e)



######################################################################################
#penalties section
for x in range(1, len(list_df[5].dropna())):
    pen_player  = list_df[5].dropna().iat[x, 1]
    pen_time  = list_df[5].dropna().iat[x, 2]
    
    cursor.execute('''
    UPDATE "{}"
    SET pim = pim + {}
    WHERE number = ?  AND team_name = ?
'''.format(game_no, pen_time), (pen_player,team_a_name,))
    conn.commit()
    

for x in range(len(list_df[6].dropna())):
      
    pen_player = int(list_df[6].dropna().iat[x, 1])
    pen_time = int(list_df[6].dropna().iat[x, 2])
    
    cursor.execute('''
    UPDATE "{}"
    SET pim = pim + {}
    WHERE number = ?  AND team_name = ?
'''.format(game_no, pen_time), (pen_player, team_b_name,))
    conn.commit()
######################################################################################    
    






#todo team b needs goals and assists, GKA2 GKB1 GKB2 need their stats to database and need to fix goals section 
    

###############################below is getting teamdatabases up and running############################################
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "{}" (
        team_name TEXT PRIMARY KEY,     
        goals INTEGER ,
        assists INTEGER,
        pim INTEGER,
        player_name TEXT,
        position TEXT,
        saves INTEGER,
        mip FLOAT,
        ga INTEGER,
        wins INTEGER, 
        sog INTEGER,
        loss INTEGER,
        tie INTEGER,
        points INTEGER     
    )
'''.format(team_a_name))

cursor.execute('''
    CREATE TABLE IF NOT EXISTS "{}" (
        team_name TEXT PRIMARY KEY,     
        goals INTEGER ,
        assists INTEGER,
        pim INTEGER,
        player_name TEXT,
        position TEXT,
        saves INTEGER,
        mip FLOAT,
        ga INTEGER,
        wins INTEGER, 
        sog INTEGER,
        loss INTEGER.
        tie INTEGER,
        points INTEGER     
    )
'''.format(team_b_name))


"""
#you can write it like this instead
cursor.execute(f'''
    INSERT INTO "{team_a_name}" (
        team_name, goals, assists, pim, player_name, position, saves, mip, ga, wins, sog
    ) VALUES (
        'Team A', 0, 0, 0, 'Player 1', 'Forward', 0, 0.0, 0, 0, 0
    )
''')
"""



