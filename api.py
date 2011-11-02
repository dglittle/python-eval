
import logging
import os
from urlparse import urlparse
import random
import base64

from google.appengine.ext import blobstore
from google.appengine.ext.blobstore import *
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db
from google.appengine.ext.db import *
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.api import *
from google.appengine.api.images import *
from google.appengine.api.channel import *
from google.appengine.api import images
from google.appengine.api import taskqueue

from myutil import *

class MyHandler(webapp.RequestHandler):
    def get(self):
        self.go()
    def post(self):
        self.go()
    def go(self):
        ret = []
        def output(a):
            ret.append(str(a))
        exec(self.request.get("code")) in globals(), locals()
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write('\n'.join(ret))

application = webapp.WSGIApplication([
    ('/.*', MyHandler),
], debug = True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

