import sqlite3
import os
import matplotlib as mat
import matplotlib.pyplot as plt
import numpy as np
from statistics import mean

# establish access to database
def setUpDatabase(db_name):
	""" Creates database and returns cur and conn """
	
	path = os.path.dirname(os.path.abspath(__file__))
	conn = sqlite3.connect(path + '/' + db_name)
	cur = conn.cursor()
	return cur, conn

def joinAllTables(cur, conn):
	"""
	This function takes a passed in cursor and db connection and joins
	all three tables in the database. It returns a list of tuples, where
	each tuple is a row in the joined table, and each element is column value.
	"""

	cur.execute("""SELECT
						w.name --0 (these are index markers for personal use)
						,w.team
						,w.code --2
						,w.song
						,w.url --4
						,w.id
						,w.artist --6
						,w.row

						,st.name --8
						,st.avg
						,st.ops --10
						,st.strikeouts
						,st.homeruns --12
						,st.rbi
						,st.row --14

						,sp.song_id
						,sp.name --16
						,sp.popularity
						,sp.duration_ms --18
						,sp.explicit
						,sp.track_info --19

					
					FROM Walkup AS w
					
					LEFT JOIN Stats AS st
					ON w.row = st.row

					LEFT JOIN Spotify AS sp
					ON w.id = sp.song_id

					--this where clause limits query only to those records that can be joined
					WHERE w.row IN (SELECT st.row FROM Stats AS st)

					""")

	#Set 'players' equal to the table that is queried. Players is a list of tuples as mentioned earlier.
	players = cur.fetchall()
	
	#return the list (table). Now we can easily filter this table and make fewer calls to the database.
	return players

def getMenuChoice():
	print("\nWelcome to Team JJT's MLB Walkup Song Visualizer!")
	print("\nWould you like to make a custom scatter plot or see a static bar graph visualization?")
	print("Press 1 for scatterplot. \nPress 2 for bar graph.")
	choice = int(input("\nWhat is your selection? "))

	if choice == 1 or choice == 2:
		pass
	else:
		print("\nInvalid choice. Default of 1 has been selected.")
		choice = 1

	return choice


def getCustomChoices():

	menu = ['Batting Average', 'OPS', 'Strikeouts', 'Homeruns', 'RBIs', 'Walk-Up Song Popularity Score', 'Song Duration (ms)']

	#print welcome message
	print("\nWelcome to Team JJT's Scatterplot Visualization Tool!")
	
	#print x-axis selection message
	print("\nWhat would you like plotted on the x-axis? Enter a number from the menu below.")
	for item in menu:
		print(menu.index(item)+1, '	', item)

	#get choice from the user
	x_choice = input("\nWhat is your selection? ")
	x_choice = int(x_choice)

	if x_choice == 1:
		x_index = 9
		x_axis = 'Batting Average'

	elif x_choice == 2:
		x_index = 10
		x_axis = 'OPS'
	
	elif x_choice == 3:
		x_index = 11
		x_axis = 'Strikeouts'

	elif x_choice == 4:
		x_index = 12
		x_axis = 'Homeruns'

	elif x_choice == 5:
		x_index = 13
		x_axis = 'RBIs'

	elif x_choice == 6:
		x_index = 17
		x_axis = 'Popularity Score'

	elif x_choice == 7:
		x_index = 18
		x_axis = 'Song Duration (ms)'

	else:
		print('Invalid choice. Set to default value of 1.')
		x_index = 9
		x_axis = 'Batting Average'

	#print y-axis selection message
	print("\nWhat would you like plotted on the y-axis? Enter a number from the menu below.")
	for item in menu:
		print(menu.index(item)+1, '	', item)

	#get choice from the user
	y_choice = input("\nWhat is your selection? ")
	y_choice = int(y_choice)

	if y_choice == 1:
		y_index = 9
		y_axis = 'Batting Average'

	elif y_choice == 2:
		y_index = 10
		y_axis = 'OPS'

	elif y_choice == 3:
		y_index = 11
		y_axis = 'Strikeouts'

	elif y_choice == 4:
		y_index = 12
		y_axis = 'Homeruns'

	elif y_choice == 5:
		y_index = 13
		y_axis = 'RBIs'

	elif y_choice == 6:
		y_index = 17
		y_axis = 'Popularity Score'

	elif y_choice == 7:
		y_index = 18
		y_axis = 'Song Duration (ms)'

	else:
		print('Invalid choice. Set to default value of 1.')
		y_index = 9
		y_axis = 'Batting Average'

	indices = [x_index, y_index, x_axis, y_axis]

	return indices

def customScatter(indices, players):

	x_index = indices[0]
	y_index = indices[1]
	x_axis = indices[2]
	y_axis = indices[3]

	#initialize a list to store points
	x_values = []
	y_values = []

	#loop through all players and determine points
	for player in players:

		x = float(player[x_index])
		x_values.append(x)

		y = float(player[y_index])
		y_values.append(y)


	#plot the points decided above
	plt.scatter(x_values, y_values)
	plt.title('Data Visualization')
	plt.xlabel(f'{x_axis}')
	plt.ylabel(f'{y_axis}')
	plt.show()

def explicitBar(players):

	xplayers = []
	cplayers = []

	#split the players into two lists; explicit and clean
	for player in players:
		if player[19] == 1:
			xplayers.append(player)
		elif player[19] == 0:
			cplayers.append(player)
		else:
			pass

	#create lists to store specific stats among hitters with explicit walkup (x) songs
	xAVG = []
	xOPS = []
	xSO = []
	xHR = []
	xRBI = []

	#create lists to store specific stats among hitters with clean walkup (c) songs
	cAVG = []
	cOPS = []
	cSO = []
	cHR = []
	cRBI = []

	#add relevant data to each list
	for player in xplayers:
		xAVG.append(float(player[9]))
		xOPS.append(float(player[10]))
		xSO.append(float(player[11]))
		xHR.append(float(player[12]))
		xRBI.append(float(player[13]))

	#add relevant data to each list
	for player in cplayers:
		cAVG.append(float(player[9]))
		cOPS.append(float(player[10]))
		cSO.append(float(player[11]))
		cHR.append(float(player[12]))
		cRBI.append(float(player[13]))

	#create list to store averages
	xStats = [mean(xAVG), mean(xOPS), mean(xSO), mean(xHR), mean(xRBI)]
	cStats = [mean(cAVG), mean(cOPS), mean(cSO), mean(cHR), mean(cRBI)]

	#create list to store variables
	labels = ['AVG', 'OPS', 'SO', 'HR', 'RBI']

	"""
	CODE HERE IS FROM TEAM MEMBER
	"""

	#set data
	label = ['Clean', 'Explicit']
	xIntStats = (xStats[2], xStats[3], xStats[4])
	cIntStats = (cStats[2], cStats[3], cStats[4])
	#first three values must be 0 to line up the bars correctly
	xDecStats = (0, 0, 0, xStats[0], xStats[1])
	cDecStats = (0, 0, 0, cStats[0], cStats[1])

	N = 3
	width = 0.25
	ind = np.arange(N)
	
	stats = ('Strikeouts', 'Homeruns', 'RBI', 'AVG', 'OPS')

	fig, ax1 = plt.subplots()
	
	ax1.set_ylabel("# Per Player")
	
	p1 = ax1.bar(ind, cIntStats, width, color='blue')
	p2 = ax1.bar(ind + width, xIntStats, width, color='red')

	ax1.legend((p1[0],p2[0]), label, loc='upper center')
	

	N = 5
	new = np.arange(N)

	ax2 = ax1.twinx()

	ax2.set_xticks(new + width / 2)
	ax2.set_xticklabels(stats)
	ax2.set_ylabel("AVG, OPS Per Player")
	ax2.set(title= "Performance based on Explicit Walkup Song")
	
	p3 = ax2.bar(new, cDecStats, width, color='blue')
	p4 = ax2.bar(new + width, xDecStats, width, color='red')

	plt.show()


"""
Main program section to test above functions.
"""
if __name__ == '__main__':
	
	#set up SQLite3 Database Requirements
	cur, conn = setUpDatabase('walkup.db')

	#call joinAllTables to return complete table
	players = joinAllTables(cur, conn)

	#prompt user to decide which visual to see
	choice = getMenuChoice()

	#choice 1 is a scatter plot
	if choice == 1:
		#call getCustomChoices and return a list with the user's picks
		user_input = getCustomChoices()

		#create a custom scatterplot using information from user_input and database query (players)
		customScatter(user_input, players)

	#choice 2 is the bar graph
	else:
		explicitBar(players)
	
	#close the database connection
	conn.close()