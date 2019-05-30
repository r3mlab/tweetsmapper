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
Results check
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("tweetsmapper-results")


def is_geo(tweet):
    """Filter geo-enabled tweets."""
    if tweet.place:
        return True
    elif tweet.coordinates:
        lat, lon = (
            tweet.coordinates["coordinates"][1],
            tweet.coordinates["coordinates"][0],
        )
        if lat == 0 and lon == 0:
            log.debug(
                "Tweet ID {} has lat: 0 & lon: 0. Filtering it out.".format(
                    tweet.id_str
                )
            )
            return False
        else:
            return True

    else:
        return False


def check(geo_tweets):
    """Check results and display how many geo enabled tweets were found."""
    if len(geo_tweets) == 0:
        log.error("Could not find tweets with geo information for this user.")
        raise SystemExit(1)
    else:
        tweets_w_coordinates_count = sum(1 for t in geo_tweets if t.coordinates)
        log.info(
            "Found {} geo enabled tweets, including {} with coordinates.".format(
                len(geo_tweets), tweets_w_coordinates_count
            )
        )
