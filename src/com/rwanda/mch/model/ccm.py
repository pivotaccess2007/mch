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
from util.record import fetch_summary, fetch_ccm, fetch_cmr, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError

class CCM(RSMSRWObj):
    """A CCM report of RapidSMS. CCMs have the
    following properties:

    Attributes: TODO
        
    """

    _table1 = 'ccm'
    _table2 = 'cmr'

    def __init__(self,  national_id, birth_date, child_number):
        """Return a CCM object which ccm_date is *ccm_date* """
        self.table1 = CCM._table1
        self.table  = CCM._table1
        self.table2 = CCM._table2
        self.national_id    = national_id
        self.birth_date     = birth_date
        self.child_number   = child_number        


    def get_or_create(self, orm, obj):
        """ Retrieve a CCM object and return CCM record """
        try:
            ccm = fetch_ccm(self.national_id, obj.UNIQUE_QUERY)
            if ccm:
                obj.FIELDS.update({'indexcol': ccm.indexcol})
            self.save(orm, obj)
            return self.get(obj.UNIQUE_QUERY)
        except Exception, e:
            raise MchCriticalError(Exception('CCM cannot be saved and fetched'))
        return False

    def get(self, filters):
        """ Retrieve a CCM object and return CCM record """
        try:
            ccm = fetch_ccm(self.national_id, filters)
            return ccm
        except Exception, e:
            print e
            raise MchCriticalError(Exception('CCM cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a CCM object and return indexcol """
        try:
            ref = orm.ORM.store(self.table1, obj.FIELDS)
            return ref
        except Exception, e:
            #print e
            raise MchCriticalError(Exception('CCM cannot be saved'))
        return False


    def get_or_create_cmr(self, orm, obj):
        """ Retrieve a CMR object and return CMR record """
        try:
            cmr = fetch_cmr(self.national_id, obj.UNIQUE_QUERY)
            if cmr:
                obj.FIELDS.update({'indexcol': cmr.indexcol})
            self.save_cmr(orm, obj)
            #print obj.UNIQUE_QUERY
            return self.get_cmr(obj.UNIQUE_QUERY)
        except Exception, e:
            raise MchCriticalError(Exception('CMR cannot be saved and fetched'))
        return False

    def get_cmr(self, filters):
        """ Retrieve a CMR object and return CMR record """
        try:
            cmr = fetch_cmr(self.national_id, filters)
            return cmr
        except Exception, e:
            print e
            raise MchCriticalError(Exception('CMR cannot be fetched'))
        return False

    def save_cmr(self, orm, obj):
        """ Save a CMR object and return indexcol """
        try:
            #print obj.FIELDS
            ref = orm.ORM.store(self.table2, obj.FIELDS)
            return ref
        except Exception, e:
            #print e
            raise MchCriticalError(Exception('CMR cannot be saved'))
        return False


    @staticmethod
    def fetch_ccms(cnds, cols, exts):
        return fetch_summary(CCM._table1, cnds, cols, exts)

    @staticmethod
    def fetch_cmrs(cnds, cols, exts):
        return fetch_summary(CCM._table2, cnds, cols, exts)

    @staticmethod
    def fetch_log_ccms(cnds, cols):
        return fetch_table(CCM._table1, cnds, cols)

    @staticmethod
    def fetch_ccms_by_location(cnds, group_by = [], INDICS = []):
        data = []#; print cnds, group_by, INDICS
        for INDIC in INDICS:
            #print "CNDS: ", cnds
            cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
            curr_cnds = {INDIC[1]: ''}
            if INDIC[1] == 'total':
                cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
                curr_cnds = {}           
            curr_cnds.update(cnds)
            #print cols
            data.append(fetch_table_by_location(CCM._table1, curr_cnds, cols, group_by))
        return data


    @staticmethod
    def fetch_log_cmrs(cnds, cols):
        return fetch_table(CCM._table2, cnds, cols)

    @staticmethod
    def fetch_cmrs_by_location(cnds, group_by = [], INDICS = []):
        data = []#; print cnds, group_by, INDICS
        for INDIC in INDICS:
            #print "CNDS: ", cnds
            cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
            curr_cnds = {INDIC[1]: ''}
            if INDIC[1] == 'total':
                cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
                curr_cnds = {}           
            curr_cnds.update(cnds)
            #print cols
            data.append(fetch_table_by_location(CCM._table2, curr_cnds, cols, group_by))
        return data
