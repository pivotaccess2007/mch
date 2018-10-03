#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"


from datetime import datetime, timedelta
from controller.main import RSMSRWController
from model.malaria import Malaria
from model.enduser import Enduser
from util import queries
from util.mch_util import makecol, makedict, give_me_table

class MalariaController(RSMSRWController):

    def __init__(self, navb):
        navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Malaria.fetch_malaria(cnds, cols, exts)[0]
        return total

    def get_patient_logs(self):
        cnds    = self.navb.conditions()
        nid     = None
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : '',
                     "(created_at) <= '%s'" % (self.navb.finish) : '',
                     "keyword = 'SMN'": ''})#; print cnds
        patient_logs, message = [], None
        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                          ('province_pk', 'Province'),
                                              ('district_pk', 'District'),
                                              ('referral_facility_pk', 'Hospital'),
                                              ('facility_pk', 'Health Centre'),
                                              ('sector_pk', 'Sector'),
                                              ('cell_pk', 'Cell'),
                                              ('village_pk', 'Village'),
                                              ('national_id', 'National ID'),
                                              ('user_phone',              'Reporter Phone'),                                          
                                              ('created_at', 'Submission Datetime'),
                                              ('indexcol', 'Message')
                                            ])

        markup.update({'action': lambda x, _, __: '<a href="/dashboards/diagnosisdash?id=%s">Fill Diagnosis Form %s</a>' % (x, x), })
        markup.update({'symptoms': lambda x, _, __: '%s' % (Malaria.get_report_symptoms(x)) })
        markup.update({'drugs': lambda x, _, __: '%s' % (Malaria.get_report_drugs(x)) })
        markup.update({'message': lambda x, _, __: '%s' % (Malaria.get_report_details(x)) })

        if self.navb.kw.get("nid"):
            nid = self.navb.kw.get('nid')
            cnds.update({'national_id = %s': nid})        
            dcols = [x[0] for x in cols]
            #print dcols, cnds
            patient_logs = Malaria.fetch_log_malaria(cnds, dcols)
        desc = "Patient SMN logs"
        return nid, desc, patient_logs, cols, markup, message

    def get_stats(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : '',
                     "(created_at) <= '%s'" % (self.navb.finish) : '',
                     "keyword = 'SMN'": ''})#;print cnds
        exts    = {
                    'smn': ('COUNT(*)', "keyword = 'SMN'"),
                    'smr': ('COUNT(*)', "keyword = 'SMR'")
                        }
        attrs   = [(makecol(x[0]), x[1]) for x in queries.MALARIA_DATA['attrs']]
        exts.update(dict([(makecol(x[0]), ('COUNT(*)', x[0])) for x in queries.MALARIA_DATA['attrs']]))#;print exts
        cols    = ['COUNT(*) AS total']
        nat     = Malaria.fetch_malaria(cnds, cols, exts)
        #print attrs, "NAT: ", nat[0].__dict__
        return [attrs, nat]

    def get_tables(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : '',
                     "(created_at) <= '%s'" % (self.navb.finish) : '',
                     "keyword = 'SMN'": ''})
        exts = {}
        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('has_gone_hc', 'Received at HC'),
                                              ('has_gone_hd', 'Received at DH'),
                                              ('province_pk', 'Province'),
                                              ('district_pk', 'District'),
                                              ('referral_facility_pk', 'Hospital'),
                                              ('facility_pk', 'Health Centre'),
                                              ('sector_pk', 'Sector'),
                                              ('cell_pk', 'Cell'),
                                              ('village_pk', 'Village'),
                                              ('national_id', 'National ID'),
                                              ('user_phone',              'Reporter Phone'),                                          
                                              ('created_at', 'Submission Datetime'),
                                              ('indexcol', 'Message')
                                            ])

        markup.update({'action': lambda x, _, __: '<a href="/dashboards/diagnosisdash?id=%s">Fill Diagnosis Form %s</a>' % (x, x), })
        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=smn&id=%s">View</a>' % (x), })
        markup.update({'has_gone_hc': lambda x, _, __: '%s' % ('<b style="color:red;">HC: NO</b>' if not x else '<b style="color:green;">HC: YES</b>') })
        markup.update({'has_gone_hd': lambda x, _, __: '%s' % ('<b style="color:red;">DH: NO</b>' if not x else '<b style="color:green;">DH: YES</b>') })
        markup.update({'symptoms': lambda x, _, __: '%s' % (Malaria.get_report_symptoms(x)) })
        markup.update({'drugs': lambda x, _, __: '%s' % (Malaria.get_report_drugs(x)) })
        markup.update({'message': lambda x, _, __: '%s' % (Malaria.get_report_details(x)) })
        
    
        DESCRI = []
        MALARIADICT = makedict(queries.MALARIA_DATA['attrs'])
        INDICS = [('all', 'total', 'Total')] + [(makecol(x[0]), x[0], x[1]) for x in queries.MALARIA_DATA['attrs']]
        attrs = []
        group = "Severe Malaria"
        title = "Severe Malaria Notifications"
        sc      = self.navb.kw.get('subcat')
        title, sc, group, attrs, nat, tabular, locateds, INDICS_HEADERS = ('', '', '', [], [], [],[],[])
        if self.navb.kw.get('subcat') and self.navb.kw.get('subcat') in [makecol(x[0]) for x in queries.MALARIA_DATA['attrs']]:
            sc = self.navb.kw.get('subcat')
            wcl = MALARIADICT.get(sc)
            cnds.update({wcl[0]: ''})
            INDICS = [(sc, wcl[0], wcl[1])] if wcl else []
            #print INDICS, MALARIADICT

        if self.navb.kw.get('view') == 'table' or self.navb.kw.get('view') != 'log' :
            group_by = []
            group_by += ['province_pk']  if self.navb.kw.get('nation') or not group_by else []
            group_by += ['district_pk'] if self.navb.kw.get('province') else []
            group_by += ['referral_facility_pk'] if self.navb.kw.get('district') else []
            group_by += ['facility_pk'] if self.navb.kw.get('hd') else [] 
            #print "\nGROUP BY: %s \n" % group_by
            LOCS = {'nation': self.navb.kw.get('nation'),
                    'province': self.navb.kw.get('province'),
                    'district': self.navb.kw.get('district'),
                    'hospital': self.navb.kw.get('hd'),
                    'location': self.navb.kw.get('hc')
                    }
            locateds = Malaria.fetch_malaria_by_location(cnds, group_by = group_by, INDICS = INDICS)
            #print [[y.__dict__ for y in x] for x in locateds]#, INDICS, LOCS, self.navb.locs()
            tabular = give_me_table(locateds, self.navb.locs(),  INDICS = INDICS, LOCS = LOCS)
            #print tabular

        INDICS_HEADERS = dict([ ( makecol(x[0]), x[2]) for x in INDICS])

        dcols = [x[0] for x in cols]
        nat = Malaria.fetch_log_malaria(cnds, dcols)
        #DESCRI.append((group, title))
        desc  = 'Severe malaria cases%s' % (' (%s)' % (self.navb.find_descr(DESCRI + [(makecol(x[0]), x[2]) for x in INDICS],
                                                                        sc or self.navb.kw.get('subcat')
                                                                    ) 
					                            )
                                    ) 
        #print title, group, attrs, "NAT: ", nat[0].__dict__
        return (title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS)

    def register_diagnosis(self):
        genders = Enduser.get_genders()
        locs    =   self.navb.locs()
        user    =   self.navb.user
        area_levels = Enduser.get_location_levels()
        message = None
        report  = None
        received = False
        #print self.navb.kw
        if self.navb.kw.get('id'):
            try:    report = Malaria.get_report(indexcol = self.navb.kw.get('id'))
            except Exception, e:
                print e
                pass

        if self.navb.kw.get("nid") and self.navb.kw.get('pk') and (self.navb.kw.get('hd') or self.navb.kw.get('hc')):
            print self.navb.kw
            nid = self.navb.kw.get('nid')
            report = Malaria.get_report(indexcol = self.navb.kw.get('pk'))
            formdata = report.__dict__#; print "REPORT: ", formdata
            if self.navb.kw.get('hc'):
                #print "FORMDATA: ",formdata
                pre_transfer_dot = []
                is_alive = False if (self.navb.kw.get('is_dead') and self.navb.kw.get('is_dead') == 'True') else True
                if self.navb.kw.get('artesunate'): pre_transfer_dot = [', '.join(pre_transfer_dot +[self.navb.kw.get('artesunate')])]
                if self.navb.kw.get('diazepam'): pre_transfer_dot = [', '.join(pre_transfer_dot +[self.navb.kw.get('diazepam')])]
                if self.navb.kw.get('phenobarbital'): pre_transfer_dot = [', '.join(pre_transfer_dot +[self.navb.kw.get('phenobarbital')])]
                formdata.update(
                                  {    
                                    "telephone": self.navb.kw.get('telephone'), 
                                    "household":      self.navb.kw.get('household'),
                                    "surname":      self.navb.kw.get('surname'),
                                    "given_name":   self.navb.kw.get('given_name'),
                                    "sex_pk":   self.navb.kw.get('sex'),
                                    "age" :  self.navb.kw.get('age'), 
                                  
                                    "hc_regno_code": self.navb.kw.get('hc_regno_code'), 
                                    "has_gone_hc" : True,
                                    "has_gone_hc_pk":  self.navb.kw.get('hc'),
                                    "hc_arrival_datetime":  self.navb.make_time(self.navb.kw.get('arrival_datetime')),
                                    "hc_user_pk": self.navb.kw.get('hc_user_pk'), 
                                    "hc_tdr_result": self.navb.kw.get('tdr'),
                                    "hc_bs_result": self.navb.kw.get('bs'),
                                    "hc_hemoglobin": self.navb.kw.get('hemoglobin'),
                                    "hc_blood_glucose": self.navb.kw.get('blood_glucose'),
                                    "hc_blood_group": self.navb.kw.get('blood_group'),
                                    "hc_transfered": bool(self.navb.kw.get('transfered')),
                                    "hc_ambulance": bool(self.navb.kw.get('ambulance')), 
                                    "hc_ambulance_departure": self.navb.kw.get('ambulance_departure'),
                                    "hc_pretransfer_treatment": pre_transfer_dot[0] if pre_transfer_dot else "",
                                    "hc_death": not is_alive,
                                    "is_alive": is_alive,
                                    "is_dead": not is_alive

                                }
                            )

            if self.navb.kw.get('hd'):
                #print "FORMDATA: ",formdata
                final_diagnostics = []
                is_alive = False if self.navb.kw.get('patient_status') and self.navb.kw.get('patient_status') == 'Dead' else True
                if self.navb.kw.get('cerebral_form'): final_diagnostics = [', '.join(final_diagnostics +[self.navb.kw.get('cerebral_form')])]
                if self.navb.kw.get('anemic_form'): final_diagnostics = [', '.join(final_diagnostics +[self.navb.kw.get('anemic_form')])]
                if self.navb.kw.get('sm_complication'): final_diagnostics=[', '.join(final_diagnostics +[self.navb.kw.get('sm_complication')])]
                if self.navb.kw.get('ma_comorbidities'): final_diagnostics=[', '.join(final_diagnostics+[self.navb.kw.get('ma_comorbidities')])]
                if self.navb.kw.get('no_ma_confirmed'): final_diagnostics=[', '.join(final_diagnostics +[self.navb.kw.get('no_ma_confirmed')])]
                formdata.update(
                                  {  
                                    "hd_regno_code": self.navb.kw.get('hd_regno_code'),     
                                    "has_gone_hd" : True,
                                    "has_gone_hd_pk":  self.navb.kw.get('hd'),
                                    "hd_arrival_datetime":  self.navb.make_time(self.navb.kw.get('arrival_datetime')),
                                    "hd_patient_status": self.navb.kw.get('patient_status'), 
                                    "hd_final_diagnostics": final_diagnostics[0] if final_diagnostics else "",
                                    "hd_death": not is_alive,
                                    "is_alive": is_alive,
                                    "is_dead": not is_alive

                                }
                            )

            #print "\nFORMDATA: ", formdata, "\n"
            saved = Malaria.update_report(formdata)
            if saved:   message = "Patient %s data updated successfully." % (nid)
            received = True
            self.navb.kw = {}

        else:
            if not report:  message = "Report not found"
            self.navb.kw = {}
        #print report, message
        return report, locs, user, genders, area_levels, message, received
