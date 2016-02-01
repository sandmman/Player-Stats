import urllib2
from BeautifulSoup import BeautifulSoup
import ssl


players = ["Christiano Ronaldo","Wayne Rooney","Lionel Messi"]
playerStats = []


for player in players:
    context = ssl._create_unverified_context()

    p = player.split(" ")
    contenturl = "https://en.wikipedia.org/wiki/" + p[0] + "_" + p[1]
    soup = BeautifulSoup(urllib2.urlopen(contenturl,context=context).read())
    rows = soup.find("table", attrs={'class':'wikitable'}).findChildren(['th', 'tr'])
    player = []
    player.append([p[0] + " " + p[1]]) # Append Name
    # Get header data
    for row in rows:
        headers = cols = row.findAll('th')
        cols = row.findAll('td')
        if len(headers) != 0:
            cols = [e.text.strip().encode('ascii', 'replace') for e in headers]
            if len(cols) != 0:
                player.append([e for e in cols])
        else:
            cols = [e.text.strip().encode('ascii', 'replace') for e in cols]
            if len(cols) != 0:
                player.append([e for e in cols])
    playerStats.append(player)

def printTable(data):
        for table in data:
            print "\n"
            for row in table:
                if len(row) != 0:
                    print str(row).strip('[]')


printTable(playerStats)
