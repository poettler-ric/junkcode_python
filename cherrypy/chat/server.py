#!/usr/bin/env python

import cherrypy
import json
import os.path

class Controller(object):
    def __init__(self):
        self.messages = []

    @cherrypy.expose()
    @cherrypy.tools.redirect(url='/static/chat.html', internal=False)
    def index(self):
        return "you shouldn't see this"

    @cherrypy.expose()
    def postMessage(self, user, message, lastId=-1):
        lastId = int(lastId)
        self.messages.append({'user': user, 'message': message})
        return json.dumps(self.messages[lastId+1:])

    @cherrypy.expose()
    def getMessage(self, lastId=-1):
        lastId = int(lastId)
        return json.dumps(self.messages[lastId+1:])

    @cherrypy.expose()
    def clear(self):
        self.messages = []
        return json.dumps(self.messages)

current_dir = os.path.dirname(os.path.abspath(__file__))

config = {
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': os.path.join(current_dir, 'static'),
    },
}

cherrypy.tree.mount(Controller(), '/', config)
cherrypy.engine.start()
cherrypy.engine.block()
