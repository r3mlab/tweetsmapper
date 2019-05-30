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
Display, formatting, etc.
"""

import logging
import datetime
import os
import jinja2
import emoji
from ttp import ttp

from tweetsmapper.utils import services, resources_path
import pkg_resources

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("tweetsmapper-display")


def format_like(num):
    """Format an integer into Twitter like string."""
    if num > 999999:
        like_num = str(round(num, -6))[: len(str(num)) - 6] + "M"
    elif num > 999:
        like_num = str(round(num, -3))[: len(str(num)) - 3] + "K"
    else:
        like_num = num

    return like_num


def format_tweet_emojis(tweet_text):
    """Detect emojis in tweet and replace them with a Twemoji html code.

    This is needed to display the most recent unicode emojis,
    many of which are unsupported by web browsers."""
    emoji_template = '<img draggable="false" class="emoji" alt="{char}" src="https://twemoji.maxcdn.com/2/72x72/{fileroot}.png">'

    for e in emoji.UNICODE_EMOJI.keys():
        if e in tweet_text:
            esc_char = e.encode("unicode-escape").lower()
            esc_char_codes = esc_char.split(b"\\u")

            fileroot_codes = [
                x.decode("utf-8").replace("000", "") for x in esc_char_codes if x != b""
            ]
            fileroot = "-".join(fileroot_codes)

            emoji_html = emoji_template.format(char=e, fileroot=fileroot)
            tweet_text = tweet_text.replace(e, emoji_html)

    return tweet_text


def format_tweet_text(tweet_text):
    """Convert tweet text to html: add mentions, hashtags, emoji, links."""
    # Emoji support
    tweet_processed_text = format_tweet_emojis(tweet_text)
    # Mentions, hashtags, links
    tweet_processed_text = ttp.Parser().parse(tweet_processed_text).html
    # Links customization
    tweet_processed_text = tweet_processed_text.replace(
        "<a ", '<a target="_blank" rel="noreferrer" '
    )

    return tweet_processed_text


def get_template(template):
    """Wrapper for jinja2 template loading."""
    templates_dir = os.path.join(resources_path, "templates")
    file_loader = jinja2.FileSystemLoader(templates_dir)
    env = jinja2.Environment(loader=file_loader)
    return env.get_template(template)


def tweet_to_html(tweet, tweet_template):
    """Convert a Tweepy status object (tweet) to a Twitter-like HTML string."""
    if tweet.coordinates:
        search_services = services.from_coordinates
    else:
        search_services = services.from_place

    html = tweet_template.render(
        tweet=tweet,
        tweet_html_text=format_tweet_text(tweet.full_text),
        tweet_date_str=tweet.created_at.strftime("%H:%M - %b %d, %Y (UTC)"),
        tweet_favcount=format_like(tweet.favorite_count),
        services=services,
    )
    return html


def create_legend(legend_title, emoji):
    """Create HTML for the legend in LayerControl."""
    legend_template = get_template("legend.html.j2")
    legend = legend_template.render(
        title=legend_title,
        emoji=emoji,
        gen_datetime=datetime.datetime.utcnow().strftime("%d %b %Y %I:%M %p"),
        version=pkg_resources.get_distribution("tweetsmapper").version,
    )

    return legend


def create_title(string):
    """Create HTML for the <title> tag."""
    title = "{} - tweetsmapper v{}".format(
        string, pkg_resources.get_distribution("tweetsmapper").version
    )
    return title
