"""ulogserver.py -

Main webserver for ulogserver

Usage:
  ulogserver.py [--port=PORT] [--host=HOST]

Options:
  --port=PORT  [default: 8888]

"""

from __future__ import print_function
import uuid
import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.gen
import logging
import tornadoredis
import os
import re
import json
from redis import Redis
#######################################################
# create logger with 'spam_application'
logger = logging.getLogger('tornado app')
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

#######################################################
host_port = 8888;
host_ip   = '192.168.1.13'
redis_host_ip = host_ip
log_url   = 'log'
R = Redis()

def websocket_processing(msg):
    logger.debug('websocket_processing(channel={0})'.format(msg))
    try:
        logger.debug('websocket_processing{0}'.format(data))
        data = simplejson.loads(msg)
        cmd = data.get('cmd',None)

        if cmd == "pub":
            log.debug("pub(param = {0})".format(data['param']))            
            R.publish(data['param']['chan'], data['param']['msg'])
    except:
        pass

class MainHandler(tornado.web.RequestHandler):
    def get(self):        
        self.render("main.html")

class PageHandler(tornado.web.RequestHandler):
    def get(self,html_file):
        if '.html' not in html_file.lower():
            html_file += '.html'

        fullfile = os.path.join(os.path.dirname(__file__), "templates",html_file)        
        if os.path.isfile(fullfile):
            self.render(html_file)
        else:
            self.write("Requested page not found {0}".format(html_file))

class CmdHandler(tornado.web.RequestHandler):
    def get(self, cmd):
        logger.info('CmdHandler.get({0}):'.format(cmd))
        R.publish('log',cmd)
        self.write('CmdHandler.get')

class MessageHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super(MessageHandler, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def open(self, chan):
        self.sub_channel = chan
        logger.debug('MessageHandler.open(channel={0})'.format(chan))
        self.listen()

    @tornado.gen.engine
    def listen(self):
        self.client = tornadoredis.Client(redis_host_ip)
        self.client.connect()
        yield tornado.gen.Task(self.client.subscribe, self.sub_channel)
        self.client.listen(self.on_message)

    def on_message(self, msg):        
        logger.debug('MessageHandler.on_message({0})'.format)
        R.publish('ws',msg)
        if isinstance(msg,unicode):            
            websocket_processing(msg)
        else:
            if msg.kind == 'message':        
                self.write_message(msg.body)
            if msg.kind == 'disconnect':
                # Do not try to reconnect, just send a message back
                # to the client and close the client connection
                self.write_message('The connection terminated '
                                   'due to a Redis server error.')
                self.close()

    def on_close(self):
        logger.debug("on_close()")
        if self.client.subscribed:
            self.client.unsubscribe(self.sub_channel)
            self.client.disconnect()

class EchoWebSocket(tornado.websocket.WebSocketHandler):
    def open(self, chan):
        logger.debug("WebSocket opened")

    def on_message(self, message):
        logger.debug("on_message = {}".format(message))
        self.write_message('\"OK\"')

    def on_close(self):        
        logger.debug("WebSocket closed")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r'/', MainHandler),
                (r'/page/(?P<html_file>.*)', PageHandler),
                (r'/cmd/(?P<cmd>.*)', CmdHandler),
                #(r'/websocket/(?P<chan>.*)', MessageHandler),
                (r'/websocket/(?P<chan>.*)', EchoWebSocket),
                ]
        
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            xsrf_cookies=False,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    logger.info('Runint: ' + __name__)
    app = Application()
    app.listen(host_port)    
    tornado.ioloop.IOLoop.instance().start()
