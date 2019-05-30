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
Map Actions
"""

import logging
import datetime
import os
import folium
from folium.plugins import MarkerCluster, FeatureGroupSubGroup
import jinja2

from tweetsmapper.utils import args_check, display, import_file, resources_path

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger("tweetsmapper-map")


def create():
    """Create the base Leaftlet map."""
    log.debug("Creating the Leaflet map...")
    tweets_map = folium.Map(
        # Start location
        [30, 0],
        tiles=None,  # Add tiles later so they don't show up on LayerControl
        max_bounds=True,
        zoom_start=2,
    )
    log.debug("Adding CartoDB tiles layer...")
    folium.raster_layers.TileLayer(
        tiles="Cartodb positron",
        attr=(
            'Tiles: <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, '
            '<a href="http://cartodb.com/attributions">CartoDB</a>'
        ),
        control=False,
        min_zoom=2,
    ).add_to(tweets_map)

    return tweets_map


def add_cluster(tweets_map):
    """Create a Leaflet MarkerCluster to hold all geo tweets."""
    with open(os.path.join(resources_path, "js", "create_cluster_icon.js")) as js_file:
        create_cluster_icon = js_file.read()

    log.debug("Creating MarkerCluster...")
    tweets_cluster = MarkerCluster(
        control=False,
        icon_create_function=create_cluster_icon,
        options={
            "showCoverageOnHover": False,
            "spiderfyDistanceMultiplier": 1.7,
            "spiderLegPolylineOptions": {
                "weight": 2,
                "color": "#1DA1F2",
                "opacity": 0.5,
            },
        },
    )
    tweets_map.add_child(tweets_cluster)

    return tweets_cluster


def find_centroid(coordinates):
    """Return the centroid of a bounding box."""
    lon_list = [point[0] for point in coordinates[0]]
    lat_list = [point[1] for point in coordinates[0]]
    centroid = (
        sum(lat_list) / float(len(lat_list)),
        sum(lon_list) / float(len(lon_list)),
    )
    return centroid


def add_marker(tweet, subgroup, popup_template):
    """Create a marker representing a tweet."""
    # Get coordinates
    if tweet.coordinates:
        lat, lon = (
            tweet.coordinates["coordinates"][1],
            tweet.coordinates["coordinates"][0],
        )
    else:
        lat, lon = find_centroid(tweet.place.bounding_box.coordinates)

    # Custom Icon
    twitter_icon = folium.features.CustomIcon(
        os.path.join(resources_path, "img", "marker.png"),
        icon_size=(36, 45),
        icon_anchor=(18, 45),
        popup_anchor=(0, -38),
    )
    # Add marker
    folium.Marker(
        location=[lat, lon],
        icon=twitter_icon,
        popup=folium.Popup(
            display.tweet_to_html(tweet, popup_template), parse_html=False
        ),
    ).add_to(subgroup)

    log.debug(
        "Added tweet {} to map. Place: {}, lat:{}, lon:{}".format(
            tweet.id_str,
            tweet.place.full_name if tweet.place else "None",
            tweet.coordinates["coordinates"][1] if tweet.coordinates else None,
            tweet.coordinates["coordinates"][0] if tweet.coordinates else None,
        )
    )


def add_tweets(geo_tweets, cluster, tweets_map):
    """Add all geo enabled tweets on the map."""

    # Define subgroups for LayerControl
    coords_count = sum(1 for t in geo_tweets if t.coordinates)
    place_count = len(geo_tweets) - coords_count
    coords_subgroup = FeatureGroupSubGroup(
        cluster, f"Tweets with coordinates ({coords_count})"
    )
    place_subgroup = FeatureGroupSubGroup(
        cluster, f"Tweets with place only ({place_count})"
    )

    # Load popup html template

    popup_template = display.get_template("popup.html.j2")

    # Map tweets
    for tweet in geo_tweets:
        subgroup = coords_subgroup if tweet.coordinates else place_subgroup

        add_marker(tweet=tweet, subgroup=subgroup, popup_template=popup_template)

    # Add subgroups to map
    for subgroup in [coords_subgroup, place_subgroup]:
        tweets_map.add_child(subgroup)


def add_info(tweets_map, args, geo_tweets):
    """Add contextual info to the map: legend title, timestamp, etc."""

    if args.custom_title:
        title = args.custom_title
        emoji = None
    elif args_check.input_source(args) == "api" or import_file.has_unique_author(
        geo_tweets
    ):
        title = "@" + geo_tweets[0].user.screen_name
        emoji = "user"
    else:
        title = os.path.basename(args.input_file)
        emoji = "file"

    legend_html = display.create_legend(title, emoji)
    tweets_map.get_root().html.add_child(folium.Element(legend_html))

    # HTML <title>
    tweets_map.get_root().header.add_child(
        folium.Element("<title>{}</title>".format(display.create_title(title)))
    )

    return tweets_map


def customize(tweets_map, args, geo_tweets):
    """Customize the Leaflet map: LayerControl, legend, additional CSS."""

    log.debug("Adding LayerControl...")
    # Adding LayerControl
    folium.LayerControl(position="bottomleft", collapsed=False).add_to(tweets_map)

    log.debug("Adding legend info...")
    # Adding legend info to map
    tweets_map = add_info(tweets_map, args, geo_tweets)

    # Additional CSS
    log.debug("Including additional CSS...")
    css_dir = os.path.join(resources_path, "css")
    for css_file_path in [x for x in os.listdir(css_dir)]:
        with open(os.path.join(css_dir, css_file_path)) as css_file:
            css = css_file.read()
            tweets_map.get_root().header.add_child(
                folium.Element(f"<style>{css}</style>")
            )

    return tweets_map


def save(tweets_map, args):
    """Save the Leaflet map as an HTML file."""

    # Define base filename
    if args_check.input_source(args) == "user":
        title = args.screen_name
    elif args_check.input_source(args) == "file":
        title = os.path.splitext(os.path.basename(args.input_file))[0]

    default_filename = "{}-{}.html".format(
        title, datetime.datetime.utcnow().strftime("%Y%m%d-%H%M")
    )

    # Saving file
    if args.output_path:
        if os.path.isdir(args.output_path):
            output_path = os.path.join(args.output_path, default_filename)
        else:
            output_path = args.output_path
    else:
        output_path = default_filename

    abs_output_path = os.path.abspath(output_path)
    log.debug(f"Trying to save map to {abs_output_path}...")
    tweets_map.save(output_path)
    log.info(f"Map saved to {abs_output_path}")
