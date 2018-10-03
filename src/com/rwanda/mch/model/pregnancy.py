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
from util.record import fetch_summary, fetch_pregnancy, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError

class Pregnancy(RSMSRWObj):
    """A pregnancy report of RapidSMS. Pregnancies have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'pregnancy'

    def __init__(self, national_id, lmp):
        """Return a Pregnancy object which lmp is *lmp* """
        self.lmp = lmp
        self.national_id = national_id
        self.table = Pregnancy._table

    def get_or_create(self, orm, obj):
        """ Retrieve a Pregnancy object and return mother record """
        try:
            preg = fetch_pregnancy(self.national_id, self.lmp)
            if preg:
                obj.FIELDS.update({'indexcol': preg.indexcol})
            self.save(orm, obj)
            return self.get()
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Pregnancy cannot be retrieved or saved'))
        return False


    def get(self):
        """ Retrieve a pregnancy object and return pregnancy record """
        try:
            preg = fetch_pregnancy(self.national_id, self.lmp)
            return preg
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Pregnancy Report cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a pregnancy object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            return ref
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Pregnancy Report cannot be saved'))
        return False

    @staticmethod
    def fetch_pregnancies(cnds, cols, exts):
        return fetch_summary(Pregnancy._table, cnds, cols, exts)

    @staticmethod
    def fetch_log_pregnancies(cnds, cols):
        return fetch_table(Pregnancy._table, cnds, cols)

    @staticmethod
    def fetch_pregnancies_by_location(cnds, group_by = [], INDICS = []):
        data = []#; print cnds, group_by, INDICS
        for INDIC in INDICS:
            #print "CNDS: ", cnds
            cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
            curr_cnds = {INDIC[1]: ''}
            if INDIC[1] == 'total':
                cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
                curr_cnds = {}
            curr_cnds.update(cnds)
            data.append(fetch_table_by_location(Pregnancy._table, curr_cnds, cols, group_by))
        return data

