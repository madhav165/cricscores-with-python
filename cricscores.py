#!/usr/bin/env python3

import urllib.request
from bs4 import BeautifulSoup
from terminaltables import AsciiTable
import textwrap
import pydoc

global URL

def set_url():
    global URL
    URL = "http://www.espncricinfo.com/ci/engine/match/index.html?view=live"

def get_html():
    with urllib.request.urlopen(URL) as response:
        return response.read();

def get_matches(html_doc):
    soup = BeautifulSoup(html_doc, 'lxml')
    main_section=soup.find('section', {'id':'live-match-data'})
    tournaments=[]
    live_statuses=[]
    dates=[]
    stadiums=[]
    team1s=[]
    team2s=[]
    score1s=[]
    score2s=[]
    match_statuses=[]
    tournament_names=[]
    full_data=[]
    tournaments_soup = main_section.findAll('div', class_='match-section-head')
    for tournament in tournaments_soup:
        tournament_names.append(tournament.h2.text.strip())
    matches_in_t_soup=main_section.findAll('section', class_='matches-day-block')
    i = 0
    for matches_in_t in matches_in_t_soup:
        matches_soup = matches_in_t.findAll('section', class_='default-match-block')
        for match in matches_soup:
            live_statuses.append(match.find('span', class_='live-icon').text.strip())
            dates.append(match.find('span', class_='bold').text.strip())
            stadiums.append(match.find('span', class_='match-no').a.text.strip())
            score1s.append(match.find('div', class_='innings-info-1').span.text.strip())
            score2s.append(match.find('div', class_='innings-info-2').span.text.strip())
            team1_soup=match.findAll('div', class_='innings-info-1')
            for x in team1_soup:
                team1s.append(x.find(text=True).strip())
            team2_soup=match.findAll('div', class_='innings-info-2')
            for x in team2_soup:
                team2s.append(x.find(text=True).strip())
            match_statuses.append(match.find('div', class_='match-status').span.text.strip())
            tournaments.append(tournament_names[i])
        i+=1
    full_data.append([textwrap.fill('Tournament',10), 
                      #textwrap.fill('Live Status',10),
                      'Date(s)',
                      'Stadium',
                      'Team',
                      'Score',
                      'Team',
                      'Score',
                      'Status'])
    for x in range(len(team1s)):
        full_data.append([textwrap.fill(tournaments[x],10), 
                          #live_statuses[x], 
                          textwrap.fill(dates[x],10),
                          textwrap.fill(stadiums[x],15), 
                          textwrap.fill(team1s[x],10),
                          textwrap.fill(score1s[x],10), 
                          textwrap.fill(team2s[x],10),
                          textwrap.fill(score2s[x],10), 
                          textwrap.fill(match_statuses[x],10)])

    return full_data

def print_matches(matches):
    table = AsciiTable(matches)
    table.inner_heading_row_border = True
    table.inner_row_border = True
    pydoc.pager (table.table)

set_url()
html_doc = get_html()
matches = get_matches(html_doc)
#get_matches(html_doc)
print_matches(matches)
