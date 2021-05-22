#imports
import requests


#import other files
import getSQL 
import insertSQL

#-------------------------------
#all functions that call the api
#-------------------------------


#function that calls the api 
#gets the data from one player -> all stats from every game he played
def getData(player_id):

    #checks if player is already downloaded
    if  not getSQL.isDownloaded(player_id):
        #call api and saves data as json
        r = requests.get(f'https://www.balldontlie.io/api/v1/stats?per_page=100&player_ids[]={player_id}')
        resp = r.json()

        #number of pages is the number of required api calls to get the data 
        pages = (resp['meta']['total_pages'])

        #call the api for every page and saves the data as json
        for i in range(pages):
            r = requests.get(f'https://www.balldontlie.io/api/v1/stats?per_page=100&player_ids[]={player_id}&page={i}')
            resp = r.json()

            #gets the stats from every game
            for game in resp['data']:
                pts = game['pts'] 
                ast = game['ast']
                rebs = game['reb']
                stl = game['stl']
                blocks = game['blk']
                fg3a = game['fg3a']
                fg3m = game['fg3m']
                fga = game['fga']
                fgm = game['fgm']
                fta = game['fta']
                ftm = game['ftm']

                season = game['game']['season']
                time = game['game']['date']
                
                #inserts the data in the 'games' table in the database
                insertSQL.insertData(player_id,pts,ast,rebs,stl,blocks,fg3a,fg3m,fga,fgm,fta,ftm,season,time)

                #sets player to downloaded
                insertSQL.setDownloaded(player_id)
        
        

#function that gets all players that played in the nba
# is only called in the beginning, when theres no databse
def getPlayers():     

    #call api and save data as json 
    r = requests.get('https://www.balldontlie.io/api/v1/players?per_page=100')
    resp = r.json()

    #number of pages is the number of required api calls to get the data 
    pages = (resp['meta']['total_pages'])

    #variable i is not allowed to start as zero, so its set to 1 -> if its zero at the beginnign page 0 is called->  page 0 does not exist
    i=1
    #call the api for every page and saves the data as json
    for i in range(pages):
        
        r = requests.get(f'https://www.balldontlie.io/api/v1/players?per_page=100&page={i+1}')
        response = r.json()

        #get the name and id for every player
        for player in response['data']:
            name =  player["first_name"] + " "+ player["last_name"]
            id = player["id"]

            #save in database in table 'players'
            insertSQL.insertPlayers(id,name)
        
            