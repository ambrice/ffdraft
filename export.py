#!/usr/bin/python

import sys
import ffdraft.models as models

models.set_database(sys.argv[1])
league = models.League.active_league()
for t in league.teams:
    team = models.Team.find_by_name(t.name)
    print team.name
    print '-' * len(team.name)
    for draft in team.drafted:
        print '{0}) {1} ({2})'.format(draft.round, draft.player.name, draft.player.team)
    print

