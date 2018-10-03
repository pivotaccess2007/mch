# -*- coding: utf-8 -*-
#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

from model.rsmsrwobj import RSMSRWObj
from model.enduser import Enduser
from util.record import fetch_simcard, fetch_facility, fetch_facilities, fetch_facility_table, fetch_table_cols, migrate, fetch_location_level
from sms.api.smser import Smser


class Facility(RSMSRWObj):
    """An facility of RapidSMS with a telephone number. Facilitys have the
    following properties:

    Attributes:
        name: A string representing the name used to request for the facility.
        fosa code: A facility code tracking the facility.
    """

    _table = 'facility'

    def __init__(self, code):
        """Return an facility object """
        self.code = self.code
        self.table = Facility._table

    @staticmethod
    def get_or_create( data):
        try:
            code = data.get('code')
            fac  = Facility.get_facility(code)
            if not fac:
                #print "SAVE DATA: ", data 
                migrate(Facility._table, data)
                fac = Facility.get_facility(code)
                facs = fetch_facilities()
                if not fac:    return ("Facility has failed to be created, try again.", None, facs)
                return ( 'Facility created', fac, facs)
            return ( 'Facility exists', fac, facs)
        except Exception, e:
            print e
            pass
        return ('Error', None, [])

    @staticmethod
    def update_facility(data):
        try:
            code = data.get('code')
            old_fac = Facility.get_facility(code)
            ## Check facility registered for the code
            if not old_fac:
                 return ( 'Facility does not exist with code %s' % (code) , None)
            else:
                data.update({"indexcol": old_fac.indexcol})
                #print "UPDATE DATA: ", data 
                migrate(Facility._table, data)
                fac = Facility.get_facility(code)
                if fac:
                    facs = fetch_facilities()                    
                    return ( 'Facility Updated', fac, facs)
                else:
                    return ( 'Facility with code %s cannot be updated, contact system administrator.' % (
                                                                        old_fac.code) , None, [])
            
        except Exception, e:
            print e
            pass
        return ('Error', None, [])

    @staticmethod
    def update_facility_info(data):
        """ Not all info is update here except few supplied data info"""
        try:
            old_fac = Facility.get_facility(data.get('code'))
            ## Check facility registered for the code
            if not old_fac:
                 return ( 'Facility does not exist with code %s' % ( data.get('code')) , None)
            else:
                #print "UPDATE DATA: ", data 
                data.update({'indexcol': old_fac.indexcol})
                migrate(Facility._table, data)
                return ( 'Facility updated', old_fac)            
        except Exception, e:
            print e
            pass
        return ('Error', None)


    @staticmethod
    def get_facility(code):
        return fetch_facility(code)

    @staticmethod
    def get_facility_type(code):
        return fetch_location_level(code)

    @staticmethod
    def get_facilities_summary(cnds, cols):
        return fetch_table_cols(Facility._table, cnds, cols)

    @staticmethod
    def fetch_facilities_table(cnds, cols):
        return fetch_facility_table(Facility._table, cnds, cols)

    



