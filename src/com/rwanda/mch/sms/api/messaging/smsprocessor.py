#!/usr/bin/env python
# encoding: utf-8
# vim: ts=2 expandtab

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

from util.record import GESTATION, fetch_current_pregnancy, fetch_current_child, fetch_current_mother_death, fetch_current_child_death, fetch_current_pregnancy_miscarriage, fetch_gravidity, fetch_parity, fetch_birth_pregnancy, fetch_duplicate_report, fetch_table_cols, fetch_delivery

from sms.api.messaging.zdmapper.messages import cbn, cmr, ccm, pnc, nbc, rar, res, dth, chi, bir, red, risk, dep, anc, ref, pre, smn, rso, common, checker
import re
import datetime
from underscore import _ as UNDERSCORE
import sys, os

WHITELIST = {
                "ASM": [u'PNC', u'NBC', u'RAR', u'RES', u'DTH', u'CHI', u'BIR', u'RED', u'RISK', u'DEP', u'ANC', u'REF', u'PRE', u'WHO'], 
                "BINOME": [u'CBN', u'CMR', u'CCM', u'DTH', u'CHI', u'DEP', u'SMN', u'SMR', u'RSO', u'SO', u'SS', u'WHO'],
                "ADMIN": [u'PNC', u'NBC', u'RAR', u'RES', u'DTH', u'CHI', u'BIR', u'RED', u'RISK', u'DEP', u'ANC', u'REF', u'PRE',
                                        u'CBN', u'CMR', u'CCM', u'DTH', u'CHI', u'DEP', u'SMN', u'SMR', u'RSO', u'SO', u'SS', u'WHO' ]
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

		     "PRE" : pre,

         "SMN" : smn,

         "SMR" : smn,

         "RSO" : rso,

         "SO"  : rso,

         "SS"  : rso
 
            }


## Validate report
class Rectifier(object):
  def __init__(self, chw, message, report, codes, smsdict, pperror):
    self.chw      = chw
    self.role     = self.chw.role_name
    self.language = self.chw.language_code.lower()
    self.message  = message
    self.report_codes    = codes
    self.sms_dict = smsdict
    self.errors   = []
    self.pperror  = pperror
    self.invalides = []
    self.errmessages = MESSAGES_MAPPER.get(report.code).MESSAGES
    self.errmessages.update(common.COMMON_MESSAGES)
    self.reports = WHITELIST.get(self.chw.role_code)
    self.report  = report
    self.GESTATION = GESTATION

  ## process a date field
  def get_date(self, text):
    """Tries to parse a string into some python date object."""

    #today = self.message.date
    #cycle_s = today - datetime.timedelta(days = 1000)
    #cycle_e = today + datetime.timedelta(days = 1000)
     
    date_string = re.search("([0-9.]+)", text)   
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
          #print "Invalid date format, must be in the form: DD.MM.YYYY"
          return None
                
        # invalid year
        #if int(yyyy) > cycle_e.year or int(yyyy) < cycle_s.year:
        #    raise Exception(_("Invalid year, year must be between %(st)d and %(en)d, and date in the form: DD.MM.YYYY" % {'st': cycle_s.year,
        #                                                                                                                 "en": cycle_e.year}))

        # invalid month
        if int(mm) > 12 or int(mm) < 1:
          #print "Invalid month, month must be between 1 and 12, and date in the form: DD.MM.YYYY"
          return None

        # invalid day
        if int(dd) > 31 or int(dd) < 1:
          #print "Invalid day, day must be between 1 and 31, and date in the form: DD.MM.YYYY"
          return None      
            
        #Otherwise, parse into our date format
        return datetime.date(int(yyyy), int(mm), int(dd))
      else:
        #print "Invalid date format, must be in the form: DD.MM.YYYY"
        return None
    else:
      #print "Invalid date format, must be in the form: DD.MM.YYYY"
      return None

  # get weight
  def get_weight(self, text):
    try:
      weight_pattern = re.search("(wt\d+\.?\d*)", text, re.IGNORECASE)
      weight = re.search("(\d+\.?\d*)", weight_pattern.group(1))
      return float(weight.group(1))
    except Exception, e:
      return None

  # get height
  def get_height(self, text):
    try:
      height_pattern = re.search("(ht\d+\.?\d*)", text, re.IGNORECASE)
      height = re.search("(\d+\.?\d*)", height_pattern.group(1))
      return float(height.group(1))
    except Exception, e:
      return None

  def get_bmi(self):
    try:
      if hasattr(self, 'mother_weight') and hasattr(self, 'mother_height'): 
        self.bmi = self.mother_weight / ((self.mother_height * self.mother_height) / 10000.0)
      if hasattr(self, 'child_weight') and hasattr(self, 'child_height'): 
        self.bmi = self.child_weight / ((self.child_height * self.child_height) / 10000.0)
    except Exception, e:
      #print e
      pass
    return None

  # get muac
  def get_muac(self, text):
    try:
      muac_pattern = re.search("(muac\d+\.?\d*)", text, re.IGNORECASE)
      muac = re.search("(\d+\.?\d*)", muac_pattern.group(1))
      return float(muac.group(1))
    except Exception, e:
      #print  e
      return None 

  ## check missing field
  def field_missing(self, position = 2, key = 'lmp', errcode = "lmp_missing"):
    try:
      dva = self.sms_dict.get(position)
      if not dva:
        sdva  = self.sms_dict.get('single')
        cdva  = self.sms_dict.get('child')
        if not (sdva or cdva):
          self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        else:
          dva = cdva.group(position) if cdva else sdva.group(position) if sdva else None
          setattr(self, key, dva)
      else:
        setattr(self, key, dva)
      return True            
    except Exception, e:
      #print "Field missing: %s" % e
      pass
        
    return False

  ## check date format field
  def misformat_datefield(self, position = 2, key = 'lmp', errcode = "misformat_lmp"):
    try:
      dva   = self.sms_dict.get(position)
      if not dva:
        sdva  = self.sms_dict.get('single')
        cdva  = self.sms_dict.get('child')
        dva = cdva.group(position) if cdva else sdva.group(position) if sdva else None

      ddva  = self.get_date(dva) 
      if not ddva:
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
      else:
        setattr(self, key,  ddva )
      return True
    except Exception, e:
      #print "Invalid date format : %s" % e
      pass   
    return False

  ## give us nine months ago
  def nine_months_ago(self, date = None):
    if date is None:    date = self.message.date
    return (date - datetime.timedelta(days = self.GESTATION)).date()

  ## give us xy days ago
  def xy_days_ago(self, date = None, days = 0):
    if date is None:    date = self.message.date
    return (date - datetime.timedelta(days = days)).date()

  ## check if date earlier 9 months ago
  def datefield_earlier_9months(self, position = 2, key = 'lmp', errcode = "lmp_earlier_9months"):
    try:
      dva = getattr(self, key)
      if dva < self.nine_months_ago(self.message.date):
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
      return True
    except Exception, e:
      #print  "Date earlier than 9 months: %s" % e
      pass
    return False

  # check our datefield not greater than current date
  def datefield_greater_currentdate(self, position = 2, key = 'lmp', errcode = "lmp_greater_currentdate"):
    try:
      dva = getattr(self, key)
      if dva > self.message.date.date():
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
      return True
    except Exception, e:
      #print " Date greater than current date : %s " % e
      pass
    return False

  # check our datefield not less than current date
  def datefield_lesser_currentdate(self, position = 3, key = 'anc2_date', errcode = "anc2_lesser_currentdate"): 
    try:
      dva = getattr(self, key)
      if dva < self.message.date.date():
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
      return True
    except Exception, e:
      #print "Date lesser than current date: %s " % e
      pass
    return False

  # get current pregnancy
  def get_current_pregnancy(self):
    try:
      self.pregnancy = fetch_current_pregnancy(self.nid, self.nine_months_ago())
      self.pregnancy_pk = self.pregnancy.indexcol
      return self.pregnancy
    except Exception, e:
      #print "Current pregnancy not found: %s" % e
      pass
    return None


  # get current pregnancy miscarriage
  def get_current_miscarriage(self):
    try:
      self.miscarriage = fetch_current_pregnancy_miscarriage(self.pregnancy.indexcol)
      return self.miscarriage
    except Exception, e:
      #print "Current pregnancy miscarriage not found: %s" % e
      pass
    return None


  # get current mother death
  def get_current_mother_death(self):
    try:
      self.mother_death = fetch_current_mother_death(self.nid)
      return self.mother_death
    except Exception, e:
      #print "Current mother death not found: %s" % e
      pass
    return None

  # get current child death
  def get_current_child_death(self):
    try:
      self.child_death = fetch_current_child_death(self.nid, self.child_number, self.birth_date)
      return self.child_death
    except Exception, e:
      #print "Current child death not found: %s" % e
      pass
    return None

  # get birth pregnancy
  def get_birth_pregnancy(self, pregnancy):
    try:
      self.birth_pregnancy = fetch_birth_pregnancy(pregnancy.indexcol)
      self.pregnancy_pk    = self.birth_pregnancy.pregnancy_pk
      return self.birth_pregnancy
    except Exception, e:
      #print "Birth pregnancy not found: %s" % e
      pass
    return None

  # get current gravidity
  def get_current_gravidity(self):
    try:
      self.current_gravidity = fetch_gravidity(self.nid)
      return self.current_gravidity
    except Exception, e:
      #print "Current gravidity not found: %s" % e
      pass
    return None

  # get current parity
  def get_current_parity(self):
    try:
      self.current_parity = fetch_parity(self.nid)
      return self.current_parity
    except Exception, e:
      #print "Current parity not found: %s" % e
      pass
    return None

  # get current LMP
  def get_current_lmp(self):
    try:
      self.lmp = self.pregnancy.lmp.date()
      return self.lmp
    except Exception, e:
      #print "LMP not found: %s " % e
      pass
    return None

  # get current EDD
  def get_current_edd(self):
    try:
      self.edd = self.lmp + datetime.timedelta(days = self.GESTATION)
      return self.edd
    except Exception, e:
      #print "EDD not found: %s " % e
      pass
    return None 

  # get current child
  def get_current_child(self):
    try:
      self.child = fetch_current_child(self.nid, self.child_number, self.birth_date)
      self.child_pk = self.child.indexcol
      self.pregnancy_pk = self.child.pregnancy_pk
      return self.child
    except Exception, e:
      #print "Current child not found: %s" % e
      pass
    return None

  # check our datefield not later than EDD
  def datefield_later_edd(self, position = 3, key = 'anc2_date', errcode = "anc2_date_later_edd"): 
    try:
      dva = getattr(self, key)
      edd = self.edd
      if dva and edd and dva > edd :
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
      return True
    except Exception, e:
      #print " Date later than EDD : %s " % e
      pass
    return False

  # check our datefield not lesser than LMP
  def datefield_lesser_lmp(self, position = 3, key = 'anc2_date', errcode = "anc2_date_lesser_lmp"): 
    try:
      dva = getattr(self, key)
      lmp = self.lmp
      if  dva and lmp and dva < lmp:
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
      return True
    except Exception, e:
      #print "Date less than LMP: %s " % e
      pass
    return False

  # check if is number field
  def misformat_numberfield(self, position = 4, key = 'gravidity', errcode = "misformat_gravidity"): 
    try:
      dva = self.sms_dict.get(position)
      if not dva:
        sdva  = self.sms_dict.get('single')
        cdva  = self.sms_dict.get('child')
        dva = cdva.group(position) if cdva else sdva.group(position) if sdva else None
      dvag = re.search("([0-9]+)", dva)
      if not dvag:
         self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
      else:
        setattr(self, key, int(dvag.group(1)) )
      return True
    except Exception, e:
      #print "Invalid Number field: %s" % e
      pass
    return False

  # check if number field is in the range of min and max
  def numberfield_not_between_minv_maxv(self, position = 4, key = 'gravidity', errcode = "gravidity_not_between_1_30", minv = 1, maxv = 30): 
    try:
      dva = getattr(self, key)
      if dva < minv or dva > maxv:
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
      return True
    except Exception, e:
      #print "Nummber not in range : %s " % e
      pass
    return False

  # check if the codes are valid
  def invalid_codes(self, position = 7, key = 'current_symptoms', errcode = "invalid_current_symptom", db_position = None):
    try:
      symptoms = UNDERSCORE(self.report_codes).chain().filter(lambda x, *args: x.position == position
                                                        ).map(lambda x, *args: x.code.lower()).sortBy().value()
      reported_symptoms = getattr(self, key).split()
      if db_position and db_position != position :            
            symptoms = UNDERSCORE(self.report_codes).chain().filter(lambda x, *args: x.position == db_position
                                                        ).map(lambda x, *args: x.code.lower()).sortBy().value()
            sdva  = self.sms_dict.get('single')
            cdva  = self.sms_dict.get('child')
            pattern_reported_symptoms = cdva.group(position) if cdva else sdva.group(position)
            if pattern_reported_symptoms:
              pattern_lower_reported_symptoms = set([x.lower() for x in pattern_reported_symptoms.split()])
              setattr(self, key, pattern_reported_symptoms)
              reported_symptoms = pattern_reported_symptoms.split()
            else:
              self.errors.append( ["missing_current_symptoms", self.errmessages.get(key).get("missing_current_symptoms").get(self.language)] )
          
      lower_reported_symptoms = set([x.lower() for x in reported_symptoms])
      if not lower_reported_symptoms.issubset(set(symptoms)):
        ## pattern at this area before denying the code
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language)] )

      for code in reported_symptoms:
        if code.lower() not in symptoms: self.invalides.append(code)
      ##print reported_symptoms, symptoms
      return True
    except Exception, e:
      #print "Invalid code : %s" % e
      pass
    return False

  # check if the sms codes are valid
  def invalid_sms_codes(self, key = 'invalid', errcode = "invalid_code"):
    try:
      if self.invalides:
        self.errors.append( [errcode,
                            self.errmessages.get(key).get(errcode).get(self.language) % {
                                'report': self.keyword, 'codes': ' '.join( self.invalides) 
                                }
                            ] )
      return True
    except Exception, e:
      #print "Invalid sms code : %s" % e
      pass
    return False

  # check if codes are without a jam code
  def incoherent_jam_codes(self, position = 7, key = 'current_symptoms', errcode = "incoherent_jam_np_symptom", jam = "np"):
    try:
      reported_symptoms = set([ x.lower() for x in getattr(self, key).split() ])
      if jam.lower() in  reported_symptoms and len(reported_symptoms) > 1:
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
      return True
    except Exception, e:
      #print "Invalid jam: %s " % e
      pass
    return False

  # check for no duplicated codes
  def duplicate_codes(self, position = 6, key = 'previous_symptoms', errcode = "duplicate_symptom", extra = None):
    try:
      reported_symptoms = [ x for x in getattr(self, key).split() ]
      set_reported_symptoms = set([ x.lower() for x in reported_symptoms])
      if len(reported_symptoms) !=  len(set_reported_symptoms):
        dups = [i for i in reported_symptoms if not i in set_reported_symptoms or set_reported_symptoms.remove(i)]
        if extra:
          self.errors.append( [errcode, self.errmessages.get(extra).get(errcode).get(self.language) % {'codes': ' '.join(set(dups))} ] )
        else:
          self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {'codes': ' '.join(set(dups))} ] )
      return True
    except Exception, e:
      #print "Duplicate code: %s" % e
      pass
    return False 

  # check if code is only one at that specific position 
  def incoherent_unique_codes(self, position = 8, key = 'location', errcode = "invalid_location"):
    try:
      reported_symptoms = set([ x.lower() for x in getattr(self, key).split() ])
      if len(reported_symptoms) > 1:
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
      return True
    except Exception, e:
      #print "Invalid unique code: %s " % e
      pass
    return False
  
  ## validate reporter
  def validate_reporter(self, key = 'invalid', errcode = 'invalid_reporter'):
    try:
      keyword = self.report.code
      if not keyword or keyword not in self.reports:
        self.errors.append([ errcode,
                            self.errmessages.get(key).get(errcode).get(self.language) % {
                            'report': getattr(self.report, self.language), 'role': self.role, 'rkey': keyword }
                          ] )
      else:
        self.keyword = keyword.upper()
      return True
    except Exception, e:
      #print "Error validating reporter: %s" % e
      pass
    return False

  ## validate nid
  def validate_nid(self, position = 1, key = 'nid', errcode = 'invalid_nid'):
    try:
      nid = self.sms_dict.get(position)
      if not nid:
        sdva  = self.sms_dict.get('single')
        cdva  = self.sms_dict.get('child')
        nid = cdva.group(position) if cdva else sdva.group(position) if sdva else None
      if not nid:
         self.errors.append( [ "patient_nid_missing" , self.errmessages.get(key).get("patient_nid_missing").get(self.language) ] )
      else:
        nid = re.search("(\d+)", nid)
        if not nid:
          self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
        else:
          nid = nid.group(1)
          if len(nid) != 16:
            self.errors.append( ["nid_not_16digits", self.errmessages.get(key).get("nid_not_16digits").get(self.language) ] )
          else:
            if nid[0:3] == '078':
              try:
                if nid[0:10] != self.chw.telephone[3:13] and self.keyword.strip() in ['PRE', 'BIR']:
                  self.errors.append( ["phone_mismatch", self.errmessages.get(key).get("phone_mismatch").get(self.language) ] )
                else:
                  phoneid_ddmmyy = datetime.datetime.strptime(nid[10:16],'%d%m%y')
                  _5daysago = self.message.date - datetime.timedelta(days = 5)
                  if self.keyword.strip() in ['PRE', 'BIR'] and (phoneid_ddmmyy < _5daysago or phoneid_ddmmyy > self.message.date):
                    self.errors.append( ["outrange_dated_nid", self.errmessages.get(key).get("outrange_dated_nid").get(self.language) ] )
                  else:
                    self.nid =  nid
              except Exception, ex:
                #print "Invalid PHONE NID: %s" % ex
                self.errors.append( ["misformat_dated_nid", self.errmessages.get(key).get("misformat_dated_nid").get(self.language) ] )         
            else:
              self.nid = nid
      if not hasattr(self, 'nid'):  self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )        
      return True
    except Exception, e:
      #print "Invalid NID: %s" % e
      if not hasattr(self, 'nid'):  self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
      pass
    return False

  ## validate lmp
  def validate_lmp(self, position = 2, key = 'lmp', errcode = 'lmp_missing'):
    try:
      self.field_missing(position = position, key = key, errcode = "lmp_missing")
      self.misformat_datefield(position = position, key = key, errcode = "misformat_lmp")
      self.datefield_earlier_9months(position = position, key = key, errcode = "lmp_earlier_9months")
      self.datefield_greater_currentdate(position = position, key = key, errcode = "lmp_greater_currentdate")
      return True
    except Exception, e:
      #print "Invalid LMP: %s" % e
      pass
    return False

  ## validate anc2_date
  def validate_anc2_date(self, position = 3, key = 'anc2_date', errcode = 'anc2_date_missing'):
    try:
      self.field_missing(position = position, key = key, errcode = "anc2_date_missing")
      self.misformat_datefield(position = position, key = key, errcode = "misformat_anc2_date")
      self.datefield_lesser_currentdate(position = position, key = key, errcode = "anc2_lesser_currentdate")
      # get EDD before comparison
      self.get_current_edd() 
      self.datefield_later_edd(position = position, key = key, errcode = "anc2_date_later_edd")
      return True
    except Exception, e:
      #print "Invalid ANC2 date: %s" % e
      pass
    return False

  ## validate anc_date
  def validate_anc_date(self, position = 2, key = 'anc_date', errcode = 'anc_date_missing'):
    try:
      self.field_missing(position = position, key = key, errcode = "anc_date_missing")
      self.misformat_datefield(position = position, key = key, errcode = "misformat_anc_date")
      self.datefield_greater_currentdate(position = position, key = key, errcode = "anc_date_greater_currentdate")
      # get EDD before comparison
      self.get_current_edd() 
      self.datefield_later_edd(position = position, key = key, errcode = "anc_date_later_edd")
      self.datefield_lesser_lmp(position = position, key = key, errcode = "anc_date_lesser_lmp")
      return True
    except Exception, e:
      #print "Invalid ANC date: %s" % e
      pass
    return False

  ## validate birth date
  def validate_birth_date(self, position = 3, key = 'birth_date', errcode = "missing_birth_date"):
    try:
      self.field_missing(position = position, key = key, errcode = "missing_birth_date")
      self.misformat_datefield(position = position, key = key, errcode = "misformat_birth_date")
      self.datefield_greater_currentdate(position = position, key = key, errcode = "birth_date_greater_currentdate")
      if hasattr(self, 'keyword') and self.keyword.strip() == "BIR":
        setattr(self, 'lmp', self.pregnancy.lmp.date())
        setattr(self, 'pregnancy_pk', self.pregnancy.indexcol)
        self.datefield_lesser_lmp(position = position, key = key, errcode = "birth_date_lesser_lmp")
      return True
    except Exception, e:
      #print "Invalid birth date: %s" % e
      pass
    return False

  ## validate delivery date
  def validate_delivery_date(self, position = 4, key = 'delivery_date', errcode = "missing_delivery_date"):
    try:
      self.field_missing(position = position, key = key, errcode = "missing_delivery_date")
      self.misformat_datefield(position = position, key = key, errcode = "misformat_delivery_date")
      self.datefield_greater_currentdate(position = position, key = key, errcode = "delivery_date_greater_currentdate")      
      if hasattr(self, 'delivery_date'):
        self.delivery = fetch_delivery(self.nid, self.delivery_date)
        if not self.delivery: 
          self.errors.append( ["missing_delivery", self.errmessages.get(key).get("missing_delivery").get(
                                                  self.language) % {'dob': self.delivery_date} ] )
        else:
          self.pregnancy_pk = self.delivery.pregnancy_pk
          self.child_pk = self.delivery.indexcol
      return True
    except Exception, e:
      #print "Invalid delivery date: %s" % e
      pass
    return False

  ## validate_child_number
  def validate_child_number(self, position = 2, key = 'child_number', errcode = "missing_child_number"):
    try:
      self.field_missing(position = position, key = key, errcode = "missing_child_number")
      self.misformat_numberfield(position = position, key = key, errcode = "invalid_child_number")
      self.numberfield_not_between_minv_maxv(position = position, key = key, errcode = "invalid_child_number", minv = 1, maxv = 6)
      return True
    except Exception, e:
      #print "Invalid child number: %s" % e
      pass
    return False
  
  ## validate gravidity
  def validate_gravidity(self, position = 4, key = 'gravidity', errcode = "gravidity_missing"):
    try:
      self.field_missing(position = position, key = key, errcode = "gravidity_missing")
      self.misformat_numberfield(position = position, key = key, errcode = "misformat_gravidity")
      self.numberfield_not_between_minv_maxv(position = position, key = key, errcode = "gravidity_not_between_1_30", minv = 1, maxv = 30)
      if self.gravidity <= self.get_current_gravidity():
         self.errors.append( ["mismatch_gravidity_record", self.errmessages.get(key).get("mismatch_gravidity_record").get(self.language
                                ) % {'nid': self.nid, 'pregs': self.current_gravidity}   ] )
      return True
    except Exception, e:
      #print "Invalid gravidity: %s" % e
      pass
    return False

  ## validate parity
  def validate_parity(self, position = 5, key = "parity", errcode = "missing_parity"):
    try:
      self.field_missing(position = position, key = key, errcode = "missing_parity")
      self.misformat_numberfield(position = position, key = key, errcode = "misformat_parity")
      if self.parity >= self.gravidity:
         self.errors.append( ["outrange_parity", self.errmessages.get(key).get("outrange_parity").get(self.language) ] )
      return True
    except Exception, e:
      #print "Invalid gravidity: %s" % e
      pass
    return False

  ## validate previous symptoms
  def validate_previous_symptoms(self, position = 6, key = 'previous_symptoms', errcode = "missing_previous_symptoms", db_position = None):
    try:
      self.field_missing(position = position, key = key, errcode = "missing_previous_symptoms")
      self.invalid_codes(position = position, key = key, errcode = "invalid_previous_symptom", db_position = db_position)
      self.duplicate_codes(position = position, key = key, errcode = "duplicate_symptom")
      self.incoherent_jam_codes(position = position, key = key, errcode = "incoherent_jam_nr_symptom", jam = "nr")
      ## TODO miscarriage, gravidity
      
      return True
    except Exception, e:
      #print "Invalid previous sysmptoms: %s" % e
      pass
    return False
    
  ## validate current symptoms
  def validate_current_symptoms(self, position = 7, key = 'current_symptoms', errcode = "missing_current_symptoms", db_position = None):
    try:
      self.field_missing(position = position, key = key, errcode = "missing_current_symptoms")
      self.invalid_codes(position = position, key = key, errcode = "invalid_current_symptom", db_position = db_position)
      self.duplicate_codes(position = position, key = key, errcode = "duplicate_symptom")
      self.incoherent_jam_codes(position = position, key = key, errcode = "incoherent_jam_np_symptom", jam = "np")
      return True
    except Exception, e:
      #print "Invalid current sysmptoms: %s" % e
      pass
    return False

  ## validate location
  def validate_location(self, position = 8, key = 'location', errcode = "missing_location", db_position = None):
    try:
      self.field_missing(position = position, key = key, errcode = "missing_location")
      self.invalid_codes(position = position, key = key, errcode = "invalid_location", db_position = db_position)
      self.duplicate_codes(position = position, key = key, errcode = "duplicate_code", extra = 'invalid')
      self.incoherent_unique_codes(position = position, key = key, errcode = "invalid_location")
      return True
    except Exception, e:
      #print "Invalid location: %s" % e
      pass
    return False

  ## validate weight
  def validate_weight(self, position = 9, key = 'mother_weight', errcode = "missing_mother_weight"):
    try:
      if key.strip() == 'mother_weight': 
        self.field_missing(position = position, key = key, errcode = "missing_mother_weight")
        setattr(self, key, self.get_weight(getattr(self, key)))
        self.numberfield_not_between_minv_maxv(position = position, key = key, errcode = "invalid_mother_weight", minv = 35, maxv = 150)
      elif key.strip() == 'child_weight':
        self.field_missing(position = position, key = key, errcode = "missing_child_weight")
        setattr(self, key, self.get_weight(getattr(self, key)))
        self.numberfield_not_between_minv_maxv(position = position, key = key, errcode = "invalid_child_weight", minv = 1, maxv = 25)
      else:
        pass
      return True
    except Exception, e:
      #print "Invalid weight: %s" % e
      pass
    return False
  
  ## validate height
  def validate_height(self, position = 10, key = 'mother_height', errcode = "missing_mother_height"):
    try:
      if key.strip() == 'mother_height': 
        self.field_missing(position = position, key = key, errcode = "missing_mother_height")
        setattr(self, key, self.get_height(getattr(self, key)))
        self.numberfield_not_between_minv_maxv(position = position, key = key, errcode = "invalid_mother_height", minv = 50, maxv = 250)
      elif key.strip() == 'child_height':
        self.field_missing(position = position, key = key, errcode = "missing_child_height")
        setattr(self, key, self.get_height(getattr(self, key)))
        self.numberfield_not_between_minv_maxv(position = position, key = key, errcode = "invalid_child_height", minv = 40, maxv = 150)
      else:
        pass
      return True
    except Exception, e:
      #print "Invalid height: %s" % e
      pass
    return False

  ## validate toilet
  ## validate handwash
  def validate_unique_codes(self, position = 11, key = 'toilet', errcodes = ["missing_toilet", "invalid_toilet"] , db_position = None):
    try:
      self.field_missing(position = position, key = key, errcode = errcodes[0] )
      self.invalid_codes(position = position, key = key, errcode = errcodes[1] , db_position = db_position)
      self.duplicate_codes(position = position, key = key, errcode = "duplicate_code", extra = 'invalid')
      self.incoherent_unique_codes(position = position, key = key, errcode = errcodes[1] )
      return True
    except Exception, e:
      #print "Invalid unique code: %s" % e
      pass
    return False


  def validate_death_codes(self, position = 4, key = 'death', errcode = "missing_death", db_position = None):
    try:
      self.field_missing(position = position, key = key, errcode = errcode )
      self.invalid_codes(position = position, key = key, errcode = "invalid_death" , db_position = db_position)
      self.duplicate_codes(position = position, key = key, errcode = "duplicate_code", extra = 'invalid')
      self.incoherent_unique_codes(position = position, key = key, errcode = "invalid_death" )
      self.pregnancy = self.get_current_pregnancy()
      self.child = self.get_current_child()
      if hasattr(self, 'death') and getattr(self, 'death').strip().upper() == 'MD':
        pregnancy = getattr(self, 'pregnancy') if hasattr(self, 'pregnancy') else None
        birth_pregnancy = getattr(self, 'child') if hasattr(self, 'child') else None
        if (pregnancy and (pregnancy.lmp <= self.message.date <= self.pregnancy.lmp + datetime.timedelta(days = GESTATION + 42)) ) or (
        birth_pregnancy and (birth_pregnancy.birth_date <= self.message.date <= birth_pregnancy.birth_date + datetime.timedelta(days = 42) ) ):
          pass
        else:
          self.errors.append( ["outrange_md_death", self.errmessages.get(key).get("outrange_md_death").get(self.language) ] )

      if hasattr(self, 'death') and getattr(self, 'death').strip().upper() == 'ND':
        if self.birth_date <= self.message.date.date() <= self.birth_date + datetime.timedelta(days = 28): pass
        else:
          self.errors.append( ["outrange_nd_death", self.errmessages.get(key).get("outrange_nd_death").get(self.language) ] )

      if hasattr(self, 'death') and getattr(self, 'death').strip().upper() == 'CD':
        if self.birth_date + datetime.timedelta(days = 28) <= self.message.date.date() <= self.birth_date + datetime.timedelta(days = 1830):
          pass
        else:
          self.errors.append( ["outrange_cd_death", self.errmessages.get(key).get("outrange_cd_death").get(self.language) ] )
        
      return True
    except Exception, e:
      #print "Invalid unique code: %s" % e
      pass
    return False

  ## validate muac
  def validate_muac(self, position = 13, key = 'muac', errcode = "missing_muac"):
    try:
      muac = self.sms_dict.get(position)
      if not muac:
        sdva  = self.sms_dict.get('single')
        cdva  = self.sms_dict.get('child')
        muac = cdva.group(position) if cdva else sdva.group(position) if sdva else None
        
      if hasattr(self, 'birth_date') and self.birth_date + datetime.timedelta(days = 180)  < datetime.datetime.today().date() and not muac: 
        pass
      else:
        self.field_missing(position = position, key = key, errcode = "missing_muac")
        setattr(self, key, self.get_muac(getattr(self, key)))
        self.numberfield_not_between_minv_maxv(position = position, key = key, errcode = "invalid_muac", minv = 6, maxv = 26)
      return True
    except Exception, e:
      #print "Invalid muac: %s" % e
      pass
    return False

  ## validate mother's telephone
  def mother_has_phone(self, position = 14, key = 'mother_phone', errcode = "invalid_phone"):
    try:
      phone = self.sms_dict.get(position)
      if not phone:
        sdva  = self.sms_dict.get('single')
        cdva  = self.sms_dict.get('child')
        phone = cdva.group(position) if cdva else sdva.group(position) if sdva else None
      phone = re.search("(\d+)", phone)            
      if phone and not (len(phone.group(1)) == 10 and phone.group(1)[0:2] == '07'):
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) ] )
      else:
        self.mother_phone = phone.group(1)
      return True                
    except Exception, e:
      #print "Invalid mother phone: %s" % e
      pass
    return False

  ## validate current pregnancy from record
  ## validate current mother death from record
  ## validate current pregnancy miscarriage from record
  ## validate duplicate report
  def validate_current_pregnancy(self, key = 'invalid', errcode = 'missing_pregnancy'):
    try:
      pregnancy = self.get_current_pregnancy()
      miscarriage = self.get_current_miscarriage()
      birth_pregnancy = self.get_birth_pregnancy(pregnancy)
      death = self.get_current_mother_death()
      bmi = self.get_bmi()

      if birth_pregnancy and self.keyword.strip() != 'PRE':
          if self.keyword.strip() == 'RED' and self.xy_days_ago(days = 90) < birth_pregnancy.birth_date.date():
            pass
          else:
            self.errors.append( ["delivered_already", self.errmessages.get(key).get("delivered_already").get(self.language) % {
                                                'report': self.keyword, 'nid': self.nid } ] )

      if death:
        self.errors.append( ['mother_death', self.errmessages.get(key).get('mother_death').get(self.language) % {
                                            'report': self.keyword, 'nid': self.nid }] )

      if pregnancy and miscarriage and self.keyword.strip() != 'PRE':
        self.errors.append( ["miscarriage", self.errmessages.get('invalid').get("miscarriage").get(self.language) % {
                                              'nid': self.nid, 'report': self.keyword } ] )

      if pregnancy and self.keyword.strip() == 'PRE' and not ( miscarriage or birth_pregnancy) :
        self.errors.append( ["preg_duplicated_nid", self.errmessages.get('nid').get("preg_duplicated_nid").get(self.language) ] )
     
      if not pregnancy and self.keyword.strip() != 'PRE':
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {
                                      'nid': self.nid, 'report': self.keyword } 
                            ] )

      return True                
    except Exception, e:
      #print "Invalid current pregnancy: %s" % e
      pass
    return False

  ## validate current child from record
  ## validate current child death from record
  ## validate duplicate report
  def validate_current_child(self, key = 'invalid', errcode = 'missing_child'):
    try:
      child = self.get_current_child()
      death = self.get_current_child_death()
      bmi   = self.get_bmi()

      if death:
        self.errors.append( ["child_death", self.errmessages.get(key).get("child_death").get(self.language) % {
                                            'report': self.keyword,
                                            'nid': self.nid,
                                            'chino': self.child_number,
                                            'dob': self.birth_date }
                            ] )

      if child and self.keyword.strip() == 'BIR':
        self.errors.append( ["duplicate_birth", self.errmessages.get('birth_date').get("duplicate_birth").get(self.language) % {
                                      'nid': self.nid, "chino": self.child_number, "dob": self.birth_date }
                             ] )
      elif not child and self.keyword.strip() != 'BIR':
        self.errors.append( [errcode, self.errmessages.get(key).get(errcode).get(self.language) % {
                                      'nid': self.nid, 'report': self.keyword } 
                            ] )
      else:
        pass
      return True                
    except Exception, e:
      #print "Invalid current child : %s" % e
      pass
    return False

  ## validate result report
  ## validate duplicate report
  ## Need to optimize the if clause here TODO
  def validate_duplicate_report(self):
    from sms.api.messaging.persister import Persister
    try:
      mapper  = Persister(self).mapper
      filters = getattr(mapper.get_unique_query(), 'UNIQUE_QUERY')
      tbl   = getattr(mapper, self.keyword.lower()).table
      dup  = fetch_duplicate_report(tbl, filters)
      #print "DUP", dup

      if self.keyword.strip() in ['ANC', 'NBC', 'PNC', 'CHI']:
        filters = {'national_id = %s': self.nid}
        if self.keyword.strip() == 'ANC':
          num_visit  = int(self.anc_visit[3:]) - 1
          prev_visit = 'anc%d' % num_visit
          filters.update({"lower(anc_visit) LIKE %s" : '%%%s%%' % prev_visit, 'pregnancy_pk = %s': self.pregnancy_pk})
          res= fetch_table_cols('ancvisit', filters, cols = ['indexcol'])
          if not res and num_visit >= 2:
            self.errors.append( ["invalid_sequence", self.errmessages.get("anc_visit").get("invalid_sequence"
                                  ).get(self.language) % {'visit': num_visit + 1, 'pre_visit': num_visit}] )
        if self.keyword.strip() == 'PNC':
          num_visit  = int(self.pnc_visit[3:]) - 1
          prev_visit = 'pnc%d' % num_visit
          filters.update({"lower(pnc_visit) LIKE %s" : '%%%s%%' % prev_visit, 'pregnancy_pk = %s': self.pregnancy_pk})
          res= fetch_table_cols('pncvisit', filters, cols = ['indexcol'])
          if not res and num_visit >= 2:
            self.errors.append( ["invalid_sequence", self.errmessages.get("pnc_visit").get("invalid_sequence"
                                  ).get(self.language) % {'visit': num_visit + 1, 'pre_visit': num_visit}] )
        if self.keyword.strip() == 'NBC':
          num_visit  = int(self.nbc_visit[3:]) - 1
          prev_visit = 'nbc%d' % num_visit
          filters.update({"lower(nbc_visit) LIKE %s" : '%%%s%%' % prev_visit, 'child_pk = %s': self.child_pk})
          res= fetch_table_cols('nbcvisit', filters, cols = ['indexcol'])
          if not res and num_visit >= 2:
            self.errors.append( ["invalid_sequence", self.errmessages.get("nbc_visit").get("invalid_sequence"
                                  ).get(self.language) % {'visit': num_visit + 1, 'pre_visit': num_visit}] )

        if self.keyword.strip() == 'CHI':
          res = None
          if hasattr(self, 'vaccine'):
            num_visit  = int(self.vaccine[1:]) - 1
            prev_visit = 'v%d' % num_visit
            filters.update({"lower(vaccine) LIKE %s" : '%%%s%%' % prev_visit, 'child_pk = %s': self.child_pk})
            res= fetch_table_cols('childhealth', filters, cols = ['indexcol'])
            if not res and num_visit > 2:
              self.errors.append( ["invalid_sequence", self.errmessages.get("vaccine").get("invalid_sequence"
                                  ).get(self.language) % {'visit': num_visit + 1, 'pre_visit': num_visit}] )          

      if self.keyword.strip() in ['RED', 'RAR', 'CCM', 'CMR', 'RISK', 'RES']:
        filters = {'national_id = %s': self.nid}
        if hasattr(self, 'birth_date') and hasattr(self, 'child_number'):
          filters = { 'national_id = %s': self.nid, 'birth_date = %s': self.birth_date, 'child_number = %s': self.child_number}
        
        ##print filters
        rpts = fetch_table_cols(tbl, filters, cols = ['indexcol'])
        res  = []
        if self.keyword.strip() == 'RED':
          if not (hasattr(self, 'birth_date') or hasattr(self, 'child_number') ): filters.update({'child_pk IS NULL': ''})
          res = fetch_table_cols('redresult', filters, cols = ['red_pk AS res'])
        if self.keyword.strip() == 'CCM': res = fetch_table_cols('cmr', filters, cols = ['ccm_pk AS res'])
        if self.keyword.strip() == 'RISK': res= fetch_table_cols('riskresult', filters, cols = ['risk_pk AS res'])
        if self.keyword.strip() == 'RAR':
          if not (hasattr(self, 'birth_date') or hasattr(self, 'child_number') ): filters.update({'child_pk IS NULL': ''})
          rpts  = fetch_table_cols('redalert', filters, cols = ['indexcol'])
          res   = fetch_table_cols('redresult', filters, cols = ['red_pk AS res'])
        if self.keyword.strip() == 'CMR':
          rpts  = fetch_table_cols('ccm', filters, cols = ['indexcol'])
          res   = fetch_table_cols('cmr', filters, cols = ['ccm_pk AS res'])
        if self.keyword.strip() == 'RES':
          rpts  = fetch_table_cols('risk', filters, cols = ['indexcol'])
          res  = fetch_table_cols('riskresult', filters, cols = ['risk_pk AS res'])
        
        
        set_rpts  = set([ r.indexcol for r in rpts])
        set_res   = set([ r.res for r in res])
        #print set_rpts, set_res, len(set_rpts), len(set_res)
        if set_rpts == set_res and self.keyword.strip() == 'RAR':
           self.errors.append( ["red_to_respond", self.errmessages.get("invalid").get("red_to_respond").get(self.language) ] )
        if set_rpts == set_res and self.keyword.strip() == 'RES':
           self.errors.append( ["risk_to_respond", self.errmessages.get("invalid").get("risk_to_respond").get(self.language) ] )
        if set_rpts == set_res and self.keyword.strip() == 'CMR':
           self.errors.append( ["ccm_to_respond", self.errmessages.get("invalid").get("ccm_to_respond").get(self.language) ] )

        if len(set_rpts) > len(set_res) and self.keyword.strip() in ['RED', 'CCM', 'RISK']:
          if hasattr(self, 'birth_date') and hasattr(self, 'child_number'):
            self.errors.append( ["unresponded_child_report", self.errmessages.get("invalid").get("unresponded_child_report").get(self.language
                                ) % {'report': self.keyword, 'nid': self.nid, 'chino': self.child_number, 'dob': self.birth_date } ] )
          else:
            self.errors.append( ["unresponded_report", self.errmessages.get("invalid"
                                ).get("unresponded_report").get(self.language) % {'report': self.keyword, 'nid': self.nid } ] )

        elif len(set_rpts) > len(set_res) and self.keyword.strip() in ['RAR', 'CMR', 'RES']:
          rpt_pk_l = list(set_rpts - set_res)
          rpt_pk_l.sort()
          rpt_pk   = rpt_pk_l[len(rpt_pk_l) - 1 ] if  rpt_pk_l and len(rpt_pk_l) - 1 > -1 else None
          if rpt_pk:
            setattr(self, 'report_pk', rpt_pk)
            if self.keyword.strip() == 'RAR': dup = fetch_duplicate_report(tbl, {'red_pk = %s': rpt_pk})
            if self.keyword.strip() == 'RES': dup = fetch_duplicate_report(tbl, {'risk_pk = %s': rpt_pk})
            if self.keyword.strip() == 'CMR': dup = fetch_duplicate_report(tbl, {'ccm_pk = %s': rpt_pk})
         
        
      if dup:
        if self.keyword.strip() in ['ANC', 'RED', 'CCM', 'CMR', 'RISK', 'RES', 'RAR', 'PNC', 'SMN', 'SMR',
                                    'SS', 'RSO', 'SO', 'CHI', 'DEP', 'NBC', 'DTH']:
          self.errors.append( ["duplicate_report", self.errmessages.get("invalid"
                                ).get("duplicate_report").get(self.language)  % {'report':self.message.text } ] )
        if self.keyword.strip() == 'CBN':
            self.errors.append( ["duplicate_cbn", self.errmessages.get("birth_date").get("duplicate_cbn"
                                ).get(self.language)  % {'nid':self.nid, 'chino': self.child_number, 'dob': self.birth_date } ] )
        if self.keyword.strip() == 'REF':
            self.errors.append( ["ref_duplicated_nid", self.errmessages.get("nid"
                                ).get("ref_duplicated_nid").get(self.language)  % {'nid':self.nid } ] )
      else:
        pass
            
      return True      
    except Exception, e:
      #print "Duplicate sms report: %s" % e
      #exc_type, exc_obj, exc_tb = sys.exc_info()
      #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
      #print(exc_type, fname, exc_tb.tb_lineno)
      pass
    return False


## Store report
## Send back feedback message
## Send notifications (sms)
## Send notifications (email)
## Send reminders

