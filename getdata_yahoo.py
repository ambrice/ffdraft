#!/usr/bin/python2

import json
from xml.etree.ElementTree import ElementTree
from ffdraft.yahoo.auth import OAuthWrapper

def remove_namespace(root, namespace):
    ns = '{{{0}}}'.format(namespace)
    nsl = len(ns)
    if root.tag.startswith(ns):
        root.tag = root.tag[nsl:]
    for elem in root.getiterator():
        if elem.tag.startswith(ns):
            elem.tag = elem.tag[nsl:]

wrap = OAuthWrapper()
#response = wrap.request('http://fantasysports.yahooapis.com/fantasy/v2/game/nfl/stat_categories')
#response = wrap.request('http://fantasysports.yahooapis.com/fantasy/v2/users;use_login=1/games;game_keys=nfl/leagues')

players = []

for start in range(0,800,25):
    response = wrap.request('http://fantasysports.yahooapis.com/fantasy/v2/league/nfl.l.15740/players;sort=OR;count=25;start={0}/'.format(start))
    tree = ElementTree()
    tree.parse(response)
    remove_namespace(tree.getroot(), 'http://fantasysports.yahooapis.com/fantasy/v2/base.rng')

    for (rank, player) in enumerate(tree.findall('league/players/player'), 1):
        player_data = {
                'yahoo_id': int(player.findtext('player_id')),
                'rank': start + rank,
                'name': player.findtext('name/full'),
                'team': player.findtext('editorial_team_abbr'),
                'bye': int(player.findtext('bye_weeks/week')),
                'position': player.findtext('display_position'),
                }
        players.append(player_data)

with open('players.json', 'w') as f:
    f.write(json.dumps(players, sort_keys=True, indent=4))
