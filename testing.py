# -*- coding: utf-8 -*-
import sqlite3
import tabula
import pandas as pd
import re
#connects to database
conn = sqlite3.connect('C:\\Users\\Johnny\\source\\repos\\Hockey program v2\\Hockey program v2\\test.db')
cursor = conn.cursor()

list_df = tabula.read_pdf_with_template(
    input_path='D:\\Downloads\\Hockey\\2-11.pdf',
    template_path="D:\\Downloads\\Hockey\\template8.json",
    pages='all',        
)


for index, i in enumerate(list_df):
    print("INDEX IS: " , index, list_df[index])
 
#creates League database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "KIHF" (
        "division"  INTEGER,
        "team_name" TEXT UNIQUE,
        "goal"     INTEGER DEFAULT 0,
        "wins"      INTEGER DEFAULT 0,
        "losses"    INTEGER DEFAULT 0,
        "ties"      INTEGER DEFAULT 0,
        "sog"       INTEGER DEFAULT 0,
        "ga"        INTEGER DEFAULT 0,
        "pim"       INTEGER DEFAULT 0,
        "sa"        INTEGER DEFAULT 0
    )
''')
conn.commit()


#table creation naming
pattern2 = re.compile(r'^\d+-\d+$')      
if pattern2.match(list_df[0].columns[10]):
    game_no = list_df[0].columns[10]
else:
    game_no = list_df[0].columns[11]

div,game = game_no.split("-")

#create game table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "{}" (
        number INTEGER ,
        team_name TEXT,       
        goal INTEGER ,
        assist INTEGER,
        pim INTEGER,
        player_name TEXT,
        position TEXT,
        saves INTEGER,
        mip FLOAT,
        ga INTEGER,
        FOREIGN KEY (team_name) REFERENCES KIHF(team_name)       
    )
'''.format(game_no))

conn.commit()

team_a_name = list_df[1].columns[1]
team_b_name = list_df[10].columns[1]
cursor.execute('''
    INSERT OR IGNORE INTO KIHF (division,team_name)
    VALUES (?,?)
''',(div,team_a_name,))
conn.commit()
cursor.execute('''
    INSERT OR IGNORE INTO KIHF (division,team_name)
    VALUES (?,?)
''',(div,team_b_name,))
conn.commit()
print(team_a_name)
#adding team tables 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "{}" (     
        player_name TEXT,
        number INTEGER UNIQUE,
        goal INTEGER DEFAULT 0,
        assist INTEGER DEFAULT 0,
        pim INTEGER DEFAULT 0,
        position TEXT,
        saves INTEGER DEFAULT 0,
        mip FLOAT DEFAULT 0,
        ga INTEGER DEFAULT 0,
        sa INTEGER DEFAULT 0,
        team_name TEXT DEFAULT  "{}",         
        FOREIGN KEY (team_name) REFERENCES KIHF(team_name)             
    )
'''.format(team_a_name, team_a_name))
conn.commit()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "{}" (
        player_name TEXT,
        number INTEGER UNIQUE,
        goal INTEGER DEFAULT 0,
        assist INTEGER DEFAULT 0,
        pim INTEGER DEFAULT 0,
        position TEXT,
        saves INTEGER DEFAULT 0,
        mip FLOAT DEFAULT 0,
        ga INTEGER DEFAULT 0,
        sa INTEGER DEFAULT 0,
        team_name TEXT DEFAULT  "{}",     
        FOREIGN KEY (team_name) REFERENCES KIHF(team_name)         
    )
'''.format(team_b_name, team_b_name))
conn.commit()
##########################################################################################################################################################################
''''''
#Adding Players to tables 
print("HERE", team_a_name)
print(pd.isna(list_df[2].iat[0, 1]))
#goals and assists, drops empty rows for processing
team_a_ga = list_df[3].dropna()
team_a_roster = list_df[2]
#adds players on the scoresheet to the database
for y in range(len(team_a_roster) ):
    
    #edge case detection for team A
    if pd.isna(list_df[2].iat[0, 1]) or list_df[2].iat[0, 1] in ["(C)", "(A)"]:
        #try is here because this can t
        try:
            player = list_df[2].iat[y, 0]
            print("BREAKS HERE:", player)
            player = player.replace("V", '',).replace("T", '',1).replace("F", '',1).strip()
            
            player, player_name = player.split(" ",1) 
            position = team_a_roster.iat[y, 2]
            #sometimes tabula mistakes D for 0
            if position == "0" or 0 : 
                position = 'D'
            cursor.execute('''
                            INSERT INTO"{}"  (number, team_name, goal, assist, pim, player_name, position)
                            VALUES (?,?,0,0,0,?,?)
                            
                        '''.format(game_no), (player,team_a_name ,player_name,position,))
            #adds players to their team tables if they havent been added before. This is more for automation because I dont want to make the tables manually
            cursor.execute('''
                            INSERT OR IGNORE INTO  "{}"  (number, team_name, player_name, position)
                            VALUES (?,?,?,?)
                            
                        '''.format(team_a_name), (player,team_a_name ,player_name,position,))
            conn.commit()
            print(player, player_name,position)
        except:
            continue


     #Normal Condition for A 
    else: 
        player = team_a_roster.iat[y, 1]
        player_name = team_a_roster.iat[y, 2]
        try:
            position = team_a_roster.iat[y, 3]
            #sometimes tabula mistakes D for 0
            if position == "0" or 0 : 
                position = 'D'
            player = int(player)
            print("PssssNAME", player_name)
            #replaces V (which is in there for some reason) and replaces it, strips out white space. Next  remove captian and assistant captian marks 
            player_name = player_name.replace("V", '').strip()
            player_name = player_name.replace("(C)", '').strip()
            player_name = player_name.replace("T", '').strip()
            player_name = player_name.replace("(A)", '').strip()
            print("NAME A",player_name)
            cursor.execute('''
                        INSERT INTO "{}"  (number, team_name, goal, assist, pim, player_name, position)
                        VALUES (?,?,0,0,0,?,?)
                        
                    '''.format(game_no), (player,team_a_name ,player_name,position,))
            #adds players to their team tables if they havent been added before. This is more for automation because I dont want to make the tables manually
            cursor.execute('''
                        INSERT OR IGNORE INTO  "{}"  (number, team_name, player_name, position)
                        VALUES (?,?,?,?)
                        
                    '''.format(team_a_name), (player,team_a_name ,player_name,position,))
            conn.commit()
        except Exception as e:
            print(e)
            continue
   
        







print(team_b_name)
#goals and assists, drops empty rows for processing
team_b_ga = list_df[8].dropna()
print("ga", team_b_ga)
team_b_roster = list_df[9]

#adds players on the scoresheet to the game table and team table
print(list_df[9].iat[0, 1]) 
for y in range(len(team_b_roster) ):
    if pd.isna(list_df[9].iat[0, 1]) or list_df[2].iat[0, 1] in ["(C)", "(A)"]:
        player = list_df[9].iat[y, 0]
        player = player.replace("V", '',).replace("T", '',1).replace("F", '',1).strip()
        player, player_name = player.split(" ",1) 
        position = team_b_roster.iat[y, 2]
        #sometimes tabula mistakes D for 0
        if position == "0" or 0 : 
            position = 'D'
        cursor.execute('''
                        INSERT INTO "{}" (number, team_name, goal, assist, pim, player_name, position)
                        VALUES (?,?,0,0,0,?,?)
                        
                    '''.format(game_no), (player,team_b_name ,player_name,position,))
        cursor.execute('''
                        INSERT OR IGNORE INTO  "{}"  (number, team_name, player_name, position)
                        VALUES (?,?,?,?)
                        
                    '''.format(team_b_name), (player,team_b_name ,player_name,position,))
        conn.commit()
        print("BREEEEEE",player, player_name,position)
    else:    
        player = team_b_roster.iat[y, 0]
        player_name = team_b_roster.iat[y, 1]
        
        try:
            position = team_b_roster.iat[y, 2]
            #sometimes tabula mistakes D for 0
            if position == "0" or 0 : 
                position = 'D'
            player = int(player)
            #replaces V (which is in there for some reason) and replaces it, strips out white space. Next  remove captian and assistant captian marks 
            player_name = player_name.replace("V", '').strip()
            player_name = player_name.replace("T", '').strip()
            player_name = player_name.replace("(C)", '').strip()
            player_name = player_name.replace("(A)", '').strip()
            print("BREEEEEE",player," ", player_name," ",position)
            cursor.execute('''
                        INSERT INTO "{}"  (number, team_name, goal, assist, pim, player_name, position)
                        VALUES (?,?,0,0,0,?,?)
                        
                    '''.format(game_no), (player,team_b_name,player_name,position,))
            #adds players to their team tables if they havent been added before. This is more for automation because I dont want to make the tables manually
            cursor.execute('''
                        INSERT OR IGNORE INTO  "{}"  (number, team_name,goal, player_name, position)
                        VALUES (?,?,0,?,?)
                        
                    '''.format(team_b_name), (player,team_b_name ,player_name,position,))
            conn.commit()
        except Exception as e:
            print(e)
            continue


########################################################################################################################################################
#adding assists and goals to the tables   
for x in range(1, len(team_a_ga)):
    
    
    try:
        
        print(team_a_ga.iat[x, 1])
        #goal
        cursor.execute('''
                UPDATE "{}" 
                SET goal = goal + 1
                WHERE number = ? AND team_name = ?
            '''.format(game_no), (team_a_ga.iat[x, 1],team_a_name,))
        conn.commit()
        #goal into team table
        cursor.execute('''
                UPDATE "{}" 
                SET goal = goal + 1
                WHERE number = ? 
            '''.format(team_a_name), (team_a_ga.iat[x, 1],))
        conn.commit()
        # These are in the same try block because if there is only 1 assist the next execute will fail and just continue but the first was already commited so its fine.
        #assist 1 
        try:
            
            
            cursor.execute('''
                UPDATE "{}" 
                SET assist = assist + 1
                WHERE number = ? AND team_name = ?
            '''.format(game_no), (team_a_ga.iat[x, 2],team_a_name,))
            conn.commit()
            cursor.execute('''
                UPDATE "{}" 
                SET assist = assist + 1
                WHERE number = ? 
            '''.format(team_a_name), (team_a_ga.iat[x, 2],))
            conn.commit()
            
            #assist 2
            cursor.execute('''
                UPDATE "{}" 
                SET assist = assist + 1
                WHERE number = ? AND team_name = ?
            '''.format(game_no), (team_a_ga.iat[x, 3],team_a_name,))
            conn.commit()
            cursor.execute('''
                UPDATE "{}" 
                SET assist = assist + 1
                WHERE number = ? 
            '''.format(team_a_name), (team_a_ga.iat[x, 3],))
            conn.commit()    



        except:
            continue
    except Exception as a:
        print(a)
        pass




#below is same as above but for team B

team_b_name = list_df[10].columns[1]
team_b_ga = list_df[8].dropna()
print("\n")
for x in range(1,len(team_b_ga)):
    try:
        

    
        cursor.execute('''
                UPDATE "{}" 
                SET goal = goal + 1
                WHERE number = ? AND team_name = ?
            '''.format(game_no), (team_b_ga.iat[x, 1],team_b_name,))
        conn.commit()
        cursor.execute('''
                UPDATE "{}" 
                SET goal = goal + 1
                WHERE number = ? 
            '''.format(team_b_name), (team_b_ga.iat[x, 1],))
        conn.commit()


        try:
            
            
            cursor.execute('''
                UPDATE "{}" 
                SET assist = assist + 1
                WHERE number = ? AND team_name = ?
            '''.format(game_no), (team_b_ga.iat[x, 2],team_b_name,))
            conn.commit()
            cursor.execute('''
                UPDATE "{}" 
                SET assist = assist + 1
                WHERE number = ? 
            '''.format(team_b_name), (team_b_ga.iat[x, 2],))
            conn.commit()
            
            
            cursor.execute('''
                UPDATE "{}" 
                SET assist = assist + 1
                WHERE number = ? AND team_name = ?
            '''.format(game_no), (team_b_ga.iat[x, 3],team_b_name,))
            conn.commit()
            cursor.execute('''
                UPDATE "{}" 
                SET assist = assist + 1
                WHERE number = ? 
            '''.format(team_b_name), (team_b_ga.iat[x, 3],))
            conn.commit()



        except:
            continue
    except Exception as a:
        print(a)
        pass
    print("TEAM B: ")
    
    try:
        print("goal:", team_b_ga.iat[x, 1], "A1:", team_b_ga.iat[x, 2], "A2:", team_b_ga.iat[x, 3])
    except Exception as a:
        print(a)
        pass




########################################################################################################################################################
#GOALIE STATS SECTION

# this function cleans data for cells with A:B, for some reason tabula breaks it and has extra whitespace characters in there
def clean_data(cell):
    cell1,cell2 = re.sub(r'\s+', '', cell).strip().split(":")
    return int(cell1), int(cell2)
def clean_data2(cell):
    cell1,cell2 = re.sub(r'\s+', '', cell).strip().split(":")
    return cell1,cell2

def get_sec(time_str):
    """Get seconds from time."""
    m, s = time_str.split(':')
    return 3600 + int(m) * 60 + int(s)







#use map int on mip 







#GKA1
gka1_saves = int(list_df[13].iat[5, 0])
gka1_number = int(list_df[12].iat[0, 0])
gka1_mip,y = list_df[12].iat[0, 1].split(":")
gka1_ga = int(list_df[12].iat[0, 2])
gka1_mip = int(gka1_mip)
gka1_sa = gka1_saves + gka1_ga
print("SA", gka1_sa)
#add GKA1 stats to game table
cursor.execute('''
    UPDATE "{}"
    SET saves = ?,
        mip = ?,
        ga = ?
    WHERE number = ? AND team_name = ?
'''.format(game_no), (gka1_saves, gka1_mip, gka1_ga, gka1_number, team_a_name))
conn.commit()

#adds to team table
cursor.execute('''
    UPDATE "{}"
    SET saves = saves + ?,
        mip = mip +  ?,
        ga = ga + ?,
        sa = sa + ?
    WHERE number = ? 
'''.format(team_a_name), (gka1_saves, gka1_mip, gka1_ga,gka1_sa,gka1_number))
conn.commit()  




try:
#GKA2 wrapped in try block becuase there isn't always a second goalie
    gka2_saves = int(list_df[13].iat[5, 1])
    
    gka2_number = int(list_df[12].iat[1, 0])
    
    gka2_mip,y = list_df[12].iat[1, 1].split(":")
    gka2_ga = int(list_df[12].iat[1, 2])
    gka2_mip = int(gka2_mip)
    gka2_sa = gka2_saves + gka2_ga
    #print(gka2_number, " " ,gka2_mip , gka2_saves )
    cursor.execute('''
        UPDATE "{}"
        SET saves = ?,
            mip = ?,
            ga = ?
        WHERE number = ? AND team_name = ?
    '''.format(game_no), (gka2_saves, gka2_mip, gka2_ga, gka2_number, team_a_name))
    cursor.execute('''
    UPDATE "{}"
    SET saves = saves + ?,
        mip = mip +  ?,
        ga = ga + ?,
        sa = sa + ?
    WHERE number = ? 
'''.format(team_a_name), (gka2_saves, gka2_mip, gka2_ga,gka2_sa,gka2_number))

except Exception as e:
    pass

#GKB1
gkb1_saves = int(list_df[13].iat[5, 2])
#another try block for another edge case where the sheet is filled out incorrectly
try:
    gkb1_number = int(list_df[12].iat[0, 3])
except:
    gkb1_number = int(list_df[12].iat[1, 3])
gkb1_mip,y = list_df[12].iat[0, 4].split(":")
gkb1_ga = int(list_df[12].iat[0, 5])
gkb1_mip = int(gkb1_mip)
gkb1_sa = gkb1_saves + gkb1_ga

cursor.execute('''
    UPDATE "{}"
    SET saves = ?,
        mip = ?,
        ga = ?
    WHERE number = ? AND team_name = ?
    '''.format(game_no), (gkb1_saves, gkb1_mip, gkb1_ga, gkb1_number,team_b_name, ))
conn.commit()
#adds to team table
cursor.execute('''
    UPDATE "{}"
    SET saves = saves + ?,
        mip = mip +  ?,
        ga = ga + ?,
        sa = sa + ?
    WHERE number = ? 
'''.format(team_b_name), (gkb1_saves, gkb1_mip, gkb1_ga,gkb1_sa,gkb1_number))
conn.commit()  




try:
#GKB2 
#GKB2 wrapped in try block becuase there isn't always a second goalie
   
#GKB2
    gkb2_saves = int(list_df[13].iat[5, 3])
    gkb2_number = int(list_df[12].iat[1, 3])
    gkb2_mip,y = list_df[12].iat[1, 4].split(":")
    gkb2_ga = int(list_df[12].iat[1, 5])
    gkb2_mip = int(gkb2_mip)
    gkb2_sa = gkb2_saves + gkb2_ga


    cursor.execute('''
        UPDATE "{}"
        SET saves = ?,
            mip = ?,
            ga = ?
        WHERE number = ? AND team_name = ?
    '''.format(game_no), (gkb2_saves, gkb2_mip, gkb2_ga, gkb2_number, team_b_name,))
    cursor.execute('''
    UPDATE "{}"
    SET saves = saves + ?,
        mip = mip +  ?,
        ga = ga + ?,
        sa = sa + ?
    WHERE number = ? 
    '''.format(team_b_name), (gkb2_saves, gkb2_mip, gkb2_ga,gkb2_sa,gkb2_number))
    conn.commit()      

    
except Exception as e:
    print(e)








######################################################################################
#penalties section
#team A    
for x in range(1, len(list_df[5].dropna())):
    #this try block is here only because they sometimes forget to put in penalty times, this is an edge case that case up. Prob better ways to deal with this but it will be skiped for now
    try:
        if str(list_df[5].dropna().iat[x, 1]).startswith("T"):
            #add to team PIM not to player here todo
            
            continue
        
        else:
            pen_player  = list_df[5].dropna().iat[x, 1]
            pen_time  = list_df[5].dropna().iat[x, 2]
            
            cursor.execute('''
            UPDATE "{}"
            SET pim = pim + {}
            WHERE number = ?  AND team_name = ?
        '''.format(game_no, pen_time), (pen_player,team_a_name,))
            conn.commit()
            cursor.execute('''
            UPDATE "{}"
            SET pim = pim + {}
            WHERE number = ?  
        '''.format(team_a_name, pen_time), (pen_player,))
            conn.commit()
    except:
        continue
    
#Where there is a bench minor the number with start with T, sould be just added to team PIM 
#team B
for x in range(len(list_df[6].dropna())):
    try:
        if str(list_df[6].dropna().iat[x, 1]).startswith("T"):
            #add to team PIM not to player here todo
            
            continue
        else:
            pen_player = int(list_df[6].dropna().iat[x, 1])
            pen_time = int(list_df[6].dropna().iat[x, 2])
            
            cursor.execute('''
            UPDATE "{}"
            SET pim = pim + {}
            WHERE number = ?  AND team_name = ?
        '''.format(game_no, pen_time), (pen_player, team_b_name,))
            conn.commit()
            cursor.execute('''
            UPDATE "{}"
            SET pim = pim + {}
            WHERE number = ? 
        '''.format(team_b_name, pen_time), (pen_player,))
            conn.commit()
    except:
        continue
        
######################################################################################    
#KIHF table update section
#todo add edge case where numbers could be messed up    
try: 
    
    team_a_goals, team_b_goals = clean_data(list_df[14].iat[9,2])
    team_a_sog, team_b_sog = clean_data(list_df[14].iat[9,3])
    team_a_pim, team_b_pim =  clean_data(list_df[14].iat[9,4])
    team_b_sa, team_a_sa = clean_data(list_df[14].iat[9,3])    
    team_b_ga, team_a_ga = clean_data(list_df[14].iat[9,2])
except:
    team_a_goals, team_b_goals = clean_data(list_df[14].iat[6,2])
    team_a_sog, team_b_sog = clean_data(list_df[14].iat[6,3])
    team_a_pim, team_b_pim =  clean_data(list_df[14].iat[6,4])
    team_b_sa, team_a_sa = clean_data(list_df[14].iat[6,3])    
    team_b_ga, team_a_ga = clean_data(list_df[14].iat[6,2])
    


#just setting the variables to zero before if statment 

team_a_win,team_b_win,team_a_loss,team_b_loss,team_a_tie,team_b_tie = 0,0,0,0,0,0

if team_a_goals > team_b_goals:
    team_a_win = 1
    team_b_loss = 1
elif team_a_goals < team_b_goals:
    team_b_win = 1
    team_a_loss = 1
else:
    team_a_tie = 1 
    team_b_tie = 1

cursor.execute('''
    UPDATE "KIHF"
    SET goal = goal + ?, 
        sog = sog + ?,
        ga = ga + ?,
        pim = pim + ?,
        sa = sa + ?,
        wins = wins + ?,
        losses = losses +?,
        ties = ties +?
    WHERE team_name = ?
''', (team_a_goals, team_a_sog, team_a_ga, team_a_pim, team_a_sa,team_a_win,team_a_loss,team_a_tie, team_a_name))
conn.commit()
cursor.execute('''
    UPDATE "KIHF"
    SET goal = goal + ?, 
        sog = sog + ?,
        ga = ga + ?,
        pim = pim + ?,
        sa = sa + ?,
        wins = wins + ?,
        losses = losses +?,
        ties = ties + ?
    WHERE team_name = ?
''', (team_b_goals, team_b_sog, team_b_ga, team_b_pim, team_b_sa,team_b_win,team_b_loss,team_b_tie, team_b_name))
conn.commit()

#goalie table?

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



