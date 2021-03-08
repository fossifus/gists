# scrape top games on BGG to sqlite db

import boardgamegeek
import sqlite3
import requests
from bs4 import BeautifulSoup
from time import sleep

# setup
db_loc = 'bgg.sqlite'

# normalize characters in string, courtesy of Aliison Tharp
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

# request wrapper, courtesy of Sonya Sawtelle
def request(msg, slp=1):
    '''A wrapper to make robust https requests.'''
    status_code = 500  # Want to get a status-code of 200
    while status_code != 200:
        sleep(slp)  # Don't ping the server too often
        try:
            r = requests.get(msg)
            status_code = r.status_code
            if status_code != 200:
                print("Server Error! Response Code %i. Retrying..." % (r.status_code))
        except:
            print("An exception has occurred, probably a momentory loss of connection. Waiting one seconds...")
            sleep(1)
    return r

# connections
bgg = boardgamegeek.BGGClient()
conn = sqlite3.connect(db_loc)
c = conn.cursor()

# loop through BGG's "Browse All Board Games" pre-sorted by num voters
game_ids = []
nratings = 1e8
npage = 1
nrate_threshold = 5000
while nratings > nrate_threshold:
    # get HTML
    r = request("https://boardgamegeek.com/browse/boardgame/page/%i?sort=numvoters&sortdir=desc" % (npage,))
    soup = BeautifulSoup(r.text, "html.parser")
    # parse HTML for list of all the rows (tags) in the list of games on this page
    table = soup.find_all("tr", attrs={"id": "row_"})

    # for each row, parse game data
    for i, row in enumerate(table):
        # find all hyperlinks in HTML
        links = row.find_all("a")
        # get URL of the hyperlink for this game, and handle case where some games may have global rank as first column
        if "name" in links[0].attrs.keys():
            del links[0]
        # parse game ID from URL
        gameid = int(links[1]["href"].split("/")[2])
        game_ids.append(gameid)
        # parse number of ratings from HTML
        ratings_str = row.find_all("td", attrs={"class": "collection_bggrating"})[2].contents[0]
        nratings = int("".join(ratings_str.split()))
        if nratings < nrate_threshold:
            break

    npage = npage + 1
    sleep(1)

####
#### GET GAME DATA AND STORE IN DB
####

strip_accents()

# commit and close db connection
conn.commit()
