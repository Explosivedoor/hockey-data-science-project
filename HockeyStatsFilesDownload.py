
from tkinter import EXCEPTION   
import urllib.request
from bs4 import BeautifulSoup
import re
import wget
import csv

import sqlite3

# makes connection to database, and makes the table if it isn't there yet (though realisticlly that part isnt needed)
conn = sqlite3.connect('./KIHF.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS game (
        game_no TEXT PRIMARY KEY,
        team_a TEXT,
        team_a_score INTEGER,
        team_b  TEXT,
        team_b_score INTEGER,                 
        location TEXT,
        date TEXT       
    )
''')

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
#date format checking and game code checking for if statement below 
pattern = re.compile(r'^\d+/\d+$') #match strings like 12/23
pattern2 = re.compile(r'^\d+-\d+$') #match streings like 12-24
#opens and allows writing to CSV
csv_file_path = 'D:\\Downloads\\events-sample (1).csv' 
with open(csv_file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = list(reader)

#print(data)

##beautifulsoup setup##
#This is the docker webpage url because i don't want to constantly hit the real site when testing
url = 'http://192.168.1.8:32932/'
html = urllib.request.urlopen(url).read()
soup= BeautifulSoup(html,'html.parser')


tables = soup('table')

#finds all table rows in 7th table , which is the table on the page we need. 
tr = tables[6].find_all('tr')



#TODO add check using dic and game code 


#enumerate function helps get index, which is used when there are two games on the same day this is because the date and time are on a different index for ONLY those instances.  

for index, x in enumerate(tr,):
    print(f"Index {index}: {x}")
    x = x.find_all('td')
    
    #checks if first row is date or not by checking if it is a date and if it is a leauge game by checking for the formating x-y
    #try block is for when the game isn't over
    try:
        if pattern.match(x[0].text.strip()) and pattern2.match(x[4].text.strip()):
            
            try:
                print("Date and Time: ",  x[0].text.strip() + " " + x[1].text.strip()+ " "+ x[2].text.strip()+ " ")
                #this strips the score eg 1-2 4-7
                score = x[6].text.strip()
                team_a_score,team_b_score = score.split('-')
                #adds two spaces 
                data.append(' '+ ' ')
                #date formating
                m,d = x[0].text.strip().split('/')
                m = int(m)
                d = int(d)
                #as the year isn't listed, we need to add the year to the formating based on when the game occurs. 
                if m < 6 :
                    t = str(m) + "/" + str(d) + "/" +"2024" 
                    tdb = str(m) + "-" + str(d) + "-" +"2024"  
                else:
                    t = str(m) + "/" + str(d) + "/" +"2023" 
                    tdb = str(m) + "-" + str(d) + "-" +"2023"  

                """
                A little complicated 
                Date | Time | Location | Team A | A Score  
                (  ) | (  ) | (      ) | Team B | B Score 
                
                """
                data.append([t, x[2].text.strip(), x[3].text.strip(),x[5].text.strip(), team_a_score ])
                data.append(['', '', '', x[7].text.strip(),team_b_score])

                game_data = [
                    {'game_no': x[4].text.strip(), 'team_a': x[5].text.strip(), 'team_a_score': team_a_score, 'team_b': x[7].text.strip(), 'team_b_score': team_b_score, 'location': x[3].text.strip(), 'date': tdb},
                    
                    
                ]
                cursor.executemany('INSERT INTO game (game_no, team_a, team_a_score, team_b, team_b_score, location, date) VALUES (:game_no, :team_a, :team_a_score, :team_b, :team_b_score, :location, :date)', game_data)
                conn.commit()

                
                print("Place " + x[3].text.strip())
                print ("Game No. " + x[4].text.strip())
                print ("Home: " + x[5].text.strip() + " "+ "Away: " + x[7].text.strip() )
                print ("Final Score: " + x[6].text.strip())
                print("\n")
                
            except Exception as e:
                print(f"Error: {e}")
                pass
        
        elif  pattern2.match(x[2].text.strip()): 
            #because of the way the table is you have to go back 1 index to get the correct date. This else condition is for when there are two games on the same date, as the table row index changes by 1, prob a more simple way to do this but eh. 
            y = tr[index-1].find_all('td')
            q = y[1].text.strip()
            y = y[0].text.strip()
            
            try:
            # print(x[4].text.strip() + "test")
                
                print("Date and Time: ", y + " " + q + " " + x[0].text.strip()+ " ")
                m,d = y.split('/')
                m = int(m)
                d = int(d)
                #as the year isn't listed, we need to add the year to the formating based on when the game occurs. 
                if m < 6 :
                    t = str(m) + "/" + str(d) + "/" +"2024" 
                    tdb = str(m) + "-" + str(d) + "-" +"2024"  
                else:
                    t = str(m) + "/" + str(d) + "/" +"2023" 
                    tdb = str(m) + "-" + str(d) + "-" +"2023"
                o = x[4].text.strip()
                p,o = o.split('-')
                data.append(' '+ ' ')
                data.append([y, x[0].text.strip(), x[1].text.strip(),x[3].text.strip(), p ])
                data.append(['', '', '', x[5].text.strip(),o])
                            

                game_data = [
                    {'game_no': x[2].text.strip(), 'team_a': x[3].text.strip(), 'team_a_score': p, 'team_b': x[5].text.strip(), 'team_b_score': o, 'location': x[1].text.strip(), 'date': tdb},
                    
                    
                ]
                cursor.executemany('INSERT OR REPLACE INTO game (game_no, team_a, team_a_score, team_b, team_b_score, location, date) VALUES (:game_no, :team_a, :team_a_score, :team_b, :team_b_score, :location, :date)', game_data)
                conn.commit()



                #data[index+2][0] = y
                print("Place: " + x[1].text.strip())
                print ("Game No. " + x[2].text.strip())
                print ("Home: " + x[3].text.strip() + " "+ "Away: " + x[5].text.strip() )
                print ("Final Score: " + x[4].text.strip())
                print("\n")
            except Exception as e:
                print(f"Error: {e}")
                pass
        else:
            pass

    except Exception as e:
        print(f"Error: {e}")
        pass



with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(data)

conn.close()

#################################################################################################################
#now to get the game stats and program in forfit condition
#TODO 
conn = sqlite3.connect('./KIHF.db')
cursor = conn.cursor()
link_list = []
formatted_link_list = []
tags = soup('a')
for tag in tags:
     links= tag.get('href',None)
     
     
     
     link = re.findall('\\S+/files/71ks/[1-5].+',links)
    
     link_list.append(str(link))
     print(tag.get('href',None))
     
cursor.execute('''
    CREATE TABLE IF NOT EXISTS game_ids (
        id TEXT PRIMARY KEY    )
''')
conn.commit()

cursor.execute("SELECT * FROM game_ids")
game_ids = cursor.fetchall()
game_ids_list =[]
for i in game_ids:
    x= i[0] 
    game_ids_list.append(x)



print("GAME IDS:", game_ids_list)
#it makes the list of all of the links     
for x in link_list:
    formatted_link_list.append(x.replace("[","").replace("]","").replace("'",""))
formatted_link_list = ' '.join(formatted_link_list)
formatted_link_list = list(formatted_link_list.split())
print(formatted_link_list)



cursor.execute("SELECT * FROM game_ids")
myresult = cursor.fetchall()


for link in formatted_link_list:
    
    filename = re.findall('[1-5].+',link)
    databasename = re.findall('[1-5]-[0-9]+',link)
    
    filename = filename[0] if filename else ""
    
    databasename = databasename[0] if databasename else ""
    
    #this checks if it has already been downloaded
    if databasename not in game_ids_list:
        print( "file name" , str(filename))
        print("database name" , databasename)
        
        
        
        sql = "INSERT OR IGNORE INTO game_ids (id) VALUES (?)"
        
        val = (databasename,)   
        try:
            #this tries to commit the game number to the table, if it exsists it will throw an exception, 
            #then it will loop again, if no exception it will download.
            cursor.execute(sql, val)
            conn.commit()
        #this is the conversion function from PDF to text
            print('working')
            print(databasename)
            print(link)
            wget.download(link, './game_files' ) 

            
        #  list_df = tabula.read_pdf_with_template(
        #   input_path='D:\\Downloads\\Hockey\\'+ str(databasename).replace("[","").replace("]","").replace("'","")+'.pdf',
        #  template_path="D:\\Downloads\\Hockey\\template6.json",
        #   pages='all',encoding='cp1252'        
        # )
            
            #PASTE CODE HERE AFTER FIXING#######################################        

        
    

        #print("THIS IS IT", list_df[1].columns[1])
        #df = tabula.read_pdf_with_template( input_path='D:\\Downloads\\Hockey\\'+ str(databasename).replace("["","").replace("]","").replace("'","")+'.pdf', template_path= "D:\\Downloads\\Hockey\\KIHF-6-selc.json",  pages='all', encoding='ISO-8859-1')[0]
        #print(df)
        #tabula.convert_into('D:\\Downloads\\Hockey\\'+ str(databasename)+(".pdf"), 'D:\\Downloads\\Hockey\\'+str(databasename).replace("[","").replace("]","").replace("'","")+ ".csv", output_format="csv", pages='all')    
#download function
        except sqlite3.IntegrityError:
            continue
    #else:
    else:
        pass    



        #downloading and conversion working above up to line 248
        #not working is getting the marker for index for edge cases. Maybe just dont bother and write a log for edge casess 
    




#ughhhhhhhhhhhhhhhhh need to add the forfite condition to update KIHF table with win loss. That will be annowing. 
#TODO add check using dic and game code to skip  
