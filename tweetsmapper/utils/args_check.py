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
Argument checks
"""

import logging
import os
import argparse


logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("tweetsmapper-argscheck")


def screen_name(screen_name):
    """Remove @ in screen name if needed."""
    if screen_name.startswith("@"):
        log.debug("Removing @ in target screen_name")
        screen_name.replace("@", "")
    return screen_name


def input_file(path):
    """Checks if the input file has valid path and filetype."""

    if os.path.exists(path) is False:
        raise argparse.ArgumentTypeError(f"Could not find file {path}")
    log.debug("Found input file: {path}")
    suffix = os.path.splitext(path)[1].lower()[1:]
    supported_filetypes = ["jsonl", "txt"]

    if suffix in supported_filetypes:
        return path
    else:
        raise argparse.ArgumentTypeError(
            "Cannot process file {}. Supported extensions: {}".format(
                path, " ".join(supported_filetypes)
            )
        )


def output_path(path):
    """Validate output path."""
    if os.path.dirname(path) == "" or os.path.isdir(os.path.dirname(path)):
        log.debug(f"Output path {path} is correct.")
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid output path.")


def input_source(args):
    """Check if we should map tweets for a username or from a file."""
    if args.screen_name:
        return "user"
    elif args.input_file:
        return "file"
    else:
        log.critical(
            "Please specify a username (-n user) or a collection of tweets (-i tweets.jsonl) to start,"
            "\n"
            "or see the help: tweetsmapper -h"
        )
        raise SystemExit(1)


def config_file(path):
    """Check if configuration file exists."""
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f"{path} is not a valid path.")
    log.debug(f"Found configuration file: {path}")
