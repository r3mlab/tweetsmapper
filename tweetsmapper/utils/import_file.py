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
File Imports
"""

import logging
import os
import json
import tweepy

from tweetsmapper.utils import results, api

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("tweetsmapper-fileinput")


def process_tweets(input_file, config_file=None):
    """Check file extension and process the file accordingly."""

    suffix = os.path.splitext(input_file)[1].lower()[1:]

    if suffix == "jsonl":
        log.info(f"Reading tweets from {input_file}...")
        log.debug("Processing JSONL file.")
        geo_tweets = read_jsonl(input_file)

    elif suffix == "txt":
        log.info(f"Reading tweet IDs from {input_file}...")
        keys = api.get_keys(config_file)
        twitter_api = api.authenticate(keys)
        geo_tweets = read_txt(input_file, twitter_api)
    return geo_tweets


def read_jsonl(input_file):
    """Read tweets from a .jsonl file."""
    geo_tweets = []
    with open(input_file) as input:
        for line in input.readlines():
            tweet_json = json.loads(line)
            tweet = tweepy.models.Status().parse(tweepy.api, tweet_json)
            if results.is_geo(tweet):
                geo_tweets.append(tweet)
    return geo_tweets


def read_txt(input_file, twitter_api):
    """Read tweets ids from a .txt file and rehydrate them with the API."""
    ids_list = []
    with open(input_file) as input:
        for line in input.readlines():
            line = line.strip()
            if line.isdigit():
                id = line
            else:
                id = line.split(" ")[0]
            ids_list.append(id)

    tweets = api.hydrate(ids_list, twitter_api)

    geo_tweets = [t for t in tweets if results.is_geo(t)]
    # for t in tweets:
    #     if results.is_geo(t):
    #         geo_tweets.append(t)

    return geo_tweets


def has_unique_author(geo_tweets):
    "Check if all geo tweets are from the same user."
    userid_list = []
    for num, tweet in enumerate(geo_tweets):
        if tweet.user.id not in userid_list:
            userid_list.append(tweet.user.id)

    return True if len(userid_list) == 1 else False
