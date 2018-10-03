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
from util.record import fetch_summary, fetch_mother, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError

class Mother(RSMSRWObj):
    """A mother report of RapidSMS. Pregnancies have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'mother'

    def __init__(self, national_id):
        """Return a Mother object which lmp is *lmp* """
        self.national_id = national_id
        self.table = Mother._table

    def get_or_create(self, orm, obj):
        """ Retrieve a mother object and return mother record """
        try:
            mth = fetch_mother(self.national_id)
            if mth:
                obj.FIELDS.update({'indexcol': mth.indexcol})
            self.save(orm, obj)
            return self.get()
        except:
            raise MchCriticalError(Exception('Mother cannot be fetched'))
        return False

    def get(self):
        """ Retrieve a mother object and return mother record """
        try:
            mth = fetch_mother(self.national_id)
            return mth
        except:
            raise MchCriticalError(Exception('Mother cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a mother object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            return ref
        except:
            raise MchCriticalError(Exception('Mother cannot be saved'))
        return False

    @staticmethod
    def fetch_mothers(cnds, cols, exts):
        return fetch_summary(Mother._table, cnds, cols, exts)


    @staticmethod
    def fetch_log_mothers(cnds, cols):
        return fetch_table(Mother._table, cnds, cols)

    @staticmethod
    def fetch_mothers_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Mother._table, curr_cnds, cols, group_by))
        return data
