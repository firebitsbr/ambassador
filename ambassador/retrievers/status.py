#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
StatusRetriever module
"""

from __future__ import absolute_import, unicode_literals

from farnsworth.models import (
    Round,
    Score,
)

import ambassador.retrievers
LOG = ambassador.retrievers.LOG.getChild('status')


class StatusRetriever(object):
    """
    StatusRetriever class
    """

    def __init__(self, cgc):
        """A normal __init__. Happy now pylint?"""
        self._cgc = cgc
        self._round = None

    @property
    def current_round(self):
        """Return corrent round"""
        return self._round

    def run(self):
        """
        Update game status, including round number and the current scores.

        If we notice that the round number has jumped backward, explicitly create a new round.
        """
        LOG.debug("Getting status")
        status = self._cgc.getStatus()

        status_quo_round = Round.current_round()

        if status_quo_round is None:
            LOG.info("First game starts")
            self._round = Round.create(num=status['round'])
        elif status_quo_round.num == status['round']:
            LOG.debug("Continuing current round")
            self._round = status_quo_round
        else:
            if status_quo_round.num > status['round']:
                LOG.info("New game started")
            else:
                LOG.info("New round started")
            self._round = Round.create(num=status['round'])

        Score.update_or_create(self._round, scores=status['scores'])
