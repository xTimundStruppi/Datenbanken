#import file that is tested
import getSQL


#---------------------------------------------------------------------------------------------
#database has to be created and the players LeBron James and Michael Jordan must be donwloaded
#---------------------------------------------------------------------------------------------


#tests if LeBron James (id =237) is downloaded
def test_isDownloaded():
    assert getSQL.isDownloaded(237) == 1

#tests the average data of LeBron James and Michael Jordan
def test_avgData():
   test =  getSQL.avgData(237,'points',2931)
   comp = test['games'].values[0]
   assert comp == 0
   
#tests the game data of LeBron James and Michael Jordan
def test_gameData():
   test =  getSQL.gameData(237,'points',2931)
   comp = test['games'].values[0]
   assert comp == 0
   