import urllib2
from BeautifulSoup import BeautifulSoup
import ssl
import csv
from tabulate import tabulate

def createURL(player):
    url = "https://en.wikipedia.org/wiki/"
    for x in player:
        url += x + "_"
    return url[0:-1]
def insertRowSpans(rowspans,playerTable):
    for span in rowspans:
        for i in xrange(span[0],span[0]+span[2]):
            playerTable[i].insert(span[1],span[3])
    return playerTable
def outputStats(playerStats,columns):
    with open('playerStats.csv', 'wb') as fp:
        a = csv.writer(fp, delimiter=',')
        for p in playerStats:
            indices = []
            try:
                club = p[2].index('Club')
            except ValueError:
                club = 0
            try:
                season = p[2].index('Season')
            except ValueError:
                season = 1
            p[2].reverse()
            try:
                goals = p[2].index("Goals")
            except ValueError:
                goals = p[2].index("CS")
            try:
                apps = p[2].index("Apps")
            except ValueError:
                apps = p[2].index("App")
            p[2].reverse()
            for i in xrange(len(p)):
                if i == 0:
                    a.writerows([p[i]])
                else:
                    ret = []
                    row = p[i]
                    ret.append(row[club])
                    ret.append(row[season])
                    ret.append(row[-1*apps-1])
                    ret.append(row[-1*goals-1])
                    a.writerows([ret])



# Get player names to scrape
f = open("players.txt")
players =  f.readlines()[:458]
#Establish context and user-agent
context = ssl._create_unverified_context()
def scrapePlayerStats(players):
    playerStats = []
    for player in players:
        rowspan = []
        print player
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
            v = False
            rows = soup.findAll("table", attrs={'class':'wikitable'})
            for table in rows:
                if table.findChildren(['tr'])[0].text.startswith("Club") == True or table.findChildren(['tr'])[0].text.startswith("Season") == True:
                    rows = table.findChildren(['tr'])

                    v = True
            if(v == False):
                raise AttributeError
        except AttributeError as e:
            print 'No tables found for %s' % (player)
            valid = False

        if(valid):
            playerTable = []
            # Get header data
            for j in xrange(len(rows)): # every set of rows
                headers = rows[j].findAll('th')
                cols = rows[j].findAll('td')
                ret = []
                if len(headers) != 0:
                    loc = 0
                    for i in xrange(len(headers)):
                        if headers[i].has_key("rowspan"):
                            rowspan.append((j, loc, int(headers[i]["rowspan"]), headers[i].getText().strip().encode('ascii', 'replace')))
                        elif headers[i].has_key("colspan"):
                            x = [headers[i].text.strip().encode('ascii', 'replace')]
                            for _ in xrange(int(headers[i]["colspan"])-1):
                                x.append("-")
                            ret.extend(x)
                            loc+=int(headers[i]["colspan"])
                        else:
                            ret.append(headers[i].text.strip().encode('ascii', 'replace'))
                        loc += 1
                # td rows
                if len(cols) != 0:
                    loc = 0
                    for i in xrange(len(cols)):
                        if cols[i].has_key("rowspan"):
                            rowspan.append((j, i, int(cols[i]["rowspan"]), cols[i].getText().strip().encode('ascii', 'replace')))
                        elif cols[i].has_key("colspan"):
                            x = [cols[i].text.strip().encode('ascii', 'replace')]
                            for _ in xrange(int(cols[i]["colspan"])-1):
                                x.append("-")
                            ret.extend(x)
                            loc+=int(cols[i]["colspan"])
                        else:
                            ret.append(cols[i].text.strip().encode('ascii', 'replace'))
                        loc += 1

                if(len(ret) != 0):
                    playerTable.append(ret)

            playerTable = insertRowSpans(rowspan, playerTable)
            playerTable.insert(0, [player.strip()])
            playerStats.append(playerTable)
    return playerStats

playerStats = scrapePlayerStats(players)
outputStats(playerStats,["Club","Season","Apps","Goals"])
