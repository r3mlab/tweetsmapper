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

from sys import version_info
from tweetsmapper import run


def main():
    """Entry point for the application script."""
    if version_info.major == "2":
        print("You appear to be running Python 2. tweetsmapper requires Python 3.")
    else:
        try:
            run.main()
        except KeyboardInterrupt:
            print("\rExiting tweetsmapper...")
            raise SystemExit(1)
