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
from util.record import fetch_summary, fetch_mother_departure, fetch_child_departure, fetch_table, fetch_table_by_location

class Departure(RSMSRWObj):
    """A departure report of RapidSMS. Departures have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'departure'

    def __init__(self, national_id, lmp = None, pregnancy_pk = None, birth_date = None, child_number = None):
        """Return a Departure  """
        self.national_id = national_id
        self.lmp = lmp
        self.pregnancy_pk = pregnancy_pk
        self.birth_date = birth_date
        self.child_number = child_number
        self.table = Departure._table

    def get_or_create(self, orm, obj):
        """ Retrieve a departure object and return departure record """
        try:
            dep = self.get()
            if dep:
                obj.FIELDS.update({'indexcol': dep.indexcol})
            self.save(orm, obj)
            return self.get()
        except:
            raise MchCriticalError(Exception('Departure cannot be saved and fetched'))
        return False

    def get(self):
        """ Retrieve a departure object and return departure record """
        try:
            dep = fetch_mother_departure(self.national_id, self.lmp)
            if self.birth_date and self.child_number:
                dep = fetch_child_departure(self.national_id, self.birth_date, self.child_number)
            return dep
        except:
            raise MchCriticalError(Exception('Departure cannot be fetched'))
        return False

    def save(self, orm, obj):
        """ Save a departure object and return indexcol """
        try:
            ref = orm.ORM.store(self.table, obj.FIELDS)
            return ref
        except:
            raise MchCriticalError(Exception('Departure cannot be saved'))
        return False

    @staticmethod
    def fetch_departures(cnds, cols, exts):
        return fetch_summary(Departure._table, cnds, cols, exts)

    @staticmethod
    def fetch_log_departures(cnds, cols):
        return fetch_table(Departure._table, cnds, cols)

    @staticmethod
    def fetch_departures_by_location(cnds, group_by = [], INDICS = []):
        data = []; print cnds, group_by, INDICS
        for INDIC in INDICS:
            #print "CNDS: ", cnds
            cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
            curr_cnds = {INDIC[1]: ''}
            if INDIC[1] == 'total':
                cols = group_by + ['COUNT (*) AS %s' % INDIC[0]]
                curr_cnds = {}           
            curr_cnds.update(cnds)
            #print cols
            data.append(fetch_table_by_location(Departure._table, curr_cnds, cols, group_by))
        return data
