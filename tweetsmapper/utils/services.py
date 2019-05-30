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
Search services
"""

from_coordinates = [
    {
        "name": "Bing Maps",
        "countries": ["all"],
        "link": "https://www.bing.com/maps?&cp={lat}~{lon}&lvl=20&sty=a&w=100%",
        "logo_css_class": "bing-logo",
    },
    {
        "name": "Descartes Labs",
        "countries": ["all"],
        "link": "https://search.descarteslabs.com/?layer=landsat-8_v3_rgb_2013-2017#lat={lat}&lng={lon}&skipTut=true&zoom=17",
        "logo_css_class": "descartes-logo",
    },
    {
        "name": "Here",
        "countries": ["all"],
        "link": "https://wego.here.com/?map={lat},{lon},18,satellite&x=ep",
        "logo_css_class": "here-logo",
    },
    {
        "name": "Google Maps",
        "countries": ["all"],
        "link": "https://maps.google.com/?t=k&q={lat}, {lon}",
        "logo_css_class": "googlemaps-logo",
    },
    {
        "name": "EOS Landviewer",
        "countries": ["all"],
        "link": "https://eos.com/landviewer/?lat={lat}&lng={lon}&z=16",
        "logo_css_class": "landviewer-logo",
    },
    {
        "name": "Mapbox",
        "countries": ["all"],
        "link": "https://labs.mapbox.com/bites/00145/#12/{lat}/{lon}",
        "logo_css_class": "mapbox-logo",
    },
    {
        "name": "Mapillary",
        "countries": ["all"],
        "link": "https://www.mapillary.com/app/?lat={lat}&lng={lon}&z=18.123926367677527&p=&mapStyle=mapbox_satellite",
        "logo_css_class": "mapillary-logo",
    },
    {
        "name": "OpenStreetCam",
        "countries": ["all"],
        "link": "https://openstreetcam.org/map/@{lat},{lon},18z",
        "logo_css_class": "openstreetcam-logo",
    },
    {
        "name": "OpenStreetMap",
        "countries": ["all"],
        "link": "https://www.openstreetmap.org/#map=18/{lat}/{lon}",
        "logo_css_class": "openstreetmap-logo",
    },
    {
        "name": "SentinelHub",
        "countries": ["all"],
        "link": "https://apps.sentinel-hub.com/eo-browser/?lat={lat}&lng={lon}&zoom=18",
        "logo_css_class": "sentinelhub-logo",
    },
    {
        "name": "SnapMap",
        "countries": ["all"],
        "link": "https://map.snapchat.com/@{lat},{lon},18z",
        "logo_css_class": "snapchat-logo",
    },
    {
        "name": "Wikimapia",
        "countries": ["all"],
        "link": "https://wikimapia.org/#lang=en&lat={lat}&lon={lon}&z=18&m=w",
        "logo_css_class": "wikimapia-logo",
    },
    {
        "name": "Yandex Maps",
        "countries": ["all"],
        "link": "https://yandex.com/maps/?l=sat&ll={lon},{lat}&z=19",
        "logo_css_class": "yandexmaps-logo",
    },
    {
        "name": "Zillow",
        "countries": ["US", "CA"],
        "link": "https://www.zillow.com/homes/for_sale/globalrelevanceex_sort/{lat},{lon}/15_zm/",
        "logo_css_class": "zillow-logo",
    },
    {
        "name": "ZoomEarth",
        "countries": ["all"],
        "link": "https://zoom.earth/#{lat},{lon},18z,sat",
        "logo_css_class": "zoomearth-logo",
    },
]

from_place = [
    {
        "name": "Bing Maps",
        "countries": ["all"],
        "link": "https://www.bing.com/maps?q={search}",
        "logo_css_class": "bing-logo",
    },
    {
        "name": "Google Maps",
        "countries": ["all"],
        "link": "https://www.google.com/maps?q={search}",
        "logo_css_class": "googlemaps-logo",
    },
    {
        "name": "OpenStreetMap",
        "countries": ["all"],
        "link": "https://www.openstreetmap.org/search?query={search}",
        "logo_css_class": "openstreetmap-logo",
    },
    {
        "name": "Twitter",
        "countries": ["all"],
        "link": "https://twitter.com/search?q=place:{place_id}",
        "logo_css_class": "twitter-logo",
    },
    {
        "name": "Wikimapia",
        "countries": ["all"],
        "link": "http://wikimapia.org/#search={search}",
        "logo_css_class": "wikimapia-logo",
    },
    {
        "name": "Yandex",
        "countries": ["all"],
        "link": "https://yandex.com/maps/?l=sat&mode=search&text={search}",
        "logo_css_class": "yandexmaps-logo",
    },
]
