#imports
import sqlite3

#--------------------------------------------------
#all the functions that insert data in the database
#-------------------------------------------------

#executes the databse statements
def execute(test):

    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute(test)
    conn.commit()
    conn.close()


#sets the database
def setDatabase():
   #table that contains all players that played in the nba
    execute("""CREATE TABLE players (       
                id integer, 
                name text,
                downloaded bool          
    )""")

    #table that contains all the game stats
    execute("""CREATE TABLE games (       
                id integer, 
                points integer,
                assists integer,
                rebounds integer,
                steals integer,
                blocks integer,
                fg3a integer,
                fg3m integer,
                fga integer,
                fgm integer,
                fta integer,
                ftm integer,
                season text,
                date text          
    )""")


#inserts game Data from a player
def insertData(player_id,pts,ast,rebs,stl,blocks,fg3a,fg3m,fga,fgm,fta,ftm,season,time):

    #intercept wrong data from the api call and writes data in database in table 'games'
    if pts is not None:
        insert=(f'INSERT INTO "games" VALUES ("{player_id}","{pts}","{ast}","{rebs}","{stl}","{blocks}","{fg3a}","{fg3m}","{fga}","{fgm}","{fta}","{ftm}","{season}","{time}")')
        execute(insert)

        return True
    
    return False 

  
#insert playes in database in table 'players'
def insertPlayers(id,name):
    insert=(f'INSERT INTO "players" VALUES ("{id}","{name}",0)')
    execute(insert)
    



#is called when a player is donwloaded and sets the value to 1 -> means player is downloaded
def setDownloaded(player_id):
    updatedData = f"UPDATE players SET downloaded = 1 WHERE id = {player_id}"
    execute(updatedData)  
    

#can delelte rows of tables
#is used in test 
def delete(table,id):
    insert = f"DELETE  FROM '{table}' WHERE id = {id}"
    execute(insert)  
    return True
    

 
