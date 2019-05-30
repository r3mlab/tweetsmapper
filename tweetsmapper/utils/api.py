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
API Actions
"""

import logging
import os
import configparser
import tweepy
from tqdm import tqdm

from tweetsmapper.utils import results

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("tweetsmapper-api")


def check_keys_env():
    """Check if API credentials are defined through environment variables."""
    env_vars = [
        "CONSUMER_KEY",
        "CONSUMER_SECRET",
        "ACCESS_TOKEN",
        "ACCESS_TOKEN_SECRET",
    ]

    if all(variable in os.environ for variable in env_vars):
        log.debug("All credentials environment variables are defined")
        return True
    else:
        return False
        log.debug("Environmental variables missing or incomplete")


def authenticate(keys):
    """Configure the Twitter API."""
    auth = tweepy.OAuthHandler(keys["consumer_key"], keys["consumer_secret"])
    auth.set_access_token(keys["access_token"], keys["access_token_secret"])
    twitter_api = tweepy.API(
        auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True
    )
    return twitter_api


def register_config(config_path):
    """Save the API credentials to a file."""
    log.debug("Registering API credentials")

    print("Please enter your Twitter API credentials.")
    consumer_key = input("Consumer key: ")
    consumer_secret = input("Consumer secret: ")
    access_token = input("Access Token: ")
    access_token_secret = input("Access Token Secret: ")

    twitter_api = authenticate(
        consumer_key, consumer_secret, access_token, access_token_secret
    )

    try:
        log.debug("Verifying credentials...")
        twitter_api.verify_credentials()
        log.info("Congratulations! Your credentials are valid.")

        profile = twitter_api.me().screen_name
        log.debug(f"API User: {profile}")

        config = configparser.ConfigParser()
        config.add_section(profile)
        config.set(profile, "consumer_key", consumer_key)
        config.set(profile, "consumer_secret", consumer_secret)
        config.set(profile, "access_token", access_token)
        config.set(profile, "access_token_secret", access_token_secret)

        # config_path = os.path.join(os.path.expanduser("~"), ".tweetsmapper")
        log.debug(f"Config will be written to {config_path}")
        with open(config_path, "w") as config_file:
            log.debug("Writing file...")
            config.write(config_file)
            log.info(
                f"\nTwitter API credentials for user {profile} have been stored in {config_path}"
            )
            log.info(
                "Your are free to move this file around and specify its path with -c"
            )

    except tweepy.error.TweepError as e:
        log.error(
            "Your API credentials are invalid.",
            "Please double check them and run the configuration utility again.",
            "(tweetsmapper --configure)",
        )
        log.debug(f"Error: {e}")


def validate_keys(twitter_api):
    """Verify the API credentials are correct."""
    log.debug("Checking credentials validity...")
    try:
        twitter_api.verify_credentials()
        log.debug("Credentials are valid.")
        return True
    except tweepy.error.TweepError as e:
        return False
        log.debug(f"Error: {e}")


def get_keys(config_path):
    """Get the api credentials from env variables or from a file.

    Priority is given to env variables, unless a custom config path is given."""
    log.debug("Getting API keys...")
    keys = {}
    if check_keys_env() and config_path is None:
        log.debug("Trying to get API keys from env vars")
        env = os.environ.get
        keys["consumer_key"] = env("CONSUMER_KEY")
        keys["consumer_secret"] = env("CONSUMER_SECRET")
        keys["access_token"] = env("ACCESS_TOKEN")
        keys["access_token_secret"] = env("ACCESS_TOKEN_SECRET")
        log.debug(f"Keys: {keys}")
    else:
        log.debug("Trying to get API keys from config file")
        config = configparser.ConfigParser()

        if config_path == None:
            log.debug(f"No custom config file specified")
            log.debug("Setting config file path to default")
            config_path = os.path.join(os.path.expanduser("~"), ".tweetsmapper")

        log.debug(f"Reading config file {config_path}...")
        config.read(config_path)
        profile = config.sections()[0]

        keys["consumer_key"] = config.get(profile, "consumer_key")
        keys["consumer_secret"] = config.get(profile, "consumer_secret")
        keys["access_token"] = config.get(profile, "access_token")
        keys["access_token_secret"] = config.get(profile, "access_token_secret")
        log.debug(f"Keys: {keys}")

    return keys


def configure(config_path):
    """Configure API credentials."""
    try:
        register = "yes"

        # Check existing credentials
        if config_path == None:
            config_path = os.path.join(os.path.expanduser("~"), ".tweetsmapper")

            if check_keys_env() or os.path.exists(config_path):
                if check_keys_env():
                    log.info("Environment variables detected")
                elif os.path.exists(config_path):
                    log.info(f"Configuration file detected: {config_path}")

                    keys = get_keys(config_path)

                    log.info(f"Consumer Key: {keys['consumer_key']}")
                    log.info(f"Consumer Secret: {keys['consumer_secret']}")
                    log.info(f"Access Token: {keys['access_token']}")
                    log.info(f"Access Token Secret: {keys['access_token_secret']}")

                    twitter_api = authenticate(keys)

                    if validate_keys(twitter_api):
                        if check_keys_env():
                            log.info(
                                "Valid configuration for user {} found in environment variables.".format(
                                    twitter_api.me().screen_name, config_path
                                )
                            )
                            register = "no"
                        elif os.path.exists(config_path):
                            log.info(
                                "Valid configuration for user {} found at {}".format(
                                    twitter_api.me().screen_name, config_path
                                )
                            )
                            replace = input(
                                "Would you like to replace this configuration? (y/n): "
                            )
                            if replace.lower() not in ["y", "yes"]:
                                register = "no"
                            else:
                                log.debug("Checking if we get keys from env...")
                                if check_keys_env():
                                    log.info("Logging error...")
                                    log.error(
                                        "Your API credentials are invalid."
                                        "\n"
                                        "Please check your environment variables and try again."
                                    )
                                    register = "no"
                                elif os.path.exists(config_path):
                                    log.error(
                                        f"Your API credentials are invalid. Reconfiguring...\n"
                                    )

                                    if register == "yes":
                                        register_config(config_path)
    except KeyboardInterrupt:
        log.critical("\n\rExiting Twitter API configuration utility...")


def get_user_info(twitter_api, screen_name):
    """Fetch info about a user from the API."""
    try:
        log.debug(f"Trying to fetch info for user {screen_name}")
        user_info = twitter_api.get_user(screen_name=screen_name)
        log.debug(f"Fetched user info.")
        return user_info
    except tweepy.error.TweepError as error:
        try:
            message = error.args[0][0]["message"]
            log.error(f"Twitter error: {message}")
            if message in ["Could not authenticate you.", "Bad Authentication data."]:
                log.info(
                    "Please check your API credentials "
                    "or run tweetsmapper --configure to register them."
                )
        except TypeError:
            log.error(f"Twitter error: {error}")

        raise SystemExit(1)


def download_tweets(twitter_api, screen_name, limit):
    """Download tweets from the API and filter those containing geo information."""

    log.info(f"Trying to download last {limit} tweets for user {screen_name}...")

    log.debug("Checking if user exists...")

    log.debug("Starting to download tweets...")
    tweets_list = tweepy.Cursor(
        twitter_api.user_timeline, screen_name=screen_name, tweet_mode="extended"
    ).items(limit)

    geo_tweets = []
    try:
        count = 0
        for tweet in tqdm(tweets_list, unit=" tweets", total=limit):
            count += 1
            if results.is_geo(tweet):
                geo_tweets.append(tweet)
        if count != limit:
            log.info(f"Could only fetch {count} tweets.")
    except tweepy.error.TweepError as error:
        log.error(f"Twitter error: {error}")
        raise SystemExit(1)

    return geo_tweets


def chunks(list, chunk_size):
    """Yield successive chunks from a list."""
    for i in range(0, len(list), chunk_size):
        yield list[i : i + chunk_size]


def hydrate(ids_list, twitter_api):
    log.info("Hydrating tweets...")
    try:
        pbar = tqdm(unit=" tweets", total=len(ids_list))
        all_statuses = []
        for chunk in chunks(ids_list, 100):
            statuses = twitter_api.statuses_lookup(chunk, tweet_mode="extended")
            all_statuses.extend(statuses)
            pbar.update(len(chunk))
        pbar.close()
        return all_statuses
    except tweepy.error.TweepError as error:
        log.error(f"Twitter error: {error}")
        raise SystemExit(1)
