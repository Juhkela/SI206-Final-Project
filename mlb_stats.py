import requests
import re
import json
import sqlite3
import os
import pprint
import time


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
    #skip repeat names, we have plenty of data
    if r['search_player_all']['queryResults']['totalSize'] == '1':
        #pitchers are zero
        if r['search_player_all']['queryResults']['row']['position'] == 'P':
            return 0
        id = r['search_player_all']['queryResults']['row']['player_id']
        return id
    
    return 0
    
def createPlayerDict(player_id):
    """ Takes in a player id and requests the stats from the MLB API.  Returns a dictionary with those values"""

    try:
        baseurl = "http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season='2019'&player_id='{}'".format(player_id)
        full = baseurl + "&sport_hitting_tm.col_in=avg&sport_hitting_tm.col_in=ops&sport_hitting_tm.col_in=so&sport_hitting_tm.col_in=hr&sport_hitting_tm.col_in=rbi"
        r = requests.get(full).json()
        if r['sport_hitting_tm']['queryResults']['totalSize'] != '1':
            return {}
    except:
        print("Couldn't find stats")
        return {}

    return r

def setUpStatsTable(cur, conn):
    """ Iterates through walkup song table and creates new table with each row as various stats for each player"""

    cur.execute("DROP TABLE IF EXISTS Stats")
    cur.execute("CREATE TABLE Stats (name TEXT PRIMARY KEY,  avg TEXT, ops TEXT, strikeouts TEXT, homeruns TEXT, rbi TEXT)")
    cur.execute("SELECT * FROM Walkup")
    players = cur.fetchall()
    
    count = 0
    for player in players:
        name = player[0]
        print(name)
        if type(name) != str:
            continue
        id = getPlayerID(name)
        if id == 0:
            continue #skip pitchers
        results = createPlayerDict(id)
        if len(results) == 0:
            continue #skip if something goes wrong with api

        stats = results['sport_hitting_tm']['queryResults']['row']
        cur.execute("""INSERT INTO Stats (name, avg, ops, strikeouts, homeruns, rbi) VALUES (?, ?, ?, ?, ?, ?)
        """, (name, stats['avg'], stats['ops'], stats['so'], stats['hr'], stats['rbi']))
        count = count + 1
        conn.commit()

        if count % 5 == 0:
            print('Pausing for a bit...')
            time.sleep(5)
    
    





"""
Main program section to test above functions.
"""
if __name__ == '__main__':
    cur, conn = setUpDatabase('walkup.db') 
    setUpStatsTable(cur, conn)
   
    name = None
    if type(name) != str:
        print("PLAYER NOT FOUND")
    id = getPlayerID(name)
    if id == 0:
        print("pitcher") #skip pitchers
    results = createPlayerDict(id)
    if len(results) == 0 or results['sport_hitting_tm']['queryResults']['totalSize'] == '0':
        print("PLAYER NOT FOUND") #skip when api doesn't work for whatever reason

    stats = results['sport_hitting_tm']['queryResults']['row']
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(results)
    conn.close()
    

	