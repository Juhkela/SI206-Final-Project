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
os.environ['SPOTIPY_CLIENT_ID'] = 'af0da31f178949c58f60415516fb1faa'
os.environ['SPOTIPY_CLIENT_SECRET'] = '7803f391738242ebaf499fcd5ac26645'
os.environ['SPOTIPY_REDIRECT_URI'] = 'https://google.com/'



# Grabbing Auth Token:
# Client ID:     af0da31f178949c58f60415516fb1faa
# Client Secret: 7803f391738242ebaf499fcd5ac26645
# GET https://accounts.spotify.com/authorize?client_id=af0da31f178949c58f60415516fb1faa&response_type=code&redirect_uri=https%3A%2F%2Fgoogle.com%2F&scope=playlist-read-private
# RUN CURL BELOW IN CMD
# curl -H "Authorization: Basic YWYwZGEzMWYxNzg5NDljNThmNjA0MTU1MTZmYjFmYWE6NzgwM2YzOTE3MzgyNDJlYmFmNDk5ZmNkNWFjMjY2NDU=" -d grant_type=authorization_code -d code=AQAv7cmKBhZlwSjgqr7uJrdvW-lpU_VXpTS5wQ8UD5mfp_S-j0Y1pQo5hJE13s3porPMvyY5pbEHEIUC4Zgc9F5aTYWi1APS9znn4jimDov5CC0g59pX20CohqWuQhtr3y26VaI9zZbip6Ip7ZU0PIBJbAPabI078d6rNbe4jFSlOC64iWsDqENikmtsEq6ofDPB8cuFvdtnq0DCCzFf4Q -d redirect_uri=https%3A%2F%2Fgoogle.com%2F https://accounts.spotify.com/api/token


def fillPlaylist(user_id, playlist_id, cur, conn):

    # username = sys.argv[1] # The username is 'SI206Project'

    # scope = 'playlist-modify-public'
    # token = util.prompt_for_user_token(username, scope)

    # Access token expires every hour: Grab a new one here --> https://developer.spotify.com/console/post-playlist-tracks/ 
    # token = 'BQC3E7TlyCS5bqOMw2qHhgm-1KuazC4tVhUBXpoIy75TbcAL4orKV3Y_hfXFrV_g1yZ6W-RTkB6hEh6MocHcjMhWN0V6QiXyG7fScBLaVyMEiM4d_6SYjnFIfDISl1M0l1W_d1Bth6lMEpLLdoN0DZ64g5zN2BYR2sfjXuV8qBCBuxzk0sv0-tX5bqJtTT1awoJvkX-W1cQ28IopXqUXnNbL7vxXH53x7_Vk1XAIRFQy6ZK07F-N-Zsgv9FtX2ChksK49-xdOWxpA4b3gEw-SGIgMQvuAQ'
    track_ids = []
    cur.execute('SELECT DISTINCT id FROM Walkup') # Grabs Spotify Song ID's from the Walkup table
    tuple_id = cur.fetchall()

    for i in range(len(tuple_id)):
        track_ids.append(tuple_id[i][0])
    
    split_list_tracks = chunks(track_ids, 100)

    # client_credentials_manager = SpotifyClientCredentials()
    # sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # sp = spotipy.Spotify(auth = token)
    # sp.trace = False

    # for i in split_list_tracks:
    #     sp.user_playlist_remove_all_occurrences_of_tracks(user_id, playlist_id, i)
    #     sp.user_playlist_add_tracks(user_id, playlist_id, i)

    return track_ids
    

def grabTrackData(track_ids):

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    split_list = chunks(track_ids, 50)
    track_data = []
    for i in split_list:
        track_data.extend(sp.tracks(i)['tracks'])

    return track_data

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    return [lst[i:i + n] for i in range(0, len(lst), n)]
    

def setUpSpotifyTable(data, cur, conn):

    cur.execute('''CREATE TABLE IF NOT EXISTS Spotify (song_id TEXT PRIMARY KEY, name TEXT, popularity INTEGER, 
                   duration_ms INTEGER, explicit BOOL, track_info TEXT)''')
    cur.execute('SELECT COUNT(*) FROM Spotify')
    total_rows = cur.fetchone()[0]
    for i in data[total_rows:total_rows+20]:
        cur.execute('''INSERT INTO Spotify (song_id, name, popularity, duration_ms, explicit, track_info)
                       VALUES (?, ?, ?, ?, ?, ?)''', 
                       (i['id'], i['name'], i['popularity'], i['duration_ms'], i['explicit'], i['external_urls']['spotify']))

    conn.commit()

def main():

    # username = sys.argv[1]
    # token = util.prompt_for_user_token(username)

    playlist_id = '3ExuKCBDeMaelDsAiMKz97'
    user_id = 'a75zp3fq9fm0y8cyb4eki5yb7'
    conn = sqlite3.connect('walkup.db')
    cur = conn.cursor()
    track_ids = fillPlaylist(user_id, playlist_id, cur, conn) # ---> Playlist filled. No need to run again.
    # print(track_ids)

    track_data = grabTrackData(track_ids)
    # pp = pprint.PrettyPrinter(depth=6)
    # pp.pprint(track_data)
    setUpSpotifyTable(track_data, cur, conn)
    

    conn.close()
    



if __name__ == "__main__":
    main()

