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

import logging
import pkg_resources
import os
import sys
import datetime
import argparse

from .utils import args_check, api, import_file, map, results, scrape


# logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("tweetsmapper")


def get_tweets(args):
    """Get tweets to consider for mapping."""
    geo_tweets = []

    input_source = args_check.input_source(args)

    if input_source == "user":
        log.debug("Input source = user")
        # Auth
        keys = api.get_keys(args.config_path)
        twitter_api = api.authenticate(keys)

        # Check that user exists
        api.get_user_info(twitter_api, args.screen_name)

        # Download
        if args.limit and args.limit <= 3200:
            geo_tweets = api.download_tweets(
                twitter_api, args.screen_name, limit=args.limit
            )
        else:
            ids = scrape.get_ids(args.screen_name, args.limit)
            tweets = api.hydrate(ids, twitter_api)
            geo_tweets = [t for t in tweets if results.is_geo(t)]

    elif input_source == "file":
        log.debug("Input source = file")
        if args.limit != 3200:
            log.info(
                "Note: Limit argument (-l) has no effect when mapping from a file."
            )
        geo_tweets = import_file.process_tweets(args.input_file, args.config_path)

    results.check(geo_tweets)

    return geo_tweets


def tweetsmapper(args):
    """Main logic."""
    if args.configure:
        api.configure(args.config_path)
    else:

        geo_tweets = get_tweets(args)

        # Initialize Leaflet map
        tweets_map = map.create()
        # Initialize Leaflet MarkerCluster & FeatureGroupSubGroups
        tweets_cluster = map.add_cluster(tweets_map)

        map.add_tweets(
            geo_tweets=geo_tweets, cluster=tweets_cluster, tweets_map=tweets_map
        )
        # Customize map
        tweets_map = map.customize(tweets_map, args, geo_tweets)

        # Save map
        map.save(tweets_map, args)


def main():
    banner = "tweetsmapper v{} - (C) r3mlab - GPLv3 License - https://github.com/r3mlab/tweetsmapper".format(
        pkg_resources.get_distribution("tweetsmapper").version
    )
    log.info(banner)
    # Parse arguments
    script_description = "Generate Leaflet maps from geo-enabled tweets."
    # usage = "\n\ntweetsmapper -n <screen_name> [options]"
    parser = argparse.ArgumentParser(description=script_description)
    # parser = argparse.ArgumentParser(description=script_description, usage=usage)

    exclusive = parser.add_mutually_exclusive_group()

    exclusive.add_argument(
        "-n",
        "--screen-name",
        type=args_check.screen_name,
        # required=True,
        help="Screen name of the user to target (uses the API)",
        metavar="SCREEN_NAME",
    )

    exclusive.add_argument(
        "-i",
        "--input-file",
        type=args_check.input_file,
        help="Path to a collection of tweets. Supports: JSONL, TXT",
        metavar="INPUT_FILE",
    )

    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        help="Limit the number of tweets to retrieve (default = no limit)",
        metavar="N",
    )

    parser.add_argument(
        "-o",
        "--output-path",
        type=args_check.output_path,
        help="Map output file",
        metavar="OUTPUT_FILE",
    )

    parser.add_argument(
        "-t",
        "--custom-title",
        type=str,
        help="Custom HTML title for map legend",
        metavar="CUSTOM_TITLE",
    )

    exclusive.add_argument(
        "--configure", action="store_true", help="Configure Twitter API credentials"
    )

    parser.add_argument(
        "-c",
        "--config-path",
        type=args_check.config_file,
        help="Path to configuration file",
        metavar="CONFIG_FILE",
    )

    args = parser.parse_args()

    tweetsmapper(args)
