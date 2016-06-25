#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
from terminaltables import AsciiTable
import textwrap
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
    #wrapped=textwrap.fill(x,50)
    for x in match_status_soup:
        match_statuses.append(str(x.span.string).strip())
    matches = zip(dates, stadiums, team1s, score1s, team2s, score2s, match_statuses)
    return matches

def print_matches(matches):
    matches_arr = []
    for match in matches:
        #match_arr = [str(match[2]), str(match[3]), str(match[4]), str(match[5]), str(match[1])]
        match_arr = [str(match[2]), str(match[3]), str(match[4]), str(match[5])]
        matches_arr.append(match_arr)
    #print (matches_array)
    table = AsciiTable(matches_arr)
    table.inner_heading_row_border = False
    table.inner_row_border = True
    print (table.table)

set_url()
html_doc = get_html()
matches = get_matches(html_doc)
print_matches(matches)
