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


import sys
import os
import os.path
import logging
import json
from daemon import Daemon

import bottle
from logging.handlers import RotatingFileHandler

from AllPlayController import AllPlayController

"""A Web interface to beets."""
from __future__ import division, absolute_import, print_function

from beets.plugins import BeetsPlugin
from beets import ui
from beets import util
import beets.library
import flask
from flask import g
from werkzeug.routing import BaseConverter, PathConverter
import os
import json


script_dir, script_name = os.path.split(os.path.abspath(__file__))
bottle.TEMPLATE_PATH.append(script_dir)

allplayerController = AllPlayController()


def create_logger(foreground=False, verbose=False):
    logger = logging.getLogger()

    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if foreground:
        handler = logging.StreamHandler()
    else:
        handler = RotatingFileHandler(
            '/var/log/allplyserver.log', maxBytes=204800)

    logger.addHandler(handler)
    return logger


app = flask.Flask(__name__)
#app.url_map.converters['idlist'] = IdListConverter
#app.url_map.converters['query'] = QueryConverter


def resource_list(name):
    """Decorates a function to handle RESTful HTTP request for a list of
    resources.
    """
    def make_responder(list_all):
        def responder():
            return app.response_class(
                json_generator(list_all(), root=name),
                mimetype='application/json'
            )
        responder.__name__ = b'all_%s' % name.encode('utf8')
        return responder
    return make_responder


@app.before_request
def before_request():
    g.lib = app.config['lib']


@app.error(404)
def error404(error):
    return 'Nothing here, sorry'


@app.error(500)
def error500(error):
    return 'Unknown Error'


@app.route('/favicon.ico')
def send_favicon():
    return bottle.static_file('favicon.ico', root=os.path.join(script_dir, 'static/'))


@app.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root=os.path.join(script_dir, 'static/'))


@app.route('/get_devices', method=['GET'])
def get_devices():
    bottle.response.content_type = 'application/json'
    return json.dumps(allplayerController.GetPlayers())

@app.route('/create_zone', method='POST')
def create_zone():
    data = bottle.request.json
    devices = data.get('selected_devices', [])
    allplayerController.CreateZone(devices)
    return json.dumps({'return': 'ok'})

@app.route('/run', method='POST')
def run():
    data = bottle.request.json
    player = allplayerController.GetPlayer()
    if player.paused:
        player.Resume()
    else:
        player.PlayUrl(data['uri'])
    return json.dumps({'return': 'ok'})

@app.route('/adjust_volume', method='POST')
def adjust_volume():
    data = bottle.request.json
    device_id = data.get('device_id', None)
    volume = data.get('volume')
    allplayerController.SetVolume(device_id, volume)
    return json.dumps({'return': 'ok'})

@app.route('/stop')
def stop():
    player = allplayerController.GetPlayer()
    player.Stop()
    return json.dumps({'return': 'ok'})

@app.route('/pause')
def pause():
    player = allplayerController.GetPlayer()
    player.Pause()
    return json.dumps({'return': 'ok'})

@app.route('/tracks/')
@resource_list('items')
def all_items():
    return g.lib.items()

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