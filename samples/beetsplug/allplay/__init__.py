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
from flask import g, jsonify
from werkzeug.routing import BaseConverter, PathConverter
import os
import json
from .AllPlayController import AllPlayController

allplayerController = AllPlayController()

app = flask.Flask(__name__)
#app.url_map.converters['idlist'] = IdListConverter
#app.url_map.converters['query'] = QueryConverter


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


@app.route('/run', methods= ['POST'])
def run():
    data = request.get_json()
    player = allplayerController.GetPlayer()
    if player.paused:
        player.Resume()
    else:
        player.PlayUrl(data['uri'])
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
    player.Pause()
    return jsonify({'return': 'ok'})


@app.route('/tracks/')
def all_items():
    return jsonify(g.lib.items())


@app.route('/item/<int:item_id>/file')
def play_item(item_id):
    item = g.lib.get_item(item_id)
    response = flask.send_file(item.path, as_attachment=True,
                               attachment_filename=os.path.basename(item.path))
    response.headers['Content-Length'] = os.path.getsize(item.path)
    return response


@app.route('/')
def home():
    return flask.render_template('index.html')


# Plugin hook.
class AllPlayWebPlugin(BeetsPlugin):
    def __init__(self):
        super(AllPlayWebPlugin, self).__init__()
        self.config.add({
            'host': u'127.0.0.1',
            'port': 8337,
            'cors': '',
        })

        #self._log

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
