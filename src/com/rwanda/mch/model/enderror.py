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
from util.record import migrate, fetch_summary, fetch_enderror, fetch_table, fetch_table_by_location
from exception.mch_critical_error import MchCriticalError
from model.enduser import Enduser
import datetime


class Enderror(RSMSRWObj):
    """A Enderror report from RapidSMS. Enderrors have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'enderror'

    def __init__(self, telephone, error_code, message, created_at = datetime.datetime.now()):
        """Return a Enderror object which code is *error_code* done by user of telephone *telephone* """
        self.user_phone     = telephone
        self.error_code     = error_code
        self.message        = message
        self.created_at     = created_at


    def get(self):
        """ Retrieve a enderror object and return enderror record """
        try:
            err = fetch_enderror(self.user_phone, self.error_code, self.created_at)
            return err
        except:
            raise MchCriticalError(Exception('Enderror cannot be fetched'))
        return False

    def save(self, user = None):
        """ Save a enderror object and return indexcol """
        try:
            FIELDS = self.__dict__
            if not user: user   = Enduser.get_active_user(self.user_phone)
            if user:
                FIELDS.update({
                                    "user_pk":  user.indexcol, 
                                    "nation_pk":    user.nation_pk,
                                    "province_pk":  user.province_pk,
                                    "district_pk":  user.district_pk,
                                    "referral_facility_pk": user.referral_facility_pk,
                                    "facility_pk":  user.facility_pk,
                                    "sector_pk":    user.facility_pk,
                                    "cell_pk":  user.facility_pk,
                                    "village_pk":   user.facility_pk, 
                                })
            err = migrate(Enderror._table, FIELDS)
            return err
        except Exception, e:
            print e
            raise MchCriticalError(Exception('Enderror cannot be saved'))
        return False

    @staticmethod
    def record_enderrors(chw, message, errors):
        try:
            for err in errors:
                rcd = Enderror(chw.telephone, err[0], message)
                rcd.save(user = chw)
        except Exception, e:
            pass
        return False

    @staticmethod
    def fetch_enderrors(cnds, cols, exts):
        return fetch_summary(Enderror._table, cnds, cols, exts)

    @staticmethod
    def fetch_log_enderrors(cnds, cols):
        return fetch_table(Enderror._table, cnds, cols)

    @staticmethod
    def fetch_enderrors_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Enderror._table, curr_cnds, cols, group_by))
        return data
