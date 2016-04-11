#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2016, Glenn Pierce.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

from __future__ import division, absolute_import, print_function

import sys
import os
import os.path
from beets.plugins import BeetsPlugin
from beets import ui
from beets import util
import beets.library
import flask
from flask import g, jsonify, request
from werkzeug.routing import BaseConverter, PathConverter
import os
import json
from .AllPlayController import AllPlayController

allplayerController = AllPlayController()

app = flask.Flask(__name__)


@app.before_request
def before_request():
    g.lib = app.config['lib']

@app.route('/get_devices', methods=['GET'])
def get_devices():
    return jsonify({'devices':allplayerController.GetPlayers()})


@app.route('/create_zone', methods= ['POST'])
def create_zone():
    data = request.get_json()
    devices = data.get('selected_devices', [])
    allplayerController.CreateZone(devices)
    return jsonify({'return': 'ok'})


@app.route('/play', methods= ['POST'])
def play():
    data = request.get_json()
    allplayerController.SetQueue(data['queue'])
    player = allplayerController.GetPlayer()
    state, position = player.GetPlayingState()
    if state == "paused":
        player.Resume()
    else:
        allplayerController.PlayQueue()
    return jsonify({'return': 'ok'})


@app.route('/playtrack', methods= ['POST'])
def playtrack():
    data = request.get_json()
    player = allplayerController.GetPlayer()
    state, position = player.GetPlayingState()
    if state == "paused":
        player.Resume()
    else:
        allplayerController.PlayTrack(data['track_id'])
    return jsonify({'return': 'ok'})


@app.route('/adjust_volume', methods=['POST'])
def adjust_volume():
    data = request.get_json()
    device_id = data.get('device_id', None)
    volume = data.get('volume')
    allplayerController.SetVolume(device_id, volume)
    return jsonify({'return': 'ok'})


@app.route('/stop')
def stop():
    player = allplayerController.GetPlayer()
    player.Stop()
    return jsonify({'return': 'ok'})


@app.route('/pause')
def pause():
    player = allplayerController.GetPlayer()
    state, position = player.GetPlayingState()
    if state.lower() == "paused":
        player.Resume()
    else:
        player.Pause()
    return jsonify({'return': 'ok'})


@app.route('/update', methods= ['POST'])
def update():
    data = request.get_json()
    item = data['item']
    db_item = g.lib.get_item(item['id'])
    db_item.update(item)
    db_item.try_sync(True, False)

    return jsonify({'return': 'ok'})


@app.route('/tracks/')
def tracks():
    tracks = []
    for item in g.lib.items():
        tracks.append(
                {
                   'id': item.id,
                   'title': item.title,
                   'path': item.path,
                   'artist': item.artist,
                   'album': item.album
                }
            )

    return jsonify({'items': tracks})  # g.lib.items()


@app.route('/showtracks.html')
def showtracks():
    return flask.render_template('showtracks.html')


@app.route('/showqueue.html')
def showqueue():
    return flask.render_template('showqueue.html')


@app.route('/trackfile/<int:item_id>')
def trackfile(item_id):
    item = g.lib.get_item(item_id)
    response = flask.send_file(item.path, as_attachment=False)
    response.headers['Content-Length'] = os.path.getsize(item.path)
    return response


@app.route('/track.html')
def track():
    return flask.render_template('track.html')


@app.route('/queuetrack.html')
def queuetrack():
    return flask.render_template('queuetrack.html')


@app.route('/')
def home():
    return flask.render_template('index.html')


@app.route('/showmetadata.html')
def showmetadata():
    return flask.render_template('showmetadata.html')


# Plugin hook.
class AllPlayWebPlugin(BeetsPlugin):
    def __init__(self):
        super(AllPlayWebPlugin, self).__init__()
        self.config.add({
            'host': u'127.0.0.1',
            'port': 8337,
            'cors': '',
        })

    def commands(self):
        cmd = ui.Subcommand('allplay', help=u'start an AllPlay Web interface')
        cmd.parser.add_option(u'-d', u'--debug', action='store_true',
                              default=False, help=u'debug mode')

        def func(lib, opts, args):
            args = ui.decargs(args)
            if args:
                self.config['host'] = args.pop(0)
            if args:
                self.config['port'] = int(args.pop(0))

            app.config['lib'] = lib
            # Enable CORS if required.
            if self.config['cors']:
                self._log.info(u'Enabling CORS with origin: {0}',
                               self.config['cors'])
                from flask.ext.cors import CORS
                app.config['CORS_ALLOW_HEADERS'] = "Content-Type"
                app.config['CORS_RESOURCES'] = {
                    r"/*": {"origins": self.config['cors'].get(str)}
                }
                CORS(app)
            # Start the web application.
            app.run(host=self.config['host'].get(unicode),
                    port=self.config['port'].get(int),
                    debug=opts.debug, threaded=True)
        cmd.func = func
        return [cmd]


# {
#       "lyrics": "",
#       "album_id": 168,
#       "albumstatus": "Official",
#       "disctitle": "",
#       "year": 2002,
#       "month": 0,
#       "channels": 2,
#       "genre": "",
#       "original_day": 0,
#       "disc": 1,
#       "mb_trackid": "4076fdb8-0e08-4703-bbf8-10a10a222cf2",
#       "composer": "",
#       "mtime": 1459259549,
#       "albumdisambig": "",
#       "samplerate": 44100,
#       "albumartist_sort": "Firin' Squad, The",
#       "id": 1954,
#       "size": 0,
#       "album": "The Very Best of Pure R&B: The Winter Collection",
#       "mb_artistid": "382f1005-e9ab-4684-afd4-0bdae4ee37f2",
#       "bitdepth": 0,
#       "disctotal": 2,
#       "title": "I Ain't Mad At Cha",
#       "media": "CD",
#       "artist_sort": "2Pac",
#       "mb_albumid": "bab24056-7b76-43ad-a192-3b46cf20a5ee",
#       "comments": "",
#       "acoustid_fingerprint": "",
#       "rg_album_gain": null,
#       "script": "Latn",
#       "mb_releasegroupid": "bb30dbd0-ed8e-3597-b43a-441bbe64ec78",
#       "acoustid_id": "",
#       "rg_album_peak": null,
#       "albumartist_credit": "The Firin' Squad",
#       "catalognum": "TTVCD3303",
#       "added": 1459259546.586,
#       "original_month": 0,
#       "format": "MP3",
#       "track": 15,
#       "comp": 0,
#       "encoder": "",
#       "initial_key": null,
#       "rg_track_gain": null,
#       "bitrate": 128000,
#       "day": 0,
#       "original_year": 2002,
#       "tracktotal": 40,
#       "language": "eng",
#       "artist": "2Pac",
#       "asin": "B00007E7GL",
#       "mb_albumartistid": "b93784a2-7a97-45e3-b93a-be3d57e0448a",
#       "bpm": 0,
#       "label": "Telstar TV",
#       "length": 258.489625,
#       "albumartist": "The Firin' Squad",
#       "albumtype": "compilation",
#       "artist_credit": "2Pac",
#       "country": "GB",
#       "rg_track_peak": null,
#       "grouping": ""
#     },
