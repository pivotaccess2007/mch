#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

import re
from service.malaria.params import *
from service.notification import *
from util.record import migrate, filter_data, fetch_summary, fetch_sm
from service.notification.notifications import Notification
from service.message.messages import NOTIFICATION
import datetime


class SM(object):
    """ Severe malaria report object"""

    def __init__(self, chw, text):
        self.text = text
        self.keyword = None
        self.national_id = None
        self.symptoms = None
        self.drugs = None
        self.codes = None
        self.intervention = None
        self.location = None
        self.status = None
        self.facility_response = None
        self.report = {}
        self.chw = chw
        self.errors = []
        self.response = ""
        self.table = 'malaria'
    
    def get_groups(self):
        try:
            #gs = re.search("(red|rar|risk|res|rem)\s+(\d+)\s?(.*)\s(ho|or|pr|ca|al|at|na|nr)\s?(.*)", self.text, re.IGNORECASE)
            gs = re.search("(smn)\s+(\d+)\s?(.*)", self.text, re.IGNORECASE)
            if not gs: 
                gs = re.search("(smr)\s+(\d+)\s?(.*)\s?(HO|HC|HP)\s?(PS|DTH)\s?(NR|RR)\s?(.*)", self.text, re.IGNORECASE)
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

    def get_national_id(self):
        try:
            m1 = self.get_groups()[1] 
            self.national_id = m1.strip()    
        except Exception, e:
            print e
        return self.national_id

    def get_codes(self):
        try:
            m2 = self.get_groups()[2]
            self.codes = [ x.strip() for x in m2.split(' ') if x]     
        except Exception, e:
            print e
        return self.codes

    def get_symptoms(self):
        try:
            m2 = self.get_groups()[2]
            sy = re.compile("(TDR|ARS|AL4|AL2|AL3|AL1|NDM)", re.IGNORECASE).split(m2)
            if self.keyword in ['SMR']:
                sy = re.compile("(PR\s|NA|CA|AL|AT)", re.IGNORECASE).split(m2) 
            self.symptoms = [ x.strip() for x in sy[0].split(' ') if x.upper() in KEYS.keys()]     
        except Exception, e:
            print e
        return self.symptoms

    def get_drugs(self):
        try:
            m2 = self.get_groups()[2]
            dr = re.compile("(DHM|NFM|JAM|RDM|HEM|COM|UNM|SCM|PRM|ANM|RVM|WUM)", re.IGNORECASE).split(m2) 
            self.drugs = [ x.strip() for x in dr[len(dr)-1].split(' ') if x.upper() in DRUGS.keys()]     
        except Exception, e:
            print e
        return self.drugs

    def get_intervention(self):
        try:
            m2 = self.get_groups()[2]
            it = re.compile("(DHM|NFM|JAM|RDM|HEM|COM|UNM|SCM|PRM|ANM|RVM|WUM)", re.IGNORECASE).split(m2)
            #symps = [ x.strip() for x in m2.split(it[len(it)-1])[0].split(' ') if x.upper() in KEYS.keys()]
            #if symps != self.symptoms: self.symptoms = symps
            self.intervention = [ x.strip() for x in it[len(it)-1].split(' ') if x.upper() in INTERVENTION.keys()]   
        except Exception, e:
            print e
        return self.intervention

    def get_location(self):
        try:
            m3 = self.get_groups()[3] 
            self.location = m3.strip()     
        except Exception, e:
            print e
        return self.location

    def get_status(self):
        try:
            m4 = self.get_groups()[4] 
            self.status = m4.strip()     
        except Exception, e:
            print e
        return self.status

    def get_facility_response(self):
        try:
            m5 = self.get_groups()[5] 
            self.facility_response = m5.strip()     
        except Exception, e:
            print e
        return self.facility_response    

    def get_report(self):
        try:
            #TODO
            self.get_keyword()
            self.get_national_id()
            self.get_codes()
            self.get_symptoms()
            self.get_drugs()
            self.get_intervention()
            self.get_location()
            self.get_status()
            self.get_facility_response()
            self.errors, self.report = self.get_fields()
            self.response = self.get_response()
            
        except Exception, e:
            print e
        return self.report


    def get_fields(self):
        errors, fields = [],{}
        try:
            self.report = {
                              'national_id' : self.national_id,
                              'user_phone' :  self.chw.telephone,
                              'user_pk' :  self.chw.indexcol,
                              'role_pk' : self.chw.role_pk,
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

            for s in self.symptoms:
                if s.upper() in KEYS.keys(): self.report.update( {'symptom_%s' %s.lower() : s})
                else:
                    if s: errors.append(('invalid_code', s))
                    else: pass

            if self.keyword in ['SMN']:
                for s in self.drugs:
                    if s.upper() in DRUGS.keys(): self.report.update( {'drug_%s' %s.lower() : s})
                    else:
                        if s: errors.append(('invalid_code', s))
                        else: pass

            if self.keyword in ['SMR']:
                for s in self.intervention:                
                    if s.upper() in INTERVENTION.keys(): self.report.update( {'intervention_%s' %s.lower() : s})
                    else:
                        if s: errors.append(('invalid_code', s))
                        else: pass
                
            if self.location and self.keyword in ['SMR']:
                if self.location.upper() in LOCATION.keys():
                    self.report.update({'location': self.location})
                else: errors.append(('invalid_code', self.location))

            if self.status and self.keyword in ['SMR']:
                if self.status.upper() in STATUS.keys(): self.report.update({'status': self.status})
                else: errors.append(('invalid_code', self.status))

            if self.facility_response and self.keyword in ['SMR']:
                if self.facility_response.upper() in FACILITY_RESPONSE_STATUS.keys():
                    self.report.update({'facility_response': self.facility_response})
                else: errors.append(('invalid_code', self.facility_response))
            print self.codes
            for c in self.codes:
                if c not in self.symptoms + self.drugs + self.intervention: errors.append(('invalid_sequence', c)) 
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

            if  not self.national_id:
                response += " %s" %  RESPONSE['nid_missing'][self.chw.language_code.lower()]
                self.errors.append(('nid_missing', ""))
            if  len(self.national_id) != 16:
                response += " %s" %  RESPONSE['invalid_nid'][self.chw.language_code.lower()]
                self.errors.append(('invalid_nid', ""))
            if not self.symptoms:
                response += " %s" %  RESPONSE['missing_symptoms'][self.chw.language_code.lower()]
                self.errors.append(('missing_symptoms', ""))
            if self.keyword == "SMN":
                if not self.drugs:
                    response += " %s" %  RESPONSE['missing_drugs'][self.chw.language_code.lower()]
                    self.errors.append(('missing_drugs', ""))
            if self.keyword == "SMR":
                if not self.intervention:
                    response += " %s" %  RESPONSE['missing_intervention'][self.chw.language_code.lower()]
                    self.errors.append(('missing_intervention', ""))
                if not self.location:
                    response += " %s" %  RESPONSE['missing_location'][self.chw.language_code.lower()]
                    self.errors.append(('missing_location', ""))
                if not self.status:
                    response += " %s" %  RESPONSE['missing_status'][self.chw.language_code.lower()]
                    self.errors.append(('missing_status', ""))
                if not self.facility_response:
                    response += " %s" %  RESPONSE['missing_response'][self.chw.language_code.lower()]
                    self.errors.append(('missing_response', ""))
            
            if self.errors:
                codes, seqs = [], []
                for err in self.errors:
                    if err[0] == 'invalid_code': codes.append(err[1])
                for err in self.errors:
                    if err[0] == 'invalid_sequence': seqs.append(err[1])

                if codes:   response += RESPONSE['invalid_code'][self.chw.language_code.lower()] % {'codes': ', '.join(codes)} 
                if seqs:   response += RESPONSE['invalid_sequence'][self.chw.language_code.lower()] % {'codes': ', '.join(seqs)}
                if  not (seqs or codes): response += " %s" % RESPONSE['unknown_error'][self.chw.language_code.lower()]                 
                response += " %s" % HELP[self.keyword][self.chw.language_code.lower()]
            else:
                if not response:    response = RESPONSE[self.keyword][self.chw.language_code.lower()] % {'nid' : self.national_id}
            """
            if self.count_notifs() != self.count_results() and self.keyword in ['SMN']:
                self.errors.append(('unresponded_report', self.national_id))
                response = RESPONSE['unresponded_report'][self.chw.language_code.lower()] % {'nid': self.national_id}
            if self.count_notifs() == self.count_results() and self.keyword in ['SMR']:
                self.errors.append(('report_to_respond', self.national_id))
                response = RESPONSE['report_to_respond'][self.chw.language_code.lower()] % {'nid': self.national_id}

            if self.get_sm_notif() and self.keyword in ['SMN']:
                self.errors.append(('unresponded_report', self.national_id))
                response = RESPONSE['unresponded_report'][self.chw.language_code.lower()] % {'nid': self.national_id}
            if not self.get_sm_notif() and self.keyword in ['SMR']:
                self.errors.append(('report_to_respond', self.national_id))
                response = RESPONSE['report_to_respond'][self.chw.language_code.lower()] % {'nid': self.national_id}"""

            if not response:
                response = RESPONSE["invalid_report"][self.chw.language_code.lower()]
                response += " %s" % HELP[self.keyword][self.chw.language_code.lower()]
                self.errors.append(('invalid_report', ""))

        except Exception, e:
            print "Error SM: %s" % e
            pass
        return response


    def process(self):
        try:
            is_sm = False
            report = self.get_report()
            for s in self.symptoms:
                if s.upper() in KEYS.keys():
                    is_sm = True
                    break
            if is_sm == False: return False
            #print "REPORT: %s" % report
            if  self.report and not self.errors:
                filters = {}
                for k in self.report.keys(): filters.update({ k+' = %s' : self.report[k]})
                old = filter_data(self.table, filters)
                if not ( old and old[0].created_at.date() == datetime.date.today()):
                    notif = self.get_sm_notif()
                    if notif and self.keyword == 'SMR':
                        migrate(self.table, {'indexcol': notif.indexcol, 'result': True})
                        self.report.update({'notif': notif.indexcol})
                    migrate(self.table, self.report)            
                notif = self.send_notifications()
            
            return True
        except Exception, e:
            print "ERROR: %s" % e
            pass
        return False


    def count_notifs(self):
        try:
            total = fetch_summary(table = self.table, 
                                    cnds = {'national_id = %s': self.national_id, 'keyword = %s' : 'SMN'},
                                    cols = ['COUNT(*) AS total'], exts = {}
                                    )[0].total
            return total
        except Exception, e:
            pass
        return 0

    def count_results(self):
        try:
            total = fetch_summary(table = self.table, 
                                    cnds = {'national_id = %s': self.national_id, 'keyword = %s' : 'SMR'},
                                    cols = ['COUNT(*) AS total'], exts = {}
                                    )[0].total
            return total
        except Exception, e:
            pass
        return 0

    def get_sm_notif(self):
        smn = None
        try:
            smn = fetch_sm(self.national_id,filters = {'keyword = %s' : 'SMN', 'result IS NULL': ''})
            return smr
        except Exception, e:
            pass
        return smn


    def send_notifications(self):
        try:
            #TODO
            """ message here is a dictionary of message in three language"""
            if self.report.get('keyword') == 'SMN':
                message = NOTIFICATION.get('SMN')
                cmd = Notification( message = message, chw = self.chw, national_id = self.national_id, ntype = "Severe Malaria Notification")
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
                cmd.notify_level('NATION', 'HQ', self.chw.facility_pk )
                #cmd.notify_level_by_email('NATION', 'HQ', self.chw.nation_pk)
                return True
            if self.report.get('status') == 'DTH':
                message = NOTIFICATION.get('DTH')
                cmd = Notification( message = message, chw = self.chw, national_id = self.national_id, ntype = "Severe Malaria Death")
                cmd.notify_level('HC', 'CLN', self.chw.facility_pk )
                cmd.notify_level('HC', 'HOHC', self.chw.facility_pk )
                cmd.notify_level('HC', 'EHO', self.chw.facility_pk )
                cmd.notify_level('HC', 'SUP', self.chw.facility_pk )
                cmd.notify_level('HD', 'LOG', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'SUP', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'CLN', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'DCLN', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'DNUR', self.chw.referral_facility_pk )
                cmd.notify_level('HD', 'HODI', self.chw.referral_facility_pk )
                cmd.notify_level('NATION', 'HQ', self.chw.facility_pk )
                #cmd.notify_level_by_email('NATION', 'HQ', self.chw.nation_pk)
                return True 
        except Exception, e:
            print e
        return False




