import urllib2
from BeautifulSoup import BeautifulSoup
import ssl
import csv

def createURL(player):
    url = "https://en.wikipedia.org/wiki/"
    for x in player:
        url += x + "_"
    return url[0:-1]

playerStats = []

# Get player names to scrape
f = open("players.txt")
players = f.readlines()

#Establish context and user-agent
#opener = urllib2.build_opener()
#opener.addheaders = [('User-agent', 'Mozilla/5.0')]
context = ssl._create_unverified_context()

for player in players:

    p = player.strip().split(" ")
    contentURL = createURL(p)

    valid = True

    try:
        url = urllib2.urlopen(contentURL,context=context)
    except urllib2.URLError as e:
        print 'Error (%s) occured fetching %s' % (e.reason,contentURL)
        valid = False

    soup = BeautifulSoup(url.read())

    try:
        rows = soup.find("table", attrs={'class':'wikitable'}).findChildren(['th', 'tr'])
    except AttributeError as e:
        print 'No tables found for %s' % (player)
        valid = False

    if(valid):
        stats = []
        stats.append([player]) # Append Name
        # Get header data
        for row in rows:
            headers = row.findAll('th')
            cols = row.findAll('td')
            if len(headers) != 0:
                cols = [e.text.strip().encode('ascii', 'replace') for e in headers]
                if len(cols) != 0:
                    stats.append([e for e in cols])
            else:
                cols = [e.text.strip().encode('ascii', 'replace') for e in cols]
                if len(cols) != 0:
                    stats.append([e for e in cols])
        playerStats.append(stats)

# Out to csv file
with open('playerStats.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    for p in playerStats:
        a.writerows(p)
