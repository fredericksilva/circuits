#!/usr/bin/env python

from urllib2 import build_opener, Request

from circuits import handler, Component

from circuits.web import Controller
from circuits.web.tools import gzip
from circuits.web.utils import decompress

class Gzip(Component):

    @handler("response", priority=1.0)
    def response(self, event, response):
        event[0] = gzip(response)

class Root(Controller):

    def index(self):
        return "Hello World!"

def test(webapp):
    gzip = Gzip()
    gzip.register(webapp)

    request = Request(webapp.server.base)
    request.add_header("Accept-Encoding", "gzip")
    opener = build_opener()

    f = opener.open(request)
    s = decompress(f.read())
    assert s == "Hello World!"

    gzip.unregister()