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

# Grabbing Auth Token:
# Client ID:     af0da31f178949c58f60415516fb1faa
# Client Secret: 7803f391738242ebaf499fcd5ac26645
# GET https://accounts.spotify.com/authorize?client_id=af0da31f178949c58f60415516fb1faa&response_type=code&redirect_uri=https%3A%2F%2Fgoogle.com%2F&scope=playlist-read-private
# RUN CURL BELOW IN CMD
# curl -H "Authorization: Basic YWYwZGEzMWYxNzg5NDljNThmNjA0MTU1MTZmYjFmYWE6NzgwM2YzOTE3MzgyNDJlYmFmNDk5ZmNkNWFjMjY2NDU=" -d grant_type=authorization_code -d code=AQDBQlAxPI4Ga97pk8YUqtic1z74AEiTfShjw-0-2__Z7N0apEXypq7MriH2SzvYoeKJuIdfr0SPdIBLKnDLT3dFby3-jNNSZDW5-W98UaAIWrM8Fxiti7Xs5OpfmHtK_sgpmeBPGRMOE3mIY295FKF5v_41BM9Lmdh5gC2ISSqSA7cVXnae4MYpO2AKuCQKZPBSrlhVn6Bkyv-s3VCxYw -d redirect_uri=https%3A%2F%2Fgoogle.com%2F https://accounts.spotify.com/api/token

def fillPlaylist(user_id, playlist_id, cur, conn):

    # username = sys.argv[1] # The username is 'SI206Project'

    # scope = 'playlist-modify-public'
    # token = util.prompt_for_user_token(username, scope)

    # Access token expires every hour: Grab a new one here --> https://developer.spotify.com/console/post-playlist-tracks/ 
    token = 'BQDMm68XomWdY68OcawVzQ2CKiz64uT0kgVv44It8EBoKvmNhcXvoB382JOn9VrWiC1O4K8ZULte-mzNFmDOxTeasvicWtscxd5X8c4PokbZO_DUGLuTHr-ARF_YEgjIsRg-UWMdquOVa4C3ezBZCdHzNEOkMrXLpVGakjOplxvyiRc2MqJ_ZrTAaXWMB7qx8T5AlF_Dgq_guE1eZMqJSfg0dpzt'
    increment = 0
    track_ids = []
    cur.execute('SELECT DISTINCT id FROM Walkup') # Grabs Spotify Song ID's from the Walkup table
    tuple_id = cur.fetchall()

    for i in range(len(tuple_id)):
        track_ids.append(tuple_id[i][0])
    
    # split_list_tracks = chunks(track_ids, 100)

    # if token:
    #     sp = spotipy.Spotify(auth = token)
    #     sp.trace = False

    #     for i in split_list_tracks:
    #         increment += 1
    #         # sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, i)
    #         # sp.user_playlist_add_tracks(user_id, playlist_id, i)

    # else:
    #     print("The token has expired")

    return track_ids
    

def grabTrackData(track_ids):
    token = 'BQBrk7NnHsguCY2NsVuy8KUjm46cNfA6KXJ-YOcwFw5BFhPGi7q_bdT2VdJNLz9bs0_4guBvUtL_cK8l24OypEatHrEPkL3f9JYrI95rv2ATJxkXLSA8S1t0e0Ag0gp5GrazqKwgYMNFSme10zZl2hvoZ8aOiI3WfID7tPe9lPFRc2s'
    sp = spotipy.Spotify(auth=token)
    split_list = chunks(track_ids, 50)
    track_data = []
    for i in split_list:
        track_data.extend(sp.tracks(i)['tracks'])

    return track_data

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]
    

def setUpSpotifyTable(data, cur, conn):
    cur.execute("DROP TABLE IF EXISTS Spotify")
    cur.execute('''CREATE TABLE IF NOT EXISTS Spotify (song_id TEXT PRIMARY KEY, name TEXT, popularity INTEGER, 
                   duration_ms INTEGER, explicit BOOL, track_info TEXT)''')
    for i in data:
        cur.execute('''INSERT INTO Spotify (song_id, name, popularity, duration_ms, explicit, track_info)
                       VALUES (?, ?, ?, ?, ?, ?)''', 
                       (i['id'], i['name'], i['popularity'], i['duration_ms'], i['explicit'], i['external_urls']['spotify']))

    conn.commit()

def main():
    playlist_id = '3ExuKCBDeMaelDsAiMKz97'
    user_id = 'a75zp3fq9fm0y8cyb4eki5yb7'
    conn = sqlite3.connect('walkup.db')
    cur = conn.cursor()
    track_ids = fillPlaylist(user_id, playlist_id, cur, conn) # ---> Playlist filled. No need to run again.
    # print(track_ids)

    track_data = grabTrackData(track_ids)
    setUpSpotifyTable(track_data, cur, conn)
    

    conn.close()
    



if __name__ == "__main__":
    main()

