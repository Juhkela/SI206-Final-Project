import os
import sys
import json
import requests
import pprint
import sqlite3
import spotipy
import webbrowser
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from json.decoder import JSONDecodeError

# def setUpDatabase(db_name):
# 	""" Creates database and returns cur and conn """     - CURRENTLY NOT IN USE. PLANNING TO ADD A TABLE TO walkup.db
	
# 	path = os.path.dirname(os.path.abspath(__file__))
# 	conn = sqlite3.connect(path + '/' + db_name)
# 	cur = conn.cursor()
# 	return cur, conn


def fillPlaylist(user_id, playlist_id, cur, conn):
    token = 'BQA1Y3NVWyaP8BRu5UADYbU5OQGRjAQgdQLqn9Zlites0HzBFXxn7Yw14wPOEkqV3I-t8X2gA5RpoKcMd_Pyihu1FxT1kHz0hxXAfeIy8XfJcha6s5HD9yC-0PldBpZmmuvMV5iYAgpIMzyBA9kuH4yPVTqM14BNdseo6ei4yzM9V3RMSw2my69df5bvTo9KFzvkj78HXD2WYB6mH3AfS44gTncu'
    # uri_base = 'spotify:track:'
    one = []
    two = []
    three = []
    four = []
    five = []
    track_ids = []
    cur.execute('SELECT id FROM Walkup')
    tuple_id = cur.fetchall()

    for i in range(len(tuple_id)):
        track_ids.append(tuple_id[i][0])
    for i in range(100):
        one.append(track_ids[i])
    for i in range(100, 200):
        two.append(track_ids[i])
    for i in range(200, 300):
        three.append(track_ids[i])
    for i in range(300, 400):
        four.append(track_ids[i])
    for i in range(400, 500):
        five.append(track_ids[i])
    
    

    sp = spotipy.Spotify(auth = token)

    # sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, one) # Prevents readding the
    # sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, two) 
    # sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, three) 
    # sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, four) 
    # sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, five) 
    sp.user_playlist_add_tracks(user_id, playlist_id, one) # Adds in tracks.
    sp.user_playlist_add_tracks(user_id, playlist_id, two) 
    sp.user_playlist_add_tracks(user_id, playlist_id, three) 
    sp.user_playlist_add_tracks(user_id, playlist_id, four) 
    sp.user_playlist_add_tracks(user_id, playlist_id, five) 
    
    return track_ids


def setUpSpotifyTable(data, cur, conn):
    pass

    

def grabSongData():
    pass


def main():
    playlist_id = '3ExuKCBDeMaelDsAiMKz97'
    user_id = 'a75zp3fq9fm0y8cyb4eki5yb7'
    conn = sqlite3.connect('walkup.db')
    cur = conn.cursor()
    track_id = fillPlaylist(user_id, playlist_id, cur, conn)
    print(track_id)

    conn.close()
    



if __name__ == "__main__":
    main()

