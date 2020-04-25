import sqlite3
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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

    # Gather stats per player for explicit and non explicit walkup song
    expAvg = joinStatandExplicit('avg', '1', cur, conn)
    nonAvg = joinStatandExplicit('avg', '0', cur, conn)
    avg_per_exp = sum(expAvg)/len(expAvg)
    avg_per_non = sum(nonAvg)/len(nonAvg)
    

    expOps = joinStatandExplicit('ops', '1', cur, conn)
    nonOps = joinStatandExplicit('ops', '0', cur, conn)
    ops_per_exp = sum(expOps)/len(expOps)
    ops_per_non = sum(nonOps)/len(nonOps)
    

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
    
    #set data
    
    label = ["non-explicit", "explicit"]
    expIntStats = (so_per_exp, hr_per_exp, rbi_per_exp)
    nonIntStats = (so_per_non, hr_per_non, rbi_per_non)
    #first three values must be 0 to line up the bars correctly
    expDecStats = (0, 0, 0, avg_per_exp, ops_per_exp)
    nonDecStats = (0, 0, 0, avg_per_non, ops_per_non)

    N = 3
    width = 0.25
    ind = np.arange(N)
    
    
    stats = ('Strikeouts', 'Homeruns', 'RBI', 'AVG', 'OPS')

    fig, ax1 = plt.subplots()
    
    ax1.set_ylabel("# Per Player")
    
    p1 = ax1.bar(ind, nonIntStats, width, color='blue')
    p2 = ax1.bar(ind + width, expIntStats, width, color='red')

    ax1.legend((p1[0],p2[0]), label, loc='upper center')
    



    N = 5
    new = np.arange(N)

    ax2 = ax1.twinx()

    ax2.set_xticks(new + width / 2)
    ax2.set_xticklabels(stats)
    ax2.set_ylabel("AVG, OPS Per Player")
    ax2.set(title= "Performance based on Explicit Walkup Song")
    

    p3 = ax2.bar(new, nonDecStats, width, color='blue')
    p4 = ax2.bar(new + width, expDecStats, width, color='red')
    

    fig.savefig("explicit.png")


    plt.show()











"""
Main program section to test above functions.
"""
if __name__ == '__main__':
    cur, conn = setUpDatabase('walkup.db')
    drawExplicitStatGraph(cur, conn)
    
    
    
    conn.close()