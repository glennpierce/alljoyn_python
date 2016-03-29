#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import os.path
import logging
import json
from daemon import Daemon

import bottle
from logging.handlers import RotatingFileHandler

from AllPlayController import AllPlayController

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


@bottle.error(404)
def error404(error):
    return 'Nothing here, sorry'


@bottle.error(500)
def error500(error):
    return 'Unknown Error'


@bottle.route('/favicon.ico')
def send_favicon():
    return bottle.static_file('favicon.ico', root=os.path.join(script_dir, 'static/'))


@bottle.route('/static/<filepath:path>')
def server_static(filepath):
    return bottle.static_file(filepath, root=os.path.join(script_dir, 'static/'))


@bottle.route('/get_devices', method=['GET'])
def get_devices():
    bottle.response.content_type = 'application/json'
    return json.dumps(allplayerController.GetPlayers())

@bottle.route('/create_zone', method='POST')
def create_zone():
    data = bottle.request.json
    devices = data.get('selected_devices', [])
    allplayerController.CreateZone(devices)
    return json.dumps({'return': 'ok'})

@bottle.route('/run', method='POST')
def run():
    data = bottle.request.json
    player = allplayerController.GetPlayer()
    if player.paused:
        player.Resume()
    else:
        player.PlayUrl(data['uri'])
    return json.dumps({'return': 'ok'})

@bottle.route('/adjust_volume', method='POST')
def adjust_volume():
    data = bottle.request.json
    device_id = data.get('device_id', None)
    volume = data.get('volume')
    allplayerController.SetVolume(device_id, volume)
    return json.dumps({'return': 'ok'})

@bottle.route('/stop')
def stop():
    player = allplayerController.GetPlayer()
    player.Stop()
    return json.dumps({'return': 'ok'})


@bottle.route('/pause')
def pause():
    player = allplayerController.GetPlayer()
    player.Pause()
    return json.dumps({'return': 'ok'})


@bottle.route('/', method=['GET'])
def default():
    return bottle.template('index', query=bottle.request['QUERY_STRING'])


class AllPlayServer(Daemon):

    def __init__(self, pidfile='/var/run/carnegopdf.pid', host="0.0.0.0", port=80, foreground=False):
        super(AllPlayServer, self).__init__(
            pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null')
        self.foreground = foreground
        self.host = host
        self.port = port

    def start(self):
        logging.info("starting allplayerserver")
        if self.foreground:
            return self.run()
        else:
            super(AllPlayServer, self).start()

    def shutdown(self):
        pass

    def stop(self):
        super(AllPlayServer, self).stop()

    def run(self):
        bottle.debug(True)

        app = bottle.default_app()

        logging.info(
            "started webserver host: %s port: %s", self.host, self.port)
        try:
            bottle.run(
                server='cherrypy', app=app, host=self.host, port=self.port, debug=True)
        except Exception, e:
            logging.critical("bottle: %s", e)
            sys.exit(1)


if __name__ == "__main__":

    usage = '''
            "usage: @
            "Examples"
            @ -d info -f -p 80 start
            @ --debug info --foreground --port 8882 start
            @ stop
            '''.replace('@', sys.argv[0])

    from optparse import OptionParser

    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--foreground", dest="foreground",
                      action="store_true", default=False, help="Run in foreground")
    parser.add_option("-v", "--verbose", dest="verbose",
                      action="store_true", default=False, help="Verbose logging")
    parser.add_option(
        "-p", "--port", dest="port", default=8882, help="Port to run on")
    (options, args) = parser.parse_args()

    logger = create_logger(
        foreground=options.foreground, verbose=options.verbose)

    server = AllPlayServer(
        '/var/run/allplayserver.pid', port=options.port, foreground=options.foreground)

    if len(args) != 1:
        print usage
        sys.exit(1)

    try:
        if args[0] == 'start':
            server.start()
        elif args[0] == 'stop':
            server.stop()
    except KeyboardInterrupt, e:
        logging.info("attempting to shut down")
        server.stop()
