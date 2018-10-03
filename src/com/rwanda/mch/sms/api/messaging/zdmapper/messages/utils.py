#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from sms.api.messaging.zdmapper.messages import cbn, cmr, ccm, pnc, nbc, rar, res, dth, chi, bir, red, risk, dep, anc, ref, pre, common, checker
import re
import datetime

WHITELIST = {
                "ASM": [u'PNC', u'NBC', u'RAR', u'RES', u'DTH', u'CHI', u'BIR', u'RED', u'RISK', u'DEP', u'ANC', u'REF', u'PRE'], 
                "Binome": [u'CBN', u'CMR', u'CCM', u'DTH', u'CHI', u'DEP', u'SMN', u'SMR', u'RSO', u'SO', u'SS'],
                "Administrator": [u'PNC', u'NBC', u'RAR', u'RES', u'DTH', u'CHI', u'BIR', u'RED', u'RISK', u'DEP', u'ANC', u'REF', u'PRE',
                                        u'CBN', u'CMR', u'CCM', u'DTH', u'CHI', u'DEP', u'SMN', u'SMR', u'RSO', u'SO', u'SS' ]
            }

MESSAGES_MAPPER = {
		     "CBN" : cbn, 

		     "CMR" : cmr, 

		     "CCM" : ccm, 

		     "PNC" : pnc, 

		     "NBC" : nbc, 

		     "RAR" : rar, 

		     "RES" : res, 

		     "DTH" : dth, 

		     "CHI" : chi, 

		     "BIR" : bir, 

		     "RED" : red, 

		     "RISK" : risk, 

		     "DEP" : dep, 

		     "ANC" : anc, 

		     "REF" : ref, 

		     "PRE" : pre 
            }

def dictify_sms_parts(sms_parts):
    ans = {}
    try:
        for sp in sms_parts:
            try:
                ans.update({sp.get('position'): {'key': sp.get('key'), 'value': ' %s ' % sp.get('value')}})
            except: continue    
    except Exception, e:
        pass            
    return ans


class Rectifier(object):
    def __init__(self, report, chw, parts,  positioned_parts, message, orm , GESTATION):
        #print chw.__dict__
        self.report = report
        self.chw    = chw
        self.chw_role = chw.role_name
        self.reports = WHITELIST.get(self.chw_role)
        self.parts = parts
        self.positioned_parts = positioned_parts
        self.language = chw.language_code.lower()
        self.text = message.text
        self.sms_dict = dictify_sms_parts(positioned_parts)
        self.errors = []
        self.errmessages = MESSAGES_MAPPER.get(report.keyword).MESSAGES
        self.errmessages.update(common.COMMON_MESSAGES)
        self.orm = orm
        self.message = message
        self.GESTATION = GESTATION
        self.current_symptoms = []
        self.previous_symptoms = []
        self.report_current_symptoms = []
        self.report_previous_symptoms = []

    def list_from_query(self, qry):
        try:
            ans = []
            self.records_total = qry.count()
            #print "TOTAL RECORDS: ", self.records_total
            if self.records_total > 0:
                i = 0
                while i < self.records_total:
                    ans.append(qry[i])
                    #print "RECORD: ", i
                    i += 1
            return ans
        except Exception, e:
            pass
        return []

    def get_pregnancies_records(self):
        """GET the total number of pregnancies per woman in DB"""
        try:
            pregs = self.orm.ORM.query('pregnancy', {'national_id = %s' : self.nid})
            return pregs.count()
        except Exception, e:
            return 0

    def get_anc_records(self):
        """GET the anc visits per woman in DB for current pregnancy """
        try:
            ancs = self.orm.ORM.query('ancvisit', {'pregnancy_pk = %s' : self.current_pregnancy()['indexcol']}
                                                    , sort = ('anc_visit', False))
            #self.records_total = ancs.count() 
            return self.list_from_query(ancs)
        except Exception, e:
            return []

    def get_anc_visits(self):
        """GET ALL VISITS RECEIVED"""
        try:
            ans = []
            for anc in self.get_anc_records():
                ans.append(( anc['anc_date']  , anc['anc_visit'] ))
            return ans
        except Exception, e:
            return []

    def get_risk_records(self):
        """GET the risks per woman in DB for current pregnancy """
        try:
            risks = self.orm.ORM.query('risk', {'pregnancy_pk = %s' : self.current_pregnancy()['indexcol']}
                                                    , sort = ('created_at', False))
            #self.records_total = risks.count() 
            return self.list_from_query(risks)
        except Exception, e:
            return []

    def get_unresponded_risk_records(self):
        """GET the unresponded risks per woman in DB for current pregnancy """
        try:
            res = self.orm.ORM.query('riskresult', {'pregnancy_pk = %s' : self.current_pregnancy()['indexcol']}
                                                    , sort = ('created_at', False))
            resids = [r['indexcol'] for r in res.list()]
            urisks = []
            for r in self.get_risk_records():
                if r['indexcol'] not in resids: urisks.append(r)
            return urisks
        except Exception, e:
            return []

    def get_mother_red_records(self):
        """GET the reds per woman in DB for current pregnancy """
        try:
            mreds = self.orm.ORM.query('redalert', {'pregnancy_pk = %s' : self.current_pregnancy()['indexcol'],
                                                        'child_pk IS NULL' : ''}
                                                    , sort = ('created_at', False))
            #self.records_total = mreds.count() 
            return self.list_from_query(mreds)
        except Exception, e:
            return []

    def get_mother_death_records(self):
        """GET the deaths per woman """
        try:
            mdeaths = self.orm.ORM.query('death', {'national_id = %s' : self.nid,
                                                        'child_pk IS NULL' : ''}
                                                    , sort = ('created_at', False))
            #self.records_total = mdeaths.count() 
            return self.list_from_query(mdeaths)
        except Exception, e:
            return []

    def get_child_death_records(self):
        """GET the deaths per child """
        try:
            cdeaths = self.orm.ORM.query('death', {'child_pk = %s' : self.current_child()['indexcol'] }
                                                    , sort = ('created_at', False))
            #self.records_total = cdeaths.count() 
            return self.list_from_query(cdeaths)
        except Exception, e:
            return []

    def get_unresponded_mother_red_records(self):
        """GET the unresponded reds per woman in DB for current pregnancy """
        try:
            rars = self.orm.ORM.query('redresult', {'pregnancy_pk = %s' : self.current_pregnancy()['indexcol'],
                                                    'child_pk IS NULL' : ''}
                                                    , sort = ('created_at', False))
            rarids = [r['indexcol'] for r in rars.list()]
            umreds = []
            for r in self.get_mother_red_records():
                if not rarids or r['indexcol'] not in rarids: umreds.append(r)
            return umreds
        except Exception, e:
            print e
            return []

    def get_child_red_records(self):
        """GET the reds per child in DB for current child """
        try:
            creds = self.orm.ORM.query('redalert', {'child_pk = %s' : self.current_child()['indexcol']}
                                                    , sort = ('created_at', False))
            #self.records_total = creds.count() 
            return self.list_from_query(creds)
        except Exception, e:
            return []

    def get_unresponded_child_red_records(self):
        """GET the unresponded reds per child in DB for current child """
        try:
            rars = self.orm.ORM.query('redresult', {'child_pk = %s' : self.current_child()['indexcol']}
                                                    , sort = ('created_at', False))
            rarids = [r['indexcol'] for r in rars.list()]
            ucreds = []
            for r in self.get_child_red_records():
                if not rarids or r['indexcol'] not in rarids: ucreds.append(r)
            return ucreds
        except Exception, e:
            return []

    def get_ccm_records(self):
        """GET the ccms per child in DB for current child """
        try:
            ccms = self.orm.ORM.query('ccm', {'child_pk = %s' : self.current_child()['indexcol']}
                                                    , sort = ('created_at', False))
            #self.records_total = ccms.count() 
            return self.list_from_query(ccms)
        except Exception, e:
            return []

    def get_unresponded_ccm_records(self):
        """GET the unresponded ccms per child in DB for current child """
        try:
            ccms = self.orm.ORM.query('cmr', {'child_pk = %s' : self.current_child()['indexcol']}
                                                    , sort = ('created_at', False))
            ccmids = [r['indexcol'] for r in ccms.list()]
            uccms = []
            for r in self.get_ccm_records():
                if r['indexcol'] not in ccmids: uccms.append(r)
            return uccms
        except Exception, e:
            return []

    def get_nbc_records(self):
        """GET the nbc visits per woman in DB for current pregnancy """
        try:
            nbcs = self.orm.ORM.query('nbcvisit', {'child_pk = %s' : self.current_child()['indexcol']}
                                                    , sort = ('nbc_visit', False))
            #self.records_total = nbcs.count() 
            return self.list_from_query(nbcs)
        except Exception, e:
            return []

    def get_nbc_visits(self):
        """GET ALL VISITS RECEIVED"""
        try:
            ans = []
            for nbc in self.get_nbc_records():
                ans.append(( nbc['created_at']  , nbc['nbc_visit'] ))
            return ans
        except Exception, e:
            return []

    def get_pnc_records(self):
        """GET the pnc visits per woman in DB for current pregnancy """
        try:
            pncs = self.orm.ORM.query('pncvisit', {'national_id = %s' : self.nid,
                                                        'delivery_date = %s' : self.birth_date }
                                                    , sort = ('pnc_visit', False))
            #self.records_total = pncs.count() 
            return self.list_from_query(pncs)
        except Exception, e:
            return []

    def get_pnc_visits(self):
        """GET ALL VISITS RECEIVED"""
        try:
            ans = []
            for pnc in self.get_pnc_records():
                ans.append(( pnc['delivery_date']  , pnc['pnc_visit'] ))
            return ans
        except Exception, e:
            return []

    def get_vaccine_records(self):
        """GET the vaccine visits per child """
        try:
            vaccines = self.orm.ORM.query('childhealth', {'child_pk = %s' : self.current_child()['indexcol']}
                                                    , sort = ('vaccine', False))
            #self.records_total = vaccines.count() 
            return self.list_from_query(vaccines)
        except Exception, e:
            return []

    def get_vaccine_visits(self):
        """GET ALL VACCINE VISITS RECEIVED"""
        try:
            ans = []
            for vaccine in self.get_vaccine_records():
                ans.append(( vaccine['created_at']  , vaccine['vaccine'] ))
            return ans
        except Exception, e:
            return []

    def sorted_list(self, ans):
        return all(ans[i] <= ans[i+1] for i in xrange(len(ans)-1))

    def sorted_ordered_list(self, ans):
        return all(ans[i] <= ans[i+1] and ans[i] - ans[i+1] == -1 or ans[i] - ans[i+1] == 0 for i in xrange(len(ans)-1))

    def without_duplicates_list(self, ans):
        try:
            for x in ans:
                if ans.count(x) > 1:
                    return False
        except Exception, e:
            return False
        return True

    def is_visits_in_sequence(self, visits = []):
        try:
            return self.sorted_ordered_list(visits)
        except Exception, e:
            return False

    def is_visits_duplicate(self, visits = []):
        try:
            return self.without_duplicates_list(visits)
        except Exception, e:
            return False        

    def current_pregnancy(self):
        """GET IF WE HAVE an pregnancy currently registered for the mother"""
        try:
            preg = self.orm.ORM.query('pregnancy', {'national_id = %s' : self.nid,
                                                     'lmp >= %s' : self.nine_months_ago(date=self.message.date)}
                                                    , sort = ('lmp', False))
            ##if preg.count() > 1:
                #print "PREGS: %s", preg.count()
                
            self.pregnancy =  preg[0]
            if self.pregnancy: self.lmp = self.pregnancy['lmp']
            return self.pregnancy
            #TODO IN CASE THE REPORT IS NOT ABOUT MOTHER
        except Exception, e:
            #print e
            try:
                return self.get_child_pregnancy()
            except Exception, e:
                #print e
                pass
            return None

    def current_child(self):
        """ GET IF WE HAVE A child registered in the DB"""
        try:
            child = self.orm.ORM.query('birth', {'national_id = %s' : self.nid,
                                                     'birth_date = %s' : self.birth_date,
                                                       'child_number = %s' : self.child_number }
                                                    )#;#print child.query
            self.child=child[0]
            return self.child
        except Exception, e:
            #print e
            try:
                if self.report.keyword.strip().lower() == 'red': return self.current_red_child()
                if self.report.keyword.strip().lower() == 'pnc': return self.current_pnc_child()
                return None
            except Exception, e:
                pass
            return None

    def current_pnc_child(self):
        try:
            child = self.orm.ORM.query('birth', {'national_id = %s' : self.nid,
                                                 'birth_date = %s' : self.birth_date }
                                                )#;#print child.query
            self.child=child[0]
            self.birth_date = self.child['birth_date']
            return self.child
        except Exception, ex:
            #print ex
            return None

    def current_red_child(self):
        try:
            child = self.orm.ORM.query('birth', {'national_id = %s' : self.nid,
                                                 'child_number = %s' : self.child_number,
                                                 'birth_date = %s' : self.birth_date }
                                                )#;#print child.query
            return self.child
        except Exception, ex:
            #print ex
            return None

    def get_child_pregnancy(self):
        """ GET the pregancy from which the child was born """
        try:
            preg = self.orm.ORM.query('pregnancy', {'indexcol = %s' : self.child['pregnancy_pk']})
            if preg:
                self.pregnancy = preg[0]
                self.lmp = self.pregnancy['lmp']
            return self.pregnancy
        except Exception, e:
            #print e
            return None

    def get_pregnancy_delivery(self):
        """ GET the delivery for pregancy """
        try:
            delivs = self.orm.ORM.query('birth', {'pregnancy_pk = %s' : self.current_pregnancy()['indexcol']})
            return delivs[0]
        except Exception, e:
            #print e
            return None

    def get_current_lmp(self):
        """ GET CURRENT LMP from the current pregnancy """
        try:
            if hasattr(self, 'lmp') is False:
                self.lmp = self.current_pregnancy()['lmp']
            
            try: self.lmp = self.lmp.date()
            except Exception, e: pass
            return self.lmp
        except Exception, e:
            #print "LMP", e
            pass
            return None

    def get_current_edd(self):
        """ GET current EDD """
        try:
            self.edd = self.get_current_lmp() + datetime.timedelta(days = self.GESTATION)
            try: self.edd = self.edd.date()
            except Exception, e: pass
            return self.edd
        except Exception, e:
            #print "EDD", e
            pass
            return None        

    def patient_nid_missing(self, position = 1, key = 'nid', errcode = "patient_nid_missing"):
        try:
            nid = self.sms_dict.get(position).get('value')
            self.nid = nid
        except Exception, e:
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def invalid_nid(self, position = 1, key = 'nid', errcode = "invalid_nid"):
        try:
            nid = re.search("\s(\d+)\s", self.nid)
            self.nid = nid.group(1)
            if self.nid[0:3] == '078':   self.phoneid = self.nid
        except Exception, e:
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def nid_not_16digits(self, position = 1, key = 'nid', errcode = "nid_not_16digits"):
        try:
            if self.nid and len(self.nid) != 16:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] ) 
        except Exception, e:
            pass
        return

    def phone_mismatch(self, position = 1, key = 'nid', errcode = "phone_mismatch"):
        try:
            if self.phoneid and self.phoneid[0:10] != self.chw.telephone_moh[3:13]:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            pass
        return

    def misformat_dated_nid(self, position = 1, key = 'nid', errcode = "misformat_dated_nid"):
        try:
            if self.phoneid:
                try: self.phoneid_ddmmyy = datetime.datetime.strptime(self.nid[10:16],'%d%m%y')
                except: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            pass
        return

    def outrange_dated_nid(self, position = 1, key = 'nid', errcode = "outrange_dated_nid"):
        try:
            if self.phoneid_ddmmyy:
                _5daysago = self.message.date - datetime.timedelta(days = 5)
                if self.phoneid_ddmmyy < _5daysago or self.phoneid_ddmmyy > self.message.date:
                    self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )    
        except Exception, e:
            pass
        return


    def preg_duplicated_nid(self, position = 1, key = 'nid', errcode = "preg_duplicated_nid"):
        try:
            if self.current_pregnancy():
                print "CURRENT ALREADY", self.current_pregnancy()['indexcol']
                if not self.miscarriage() or self.current_pregnancy()['indexcol'] != self.miscarriage()['pregnancy_pk'] :
                        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            ##print nid
        except Exception, e:
            print e
            pass
        return

    def missing_current_pregnancy(self, key = 'invalid', errcode = 'missing_pregnancy'):
        try:
            if not self.current_pregnancy():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'nid': self.nid,
                                                                                                          'report': getattr(self.report, 'title_%s'%self.language)} ] )
            else:
                self.pregnancy_pk = self.current_pregnancy()['indexcol']
        except Exception, e:
            pass
        return

    def missing_current_child(self, key = 'invalid', errcode = 'missing_child'):
        try:
            if not self.current_child():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'nid': self.nid,
                                                                                                          'report': getattr(self.report, 'title_%s'%self.language)} ] )
            else:
                self.child_pk = self.current_child()['indexcol']
                self.pregnancy_pk = self.current_child()['pregnancy_pk']
        except Exception, e:
            pass
        return 

    def miscarriage_found(self, key = 'invalid', errcode = 'miscarriage'):
        try:
            if self.miscarriage() and self.miscarriage()['pregnancy_pk'] == self.pregnancy_pk:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'nid': self.nid,
                                                                                                          'report': getattr(self.report, 'title_%s'%self.language)} ] )
        except Exception, e:
            pass
        return 

    def ref_duplicated_nid(self, position = 1, key = 'nid', errcode = "ref_duplicated_nid"):
        try:
            if self.current_pregnancy():
                ##print "THERE REF"
                if self.refusal():
                     self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)  % {'nid':self.nid } ] )
            ##print nid
        except Exception, e:
            #print e
            pass
        return

    def bir_duplicated(self, position = 3, key = 'birth_date', errcode = "duplicate_birth"):
        try:
            if self.current_child():
                nid = self.current_child()['national_id']
                chino = self.current_child()['child_number']
                dob = self.current_child()['birth_date']
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)  % {'nid': nid,
                                                                                                              "chino": chino,
                                                                                                              "dob": dob } ] )
        except Exception, e:
            #print e
            pass
        return

    def chi_duplicated(self, position = 3, key = 'birth_date', errcode = "duplicate_chi"):
        try:
            chi = self.orm.ORM.query('childhealth', {'national_id = %s' : self.nid,
                                                        'child_number = %s' : self.child_number,
                                                        'birth_date = %s' : self.birth_date,
                                                        'created_at = %s' : self.message.date })
            if chi[0]:
                nid = self.nid
                chino = self.child_number
                dob = self.birth_date
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)  % {'nid': nid,
                                                                                                              "chino": chino,
                                                                                                              "dob": dob } ] )
        except Exception, e:
            #print e
            pass
        return

    def cbn_duplicated(self, position = 3, key = 'birth_date', errcode = "duplicate_cbn"):
        try:
            cbn = self.orm.ORM.query('nutrition', {'national_id = %s' : self.nid,
                                                        'child_number = %s' : self.child_number,
                                                        'birth_date = %s' : self.birth_date,
                                                        'created_at = %s' : self.message.date })
            if cbn[0]:
                nid = self.nid
                chino = self.child_number
                dob = self.birth_date
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)  % {'nid': nid,
                                                                                                              "chino": chino,
                                                                                                              "dob": dob } ] )
        except Exception, e:
            #print e
            pass
        return

    def dep_child_duplicated(self, position = 3, key = 'birth_date', errcode = "duplicate_child_dep"):
        try:
            deps = self.orm.ORM.query('departure', {'national_id = %s' : self.nid,
                                                        'birth_date = %s' : self.birth_date,
                                                        'child_number = %s' : self.child_number })
            dep = deps[0]
            if dep:
                nid = dep['national_id']
                chino = dep['child_number']
                dob = dep['birth_date']
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)  % {'nid': nid,
                                                                                                              "chino": chino,
                                                                                                              "dob": dob } ] )
        except Exception, e:
            #print e
            pass
        return

    def dep_mother_duplicated(self, position = 3, key = 'birth_date', errcode = "duplicate_mother_dep"):
        try:
            deps = self.orm.ORM.query('departure', {'national_id = %s' : self.nid,
                                                        'created_at >= %s' : self.current_pregnancy()['lmp'] })
            dep = deps[0]
            if dep:
                nid = dep['national_id']
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)  % {'nid': nid } ] )
        except Exception, e:
            #print e
            pass
        return


    def preg_not_exists_nid(self, position = 1, key = 'nid', errcode = "preg_not_exists_nid"):
        try:
            if not self.current_pregnancy():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)  % {'nid':self.nid } ] )
            ##print nid
        except Exception, e:
            #print e
            pass
        return
    
    def miscarriage(self):
        try:
            misc = self.orm.ORM.query('redalert', {'national_id = %s' : self.nid, 
                                                        'red_symptom_mc IS NOT NULL' : '',
                                                        'lmp >= %s' : self.nine_months_ago(date=self.message.date) },
                                                        sort = ('created_at', False) )
            ##print misc.query
            return misc[0]
        except Exception, e:
            return None

    def refusal(self):
        try:
            ##print "THERE REF: ", self.nid, self.nine_months_ago(date=self.message.date)
            ref = self.orm.ORM.query('refusal', {'national_id = %s' : self.nid,
                                                        'created_at >= %s' : self.nine_months_ago(date=self.message.date) })
            ##print ref.query
            return ref[0]
        except Exception, e:
            #print "ERROR: ", e
            return None

    def nine_months_ago(self, date = None):
        if date is None:    date = self.message.date
        return (date - datetime.timedelta(days = self.GESTATION)).date()

    def lmp_missing(self, position = 2, key = 'lmp', errcode = "lmp_missing"):
        try:
            lmp = self.sms_dict.get(position).get('value')
            self.lmp = lmp
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def misformat_lmp(self, position = 2, key = 'lmp', errcode = "misformat_lmp"):
        try:
            self.lmp = self.get_date(self.lmp)
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def lmp_earlier_9months(self, position = 2, key = 'lmp', errcode = "lmp_earlier_9months"):
        try:
            if self.lmp < self.nine_months_ago(self.message.date):
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def lmp_greater_currentdate(self, position = 2, key = 'lmp', errcode = "lmp_greater_currentdate"):
        try:
            if self.lmp > self.message.date.date():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def anc2_date_missing(self, position = 3, key = 'anc2_date', errcode = "anc2_date_missing"): 
        try:
            anc2_date = self.sms_dict.get(position).get('value')
            self.anc2_date = anc2_date
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def misformat_anc2_date(self, position = 3, key = 'anc2_date', errcode = "misformat_anc2_date"): 
        try:
            self.anc2_date = self.get_date(self.anc2_date)
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def anc2_lesser_currentdate(self, position = 3, key = 'anc2_date', errcode = "anc2_lesser_currentdate"): 
        try:
            if self.anc2_date < self.message.date.date():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def anc2_date_later_edd(self, position = 3, key = 'anc2_date', errcode = "anc2_date_later_edd"): 
        try:
            if self.anc2_date > self.get_current_edd():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def gravidity_missing(self, position = 4, key = 'gravidity', errcode = "gravidity_missing"): 
        try:
            gravidity = self.sms_dict.get(position).get('value')
            self.gravidity = gravidity
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return
    def misformat_gravidity(self, position = 4, key = 'gravidity', errcode = "misformat_gravidity"): 
        try:
            gravidity = re.search("\s([0-9]+)\s", self.gravidity)
            self.gravidity = int(gravidity.group(1))
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return 
    def gravidity_not_between_1_30(self, position = 4, key = 'gravidity', errcode = "gravidity_not_between_1_30"): 
        try:
            if self.gravidity < 1 or self.gravidity > 30:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return
    def mismatch_gravidity_record(self, position = 4, key = 'gravidity', errcode = "mismatch_gravidity_record"): 
        try:
            if self.gravidity < self.get_pregnancies_records() + 1:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'nid':self.nid, 'pregs':self.get_pregnancies_records()} ] )
        except Exception, e:
            #print e
            pass
        return

    def missing_parity(self, position = 5, key = 'parity', errcode = "missing_parity"): 
        try:
            parity = self.sms_dict.get(position).get('value')
            self.parity = parity
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return
    def misformat_parity(self, position = 5, key = 'parity', errcode = "misformat_parity"): 
        try:
            parity = re.search("\s([0-9]+)\s", self.parity)
            self.parity = int(parity.group(1))
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return
    def outrange_parity(self, position = 5, key = 'parity', errcode = "outrange_parity"): 
        try:
            if self.parity >= self.gravidity:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)  ] )
        except Exception, e:
            #print e
            pass
        return

    def get_previous_symptoms(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'previous symptoms'):
                ans.append(f.key.lower())
            self.report_previous_symptoms = ans
            return self.report_previous_symptoms
        except Exception, e:
            #print e
            return []

    def get_current_symptoms(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'current symptoms'):
                ans.append(f.key.lower())
            self.report_current_symptoms = ans
            return self.report_current_symptoms
        except Exception, e:
            #print e
            return []

    def get_red_symptoms(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'red alert'):
                ans.append(f.key.lower())
            self.report_red_symptoms = ans
            return self.report_red_symptoms
        except Exception, e:
            #print e
            return []

    def get_location(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'location'):#.exclude(key__icontains = 'cl'):
                ans.append(f.key.lower())
            self.report_location = ans
            return self.report_location
        except Exception, e:
            #print e
            return []

    def get_toilet(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'toilet'):
                ans.append(f.key.lower())
            self.report_toilet = ans
            return self.report_toilet
        except Exception, e:
            #print e
            return []

    def get_handwashing(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'handwashing'):
                ans.append(f.key.lower())
            self.report_handwashing = ans
            return self.report_handwashing
        except Exception, e:
            #print e
            return []

    def get_intervention(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'intervention'):
                ans.append(f.key.lower())
            self.report_intervention = ans
            return self.report_intervention
        except Exception, e:
            #print e
            return []

    def get_mother_status(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'Mother Status'):
                ans.append(f.key.lower())
            self.report_mother_status = ans
            return self.report_mother_status
        except Exception, e:
            #print e
            return []

    def get_child_status(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'Child Status'):
                ans.append(f.key.lower())
            self.report_child_status = ans
            return self.report_child_status
        except Exception, e:
            #print e
            return []

    def get_gender(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'Gender'):
                ans.append(f.key.lower())
            self.report_gender = ans
            return self.report_gender
        except Exception, e:
            #print e
            return []

    def get_breastfeeding(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'Breastfeeding'):
                ans.append(f.key.lower())
            self.report_breastfeeding = ans
            return self.report_breastfeeding
        except Exception, e:
            #print e
            return []

    def missing_previous_symptoms(self, position = 6, key = 'previous_symptoms', errcode = "missing_previous_symptoms"):
        try:
            symptoms = self.sms_dict.get(position).get('value')
            symptoms = symptoms.strip().split(" ")
            self.previous_symptoms = symptoms
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return 

    def duplicate_symptom(self, position = 6, key = 'previous_symptoms', errcode = "duplicate_symptom"):
        try:
            dups = []
            symps_lower = [x.lower() for x in self.parts ]
            for x in self.parts:
                if symps_lower.count(x.lower()) > 1 and self.get('position').get('value').strip().split(' ').count(x) > 1:
                    dups.append(x)
            if len(dups) > 0:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'codes': ' '.join(x for x in set(dups))} ] )
        except Exception, e:
            #print e
            pass
        return 

    def miscarriage_mismatch(self, position = 6, key = 'previous_symptoms', errcode = "miscarriage_mismatch"):
        try:
            symps_lower = [x.lower() for x in self.previous_symptoms]
            if 'rm' in  symps_lower and self.miscarriage() < 3:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return  
    def gravidity_mismatch_symptoms(self, position = 6, key = 'previous_symptoms', errcode = "gravidity_mismatch_symptoms"):
        try:
            symps_lower = [x.lower() for x in self.previous_symptoms]
            if 'nr' not in  symps_lower and self.gravidity == 1:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return
    def incoherent_jam_nr_symptom(self, position = 6, key = 'previous_symptoms', errcode = "incoherent_jam_nr_symptom"):
        try:
            symps_lower = [x.lower() for x in self.previous_symptoms]
            if 'nr' in  symps_lower and len(symps_lower) > 1:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 
    def invalid_previous_symptom(self, position = 6, key = 'previous_symptoms', errcode = "invalid_previous_symptom"):
        try:
            self.report_previous_symptoms = self.get_previous_symptoms()
            symps_lower = [x.lower() for x in self.previous_symptoms]
            inv = False
            for x in symps_lower:
                if x not in self.report_previous_symptoms:
                    inv = True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 

    def missing_current_symptoms(self, position = 7, key = 'current_symptoms', errcode = "missing_current_symptoms"):
        try:
            symptoms = self.sms_dict.get(position).get('value')
            symptoms = symptoms.strip().split(" ")
            self.current_symptoms = symptoms
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return 

    def invalid_current_symptom(self, position = 7, key = 'current_symptoms', errcode = "invalid_current_symptom"):
        try:
            self.report_current_symptoms = self.get_current_symptoms()
            symps_lower = [x.lower() for x in self.current_symptoms]
            inv = False
            for x in symps_lower:
                if x not in self.report_current_symptoms:
                    inv = True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)] )
        except Exception, e:
            #print e
            pass
        return

    def incoherent_jam_np_symptom(self, position = 7, key = 'current_symptoms', errcode = "incoherent_jam_np_symptom"):
        try:
            symps_lower = [x.lower() for x in self.current_symptoms]
            if 'np' in  symps_lower and len(symps_lower) > 1:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return

    def incoherent_np_symptom(self, position = 7, key = 'current_symptoms', errcode = "incoherent_np_symptom"):
        try:
            symps_lower = [x.lower() for x in self.current_symptoms]
            if 'np' in  symps_lower and len(symps_lower) > 1:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 

    def missing_red_symptoms(self, position = 4, key = 'red_symptoms', errcode = "missing_red_symptoms"):
        try:
            symptoms = self.sms_dict.get(position).get('value')
            symptoms = symptoms.strip().split(" ")
            self.red_symptoms = symptoms
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return 

    def invalid_red_symptom(self, position = 4, key = 'red_symptoms', errcode = "invalid_red_symptom"):
        try:
            self.report_red_symptoms = self.get_red_symptoms()
            symps_lower = [x.lower() for x in self.red_symptoms]
            inv = False
            for x in symps_lower:
                if x not in self.report_red_symptoms:
                    inv = True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)] )
        except Exception, e:
            #print e
            pass
        return

    def incoherent_red_np_symptom(self, position = 4, key = 'red_symptoms', errcode = "incoherent_red_np_symptom"):
        try:
            symps_lower = [x.lower() for x in self.red_symptoms]
            if 'np' in  symps_lower:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 

    def invalid_code(self, key = 'invalid', errcode = 'invalid_code'):
        try:
            codes = re.findall("\s[A-Za-z]{2,4}", self.text)
            invalides = []#; print codes
            for x in codes:
                if x.lower().strip() in self.parts and x.lower().strip() not in [ k.key for k in self.report.smsreportfield_set.all()] + [
                                                         k.prefix for k in self.report.smsreportfield_set.all() if k.prefix] + [
                                                            self.report.keyword.lower() ]:
                    invalides.append(x.strip())
            if invalides: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {
                                                                                                    'report': getattr(self.report, 'title_%s'%self.language),
                                                                                                    'codes': ' '.join( x for x in  invalides) } ] )
        except Exception, e:
            #print e
            pass
        return

    def missing_location(self, position = 8, key = 'location', errcode = "missing_location"):
        try:
            location = self.sms_dict.get(position).get('value')
            self.location = location.strip().split(" ") 
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def invalid_location(self, position = 8, key = 'location', errcode = "invalid_location"):
        try:
            self.report_location = self.get_location()
            symps_lower = [x.lower() for x in self.location]
            inv = False
            for x in symps_lower:
                if len(symps_lower) > 1 or x not in self.report_location:
                    inv= True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return

    def missing_mother_weight(self, position = 9, key = 'mother_weight', errcode = "missing_mother_weight"):
        try:
            weight = self.sms_dict.get(position).get('value')
            self.mother_weight = self.get_weight(weight)
            #print self.mother_weight
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def invalid_mother_weight(self, position = 9, key = 'mother_weight', errcode = "invalid_mother_weight"):
        try:
            if self.mother_weight > 150 or self.mother_weight < 35:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 

    def missing_child_weight(self, position = 9, key = 'child_weight', errcode = "missing_child_weight"):
        try:
            weight = self.sms_dict.get(position).get('value')
            self.child_weight = self.get_weight(weight)
            #print self.child_weight
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def invalid_child_weight(self, position = 9, key = 'child_weight', errcode = "invalid_child_weight"):
        try:
            if self.child_weight > 25 or self.child_weight < 1:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 

    def missing_muac(self, position = 9, key = 'muac', errcode = "missing_muac"):
        try:
            muac = self.sms_dict.get(position).get('value')
            self.muac = self.get_muac(muac)
            #print self.muac
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def get_bmi(self):
        self.bmi = None
        try:
            if self.mother_weight and self.mother_height: 
                self.bmi = self.mother_weight / ((self.mother_height* self.mother_height) / 10000.0)
            if self.child_weight and self.child_height: 
                self.bmi = self.child_weight / ((self.child_height* self.child_height) / 10000.0)
        except Exception, e:
            #print e
            pass
        return 

    def mother_has_phone(self, position = 14, key = 'mother_phone', errcode = "invalid_phone"):
        try:
            phone = self.sms_dict.get(position) or self.sms_dict.get(len(self.parts)-1)
            phone = phone.get('value')
            phone = re.search("\s(\d+)\s", phone)            
            if phone and not (len(phone.group(1)) == 10 and phone.group(1)[0:2] == '07'):
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            else:
                self.mother_phone = phone.group(1)                
        except Exception, e:
            #print e, key
            pass
        return

    def invalid_muac(self, position = 9, key = 'muac', errcode = "invalid_muac"):
        try:
            if self.muac > 26 or self.muac < 6:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 

    def missing_mother_height(self, position = 10, key = 'mother_height', errcode = "missing_mother_height"):
        try:
            height = self.sms_dict.get(position).get('value')
            self.mother_height = self.get_height(height)
            #print self.mother_height
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def invalid_mother_height(self, position = 10, key = 'mother_height', errcode = "invalid_mother_height"):
        try:
            if self.mother_height > 250 or self.mother_height < 50:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 

    def missing_toilet(self, position = 11, key = 'toilet', errcode = "missing_toilet"):
        try:
            toilet = self.sms_dict.get(position).get('value')
            self.toilet = toilet.strip().split(" ") 
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            pass
        return

    def invalid_toilet(self, position = 11, key = 'toilet', errcode = "invalid_toilet"):
        try:
            self.report_toilet = self.get_toilet()
            symps_lower = [x.lower() for x in self.toilet]
            inv = False
            for x in symps_lower:
                if len(symps_lower) > 1 or x not in self.report_toilet:
                    inv= True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return

    def missing_handwashing(self, position = 12, key = 'handwashing', errcode = "missing_handwashing"):
        try:
            handwashing = self.sms_dict.get(position).get('value')
            self.handwashing = handwashing.strip().split(" ") 
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def invalid_handwashing(self, position = 12, key = 'handwashing', errcode = "invalid_handwashing"):
        try:
            self.report_handwashing = self.get_handwashing()
            symps_lower = [x.lower() for x in self.handwashing]
            inv = False
            for x in symps_lower:
                if len(symps_lower) > 1 or x not in self.report_handwashing:
                    inv= True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return


    def field_missing(self, position = 2, key = 'lmp', errcode = "lmp_missing"):
        try:
            dva = self.sms_dict.get(position).get('value')
            setattr(self, key, dva)            
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def misformat_datefield(self, position = 2, key = 'lmp', errcode = "misformat_lmp"):
        try:
            dva = self.sms_dict.get(position).get('value')
            setattr(self, key,  self.get_date(dva) )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def datefield_earlier_9months(self, position = 2, key = 'lmp', errcode = "lmp_earlier_9months"):
        try:
            dva = getattr(self, key)
            if dva < self.nine_months_ago(self.message.date):
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def datefield_mismatch(self, position = 2, key = 'emergency_date', errcode = "emergency_date_mismatch_created_at", records = [], match_key = 'created_at'):
        try:
            dva = getattr(self, key)
            if (dva and records) and records[0][match_key] != dva:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def datefield_greater_currentdate(self, position = 2, key = 'lmp', errcode = "lmp_greater_currentdate"):
        try:
            dva = getattr(self, key)
            if dva > self.message.date.date():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def datefield_lesser_currentdate(self, position = 3, key = 'anc2_date', errcode = "anc2_lesser_currentdate"): 
        try:
            dva = getattr(self, key)
            if dva < self.message.date.date():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def datefield_later_edd(self, position = 3, key = 'anc2_date', errcode = "anc2_date_later_edd"): 
        try:
            dva = getattr(self, key)
            if dva > self.get_current_edd():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def datefield_lesser_lmp(self, position = 3, key = 'anc2_date', errcode = "anc2_date_lesser_lmp"): 
        try:
            dva = getattr(self, key)
            if self.get_current_lmp() and  dva < self.get_current_lmp():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def valid_number_field(self, position = 2 ):
        try:
            dva = self.sms_dict.get(position).get('value')
            dva = re.search("\s([0-9]+)\s", dva)
            dvano = int(dva.group(1))
            if dvano: return True
        except Exception, e:
            pass        
        return False

    def valid_date_field(self, position = 3 ):
        try:
            dva = self.sms_dict.get(position).get('value')
            dva = self.get_date(dva)
            if dva: return True
        except Exception, e:
            pass        
        return False

    def misformat_numberfield(self, position = 4, key = 'gravidity', errcode = "misformat_gravidity"): 
        try:
            dva = self.sms_dict.get(position).get('value')
            dva = re.search("\s([0-9]+)\s", dva)
            setattr(self, key, int(dva.group(1)) )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return 
    def numberfield_not_between_minv_maxv(self, position = 4, key = 'gravidity', errcode = "gravidity_not_between_1_30", minv = 1, maxv = 30): 
        try:
            dva = getattr(self, key)
            if dva < minv or dva > maxv:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return

    def anc_date_lesser_lastanc(self, position = 2, key = 'anc_date', errcode = "anc_date_lesser_lastanc", visits = [] ): 
        try:
            dva = visits
            dvanow = getattr(self, key)
            if dva and dva[0][0].date() > dvanow:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            if hasattr(self, key):  self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def make_sure_numbers(self, strv):
        try:
            ##print "V: ", strv
            return [int(s) for s in strv if s.isdigit()]
        except Exception, e:
            ##print e, strv
            return []

    def acknowledge_previous_visit(self, position = 3, key = 'nbc1', errcode = "previous_ack_missing"):
        try:
            visit = self.sms_dict.get(position).get('value')
            if visit:                
                if visit.strip().lower() in ['yego', 'yes', 'oui']:
                    setattr(self, key, True)
                elif visit.strip().lower() in ['oya', 'no', 'non']:
                    setattr(self, key, False)
                else:
                    self.errors.append( [errcode, self.errmessages.get('invalid').get(errcode).get(self.language) % {'visit': key.upper()} ] )
            else:
                self.errors.append( [errcode, self.errmessages.get('invalid').get(errcode).get(self.language) % {'visit': key.upper()} ] )
            
        except Exception, e:
            print e
            pass
        return

    def invalid_sequence(self, position = 3, key = 'anc_visit', errcode = "invalid_sequence", max_sequence = range(2,5) , visits = []):
        try:
            dva = visits
            dvanow = self.make_sure_numbers(getattr(self, key)[0])
            #print "VISITS", dva, dvanow, [ s[1] for s in dva] + dvanow
            #seq = [ s[1] for s in dva]
            seq = [ self.make_sure_numbers(s[1])[0] for s in dva]
            if len(seq) > 1:
                if seq[0] > seq[1]: seq.reverse()
            if dva and self.is_visits_in_sequence( seq + dvanow) is False:
                #print "INV 1", seq, visits, dvanow
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {"visit": dvanow[0] , "pre_visit": dvanow[0]-1 } ] )
            if not dva and dvanow[0] in max_sequence and dvanow[0] != max_sequence[0]:
                print dva, max_sequence, max_sequence[0]
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {"visit": dvanow[0] , "pre_visit": dvanow[0]-1 } ] )
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def outrange_dated_field(self, position = 3, key = 'nbc_visit', errcode = "outrange_nbc_visit", delta_comp = None, delta = 60):
        try:
            if delta_comp:
                deltago = self.message.date - datetime.timedelta(days = delta)
                if delta_comp < deltago:
                    self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )    
        except Exception, e:
            pass
        return

    def duplicate_visit(self, position = 3, key = 'anc_visit', errcode = "duplicate_anc_visit" , visits = []):
        try:
            dva = visits
            dvanow = self.make_sure_numbers(getattr(self, key)[0])
            ##print "DUPS VISITS", dva, dvanow
            if dva and self.is_visits_duplicate([ s[1] for s in dva] + dvanow) is False:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {"visit" : dvanow[0]} ] )
            
        except Exception, e:
            #print e
            if hasattr(self, key):   self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return   


    def get_group_fields(self, group='anc_visit'):
        try:
            ans = []
            fld = self.report.smsreportfield_set.get(key__iexact = group)#;print fld.category_en
            for f in self.report.smsreportfield_set.filter(category_en__icontains = fld.category_en):
                ans.append(f.key.lower())
            #setattr(self, group, ans)
            #print ans
            return ans
        except Exception, e:
            #print "FLD: %s" % e
            return []


    def missing_group_fields(self, position = 3, key = 'anc_visit', errcode = "missing_anc_visit"):
        try:
            dvas = self.sms_dict.get(position).get('value')
            dvas = dvas.strip().split(" ")#; #print key,"GRP FLDS",dvas
            setattr(self, key, dvas)
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return 

    def invalid_group_field(self, position = 3, key = 'anc_visit', errcode = "invalid_anc_visit" ):
        try:
            dvas = getattr(self, key)
            flds = self.get_group_fields( group = dvas[0] ) 
            symps_lower = [x.lower() for x in dvas]
            inv = False
            
            for x in symps_lower:
                if x not in flds:
                    inv = True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)] )
            setattr(self, key, dvas)
        except Exception, e:
            #print e
            pass
        return

    def unresponded_record(self, key="invalid", errcode = 'unresponded_report', records = []):
        try:
            if len( [x for x in records] ) > 0:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'report': getattr(self.report, 'title_%s'%self.language),
                                                                                           'nid': self.nid, 'sms': records[0]['message'] }] )
        except Exception, e:
            print e
            return

    def missing_to_respond_record(self, key="invalid", errcode = 'risk_to_respond', records = []):
        try:
            if len( [x for x in records] )  < 1:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'report': getattr(self.report, 'title_%s'%self.language),
                                                                                                            'nid': self.nid }] )
        except Exception, e:
            #print e
            pass
        return 

    def invalid_symptom_to_respond(self, key="invalid", errcode = 'invalid_symptom_to_respond', column_prefix = "symptom", symptoms = [], records = []):
        try:
            ans = []
            reps = [y for y in records]
            for x in symptoms:
                xv = "%s_%s" % (column_prefix, x.lower())
                try:
                    if reps[0][xv]:
                        continue
                    else:
                        ans.append(x)
                        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
                except KeyError, e:
                    ##print "KEY ERROR: ", x, ans
                    continue
        except Exception, e:
            ##print "ERROR: ",e
            return

    def missing_intervention(self, position = 4, key = 'intervention', errcode = "missing_intervention"):
        try:
            intervention = self.sms_dict.get(position).get('value')
            self.intervention = intervention.strip().split(" ") 
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def invalid_intervention(self, position = 4, key = 'intervention', errcode = "invalid_intervention"):
        try:
            self.report_intervention = self.get_intervention()
            symps_lower = [x.lower() for x in self.intervention]
            inv = False
            for x in symps_lower:
                if len(symps_lower) > 1 or x not in self.report_intervention:
                    inv= True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 


    def missing_mother_status(self, position = 5, key = 'mother_status', errcode = "missing_mother_status"):
        try:
            mother_status = self.sms_dict.get(position).get('value')
            self.mother_status = mother_status.strip().split(" ") 
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def invalid_mother_status(self, position = 5, key = 'mother_status', errcode = "invalid_mother_status"):
        try:
            self.report_mother_status = self.get_mother_status()
            symps_lower = [x.lower() for x in self.mother_status]
            inv = False
            for x in symps_lower:
                if len(symps_lower) > 1 or x not in self.report_mother_status:
                    inv= True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 

    def missing_child_status(self, position = 12, key = 'child_status', errcode = "missing_child_status"):
        try:
            child_status = self.sms_dict.get(position).get('value')
            self.child_status = child_status.strip().split(" ") 
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def invalid_child_status(self, position = 12, key = 'child_status', errcode = "invalid_child_status"):
        try:
            self.report_child_status = self.get_child_status()
            symps_lower = [x.lower() for x in self.child_status]
            inv = False
            for x in symps_lower:
                if len(symps_lower) > 1 or x not in self.report_child_status:
                    inv= True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 

    def missing_gender(self, position = 4, key = 'gender', errcode = "missing_gender"):
        try:
            gender = self.sms_dict.get(position).get('value')
            self.gender = gender.strip().split(" ") 
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def invalid_gender(self, position = 4, key = 'gender', errcode = "invalid_gender"):
        try:
            self.report_gender = self.get_gender()
            symps_lower = [x.lower() for x in self.gender]
            inv = False
            for x in symps_lower:
                if len(symps_lower) > 1 or x not in self.report_gender:
                    inv= True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 

    def missing_breastfeeding(self, position = 7, key = 'breastfeeding', errcode = "missing_breastfeeding"):
        try:
            breastfeeding = self.sms_dict.get(position).get('value')
            self.breastfeeding = breastfeeding.strip().split(" ") 
        except Exception, e:
            #print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def invalid_breastfeeding(self, position = 7, key = 'breastfeeding', errcode = "invalid_breastfeeding"):
        try:
            self.report_breastfeeding = self.get_breastfeeding()
            symps_lower = [x.lower() for x in self.breastfeeding]
            inv = False
            for x in symps_lower:
                if len(symps_lower) > 1 or x not in self.report_breastfeeding:
                    inv= True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            #print e
            pass
        return 

    def invalid_reporter(self, key = 'invalid', errcode = 'invalid_reporter'):
        try:
            if not self.chw_role or not self.report or not self.reports or self.report.keyword not in  self.reports:
                 self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'report': getattr(self.report, 'title_%s'%self.language),
                                                                                                            'role': self.chw_role,
                                                                                                            'rkey': self.report }] )
        except Exception, e:
            print "REPORTER: ", e
            return

    def delivered_already(self, key = 'invalid', errcode = 'delivered_already'):
        try:
            if self.get_pregnancy_delivery():
                 self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'report': getattr(self.report, 'title_%s'%self.language),
                                                                                                            'nid': self.nid }] )
        except Exception, e:
            print e
            return 

    def has_mother_death(self, key = 'invalid', errcode = 'mother_death'):
        try:
            deaths = self.get_mother_death_records()
            if deaths and deaths[0]:
                 self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'report': self.report.keyword,
                                                                                                            'nid': self.nid }] )
        except Exception, e:
            print e
            return 

    def has_child_death(self, key = 'invalid', errcode = 'child_death'):
        try:
            deaths = self.get_child_death_records()
            if deaths and deaths[0]:
                 self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'report': self.report.keyword,
                                                                                                            'nid': self.nid,
                                                                                                            'chino': self.child_number,
                                                                                                            'dob': self.birth_date }] )
        except Exception, e:
            print e
            return 

    def get_weight(self, text):
        try:
            weight_pattern = re.search("\s(wt\d+\.?\d*)", text, re.IGNORECASE)
            weight = re.search("(\d+\.?\d*)", weight_pattern.group(1))
            return float(weight.group(1))
        except Exception, e:
            return None

    def get_height(self, text):
        try:
            height_pattern = re.search("\s(ht\d+\.?\d*)", text, re.IGNORECASE)
            height = re.search("(\d+\.?\d*)", height_pattern.group(1))
            return float(height.group(1))
        except Exception, e:
            return None

    def get_muac(self, text):
        try:
            muac_pattern = re.search("\s(muac\d+\.?\d*)", text, re.IGNORECASE)
            muac = re.search("(\d+\.?\d*)", muac_pattern.group(1))
            return float(muac.group(1))
        except Exception, e:
            print e
            return None              


    def get_date(self, text):
        """Tries to parse a string into some python date object."""
        
        today = self.message.date
        cycle_s = today - datetime.timedelta(days = 1000)
        cycle_e = today + datetime.timedelta(days = 1000)
           
        date_string = re.search("\s([0-9.]+)\s", text)   
        # full date: DD.MM.YYYY
        if date_string:
            date_pattern = re.search("^(\d+)\.(\d+)\.(\d+)$", date_string.group(1)) 
            if date_pattern:
                dd = date_pattern.group(1)
                mm = date_pattern.group(2)
                yyyy = date_pattern.group(3)
            
                ##print "%s = '%s' '%s' '%s'" % (date_string, dd, mm, yyyy)
            
                # make sure we are in the right format
                if len(dd) > 2 or len(mm) > 2 or len(yyyy) != 4: 
                    raise Exception(_("Invalid date format, must be in the form: DD.MM.YYYY"))
                
                # invalid year
                #if int(yyyy) > cycle_e.year or int(yyyy) < cycle_s.year:
                #    raise Exception(_("Invalid year, year must be between %(st)d and %(en)d, and date in the form: DD.MM.YYYY" % {'st': cycle_s.year,
                #                                                                                                                 "en": cycle_e.year}))
            
                # invalid month
                if int(mm) > 12 or int(mm) < 1:
                    raise Exception(_("Invalid month, month must be between 1 and 12, and date in the form: DD.MM.YYYY"))
            
                # invalid day
                if int(dd) > 31 or int(dd) < 1:
                    raise Exception(_("Invalid day, day must be between 1 and 31, and date in the form: DD.MM.YYYY"))
            
            
                #Otherwise, parse into our date format
                return datetime.date(int(yyyy), int(mm), int(dd))
            else:
                raise Exception(_("Invalid date format, must be in the form: DD.MM.YYYY"))
        else:
            raise Exception(_("Invalid date format, must be in the form: DD.MM.YYYY")) 


