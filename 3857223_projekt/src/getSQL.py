#imports
import sqlite3
import pandas as pd

#--------------------------------------------------
#all the functions that get data from the database
#-------------------------------------------------


#executes the databse statements
def execute(test):

    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    c.execute(test)
    conn.commit()
    conn.close()


#get the season average from both players in the selected stat (points, assists)
def avgData(player_id1,player_id2,stat):
        
        #get database connection
        conn = sqlite3.connect('players.db')

        #get the season averages from player 1 and sort it by data
        df1 = pd.read_sql_query(f"SELECT AVG({stat}),date FROM 'games' WHERE id = {player_id1} group by season ", conn)
        sortedData1 = df1.sort_values(by=["date"])

        #get playername by innerjoin from table 'games' in table 'players and put it in the date
        #this is required to show the name in the graph
        playername =  pd.read_sql_query(f"SELECT name FROM games INNER JOIN players ON {player_id1} = players.id;", conn)
        names = playername['name']   
        sortedData1 = sortedData1.join(names)
        
        #create a bonus index called indexForComparison
        # this index is necesssary for the comparison mode. To understand this we have to take a closer look at the Plotly graph. 
        # in historical modus the x values are the dates
        # in comparison mode the two graph of the two players has the same x values -> they need the same x -value -> create index
        indexForComparison=[]
        #increment the indexForComparison for every played season of the player. indexForComparison can be seen as "seasons the player played"
        for i in range(len(sortedData1.index)):
            indexForComparison.append(i)
        #add indexForComparison to the data of player1
        sortedData1['games'] = indexForComparison

        #get the season averages from player 1 and sort it by date
        df2 = pd.read_sql_query(f"SELECT AVG({stat}),date FROM 'games' WHERE id = {player_id2} GROUP BY season ", conn)
        sortedData2 = df2.sort_values(by=["date"])

        #get playername by innerjoin from table 'games' in table 'players and put it in the data
        #this is required to show the name in the graph
        playername2 =  pd.read_sql_query(f"SELECT name FROM games INNER JOIN players ON {player_id2} = players.id;", conn)
        names2 = playername2['name']   
        sortedData2 = sortedData2.join(names2)
       
        #create a bonus index called indexForComparison. For an explanation why, look at line 37 in this file
        indexForComparison2=[]
        #increment the indexForComparison2 for every played season of the player. indexForComparison can be seen as "seasons the player played"
        for i in range(len(sortedData2.index)):
            indexForComparison2.append(i)
        #add indexForComparison2 to the data of player2
        sortedData2['games'] = indexForComparison2
        
        #combine the data of player1 anf player 2 and return it 
        combinedData=[sortedData1, sortedData2]
        result = pd.concat(combinedData)
        
        return result


#get the stats for all games from both players in the selected stat (points, assists)
def gameData(player_id1,player_id2,stat):

        #get the database connection
        conn = sqlite3.connect('players.db')
        
        #get the stats for all games from player1 and sort it by date
        df1 = pd.read_sql_query(f"SELECT {stat},date FROM 'games' WHERE id= {player_id1}", conn)
        sortedData1 = df1.sort_values(by=["date"])

        #get playername by innerjoin from table 'games' in table 'players and put it in the date
        #this is required to show the name in the graph
        playername =  pd.read_sql_query(f"SELECT name FROM games INNER JOIN players ON {player_id1} = players.id;", conn)
        names = playername['name']   
        sortedData1 = sortedData1.join(names)
        
        #create a bonus index called indexForComparison. For an explanation why, look at line 37 in this file
        indexForComparison=[]
        #increment the indexForComparison for every played game of the player. indexForComparison can be seen as "games the player played"
        for i in range(len(sortedData1.index)):
            indexForComparison.append(i)
        #add indexForComparison to the data of player1
        sortedData1['games'] = indexForComparison
        
        
        #get the stats for all games from player1 and sort it by date
        df2 = pd.read_sql_query(f"SELECT {stat},date FROM 'games' WHERE id= {player_id2}", conn)
        sortedData2 = df2.sort_values(by=["date"])

        #get playername by innerjoin from table 'games' in table 'players and put it in the date
        #this is required to show the name in the graph
        playername2 =  pd.read_sql_query(f"SELECT name FROM games INNER JOIN players ON {player_id2} = players.id;", conn)
        names2 = playername2['name']   
        sortedData2 = sortedData2.join(names2)
        
        #create a bonus index called indexForComparison2. For an explanation why, look at line 37 in this file
        indexForComparison2=[]
        #increment the indexForComparison for every played game of the player. indexForComparison can be seen as "games the player played"
        for i in range(len(sortedData2.index)):
            indexForComparison2.append(i)
        #add indexForComparison to the data of player1
        sortedData2['games'] = indexForComparison2
        
        #combine the data of player1 anf player 2 and return it 
        combinedData=[sortedData1, sortedData2]
        result = pd.concat(combinedData)
       
        return result

    
#gets all players that played in the nba
def getPlayers():
    conn = sqlite3.connect('players.db')
    df = pd.read_sql_query("SELECT * FROM 'players'", conn)
    return df    

#checks if a player is already downloaded
def isDownloaded(player_id):
  
    conn = sqlite3.connect('players.db')
    c = conn.cursor()
    status = c.execute(f"SELECT downloaded FROM 'players' WHERE id = {player_id}")
    data=status.fetchone()
    return data[0]    
