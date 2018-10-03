#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


RECTIFIER_MAPPER = {
		     "CBN" : lambda x: cbn_checker(x), 

		     "CMR" : lambda x:  cmr_checker(x), 

		     "CCM" : lambda x:  ccm_checker(x), 

		     "PNC" : lambda x:  pnc_checker(x), 

		     "NBC" : lambda x:  nbc_checker(x), 

		     "RAR" : lambda x:  rar_checker(x), 

		     "RES" : lambda x:  res_checker(x), 

		     "DTH" : lambda x:  dth_checker(x), 

		     "CHI" : lambda x:  chi_checker(x), 

		     "BIR" : lambda x:  bir_checker(x), 

		     "RED" : lambda x:  red_checker(x), 

		     "RISK" : lambda x:  risk_checker(x), 

		     "DEP" : lambda x:  dep_checker(x), 

		     "ANC" : lambda x:  anc_checker(x), 

		     "REF" : lambda x:  ref_checker(x), 

		     "PRE" : lambda x:  pre_checker(x) 
            }

def pre_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    r.lmp_missing()
    r.misformat_lmp()
    r.lmp_earlier_9months()
    r.lmp_greater_currentdate()
    r.anc2_date_missing()
    r.misformat_anc2_date()
    r.anc2_lesser_currentdate()
    r.anc2_date_later_edd()
    r.gravidity_missing()
    r.misformat_gravidity()
    r.gravidity_not_between_1_30()
    r.mismatch_gravidity_record()
    r.missing_parity()
    r.misformat_parity()
    r.outrange_parity()
    r.missing_previous_symptoms()
    r.duplicate_symptom()
    r.miscarriage_mismatch()
    r.gravidity_mismatch_symptoms()
    r.incoherent_jam_nr_symptom()
    r.invalid_previous_symptom()
    r.missing_current_symptoms()
    r.invalid_current_symptom()
    r.incoherent_jam_np_symptom()
    r.invalid_code()
    r.missing_location()
    r.invalid_location()
    r.missing_mother_weight()
    r.invalid_mother_weight()
    r.missing_mother_height()
    r.invalid_mother_height()
    r.missing_toilet()
    r.invalid_toilet()
    r.missing_handwashing()
    r.invalid_handwashing()
    r.missing_muac(position = 13, key = 'muac', errcode = "missing_muac")
    r.invalid_muac(position = 13, key = 'muac', errcode = "invalid_muac")
    r.mother_has_phone(position = 14, key = 'mother_phone', errcode = "invalid_phone")
    r.get_bmi()
    ## DUPLICATE
    r.preg_duplicated_nid()
    ## DEATH
    r.has_mother_death()
    return r

def ref_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    r.ref_duplicated_nid(position = 1, key = 'nid', errcode = "ref_duplicated_nid") 
    r.preg_not_exists_nid( position = 1, key = 'nid', errcode = "preg_not_exists_nid")
    r.has_mother_death()   
    return r

def anc_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    r.field_missing(position = 2, key = 'anc_date', errcode = "anc_date_missing")
    r.misformat_datefield(position = 2, key = 'anc_date', errcode = "misformat_anc_date")
    r.datefield_greater_currentdate(position = 2, key = 'anc_date', errcode = "anc_date_greater_currentdate")
    r.datefield_later_edd(position = 2, key = 'anc_date', errcode = "anc_date_later_edd")
    r.datefield_lesser_lmp(position = 2, key = 'anc_date', errcode = "anc_date_lesser_lmp")
    r.missing_group_fields(position = 3, key = 'anc_visit', errcode = "missing_anc_visit")
    r.invalid_group_field(position = 3, key = 'anc_visit', errcode = "invalid_anc_visit" )
    r.missing_current_symptoms(position = 4, key = 'current_symptoms', errcode = "missing_current_symptoms")
    r.invalid_current_symptom(position = 4, key = 'current_symptoms', errcode = "invalid_current_symptom")
    r.incoherent_jam_np_symptom(position = 4, key = 'current_symptoms', errcode = "incoherent_jam_np_symptom")
    r.duplicate_symptom(position = 4, key = 'current_symptoms', errcode = "duplicate_symptom")
    r.missing_location(position = 5, key = 'location', errcode = "missing_location")
    r.invalid_location(position = 5, key = 'location', errcode = "invalid_location")
    r.missing_mother_weight(position = 6, key = 'mother_weight', errcode = "missing_mother_weight")
    r.invalid_mother_weight(position = 6, key = 'mother_weight', errcode = "invalid_mother_weight")    
    r.missing_muac(position = 7, key = 'muac', errcode = "missing_muac")
    r.invalid_muac(position = 7, key = 'muac', errcode = "invalid_muac")
    ## INVALID CODE
    r.invalid_code()
    ##DUPLICATES
    r.anc_date_lesser_lastanc(position = 2, key = 'anc_date', errcode = "anc_date_lesser_lastanc", visits = r.get_anc_visits())
    r.duplicate_visit(position = 3, key = 'anc_visit', errcode = "duplicate_anc_visit", visits = r.get_anc_visits() )
    r.invalid_sequence(position = 3, key = 'anc_visit', errcode = "invalid_sequence", max_sequence = range(2,5), visits = r.get_anc_visits() )
    ##PREGNANCY
    r.missing_current_pregnancy()
    ## MISCARRIAGE
    r.miscarriage_found()
    ## DELIVERY
    r.delivered_already( key = 'invalid', errcode = 'delivered_already')
    ## r.missing_current_child()   
    ##DEATH
    r.has_mother_death()
    ##ANC AFTER BIR NOT ACCEPTABLE
    
    return r

def dep_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    if r.valid_number_field(position = 2 ) or r.valid_date_field(position = 2 ) or r.valid_date_field(position = 3):
        r.field_missing(position = 2, key = 'child_number', errcode = "missing_child_number")
        r.misformat_numberfield(position = 2, key = 'child_number', errcode = "invalid_child_number")
        r.numberfield_not_between_minv_maxv(position = 2, key = 'child_number', errcode = "invalid_child_number", minv = 1, maxv = 6)
        r.field_missing(position = 3, key = 'birth_date', errcode = "missing_birth_date")
        r.misformat_datefield(position = 3, key = 'birth_date', errcode = "misformat_birth_date")
        r.datefield_greater_currentdate(position = 3, key = 'birth_date', errcode = "birth_date_greater_currentdate")
        r.missing_current_child()
        r.has_child_death()
    else:
        r.missing_current_pregnancy()
        r.delivered_already( key = 'invalid', errcode = 'delivered_already')
        r.miscarriage_found()
        r.has_mother_death()
        #pass

    r.invalid_code()

    return r


def risk_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    r.missing_current_symptoms(position = 2, key = 'current_symptoms', errcode = "missing_current_symptoms")
    r.invalid_current_symptom(position = 2, key = 'current_symptoms', errcode = "invalid_current_symptom")
    r.incoherent_np_symptom(position = 2, key = 'current_symptoms', errcode = "incoherent_np_symptom")
    r.duplicate_symptom(position = 2, key = 'current_symptoms', errcode = "duplicate_symptom")
    r.missing_location(position = 3, key = 'location', errcode = "missing_location")
    r.invalid_location(position = 3, key = 'location', errcode = "invalid_location")
    r.missing_mother_weight(position = 4, key = 'mother_weight', errcode = "missing_mother_weight")
    r.invalid_mother_weight(position = 4, key = 'mother_weight', errcode = "invalid_mother_weight")
    ## INVALID CODE
    r.invalid_code()
    r.unresponded_record( key="invalid", errcode = 'unresponded_report', records = r.get_unresponded_risk_records())
    r.missing_current_pregnancy()
    r.delivered_already( key = 'invalid', errcode = 'delivered_already')
    r.miscarriage_found()
    r.has_mother_death()
    return r

def res_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    r.missing_current_symptoms(position = 2, key = 'current_symptoms', errcode = "missing_current_symptoms")
    r.invalid_current_symptom(position = 2, key = 'current_symptoms', errcode = "invalid_current_symptom")
    r.incoherent_np_symptom(position = 2, key = 'current_symptoms', errcode = "incoherent_np_symptom")
    r.duplicate_symptom(position = 2, key = 'current_symptoms', errcode = "duplicate_symptom")
    r.missing_location(position = 3, key = 'location', errcode = "missing_location")
    r.invalid_location(position = 3, key = 'location', errcode = "invalid_location")
    r.missing_intervention(position = 4, key = 'intervention', errcode = "missing_intervention")
    r.invalid_intervention(position = 4, key = 'intervention', errcode = "invalid_intervention")
    r.missing_mother_status(position = 5, key = 'mother_status', errcode = "missing_mother_status")
    r.invalid_mother_status(position = 5, key = 'mother_status', errcode = "invalid_mother_status")
    ## INVALID CODE
    r.invalid_code()
    r.missing_to_respond_record(key="invalid", errcode = 'risk_to_respond', records = r.get_unresponded_risk_records())
    r.invalid_symptom_to_respond(key="invalid", errcode = 'invalid_symptom_to_respond',
                                 column_prefix = "symptom", symptoms = r.current_symptoms, records = r.get_unresponded_risk_records())
    r.missing_current_pregnancy()
    r.delivered_already( key = 'invalid', errcode = 'delivered_already')
    r.miscarriage_found()
    r.has_mother_death()
    return r

def red_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    
    if r.valid_number_field(position = 2 ) or r.valid_date_field(position = 2 ) or r.valid_date_field(position = 3):
        r.field_missing(position = 2, key = 'child_number', errcode = "missing_child_number")
        r.misformat_numberfield(position = 2, key = 'child_number', errcode = "invalid_child_number")
        r.numberfield_not_between_minv_maxv(position = 2, key = 'child_number', errcode = "invalid_child_number", minv = 1, maxv = 6)
        r.field_missing(position = 3, key = 'birth_date', errcode = "missing_birth_date")
        r.misformat_datefield(position = 3, key = 'birth_date', errcode = "misformat_birth_date")
        r.datefield_greater_currentdate(position = 3, key = 'birth_date', errcode = "birth_date_greater_currentdate")
        r.missing_child_weight(position = 6, key = 'child_weight', errcode = "missing_child_weight")
        r.invalid_child_weight(position = 6, key = 'child_weight', errcode = "invalid_child_weight")
        r.unresponded_record( key="invalid", errcode = 'unresponded_report', records = r.get_unresponded_child_red_records())
        r.missing_current_child()
        r.has_child_death()
    else:
        r.missing_mother_weight(position = 6, key = 'mother_weight', errcode = "missing_mother_weight")
        r.invalid_mother_weight(position = 6, key = 'mother_weight', errcode = "invalid_mother_weight")
        r.unresponded_record( key="invalid", errcode = 'unresponded_report', records = r.get_unresponded_mother_red_records())
        r.missing_current_pregnancy()
        r.delivered_already( key = 'invalid', errcode = 'delivered_already')
        r.miscarriage_found()
        r.has_mother_death()
    
    r.missing_red_symptoms(position = 4, key = 'red_symptoms', errcode = "missing_red_symptoms")
    r.invalid_red_symptom(position = 4, key = 'red_symptoms', errcode = "invalid_red_symptom")
    r.incoherent_red_np_symptom(position = 4, key = 'red_symptoms', errcode = "incoherent_red_np_symptom")
    r.duplicate_symptom(position = 4, key = 'current_symptoms', errcode = "duplicate_symptom")
    r.missing_location(position = 5, key = 'location', errcode = "missing_location")
    r.invalid_location(position = 5, key = 'location', errcode = "invalid_location")
    r.invalid_code()
        
    return r

def rar_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    records = []

    if r.valid_number_field(position = 2 ) or r.valid_date_field(position = 2 ) or r.valid_date_field(position = 3):
        r.field_missing(position = 2, key = 'child_number', errcode = "missing_child_number")
        r.misformat_numberfield(position = 2, key = 'child_number', errcode = "invalid_child_number")
        r.numberfield_not_between_minv_maxv(position = 2, key = 'child_number', errcode = "invalid_child_number", minv = 1, maxv = 6)
        r.field_missing(position = 3, key = 'birth_date', errcode = "missing_birth_date")
        r.misformat_datefield(position = 3, key = 'birth_date', errcode = "misformat_birth_date")
        r.datefield_greater_currentdate(position = 3, key = 'birth_date', errcode = "birth_date_greater_currentdate")
        r.missing_child_status(position = 7, key = 'child_status', errcode = "missing_child_status")
        r.invalid_child_status(position = 7, key = 'child_status', errcode = "invalid_child_status")
        records = r.get_unresponded_child_red_records()
        r.missing_current_child()
        r.has_child_death()
    else:
        ##TAKE VALUE AT 2 TO THREE IF EMERGENCY DATE IS STILL USED OTHERWISE USE BIRTH_DATE
        r.sms_dict.update( { 3: r.sms_dict.get(2) } )
        r.missing_mother_status(position = 7, key = 'mother_status', errcode = "missing_mother_status")
        r.invalid_mother_status(position = 7, key = 'mother_status', errcode = "invalid_mother_status")
        records = r.get_unresponded_mother_red_records()
        r.missing_current_pregnancy()
        r.delivered_already( key = 'invalid', errcode = 'delivered_already')
        r.miscarriage_found()
        r.has_mother_death()
    
    if records:
        r.sms_dict.update({'emergency_date': records[0]['created_at']})
        #r.field_missing(position = 3, key = 'emergency_date', errcode = "missing_emergency_date")
        #r.misformat_datefield(position = 3, key = 'emergency_date', errcode = "misformat_emergency_date")
        #r.datefield_greater_currentdate(position = 3, key = 'emergency_date', errcode = "emergency_date_greater_currentdate")
        #r.datefield_mismatch(position = 3, key = 'emergency_date', errcode = "emergency_date_mismatch_report_date", records = records, match_key = 'report_date')
           
    r.missing_red_symptoms(position = 4, key = 'red_symptoms', errcode = "missing_red_symptoms")
    r.invalid_red_symptom(position = 4, key = 'red_symptoms', errcode = "invalid_red_symptom")
    r.incoherent_red_np_symptom(position = 4, key = 'red_symptoms', errcode = "incoherent_red_np_symptom")
    r.duplicate_symptom(position = 4, key = 'current_symptoms', errcode = "duplicate_symptom")
    r.missing_location(position = 5, key = 'location', errcode = "missing_location")
    r.invalid_location(position = 5, key = 'location', errcode = "invalid_location")
    r.missing_intervention(position = 6, key = 'intervention', errcode = "missing_intervention")
    r.invalid_intervention(position = 6, key = 'intervention', errcode = "invalid_intervention")
    
    r.invalid_code()    
    r.missing_to_respond_record(key="invalid", errcode = 'red_to_respond', records = records)
    r.invalid_symptom_to_respond(key="invalid", errcode = 'invalid_red_symptom_to_respond', column_prefix = "red_symptom", symptoms = r.red_symptoms, records = records)
    return r


def bir_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    r.field_missing(position = 2, key = 'child_number', errcode = "missing_child_number")
    r.misformat_numberfield(position = 2, key = 'child_number', errcode = "invalid_child_number")
    r.numberfield_not_between_minv_maxv(position = 2, key = 'child_number', errcode = "invalid_child_number", minv = 1, maxv = 6)
    r.field_missing(position = 3, key = 'birth_date', errcode = "missing_birth_date")
    r.misformat_datefield(position = 3, key = 'birth_date', errcode = "misformat_birth_date")
    r.datefield_greater_currentdate(position = 3, key = 'birth_date', errcode = "birth_date_greater_currentdate")
    r.datefield_lesser_lmp(position = 3, key = 'birth_date', errcode = "birth_date_lesser_lmp")
    r.bir_duplicated(position = 3, key = 'birth_date', errcode = "duplicate_birth")
    #GENDER, BREASTFEEDING, LOCATION TODO
    r.missing_gender(position = 4, key = 'child_weight', errcode = "missing_child_weight")
    r.invalid_gender(position = 4, key = 'child_weight', errcode = "invalid_child_weight")
    r.missing_current_symptoms(position = 5, key = 'current_symptoms', errcode = "missing_current_symptoms")
    r.invalid_current_symptom(position = 5, key = 'current_symptoms', errcode = "invalid_current_symptom")
    r.incoherent_np_symptom(position = 5, key = 'current_symptoms', errcode = "incoherent_np_symptom")
    r.duplicate_symptom(position = 5, key = 'current_symptoms', errcode = "duplicate_symptom")
    r.missing_location(position = 6, key = 'location', errcode = "missing_location")
    r.invalid_location(position = 6, key = 'location', errcode = "invalid_location")
    r.missing_breastfeeding(position = 7, key = 'breastfeeding', errcode = "missing_breastfeeding")
    r.invalid_breastfeeding(position = 7, key = 'breastfeeding', errcode = "invalid_breastfeeding")
    r.missing_child_weight(position = 8, key = 'child_weight', errcode = "missing_child_weight")
    r.invalid_child_weight(position = 8, key = 'child_weight', errcode = "invalid_child_weight")
    #CHECK PLZ TODO
    r.invalid_code()  
    r.missing_current_pregnancy()
    r.delivered_already( key = 'invalid', errcode = 'delivered_already')
    r.miscarriage_found()
    r.has_mother_death()
    return r

def chi_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    r.field_missing(position = 2, key = 'child_number', errcode = "missing_child_number")
    r.misformat_numberfield(position = 2, key = 'child_number', errcode = "invalid_child_number")
    r.numberfield_not_between_minv_maxv(position = 2, key = 'child_number', errcode = "invalid_child_number", minv = 1, maxv = 6)
    r.field_missing(position = 3, key = 'birth_date', errcode = "missing_birth_date")
    r.misformat_datefield(position = 3, key = 'birth_date', errcode = "misformat_birth_date")
    r.datefield_greater_currentdate(position = 3, key = 'birth_date', errcode = "birth_date_greater_currentdate")
    r.chi_duplicated(position = 3, key = 'birth_date', errcode = "duplicate_chi")
    r.missing_group_fields(position = 4, key = 'vaccine', errcode = "missing_vaccine")
    r.invalid_group_field(position = 4, key = 'vaccine', errcode = "invalid_vaccine" )
    r.duplicate_visit(position = 4, key = 'vaccine', errcode = "duplicate_vaccine_visit", visits = r.get_vaccine_visits() )
    r.invalid_sequence(position = 4, key = 'vaccine', errcode = "invalid_sequence", max_sequence = range(1,7), visits = r.get_vaccine_visits() )
    r.missing_group_fields(position = 5, key = 'vaccine_completion', errcode = "missing_vaccine_completion")
    r.invalid_group_field(position = 5, key = 'vaccine_completion', errcode = "invalid_vaccine_completion" )
    r.missing_current_symptoms(position = 6, key = 'current_symptoms', errcode = "missing_current_symptoms")
    r.invalid_current_symptom(position = 6, key = 'current_symptoms', errcode = "invalid_current_symptom")
    r.incoherent_jam_np_symptom(position = 6, key = 'current_symptoms', errcode = "incoherent_jam_np_symptom")
    r.duplicate_symptom(position = 6, key = 'current_symptoms', errcode = "duplicate_symptom")
    r.missing_location(position = 7, key = 'location', errcode = "missing_location")
    r.invalid_location(position = 7, key = 'location', errcode = "invalid_location")
    r.missing_child_weight(position = 8, key = 'child_weight', errcode = "missing_child_weight")
    r.invalid_child_weight(position = 8, key = 'child_weight', errcode = "invalid_child_weight")
    r.missing_muac(position = 9, key = 'muac', errcode = "missing_muac")
    r.invalid_muac(position = 9, key = 'muac', errcode = "invalid_muac")
    r.invalid_code()  
    r.missing_current_child()
    r.has_child_death()
    return r


def cbn_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    r.field_missing(position = 2, key = 'child_number', errcode = "missing_child_number")
    r.misformat_numberfield(position = 2, key = 'child_number', errcode = "invalid_child_number")
    r.numberfield_not_between_minv_maxv(position = 2, key = 'child_number', errcode = "invalid_child_number", minv = 1, maxv = 6)
    r.field_missing(position = 3, key = 'birth_date', errcode = "missing_birth_date")
    r.misformat_datefield(position = 3, key = 'birth_date', errcode = "misformat_birth_date")
    r.datefield_greater_currentdate(position = 3, key = 'birth_date', errcode = "birth_date_greater_currentdate")
    r.cbn_duplicated(position = 3, key = 'birth_date', errcode = "duplicate_chi")
    r.missing_breastfeeding(position = 4, key = 'breastfeeding', errcode = "missing_breastfeeding")
    r.invalid_breastfeeding(position = 4, key = 'breastfeeding', errcode = "invalid_breastfeeding")
    #r.missing_child_height(position = 5, key = 'child_height', errcode = "missing_child_height")
    #r.invalid_child_height(position = 5, key = 'child_height', errcode = "invalid_child_height")
    r.missing_child_weight(position = 6, key = 'child_weight', errcode = "missing_child_weight")
    r.invalid_child_weight(position = 6, key = 'child_weight', errcode = "invalid_child_weight")
    r.missing_muac(position = 7, key = 'muac', errcode = "missing_muac")
    r.invalid_muac(position = 7, key = 'muac', errcode = "invalid_muac")
    r.missing_current_child()
    r.has_child_death()
    return r

def ccm_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    r.field_missing(position = 2, key = 'child_number', errcode = "missing_child_number")
    r.misformat_numberfield(position = 2, key = 'child_number', errcode = "invalid_child_number")
    r.numberfield_not_between_minv_maxv(position = 2, key = 'child_number', errcode = "invalid_child_number", minv = 1, maxv = 6)
    r.field_missing(position = 3, key = 'birth_date', errcode = "missing_birth_date")
    r.misformat_datefield(position = 3, key = 'birth_date', errcode = "misformat_birth_date")
    r.datefield_greater_currentdate(position = 3, key = 'birth_date', errcode = "birth_date_greater_currentdate")
    #r.ccm_duplicated(position = 3, key = 'birth_date', errcode = "duplicate_ccm")
    r.missing_current_symptoms(position = 4, key = 'current_symptoms', errcode = "missing_current_symptoms")
    r.invalid_current_symptom(position = 4, key = 'current_symptoms', errcode = "invalid_current_symptom")
    r.incoherent_jam_np_symptom(position = 4, key = 'current_symptoms', errcode = "incoherent_jam_np_symptom")
    r.duplicate_symptom(position = 4, key = 'current_symptoms', errcode = "duplicate_symptom")
    r.missing_intervention(position = 5, key = 'intervention', errcode = "missing_intervention")
    r.invalid_intervention(position = 5, key = 'intervention', errcode = "invalid_intervention")
    r.missing_muac(position = 6, key = 'muac', errcode = "missing_muac")
    r.invalid_muac(position = 6, key = 'muac', errcode = "invalid_muac")
    r.invalid_code()
    r.unresponded_record( key="invalid", errcode = 'unresponded_report', records = r.get_unresponded_ccm_records())
    r.missing_current_child()
    r.has_child_death()
    return r

def cmr_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    ##PLEASE RESPOND BEFORE ANY NEW FOR THIS MOTHER CHILD
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    r.field_missing(position = 2, key = 'child_number', errcode = "missing_child_number")
    r.misformat_numberfield(position = 2, key = 'child_number', errcode = "invalid_child_number")
    r.numberfield_not_between_minv_maxv(position = 2, key = 'child_number', errcode = "invalid_child_number", minv = 1, maxv = 6)
    r.field_missing(position = 3, key = 'birth_date', errcode = "missing_birth_date")
    r.misformat_datefield(position = 3, key = 'birth_date', errcode = "misformat_birth_date")
    r.datefield_greater_currentdate(position = 3, key = 'birth_date', errcode = "birth_date_greater_currentdate")
    #r.ccm_duplicated(position = 3, key = 'birth_date', errcode = "duplicate_ccm")
    r.missing_current_symptoms(position = 4, key = 'current_symptoms', errcode = "missing_current_symptoms")
    r.invalid_current_symptom(position = 4, key = 'current_symptoms', errcode = "invalid_current_symptom")
    r.incoherent_jam_np_symptom(position = 4, key = 'current_symptoms', errcode = "incoherent_jam_np_symptom")
    r.duplicate_symptom(position = 4, key = 'current_symptoms', errcode = "duplicate_symptom")
    r.missing_intervention(position = 5, key = 'intervention', errcode = "missing_intervention")
    r.invalid_intervention(position = 5, key = 'intervention', errcode = "invalid_intervention")
    r.missing_child_status(position = 6, key = 'child_status', errcode = "missing_child_status")
    r.invalid_child_status(position = 6, key = 'child_status', errcode = "invalid_child_status")
    r.invalid_code()
    r.missing_to_respond_record(key="invalid", errcode = 'ccm_to_respond', records = r.get_unresponded_ccm_records())
    r.invalid_symptom_to_respond(key="invalid", errcode = 'invalid_ccm_symptom_to_respond',
                                 column_prefix = "symptom", symptoms = r.current_symptoms, records = r.get_unresponded_ccm_records())
    r.missing_current_child()
    r.has_child_death()
    
    return r


def pnc_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    r.missing_group_fields(position = 2, key = 'pnc_visit', errcode = "missing_pnc_visit")
    r.invalid_group_field(position = 2, key = 'pnc_visit', errcode = "invalid_pnc_visit" )
    r.acknowledge_previous_visit(position = 3, key = 'pnc1', errcode = "previous_ack_missing")
    r.field_missing(position = 4, key = 'birth_date', errcode = "missing_birth_date")
    r.misformat_datefield(position = 4, key = 'birth_date', errcode = "misformat_birth_date")
    r.datefield_greater_currentdate(position = 4, key = 'birth_date', errcode = "birth_date_greater_currentdate")
    r.missing_current_symptoms(position = 5, key = 'current_symptoms', errcode = "missing_current_symptoms")
    r.invalid_current_symptom(position = 5, key = 'current_symptoms', errcode = "invalid_current_symptom")
    r.incoherent_jam_np_symptom(position = 5, key = 'current_symptoms', errcode = "incoherent_jam_np_symptom")
    r.duplicate_symptom(position = 5, key = 'current_symptoms', errcode = "duplicate_symptom")
    r.duplicate_visit(position = 2, key = 'pnc_visit', errcode = "duplicate_pnc_visit", visits = r.get_pnc_visits() )
    r.invalid_sequence(position = 2, key = 'pnc_visit', errcode = "invalid_sequence", max_sequence = range(2,6), visits = r.get_pnc_visits() )
    r.missing_intervention(position = 6, key = 'intervention', errcode = "missing_intervention")
    r.invalid_intervention(position = 6, key = 'intervention', errcode = "invalid_intervention")
    r.missing_mother_status(position = 7, key = 'mother_status', errcode = "missing_mother_status")
    r.invalid_mother_status(position = 7, key = 'mother_status', errcode = "invalid_mother_status")
    r.missing_current_child()
    r.has_mother_death()
    return r



def nbc_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    r.field_missing(position = 2, key = 'child_number', errcode = "missing_child_number")
    r.misformat_numberfield(position = 2, key = 'child_number', errcode = "invalid_child_number")
    r.numberfield_not_between_minv_maxv(position = 2, key = 'child_number', errcode = "invalid_child_number", minv = 1, maxv = 6)
    r.missing_group_fields(position = 3, key = 'nbc_visit', errcode = "missing_nbc_visit")
    r.invalid_group_field(position = 3, key = 'nbc_visit', errcode = "invalid_nbc_visit" )
    r.acknowledge_previous_visit(position = 4, key = 'nbc1', errcode = "previous_ack_missing")
    r.field_missing(position = 5, key = 'birth_date', errcode = "missing_birth_date")
    r.misformat_datefield(position = 5, key = 'birth_date', errcode = "misformat_birth_date")
    r.datefield_greater_currentdate(position = 5, key = 'birth_date', errcode = "birth_date_greater_currentdate")
    r.acknowledge_previous_visit(position = 6, key = 'v2', errcode = "previous_ack_missing")
    r.missing_current_symptoms(position = 7, key = 'current_symptoms', errcode = "missing_current_symptoms")
    r.invalid_current_symptom(position = 7, key = 'current_symptoms', errcode = "invalid_current_symptom")
    r.incoherent_jam_np_symptom(position = 7, key = 'current_symptoms', errcode = "incoherent_jam_np_symptom")
    r.duplicate_symptom(position = 7, key = 'current_symptoms', errcode = "duplicate_symptom")
    r.duplicate_visit(position = 3, key = 'nbc_visit', errcode = "duplicate_nbc_visit", visits = r.get_nbc_visits() )
    r.invalid_sequence(position = 3, key = 'nbc_visit', errcode = "invalid_sequence", max_sequence = range(2,6), visits = r.get_nbc_visits() )
    r.missing_breastfeeding(position = 8, key = 'breastfeeding', errcode = "missing_breastfeeding")
    r.invalid_breastfeeding(position = 8, key = 'breastfeeding', errcode = "invalid_breastfeeding")
    r.missing_intervention(position = 9, key = 'intervention', errcode = "missing_intervention")
    r.invalid_intervention(position = 9, key = 'intervention', errcode = "invalid_intervention")
    r.missing_child_status(position = 10, key = 'child_status', errcode = "missing_child_status")
    r.invalid_child_status(position = 10, key = 'child_status', errcode = "invalid_child_status")
    #r.datefield_mismatch(position = 3, key = 'birth_date', errcode = "birth_date_mismatch", records = records, match_key = 'birth_date')
    #r.outrange_dated_field(position = 3, key = 'nbc_visit', errcode = "outrange_nbc_visit", delta_comp = r.birth_date, delta = 60)
    r.missing_current_child()
    r.has_child_death()
    return r


def dth_checker(r = None):
    r.invalid_reporter(key = 'invalid', errcode = 'invalid_reporter')
    r.patient_nid_missing()
    r.invalid_nid()
    r.nid_not_16digits()
    r.phone_mismatch()
    r.misformat_dated_nid()
    r.outrange_dated_nid()
    if r.valid_number_field(position = 2 ) or r.valid_date_field(position = 2 ) or r.valid_date_field(position = 3):
        r.field_missing(position = 2, key = 'child_number', errcode = "missing_child_number")
        r.misformat_numberfield(position = 2, key = 'child_number', errcode = "invalid_child_number")
        r.numberfield_not_between_minv_maxv(position = 2, key = 'child_number', errcode = "invalid_child_number", minv = 1, maxv = 6)
        r.field_missing(position = 3, key = 'birth_date', errcode = "missing_birth_date")
        r.misformat_datefield(position = 3, key = 'birth_date', errcode = "misformat_birth_date")
        r.datefield_greater_currentdate(position = 3, key = 'birth_date', errcode = "birth_date_greater_currentdate")
        r.missing_group_fields(position = 5, key = 'death', errcode = "missing_death")
        r.invalid_group_field(position = 5, key = 'death', errcode = "invalid_death" )
        if hasattr(r, 'death') and getattr(r, 'death')[0].lower() == 'nd':
            r.outrange_dated_field(position = 3, key = 'death', errcode = "outrange_nd_death", delta_comp = r.birth_date, delta = 28)
        if hasattr(r, 'death') and getattr(r, 'death')[0].lower() == 'cd':
            r.outrange_dated_field(position = 3, key = 'death', errcode = "outrange_md_death", delta_comp = r.birth_date, delta = 60)
        r.missing_current_child()
        r.has_child_death()
    else:
        r.missing_group_fields(position = 5, key = 'death', errcode = "missing_death")
        r.invalid_group_field(position = 5, key = 'death', errcode = "invalid_death" )
        if hasattr(r, 'death') and getattr(r, 'death')[0].lower() == 'md':
            pass#r.outrange_dated_field(position = 3, key = 'death', errcode = "outrange_md_death", delta_comp = r.birth_date, delta = 60)
        r.missing_current_pregnancy()
        r.has_mother_death()
        #pass

    r.missing_location(position = 4, key = 'location', errcode = "missing_location")
    r.invalid_location(position = 4, key = 'location', errcode = "invalid_location")

    return r
