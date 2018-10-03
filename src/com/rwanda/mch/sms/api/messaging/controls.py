#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


CONTROLS = {
		     "CBN" : lambda x: cbn_control(x), 

		     "CMR" : lambda x:  cmr_control(x), 

		     "CCM" : lambda x:  ccm_control(x), 

		     "PNC" : lambda x:  pnc_control(x), 

		     "NBC" : lambda x:  nbc_control(x), 

		     "RAR" : lambda x:  rar_control(x), 

		     "RES" : lambda x:  res_control(x), 

		     "DTH" : lambda x:  dth_control(x), 

		     "CHI" : lambda x:  chi_control(x), 

		     "BIR" : lambda x:  bir_control(x), 

		     "RED" : lambda x:  red_control(x), 

		     "RISK" : lambda x:  risk_control(x), 

		     "DEP" : lambda x:  dep_control(x), 

		     "ANC" : lambda x:  anc_control(x), 

		     "REF" : lambda x:  ref_control(x), 

		     "PRE" : lambda x:  pre_control(x) 
            }

def pre_control(r = None):
    try:    r.validate_nid(position = 1)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
    try:    r.validate_lmp(position = 2)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LMP'} ] )
    try:    r.validate_anc2_date(position = 3)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'ANC2DATE'} ] )
    try:    r.validate_gravidity(position = 4)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'GRAVIDITY'} ] )
    try:    r.validate_parity(position = 5)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PARITY'} ] )
    try:    r.validate_previous_symptoms(position = 6, db_position = 6)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PRE_SYMPTOM'} ] )
    try:    r.validate_current_symptoms(position = 7, db_position = 7)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CUR_SYMPTOM'} ] )
    try:    r.validate_location(position = 8, db_position = 8)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
    try:    r.validate_weight(position = 9, key = 'mother_weight', errcode = "missing_mother_weight")
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'WEIGHT'} ] )
    try:    r.validate_height(position = 10, key = 'mother_height', errcode = "missing_mother_height")
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'HEIGHT'} ] )
    try:    r.validate_unique_codes(position = 11, key = 'toilet', errcodes = ["missing_toilet", "invalid_toilet"], db_position = 11 )
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'TOILET'} ] )
    try:    r.validate_unique_codes(position = 12, key='handwashing', errcodes=["missing_handwashing", "invalid_handwashing"], db_position=12 )
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'HANDWASHING'} ] )
    try:    r.validate_muac()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'MUAC'} ] )
    try:    r.mother_has_phone(position = 14)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PHONE'} ] )
    try:    r.invalid_sms_codes()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
    try:    r.validate_current_pregnancy()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PRE'} ] )
    return r

def ref_control(r = None):
    try:    r.validate_nid(position = 1)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
    try:    r.validate_duplicate_report()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )
    return r

def anc_control(r = None):
    try:    r.validate_nid(position = 1)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
    try:    r.validate_current_pregnancy()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PRE'} ] )
    try:    r.validate_anc_date(position = 2)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'ANCDATE'} ] )
    try:    r.validate_unique_codes(position = 3, key = 'anc_visit', errcodes = ["missing_anc_visit", "invalid_anc_visit"], db_position = 3 )
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'ANCVISIT'} ] )
    try:    r.validate_current_symptoms(position = 4, db_position = 4)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CUR_SYMPTOM'} ] )
    try:    r.validate_location(position = 5, db_position = 5)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
    try:    r.validate_weight(position = 6, key = 'mother_weight', errcode = "missing_mother_weight")
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'WEIGHT'} ] )
    try:    r.validate_muac(position = 7)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'MUAC'} ] )
    try:    r.invalid_sms_codes()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
    try:    r.validate_duplicate_report()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )
    
    return r

def dep_control(r = None):
    if hasattr(r, 'sms_dict')  and r.sms_dict.get('child'):
        try:    r.validate_nid(position = 1)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
        try:    r.validate_child_number(position = 2)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD_NO'} ] )
        try:    r.validate_birth_date(position = 3)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DOB'} ] )
        try:    r.validate_current_child()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD'} ] )
        try:    r.validate_duplicate_report()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )

    else:
        try:    r.validate_nid(position = 1)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
        try:    r.validate_current_pregnancy()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PRE'} ] )
        try:    r.validate_duplicate_report()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )

    return r


def risk_control(r = None):
    try:    r.validate_nid(position = 1)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
    try:    r.validate_current_pregnancy()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PRE'} ] )
    try:    r.validate_current_symptoms(position = 2)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CUR_SYMPTOM'} ] )
    try:    r.validate_location(position = 3)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
    try:    r.validate_weight(position = 4, key = 'mother_weight', errcode = "missing_mother_weight")
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'WEIGHT'} ] )
    try:    r.invalid_sms_codes()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
    try:    r.validate_duplicate_report()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )
    return r

def res_control(r = None):
    try:    r.validate_nid(position = 1)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
    try:    r.validate_current_pregnancy()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PRE'} ] )
    try:    r.validate_current_symptoms(position = 2)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CUR_SYMPTOM'} ] )
    try:    r.validate_location(position = 3)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
    try:    r.validate_unique_codes(position = 4, key = 'intervention', errcodes = ['missing_intervention', 'invalid_intervention'])
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'INTERVENTION'} ] )
    try:    r.validate_unique_codes(position = 5, key = 'mother_status', errcodes = ['missing_mother_status', 'invalid_mother_status'])
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'STATUS'} ] )
    try:    r.invalid_sms_codes()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
    try:    r.validate_duplicate_report()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )
    return r
    return r

def red_control(r = None):
    if hasattr(r, 'sms_dict')  and r.sms_dict.get('child'):
        try:    r.validate_nid(position = 1)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
        try:    r.validate_child_number(position = 2)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD_NO'} ] )
        try:    r.validate_birth_date(position = 3)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DOB'} ] )
        try:    r.validate_current_symptoms(position = 4, key = 'red_symptoms')
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'RED_SYMPTOM'} ] )
        try:    r.validate_location(position = 5, key = 'location')
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
        try:    r.validate_weight(position = 6, key = 'child_weight', errcode = "missing_child_weight")
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'WEIGHT'} ] )
        try:    r.invalid_sms_codes()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
        try:    r.validate_current_child()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD'} ] )
        try:    r.validate_duplicate_report()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )

    else:
        try:    r.validate_nid(position = 1)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
        try:    r.validate_current_pregnancy()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PRE'} ] )
        try:    r.validate_current_symptoms(position = 2, key = 'red_symptoms', db_position = 4)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'RED_SYMPTOM'} ] )
        try:    r.validate_location(position = 3, key = 'location', db_position = 5)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
        try:    r.validate_weight(position = 4, key = 'mother_weight', errcode = "missing_mother_weight")
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'WEIGHT'} ] )
        try:    r.invalid_sms_codes()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
        try:    r.validate_duplicate_report()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )
    
    return r

def rar_control(r = None):
    if hasattr(r, 'sms_dict')  and r.sms_dict.get('child'):
        try:    r.validate_nid(position = 1)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
        try:    r.validate_child_number(position = 2)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD_NO'} ] )
        try:    r.validate_birth_date(position = 3)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DOB'} ] )
        try:    r.validate_current_symptoms(position = 4, key = 'red_symptoms')
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'RED_SYMPTOM'} ] )
        try:    r.validate_location(position = 5, key = 'location')
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
        try:    r.validate_unique_codes(position = 6, key = 'intervention', errcodes = ['missing_intervention', 'invalid_intervention'])
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'INTERVENTION'} ] )
        try:    r.validate_unique_codes(position = 7, key = 'child_status', errcodes = ['missing_mother_status', 'invalid_child_status'])
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'STATUS'} ] )
        try:    r.invalid_sms_codes()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
        try:    r.validate_current_child()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD'} ] )
        try:    r.validate_duplicate_report()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )

    else:
        try:    r.validate_nid(position = 1)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
        try:    r.validate_current_pregnancy()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PRE'} ] )
        try:    r.validate_current_symptoms(position = 2, key = 'red_symptoms', db_position = 4)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'RED_SYMPTOM'} ] )
        try:    r.validate_location(position = 3, key = 'location', db_position = 5)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
        try:    r.validate_unique_codes(position = 4, key = 'intervention', 
                                errcodes = ['missing_intervention', 'invalid_intervention'], db_position = 6)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'INTERVENTION'} ] )
        try:    r.validate_unique_codes(position = 5, key = 'mother_status', 
                                    errcodes = ['missing_mother_status', 'invalid_mother_status'], db_position = 7)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'STATUS'} ] )
        try:    r.invalid_sms_codes()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
        try:    r.validate_duplicate_report()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )
    return r


def bir_control(r = None):
    try:    r.validate_nid(position = 1)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
    try:    r.validate_current_pregnancy()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PRE'} ] )
    try:    r.validate_child_number(position = 2)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD_NO'} ] )
    try:    r.validate_birth_date(position = 3)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DOB'} ] )
    try:    r.validate_unique_codes(position = 4, key = 'gender', errcodes = ["missing_gender", "invalid_gender"] )
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'SEX'} ] )
    try:    r.validate_current_symptoms(position = 5)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CUR_SYMPTOM'} ] )
    try:    r.validate_location(position = 6)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
    try:    r.validate_unique_codes(position = 7, key = 'breastfeeding', errcodes = ["missing_breastfeeding", "invalid_breastfeeding"] )
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'BREASTFEEDING'} ] )
    try:    r.validate_weight(position = 8, key = 'child_weight', errcode = "missing_child_weight")
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'WEIGHT'} ] )
    try:    r.invalid_sms_codes()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
    try:    r.validate_current_child()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'BIR'} ] )
    return r

def chi_control(r = None):
    if hasattr(r, 'sms_dict')  and r.sms_dict.get('child'):
        try:    r.validate_nid(position = 1)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
        try:    r.validate_child_number(position = 2)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD_NO'} ] )
        try:    r.validate_birth_date(position = 3)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DOB'} ] )
        try:    r.validate_unique_codes(position = 4, key = 'vaccine_completion',
                                    errcodes = ["missing_vaccine_completion", "invalid_vaccine_completion"], db_position = 5 )
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'VACCINE_STATUS'} ] )
        try:    r.validate_location(position = 5, db_position = 7)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
        try:    r.validate_weight(position = 6, key = 'child_weight', errcode = "missing_child_weight")
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'WEIGHT'} ] )
        try:    r.validate_muac(position = 7, key = 'muac', errcode = "missing_muac")
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'MUAC'} ] )
        try:    r.invalid_sms_codes()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
        try:    r.validate_current_child()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD'} ] )
        try:    r.validate_duplicate_report()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )

    else:
        try:    r.validate_nid(position = 1)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
        try:    r.validate_child_number(position = 2)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD_NO'} ] )
        try:    r.validate_birth_date(position = 3)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DOB'} ] )
        try:    r.validate_unique_codes(position = 4, key = 'vaccine', errcodes = ["missing_vaccine", "invalid_vaccine"] )
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'VACCINE'} ] )
        try:    r.validate_unique_codes(position = 5, key = 'vaccine_completion',
                                          errcodes = ["missing_vaccine_completion", "invalid_vaccine_completion"] )
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'VACCINE_STATUS'} ] )
        try:    r.validate_current_symptoms(position = 6)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CUR_SYMPTOM'} ] )
        try:    r.validate_location(position = 7)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
        try:    r.validate_weight(position = 8, key = 'child_weight', errcode = "missing_child_weight")
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'WEIGHT'} ] )
        try:    r.validate_muac(position = 9, key = 'muac', errcode = "missing_muac")
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'MUAC'} ] )
        try:    r.invalid_sms_codes()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
        try:    r.validate_current_child()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD'} ] )
        try:    r.validate_duplicate_report()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )

    return r


def cbn_control(r = None):
    try:    r.validate_nid(position = 1)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
    try:    r.validate_child_number(position = 2)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD_NO'} ] )
    try:    r.validate_birth_date(position = 3)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DOB'} ] )
    try:    r.validate_unique_codes(position = 4, key = 'breastfeeding', errcodes = ["missing_breastfeeding", "invalid_breastfeeding"] )
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'BREASTFEEDING'} ] )
    try:    r.validate_weight(position = 5, key = 'child_weight', errcode = "missing_child_weight")
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'WEIGHT'} ] )
    try:    r.validate_muac(position = 6, key = 'muac', errcode = "missing_muac")
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'MUAC'} ] )
    try:    r.invalid_sms_codes()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
    try:    r.validate_current_child()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD'} ] )
    try:    r.validate_duplicate_report()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )
    return r

def ccm_control(r = None):
    try:    r.validate_nid(position = 1)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
    try:    r.validate_child_number(position = 2)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD_NO'} ] )
    try:    r.validate_birth_date(position = 3)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DOB'} ] )
    try:    r.validate_current_symptoms(position = 4, key = 'current_symptoms', errcode = 'missing_current_symptoms')
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CUR_SYMPTOM'} ] )
    try:    r.validate_unique_codes(position = 5, key = 'intervention', errcodes = ['missing_intervention', 'invalid_intervention'])
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'INTERVENTION'} ] )
    try:    r.validate_muac(position = 6, key = 'muac', errcode = "missing_muac")
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'MUAC'} ] )
    try:    r.invalid_sms_codes()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
    try:    r.validate_current_child()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD'} ] )
    try:    r.validate_duplicate_report()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )
    return r

def cmr_control(r = None):
    try:    r.validate_nid(position = 1)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
    try:    r.validate_child_number(position = 2)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD_NO'} ] )
    try:    r.validate_birth_date(position = 3)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DOB'} ] )
    try:    r.validate_current_symptoms(position = 4, key = 'current_symptoms', errcode = 'missing_current_symptoms')
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CUR_SYMPTOM'} ] )
    try:    r.validate_unique_codes(position = 5, key = 'intervention', errcodes = ['missing_intervention', 'invalid_intervention'])
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'INTERVENTION'} ] )
    try:    r.validate_unique_codes(position = 6, key = 'child_status', errcodes = ['missing_mother_status', 'invalid_child_status'])
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'STATUS'} ] )
    try:    r.invalid_sms_codes()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
    try:    r.validate_current_child()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD'} ] )
    try:    r.validate_duplicate_report()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )
    return r


def pnc_control(r = None):
    try:    r.validate_nid(position = 1)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
    try:    r.validate_unique_codes(position = 2, key = 'pnc_visit', errcodes = ["missing_pnc_visit", "invalid_pnc_visit"] )
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PNCVISIT'} ] )
    try:    r.validate_unique_codes(position = 3, key = 'pnc1', errcodes = ["missing_nbc1", "invalid_pnc1"] )
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'PNC1'} ] )
    try:    r.validate_delivery_date(position = 4)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DELIVERYDATE'} ] )
    try:    r.validate_current_symptoms(position = 5)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CUR_SYMPTOM'} ] )
    try:    r.validate_unique_codes(position = 6, key = 'intervention', errcodes = ['missing_intervention', 'invalid_intervention'])
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'INTERVENTION'} ] )
    try:    r.validate_unique_codes(position = 7, key = 'mother_status', errcodes = ['missing_mother_status', 'invalid_mother_status'])
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'STATUS'} ] )
    try:    r.invalid_sms_codes()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
    try:    r.validate_duplicate_report()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )
    return r


def nbc_control(r = None):
    try:    r.validate_nid(position = 1)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
    try:    r.validate_child_number(position = 2)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD_NO'} ] )
    try:    r.validate_unique_codes(position = 3, key = 'nbc_visit', errcodes = ["missing_nbc_visit", "invalid_nbc_visit"] )
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NBCVISIT'} ] )
    try:    r.validate_unique_codes(position = 4, key = 'nbc1', errcodes = ["missing_nbc1", "invalid_nbc1"] )
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NBC1'} ] )
    try:    r.validate_birth_date(position = 5)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DOB'} ] )
    try:    r.validate_unique_codes(position = 6, key = 'v2', errcodes = ["missing_v2", "invalid_v2"] )
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'V2'} ] )
    try:    r.validate_current_symptoms(position = 7)
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CUR_SYMPTOM'} ] )
    try:    r.validate_unique_codes(position = 8, key = 'breastfeeding', errcodes = ["missing_breastfeeding", "invalid_breastfeeding"] )
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'BREASTFEEDING'} ] )
    try:    r.validate_unique_codes(position = 9, key = 'intervention', errcodes = ['missing_intervention', 'invalid_intervention'])
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'INTERVENTION'} ] )
    try:    r.validate_unique_codes(position = 10, key = 'child_status', errcodes = ['missing_child_status', 'invalid_child_status'])
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'STATUS'} ] )
    try:    r.invalid_sms_codes()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CODES'} ] )
    try:    r.validate_current_child()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD'} ] )
    try:    r.validate_duplicate_report()
    except Exception, e:
        r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )
    return r


def dth_control(r = None):
    if hasattr(r, 'sms_dict')  and r.sms_dict.get('child'):
        try:    r.validate_nid(position = 1)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
        try:    r.validate_child_number(position = 2)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'CHILD_NO'} ] )
        try:    r.validate_birth_date(position = 3)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DOB'} ] )
        try:    r.validate_location(position = 4)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
        try:    r.validate_death_codes(position = 5, key = 'death', errcode = 'missing_death')
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DEATHCODE'} ] )
        try:    r.validate_duplicate_report()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )
    else:
        try:    r.validate_nid(position = 1)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'NID'} ] )
        try:    r.validate_location(position = 2, db_position = 4)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'LOCATION'} ] )
        try:    r.validate_death_codes(position = 3, key = 'death', errcode = 'missing_death', db_position = 5)
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DEATHCODE'} ] )
        try:    r.validate_duplicate_report()
        except Exception, e:
            r.errors.append( ['invalid_data', r.errmessages.get('invalid').get('invalid_data').get(r.language) % {'data': 'DUP'} ] )

    return r
