#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
import time

global URL

def set_url():
    global URL
    URL = "http://www.espncricinfo.com/ci/engine/match/index.html?view=live"

def get_html():
    with urllib.request.urlopen(URL) as response:
        return response.read();

def get_matches(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')

    match_info_soup=soup.find_all('div', class_='match-info')
    innings_info_1_soup=soup.find_all('div', class_='innings-info-1')
    innings_info_2_soup=soup.find_all('div', class_='innings-info-2')
    match_status_soup=soup.find_all('div', class_='match-status')

    dates = []
    stadiums = []
    team1s = []
    score1s = []
    team2s = []
    score2s = []
    match_statuses = []

    for x in match_info_soup:
        dates.append(x.find('span', class_='bold').string.strip())
        stadiums.append(x.find('span', class_='match-no').a.string.strip())
    
    for x in innings_info_1_soup:
        team1s.append(x.find(text=True).strip())
        if str(x.span.string).strip() != 'None':
            score1s.append(str(x.span.string).strip())
        else:
            score1s.append("")

    for x in innings_info_2_soup:
        team2s.append(x.find(text=True).strip())
        if str(x.span.string).strip() != 'None':
            score2s.append(str(x.span.string).strip())
        else:
            score2s.append("")

    for x in match_status_soup:
        match_statuses.append(str(x.span.string).strip())
    matches = zip(dates, stadiums, team1s, score1s, team2s, score2s, match_statuses)
    return matches

def print_matches(matches):
    print()
    print ('%-40s %-10s %-40s %5s' % ("-----------------------------------", "SCORES", "-----------------------------------", "\n\n"))
    for x in matches:
        print ('%-30s %-20s %-30s %-20s %5s' % (str(x[2]), str(x[3]), str(x[4]), str(x[5]), "\n\n"))

#t1 = time.time();
set_url()
html_doc = get_html()
matches = get_matches(html_doc)
print_matches(matches)
#t2 = time.time();
#print ('Retreived in %.f milliseconds' % (1000*(t2-t1)))
