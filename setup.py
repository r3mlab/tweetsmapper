#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2019 r3mlab
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


from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

requirements = [
    "folium",
    "tweepy",
    "twint @ git+https://github.com/twintproject/twint.git@master#egg=twint",
    "tqdm",
    "twitter_text_python",
    "emoji",
]

setup(
    name="tweetsmapper",
    version="1.0",
    description="Generate Leaflet maps from geo-enabled tweets.",
    long_description_content_type="text/markdown",
    url="https://github.com/r3mlab/tweetsmapper",
    author="r3mlab",
    author_email="remlab@protonmail.com",
    packages=find_packages(exclude=["docs"]),
    python_requires=">=3.5",
    install_requires=requirements,
    license="GPLv3",
    entry_points={"console_scripts": ["tweetsmapper=tweetsmapper:main"]},
    zip_safe=False,
    include_package_data=True,
)
