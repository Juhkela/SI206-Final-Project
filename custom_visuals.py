import sqlite3
import os
import matplotlib as mat
import matplotlib.pyplot as plt

# establish access to database
def setUpDatabase(db_name):
	""" Creates database and returns cur and conn """
	
	path = os.path.dirname(os.path.abspath(__file__))
	conn = sqlite3.connect(path + '/' + db_name)
	cur = conn.cursor()
	return cur, conn

def joinAllTables(cur, conn):

    #begin by querying the database to retrieve the data we need to make graph
    cur.execute(""" SELECT
	    				w.name
	    				,w.team
	    				,w.code
	    				,w.song
	    				,w.url
	    				,w.id
	    				,w.artist
	    				,w.row

	    				,st.name
	    				,st.avg
	    				,st.ops
	    				,st.strikeouts
	    				,st.homeruns
	    				,st.rbi
	    				,st.row

	    				,sp.song_id
	    				,sp.name
	    				,sp.popularity
	    				,sp.duration_ms
	    				,sp.explicit
	    				,sp.track_info

    				
    				FROM Walkup AS w
    				
    				LEFT JOIN Stats AS st
    				ON w.row = st.row

    				LEFT JOIN Spotify AS sp
    				ON w.id = sp.song_id

    				--this where clause limits query only to those records that can be joined
    				WHERE w.row IN (SELECT st.row FROM Stats AS st)

    				""")

    players = cur.fetchall()
    
    return players


def getCustomChoices():

	menu = ['Batting Average', 'OPS', 'Strikeouts', 'Homeruns', 'RBIs', 'Walk-Up Song Popularity Score', 'Song Duration']

	#print welcome message
	print("\nWelcome to Team JJT's MLB Walkup Song Visualizer!")
	
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
		x_axis = 'Song Duration'

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
		y_axis = 'Song Duration'

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



"""
Main program section to test above functions.
"""
if __name__ == '__main__':
    cur, conn = setUpDatabase('walkup.db')

    players = joinAllTables(cur, conn)

    #call getCustomChoices and return a list with the user's picks
    user_input = getCustomChoices()

    #create a custom scatterplot using information from user_input and database query (players)
    customScatter(user_input, players)
    
    conn.close()