from bs4 import BeautifulSoup
import requests
import re
import json
import pprint
import sqlite3
import os


def setUpDatabase(db_name):
	""" Creates database and returns cur and conn"""
	
	path = os.path.dirname(os.path.abspath(__file__))
	conn = sqlite3.connect(path + '/' + db_name)
	cur = conn.cursor()
	return cur, conn

def setUpWalkUpTable(data, cur, conn):
	"""Creates walk-up table"""

	cur.execute("DROP TABLE IF EXISTS Walkup")
	cur.execute("CREATE TABLE Walkup (name TEXT PRIMARY KEY, team TEXT, code TEXT, song TEXT, url TEXT, id TEXT, artist TEXT, row INTEGER)")
	count = 1
	for player in data:
		cur.execute("""INSERT INTO Walkup (name, team, code, song, url, id, artist, row) 
		VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", (player, data[player]['team'], data[player]['team_code'], data[player]['song'], data[player]['spotify_url'], data[player]['track_id'], data[player]['artist'], count))
		count = count + 1
	conn.commit()



def get_team_codes():
	""" Returns a list of MLB team abbreviations from MLB Entertainment website"""

	#website being scraped
	source = requests.get('https://www.mlb.com/entertainment/walk-up').text

	#create soup object
	soup = BeautifulSoup(source, 'lxml')

	#team code dictionary
	tc = []

	#find all team codes in option tags and loop through them, adding to tc dictionary
	for team in soup.find_all('option'):
		code = team['value']

		tc.append(code)

	#remove the first element of the list ('featured')
	tc.remove(tc[0])

	return tc


def isolate_name(text):
	"""Player names on the MLB Entertainment website are formatted five different ways.
	This function takes a passed-in string and isolates only the player's name.
	The function then returns that isolated name.
	"""
	
	# CASE 1:	'Justin Turner', 'J.D. Martinez', 'Ronald Acuna Jr.'
	if all((x.isalpha() or x == '.' or x == ' ') for x in text):
		text = text

	# CASE 2:	'#35 - CODY BELLINGER'
	elif '#' in text and '(' not in text:
		text = text.split('-')[1].strip()

	#CASE 3:	'WANDY PERALTA (FIRST AT-BAT)'
	elif '(' in text and '#' not in text:
		text = text.split('(')[0].strip()

	# CASE 4:	'JUAN SOTO - FIRST SONG'
	elif ' - ' in text and '#' not in text and '(' not in text:
		text = text.split(' - ')[0].strip()

	# CASE 5:	'#22 - CLAYTON KERSHAW (PITCHING)'
	elif '#' in text and ' - ' in text and '(' in text:
		text = text.split(' - ')[1].split('(')[0].strip()
	
	else:
		text = None

	return text




def get_walkup_songs(team_code):
	"""Returns a dictionary of players and corresponsing information from passed-in team code.
	Any MLB player who has not provided a walk-up song will be omitted from the dictionary.
	"""

	#initialize dictionary to hold player keys and associated song data
	players = {}

	#website being scraped
	url = f'https://www.mlb.com/entertainment/walk-up/{team_code}'
	source = requests.get(url).text

	#create soup object 
	soup = BeautifulSoup(source, 'lxml')

	#loop through all players on the roster
	for player in soup.find_all('tr', class_=re.compile(r'teams-row.*')):

		#grab name_text from HTML code and isolate name using isolate_name() function (at bottom)
		name_text = player.find(class_='player-name').text.strip()
		name = isolate_name(name_text)

		#grab team name
		team = player['data-team'].strip()

		#grab song name (using error handling if song not present)
		try:
			song = player.find(class_='song-title').text.strip()
		except Exception as e:
			song = None

		#grab artist name (using error handling if song not present)
		try:
			artist = player.find(class_='song-artist').text.strip()
		except Exception as e:
			artist = None

		#grab Spotify URL and Track ID (using error handling if song not present)
		try:
			spotify_url = player['data-spotifyurl'].strip()
			track_id = spotify_url.split('/')[-1]
		except Exception as e:
			spotify_url = None
			track_id = None

		#If player does not have a song on spotify, then do not add them
		if spotify_url != None:

			#If player is not in dictionary already, add information
			if name not in players:
				players[name]={
				'team': team,
				'song': song,
				'artist': artist,
				'spotify_url': spotify_url,
				'track_id': track_id,
				'team_code': team_code
				}

	#return the players dictionary
	return players

def get_all_walkup_data():
	""" Returns a dictionary of all players and song info from MLB website. """

	#initialize a master dictionary to store walk-up data for all players
	all_players = {}

	#create a list to store team codes
	team_codes = get_team_codes()

	#fetch walkup songs for every team and add that data to the all_players dictionary
	for code in team_codes:
		team_dict = get_walkup_songs(code)
		all_players.update(team_dict)

	#return the cumulative dictionary
	return all_players


"""
Main program section to test above functions.
"""
if __name__ == '__main__':

	#create a dictionary to hold all walk up song data
	test_dict = get_all_walkup_data()

	#create database to store walk up song data
	cur, conn = setUpDatabase("walkup.db")
	setUpWalkUpTable(test_dict, cur, conn)

	#create PrettyPrinter object for better visual of how dictionary is organized
	#pp = pprint.PrettyPrinter(indent=4)
	#pp.pprint(test_dict)

	conn.close()