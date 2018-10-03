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
from util.record import fetch_summary, fetch_birth, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError

class Birth(RSMSRWObj):
    """A Birth report of RapidSMS. Births have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'birth'

    def __init__(self, national_id, birth_date, child_number):
        """Return a Birth object which birth_date is *birth_date* """
        self.national_id    = national_id
        self.birth_date     = birth_date
        self.child_number   = child_number
        self.table = Birth._table


    def get_or_create(self, orm, obj):
        """ Retrieve a child object and return child record """
        try:
            chi = fetch_birth(self.national_id, self.birth_date, self.child_number)
            if chi:
                obj.FIELDS.update({'indexcol': chi.indexcol})
            self.save(orm, obj)
            return self.get()
        except:
            raise MchCriticalError(Exception('Child cannot be fetched'))
        return False

    def get(self):
        """ Retrieve a child object and return child record """
        try:
            chi = fetch_birth(self.national_id, self.birth_date, self.child_number)
            return chi
        except:
            raise MchCriticalError(Exception('Child cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a child object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            return ref
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Child cannot be saved'))
        return False

    @staticmethod
    def fetch_births(cnds, cols, exts):
        return fetch_summary(Birth._table, cnds, cols, exts)


    @staticmethod
    def fetch_log_births(cnds, cols):
        return fetch_table(Birth._table, cnds, cols)

    @staticmethod
    def fetch_births_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Birth._table, curr_cnds, cols, group_by))
        return data
