#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

import json

from StringIO import StringIO
import gzip
import urllib2
from urllib2 import URLError

class IatiBaseMiner():

    def __init__(self, connection):

        self.connection = connection
        
    def fetch_json_data_from_web_service(self, url, key = 'value'):

        try:
            req = urllib2.Request(url)
            req.add_header('Accept-encoding', 'gzip')
            response = urllib2.urlopen(req)

            buf = StringIO(response.read())
            #f = gzip.GzipFile(fileobj=buf)
            the_page = buf.read()

            s = json.loads(the_page)
            
            return s[key]

        except URLError, urle:

            if hasattr(urle, 'reason'):
                print urle.reason
            else:
                print urle.__str__()
                
    def fetch_xml_data_from_web_service(self, url):

        try:
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)

            buf = StringIO(response.read())
            the_page = buf.read()
            
            return the_page

        except URLError, urle:

            if hasattr(urle, 'reason'):
                print urle.reason
            else:
                print urle.__str__()                
