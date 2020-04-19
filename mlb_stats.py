import requests
import re
import json
import sqlite3
import os
import pprint


def setUpDatabase(db_name):
	""" Creates database and returns cur and conn """
	
	path = os.path.dirname(os.path.abspath(__file__))
	conn = sqlite3.connect(path + '/' + db_name)
	cur = conn.cursor()
	return cur, conn

def getPlayerID(name):
    """ Take name from database, search in Stats API and return the player id.
    Returns 0 for pitchers so easily filtered out in table """

    url = "http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part='" + name + "%25'&search_player_all.col_in=player_id&search_player_all.col_in=position"
    r = requests.get(url).json()
    if r['search_player_all']['queryResults']['row']['position'] == 'P':
        return 0
    id = r['search_player_all']['queryResults']['row']['player_id']
    
    return id
    
def createPlayerDict(player_id):
    """ Takes in a player id and requests the stats from the MLB API.  Returns a dictionary with those values"""
    pass

def setUpStatsTable(cur, conn):
    """ Iterates through walkup song table and creates new table with various stats for each player"""

    cur.execute("DROP TABLE IF EXISTS Stats")
    cur.execute("CREATE TABLE Stats (name TEXT PRIMARY KEY,  avg )
    pass





"""
Main program section to test above functions.
"""
if __name__ == '__main__':
    cur, conn = setUpDatabase('walkup.db')
    getPlayerID("Seth Lugo", cur, conn)

    conn.close()
    

	