#!/usr/bin/env python
# encoding: utf-8
# vim: ts=2 expandtab

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

import cherrypy
import os, sys
import re
import subprocess

from util.mch_connection import APP_DATA, WEBAPP, FACILITIES
from util.record import fetch_facilities

class URLMapping(cherrypy.dispatch.Dispatcher):
  def __init__(self, mapper, *args, **kw):
    self.mapper = mapper
    super(URLMapping, self).__init__(*args, **kw)

  def __call__(self, path):
    gat = re.search(r'/static/(.*)', path)
    if gat:
      return super(URLMapping, self).__call__(path)
    return super(URLMapping, self).__call__(self.mapper.match(path))

def mch_main(argv):
  larg  = len(argv)
  if larg < 4:
    sys.stderr.write('%s templatedir staticdir staticpath [port] [host]\r\n' % (argv[0], ))
    return 1
  pth       = os.path.abspath(argv[1])
  stt       = argv[2]
  stp       = argv[3]
  FACILITIES = fetch_facilities()
  handler   = __import__(WEBAPP).Application(pth, stt, stp, APP_DATA, FACILITIES)
  def launch(hst, prt, *args):
    cherrypy.server.socket_host = hst
    cherrypy.server.socket_port = prt
    cherrypy.quickstart(handler, '/', {
      '/':  {
        'request.dispatch':   URLMapping(handler),
        'tools.sessions.on':  True
      },
      # '/static':{
      stp:{
        'tools.staticdir.on':   True,
        'tools.staticdir.root': os.path.abspath(stt),
        # 'tools.staticdir.root': pth,
        'tools.staticdir.dir':  ''
      }
    })
  
  hst = '0.0.0.0'
  prt = '8081'
  if larg == 5:
    prt = argv[4]
  if larg == 6:
    hst = argv[5]
  
  return launch(hst, int(prt))

if __name__ == '__main__':
  bottom  = sys.exit(mch_main(sys.argv))
