import insertSQL

#test insertData with dummy data
def test_insertData():
    assert insertSQL.insertData(0,1,1,1,1,1,1,1,1,1,1,1,1,"test") == True
    
#deletes dummy data to prevent alot of useless information in the database
def test_delete():
    assert insertSQL.delete('games',0) == True    