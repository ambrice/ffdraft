import json
import re
from xml.etree import ElementTree

from PyQt4 import QtCore, QtGui

from sqlalchemy import func, create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base = declarative_base()
Session = sessionmaker()
session = None

def set_database(path):
    global session
    engine = create_engine('sqlite:///{0}'.format(path), echo=False)
    Session.configure(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

def remove_namespace(root, namespace):
    ns = '{{{0}}}'.format(namespace)
    nsl = len(ns)
    if root.tag.startswith(ns):
        root.tag = root.tag[nsl:]
    for elem in root.getiterator():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]

### sqlalchemy models ###

class YahooAuth(Base):
    __tablename__ = 'yahoo_auth'

    id = Column(Integer, primary_key=True)
    access_token_key = Column(String)
    access_token_secret = Column(String)
    access_expires = Column(Integer)
    session_handle = Column(String)

    @staticmethod
    def total_count():
        return session.query(func.count(YahooAuth.id)).scalar()

    @staticmethod
    def first():
        return session.query(YahooAuth).order_by(YahooAuth.id).first()

    def __init__(self, key, secret, session_handle, expires):
        self.access_token_key = key
        self.access_token_secret = secret
        self.access_expires = expires
        self.session_handle = session_handle

    def save(self):
        session.add(self)
        session.commit()

class League(Base):
    __tablename__ = 'leagues'

    id = Column(Integer, primary_key=True)
    yahoo_id = Column(Integer)
    name = Column(String)
    current_round = Column(Integer)
    current_draft_index = Column(Integer)
    time_limit = Column(Integer)
    autopick = Column(Integer)
    active = Column(Boolean)
    roster_count = Column(Integer)

    @staticmethod
    def total_count():
        return session.query(func.count(League.id)).scalar()

    @staticmethod
    def names():
        return [ row.name for row in session.query(League.name).all() ]

    @staticmethod
    def find_by_name(name):
        return session.query(League).filter_by(name=str(name)).one()

    @staticmethod
    def active_league():
        return session.query(League).filter_by(active=True).one()

    @staticmethod
    def load_from_xml(xml):
        session.query(League).delete()
        root = ElementTree.fromstring(xml)
        remove_namespace(root, 'http://fantasysports.yahooapis.com/fantasy/v2/base.rng')
        leagues = []
        for leaguexml in root.findall('users/user/games/game/leagues/league'):
            name = leaguexml.findtext('name')
            yahoo_id = leaguexml.findtext('league_id')
            league = League(name, yahoo_id)
            session.add(league)
            leagues.append(league)
        session.commit()
        return leagues

    @staticmethod
    def set_roster(xml):
        root = ElementTree.fromstring(xml)
        remove_namespace(root, 'http://fantasysports.yahooapis.com/fantasy/v2/base.rng')
        league_yahoo_id = root.findtext('league/league_id')
        league = session.query(League).filter_by(yahoo_id=league_yahoo_id).one()
        count = 0
        for position in root.findall('league/settings/roster_positions/roster_position'):
            count += int(position.findtext('count'))
        league.roster_count = count
        session.add(league)
        session.commit()

    def __init__(self, name, yahoo_id=None):
        self.name = name
        self.yahoo_id = yahoo_id
        self.current_round = 1
        self.current_draft_index = 0
        self.time_limit = 120
        self.autopick = 1
        self.active = False
        self.roster_count = 0

    def __repr__(self):
        return "<League('{0}')>".format(self.name)

    def save(self):
        session.add(self)
        session.commit()

    def activate(self):
        actives = session.query(League).filter_by(active=True).all()
        for current in actives:
            current.active = False
            session.add(current)
        self.active = True
        session.add(self)
        session.commit()

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    yahoo_id = Column(Integer)
    league_id = Column(Integer, ForeignKey('leagues.id'))
    name = Column(String)
    manager = Column(String)
    order = Column(Integer)
    img_url = Column(String)

    league = relationship('League', backref=backref('teams', order_by=id))

    @staticmethod
    def find_by_name(name):
        current_league = League.active_league()
        return session.query(Team).filter_by(name=str(name), league_id=current_league.id).one()

    @staticmethod
    def load_from_xml(xml):
        root = ElementTree.fromstring(xml)
        remove_namespace(root, 'http://fantasysports.yahooapis.com/fantasy/v2/base.rng')
        league_yahoo_id = root.findtext('league/league_id')
        league = session.query(League).filter_by(yahoo_id=league_yahoo_id).one()
        session.query(Team).filter_by(league_id=league.id).delete()
        teams = []
        for order, teamxml in enumerate(root.findall('league/teams/team')):
            name = teamxml.findtext('name')
            yahoo_id = teamxml.findtext('team_id')
            manager = teamxml.findtext('managers/manager/nickname')
            img_url = teamxml.findtext('team_logos/team_logo/url')
            team = Team(league, name, manager, order, img_url, yahoo_id)
            session.add(team)
            teams.append(team)
        session.commit()
        return teams

    def __init__(self, league, name, manager, order, img_url, yahoo_id=None):
        self.league = league
        self.name = name
        self.manager = manager
        self.order = order
        self.img_url = img_url
        self.yahoo_id = yahoo_id

    def __repr__(self):
        return "<Team({0},'{1}','{2}',{3},'{4}')>".format(self.league, self.name, self.manager, self.order, self.img_url)

class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    yahoo_id = Column(Integer)
    rank = Column(Integer)
    name = Column(String)
    team = Column(String)
    bye = Column(Integer)
    position = Column(String)
    img_url = Column(String)

    @staticmethod
    def clear():
        session.query(Player).delete()
        session.commit()

    @staticmethod
    def append_from_xml(xml, start):
        root = ElementTree.fromstring(xml)
        remove_namespace(root, 'http://fantasysports.yahooapis.com/fantasy/v2/base.rng')
        for rank, playerxml in enumerate(root.findall('league/players/player'), start+1):
            yahoo_id = playerxml.findtext('player_id')
            name = playerxml.findtext('name/full')
            team = playerxml.findtext('editorial_team_abbr')
            bye = playerxml.findtext('bye_weeks/week')
            position = playerxml.findtext('display_position')
            img_url = playerxml.findtext('image_url')
            player = Player(yahoo_id, rank, name, team, bye, position, img_url)
            session.add(player)
        session.commit()

    @staticmethod
    def load_from_json(jsonfile):
        with open(jsonfile, 'r') as f:
            players = json.load(f)
        for p in players:
            session.add(Player(**p))
        session.commit()

    def __init__(self, yahoo_id, rank, name, team, bye, position, img_url):
        self.yahoo_id = yahoo_id
        self.rank = rank
        self.name = name
        self.team = team
        self.bye = bye
        self.position = position
        self.img_url = img_url

    def __repr__(self):
        return "<Player({0},{1},'{2}','{3}',{4},'{5}','{6}')>".format(self.yahoo_id, self.rank, self.name, self.team, self.bye, self.position, self.img_url)

class DraftedPlayer(Base):
    __tablename__ = 'drafted_players'

    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))
    round = Column(Integer)

    player = relationship('Player', backref=backref('drafted', order_by=round))
    team = relationship('Team', backref=backref('drafted', order_by=round))

    def __init__(self, player, team, round):
        self.player = player
        self.team = team
        self.round = round

    def __repr__(self):
        return "<DraftedPlayer({0},{1},{2})>".format(self.player, self.team, self.round)

    def change_round(self, rnd):
        self.round = rnd
        session.add(self)
        session.commit()

### Qt Model/View models ###

class LeagueModel(QtCore.QAbstractListModel):
    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return session.query(func.count(League.id)).scalar()

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        league = session.query(League).order_by(League.id).all()[index.row()]
        return QtCore.QVariant(league.name)

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return False
        self.beginRemoveRows(parent, row, row + count - 1)
        for league in session.query(League).order_by(League.id).all()[row:row+count]:
            session.delete(league)
        session.commit()
        self.endRemoveRows()
        return True

    def append_league(self, name):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        session.add(League(name))
        session.commit()
        self.endInsertRows()

class TeamModel(QtCore.QAbstractListModel):
    def __init__(self, league_name, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.league = session.query(League).filter_by(name=league_name).one()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.league.teams)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        team = session.query(Team).filter_by(league_id=self.league.id, order=index.row()).one()
        return QtCore.QVariant('{0} ({1})'.format(team.name, team.manager))

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return False
        self.beginRemoveRows(parent, row, row + count - 1)
        for team in self.league.team[row:row+count]:
            session.delete(team)
        session.commit()
        self.endRemoveRows()
        # TODO: Update the order
        return True

    def append_team(self, team, manager):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        session.add(Team(self.league, team, manager, self.rowCount()))
        session.commit()
        self.endInsertRows()

    def move_up(self, row):
        t1 = session.query(Team).filter_by(league_id=self.league.id, order=row).first()
        t2 = session.query(Team).filter_by(league_id=self.league.id, order=row-1).first()
        t1.order = row-1
        t2.order = row
        session.add(t1)
        session.add(t2)
        session.commit()
        self.dataChanged.emit(self.index(row-1,0), self.index(row,0))

    def move_down(self, row):
        t1 = session.query(Team).filter_by(league_id=self.league.id, order=row).first()
        t2 = session.query(Team).filter_by(league_id=self.league.id, order=row+1).first()
        t1.order = row+1
        t2.order = row
        session.add(t1)
        session.add(t2)
        session.commit()
        self.dataChanged.emit(self.index(row,0), self.index(row+1,0))

    def team_names(self):
        return [ row.name for row in session.query(Team).filter_by(league_id=self.league.id).order_by(Team.order).all() ]

class PlayerModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self,parent)
        self.headers = ['id', 'yahoo_id', 'Rank', 'Name', 'Team', 'Bye', 'Position']
        self.cache = session.query(Player).order_by(Player.rank).all()

    def __getitem__(self, idx):
        return self.cache[idx]

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.cache)
    
    def columnCount(self, parent=QtCore.QModelIndex()):
        return 0 if parent.isValid() else 7

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal:
            return QtCore.QVariant(self.headers[section])
        else:
            return QtCore.QVariant(section + 1)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        return QtCore.QVariant(self._get_row(index.row())[index.column()])
    
    def load(self, filename):
        Player.load_from_json(filename)
        self.cache = session.query(Player).order_by(Player.rank).all()

    def add_player(self, player):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        session.add(player)
        session.commit()
        self.cache = session.query(Player).order_by(Player.rank).all()
        self.endInsertRows()

    def _get_row(self, row):
        # It's only 800 read-only rows, no point in lazy-loading..
        if not self.cache:
            self.cache = session.query(Player).order_by(Player.rank).all()
        p = self.cache[row]
        return ( p.id, p.yahoo_id, p.rank, p.name, p.team, p.bye, p.position )

class DraftedPlayerModel(QtCore.QAbstractListModel):
    def __init__(self, team_name, parent=None):
        QtCore.QAbstractListModel.__init__(self,parent)
        self.team = session.query(Team).filter_by(name=team_name).first()

    def __getitem__(self, idx):
        return self.team.drafted[idx]

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self.team.drafted)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        drafted = self.team.drafted[index.row()]
        player = drafted.player
        return QtCore.QVariant('{0}) {1}: {2} (Bye: {3})'.format(drafted.round, player.position, player.name, player.bye))

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return False
        self.beginRemoveRows(parent, row, row + count - 1)
        for drafted in self.team.drafted[row:row+count]:
            session.delete(drafted)
        session.commit()
        self.endRemoveRows()
        return True

    def draft(self, player, round):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        session.add(DraftedPlayer(player, self.team, round))
        session.commit()
        self.endInsertRows()

    def has_drafted(self, round):
        drafted = session.query(DraftedPlayer).filter_by(team_id=self.team.id, round=round).first()
        if drafted:
            return drafted.player
        else:
            return None

class PlayerFilterProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent = None):
        QtGui.QSortFilterProxyModel.__init__(self, parent)
        self.position = 'All'
        self.numrx = re.compile(r'^-?\d+$')
        self.drafted = [ d.player.id for d in session.query(DraftedPlayer).all() ]

    def __getitem__(self, idx):
        sourceRow = self.mapToSource(self.index(idx, 0)).row()
        return self.sourceModel()[sourceRow]

    def lessThan(self, left, right):
        ldata = str(left.data().toString())
        rdata = str(right.data().toString())
        if ldata == "-":
            return True
        elif rdata == "-":
            return False
        elif self.numrx.match(ldata) != None and self.numrx.match(rdata) != None:
            # Both numbers, do numeric comparison
            return int(ldata) < int(rdata)
        else:
            return ldata < rdata

    def filterAcceptsRow(self, sourceRow, sourceParent):
        player = self.sourceModel()[sourceRow]
        if self.position != 'All' and self.position != player.position:
            return False
        if player.id in self.drafted:
            return False
        else:
            return True

    def set_position(self, position):
        self.position = position

    def draft(self, player):
        self.drafted.append(player.id)
        self.invalidate()

    def remove_draft(self, player):
        self.drafted.remove(player.id)
        self.invalidate()

