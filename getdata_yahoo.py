#!/usr/bin/python

from twill.commands import go, formvalue, submit, follow
from twill import get_browser
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
import re
import getpass

class Schedule(object):
    def __init__(self):
        soup = BeautifulStoneSoup(self.read_schedule_data())

        self.game_data = {}

        for game in soup.findAll('game'):
            (week, home, away) = (game['week'], game['hometeam'], game['awayteam'])
            if week == "" or home == "" or away == "":
                next
            if not self.game_data.has_key(week):
                self.game_data[week] = {}
            self.game_data[week][home] = away
            self.game_data[week][away] = "@" + home

    def read_schedule_data(self):
        # Get the bye weeks from Fantasy Football Nerd, because I can't find them on Yahoo (?!?!)
        try:
            f = open('schedule.xml')
            schedule_data = f.read()
            f.close()
        except:
            b = get_browser()
            b.go("http://api.fantasyfootballnerd.com/ffnScheduleXML.php?apiKey=2008093012495907")
            schedule_data = b.get_html()
            f = open('schedule.xml', 'w')
            f.write(schedule_data)
            f.close()
        return schedule_data

    def bye(self, team):
        for week in self.game_data.keys():
            if not self.game_data[week].has_key(team.upper()):
                return week

class PlayerData(object):
    def __init__(self, user, passwd):
        self.user = user
        self.passwd = passwd
        self.islogin = False
        self.schedule = Schedule()
        self.teamrx = re.compile(r'\((\w+) - ([\w]+)')

    def login(self):
        if not self.islogin:
            # First log in to Yahoo
            go("http://login.yahoo.com")
            formvalue("1", "login", self.user)
            formvalue("1", "passwd", self.passwd)
            submit()

            # Now go to player list
            go("http://football.fantasysports.yahoo.com")
            follow("Player List")

            self.islogin = True

    def _get_tds(self, tr):
        tds = []
        name = tr.td
        status = name.find('span', 'status')
        if status:
            tds.append(name.a.string + "(" + status.string + ")")
        else:
            tds.append(name.a.string)

        m = self.teamrx.match(name.span.string)
        if m:
            tds.append(m.group(1))
            tds.append(m.group(2))
            tds.append(self.schedule.bye(m.group(1)))
        td = name.findNextSibling('td')
        td = td.findNextSibling('td')
        td = td.findNextSibling('td')
        td = td.findNextSibling('td')
        td = td.findNextSibling('td')
        while td:
            tmp = str(td.string)
            if tmp == "&nbsp;":
                tmp = "-"
            tds.append(tmp)
            td = td.findNextSibling('td')
        return tds

    def _parse_player_data(self, html_data):
        players = []
        soup = BeautifulSoup(html_data)
        for tr in soup.table.tbody:
            player = {}
            data = self._get_tds(tr)
            for header in self.headers:
                if len(data) == 0:
                    break
                if header == None:
                    data.pop(0)
                else:
                    player[header] = data.pop(0)
            players.append(player)
        return players

    def players(self):
        self.login()
        players = []
        b = get_browser()

        self.headers = ['Player','Team','Position','Bye','Projected','Actual',None,'Passing Yds','Passing TD','Int','Rushing Yds','Rushing TD','Receiving Yds','Receiving TD',None,'Ret TD','Misc 2pt','Fum Lost','Fan Pts']
        formvalue("2", "status", "ALL")
        formvalue("2", "pos", "O")
        submit()
        players.extend(self._parse_player_data(b.get_html()))
        for i in range(11):
            follow("Next 25")
            players.extend(self._parse_player_data(b.get_html()))

        self.headers  = ['Player','Team','Position','Bye','Projected','Actual',None,None,None,None,None,None,None,None,None,'Fan Pts']
        formvalue("2", "status", "ALL")
        formvalue("2", "pos", "DEF")
        submit()
        players.extend(self._parse_player_data(b.get_html()))
        follow("Next 25")
        players.extend(self._parse_player_data(b.get_html()))

        self.headers  = ['Player','Team','Position','Bye','Projected','Actual',None,None,None,None,None,None,None,'Fan Pts']
        formvalue("2", "status", "ALL")
        formvalue("2", "pos", "K")
        submit()
        players.extend(self._parse_player_data(b.get_html()))
        follow("Next 25")
        players.extend(self._parse_player_data(b.get_html()))

        return players

user = raw_input("Yahoo user name: ")
passwd = getpass.getpass("Yahoo password:  ")
data = PlayerData(user, passwd)
players = data.players()
players.sort(key=lambda p: 0 if p['Projected'] == "-" else int(p['Projected']))

headers = ['Player','Team','Position','Bye','Projected','Actual','Passing Yds','Passing TD','Int','Rushing Yds','Rushing TD','Receiving Yds','Receiving TD','Ret TD','Misc 2pt','Fum Lost','Fan Pts']

f = open("playerdata.csv", "w")
f.write(",".join(headers) + "\n")
for player in players:
    f.write(",".join([ player.get(header, "-") for header in headers ]) + "\n")
f.close()

