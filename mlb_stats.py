import requests
import re
import json
import sqlite3
import os


def setUpDatabase(db_name):
	""" Creates database and returns cur and conn """
	
	path = os.path.dirname(os.path.abspath(__file__))
	conn = sqlite3.connect(path + '/' + db_name)
	cur = conn.cursor()
	return cur, conn

def getPlayerID(name, cur, conn):
    """ Take name from database, search in Stats API and return the player id """

    url = "http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code='mlb'&active_sw='Y'&name_part=" + name + "%25&search_player_all.col_in=player_id&search_player_all.col_in=position"
    r = requests.get(url)
    dic = json.loads(r)
    print(dic)
    return
    


def setUpStatsTable():
    pass





"""
Main program section to test above functions.
"""
if __name__ == '__main__':
    cur, conn = setUpDatabase('walkup.db')
    getPlayerID("Seth Lugo", cur, conn)
    

	