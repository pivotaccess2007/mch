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
from util.record import fetch_summary, fetch_table, fetch_table_by_location, filter_data, fetch_report, fetch_resource, migrate
from exception.mch_critical_error import MchCriticalError
from service.malaria.params import DRUGS, KEYS, LOCATION, INTERVENTION, FACILITY_RESPONSE_STATUS, STATUS
from util.mch_util import parse_codes

class Malaria(RSMSRWObj):
    """A malaria report of RapidSMS. Malaria have the
    following properties:

    Attributes: TODO
        
    """

    _table = 'malaria'

    def __init__(self, national_id):
        """Return a malaria object which national_id is *national_id* """
        self.national_id = national_id
        self.table = Malaria._table

    @staticmethod
    def fetch_malaria(cnds, cols, exts):
        return fetch_summary(Malaria._table, cnds, cols, exts)

    @staticmethod
    def fetch_log_malaria(cnds, cols):
        return fetch_table(Malaria._table, cnds, cols)

    @staticmethod
    def fetch_malaria_by_location(cnds, group_by = [], INDICS = []):
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
            data.append(fetch_table_by_location(Malaria._table, curr_cnds, cols, group_by))
        return data

    @staticmethod
    def get_patient(national_id):
        filters = {'national_id = %s': national_id, "keyword = 'SMN'": ''}
        sort=('created_at', False)
        return filter_data(Malaria._table, filters = filters, sort = sort)

    @staticmethod
    def get_report(indexcol):
        filters = {'indexcol = %s': indexcol}
        return filter_data(Malaria._table, filters = filters)[0]

    @staticmethod
    def update_report(data):
        try:
            p = migrate(Malaria._table, data)
            return True
        except Exception, e:
            pass
        return False

    @staticmethod
    def get_report_symptoms(pk):
        message = ""
        try:
            record = fetch_report(Malaria._table, pk)
            report = fetch_resource(code = record.keyword)
            message = parse_codes(report, record, CODES = KEYS)
        except Exception,e :
            #print e
            pass
        return message


    @staticmethod
    def get_report_drugs(pk):
        message = ""
        try:
            record = fetch_report(Malaria._table, pk)
            report = fetch_resource(code = record.keyword)
            message = parse_codes(report, record, CODES = DRUGS)
        except Exception,e :
            #print e
            pass
        return message

    @staticmethod
    def get_report_details(pk):
        message = ""
        try:
            record = fetch_report(Malaria._table, pk)
            return record.message
            report = fetch_resource(code = record.keyword)
            if record.keyword == "SMN":
                message = "Report: %(keyword)s, NID: %(nid)s, SYMPTOMS: %(signs)s, DRUGS: %(drugs)s" % {'keyword': record.keyword,
                                            'nid': record.national_id, 'signs': parse_codes(report, record, CODES = KEYS),
                                            'drugs': parse_codes(report, record, CODES = DRUGS)}
            elif record.keyword == "SMR":
                message = "Report: %(keyword)s, NID: %(nid)s, SYMPTOMS: %(signs)s, INTERVENTION: %(intervention)s,\
                            LOCATION: %(location)s , STATUS: %(status)s, FACILITY RESPONSE: %(facility_response)s" % {
                                            'keyword': record.keyword,
                                            'nid': record.national_id, 'signs': parse_codes(report, record, CODES = KEYS),
                                            'intervention': parse_codes(report, record, CODES = INTERVENTION),
                                            'location': parse_codes(report, record, CODES = LOCATION),
                                            'status': parse_codes(report, record, CODES = STATUS),
                                            'facility_response': parse_codes(report, record, CODES = FACILITY_RESPONSE_STATUS)
                                        }
            else:
                message = record.message
        except Exception,e :
            #print e
            pass
        return message
