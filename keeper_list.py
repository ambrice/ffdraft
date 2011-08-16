#!/usr/bin/python2

from ffdraft import models

models.set_database('ffdraft.db')
session = models.Session()
for player in session.query(models.Player).order_by(models.Player.rank):
    if (player.rank % 10 == 1):
        print "\nRound " + str((player.rank / 10) + 1)
        print "-------"
    print ' {0} ({1} - {2})'.format(player.name, player.team, player.position)
