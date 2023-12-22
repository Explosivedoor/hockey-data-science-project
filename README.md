# hockey-data-science-project

To start off the data extraction for the pdfs using tabula was very inconsistant, resulting in a LOT of extra code, and non-reusable code, to combat the edge cases and different formating. 
For example, for two tables that should be the same, one table would start the data at row 0 and the other at row 1. Another example about those specific tables is the numbers in one were intergers and floats in the other. 

# Function of the project 
This project is pretty complex (for me at least) in the future I will illusrate below to give a better understanding. For now though, I will explain in the best way I can. This project first scrapes a website for information about a hockey leauge's schedule and current game results. It takes that information and writes into a CSV with proper formating, to upload on to a second site, which uses SportsPress (in the future this will hopfully be updated to use a REST api to update SportsPress). The next part of the program finds all links to completed games' scoresheets in PDF format and downloads them. It checks to see if they have already been downloaded, skips those that have. The data from those PDF scoresheets are then extracted using tabula into dataframes. These dataframes are manipulated to extract the stats for each game (eg. Goals, Assits, Roster, etc.). The manipulated data is also placed into a SQlite database, with each game being its own table in the database. Finally (and still currently a work in progress) the database will be used to update SportsPress with the statistics. 

# Below is an example of the scoresheet
![ice hockey scoresheet](https://github.com/Explosivedoor/hockey-data-science-project/blob/main/docs/5-1.jpg?raw?=true)
