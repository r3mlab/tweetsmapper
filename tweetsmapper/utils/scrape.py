#!/usr/bin/env python
# -*- coding: utf-8 -*-

# tweetsmapper
# Copyright (C) 2019 r3mlab
# https://github.com/r3mlab/tweetsmapper
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Scraping with twint
"""

import logging
import twint

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("tweetsmapper-scrape")


def get_ids(screen_name, limit):
    """Scrape tweet IDs for a given user."""
    c = twint.Config()
    c.Username = screen_name
    if limit:
        c.Limit = limit
    c.Store_object = True
    # c.Hide_output = True
    c.Format = "\033[A\33[2K\rID: {id} | DATE: {date}\r"

    limit_str = limit if limit != None else "all"
    log.info(
        f"Trying to collect {limit_str} tweet IDs for user {screen_name}. (May take a while)\n"
    )
    twint.run.Search(c)
    tweets = twint.output.tweets_object
    ids = [t.id for t in tweets]

    log.info("\033[A\33[2K\rDone! Collected {} tweet IDs.".format(len(ids)))

    return ids
