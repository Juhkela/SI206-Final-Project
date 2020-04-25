import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt

# establish access to database
def setUpDatabase(db_name):
	""" Creates database and returns cur and conn """
	
	path = os.path.dirname(os.path.abspath(__file__))
	conn = sqlite3.connect(path + '/' + db_name)
	cur = conn.cursor()
	return cur, conn

def joinStatandExplicit(stat, explicit, cur, conn):
    """ Joins walkup and spotify table to return a list of specific
    stats for players with explicit or non-explicit walkup songs 
    explicit == '1' for explicit songs, explict == '0' for nonexplicit"""
    
    cur.execute("""SELECT Walkup.row, Spotify.song_id AS id FROM Walkup 
    JOIN Spotify ON Spotify.song_id= Walkup.id WHERE Spotify.explicit = {}""".format(explicit))
    players = cur.fetchall() 
    results = []
    for player in players:
        #store player row
        row = player[0]
        
        #find stat
        try:
            cur.execute("SELECT Stats.{} FROM Stats WHERE row = {}".format(stat, row))
            num = float(cur.fetchone()[0])
        except:
            continue    #skip player if not in stats table

        results.append(num)
        
    return results

def drawExplicitStatGraph(cur, conn):

    # stats = ['avg', 'ops', 'strikeouts', 'homeruns', 'rbi']
    # for stat in stats:
    #     exp = joinStatandExplicit(stat, '1', cur, conn)
    #     non = joinStatandExplicit(stat, '0', cur, conn)

    expAvg = joinStatandExplicit('avg', '1', cur, conn)
    nonAvg = joinStatandExplicit('avg', '0', cur, conn)
    avg_per_exp = sum(expAvg)/len(expAvg)
    avg_per_non = sum(nonAvg)/len(nonAvg)

    expSo = joinStatandExplicit('strikeouts', '1', cur, conn)
    nonSo = joinStatandExplicit('strikeouts', '0', cur, conn)
    so_per_exp = sum(expSo)/len(expSo)
    so_per_non = sum(nonSo)/len(nonSo)

    expHr = joinStatandExplicit('homeruns', '1', cur, conn)
    nonHr = joinStatandExplicit('homeruns', '0', cur, conn)
    hr_per_exp = sum(expHr)/len(expHr)
    hr_per_non = sum(nonHr)/len(nonHr)

    expRbi = joinStatandExplicit('rbi', '1', cur, conn)
    nonRbi = joinStatandExplicit('rbi', '0', cur, conn)
    rbi_per_exp = sum(expRbi)/len(expRbi)
    rbi_per_non = sum(nonRbi)/len(nonRbi)

    

    exp = ["non-explicit", "explicit"]

    fig, ax = plt.subplots()
    
    p1 = ax.bar("Homeruns", avg_non_Hr, 0.5, color='blue')
    p2 = ax.bar(exp[1], avg_explicit_Hr, 0.5, color='red')

    ax.legend((p1[0],p2[0]), ('Non-explicit', 'Explicit'))



    plt.show()










"""
Main program section to test above functions.
"""
if __name__ == '__main__':
    cur, conn = setUpDatabase('walkup.db')
    drawExplicitStatGraph(cur, conn)
    
    
    
    conn.close()