#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

import re
from service.message.messages import NOTIFICATION


class WHO(object):
    """ WHO report object"""

    def __init__(self, chw, text):
        self.text = text
        self.chw = chw
        self.response = ""
    
    def get_response(self):
        response = ""
        try:
            user = self.chw
            response = NOTIFICATION["WHO"][self.chw.language_code.lower()]
            response = response % { 'role' : user.role_name, 'phone': user.telephone, 'dst': user.district_name, 'hd':  user.referral_name, 'hc':  user.facility_name, 'sec': user.sector_name, 'cel': user.cell_name, 'vil': user.village_name}
        except Exception, e:
            print "Error WHO: %s" % e
            pass
        return response


    def process(self):
        try:
            self.response = self.get_response()
            return True
        except Exception, e:
            print "ERROR: %s" % e
            pass
        return False




