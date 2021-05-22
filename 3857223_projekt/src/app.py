#imports
from dash.dependencies import Input, Output
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import os

#import other files
import insertSQL
import api
import getSQL


#---------------------------------------------------------------------------
# this file is the file you must run, when you want to start the localhost
#---------------------------------------------------------------------------


#load stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# creates database if it does not already exists
if not os.path.isfile('players.db'):
    insertSQL.setDatabase()
    api.getPlayers()


#set app and use stylesheets
app = dash.Dash(external_stylesheets=external_stylesheets)

# -------------get data-------------
df = getSQL.getPlayers()

#------------layout----------------------
app.layout = html.Div([

    html.H1('Compare two players'),

    #dropdownmenu to choose the first player you want to compare
    dcc.Dropdown(id="player1",
                    options=[{'label':df.iloc[i]['name'], 'value':df.iloc[i]['id']} for i in range(len(df.index))],
                    placeholder="Enter a player",
                    style={'width':"40%"}             
    ),

    #dropdownmenu to choose the stat you want to compare the players with (points, assists,...)
    dcc.Dropdown(id="statToCompare",
                    options=[
                        {"label": "Points", "value": 'points'},
                        {"label": "Assists", "value": 'assists'},
                        {"label": "Rebounds", "value": 'rebounds'},
                        {"label": "Steals", "value": 'steals'},
                        {"label": "Blocks", "value": 'blocks'},
                        {"label": "3 pointer attempted", "value": 'fg3a'},
                        {"label": "3 pointer made", "value": 'fg3m'},
                        {"label": "Field goals attempted ", "value": 'fga'},
                        {"label": "Field goals made", "value": 'fgm'},
                        {"label": "Free-throws attempted", "value": 'fta'},
                        {"label": "Free-throws made", "value": 'ftm'}],
                    value='points',
                    style={'width':"40%"}             
    ),

    #dropdownmenu to choose the second player you want to compare
    dcc.Dropdown(id="player2",
                    options=[{'label':df.iloc[i]['name'], 'value':df.iloc[i]['id']} for i in range(len(df.index))],
                    placeholder="Enter a player",
                    style={'width':"40%"}             
    ), 

    #create some space
    html.Br(),
    html.Br(),
    html.Br(),

    #dropdownmenu to choose the mode of the comparison (historical or comparison)
    dcc.Dropdown(id="dataOption",
                    options=[
                     {"label": "Historical", "value": 'hist'},
                     {"label": "Comparison", "value": 'comp'},],
                    value='hist',
                    style={'width':"40%"}               
    ),

    #dropdownmenu to choose the precision of the comparison (all games or season average)
    dcc.Dropdown(id="precision",
                    options=[
                     {"label": "All Games", "value": 'games'},
                     {"label": "Season Average", "value": 'season'},],
                    value='season',
                    style={'width':"40%"}               
    ),

    #creating a loading animation
     dcc.Loading(
            id="loading-1",
            type="default",
            children=html.Div(id="loading-output-1"),
            
        ),
    
    
    
    
#graph where the players are compared
    dcc.Graph(id="graph",figure={}),

  

])

#-------------------callback-------------------

@app.callback(
    # inputs are the dropdownmenu's
    # outputs are the graph and the loading animation
    [Output(component_id='graph',component_property='figure'),
    Output(component_id="loading-output-1", component_property="children")],
    [Input(component_id='player1',component_property='value'),
    Input(component_id='statToCompare',component_property='value'),
    Input(component_id='dataOption',component_property='value'),
    Input(component_id='precision',component_property='value'),
    Input(component_id='player2',component_property='value')],
)



def getplayers(opt_player1, statToCompare, dataOption, precision,opt_player2):

    #if is selected, when two players are chosen    
    if opt_player1 and opt_player2:
       
        #get the data from player 1
        api.getData(opt_player1)
        #get the data from player 2
        api.getData(opt_player2)

        #if is selected, when the precision is set to games
        if precision == "games":

            #if is selected, when the mode of comparison is set to historical -> comparison of all games in historical order
            #then gets data for all games from the database
            #update graph with loaded data
            if dataOption=="hist":
                Data = getSQL.gameData(opt_player1,opt_player2,statToCompare)
                fig = px.line(Data,x='date', y=Data[statToCompare],color='name')
                
            #if is selected, when the mode of comparison is set to comparison -> both graphs will start together regardless when the players actually played
            #get the data for all games for both players from the database
            #update graph with loaded data
            if dataOption=="comp":
                Data = getSQL.gameData(opt_player1,opt_player2,statToCompare)
                fig = px.line(Data,x='games', y=Data[statToCompare],color='name')

        # if is selected, when the precision is set to season -> comparison of the average of the seasons the players played
        if precision=="season":

            #if is selected, when the mode of comparison is set to historical -> comparion of the season avergages in historical order
            #get the season averages for both players from the database
            #update graph with loaded data
            if dataOption=="hist":
                Data = getSQL.avgData(opt_player1,opt_player2,statToCompare)
                fig = px.line(Data,x='date', y=Data[f'AVG({statToCompare})'],color='name')

            #if is selected, when the mode of comparison is set to comparison -> both graphs will start together regardless when the players actually played
            #get the season averages for both players from the database
            #update graph with loaded data
            if dataOption=="comp":
                Data = getSQL.avgData(opt_player1,opt_player2,statToCompare)
                fig = px.line(Data,x='games', y=Data[f'AVG({statToCompare})'],color='name')
            
            
        #insert the "zoom slider" under the graph
        fig.update_xaxes(rangeslider_visible=True)

        return fig, None

    #else is selected, when there are not two selected players
    else:
        return dash.no_update
    
   

#main that runs server    
if __name__=="__main__":
    app.run_server(debug=True)
    