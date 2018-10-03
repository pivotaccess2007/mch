#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

import re
from service.stock.metrics import *
from util.record import migrate, filter_data
from service.notification.notifications import Notification
from service.message.messages import NOTIFICATION

class ST(object):
    """ Malaria drug stock out report object"""

    def __init__(self, chw, text):
        self.text = text
        self.keyword = None
        self.drugs = None
        self.report = {}
        self.chw = chw
        self.errors = []
        self.table = 'stock'
    
    def get_groups(self):
        try:
            gs = re.search("(rso|so|ss)\s?(.*)", self.text, re.IGNORECASE)
            return gs.groups()
        except Exception, e:
            print e
        return None

    def get_keyword(self):
        try:
            m0 = self.get_groups()[0] 
            self.keyword = m0.strip().upper()    
        except Exception, e:
            print e
        return self.keyword

    def get_drugs(self):
        try:
            m1 = self.get_groups()[1] 
            self.drugs = [ x.strip() for x in m1.split(' ') if x.upper() in DRUGS.keys()]     
        except Exception, e:
            print e
        return self.drugs


    def get_report(self):
        try:
            #TODO
            self.get_keyword()
            self.get_drugs()
            self.errors, self.report = self.get_fields()
            
        except Exception, e:
            print e
        return self.report


    def get_fields(self):
        errors, fields = [],{}
        try:
            self.report = {
                              'user_phone' :  self.chw.telephone,
                              'user_pk' :  self.chw.indexcol,
                              'role_pk': self.chw.role_pk,
                              'nation_pk' :  self.chw.nation_pk,
                              'province_pk' :  self.chw.province_pk,
                              'district_pk' :  self.chw.district_pk,
                              'referral_facility_pk' :  self.chw.referral_facility_pk,
                              'facility_pk' :  self.chw.facility_pk,
                              'sector_pk' :  self.chw.sector_pk,
                              'cell_pk' :  self.chw.cell_pk,
                              'village_pk' :  self.chw.village_pk,
                              'keyword': self.keyword,
                              'message': self.text
                            }

            for s in self.drugs:
                if s.upper() in DRUGS.keys(): self.report.update( {'drug_%s' %s.lower() : s})
                else:
                    if s: errors.append(('invalid_code', s))
                    else: pass
             
            return (errors, self.report)
        except Exception, e:
            errors.append(('unknown_error', e))
            pass
        return (errors, fields)


    def get_response(self):
        response = ""
        try:
            if not self.keyword:
                response = RESPONSE["invalid_report"][self.chw.language_code.lower()]
                self.errors.append(('invalid_report', ""))
                return response

            if not self.drugs:
                response += " %s" %  RESPONSE['missing_drugs'][self.chw.language_code.lower()]
                self.errors.append(('missing_drugs', ""))
            if self.errors:
                codes = []
                for err in self.errors:
                    if err[0] == 'invalid_code': codes.append(err[1])
                if codes:   response += " %s" %  RESPONSE['invalid_code'][self.chw.language_code.lower()] % {'codes': ', '.join(codes)} 
                else: response += " %s" %  RESPONSE['unknown_error'][self.chw.language_code.lower()]
                response += " %s" % HELP[self.keyword][self.chw.language_code.lower()]
            else:
                if not response:
                    response += " %s" %  RESPONSE[self.keyword][self.chw.language_code.lower()]
        except Exception, e:
            print "Error ST: %s" % e
            pass
        return response


    def process(self):
        try:
            is_st = False
            report = self.get_report()
            for s in self.drugs:
                if s.upper() in DRUGS.keys():
                    is_st = True
                    break
            if is_st == False: return False
            #print "REPORT: %s" % report
            if  self.report and not self.errors:
                filters = {}
                for k in self.report.keys(): filters.update({ k+' = %s' : self.report[k]})
                old = filter_data(self.table, filters)
                if not old: migrate(self.table, self.report)

                notif = self.send_notifications()

            return True
        except Exception, e:
            print "ERROR: %s" % e
            pass
        return False


    def send_notifications(self):
        try:
            #TODO
            """ message here is a dictionary of message in three language"""
            drugs = ", ".join( DRUGS[d]['en'] for d in self.drugs)
            #print drugs
            if self.report.get('keyword') == 'RSO':
                message = NOTIFICATION.get('RSO')
                cmd = Notification( message = message, chw = self.chw, drugs = drugs, ntype = "Risk of Stock Out Notification")
                cmd.notify_level('HC', 'CLN', self.chw.facility_pk )
                cmd.notify_level('HC', 'HOHC', self.chw.facility_pk )
                cmd.notify_level('HC', 'EHO', self.chw.facility_pk )
                cmd.notify_level('HC', 'SUP', self.chw.facility_pk )
                cmd.notify_level('HD', 'LOG', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'SUP', self.chw.referral_facility_pk )
                cmd.notify_level('CEL', 'CECO', self.chw.cell_pk )
                #cmd.notify_level_by_email('NATION', 'HQ', self.chw.nation_pk)
                return True
            if self.report.get('keyword') == 'SO':
                message = NOTIFICATION.get('SO')
                cmd = Notification( message = message, chw = self.chw, drugs = drugs, ntype = "Stock Out Notification")
                cmd.notify_level('HC', 'CLN', self.chw.facility_pk )
                cmd.notify_level('HC', 'HOHC', self.chw.facility_pk )
                cmd.notify_level('HC', 'SUP', self.chw.facility_pk )
                cmd.notify_level('HC', 'EHO', self.chw.facility_pk )
                cmd.notify_level('HD', 'LOG', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'SUP', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'CLN', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'DCLN', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'DNUR', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'HODI', self.chw.referral_facility_pk )
                cmd.notify_level('CEL', 'CECO', self.chw.cell_pk )
                cmd.notify_level('DST', 'DHU', self.chw.district_pk )
                cmd.notify_level('DST', 'PDM', self.chw.district_pk )
                cmd.notify_level('DST', 'PHD', self.chw.district_pk )                
                cmd.notify_level('NATION', 'HQ', self.chw.facility_pk )
                #cmd.notify_level_by_email('NATION', 'HQ', self.chw.nation_pk)
                return True 
            if self.report.get('keyword') == 'SS':
                message = NOTIFICATION.get('SS')
                cmd = Notification( message = message, chw = self.chw, drugs = drugs, ntype = "Stock Supplied")
                cmd.notify_level('HC', 'CLN', self.chw.facility_pk )
                cmd.notify_level('HC', 'HOHC', self.chw.facility_pk )
                cmd.notify_level('HC', 'SUP', self.chw.facility_pk )
                cmd.notify_level('HC', 'EHO', self.chw.facility_pk )
                cmd.notify_level('HD', 'LOG', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'SUP', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'CLN', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'DCLN', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'DNUR', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'HODI', self.chw.referral_facility_pk )
                cmd.notify_level('CEL', 'CECO', self.chw.cell_pk )
                cmd.notify_level('DST', 'DHU', self.chw.district_pk )
                cmd.notify_level('DST', 'PDM', self.chw.district_pk )
                cmd.notify_level('DST', 'PHD', self.chw.district_pk )                
                cmd.notify_level('NATION', 'HQ', self.chw.facility_pk )
                #cmd.notify_level_by_email('NATION', 'HQ', self.chw.nation_pk)
                return True 
        except Exception, e:
            print e
        return False


