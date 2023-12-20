import socket
from tkinter import EXCEPTION   
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import shutil
import wget
import tabula
import csv
import codecs
import pandas
import sqlite3

# makes connection to database, and makes the table if it isn't there yet (though realisticlly that part isnt needed)
conn = sqlite3.connect('C:\\Users\\Johnny\\source\\repos\\Hockey program v2\\Hockey program v2\\KIHF.db')
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
pattern = re.compile(r'^\d+/\d+$')
pattern2 = re.compile(r'^\d+-\d+$')
#opens and allows writing to CSV
csv_file_path = 'D:\\Downloads\\events-sample (1).csv' 
with open(csv_file_path, 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = list(reader)

#print(data)

#beautifulsoup setup
url = 'http://kihf.net/detail.php?c=772'
html = urllib.request.urlopen(url).read()
soup= BeautifulSoup(html,'html.parser')


tablerow = soup.find_all('td',class_="xl789668")
tables = soup('table')

for td in tablerow:
    inner_content = td.text.strip()  # Use strip() to remove leading and trailing whitespaces
    #print(inner_content)

#finds all table rows in table 6, which is the table on the page we need. 
trww = tables[6].find_all('tr')
print(trww[2])



#todo add check using dic and game code 

tdw = trww[2].find_all('td')
#enumerate function helps get index, which is used when there are two games on the same day this is because the date and time are on a different index for ONLY those instances.  

for index, x in enumerate(trww,):
    print(f"Index {index}: {x}")
    x = x.find_all('td')
    
    #checks if first row is date or not by checking if it is a date and if it is a leauge game by checking for the formating x-y
    try:
        if pattern.match(x[0].text.strip()) and pattern2.match(x[4].text.strip()):
            
            try:
                print("Date and Time: ",  x[0].text.strip() + " " + x[1].text.strip()+ " "+ x[2].text.strip()+ " ")
                #this strips the score eg 1-2 4-7
                z = x[6].text.strip()
                y,z = z.split('-')
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
                data.append([t, x[2].text.strip(), x[3].text.strip(),x[5].text.strip(), y ])
                data.append(['', '', '', x[7].text.strip(),z])

                game_data = [
                    {'game_no': x[4].text.strip(), 'team_a': x[5].text.strip(), 'team_a_score': y, 'team_b': x[7].text.strip(), 'team_b_score': z, 'location': x[3].text.strip(), 'date': tdb},
                    
                    
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
            y = trww[index-1].find_all('td')
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
conn = sqlite3.connect('C:\\Users\\Johnny\\source\\repos\\Hockey program v2\\Hockey program v2\\KIHF2.db')
cursor = conn.cursor()
list2 = []
list3 = []
tags = soup('a')
for tag in tags:
     list1= tag.get('href',None)
     print(list1)
     #list1 = "http://kihf.net"+ list1
     print(list1)
     link = re.findall('\\S+/files/71ks/[1-5].+',list1)
     print(link)
     list2.append(str(link))
     print(tag.get('href',None))


#it makes the list of all of the links     
for x in list2:
    list3.append(x.replace("[","").replace("]","").replace("'",""))
list3 = ' '.join(list3)
list3 = list(list3.split())
print(list3)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        game TEXT PRIMARY KEY    )
''')
conn.commit()



for link in list3:
      
    filename = re.findall('[1-5].+',link)
    databasename = re.findall('[1-5]-[0-9]+',link)
    
    filename = filename[0] if filename else ""
    databasename = databasename[0] if databasename else ""
    print( "file name" , str(filename))
    print("database name" , databasename)
    
    cursor.execute("SELECT * FROM games")
    myresult = cursor.fetchall()
    print(myresult)
    
    sql = "INSERT OR IGNORE INTO games (game) VALUES (?)"
    val = (databasename,)   
    try:
        #this tries to commit the game number to the table, if it exsists it will throw an exception, 
        #then it will loop again, if no exception it will download.
        cursor.execute(sql, val)
        conn.commit()
    #this is the conversion function
        print('working')
        print(databasename)
        wget.download(link, 'D:\\Downloads\\Hockey\\' ) 
        df = tabula.read_pdf_with_template( input_path='D:\\Downloads\\Hockey\\'+ str(databasename).replace("[","").replace("]","").replace("'","")+'.pdf', template_path= "D:\\Downloads\\Hockey\\KIHF-6-selc.json",  pages='all', encoding='ISO-8859-1')[0]
        #print(df)
        tabula.convert_into('D:\\Downloads\\Hockey\\'+ str(databasename)+(".pdf"), 'D:\\Downloads\\Hockey\\'+str(databasename).replace("[","").replace("]","").replace("'","")+ ".csv", output_format="csv", pages='all')    
#download function
    except sqlite3.IntegrityError:
        continue
    #else:
        



        #downloading and conversion working above up to line 248
        #not working is getting the marker for index for edge cases. Maybe just dont bother and write a log for edge casess 