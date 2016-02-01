import urllib2
from BeautifulSoup import BeautifulSoup
import ssl


def createURL(player):
    url = "https://en.wikipedia.org/wiki/"
    for x in player:
        url += x + "_"
    return url[0:-1]

def printTable(data):
        for table in data:
            print "\n"
            for row in table:
                if len(row) != 0:
                    print str(row).strip('[]')
playerStats = []

f = open("players.txt")
players = f.readlines()
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]

for player in players[435:]:
    context = ssl._create_unverified_context()

    p = player.strip().split(" ")
    contenturl = createURL(p)
    print contenturl

    try:
        url = urllib2.urlopen(contenturl,context=context)
    except URLError as e:
        print 'An error occured fetching %s \n %s' % (url, e.reason)

    soup = BeautifulSoup(url.read())

    try:
        rows = soup.find("table", attrs={'class':'wikitable'}).findChildren(['th', 'tr'])
    except AttributeError as e:
        print 'No tables found, exiting'

    player = []
    player.append([p]) # Append Name
    # Get header data
    for row in rows:
        headers = row.findAll('th')
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



printTable(playerStats)
