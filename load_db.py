#!/usr/bin/python2

import sys
import ffdraft.models as models

models.set_database('ffdraft.db')
models.Player.load_from_json(sys.argv[1])
league = models.League('North Phoenix')
league.save()

