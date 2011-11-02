
from time import time
import hashlib
import random
from google.appengine.api import memcache
import string

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

def getRaw(o, key):
    return eval("o.__class__." + key + ".get_value_for_datastore(o)")

def getKey(x):
    if isinstance(x, Key):
        return x    
    if isinstance(x, db.Model):
        return x.key()
    error("could not get key from: " + str(x))

def myShuffle(a):
    random.shuffle(a)
    return a

def getJso(o, props):
    jso = dict([(p, eval('o.' + p)) for p in props])
    jso["key"] = str(o.key())
    return jso

def error(msg):
    raise BaseException(msg)

def myMemcache(key, func):
    val = memcache.get(key)
    if val is not None:
        return val
    else:
        val = func()
        memcache.set(key, val)
        return val

def randomId(n=20):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for r in range(n))

def myIndex(a, v):
    try:
        return a.index(v)
    except ValueError:
        return -1

def myRemove(a, v):
    try:
        a.remove(v)
    except ValueError:
        pass

def setAppend(a, v):
    if myIndex(a, v) < 0:
        a.append(v)

def mytime():
    return int(time.time() * 1000)

def tsv(data, fields):
    return "\n".join([
        "\t".join([row[f] for f in fields]) if row != 0 else "0"
        for row in data
    ])

# winner = winner's elo score
# loser = loser's elo score
# p = 0..1 (how sure are we that the winner won?)
# returns two values,
#   these are deltas that should be applied
#   to the elo scores of the winner and loser
def eloDeltas(winner, loser, p):
    Rw = winner
    Rl = loser
    
    Qw = 10**(Rw / 400)
    Ql = 10**(Rl / 400)
    
    Ew = Qw / (Qw + Ql)
    El = Ql / (Qw + Ql)
    
    Sw = 1
    Sl = 0
    
    K = 32 * p
    
    return (K * (Sw - Ew)), (K * (Sl - El))

def sha1(s):
    return hashlib.sha1(s).hexdigest()

