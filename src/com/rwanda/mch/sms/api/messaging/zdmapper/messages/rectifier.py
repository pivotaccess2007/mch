#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from api.messaging.zdmapper.messages import cbn, cmr, ccm, pnc, nbc, rar, res, dth, chi, bir, red, risk, dep, anc, ref, pre, common, checker
import re
import datetime

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
            try:    ans.update({sp.get('position'): {'key': sp.get('key'), 'value': ' %s ' % sp.get('value')}})
            except: continue    
    except Exception, e:
        pass            
    return ans


class Rectifier(object):
    def __init__(self, report, chw, parts,  positioned_parts, message, orm , GESTATION):
        self.report = report
        self.chw    = chw
        self.parts = parts
        self.positioned_parts = positioned_parts
        self.language = chw.language
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

    def get_pregnancies_records(self):
        """GET the total number of pregnancies per woman in DB"""
        try:
            pregs = self.orm.ORM.query('rw_pregnancies', {'indangamuntu = %s' : self.nid})
            return pregs.count()
        except Exception, e:
            return 0

    def current_pregnancy(self):
        """GET IF WE HAVE an pregnancy currently registered for the mother"""
        try:
            preg = self.orm.ORM.query('rw_pregnancies', {'indangamuntu = %s' : self.nid,
                                                     'lmp >= %s' : self.nine_months_ago(date=self.message.date)}
                                                    , sort = ('lmp', False))
            self.pregnancy =  preg[0]
            return self.pregnancy
            #TODO IN CASE THE REPORT IS NOT ABOUT MOTHER
        except Exception, e:
            print e
            try:
                return self.child_pregnancy()
            except Exception, e:
                print e
            return None

    def current_child(self):
        """ GET IF WE HAVE A child registered in the DB"""
        try:
            child = self.orm.ORM.query('rw_children', {'indangamuntu = %s' : self.nid,
                                                     'birth_date >= %s' : self.birth_date,
                                                       'child_number >= %s' : self.child_number }
                                                    )
            self.child=child[0]
            return self.child
        except Exception, e:
            print e
            return None

    def get_child_pregnancy(self):
        """ GET the pregancy from which the child was born """
        try:
            preg = self.orm.ORM.query('rw_pregnancies', {'indexcol = %s' : self.child['pregnancy_id']})
            return preg[0]
        except Exception, e:
            print e
            return None

    def get_current_lmp(self):
        """ GET CURRENT LMP from the current pregnancy """
        try:
            self.lmp = self.current_pregnancy()['lmp']
            return self.lmp
        except Exception, e:
            print e
            return None

    def get_current_edd(self):
        """ GET current EDD """
        try:
            self.edd = self.lmp + datetime.timedelta(days = self.GESTATION)
            return self.edd
        except Exception, e:
            print e
            return None        

    def patient_nid_missing(self, position = 1, key = 'nid', errcode = "patient_nid_missing"):
        """GET IF NID IS MISSING"""
        try:
            nid = self.sms_dict.get(position).get('value')
            #print nid
        except Exception, e:
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def invalid_nid(self, position = 1, key = 'nid', errcode = "invalid_nid"):
        """ GET IF NID IS MISSING """
        try:
            nid = re.search("\s(\d+)\s", self.sms_dict.get(position).get('value'))
            self.nid = nid.group(1)
            if self.nid[0:3] == '078':   self.phoneid = self.nid
        except Exception, e:
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def nid_not_16digits(self, position = 1, key = 'nid', errcode = "nid_not_16digits"):
        """ GET IF NID IS NOT 16 DIGITS"""
        try:
            if self.nid and len(self.nid) != 16:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] ) 
        except Exception, e:
            pass
        return

    def phone_mismatch(self, position = 1, key = 'nid', errcode = "phone_mismatch"):
        """GET IF, IN CASE, NID IS NOT PHONE MATCH"""
        try:
            if self.phoneid and self.phoneid[0:10] != self.chw.telephone_moh[3:13]:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            pass
        return

    def misformat_dated_nid(self, position = 1, key = 'nid', errcode = "misformat_dated_nid"):
        """ GET IF THE NID DATE FORMAT IS FINE """
        try:
            if self.phoneid:
                try: self.phoneid_ddmmyy = datetime.datetime.strptime(self.nid[10:16],'%d%m%y')
                except: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            pass
        return

    def outrange_dated_nid(self, position = 1, key = 'nid', errcode = "outrange_dated_nid"):
        """ GET IF THE NID DATE FORMARTED IS IN RANGE """
        try:
            if self.phoneid_ddmmyy:
                _5daysago = datetime.datetime.today() - datetime.timedelta(days = 5)
                if self.phoneid_ddmmyy < _5daysago:
                    self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )    
        except Exception, e:
            pass
        return


    def duplicated_nid(self, position = 1, key = 'nid', errcode = "preg_duplicated_nid"):
        """ MAKE SURE THE REPORT IS NOT DUPLICATED 
            DUPLICATION ID DEFINED PER REPORT AND PER REPORT WE PULL CURRENT PREGNANCY, CHILD PREGNANCY, CHILD, AND VISITS AND SO ON """
        try:
            if self.report.keyword.upper()  == 'PRE':       
                if self.current_pregnancy():
                    if not self.miscarriage():
                         self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )

            if self.report.keyword.upper()  == 'ANC':       
                if self.current_pregnancy():
                    if not self.miscarriage():
                         self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            #print nid
        except Exception, e:
            print e
        return
    
    def miscarriage(self):
        try:
            misc = self.orm.ORM.query('rw_redalerts', {'indangamuntu = %s' : self.nid, 
                                                        'red_symptom_mc IS NOT NULL' : '',
                                                        'lmp >= %s' : nine_months_ago(date=self.message.date) })
            #print misc.query
            return misc
        except Exception, e:
            return None

    def nine_months_ago(self, date = datetime.datetime.today()):
        return (date - datetime.timedelta(days = self.GESTATION)).date()

    def field_missing(self, position = 2, key = 'lmp', errcode = "lmp_missing"):
        try:
            dva = self.sms_dict.get(position).get('value')            
        except Exception, e:
            print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def misformat_datefield(self, position = 2, key = 'lmp', errcode = "misformat_lmp"):
        try:
            dva = self.sms_dict.get(position).get('value')
            setattr(self, key,  get_date(dva)
        except Exception, e:
            print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def datefield_earlier_9months(self, position = 2, key = 'lmp', errcode = "lmp_earlier_9months"):
        try:
            dva = getattr(self, key)
            if dva < self.nine_months_ago(self.message.date):
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def datefield_greater_currentdate(self, position = 2, key = 'lmp', errcode = "lmp_greater_currentdate"):
        try:
            dva = getattr(self, key)
            if dva > self.message.date.date():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def datefield_lesser_currentdate(self, position = 3, key = 'anc2_date', errcode = "anc2_lesser_currentdate"): 
        try:
            dva = getattr(self, key)
            if dva < self.message.date.date():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def datefield_later_edd(self, position = 3, key = 'anc2_date', errcode = "anc2_date_later_edd"): 
        try:
            dva = getattr(self, key)
            if dva > self.get_current_edd():
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return

    def misformat_numberfield(self, position = 4, key = 'gravidity', errcode = "misformat_gravidity"): 
        try:
            dva = self.sms_dict.get(position).get('value')
            dva = re.search("\s([0-9]+)\s", gravidity)
            setattr(self, key, int(dva.group(1)) )
        except Exception, e:
            print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return 
    def numberfield_not_between_minv_maxv(self, position = 4, key = 'gravidity', errcode = "gravidity_not_between_1_30", minv = 1, maxv = 30): 
        try:
            dva = getattr(self, key)
            if dva < minv or dva > maxv:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            print e
            return
    def mismatch_gravidity_record(self, position = 4, key = 'gravidity', errcode = "mismatch_gravidity_record"): 
        try:
            if self.gravidity < self.get_pregnancies_records() + 1:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'nid':self.nid, 'pregs':self.get_pregnancies_records()} ] )
        except Exception, e:
            print e
            return

    def outrange_parity(self, position = 5, key = 'parity', errcode = "outrange_parity"): 
        try:
            if self.parity >= self.gravidity:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)  ] )
        except Exception, e:
            print e
            return

    def get_previous_symptoms(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'previous symptoms'):
                ans.append(f.key.lower())
            self.report_previous_symptoms = ans
            return self.report_previous_symptoms
        except Exception, e:
            print e
            return []

    def get_current_symptoms(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'current symptoms'):
                ans.append(f.key.lower())
            self.report_current_symptoms = ans
            return self.report_current_symptoms
        except Exception, e:
            print e
            return []

    def get_location(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'location'):
                ans.append(f.key.lower())
            self.report_location = ans
            return self.report_location
        except Exception, e:
            print e
            return []

    def get_toilet(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'toilet'):
                ans.append(f.key.lower())
            self.report_toilet = ans
            return self.report_toilet
        except Exception, e:
            print e
            return []

    def get_handwashing(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'handwashing'):
                ans.append(f.key.lower())
            self.report_handwashing = ans
            return self.report_handwashing
        except Exception, e:
            print e
            return []

    def get_intervention(self):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = 'intervention'):
                ans.append(f.key.lower())
            self.report_intervention = ans
            return self.report_intervention
        except Exception, e:
            print e
            return []

    def missing_previous_symptoms(self, position = 6, key = 'previous_symptoms', errcode = "missing_previous_symptoms"):
        try:
            symptoms = self.sms_dict.get(position).get('value')
            symptoms = symptoms.strip().split(" ")
            self.previous_symptoms = symptoms
        except Exception, e:
            print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return 

    def duplicate_symptom(self, position = 6, key = 'previous_symptoms', errcode = "duplicate_symptom"):
        try:
            dups = []
            symps_lower = [x.lower() for x in [ y.lower() for y in self.parts] ]
            for x in symps_lower:
                if symps_lower.count(x.lower()) > 1:
                    dups.append(x)
            if len(dups) > 0:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'codes': ' '.join(x for x in set(dups))} ] )
        except Exception, e:
            print e
            return 
    def miscarriage_mismatch(self, position = 6, key = 'previous_symptoms', errcode = "miscarriage_mismatch"):
        try:
            symps_lower = [x.lower() for x in self.previous_symptoms]
            if 'rm' in  symps_lower and self.miscarriage() < 3:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            print e
            return  

    def gravidity_mismatch_symptoms(self, position = 6, key = 'previous_symptoms', errcode = "gravidity_mismatch_symptoms"):
        try:
            symps_lower = [x.lower() for x in self.previous_symptoms]
            if 'nr' not in  symps_lower and self.gravidity == 1:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            print e
            return

    def incoherent_jam_nr_symptom(self, position = 6, key = 'previous_symptoms', errcode = "incoherent_jam_nr_symptom"):
        try:
            symps_lower = [x.lower() for x in self.previous_symptoms]
            if 'nr' in  symps_lower and len(symps_lower) > 1:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            print e
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
            print e
            return 

    def missing_current_symptoms(self, position = 7, key = 'current_symptoms', errcode = "missing_current_symptoms"):
        try:
            symptoms = self.sms_dict.get(position).get('value')
            symptoms = symptoms.strip().split(" ")
            self.current_symptoms = symptoms
        except Exception, e:
            print e
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
            print e
            return

    def incoherent_jam_np_symptom(self, position = 7, key = 'current_symptoms', errcode = "incoherent_jam_np_symptom"):
        try:
            symps_lower = [x.lower() for x in self.current_symptoms]
            if 'np' in  symps_lower and len(symps_lower) > 1:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            print e
            return

    def invalid_code(self, key = 'invalid', errcode = 'invalid_code'):
        try:
            codes = re.findall("\s[A-Za-z]{2,3}", self.text)
            invalides = []
            for x in codes:
                if x.lower().strip() not in [ k.key for k in self.report.smsreportfield_set.all()] + [
                                                         k.prefix for k in self.report.smsreportfield_set.all() if k.prefix] + [
                                                            self.report.keyword.lower() ]:
                    invalides.append(x.strip())
            if invalides: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {
                                                                                                    'report': getattr(self.report, 'title_%s'%self.language),
                                                                                                    'codes': ' '.join( x for x in  invalides) } ] )
        except Exception, e:
            print e
            return

    def missing_location(self, position = 8, key = 'location', errcode = "missing_location"):
        try:
            location = self.sms_dict.get(position).get('value')
            self.location = location.strip().split(" ") 
        except Exception, e:
            print e
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
            print e
            return

    def missing_mother_weight(self, position = 9, key = 'mother_weight', errcode = "missing_mother_weight"):
        try:
            weight = self.sms_dict.get(position).get('value')
            self.mother_weight = get_weight(weight)
            print self.mother_weight
        except Exception, e:
            print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def invalid_mother_weight(self, position = 9, key = 'mother_weight', errcode = "invalid_mother_weight"):
        try:
            if self.mother_weight > 150 or self.mother_weight < 35:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            print e
            return 

    def missing_mother_height(self, position = 10, key = 'mother_height', errcode = "missing_mother_height"):
        try:
            height = self.sms_dict.get(position).get('value')
            self.mother_height = get_height(height)
            print self.mother_height
        except Exception, e:
            print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        return

    def invalid_mother_height(self, position = 10, key = 'mother_height', errcode = "invalid_mother_height"):
        try:
            if self.mother_height > 250 or self.mother_height < 50:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            print e
            return 

    def missing_toilet(self, position = 11, key = 'toilet', errcode = "missing_toilet"):
        try:
            toilet = self.sms_dict.get(position).get('value')
            self.toilet = toilet.strip().split(" ") 
        except Exception, e:
            print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
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
            print e
            return

    def missing_handwashing(self, position = 12, key = 'handwashing', errcode = "missing_handwashing"):
        try:
            handwashing = self.sms_dict.get(position).get('value')
            self.handwashing = handwashing.strip().split(" ") 
        except Exception, e:
            print e
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
            print e
            return

    def get_group_fields(self, group='anc_visit', category_en = 'Number of ANC'):
        try:
            ans = []
            for f in self.report.smsreportfield_set.filter(category_en__icontains = category_en):
                ans.append(f.key.lower())
            setattr(self, group, ans)
            return ans
        except Exception, e:
            print e
            return []


    def missing_group_fields(self, position = 3, key = 'anc_visit', errcode = "missing_anc_visit"):
        try:
            dvas = self.sms_dict.get(position).get('value')
            dvas = dvas.strip().split(" ")
            if setattr(self, key, dvas)
        except Exception, e:
            print e
            self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
            return 

    def invalid_group_field(self, position = 3, key = 'anc_visit', errcode = "invalid_anc_visit", category = 'Number of ANC' ):
        try:
            dvas = getattr(self, key)
            setattr(self, key, get_group_fields( group = key, category_en = category)) 
            symps_lower = [x.lower() for x in dvas]
            inv = False
            for x in symps_lower:
                if x not in getattr(self, key):
                    inv = True
            if inv is True: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)] )
        except Exception, e:
            print e
            return

    def incoherent_jam_np_symptom(self, position = 7, key = 'current_symptoms', errcode = "incoherent_jam_np_symptom"):
        try:
            symps_lower = [x.lower() for x in self.current_symptoms]
            if 'np' in  symps_lower and len(symps_lower) > 1:
                self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        except Exception, e:
            print e
            return

    def invalid_code(self, key = 'invalid', errcode = 'invalid_code'):
        try:
            codes = re.findall("\s[A-Za-z]{2,3}", self.text)
            invalides = []
            for x in codes:
                if x.lower().strip() not in [ k.key for k in self.report.smsreportfield_set.all()] + [
                                                         k.prefix for k in self.report.smsreportfield_set.all() if k.prefix] + [
                                                            self.report.keyword.lower() ]:
                    invalides.append(x.strip())
            if invalides: self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {
                                                                                                    'report': getattr(self.report, 'title_%s'%self.language),
                                                                                                    'codes': ' '.join( x for x in  invalides) } ] )
        except Exception, e:
            print e
            return
        

def get_weight(text):
    try:
        weight_pattern = re.search("\s(wt\d+\.?\d*)", text)
        weight = re.search("(\d+\.?\d*)", weight_pattern.group(1))
        return float(weight.group(1))
    except Exception, e:
        return None

def get_height(text):
    try:
        height_pattern = re.search("\s(ht\d+\.?\d*)", text)
        height = re.search("(\d+\.?\d*)", height_pattern.group(1))
        return float(height.group(1))
    except Excepion, e:
        return None

def get_muac(text):
    try:
        muac_pattern = re.search("\s(muac\d+\.?\d*)", text)
        muac = re.search("(\d+\.?\d*)", muac_pattern.group(1))
        return float(muac.group(1))
    except Excepion, e:
        return None        


def get_date(text):
    """Tries to parse a string into some python date object."""
    
    today = datetime.date.today()
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
        
            #print "%s = '%s' '%s' '%s'" % (date_string, dd, mm, yyyy)
        
            # make sure we are in the right format
            if len(dd) > 2 or len(mm) > 2 or len(yyyy) != 4: 
                raise Exception(_("Invalid date format, must be in the form: DD.MM.YYYY"))
            
            # invalid year
            #if int(yyyy) > cycle_e.year or int(yyyy) < cycle_s.year:
            #    raise Exception(_("Invalid year, year must be between %(st)d and %(en)d, and date in the form: DD.MM.YYYY" % {'st': cycle_s.year, "en": cycle_e.year}))
        
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


