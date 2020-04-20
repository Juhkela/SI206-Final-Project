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


def fillPlaylist(user_id, playlist_id, cur, conn):
    # Access token expires every hour: Grab a new one here --> https://developer.spotify.com/console/post-playlist-tracks/ 
    token = 'BQCmQ0mWTS_v2RlEwo0kWDlZjgMks1Ss9GdkG6FMbTW1R106kA__NUSYJ0wl5tTl2hE-tT315kBtK3Q_F3c_VbrRiKTHy4c-8FtJ6Go_ogNGYlG8S8O4Eqfs6QSmHwxgO1pa1zVi2KPJCCVQOG7g3HZ6yPECckVNlETmAs2FnN-OU4NdZ-XPum_t-Hkem5bI1MsnBu4ur4fmMCS9qkm2DEeI4ja8'
    one = [], two = [], three = [], four = [], five = [], six = [], last_fifteen = []
    track_ids = []
    cur.execute('SELECT id FROM Walkup') # Grabs Spotify Song ID's from the Walkup table
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
    for i in range(500, 600):
        six.append(track_ids[i])
    for i in range(600, 615):
        last_fifteen.append(track_ids[i])
    
    sp = spotipy.Spotify(auth = token)

    all_songs = [one, two, three, four, five, six, last_fifteen] 
    # Lists all 615 songs that were gathered from the Walkup table in walkup.db

    for i in all_songs:
        #sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, i)
        sp.user_playlist_add_tracks(user_id, playlist_id, i)
    

def grabTrackData():
    pass

def setUpSpotifyTable(data, cur, conn):
    cur.execute("DROP TABLE IF EXISTS Spotify")
    cur.execute('''CREATE TABLE Spotify (title TEXT PRIMARY KEY, song_id TEXT, popularity INTEGER, 
                   duration_ms REAL, explicit BOOL, track_info TEXT)''')

def main():
    playlist_id = '3ExuKCBDeMaelDsAiMKz97'
    user_id = 'a75zp3fq9fm0y8cyb4eki5yb7'
    conn = sqlite3.connect('walkup.db')
    cur = conn.cursor()
    # fillPlaylist(user_id, playlist_id, cur, conn) ---> Do not run this command again.

    conn.close()
    



if __name__ == "__main__":
    main()

