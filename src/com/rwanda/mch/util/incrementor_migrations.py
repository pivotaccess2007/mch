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

import time
import threading
import datetime
from util.record import *
from util.mch_security import MchSecurity
from util.mch_util import write, load

""" TEST """
"""

QRY1 = "SELECT * FROM chws_nation"
QRY2 = "SELECT * FROM nation"

ans1 = fetch_data(MCONN1, QRY1)
ans2 = fetch_data(PCONN, QRY2)
code = 'RW'
ans3 = orm.ORM.query('nation', {'code = %s': code})

for an1 in ans1:
 print an1.__dict__

for an2 in ans2:
 print an2.__dict__

ans3.list()

"""
""" END OF TEST """


PRE_FILE     = "pregnancy.json"
BIR_FILE     = "birth.json"
REF_FILE     = "refusal.json"
DEP_FILE     = "departure.json"
ANC_FILE     = "ancvisit.json"
RISK_FILE    = "risk.json"
RED_FILE     = "redalert.json"
RES_FILE    = "riskresult.json"
RAR_FILE     = "redresult.json"
DTH_FILE    = "death.json"
NBC_FILE    = "nbcvisit.json"
PNC_FILE    = "pncvisit.json"
CHI_FILE    = "childhealth.json"
CBN_FILE    = "nutrition.json"
CCM_FILE    = "ccm.json"
CMR_FILE    = "cmr.json"

def migrate(table, fields):
  try:
    orm.ORM.postgres.rollback()
    p = orm.ORM.store(table, fields)
    orm.ORM.postgres.commit()
    return True
  except Exception, e:
    print e
    orm.ORM.postgres.rollback()
    orm.ORM.postgres.commit()
  return False

def migrate_nations():
  QRY = "SELECT * FROM chws_nation WHERE name = 'Rwanda';"
  ans = fetch_data(MCONN1, QRY)
  for an in ans:
    code = 'RW'
    name = an.name
    nation = fetch_nation(code)
    indexcol = None
    if nation:  indexcol = nation.indexcol
    latitude = -1.9499500 
    longitude = 30.0588500
    orm.ORM.store('nation', {'indexcol': indexcol, 'code': code, 'name': name, 'latitude': latitude, 'longitude': longitude} )
  return True

def migrate_provinces():
  QRY = "SELECT * FROM chws_province WHERE name != 'TEST';"
  ans = fetch_data(MCONN1, QRY)
  for an in ans:
    code = an.code
    name = an.name
    nation = fetch_nation('RW')
    province = fetch_province(code)
    indexcol = None
    if province: indexcol = province.indexcol
    latitude = None
    longitude = None
    #print {'code': code, 'name': name, 'nation_pk': nation.indexcol, 'latitude': latitude, 'longitude': longitude}
    orm.ORM.store('province', {'indexcol': indexcol, 'code': code, 'name': name,
                               'nation_pk': nation.indexcol, 'latitude': latitude, 'longitude': longitude} )
  return True

def migrate_districts():
  QRY = """SELECT *, (SELECT code FROM chws_province WHERE  chws_province.id=chws_district.province_id) AS province_code 
          FROM chws_district WHERE name != 'TEST' ORDER BY code ASC;"""
  ans = fetch_data(MCONN1, QRY)
  for an in ans:
    code = an.code
    name = an.name
    province = fetch_province(an.province_code)
    district = fetch_district(code)
    indexcol = None
    if district: indexcol = district.indexcol
    latitude = None
    longitude = None
    """print {'code': code, 'name': name,
            'nation_pk': province.nation_pk,
            'province_pk': province.indexcol,
            'latitude': latitude, 'longitude': longitude}"""
    orm.ORM.store('district', {'indexcol': indexcol, 'code': code, 'name': name,
                                'nation_pk': province.nation_pk,
                                'province_pk': province.indexcol, 
                                'latitude': latitude, 'longitude': longitude} )
  return True


def migrate_sectors():
  QRY = """SELECT *, (SELECT code FROM chws_district WHERE  chws_district.id=chws_sector.district_id) AS district_code 
          FROM chws_sector WHERE name != 'TEST' ORDER BY code ASC;"""
  ans = fetch_data(MCONN1, QRY)
  for an in ans:
    code = an.code
    name = an.name
    district = fetch_district(an.district_code)
    sector = fetch_sector(code)
    indexcol = None
    if sector: indexcol = sector.indexcol
    latitude = None
    longitude = None
    """print {'code': code, 'name': name,
            'nation_pk': district.nation_pk,
            'province_pk': district.province_pk,
            'district_pk': district.indexcol,
            'latitude': latitude, 'longitude': longitude}"""
    orm.ORM.store('sector', {'indexcol': indexcol, 'code': code, 'name': name,
                                'nation_pk': district.nation_pk,
                                'province_pk': district.province_pk,
                                'district_pk': district.indexcol,
                                'latitude': latitude, 'longitude': longitude} )
  return True

def migrate_cells():
  QRY = """SELECT *, (SELECT code FROM chws_sector WHERE  chws_sector.id=chws_cell.sector_id) AS sector_code 
          FROM chws_cell WHERE name != 'TEST' ORDER BY code ASC;"""
  ans = fetch_data(MCONN1, QRY)
  for an in ans:
    code = an.code
    name = an.name
    sector = fetch_sector(an.sector_code)
    cell = fetch_cell(code)
    indexcol = None
    if cell: indexcol = cell.indexcol
    latitude = None
    longitude = None
    """print {'code': code, 'name': name,
            'nation_pk': sector.nation_pk,
            'province_pk': sector.province_pk,
	          'district_pk': sector.district_pk,
            'sector_pk': sector.indexcol,
            'latitude': latitude, 'longitude': longitude}"""
    orm.ORM.store('cell', {'indexcol': indexcol, 'code': code, 'name': name,
                                'nation_pk': sector.nation_pk,
			                          'province_pk': sector.province_pk,
			                          'district_pk': sector.district_pk,
			                          'sector_pk': sector.indexcol, 
                                'latitude': latitude, 'longitude': longitude} )
  return True

def migrate_villages():
  QRY = """SELECT *, (SELECT code FROM chws_cell WHERE  chws_cell.id=chws_village.cell_id) AS cell_code 
          FROM chws_village WHERE name != 'TEST' ORDER BY code ASC;"""
  ans = fetch_data(MCONN1, QRY)
  for an in ans:
    code = an.code
    name = an.name
    cell = fetch_cell(an.cell_code)
    village = fetch_village(code)
    indexcol = None
    if village: indexcol = village.indexcol
    latitude = None
    longitude = None
    """print {'code': code, 'name': name,
            'nation_pk': cell.nation_pk,
            'province_pk': cell.province_pk,
	          'district_pk': cell.district_pk,
            'sector_pk': cell.sector_pk,
            'cell_pk': cell.indexcol,
            'latitude': latitude, 'longitude': longitude}"""
    orm.ORM.store('village', {'indexcol': indexcol, 'code': code, 'name': name,
                                'nation_pk': cell.nation_pk,
                                'province_pk': cell.province_pk,
	                              'district_pk': cell.district_pk,
                                'sector_pk': cell.sector_pk,
                                'cell_pk': cell.indexcol, 
                                'latitude': latitude, 'longitude': longitude} )
  return True

def migrate_healthcentres():
  QRY = """SELECT DISTINCT (SELECT code FROM chws_healthcentre WHERE  chws_healthcentre.id=chws_reporter.health_centre_id) AS hc_code,
            (SELECT name FROM chws_healthcentre WHERE  chws_healthcentre.id=chws_reporter.health_centre_id) AS hc_name,
            (SELECT code FROM chws_hospital WHERE  chws_hospital.id=chws_reporter.referral_hospital_id) AS hp_code,
            (SELECT code FROM chws_district WHERE  chws_district.id=chws_reporter.district_id) AS dst_code,
            (SELECT code FROM chws_sector WHERE  chws_sector.id=chws_reporter.sector_id) AS sec_code,
            district_id
            FROM chws_reporter WHERE nation_id != 2 ORDER BY district_id ASC;"""
  ans = fetch_data(MCONN1, QRY)
  for an in ans:
    code = an.hc_code
    name = an.hc_name
    level = fetch_location_level("HC")
    district = fetch_district(an.dst_code)
    sector_pk = None
    sector = fetch_sector(an.sec_code)
    if sector:  sector_pk = sector.indexcol
    referral = fetch_facility(an.hp_code)
    facility = fetch_facility(code)
    indexcol = None
    if facility: indexcol = facility.indexcol
    latitude = None
    longitude = None
    """print {'code': code, 'name': name,
            'nation_pk': district.nation_pk,
            'province_pk': district.province_pk,
	          'district_pk': district.indexcol,
            'sector_pk': sector_pk,
            'referral_facility_pk': referral.indexcol, 
            'facility_type_pk': level.indexcol,
            'latitude': latitude, 'longitude': longitude}"""
    orm.ORM.store('facility', {'indexcol': indexcol, 'code': code, 'name': name,
                                'nation_pk': district.nation_pk,
                                'province_pk': district.province_pk,
	                              'district_pk': district.indexcol,
                                'sector_pk': sector_pk,
                                'referral_facility_pk': referral.indexcol,
                                'facility_type_pk': level.indexcol, 
                                'latitude': latitude, 'longitude': longitude} )
    
  return True

def migrate_hospitals():
  QRY = """ SELECT *, (SELECT code FROM chws_sector WHERE  chws_sector.id=chws_hospital.sector_id) AS sector_code,
                    (SELECT code FROM chws_district WHERE  chws_district.id=chws_hospital.district_id) AS district_code
                   FROM chws_hospital WHERE name != 'TEST' ORDER BY district_code, code ASC; """
  ans = fetch_data(MCONN1, QRY)
  for an in ans:
    code = an.code
    name = an.name
    level = fetch_location_level("HD")
    district = fetch_district(an.district_code)
    sector_pk = None
    sector = fetch_sector(an.sector_code)
    if sector:  sector_pk = sector.indexcol
    facility = fetch_facility(code)
    indexcol = None
    if facility: indexcol = facility.indexcol
    latitude = None
    longitude = None
    """print {'code': code, 'name': name,
            'nation_pk': district.nation_pk,
            'province_pk': district.province_pk,
	          'district_pk': district.indexcol,
            'sector_pk': sector_pk,
            'facility_type_pk': level.indexcol,
            'latitude': latitude, 'longitude': longitude}"""
    orm.ORM.store('facility', {'indexcol': indexcol, 'code': code, 'name': name,
                                'nation_pk': district.nation_pk,
                                'province_pk': district.province_pk,
	                              'district_pk': district.indexcol,
                                'sector_pk': sector_pk,
                                'facility_type_pk': level.indexcol, 
                                'latitude': latitude, 'longitude': longitude} )
  return True  


def migrate_simcards():
  QRY_CHWS = """ SELECT DISTINCT(telephone_moh) AS telephone FROM chws_reporter; """
  QRY_AMBS = """ SELECT DISTINCT(phonenumber) AS telephone FROM ambulances_ambulancedriver; """
  QRY_DTMS = """ SELECT DISTINCT(telephone_moh) AS telephone FROM chws_datamanager; """
  QRY_STFS = """ SELECT DISTINCT(telephone_moh) AS telephone FROM chws_facilitystaff; """
  QRY_HDIS = """ SELECT DISTINCT(telephone_moh) AS telephone FROM chws_hospitaldirector; """
  QRY_MNES = """ SELECT DISTINCT(telephone_moh) AS telephone FROM chws_monitorevaluator; """
  QRY_SUPS = """ SELECT DISTINCT(telephone_moh) AS telephone FROM chws_supervisor; """
  ans_chws = fetch_data(MCONN1, QRY_CHWS)
  ans_ambs = fetch_data(MCONN1, QRY_AMBS)
  ans_dtms = fetch_data(MCONN1, QRY_DTMS)
  ans_stfs = fetch_data(MCONN1, QRY_STFS)
  ans_hdis = fetch_data(MCONN1, QRY_HDIS)
  ans_mnes = fetch_data(MCONN1, QRY_MNES)
  ans_sups = fetch_data(MCONN1, QRY_SUPS)
  ans = ans_chws + ans_ambs + ans_dtms + ans_stfs + ans_hdis + ans_mnes + ans_sups
  ans.sort()
  for an_chw in ans:
    phone   =  an_chw.telephone              
    msin    = phone[len(phone)-7: ]
    mnc     = phone[len(phone)-9:len(phone)-7]
    mcc     = '250'
    spn     = ''
    if mnc == '78': spn     = 'MTN'
    if mnc == '73': spn     = 'AIRTEL'
    if mnc == '72': spn     = 'TIGO'      
    msisdn  = '+%(mcc)s%(mnc)s%(msin)s' % {'mcc': mcc, 'mnc': mnc, 'msin': msin}
    simcard = fetch_simcard(msisdn)
    indexcol = None
    if simcard: indexcol = simcard.indexcol
    #print  {'indexcol' : indexcol, 'phone': phone, 'mcc': mcc, 'mnc': mnc, 'msin': msin, 'msisdn': msisdn, 'spn': spn}
    if spn:
      if not simcard: orm.ORM.store('simcard', {'indexcol' : indexcol, 'mcc': mcc, 'mnc': mnc, 'msin': msin, 'msisdn': msisdn, 'spn': spn})

  return True

def migrate_reporters():
  QRY = """ SELECT telephone_moh AS telephone,
                        national_id AS nid,
                        surname,
                        given_name,
                        sex,
                        education_level,
                        date_of_birth,
                        join_date,
                        language,
                        last_seen,
                        is_active,
                        created,
                        updated,
                        correct_registration AS is_correct,
                        (SELECT code FROM chws_role WHERE  chws_role.id=chws_reporter.role_id) AS role_code,
                        (SELECT code FROM chws_healthcentre WHERE  chws_healthcentre.id=chws_reporter.health_centre_id) AS hc_code,
                        (SELECT name FROM chws_healthcentre WHERE  chws_healthcentre.id=chws_reporter.health_centre_id) AS hc_name,
                        (SELECT code FROM chws_hospital WHERE  chws_hospital.id=chws_reporter.referral_hospital_id) AS hp_code,
                        (SELECT code FROM chws_district WHERE  chws_district.id=chws_reporter.district_id) AS dst_code,
                        (SELECT code FROM chws_sector WHERE  chws_sector.id=chws_reporter.sector_id) AS sec_code,
                        (SELECT code FROM chws_cell WHERE  chws_cell.id=chws_reporter.cell_id) AS cel_code,
                        (SELECT code FROM chws_village WHERE  chws_village.id=chws_reporter.village_id) AS vil_code
                        FROM chws_reporter WHERE nation_id != 2 ORDER BY dst_code, cel_code, vil_code ASC ; """

  ans = fetch_data(MCONN1, QRY)
  simcard_pk = None
  for an in ans:
    created_at = an.created
    updated_at = an.updated
    simcard = fetch_simcard(an.telephone)
    if not (simcard and an.cel_code and an.vil_code and an.hc_code): continue
    simcard_pk = simcard.indexcol
    telephone = an.telephone
    national_id = an.nid
    surname = an.surname
    given_name = an.given_name
    date_of_birth = an.date_of_birth
    gender = fetch_gender(an.sex)
    sex_pk = gender.indexcol
    education_level = fetch_education_level(an.education_level)
    education_level_pk = education_level.indexcol
    language = fetch_language(an.language.upper())
    language_pk = language.indexcol
    join_date = an.join_date
    email = 'user%d@mch.moh.gov.rw' % simcard_pk
    generated_password = MchSecurity.generatedPassword(simcard.msin)
    salt = generated_password[0]
    passwd = generated_password[1]
    role = fetch_role(an.role_code.upper())
    role_pk = role.indexcol
    location_level = fetch_location_level('VIL')
    location_level_pk = location_level.indexcol
    cell = fetch_cell(an.cel_code)
    nation_pk = cell.nation_pk
    province_pk = cell.province_pk
    district_pk = cell.district_pk
    facility = fetch_facility(an.hc_code)
    referral_facility_pk = facility.referral_facility_pk
    facility_pk = facility.indexcol
    sector_pk = cell.sector_pk
    cell_pk = cell.indexcol
    village = fetch_village(an.vil_code)    
    village_pk = village.indexcol
    last_seen = an.last_seen
    is_active = bool(an.is_active)
    is_correct = bool(an.is_correct)
    enduser = fetch_enduser(national_id, telephone)
    indexcol = None
    if enduser: indexcol = enduser.indexcol

    """
    print {
            'created_at' 		: created_at,
            'updated_at' 		: updated_at,
            'simcard'		: simcard.__dict__,
            'simcard_pk' 		: simcard_pk,
            'telephone'  		: telephone,
            'national_id'		: national_id,
            'surname'    		: surname,
            'given_name' 		: given_name,
            'date_of_birth'		: date_of_birth,
            'gender'		: gender.__dict__,
            'sex_pk'          	: sex_pk,
            'education_level'	: education_level.__dict__,
            'education_level_pk'	: education_level_pk,
            'language'       	: language.__dict__,
            'language_pk'       	: language_pk,
            'join_date'      	: join_date,
            'email' 		: email,
            'salt' 			: salt,
            'passwd'		: passwd,
            'role'			: role.__dict__,
            'role_pk'        	: role_pk,
            'location_level'	: location_level.__dict__,
            'location_level_pk'	: location_level_pk,
            'cell'			: cell.__dict__,
            'nation_pk'        	: nation_pk,
            'province_pk'         	: province_pk,
            'district_pk'      	: district_pk,
            'facility'		: facility.__dict__,
            'referral_facility_pk'	: referral_facility_pk,
            'facility_pk'         	: facility_pk,
            'sector_pk'           	: sector_pk,
            'cell_pk'         	: cell_pk,
            'village'		: village.__dict__,    
            'village_pk'          	: village_pk,
            'last_seen'           	: last_seen,
            'is_active'           	: is_active,
            'is_correct'		: is_correct
    }"""


    orm.ORM.store('enduser', {
                                'indexcol': indexcol,
                                'created_at' 		: created_at,
                                'updated_at' 		: updated_at,
                                'simcard_pk' 		: simcard_pk,
                                'telephone'  		: telephone,
                                'national_id'		: national_id,
                                'surname'    		: surname,
                                'given_name' 		: given_name,
                                'date_of_birth'		: date_of_birth,
                                'sex_pk'          	: sex_pk,
                                'education_level_pk'	: education_level_pk,
                                'language_pk'       	: language_pk,
                                'join_date'      	: join_date,
                                'email' 		: email,
                                'salt' 			: salt,
                                'passwd'		: passwd,
                                'role_pk'        	: role_pk,
                                'location_level_pk'	: location_level_pk,
                                'nation_pk'        	: nation_pk,
                                'province_pk'         	: province_pk,
                                'district_pk'      	: district_pk,
                                'referral_facility_pk'	: referral_facility_pk,
                                'facility_pk'         	: facility_pk,
                                'sector_pk'           	: sector_pk,
                                'cell_pk'         	: cell_pk,
                                'village_pk'          	: village_pk,
                                'last_seen'           	: last_seen,
                                'is_active'           	: is_active,
                                'is_correct'		: is_correct
                              }
                  )

  

  return True


def migrate_ambulances():
  QRY_AMBS = """ SELECT DISTINCT(phonenumber) AS telephone FROM ambulances_ambulancedriver; """
  return True

def migrate_datamanagers():
  QRY_DTMS = """ SELECT DISTINCT(telephone_moh) AS telephone FROM chws_datamanager; """
  return True

def migrate_facilitystaffs():
  QRY_STFS = """ SELECT DISTINCT(telephone_moh) AS telephone FROM chws_facilitystaff; """
  return True

def migrate_hospitaldirectors():
  QRY_HDIS = """ SELECT DISTINCT(telephone_moh) AS telephone FROM chws_hospitaldirector; """
  return True

def migrate_monitorevaluators():
  QRY_MNES = """ SELECT DISTINCT(telephone_moh) AS telephone FROM chws_monitorevaluator; """
  return True

def migrate_supervisors():
  QRY_SUPS = """ SELECT DISTINCT(telephone_moh) AS telephone FROM chws_supervisor; """
  return True


def migrate_mother(report, enduser):  
  if not report.national_id or len(report.national_id) != 16: return False
  created_at = enduser.created_at if enduser else report.created
  updated_at = report.created
  telephone = enduser.telephone
  national_id = report.national_id
  user_phone = enduser.telephone
  user_pk = enduser.indexcol
  nation_pk = enduser.nation_pk
  province_pk = enduser.province_pk
  district_pk = enduser.district_pk
  referral_facility_pk = enduser.referral_facility_pk
  facility_pk = enduser.facility_pk
  sector_pk = enduser.sector_pk
  cell_pk = enduser.cell_pk
  village_pk = enduser.village_pk
  indexcol = None
  mother = fetch_mother( report.national_id)
  if mother:  indexcol = mother.indexcol 
  
  FLDS = {
                              'indexcol' : indexcol,
                              'created_at' : created_at,
                              'updated_at' : updated_at,
                              'telephone' : telephone,
                              'national_id' : national_id,
                              'user_phone' : user_phone,
                              'user_pk' : user_pk,
                              'nation_pk' : nation_pk,
                              'province_pk' : province_pk,
                              'district_pk' : district_pk,
                              'referral_facility_pk' : referral_facility_pk,
                              'facility_pk' : facility_pk,
                              'sector_pk' : sector_pk,
                              'cell_pk' : cell_pk,
                              'village_pk' : village_pk
                            }

  ## In case we have the mother never put the primary key in the fields
  if indexcol: FLDS.pop('national_id')
  migrate(table = 'mother', fields = FLDS)    
 
  return True

def migrate_child():
  QRY = ""
  return True

def process_field_value(temp, max_value, min_value, default):
  value = default
  if temp <= max_value or temp >= min_value: value = temp
  else:
    if temp > max_value: temp = str(temp)[0:len(str(max_value))-1]
    else: value = default
  return value

def only_values_of_dict(ans):
  vs = []
  for k in ans.keys():
    v = ans.get(k)
    if v: vs.append(v)
  return ' '.join(x for x in vs)

def filters_of_dict_keys(ans):
  vs = {}
  for k in ans.keys():
    v = ans.get(k)
    if v: vs.update({'%s IS NOT NULL' % k : ''})
  return vs


def migrate_field(report, key, max_value, min_value, default):
  
  QRY = """
                    SELECT
                        ubuzima_fieldtype.key,
                        ubuzima_field.value
                    FROM
                        ubuzima_field
                    INNER JOIN
                        ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = '%(key)s') 
                    WHERE
                        report_id = %(repid)d 
               """ 
  if key == 'location':
    key = default
    default = key[len(key) - 1]
    QRY = """
                    SELECT
                        ubuzima_fieldtype.key,
                        ubuzima_field.value
                    FROM
                        ubuzima_field
                    INNER JOIN
                        ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key IN %(key)s ) 
                    WHERE
                        report_id = %(repid)d 
               """
  
  ans = fetch_data(MCONN1, QRY % {'key': key, 'repid': report.id})
  value = default
  for an in ans:
    value = an.key
    if an.value:
      value = float(process_field_value(an.value, max_value, min_value, default))
    if an.value == 0.0: value = 0.0
  
  return value

def migrate_pregnancy(an):
  errors = []
  PRE = load(PRE_FILE)
  PRE_DATA = set(PRE.get("PRE"))
  try:
    indexcol = None
    enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
    if not enduser:
      #print "NO USER"
      errors.append("CHW: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh })
      PRE_DATA.add(an.id)

    migrate_mother(an, enduser)
    mother = fetch_mother(an.national_id)
    
    if not mother:
      #print "No MOther"
      errors.append("Mother: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh})
      PRE_DATA.add(an.id)

    #print enduser.__dict__
    #print an.__dict__
    #print mother.__dict__
    
    pregnancy = fetch_pregnancy(mother.national_id, an.date)
    if pregnancy:
      #print "DUPLICATION"
      errors.append("Mother: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh})
      PRE_DATA.add(an.id)
      indexcol = pregnancy.indexcol

    created_at = an.created
    updated_at = an.created
    user_phone = enduser.telephone
    user_pk = enduser.indexcol
    national_id = mother.national_id
    mother_pk = mother.indexcol
    nation_pk = enduser.nation_pk
    province_pk = enduser.province_pk
    district_pk = enduser.district_pk
    referral_facility_pk = enduser.referral_facility_pk
    facility_pk = enduser.facility_pk
    sector_pk = enduser.sector_pk
    cell_pk = enduser.cell_pk
    village_pk = enduser.village_pk

    lmp = an.date
    if not lmp:
      #print "No LMP"
      errors.append("LMP: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh })
      PRE_DATA.add(an.id)

    anc2_date = an.edd_anc2_date
    gravidity = int(an.gravidity) if an.gravidity else 0 #int(migrate_field(an, 'gravity', 30, 1, 1))
    parity = int(an.parity) if an.parity else 0 #int(migrate_field(an, 'parity', gravidity - 1, 0, 0))

    prev_pregnancy_gs = 'gs' if an.prev_pregnancy_gs else None #migrate_field(an, 'gs', None, None, None)
    prev_pregnancy_hd = 'hd' if an.prev_pregnancy_hd else None  #migrate_field(an, 'hd', None, None, None)
    prev_pregnancy_kx = 'kx' if an.prev_pregnancy_kx else None  #migrate_field(an, 'kx', None, None, None)
    prev_pregnancy_lz = 'lz' if an.prev_pregnancy_lz else None  #migrate_field(an, 'lz', None, None, None)
    prev_pregnancy_mu = 'mu' if an.prev_pregnancy_mu else None  #migrate_field(an, 'mu', None, None, None)
    prev_pregnancy_nr = 'nr' if an.prev_pregnancy_nr else None  #migrate_field(an, 'nr', None, None, 'nr')
    prev_pregnancy_ol = 'ol' if an.prev_pregnancy_ol else None  #migrate_field(an, 'ol', None, None, None)
    prev_pregnancy_rm = 'rm' if an.prev_pregnancy_rm else None  #migrate_field(an, 'rm', None, None, None)
    prev_pregnancy_yg = 'yg' if an.prev_pregnancy_yg else None  #migrate_field(an, 'yg', None, None, None)
    prev_pregnancy_yj = 'yj' if an.prev_pregnancy_yj else None  #migrate_field(an, 'yj', None, None, None)  

    prev_pregnancy_nr = None if ( prev_pregnancy_gs or prev_pregnancy_hd or prev_pregnancy_kx or 
       prev_pregnancy_lz or prev_pregnancy_mu or prev_pregnancy_ol or  
       prev_pregnancy_rm or prev_pregnancy_yg or prev_pregnancy_yj ) else 'nr' 

    symptom_af = 'af' if an.symptom_af  else None #migrate_field(an, 'af', None, None, None)
    symptom_ch = 'ch' if an.symptom_ch  else None #migrate_field(an, 'ch', None, None, None)
    symptom_di = 'di' if an.symptom_di  else None #migrate_field(an, 'di', None, None, None)
    symptom_ds = 'ds' if an.symptom_ds  else None #migrate_field(an, 'ds', None, None, None)
    symptom_fe = 'fe' if an.symptom_fe  else None #migrate_field(an, 'fe', None, None, None)
    symptom_fp = 'fp' if an.symptom_fp  else None #migrate_field(an, 'fp', None, None, None)
    symptom_hy = 'hy' if an.symptom_hy  else None #migrate_field(an, 'hy', None, None, None)
    symptom_ja = 'ja' if an.symptom_ja  else None #migrate_field(an, 'ja', None, None, None)
    symptom_ma = 'ma' if an.symptom_ma  else None #migrate_field(an, 'ma', None, None, None)
    symptom_np = 'np' if an.symptom_np  else None #migrate_field(an, 'np', None, None, None)
    symptom_ns = 'ns' if an.symptom_ns  else None #migrate_field(an, 'ns', None, None, None)
    symptom_oe = 'oe' if an.symptom_oe  else None #migrate_field(an, 'oe', None, None, None)
    symptom_pc = 'pc' if an.symptom_pc  else None #migrate_field(an, 'pc', None, None, None)
    symptom_sa = 'sa' if an.symptom_sa  else None #migrate_field(an, 'sa', None, None, None)
    symptom_rb = 'rb' if an.symptom_rb  else None #migrate_field(an, 'rb', None, None, None)
    symptom_vo = 'vo' if an.symptom_vo  else None #migrate_field(an, 'vo', None, None, None) 

    symptom_np = None if (symptom_af or symptom_ch or symptom_di or symptom_ds or 
        symptom_fe or symptom_fp or symptom_hy or symptom_ja or 
        symptom_ma or symptom_ns or symptom_oe or symptom_pc or 
        symptom_sa or symptom_rb or symptom_vo) else 'np'

    location = 'hp' if an.hp else 'hc' #migrate_field(an, 'location', None, None, ('hp', 'hc'))
    mother_weight = float(an.mother_weight) if an.mother_weight else 55 #migrate_field(an, 'mother_weight', 150, 35, 55)
    mother_height = float(an.mother_height) if an.mother_height else 150 #migrate_field(an, 'mother_height', 250, 50, 150)

    toilet = 'to' if an.toilet else 'nt' #migrate_field(an, 'to', '', '', 'nt')
    handwash = 'hw' if an.hw else 'nh' #migrate_field(an, 'hw', '', '', 'nh')    

    bmi = None
    if mother_weight and mother_height: 
      bmi = mother_weight / ((mother_height* mother_height) / 10000.0)

    muac = None

    prev_symptom = {
        'prev_pregnancy_gs' : prev_pregnancy_gs,
        'prev_pregnancy_hd' : prev_pregnancy_hd,
        'prev_pregnancy_kx' : prev_pregnancy_kx,
        'prev_pregnancy_lz' : prev_pregnancy_lz,
        'prev_pregnancy_mu' : prev_pregnancy_mu,
        'prev_pregnancy_nr' : prev_pregnancy_nr,
        'prev_pregnancy_ol' : prev_pregnancy_ol,
        'prev_pregnancy_rm' : prev_pregnancy_rm,
        'prev_pregnancy_yg' : prev_pregnancy_yg,
        'prev_pregnancy_yj' : prev_pregnancy_yj 
    }

    curr_symptom = {
        'symptom_af' : symptom_af,
        'symptom_ch' : symptom_ch,
        'symptom_di' : symptom_di,
        'symptom_ds' : symptom_ds,
        'symptom_fe' : symptom_fe,
        'symptom_fp' : symptom_fp,
        'symptom_hy' : symptom_hy,
        'symptom_ja' : symptom_ja,
        'symptom_ma' : symptom_ma,
        'symptom_np' : symptom_np,
        'symptom_ns' : symptom_ns,
        'symptom_oe' : symptom_oe,
        'symptom_pc' : symptom_pc,
        'symptom_sa' : symptom_sa,
        'symptom_rb' : symptom_rb,
        'symptom_vo' : symptom_vo
    }
    #print prev_symptom, curr_symptom
    TEXT = "%(keyword)s %(national_id)s %(lmp)s %(anc2_date)s %(gravidity)02d %(parity)02d %(prev_symptom)s %(curr_symptom)s %(location)s WT%(mother_weight)s HT%(mother_height)s %(toilet)s %(handwash)s" % {'keyword': 'PRE', 'national_id':national_id,
                                                               'lmp': "%02d.%02d.%04d" % (lmp.day, lmp.month, lmp.year),
                                                               'anc2_date': "%02d.%02d.%04d" % (anc2_date.day, anc2_date.month, anc2_date.year),
                                                               'gravidity': gravidity, 'parity': parity,
                                                               'prev_symptom' : only_values_of_dict(prev_symptom),
                                                               'curr_symptom': only_values_of_dict(curr_symptom),
                                                           'location': location, 'mother_weight': mother_weight, 'mother_height': mother_height,
                                                           'toilet' : toilet, 'handwash' : handwash  
                                                               }
    message = TEXT
    is_valid = True

    FLDS =  {
      'indexcol' : indexcol,
      'created_at' : created_at,
      'updated_at' : updated_at,
      'national_id' : national_id,
      'mother_pk' : mother_pk,
      'user_phone' : user_phone,
      'user_pk' : user_pk,
      'nation_pk' : nation_pk,
      'province_pk' : province_pk,
      'district_pk' : district_pk,
      'referral_facility_pk' : referral_facility_pk,
      'facility_pk' : facility_pk,
      'sector_pk' : sector_pk,
      'cell_pk' : cell_pk,
      'village_pk' : village_pk,

      'lmp' : lmp,
      'anc2_date' : anc2_date,
      'gravidity' : gravidity,
      'parity' : parity,

      'prev_pregnancy_gs' : prev_pregnancy_gs,
      'prev_pregnancy_hd' : prev_pregnancy_hd,
      'prev_pregnancy_kx' : prev_pregnancy_kx,
      'prev_pregnancy_lz' : prev_pregnancy_lz,
      'prev_pregnancy_mu' : prev_pregnancy_mu,
      'prev_pregnancy_nr' : prev_pregnancy_nr,
      'prev_pregnancy_ol' : prev_pregnancy_ol,
      'prev_pregnancy_rm' : prev_pregnancy_rm,
      'prev_pregnancy_yg' : prev_pregnancy_yg,
      'prev_pregnancy_yj' : prev_pregnancy_yj,    

      'symptom_af' : symptom_af,
      'symptom_ch' : symptom_ch,
      'symptom_di' : symptom_di,
      'symptom_ds' : symptom_ds,
      'symptom_fe' : symptom_fe,
      'symptom_fp' : symptom_fp,
      'symptom_hy' : symptom_hy,
      'symptom_ja' : symptom_ja,
      'symptom_ma' : symptom_ma,
      'symptom_np' : symptom_np,
      'symptom_ns' : symptom_ns,
      'symptom_oe' : symptom_oe,
      'symptom_pc' : symptom_pc,
      'symptom_sa' : symptom_sa,
      'symptom_rb' : symptom_rb,
      'symptom_vo' : symptom_vo,    

      'location' : location,
      'mother_weight' : mother_weight,
      'mother_height' : mother_height,

      'toilet' : toilet,
      'handwash' : handwash,    

      'bmi': bmi,
      'muac' : muac,
      'message' : message,
      'is_valid' : is_valid
    }

    #print FLDS
  
    #p = orm.ORM.store('pregnancy', FLDS)
    p = migrate(table='pregnancy', fields = FLDS)
    #print "NO: ", p, an.id, orm.ORM.cursor().closed, orm.ORM.connection().closed
    
  except Exception, e:
    PRE_DATA.add(an.id)
    print e

  PRE['PRE'] = list(PRE_DATA)
  #write(PRE, PRE_FILE)

  return True

def migrate_pregnancies():
  RP_ID = INC_ID; TYPE_ID = 10
  QRY = """
            SELECT
		          ubuzima_report.id,
                          (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                          (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                          (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                          ubuzima_report.date,
                          ubuzima_report.edd_anc2_date,
                          ubuzima_report.created,
		          (SELECT ubuzima_field.value FROM ubuzima_field 
		          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'gravity')
		          WHERE ubuzima_field.report_id = ubuzima_report.id) AS gravidity,
		          (SELECT ubuzima_field.value FROM ubuzima_field 
		          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'parity')
		          WHERE ubuzima_field.report_id = ubuzima_report.id) AS parity,
		          (SELECT ubuzima_field.value FROM ubuzima_field 
		          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'mother_weight')
		          WHERE ubuzima_field.report_id = ubuzima_report.id) AS mother_weight,
		          (SELECT ubuzima_field.value FROM ubuzima_field 
		          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'mother_height')
		          WHERE ubuzima_field.report_id = ubuzima_report.id) AS mother_height,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'gs')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS prev_pregnancy_gs,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hd')
						          WHERE ubuzima_field.report_id = ubuzima_report.id) AS prev_pregnancy_hd,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'kx')
						          WHERE ubuzima_field.report_id = ubuzima_report.id) AS prev_pregnancy_kx,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'lz')
						          WHERE ubuzima_field.report_id = ubuzima_report.id) AS prev_pregnancy_lz,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'mu')
						          WHERE ubuzima_field.report_id = ubuzima_report.id) AS prev_pregnancy_mu,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nr')
						          WHERE ubuzima_field.report_id = ubuzima_report.id) AS prev_pregnancy_nr,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ol')
						          WHERE ubuzima_field.report_id = ubuzima_report.id) AS prev_pregnancy_ol,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'rm')
						          WHERE ubuzima_field.report_id = ubuzima_report.id) AS prev_pregnancy_rm,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'yg')
						          WHERE ubuzima_field.report_id = ubuzima_report.id) AS prev_pregnancy_yg,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'yj')
						          WHERE ubuzima_field.report_id = ubuzima_report.id) AS prev_pregnancy_yj,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'af')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_af,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ch')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ch,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'di')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_di,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ds')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ds,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'fe')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_fe,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'fp')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_fp,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hy')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_hy,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ja')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ja,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ma')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ma,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'np')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_np,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ns')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ns,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'oe')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_oe,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pc')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_pc,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'rb')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_rb,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sa')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_sa,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'vo')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_vo,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hp')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS hp,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hc')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS hc,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cl')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS cl,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'to')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS toilet,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nt')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS no_toilet,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hw')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS hw,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nh')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS nh
                
            FROM 
                ubuzima_report
            INNER JOIN
                chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
            INNER JOIN
                ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
            WHERE
                ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
            ORDER BY
                (created)
            ASC
            
        """
  QRY = QRY % (TYPE_ID, RP_ID)
  ans = fetch_data(MCONN1, QRY)
  indexcol = None
  print "Try Moving %d Pregnancy" % len(ans)
  errors = []
  i = 1
  for an in ans:
    try:
      #print "NO: %d" % i, an.id 
      #t = threading.Thread(target=migrate_pregnancy, args=(an,))
      #time.sleep(2)
      #t.start()
      migrate_pregnancy(an)
      i += 1
    except Exception, e:
      print e
  #print "Found Errors: %d" % len(errors)

  return True

def migrate_births():
  RP_ID = INC_ID; TYPE_ID = 2
  QRY = """
            SELECT
		          ubuzima_report.id,
                          (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                          (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                          (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                          ubuzima_report.date AS birth_date,
                          ubuzima_report.created,
		          (SELECT ubuzima_field.value FROM ubuzima_field 
		          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_number')
		          WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_number,
		          (SELECT ubuzima_field.value FROM ubuzima_field 
		          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_weight')
		          WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_weight,
		          
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'gi')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS gender_gi,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'bo')
						          WHERE ubuzima_field.report_id = ubuzima_report.id) AS gender_bo,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'bf1')
						          WHERE ubuzima_field.report_id = ubuzima_report.id) AS bf1,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nb')
						          WHERE ubuzima_field.report_id = ubuzima_report.id) AS nb,
		          
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'af')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_af,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ci')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ci,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cm')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_cm,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pm')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_pm,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'np')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_np,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'rb')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_rb,

		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hp')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS hp,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hc')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS hc,
              (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ho')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS ho,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'or')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS route,
		          (SELECT ubuzima_field.id FROM ubuzima_field 
				          INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cl')
				          WHERE ubuzima_field.report_id = ubuzima_report.id) AS cl
                
            FROM 
                ubuzima_report
            INNER JOIN
                chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
            INNER JOIN
                ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
            WHERE
                ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
            ORDER BY
                (created)
            ASC
        """
  QRY = QRY % (TYPE_ID, RP_ID)
  ans = fetch_data(MCONN1, QRY)
  indexcol = None
  print "Try Moving %d Birth" % len(ans)
  errors = []
  i = 1
  for an in ans:
    try:
      #print "NO: %d" % i, an.id 
      #t = threading.Thread(target=migrate_birth, args=(an,))
      #time.sleep(2)
      #t.start()
      migrate_birth(an)
      i += 1
    except Exception, e:
      print e
  #print "Found Errors: %d" % len(errors)
  return True

def migrate_birth(an):
  BIR = load(BIR_FILE)
  BIR_DATA = set(BIR.get('BIR'))
  try:    
    errors = []
    indexcol = None
    enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
    if not enduser:
      #print "NO USER"
      errors.append("CHW: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh })
      BIR_DATA.add(an.id)

    migrate_mother(an, enduser)
    mother = fetch_mother(an.national_id)
    
    if not mother:
      #print "No MOther"
      errors.append("Mother: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh})
      BIR_DATA.add(an.id)

    #print enduser.__dict__
    #print an.__dict__
    #print mother.__dict__
    
    preg_start = an.birth_date - datetime.timedelta(days = 277)
    preg_end = an.birth_date
    pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
    if not pregnancy:
      pregnancy = dummy_pregnancy(enduser, mother, an.birth_date)
      pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)

    created_at = an.created
    updated_at = an.created
    user_phone = enduser.telephone
    user_pk = enduser.indexcol
    national_id = mother.national_id
    mother_pk = mother.indexcol
    nation_pk = enduser.nation_pk
    province_pk = enduser.province_pk
    district_pk = enduser.district_pk
    referral_facility_pk = enduser.referral_facility_pk
    facility_pk = enduser.facility_pk
    sector_pk = enduser.sector_pk
    cell_pk = enduser.cell_pk
    village_pk = enduser.village_pk

    birth_date = an.birth_date
    if not birth_date:
      #print "No LMP"
      errors.append("BIRTH REPORT: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh })
      BIR_DATA.add(an.id)

    child_number = int(an.child_number) if an.child_number else 1
    birth = fetch_birth(national_id, birth_date, child_number)
    if birth:
      indexcol = birth.indexcol 

    gender = 'bo' if an.gender_bo else 'gi'
    sex_code = 'M' if an.gender_bo else 'F'
    sex = fetch_gender(sex_code) 
   
    symptom_af = 'af' if an.symptom_af  else None #migrate_field(an, 'af', None, None, None)
    symptom_ci = 'ci' if an.symptom_ci  else None #migrate_field(an, 'ci', None, None, None)
    symptom_cm = 'cm' if an.symptom_cm  else None #migrate_field(an, 'cm', None, None, None)
    symptom_pm = 'pm' if an.symptom_pm  else None #migrate_field(an, 'pm', None, None, None)
    symptom_np = 'np' if an.symptom_np  else None #migrate_field(an, 'np', None, None, None)
    symptom_rb = 'rb' if an.symptom_rb  else None #migrate_field(an, 'rb', None, None, None)

    symptom_np = None if (symptom_af or symptom_ci or symptom_cm or symptom_pm or symptom_rb ) else 'np'

    breastfeeding = 'bf1' if an.bf1 else 'nb'

    location = 'hc'
    if (an.hc  or an.cl ):  location = 'hc'
    if an.route: location = 'or' 
    if an.ho: location = 'ho'  
    if an.hp: location = 'hp'

    child_weight = float(an.child_weight) if an.child_weight else 2.8 

    curr_symptom = {
        'symptom_af' : symptom_af,
        'symptom_ci' : symptom_ci,
        'symptom_cm' : symptom_cm,
        'symptom_pm' : symptom_pm,
        'symptom_np' : symptom_np,
        'symptom_rb' : symptom_rb
    }
    
    TEXT = "%(keyword)s %(national_id)s %(child_number)02d %(birth_date)s %(gender)s %(curr_symptom)s %(location)s %(breastfeeding)s WT%(child_weight)s" % {'keyword': 'BIR', 'national_id':national_id, 
                                            'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year),
                                                               'child_number': child_number, 'gender': gender,
                                                               'curr_symptom': only_values_of_dict(curr_symptom),
                                                           'location': location, 'child_weight': child_weight, 
                                                           'breastfeeding' : breastfeeding  
                                                               }
    message = TEXT
    is_valid = True

    FLDS =  {
      'indexcol' : indexcol,
      'created_at' : created_at,
      'updated_at' : updated_at,
      'national_id' : national_id,
      'mother_pk' : mother_pk,
      'user_phone' : user_phone,
      'user_pk' : user_pk,
      'nation_pk' : nation_pk,
      'province_pk' : province_pk,
      'district_pk' : district_pk,
      'referral_facility_pk' : referral_facility_pk,
      'facility_pk' : facility_pk,
      'sector_pk' : sector_pk,
      'cell_pk' : cell_pk,
      'village_pk' : village_pk,

      'birth_date' : birth_date,
      'child_number': child_number,
      'sex' : gender,
      'sex_pk': sex.indexcol,
      'pregnancy_pk': pregnancy.indexcol, 

      'symptom_af' : symptom_af,
      'symptom_ci' : symptom_ci,
      'symptom_cm' : symptom_cm,
      'symptom_pm' : symptom_pm,
      'symptom_np' : symptom_np,
      'symptom_rb' : symptom_rb,   

      'location' : location,
      'child_weight' : child_weight,
      'breastfeeding' : breastfeeding,    

      'message' : message,
      'is_valid' : is_valid
    }

    #print FLDS
    p = migrate(table='birth', fields = FLDS)
    
  except Exception, e:
    BIR_DATA.add(an.id)
    print e

  BIR['BIR'] = list(BIR_DATA)
  #write(BIR, BIR_FILE)

  return True

def dummy_pregnancy(enduser, mother, birth_date):
  indexcol = None
  lmp = birth_date - datetime.timedelta(days = 270)
  anc2_date = birth_date - datetime.timedelta(days = 150)
  gravidity = fetch_gravidity(mother.national_id)
  parity = fetch_parity(mother.national_id)
  TEXT = "%(keyword)s %(national_id)s %(lmp)s %(anc2_date)s %(gravidity)02d %(parity)02d %(prev_symptom)s %(curr_symptom)s %(location)s WT%(mother_weight)s HT%(mother_height)s %(toilet)s %(handwash)s" % {'keyword': 'PRE', 'national_id':mother.national_id,
                                                             'lmp': "%02d.%02d.%02d" % (lmp.day, lmp.month, lmp.year),
                                                             'anc2_date': "%02d.%02d.%04d" % (anc2_date.day, anc2_date.month, anc2_date.year),
                                                             'gravidity': gravidity, 'parity': parity,
                                                             'prev_symptom' : 'nr',
                                                             'curr_symptom': 'np',
                                                         'location': 'hc', 'mother_weight': '55', 'mother_height': '150',
                                                         'toilet' : 'to', 'handwash' : 'hw'  
                                                             }
  FLDS =  {
    'indexcol' : indexcol,
    'created_at' : lmp,
    'updated_at' : birth_date,
    'national_id' : mother.national_id,
    'mother_pk' : mother.indexcol,
    'user_phone' : enduser.telephone,
    'user_pk' : enduser.indexcol,
    'nation_pk' : enduser.nation_pk,
    'province_pk' : enduser.province_pk,
    'district_pk' : enduser.district_pk,
    'referral_facility_pk' : enduser.referral_facility_pk,
    'facility_pk' : enduser.facility_pk,
    'sector_pk' : enduser.sector_pk,
    'cell_pk' : enduser.cell_pk,
    'village_pk' : enduser.village_pk,

    'lmp' : lmp,
    'anc2_date' : anc2_date,
    'gravidity' : gravidity,
    'parity' : parity,

    'prev_pregnancy_nr' : 'nr',   

    'symptom_np' : 'np',

    'location' : 'hc',
    'mother_weight' : 55,
    'mother_height' : 150,

    'toilet' : 'to',
    'handwash' : 'hw',    

    'bmi': 55 / ((150* 150) / 10000.0),
    'muac' : None,
    'message' : TEXT,
    'is_valid' : False
  }

  try:
    p = migrate(table='pregnancy', fields = FLDS)
  except Exception, e:
    print e

  return True


def dummy_birth(enduser, mother, birth_date, child_number):
  indexcol = None
  gender = 'gi'
  sex_code = 'F'
  curr_symptom = 'np'
  child_weight = 2.8
  breastfeeding = 'bf1'
  location = 'hc'
  sex = fetch_gender(sex_code)
  preg_start = birth_date - datetime.timedelta(days = 277)
  preg_end = birth_date
  pregnancy = fetch_report_pregnancy(mother.national_id, preg_start, preg_end)
  if not pregnancy:
    pregnancy = dummy_pregnancy(enduser, mother, birth_date)
    pregnancy = fetch_report_pregnancy(mother.national_id, preg_start, preg_end)
  TEXT = "%(keyword)s %(national_id)s %(child_number)02d %(birth_date)s %(gender)s %(curr_symptom)s %(location)s %(breastfeeding)s WT%(child_weight)s" % {'keyword': 'BIR', 'national_id':mother.national_id,
                                                          'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year),
                                                             'child_number': child_number, 'gender': gender,
                                                             'curr_symptom': curr_symptom,
                                                         'location': location, 'child_weight': child_weight, 
                                                         'breastfeeding' : breastfeeding  
                                                             }
  FLDS =  {
    'indexcol' : indexcol,
    'created_at' : birth_date,
    'updated_at' : birth_date,
    'national_id' : mother.national_id,
    'mother_pk' : mother.indexcol,
    'user_phone' : enduser.telephone,
    'user_pk' : enduser.indexcol,
    'nation_pk' : enduser.nation_pk,
    'province_pk' : enduser.province_pk,
    'district_pk' : enduser.district_pk,
    'referral_facility_pk' : enduser.referral_facility_pk,
    'facility_pk' : enduser.facility_pk,
    'sector_pk' : enduser.sector_pk,
    'cell_pk' : enduser.cell_pk,
    'village_pk' : enduser.village_pk,

    'birth_date' : birth_date,
    'child_number' : child_number,
    'sex' : gender,
    'sex_pk' : sex.indexcol,
    'pregnancy_pk' : pregnancy.indexcol,   

    'symptom_np' : curr_symptom,

    'location' : location,
    'child_weight' : child_weight,
    'breastfeeding' : breastfeeding,
    'message' : TEXT,
    'is_valid' : False
  }

  try:
    p = migrate(table='birth', fields = FLDS)
  except Exception, e:
    print e

  return True


def migrate_refusals():
  try:
    REF = load(REF_FILE)
    REF_DATA = set(REF.get('REF'))
    RP_ID = INC_ID; TYPE_ID = 15
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.created                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              ASC
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d Refusal" % len(ans)
    
    for an in ans:
      try:        
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          REF_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          REF_DATA.add(an.id)

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk      
      
        TEXT = "%(keyword)s %(national_id)s" % {'keyword': 'REF', 'national_id':national_id }
        message = TEXT
        is_valid = True

        refusal = fetch_refusal(national_id, created_at)
        if refusal: indexcol = refusal.indexcol
        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'message' : message,
          'is_valid' : is_valid
        }

        #print FLDS
        p = migrate(table='refusal', fields = FLDS)          
      except Exception, e:
        REF_DATA.add(an.id) 
        print e
    
      REF['REF'] = list(REF_DATA)
      #write(REF, REF_FILE)         
  except Exception, e:
    print e

  return True


def migrate_ancvisits():
  try:
    ANC = load(ANC_FILE)
    ANC_DATA = set(ANC.get("ANC"))
    RP_ID = INC_ID; TYPE_ID = 1
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.date,
                            ubuzima_report.edd_anc2_date,
                            ubuzima_report.created,
		            (SELECT ubuzima_field.value FROM ubuzima_field 
		            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'mother_weight')
		            WHERE ubuzima_field.report_id = ubuzima_report.id) AS mother_weight,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'anc2')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS anc2,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'anc3')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS anc3,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'anc4')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS anc4,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'af')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_af,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ch')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ch,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'di')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_di,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ds')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ds,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'fe')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_fe,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'fp')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_fp,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hy')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_hy,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ja')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ja,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ma')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ma,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'np')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_np,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ns')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ns,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'oe')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_oe,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pc')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_pc,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'rb')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_rb,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sa')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_sa,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'vo')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_vo,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hp')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS hp,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hc')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS hc,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cl')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS cl
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              ASC
              
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d ANC VISIT" % len(ans)
    errors = []
  
    for an in ans:
      try:
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          #print "NO USER"
          errors.append("CHW: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh })
          ANC_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          #print "No MOther"
          errors.append("Mother: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh})
          ANC_DATA.add(an.id)

        #print enduser.__dict__
        #print an.__dict__
        #print mother.__dict__
        
        anc_date = an.date
        if not anc_date:
          #print "No LMP"
          errors.append("LMP: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh })
          ANC_DATA.add(an.id)

        pregnancy_pk = None
        preg_start = anc_date - datetime.timedelta(days = 277)
        preg_end = anc_date
        pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
        if not pregnancy:
          pregnancy = dummy_pregnancy(enduser, mother, anc_date)
          pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
        
        pregnancy_pk = pregnancy.indexcol

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk

        anc_visit = None
        if an.anc2: anc_visit = "anc2"
        if an.anc3: anc_visit = "anc3"
        if an.anc4: anc_visit = "anc4"
        if not anc_visit:
          ANC_DATA.add(an.id)
        
        anc_report = fetch_ancvisit(an.national_id, pregnancy_pk, anc_visit)
        ## what to do if we found that there is another same visit for this pregnancy?
        ## It means this pregnancy is from another pregnancy
        ## How do we make it then
        ## we take the difference between this pegnancy and the anc_date we divide by 2,
        ## if the difference is more than 30 days, then we set that day as the new lmp 
        if anc_report:
          new_lmp_days = (anc_date - anc_report.anc_date.date()).days / 2#; print "NEW LMP DAYS: ", new_lmp_days
          if new_lmp_days < 30 or new_lmp_days == 0:
            ANC_DATA.add(an.id)
            indexcol = anc_report.indexcol
          else:
            new_lmp = anc_report.anc_date + datetime.timedelta(days = new_lmp_days)
            pregnancy = dummy_pregnancy(enduser, mother, new_lmp + datetime.timedelta(days = 270))
            pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
            pregnancy_pk = pregnancy.indexcol
            indexcol = None
        
        symptom_af = 'af' if an.symptom_af  else None #migrate_field(an, 'af', None, None, None)
        symptom_ch = 'ch' if an.symptom_ch  else None #migrate_field(an, 'ch', None, None, None)
        symptom_di = 'di' if an.symptom_di  else None #migrate_field(an, 'di', None, None, None)
        symptom_ds = 'ds' if an.symptom_ds  else None #migrate_field(an, 'ds', None, None, None)
        symptom_fe = 'fe' if an.symptom_fe  else None #migrate_field(an, 'fe', None, None, None)
        symptom_fp = 'fp' if an.symptom_fp  else None #migrate_field(an, 'fp', None, None, None)
        symptom_hy = 'hy' if an.symptom_hy  else None #migrate_field(an, 'hy', None, None, None)
        symptom_ja = 'ja' if an.symptom_ja  else None #migrate_field(an, 'ja', None, None, None)
        symptom_ma = 'ma' if an.symptom_ma  else None #migrate_field(an, 'ma', None, None, None)
        symptom_np = 'np' if an.symptom_np  else None #migrate_field(an, 'np', None, None, None)
        symptom_ns = 'ns' if an.symptom_ns  else None #migrate_field(an, 'ns', None, None, None)
        symptom_oe = 'oe' if an.symptom_oe  else None #migrate_field(an, 'oe', None, None, None)
        symptom_pc = 'pc' if an.symptom_pc  else None #migrate_field(an, 'pc', None, None, None)
        symptom_sa = 'sa' if an.symptom_sa  else None #migrate_field(an, 'sa', None, None, None)
        symptom_rb = 'rb' if an.symptom_rb  else None #migrate_field(an, 'rb', None, None, None)
        symptom_vo = 'vo' if an.symptom_vo  else None #migrate_field(an, 'vo', None, None, None) 

        symptom_np = None if (symptom_af or symptom_ch or symptom_di or symptom_ds or 
            symptom_fe or symptom_fp or symptom_hy or symptom_ja or 
            symptom_ma or symptom_ns or symptom_oe or symptom_pc or 
            symptom_sa or symptom_rb or symptom_vo) else 'np'

        location = 'hp' if an.hp else 'hc' #migrate_field(an, 'location', None, None, ('hp', 'hc'))
        mother_weight = float(an.mother_weight) if an.mother_weight else 55 #migrate_field(an, 'mother_weight', 150, 35, 55)
        
        curr_symptom = {
            'symptom_af' : symptom_af,
            'symptom_ch' : symptom_ch,
            'symptom_di' : symptom_di,
            'symptom_ds' : symptom_ds,
            'symptom_fe' : symptom_fe,
            'symptom_fp' : symptom_fp,
            'symptom_hy' : symptom_hy,
            'symptom_ja' : symptom_ja,
            'symptom_ma' : symptom_ma,
            'symptom_np' : symptom_np,
            'symptom_ns' : symptom_ns,
            'symptom_oe' : symptom_oe,
            'symptom_pc' : symptom_pc,
            'symptom_sa' : symptom_sa,
            'symptom_rb' : symptom_rb,
            'symptom_vo' : symptom_vo
        }
        #print curr_symptom
        TEXT = "%(keyword)s %(national_id)s %(anc_date)s %(anc_visit)s %(curr_symptom)s %(location)s WT%(mother_weight)s" % {
                                                               'keyword': 'ANC', 'national_id':national_id,
                                                               'anc_date': "%02d.%02d.%04d" % (anc_date.day, anc_date.month, anc_date.year),
                                                                   'anc_visit': anc_visit,
                                                                   'curr_symptom': only_values_of_dict(curr_symptom),
                                                               'location': location, 'mother_weight': mother_weight
                                                                   }
        message = TEXT
        is_valid = True

        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'anc_date' : anc_date,
          'pregnancy_pk' : pregnancy_pk,
          'anc_visit' : anc_visit,

          'symptom_af' : symptom_af,
          'symptom_ch' : symptom_ch,
          'symptom_di' : symptom_di,
          'symptom_ds' : symptom_ds,
          'symptom_fe' : symptom_fe,
          'symptom_fp' : symptom_fp,
          'symptom_hy' : symptom_hy,
          'symptom_ja' : symptom_ja,
          'symptom_ma' : symptom_ma,
          'symptom_np' : symptom_np,
          'symptom_ns' : symptom_ns,
          'symptom_oe' : symptom_oe,
          'symptom_pc' : symptom_pc,
          'symptom_sa' : symptom_sa,
          'symptom_rb' : symptom_rb,
          'symptom_vo' : symptom_vo,    

          'location' : location,
          'mother_weight' : mother_weight,

          'message' : message,
          'is_valid' : is_valid
        }

        #print FLDS      
        p = migrate(table='ancvisit', fields = FLDS)
                
      except Exception, e:
        ANC_DATA.add(an.id)
        print e

      ANC['ANC'] = list(ANC_DATA)
      #write(ANC, ANC_FILE)

  except Exception, e:
    print e
  #print "Found Errors: %d" % len(errors)

  return True


def migrate_departures():
  try:
    DEP = load(DEP_FILE)
    DEP_DATA = set(DEP.get('DEP'))
    RP_ID = INC_ID; TYPE_ID = 16
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.date AS birth_date,
                          ubuzima_report.created,
                      (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_number')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_number
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              ASC
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d Departure" % len(ans)
    
    for an in ans:
      try:        
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          DEP_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          DEP_DATA.add(an.id)

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk 

        pregnancy_pk = None
        child_pk = None
        child_number = None
        birth_date = None
    
        dep_mother = fetch_mother_departure(national_id, created_at)
        preg_start = an.created - datetime.timedelta(days = 277)
        preg_end = an.created
        pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
        if pregnancy: pregnancy_pk = pregnancy.indexcol
        else:
          pregnancy  = dummy_pregnancy(enduser, mother, an.created)
          pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
          pregnancy_pk = pregnancy.indexcol

        TEXT = "%(keyword)s %(national_id)s" % {'keyword': 'DEP', 'national_id':national_id }
        if dep_mother:
          indexcol = dep_mother.indexcol

        if an.birth_date:
          indexcol = None
          birth_date = an.birth_date
          child_number = int(an.child_number) if an.child_number else 0
          birth = fetch_birth(national_id, birth_date, child_number)  
          dep_child = fetch_child_departure(national_id, birth_date, child_number)
          if dep_child:
            indexcol = dep_child.indexcol
          else:
            dep_child = dummy_birth(enduser, mother, birth_date, child_number)
            dep_child = fetch_birth(national_id, birth_date, child_number)
        
          pregnancy_pk = dep_child.pregnancy_pk
          child_pk = dep_child.indexcol    
          TEXT = "%(keyword)s %(national_id)s %(child_number)02d %(birth_date)s" % {'keyword': 'DEP', 'national_id':national_id,
                                                                                    'child_number': child_number, 
                                                       'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year) }
        message = TEXT
        is_valid = True
        
        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'child_number': child_number,
          'birth_date': birth_date,
          'pregnancy_pk': pregnancy_pk,
          'child_pk': child_pk,

          'message' : message,
          'is_valid' : is_valid
        }

        #print FLDS
        p = migrate(table='departure', fields = FLDS)          
      except Exception, e:
        DEP_DATA.add(an.id)
        print e 

    
      DEP['DEP'] = list(DEP_DATA)
      #write(DEP, DEP_FILE)         
  except Exception, e:
    print e

  return True


def migrate_risks():
  try:
    RISK = load(RISK_FILE)
    RISK_DATA = set(RISK.get("RISK"))
    RP_ID = INC_ID; TYPE_ID = 14
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.created,
		            (SELECT ubuzima_field.value FROM ubuzima_field 
		            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'mother_weight')
		            WHERE ubuzima_field.report_id = ubuzima_report.id) AS mother_weight,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'af')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_af,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ch')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ch,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'di')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_di,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ds')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ds,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'fe')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_fe,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'fp')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_fp,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hy')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_hy,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ja')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ja,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ma')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ma,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ns')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ns,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'oe')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_oe,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pc')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_pc,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'rb')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_rb,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sa')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_sa,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'vo')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_vo,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ho')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS ho,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'or')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS route
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              ASC
              
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d RISK" % len(ans)
    errors = []
  
    for an in ans:
      try:
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          #print "NO USER"
          errors.append("CHW: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh })
          RISK_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          #print "No MOther"
          errors.append("Mother: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh})
          RISK_DATA.add(an.id)

        pregnancy_pk = None
        preg_start = an.created - datetime.timedelta(days = 277)
        preg_end = an.created
        pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
        if not pregnancy:
          pregnancy = dummy_pregnancy(enduser, mother, an.created)
          pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
        
        pregnancy_pk = pregnancy.indexcol

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk

                
        symptom_af = 'af' if an.symptom_af  else None #migrate_field(an, 'af', None, None, None)
        symptom_ch = 'ch' if an.symptom_ch  else None #migrate_field(an, 'ch', None, None, None)
        symptom_di = 'di' if an.symptom_di  else None #migrate_field(an, 'di', None, None, None)
        symptom_ds = 'ds' if an.symptom_ds  else None #migrate_field(an, 'ds', None, None, None)
        symptom_fe = 'fe' if an.symptom_fe  else None #migrate_field(an, 'fe', None, None, None)
        symptom_fp = 'fp' if an.symptom_fp  else None #migrate_field(an, 'fp', None, None, None)
        symptom_hy = 'hy' if an.symptom_hy  else None #migrate_field(an, 'hy', None, None, None)
        symptom_ja = 'ja' if an.symptom_ja  else None #migrate_field(an, 'ja', None, None, None)
        symptom_ma = 'ma' if an.symptom_ma  else None #migrate_field(an, 'ma', None, None, None)
        symptom_ns = 'ns' if an.symptom_ns  else None #migrate_field(an, 'ns', None, None, None)
        symptom_oe = 'oe' if an.symptom_oe  else None #migrate_field(an, 'oe', None, None, None)
        symptom_pc = 'pc' if an.symptom_pc  else None #migrate_field(an, 'pc', None, None, None)
        symptom_sa = 'sa' if an.symptom_sa  else None #migrate_field(an, 'sa', None, None, None)
        symptom_rb = 'rb' if an.symptom_rb  else None #migrate_field(an, 'rb', None, None, None)
        symptom_vo = 'vo' if an.symptom_vo  else None #migrate_field(an, 'vo', None, None, None) 

        if not (symptom_af or symptom_ch or symptom_di or symptom_ds or 
            symptom_fe or symptom_fp or symptom_hy or symptom_ja or 
            symptom_ma or symptom_ns or symptom_oe or symptom_pc or 
            symptom_sa or symptom_rb or symptom_vo):  RISK_DATA.add(an.id)

        location = 'or' if an.route else 'ho' 
        mother_weight = float(an.mother_weight) if an.mother_weight else 55 
        
        curr_symptom = {
            'symptom_af' : symptom_af,
            'symptom_ch' : symptom_ch,
            'symptom_di' : symptom_di,
            'symptom_ds' : symptom_ds,
            'symptom_fe' : symptom_fe,
            'symptom_fp' : symptom_fp,
            'symptom_hy' : symptom_hy,
            'symptom_ja' : symptom_ja,
            'symptom_ma' : symptom_ma,
            'symptom_ns' : symptom_ns,
            'symptom_oe' : symptom_oe,
            'symptom_pc' : symptom_pc,
            'symptom_sa' : symptom_sa,
            'symptom_rb' : symptom_rb,
            'symptom_vo' : symptom_vo
        }
        #print curr_symptom
        TEXT = "%(keyword)s %(national_id)s %(curr_symptom)s %(location)s WT%(mother_weight)s" % {
                                                               'keyword': 'RISK', 'national_id':national_id,
                                                               'curr_symptom': only_values_of_dict(curr_symptom),
                                                               'location': location, 'mother_weight': mother_weight
                                                                   }
        message = TEXT
        is_valid = True

        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'pregnancy_pk' : pregnancy_pk,

          'symptom_af' : symptom_af,
          'symptom_ch' : symptom_ch,
          'symptom_di' : symptom_di,
          'symptom_ds' : symptom_ds,
          'symptom_fe' : symptom_fe,
          'symptom_fp' : symptom_fp,
          'symptom_hy' : symptom_hy,
          'symptom_ja' : symptom_ja,
          'symptom_ma' : symptom_ma,
          'symptom_ns' : symptom_ns,
          'symptom_oe' : symptom_oe,
          'symptom_pc' : symptom_pc,
          'symptom_sa' : symptom_sa,
          'symptom_rb' : symptom_rb,
          'symptom_vo' : symptom_vo,    

          'location' : location,
          'mother_weight' : mother_weight,

          'message' : message,
          'is_valid' : is_valid
        }

        #print FLDS, only_values_of_dict(curr_symptom) , an.id
        ## if no symptoms no need to save this report
        if len(only_values_of_dict(curr_symptom).strip()) == 0: RISK_DATA.add(an.id)     
        else: p = migrate(table='risk', fields = FLDS)
                
      except Exception, e:
        RISK_DATA.add(an.id)
        print e

      RISK['RISK'] = list(RISK_DATA)
      #write(RISK, RISK_FILE)

  except Exception, e:
    print e
  #print "Found Errors: %d" % len(errors)

  return True


def migrate_redalerts():
  try:
    RED = load(RED_FILE)
    RED_DATA = set(RED.get("RED"))
    RP_ID = INC_ID; TYPE_ID = 12
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.date AS birth_date,
                            ubuzima_report.created,
                (SELECT ubuzima_field.value FROM ubuzima_field 
                INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_number')
                WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_number,
		            (SELECT ubuzima_field.value FROM ubuzima_field 
		            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'mother_weight')
		            WHERE ubuzima_field.report_id = ubuzima_report.id) AS mother_weight,
		            (SELECT ubuzima_field.value FROM ubuzima_field 
		            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_weight')
		            WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_weight,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ads')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_ads,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cdg')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_cdg,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'co')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_co,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'con')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_con,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hbt')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_hbt,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hfp')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_hfp,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'iuc')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_iuc,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'lbt')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_lbt,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'mc')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_mc,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nbf')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_nbf,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ncb')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_ncb,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nhe')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_nhe,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nsc')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_nsc,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nuf')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_nuf,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pa')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_pa,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ps')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_ps,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'rv')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_rv,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sbp')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_sbp,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sfh')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_sfh,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'shb')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_shb,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'shp')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_shp,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sp')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_sp,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'wu')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_wu,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ys')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_ys,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ap')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_ap,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'bsp')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_bsp,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cop')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_cop,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'he')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_he,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'la')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_la,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sc')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_sc,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sl')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_sl,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'un')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_un,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ho')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS ho,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'or')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS route
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              ASC
              
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d RED ALERT" % len(ans)
    errors = []
  
    for an in ans:
      try:
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          #print "NO USER"
          errors.append("CHW: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh })
          RED_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          #print "No MOther"
          errors.append("Mother: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh})
          RED_DATA.add(an.id)

        pregnancy_pk = None
        preg_start = an.created - datetime.timedelta(days = 277)
        preg_end = an.created
        pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
        if not pregnancy:
          pregnancy = dummy_pregnancy(enduser, mother, an.created)
          pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
        
        pregnancy_pk = pregnancy.indexcol

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk
                
        red_symptom_ads = 'ads' if an.red_symptom_ads else None
        red_symptom_cdg = 'cdg' if an.red_symptom_cdg else None
        red_symptom_co = 'co' if an.red_symptom_co else None
        red_symptom_con = 'con' if an.red_symptom_con else None
        red_symptom_hbt = 'hbt' if an.red_symptom_hbt else None
        red_symptom_hfp = 'hfp' if an.red_symptom_hfp else None
        red_symptom_iuc = 'iuc' if an.red_symptom_iuc else None
        red_symptom_lbt = 'lbt' if an.red_symptom_lbt else None
        red_symptom_mc = 'mc' if an.red_symptom_mc else None
        red_symptom_nbf = 'nbf' if an.red_symptom_nbf else None
        red_symptom_ncb = 'ncb' if an.red_symptom_ncb else None
        red_symptom_nhe = 'nhe' if an.red_symptom_nhe else None
        red_symptom_nsc = 'nsc' if an.red_symptom_nsc else None
        red_symptom_nuf = 'nuf' if an.red_symptom_nuf else None
        red_symptom_pa = 'pa' if an.red_symptom_pa else None
        red_symptom_ps = 'ps' if an.red_symptom_ps else None
        red_symptom_rv = 'rv' if an.red_symptom_rv else None
        red_symptom_sbp = 'sbp' if an.red_symptom_sbp else None
        red_symptom_sfh = 'sfh' if an.red_symptom_sfh else None
        red_symptom_shb = 'shb' if an.red_symptom_shb else None
        red_symptom_shp = 'shp' if an.red_symptom_shp else None
        red_symptom_sp = 'sp' if an.red_symptom_sp else None
        red_symptom_wu = 'wu' if an.red_symptom_wu else None
        red_symptom_ys = 'ys' if an.red_symptom_ys else None
        red_symptom_ap = 'ap' if an.red_symptom_ap else None
        red_symptom_bsp = 'bsp' if an.red_symptom_bsp else None
        red_symptom_cop = 'cop' if an.red_symptom_cop else None
        red_symptom_he = 'he' if an.red_symptom_he else None
        red_symptom_la = 'la' if an.red_symptom_la else None
        red_symptom_sc = 'sc' if an.red_symptom_sc else None
        red_symptom_sl = 'sl' if an.red_symptom_sl else None
        red_symptom_un = 'un' if an.red_symptom_un else None 

        if not (red_symptom_ads or red_symptom_cdg or red_symptom_co or red_symptom_con or red_symptom_hbt or red_symptom_hfp or red_symptom_iuc or red_symptom_lbt or red_symptom_mc or red_symptom_nbf or red_symptom_ncb or red_symptom_nhe or red_symptom_nsc or red_symptom_nuf or red_symptom_pa or red_symptom_ps or red_symptom_rv or red_symptom_sbp or red_symptom_sfh or red_symptom_shb or red_symptom_shp or red_symptom_sp or red_symptom_wu or red_symptom_ys or red_symptom_ap or red_symptom_bsp or red_symptom_cop or red_symptom_he or red_symptom_la or red_symptom_sc or red_symptom_sl or red_symptom_un):  RED_DATA.add(an.id)

        location = 'or' if an.route else 'ho' 
        mother_weight = float(an.mother_weight) if an.mother_weight else 0.0
        child_weight = float(an.child_weight) if an.child_weight else 0.0 
        
        red_symptom = {
            'red_symptom_ads' : red_symptom_ads,
            'red_symptom_cdg' : red_symptom_cdg,
            'red_symptom_co' : red_symptom_co,
            'red_symptom_con' : red_symptom_con,
            'red_symptom_hbt' : red_symptom_hbt,
            'red_symptom_hfp' : red_symptom_hfp,
            'red_symptom_iuc' : red_symptom_iuc,
            'red_symptom_lbt' : red_symptom_lbt,
            'red_symptom_mc' : red_symptom_mc,
            'red_symptom_nbf' : red_symptom_nbf,
            'red_symptom_ncb' : red_symptom_ncb,
            'red_symptom_nhe' : red_symptom_nhe,
            'red_symptom_nsc' : red_symptom_nsc,
            'red_symptom_nuf' : red_symptom_nuf,
            'red_symptom_pa' : red_symptom_pa,
            'red_symptom_ps' : red_symptom_ps,
            'red_symptom_rv' : red_symptom_rv,
            'red_symptom_sbp' : red_symptom_sbp,
            'red_symptom_sfh' : red_symptom_sfh,
            'red_symptom_shb' : red_symptom_shb,
            'red_symptom_shp' : red_symptom_shp,
            'red_symptom_sp' : red_symptom_sp,
            'red_symptom_wu' : red_symptom_wu,
            'red_symptom_ys' : red_symptom_ys,
            'red_symptom_ap' : red_symptom_ap,
            'red_symptom_bsp' : red_symptom_bsp,
            'red_symptom_cop' : red_symptom_cop,
            'red_symptom_he' : red_symptom_he,
            'red_symptom_la' : red_symptom_la,
            'red_symptom_sc' : red_symptom_sc,
            'red_symptom_sl' : red_symptom_sl,
            'red_symptom_un' : red_symptom_un
        }
        #print red_symptom
        TEXT = "%(keyword)s %(national_id)s %(red_symptom)s %(location)s WT%(mother_weight)s" % {'keyword': 'RED', 'national_id':national_id,
                                                  'red_symptom': only_values_of_dict(red_symptom),
                                                               'location': location, 'mother_weight': mother_weight }
        birth_date = None
        child_number = None
        child_pk = None
        if an.birth_date:
          birth_date = an.birth_date
          child_number = int(an.child_number) if an.child_number else 1
          birth = fetch_birth(national_id, birth_date, child_number)  
          if not birth:
            birth = dummy_birth(enduser, mother, birth_date, child_number)
            birth = fetch_birth(national_id, birth_date, child_number)
        
          pregnancy_pk = birth.pregnancy_pk
          child_pk = birth.indexcol    
          TEXT = "%(keyword)s %(national_id)s %(child_number)02d %(birth_date)s %(red_symptom)s %(location)s WT%(child_weight)s" % {
                                                               'keyword': 'RED', 'national_id':national_id,
                                                               'child_number': child_number, 
                                                       'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year),
                                                               'red_symptom': only_values_of_dict(red_symptom),
                                                               'location': location, 'child_weight': child_weight
                                                                   }
        message = TEXT
        is_valid = True

        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'child_number': child_number,
          'birth_date': birth_date,
          'pregnancy_pk': pregnancy_pk,
          'child_pk': child_pk,

          'red_symptom_ads' : red_symptom_ads,
            'red_symptom_cdg' : red_symptom_cdg,
            'red_symptom_co' : red_symptom_co,
            'red_symptom_con' : red_symptom_con,
            'red_symptom_hbt' : red_symptom_hbt,
            'red_symptom_hfp' : red_symptom_hfp,
            'red_symptom_iuc' : red_symptom_iuc,
            'red_symptom_lbt' : red_symptom_lbt,
            'red_symptom_mc' : red_symptom_mc,
            'red_symptom_nbf' : red_symptom_nbf,
            'red_symptom_ncb' : red_symptom_ncb,
            'red_symptom_nhe' : red_symptom_nhe,
            'red_symptom_nsc' : red_symptom_nsc,
            'red_symptom_nuf' : red_symptom_nuf,
            'red_symptom_pa' : red_symptom_pa,
            'red_symptom_ps' : red_symptom_ps,
            'red_symptom_rv' : red_symptom_rv,
            'red_symptom_sbp' : red_symptom_sbp,
            'red_symptom_sfh' : red_symptom_sfh,
            'red_symptom_shb' : red_symptom_shb,
            'red_symptom_shp' : red_symptom_shp,
            'red_symptom_sp' : red_symptom_sp,
            'red_symptom_wu' : red_symptom_wu,
            'red_symptom_ys' : red_symptom_ys,
            'red_symptom_ap' : red_symptom_ap,
            'red_symptom_bsp' : red_symptom_bsp,
            'red_symptom_cop' : red_symptom_cop,
            'red_symptom_he' : red_symptom_he,
            'red_symptom_la' : red_symptom_la,
            'red_symptom_sc' : red_symptom_sc,
            'red_symptom_sl' : red_symptom_sl,
            'red_symptom_un' : red_symptom_un,   

          'location' : location,
          'mother_weight' : mother_weight,
          'child_weight' : child_weight,

          'message' : message,
          'is_valid' : is_valid
        }

        #print FLDS, only_values_of_dict(red_symptom) , an.id
        ## if no symptoms no need to save this report
        if len(only_values_of_dict(red_symptom).strip()) == 0: RED_DATA.add(an.id)     
        else: p = migrate(table='redalert', fields = FLDS)
                
      except Exception, e:
        RED_DATA.add(an.id)
        print e

      RED['RED'] = list(RED_DATA)
      #write(RED, RED_FILE)

  except Exception, e:
    print e
  #print "Found Errors: %d" % len(errors)

  return True

def migrate_redresults():
  try:
    RAR = load(RAR_FILE)
    RAR_DATA = set(RAR.get("RAR"))
    RP_ID = INC_ID; TYPE_ID = 11
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.date AS birth_date,
                            ubuzima_report.created,
                (SELECT ubuzima_field.value FROM ubuzima_field 
                INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_number')
                WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_number,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ads')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_ads,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cdg')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_cdg,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'co')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_co,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'con')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_con,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hbt')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_hbt,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hfp')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_hfp,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'iuc')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_iuc,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'lbt')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_lbt,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'mc')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_mc,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nbf')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_nbf,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ncb')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_ncb,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nhe')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_nhe,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nsc')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_nsc,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nuf')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_nuf,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pa')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_pa,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ps')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_ps,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'rv')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_rv,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sbp')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_sbp,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sfh')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_sfh,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'shb')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_shb,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'shp')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_shp,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sp')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_sp,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'wu')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_wu,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ys')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_ys,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ap')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_ap,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'bsp')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_bsp,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cop')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_cop,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'he')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_he,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'la')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_la,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sc')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_sc,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sl')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_sl,
                (SELECT ubuzima_field.id FROM ubuzima_field 
                            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'un')
                            WHERE ubuzima_field.report_id = ubuzima_report.id) AS red_symptom_un,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ho')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS ho,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'or')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS route,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hp')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS hp,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hc')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS hc,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cl')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS cl,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'at')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS at,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'al')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS al,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'na')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS na,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'mw')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS mw,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ms')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS ms,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cw')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS cw,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cs')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS cs
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              ASC
              
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d RED ALERT RESULT" % len(ans)
    errors = []
  
    for an in ans:
      try:
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          #print "NO USER"
          errors.append("CHW: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh })
          RAR_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          #print "No MOther"
          errors.append("Mother: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh})
          RAR_DATA.add(an.id)

        pregnancy_pk = None
        red_pk = None
        emergency_date = None

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk
                
        red_symptom_ads = 'ads' if an.red_symptom_ads else None
        red_symptom_cdg = 'cdg' if an.red_symptom_cdg else None
        red_symptom_co = 'co' if an.red_symptom_co else None
        red_symptom_con = 'con' if an.red_symptom_con else None
        red_symptom_hbt = 'hbt' if an.red_symptom_hbt else None
        red_symptom_hfp = 'hfp' if an.red_symptom_hfp else None
        red_symptom_iuc = 'iuc' if an.red_symptom_iuc else None
        red_symptom_lbt = 'lbt' if an.red_symptom_lbt else None
        red_symptom_mc = 'mc' if an.red_symptom_mc else None
        red_symptom_nbf = 'nbf' if an.red_symptom_nbf else None
        red_symptom_ncb = 'ncb' if an.red_symptom_ncb else None
        red_symptom_nhe = 'nhe' if an.red_symptom_nhe else None
        red_symptom_nsc = 'nsc' if an.red_symptom_nsc else None
        red_symptom_nuf = 'nuf' if an.red_symptom_nuf else None
        red_symptom_pa = 'pa' if an.red_symptom_pa else None
        red_symptom_ps = 'ps' if an.red_symptom_ps else None
        red_symptom_rv = 'rv' if an.red_symptom_rv else None
        red_symptom_sbp = 'sbp' if an.red_symptom_sbp else None
        red_symptom_sfh = 'sfh' if an.red_symptom_sfh else None
        red_symptom_shb = 'shb' if an.red_symptom_shb else None
        red_symptom_shp = 'shp' if an.red_symptom_shp else None
        red_symptom_sp = 'sp' if an.red_symptom_sp else None
        red_symptom_wu = 'wu' if an.red_symptom_wu else None
        red_symptom_ys = 'ys' if an.red_symptom_ys else None
        red_symptom_ap = 'ap' if an.red_symptom_ap else None
        red_symptom_bsp = 'bsp' if an.red_symptom_bsp else None
        red_symptom_cop = 'cop' if an.red_symptom_cop else None
        red_symptom_he = 'he' if an.red_symptom_he else None
        red_symptom_la = 'la' if an.red_symptom_la else None
        red_symptom_sc = 'sc' if an.red_symptom_sc else None
        red_symptom_sl = 'sl' if an.red_symptom_sl else None
        red_symptom_un = 'un' if an.red_symptom_un else None 

        if not (red_symptom_ads or red_symptom_cdg or red_symptom_co or red_symptom_con or red_symptom_hbt or red_symptom_hfp or red_symptom_iuc or red_symptom_lbt or red_symptom_mc or red_symptom_nbf or red_symptom_ncb or red_symptom_nhe or red_symptom_nsc or red_symptom_nuf or red_symptom_pa or red_symptom_ps or red_symptom_rv or red_symptom_sbp or red_symptom_sfh or red_symptom_shb or red_symptom_shp or red_symptom_sp or red_symptom_wu or red_symptom_ys or red_symptom_ap or red_symptom_bsp or red_symptom_cop or red_symptom_he or red_symptom_la or red_symptom_sc or red_symptom_sl or red_symptom_un):  RAR_DATA.add(an.id) 
        
        red_symptom = {
            'red_symptom_ads' : red_symptom_ads,
            'red_symptom_cdg' : red_symptom_cdg,
            'red_symptom_co' : red_symptom_co,
            'red_symptom_con' : red_symptom_con,
            'red_symptom_hbt' : red_symptom_hbt,
            'red_symptom_hfp' : red_symptom_hfp,
            'red_symptom_iuc' : red_symptom_iuc,
            'red_symptom_lbt' : red_symptom_lbt,
            'red_symptom_mc' : red_symptom_mc,
            'red_symptom_nbf' : red_symptom_nbf,
            'red_symptom_ncb' : red_symptom_ncb,
            'red_symptom_nhe' : red_symptom_nhe,
            'red_symptom_nsc' : red_symptom_nsc,
            'red_symptom_nuf' : red_symptom_nuf,
            'red_symptom_pa' : red_symptom_pa,
            'red_symptom_ps' : red_symptom_ps,
            'red_symptom_rv' : red_symptom_rv,
            'red_symptom_sbp' : red_symptom_sbp,
            'red_symptom_sfh' : red_symptom_sfh,
            'red_symptom_shb' : red_symptom_shb,
            'red_symptom_shp' : red_symptom_shp,
            'red_symptom_sp' : red_symptom_sp,
            'red_symptom_wu' : red_symptom_wu,
            'red_symptom_ys' : red_symptom_ys,
            'red_symptom_ap' : red_symptom_ap,
            'red_symptom_bsp' : red_symptom_bsp,
            'red_symptom_cop' : red_symptom_cop,
            'red_symptom_he' : red_symptom_he,
            'red_symptom_la' : red_symptom_la,
            'red_symptom_sc' : red_symptom_sc,
            'red_symptom_sl' : red_symptom_sl,
            'red_symptom_un' : red_symptom_un
        }

        location = 'hc'
        if (an.hc  or an.cl ):  location = 'hc'
        if an.route: location = 'or' 
        if an.ho: location = 'ho'  
        if an.hp: location = 'hp'

        intervention = 'at'
        health_status = 'mw'
        if an.at: intervention = 'at'
        if an.al: intervention = 'al'
        if an.na: intervention = 'na'
    
        if an.mw: health_status = 'mw'
        if an.ms: health_status = 'ms'

        filters = filters_of_dict_keys(red_symptom)
        red_created_at = an.created - datetime.timedelta(days = 2)
        filters.update( {"created_at > %s" : red_created_at})
        #print "FLTS: ", filters
        
        #print red_symptom
        TEXT = "%(keyword)s %(national_id)s %(red_symptom)s %(location)s %(intervention)s %(health_status)s" % {'keyword': 'RAR',
                                                  'national_id':national_id,
                                                  'red_symptom': only_values_of_dict(red_symptom),
                                                  'location': location, 'intervention': intervention, 'health_status': health_status }
        
        preg_start = an.created - datetime.timedelta(days = 277)
        preg_end = an.created
        pregnancy = fetch_report_pregnancy(mother.national_id, preg_start, preg_end)
        if pregnancy: pregnancy_pk = pregnancy.indexcol
        if not pregnancy:
          pregnancy = dummy_pregnancy(enduser, mother, an.created)
          pregnancy = fetch_report_pregnancy(mother.national_id, preg_start, preg_end)
                  

        birth_date = None
        child_number = None
        child_pk = None
        if an.birth_date:
          birth_date = an.birth_date
          child_number = int(an.child_number) if an.child_number else 1
          birth = fetch_birth(national_id, birth_date, child_number)
          filters.update({'child_number = %s': child_number, 'birth_date = %s': birth_date})  
          if not birth:
            birth = dummy_birth(enduser, mother, birth_date, child_number)
            birth = fetch_birth(national_id, birth_date, child_number)

          if an.cw: health_status = 'cw'
          if an.cs: health_status = 'cs'
        
          pregnancy_pk = birth.pregnancy_pk
          child_pk = birth.indexcol    
          TEXT="%(keyword)s %(national_id)s %(child_number)02d %(birth_date)s %(red_symptom)s %(location)s %(intervention)s %(status)" % {

                                                               'keyword': 'RAR', 'national_id':national_id,
                                                               'child_number': child_number, 
                                                       'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year),
                                                               'red_symptom': only_values_of_dict(red_symptom),
                                   'location': location, 'intervention': intervention, 'status': health_status }

        
        red = fetch_redalert(national_id, filters )#; print red.__dict__
        if red:
          red_pk = red.indexcol
          pregnancy_pk = red.pregnancy_pk
          emergency_date = red.created_at
          rar = fetch_redresult(an.national_id, red_pk, {}) #; print rar.__dict__
          if rar: indexcol = rar.indexcol
                                                                   
        message = TEXT
        is_valid = True
        
        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'child_number': child_number,
          'birth_date': birth_date,
          'pregnancy_pk': pregnancy_pk,
          'child_pk': child_pk,
          'red_pk': red_pk,
          'emergency_date': emergency_date,

          'red_symptom_ads' : red_symptom_ads,
            'red_symptom_cdg' : red_symptom_cdg,
            'red_symptom_co' : red_symptom_co,
            'red_symptom_con' : red_symptom_con,
            'red_symptom_hbt' : red_symptom_hbt,
            'red_symptom_hfp' : red_symptom_hfp,
            'red_symptom_iuc' : red_symptom_iuc,
            'red_symptom_lbt' : red_symptom_lbt,
            'red_symptom_mc' : red_symptom_mc,
            'red_symptom_nbf' : red_symptom_nbf,
            'red_symptom_ncb' : red_symptom_ncb,
            'red_symptom_nhe' : red_symptom_nhe,
            'red_symptom_nsc' : red_symptom_nsc,
            'red_symptom_nuf' : red_symptom_nuf,
            'red_symptom_pa' : red_symptom_pa,
            'red_symptom_ps' : red_symptom_ps,
            'red_symptom_rv' : red_symptom_rv,
            'red_symptom_sbp' : red_symptom_sbp,
            'red_symptom_sfh' : red_symptom_sfh,
            'red_symptom_shb' : red_symptom_shb,
            'red_symptom_shp' : red_symptom_shp,
            'red_symptom_sp' : red_symptom_sp,
            'red_symptom_wu' : red_symptom_wu,
            'red_symptom_ys' : red_symptom_ys,
            'red_symptom_ap' : red_symptom_ap,
            'red_symptom_bsp' : red_symptom_bsp,
            'red_symptom_cop' : red_symptom_cop,
            'red_symptom_he' : red_symptom_he,
            'red_symptom_la' : red_symptom_la,
            'red_symptom_sc' : red_symptom_sc,
            'red_symptom_sl' : red_symptom_sl,
            'red_symptom_un' : red_symptom_un,   

          'location' : location,
          'intervention' : intervention,
          'health_status' : health_status,

          'message' : message,
          'is_valid' : is_valid
        }

        if not red:
          red = dummy_red(FLDS, red_symptom)
          red = fetch_redalert(national_id, filters )
          FLDS['red_pk'] = red.indexcol
          FLDS['emergency_date'] = red.created_at
        #print FLDS, only_values_of_dict(red_symptom) , an.id
        ## if no symptoms no need to save this report
        if len(only_values_of_dict(red_symptom).strip()) == 0: RAR_DATA.add(an.id)     
        else: p = migrate(table='redresult', fields = FLDS)
                
      except Exception, e:
        RAR_DATA.add(an.id)
        print e

      RAR['RAR'] = list(RAR_DATA)
      #write(RAR, RAR_FILE)

  except Exception, e:
    print e
  #print "Found Errors: %d" % len(errors)

  return True


def dummy_red(flds, red_symptom):
  if flds.get('child_number') or flds.get('birth_date'):
    child_number = flds.get('child_number')
    birth_date = flds.get('birth_date')
    flds['child_weight'] = 3.5
    flds['message'] =  "%(keyword)s %(national_id)s %(child_number)02d %(birth_date)s %(red_symptom)s %(location)s WT%(child_weight)s" % {
                                                               'keyword': 'RED', 'national_id':flds.get('national_id'),
                                                               'child_number': child_number, 
                                                       'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year),
                                                               'red_symptom': only_values_of_dict(red_symptom),
                                                               'location': 'ho', 'child_weight': child_weight
                                                                   }
  else:
    flds['mother_weight'] = 56  
    flds['message'] = "%(keyword)s %(national_id)s %(red_symptom)s %(location)s WT%(mother_weight)s" % {
                                                               'keyword': 'RED', 'national_id':flds.get('national_id'),
                                                               'red_symptom': only_values_of_dict(red_symptom),
                                                               'location': 'ho', 'mother_weight': flds.get('mother_weight')
                                                                   }

  flds.pop('intervention')
  flds.pop('health_status')
  flds.pop('emergency_date')
  flds.pop('red_pk')
  flds['created_at'] = flds.get('created_at') - datetime.timedelta(days = 1)
  flds['is_valid'] = False
  #print "FIELDS: ", flds
  if len(only_values_of_dict(red_symptom).strip()) > 0: p = migrate(table='redalert', fields = flds)
  return True


def migrate_riskresults():
  try:
    RES = load(RES_FILE)
    RES_DATA = set(RES.get("RES"))
    RP_ID = INC_ID; TYPE_ID = 13
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.created,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'af')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_af,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ch')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ch,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'di')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_di,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ds')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ds,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'fe')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_fe,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'fp')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_fp,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hy')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_hy,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ja')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ja,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ma')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ma,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ns')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ns,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'oe')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_oe,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pc')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_pc,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'rb')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_rb,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sa')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_sa,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'vo')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_vo,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ho')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS ho,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'or')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS route,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hp')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS hp,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hc')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS hc,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cl')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS cl,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'aa')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS aa,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pr')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS pr,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'mw')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS mw,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ms')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS ms
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              ASC
              
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d RISK RESULT" % len(ans)
    errors = []
  
    for an in ans:
      try:
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          #print "NO USER"
          errors.append("CHW: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh })
          RES_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          #print "No MOther"
          errors.append("Mother: Report %(id)d, Patient %(nid)s, CHW %(tel)s " % {'id': an.id, 'nid': an.national_id, 'tel': an.telephone_moh})
          RES_DATA.add(an.id)

        pregnancy_pk = None
        preg_start = an.created - datetime.timedelta(days = 277)
        preg_end = an.created
        pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
        if not pregnancy:
          pregnancy = dummy_pregnancy(enduser, mother, an.created)
          pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
        
        pregnancy_pk = pregnancy.indexcol

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk

                
        symptom_af = 'af' if an.symptom_af  else None #migrate_field(an, 'af', None, None, None)
        symptom_ch = 'ch' if an.symptom_ch  else None #migrate_field(an, 'ch', None, None, None)
        symptom_di = 'di' if an.symptom_di  else None #migrate_field(an, 'di', None, None, None)
        symptom_ds = 'ds' if an.symptom_ds  else None #migrate_field(an, 'ds', None, None, None)
        symptom_fe = 'fe' if an.symptom_fe  else None #migrate_field(an, 'fe', None, None, None)
        symptom_fp = 'fp' if an.symptom_fp  else None #migrate_field(an, 'fp', None, None, None)
        symptom_hy = 'hy' if an.symptom_hy  else None #migrate_field(an, 'hy', None, None, None)
        symptom_ja = 'ja' if an.symptom_ja  else None #migrate_field(an, 'ja', None, None, None)
        symptom_ma = 'ma' if an.symptom_ma  else None #migrate_field(an, 'ma', None, None, None)
        symptom_ns = 'ns' if an.symptom_ns  else None #migrate_field(an, 'ns', None, None, None)
        symptom_oe = 'oe' if an.symptom_oe  else None #migrate_field(an, 'oe', None, None, None)
        symptom_pc = 'pc' if an.symptom_pc  else None #migrate_field(an, 'pc', None, None, None)
        symptom_sa = 'sa' if an.symptom_sa  else None #migrate_field(an, 'sa', None, None, None)
        symptom_rb = 'rb' if an.symptom_rb  else None #migrate_field(an, 'rb', None, None, None)
        symptom_vo = 'vo' if an.symptom_vo  else None #migrate_field(an, 'vo', None, None, None) 

        if not (symptom_af or symptom_ch or symptom_di or symptom_ds or 
            symptom_fe or symptom_fp or symptom_hy or symptom_ja or 
            symptom_ma or symptom_ns or symptom_oe or symptom_pc or 
            symptom_sa or symptom_rb or symptom_vo):  RES_DATA.add(an.id) 
        
        curr_symptom = {
            'symptom_af' : symptom_af,
            'symptom_ch' : symptom_ch,
            'symptom_di' : symptom_di,
            'symptom_ds' : symptom_ds,
            'symptom_fe' : symptom_fe,
            'symptom_fp' : symptom_fp,
            'symptom_hy' : symptom_hy,
            'symptom_ja' : symptom_ja,
            'symptom_ma' : symptom_ma,
            'symptom_ns' : symptom_ns,
            'symptom_oe' : symptom_oe,
            'symptom_pc' : symptom_pc,
            'symptom_sa' : symptom_sa,
            'symptom_rb' : symptom_rb,
            'symptom_vo' : symptom_vo
        }
        
        location = 'hc'
        if (an.hc  or an.cl ):  location = 'hc'
        if an.route: location = 'or' 
        if an.ho: location = 'ho'  
        if an.hp: location = 'hp'

        intervention = 'aa'
        health_status = 'mw'
        if an.aa: intervention = 'aa'
        if an.pr: intervention = 'pr'
    
        if an.mw: health_status = 'mw'
        if an.ms: health_status = 'ms'

        filters = filters_of_dict_keys(curr_symptom)
        risk_created_at = an.created - datetime.timedelta(days = 2)
        filters.update( {"created_at > %s" : risk_created_at})
        #print "FLTS: ", filters
        
        #print curr_symptom
        TEXT = "%(keyword)s %(national_id)s %(curr_symptom)s %(location)s %(intervention)s %(health_status)s" % {'keyword': 'RES',
                                                  'national_id':national_id,
                                                  'curr_symptom': only_values_of_dict(curr_symptom),
                                                  'location': location, 'intervention': intervention, 'health_status': health_status }

        risk = fetch_risk(national_id, filters )#; print red.__dict__
        if risk:
          risk_pk = risk.indexcol
          pregnancy_pk = risk.pregnancy_pk
          res = fetch_riskresult(an.national_id, risk_pk, {}) #; print rar.__dict__
          if res: indexcol = res.indexcol

        message = TEXT
        is_valid = True

        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'pregnancy_pk' : pregnancy_pk,
          'risk_pk': risk_pk,

          'symptom_af' : symptom_af,
          'symptom_ch' : symptom_ch,
          'symptom_di' : symptom_di,
          'symptom_ds' : symptom_ds,
          'symptom_fe' : symptom_fe,
          'symptom_fp' : symptom_fp,
          'symptom_hy' : symptom_hy,
          'symptom_ja' : symptom_ja,
          'symptom_ma' : symptom_ma,
          'symptom_ns' : symptom_ns,
          'symptom_oe' : symptom_oe,
          'symptom_pc' : symptom_pc,
          'symptom_sa' : symptom_sa,
          'symptom_rb' : symptom_rb,
          'symptom_vo' : symptom_vo,    

          'location' : location,
          'intervention' : intervention,
          'health_status' : health_status,

          'message' : message,
          'is_valid' : is_valid
        }

        if not risk:
          risk = dummy_risk(FLDS, curr_symptom)
          risk = fetch_risk(national_id, filters )
          FLDS['risk_pk'] = risk.indexcol

        #print FLDS, only_values_of_dict(curr_symptom) , an.id
        ## if no symptoms no need to save this report
        if len(only_values_of_dict(curr_symptom).strip()) == 0: RES_DATA.add(an.id)     
        else: p = migrate(table='riskresult', fields = FLDS)
                
      except Exception, e:
        RES_DATA.add(an.id)
        print e

      RES['RES'] = list(RES_DATA)
      #write(RES, RES_FILE)

  except Exception, e:
    print e
  #print "Found Errors: %d" % len(errors)

  return True

def dummy_risk(flds, curr_symptom):
  flds['mother_weight'] = 56.0  
  flds['message'] = "%(keyword)s %(national_id)s %(curr_symptom)s %(location)s WT%(mother_weight)s" % {
                                                               'keyword': 'RISK', 'national_id':flds.get('national_id'),
                                                               'curr_symptom': only_values_of_dict(curr_symptom),
                                                               'location': 'ho', 'mother_weight': flds.get('mother_weight')
                                                                   }

  flds.pop('intervention')
  flds.pop('health_status')
  flds.pop('risk_pk')
  flds['created_at'] = flds.get('created_at') - datetime.timedelta(days = 1)
  flds['is_valid'] = False
  #print "FIELDS: ", flds
  if len(only_values_of_dict(curr_symptom).strip()) > 0: p = migrate(table='risk', fields = flds)
  return True


def migrate_deaths():
  try:
    DTH = load(DTH_FILE)
    DTH_DATA = set(DTH.get('DTH'))
    RP_ID = INC_ID; TYPE_ID = 7
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.date AS birth_date,
                          ubuzima_report.created,
                      (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_number')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_number,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ho')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS ho,
		                  (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'or')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS route,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hp')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS hp,
		                  (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hc')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS hc,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cl')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS cl,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nd')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS nd,
		                  (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cd')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS cd,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'md')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS md,
		                  (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sbd')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS sbd,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'mcc')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS mcc
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              ASC
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d Death" % len(ans)
    
    for an in ans:
      try:        
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          DTH_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          DTH_DATA.add(an.id)

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk 

        pregnancy_pk = None
        child_pk = None
        child_number = None
        birth_date = None
    
        dth_mother = fetch_mother_death(national_id, created_at)
        preg_start = an.created - datetime.timedelta(days = 277)
        preg_end = an.created
        pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
        if pregnancy: pregnancy_pk = pregnancy.indexcol
        else:
          pregnancy  = dummy_pregnancy(enduser, mother, an.created)
          pregnancy = fetch_report_pregnancy(an.national_id, preg_start, preg_end)
          pregnancy_pk = pregnancy.indexcol


        location = 'ho'
        if (an.hc  or an.cl ):  location = 'hc'
        if an.route: location = 'or' 
        if an.ho: location = 'ho'  
        if an.hp: location = 'hp'

        death_code = 'md'
        if an.nd: death_code = 'nd'
        if an.cd: death_code = 'cd'
        if an.md: death_code = 'md'
        if an.sbd: death_code = 'sbd'
        if an.mcc: death_code = 'mcc'

        TEXT = "%(keyword)s %(national_id)s %(location)s %(death_code)s" % {'keyword': 'DTH', 'national_id':national_id,
                                                                             'location': location, 'death_code': death_code }
        if dth_mother:
          indexcol = dth_mother.indexcol

        if an.nd or an.cd:
          indexcol = None
          birth_date = an.birth_date
          child_number = int(an.child_number) if an.child_number else None
          if not birth_date:  birth_date = an.created - datetime.timedelta(days = 30)
          if not child_number:  fetch_parity(national_id) + 1            
          if not death_code: death_code = 'cd'
          birth = fetch_birth(national_id, birth_date, child_number)  
          dth_child = fetch_child_death(national_id, birth_date, child_number)
          if dth_child:
            indexcol = dth_child.indexcol
          else:
            child = dummy_birth(enduser, mother, birth_date, child_number)
            birth = fetch_birth(national_id, birth_date, child_number)
        
          pregnancy_pk = birth.pregnancy_pk
          child_pk = birth.indexcol    
          TEXT = "%(keyword)s %(national_id)s %(child_number)02d %(birth_date)s %(location)s %(death_code)s" % {'keyword': 'DTH',
                                                                                    'national_id':national_id,
                                                                                    'child_number': child_number, 
                                                       'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year),
                                                          'location': location, 'death_code': death_code }
        message = TEXT
        is_valid = True
        
        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'child_number': child_number,
          'birth_date': birth_date,
          'pregnancy_pk': pregnancy_pk,
          'child_pk': child_pk,

          'location': location,
          'death_code': death_code,

          'message' : message,
          'is_valid' : is_valid
        }

        #print FLDS
        p = migrate(table='death', fields = FLDS)          
      except Exception, e:
        DTH_DATA.add(an.id)
        print e 

    
      DTH['DTH'] = list(DTH_DATA)
      #write(DTH, DTH_FILE)         
  except Exception, e:
    print e

  return True


def migrate_nbcvisits():
  try:
    NBC = load(NBC_FILE)
    NBC_DATA = set(NBC.get('NBC'))
    RP_ID = INC_ID; TYPE_ID = 8
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.date AS birth_date,
                          ubuzima_report.created,
                      (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_number')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_number,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nbc1')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS nbc1,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nbc2')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS nbc2,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nbc3')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS nbc3,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nbc4')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS nbc4,
                  (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nbc5')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS nbc5,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'af')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_af,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pm')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_pm,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'rb')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_rb,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ci')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ci,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cm')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_cm,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'np')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_np,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ebf')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS ebf,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cbf')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS cbf,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nb')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS nb,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'aa')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS aa,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pr')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS pr,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cw')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS cw,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cs')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS cs
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              DESC 
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d NBC" % len(ans)
    
    for an in ans:
      try:        
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          NBC_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          NBC_DATA.add(an.id)

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk 

        pregnancy_pk = None
        child_pk = None
        child_number = None
        birth_date = None

        nbc_visit = None
        if an.nbc1: nbc_visit = "nbc1"
        if an.nbc2: nbc_visit = "nbc2"
        if an.nbc3: nbc_visit = "nbc3"
        if an.nbc4: nbc_visit = "nbc4"
        if an.nbc5: nbc_visit = "nbc5"
        if not nbc_visit:
          NBC_DATA.add(an.id)

        breastfeeding = 'ebf'
        if an.ebf: breastfeeding = 'ebf' 
        if an.cbf: breastfeeding = 'cf'  
        if an.nb: breastfeeding = 'nb'

        intervention = 'aa'
        health_status = 'cw'
        if an.aa: intervention = 'aa'
        if an.pr: intervention = 'pr'
    
        if an.cw: health_status = 'cw'
        if an.cs: health_status = 'cs'

        symptom_af = 'af' if an.symptom_af  else None 
        symptom_ci = 'ci' if an.symptom_ci  else None 
        symptom_cm = 'cm' if an.symptom_cm  else None 
        symptom_np = 'np' if an.symptom_np  else None 
        symptom_pm = 'pm' if an.symptom_pm  else None 
        symptom_rb = 'rb' if an.symptom_rb  else None  

        symptom_np = None if (symptom_af or symptom_ci or symptom_cm or symptom_pm or 
            symptom_rb ) else 'np'

        curr_symptom = {
            'symptom_af' : symptom_af,
            'symptom_ci' : symptom_ci,
            'symptom_cm' : symptom_cm,
            'symptom_np' : symptom_np,
            'symptom_pm' : symptom_pm,
            'symptom_rb' : symptom_rb,
        }
    
        if an.birth_date:
          birth_date = an.birth_date
          child_number = int(an.child_number) if an.child_number else fetch_parity(national_id) + 1
          birth = fetch_birth(national_id, birth_date, child_number)
          if birth: child_pk = birth.indexcol
          nbcvisit = fetch_nbcvisit(national_id, child_pk, nbc_visit)
          if not birth:
            birth = dummy_birth(enduser, mother, birth_date, child_number)
            birth = fetch_birth(national_id, birth_date, child_number)
          if nbcvisit:
            indexcol = nbcvisit.indexcol
          
          child_pk = birth.indexcol
          pregnancy_pk = birth.pregnancy_pk      
          
        else:
          NBC_DATA.add(an.id)
        
        TEXT = "%(keyword)s %(national_id)s %(child_number)02d %(nbc_visit)s %(birth_date)s %(curr_symptom)s %(breastfeeding)s %(intervention)s %(health_status)s" % {'keyword': 'NBC', 'national_id':national_id,
                                                       'child_number': child_number, 'nbc_visit': nbc_visit,
                                                       'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year),
                                                       'curr_symptom': only_values_of_dict(curr_symptom),
                                   'breastfeeding': breastfeeding, 'intervention': intervention, 'health_status': health_status
                                                         }
        message = TEXT
        is_valid = True
        
        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'child_number': child_number,
          'birth_date': birth_date,
          'pregnancy_pk': pregnancy_pk,
          'child_pk': child_pk,
          'nbc_visit': nbc_visit,

          'symptom_af' : symptom_af,
          'symptom_ci' : symptom_ci,
          'symptom_cm' : symptom_cm,
          'symptom_np' : symptom_np,
          'symptom_pm' : symptom_pm,
          'symptom_rb' : symptom_rb,

          'breastfeeding' : breastfeeding,
          'intervention' : intervention,
          'health_status' : health_status,
          
          'message' : message,
          'is_valid' : is_valid
        }

        #print FLDS, an.id
        p = migrate(table='nbcvisit', fields = FLDS)          
      except Exception, e:
        NBC_DATA.add(an.id)
        print e 

    
      NBC['NBC'] = list(NBC_DATA)
      #write(NBC, NBC_FILE)         
  except Exception, e:
    print e

  return True


def migrate_pncvisits():
  try:
    PNC = load(PNC_FILE)
    PNC_DATA = set(PNC.get('PNC'))
    RP_ID = INC_ID; TYPE_ID = 9
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.date AS birth_date,
                          ubuzima_report.created,
                      (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_number')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_number,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pnc1')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS pnc1,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pnc2')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS pnc2,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pnc3')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS pnc3,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'np')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_np,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ch')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ch,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'di')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_di,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ds')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ds,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'fe')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_fe,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'fp')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_fp,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hy')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_hy,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ja')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ja,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ma')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ma,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ns')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ns,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'oe')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_oe,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pc')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_pc,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'rb')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_rb,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'sa')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_sa,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'vo')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_vo,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'aa')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS aa,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pr')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS pr,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'mw')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS mw,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ms')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS ms
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              DESC 
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d PNC" % len(ans)
    
    for an in ans:
      try:        
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          PNC_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          PNC_DATA.add(an.id)

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk 

        pregnancy_pk = None
        child_pk = None
        child_number = None
        delivery_date = None

        pnc_visit = None
        if an.pnc1: pnc_visit = "pnc1"
        if an.pnc2: pnc_visit = "pnc2"
        if an.pnc3: pnc_visit = "pnc3"
        if not pnc_visit:
          PNC_DATA.add(an.id)

        intervention = 'aa'
        health_status = 'mw'
        if an.aa: intervention = 'aa'
        if an.pr: intervention = 'pr'
    
        if an.mw: health_status = 'mw'
        if an.ms: health_status = 'ms'

        symptom_af = 'np' if an.symptom_np  else None #migrate_field(an, 'np', None, None, None)
        symptom_ch = 'ch' if an.symptom_ch  else None #migrate_field(an, 'ch', None, None, None)
        symptom_di = 'di' if an.symptom_di  else None #migrate_field(an, 'di', None, None, None)
        symptom_ds = 'ds' if an.symptom_ds  else None #migrate_field(an, 'ds', None, None, None)
        symptom_fe = 'fe' if an.symptom_fe  else None #migrate_field(an, 'fe', None, None, None)
        symptom_fp = 'fp' if an.symptom_fp  else None #migrate_field(an, 'fp', None, None, None)
        symptom_hy = 'hy' if an.symptom_hy  else None #migrate_field(an, 'hy', None, None, None)
        symptom_ja = 'ja' if an.symptom_ja  else None #migrate_field(an, 'ja', None, None, None)
        symptom_ma = 'ma' if an.symptom_ma  else None #migrate_field(an, 'ma', None, None, None)
        symptom_ns = 'ns' if an.symptom_ns  else None #migrate_field(an, 'ns', None, None, None)
        symptom_oe = 'oe' if an.symptom_oe  else None #migrate_field(an, 'oe', None, None, None)
        symptom_pc = 'pc' if an.symptom_pc  else None #migrate_field(an, 'pc', None, None, None)
        symptom_sa = 'sa' if an.symptom_sa  else None #migrate_field(an, 'sa', None, None, None)
        symptom_rb = 'rb' if an.symptom_rb  else None #migrate_field(an, 'rb', None, None, None)
        symptom_vo = 'vo' if an.symptom_vo  else None #migrate_field(an, 'vo', None, None, None) 

        if not (symptom_ch or symptom_di or symptom_ds or 
            symptom_fe or symptom_fp or symptom_hy or symptom_ja or 
            symptom_ma or symptom_ns or symptom_oe or symptom_pc or 
            symptom_sa or symptom_rb or symptom_vo):  symptom_np = 'np' 
        
        curr_symptom = {
            'symptom_np' : symptom_np,
            'symptom_ch' : symptom_ch,
            'symptom_di' : symptom_di,
            'symptom_ds' : symptom_ds,
            'symptom_fe' : symptom_fe,
            'symptom_fp' : symptom_fp,
            'symptom_hy' : symptom_hy,
            'symptom_ja' : symptom_ja,
            'symptom_ma' : symptom_ma,
            'symptom_ns' : symptom_ns,
            'symptom_oe' : symptom_oe,
            'symptom_pc' : symptom_pc,
            'symptom_sa' : symptom_sa,
            'symptom_rb' : symptom_rb,
            'symptom_vo' : symptom_vo
        }
    
        if an.birth_date:
          delivery_date = an.birth_date
          child_number = int(an.child_number) if an.child_number else fetch_parity(national_id) + 1
          birth = fetch_delivery(national_id, delivery_date)
          pncvisit = fetch_pncvisit(national_id, delivery_date, pnc_visit)
          if not birth:
            birth = dummy_birth(enduser, mother, delivery_date, child_number)
            birth = fetch_birth(national_id, delivery_date, child_number)
          if pncvisit:
            indexcol = pncvisit.indexcol
          
          child_pk = birth.indexcol
          pregnancy_pk = birth.pregnancy_pk
          child_number = birth.child_number      
          
        else:
          PNC_DATA.add(an.id)
        
        TEXT = "%(keyword)s %(national_id)s %(pnc_visit)s %(birth_date)s %(curr_symptom)s %(intervention)s %(health_status)s" % {
                                                       'keyword': 'PNC', 'national_id':national_id,
                                                       'pnc_visit': pnc_visit,
                                                 'birth_date': "%02d.%02d.%04d" % (delivery_date.day, delivery_date.month, delivery_date.year),
                                                       'curr_symptom': only_values_of_dict(curr_symptom),
                                                       'intervention': intervention, 'health_status': health_status
                                                         }
        message = TEXT
        is_valid = True
        
        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'delivery_date': delivery_date,
          'pregnancy_pk': pregnancy_pk,
          'child_pk': child_pk,
          'pnc_visit': pnc_visit,

          'symptom_np' : symptom_np,
            'symptom_ch' : symptom_ch,
            'symptom_di' : symptom_di,
            'symptom_ds' : symptom_ds,
            'symptom_fe' : symptom_fe,
            'symptom_fp' : symptom_fp,
            'symptom_hy' : symptom_hy,
            'symptom_ja' : symptom_ja,
            'symptom_ma' : symptom_ma,
            'symptom_ns' : symptom_ns,
            'symptom_oe' : symptom_oe,
            'symptom_pc' : symptom_pc,
            'symptom_sa' : symptom_sa,
            'symptom_rb' : symptom_rb,
            'symptom_vo' : symptom_vo,

          'intervention' : intervention,
          'health_status' : health_status,
          
          'message' : message,
          'is_valid' : is_valid
        }

        #print FLDS, an.id
        p = migrate(table='pncvisit', fields = FLDS)          
      except Exception, e:
        PNC_DATA.add(an.id)
        print e 

    
      PNC['PNC'] = list(PNC_DATA)
      #write(PNC, PNC_FILE)         
  except Exception, e:
    print e

  return True

def migrate_ccms():
  try:
    CCM = load(CCM_FILE)
    CCM_DATA = set(CCM.get('CCM'))
    RP_ID = INC_ID; TYPE_ID = 4
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.date AS birth_date,
                          ubuzima_report.created,
                      (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_number')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_number,
                     (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'muac')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS muac,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ib')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ib,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'db')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_db,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'di')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_di,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ma')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ma,
                  (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'np')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_np,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'oi')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_oi,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pc')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_pc,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nv')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_nv,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'aa')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS aa,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pr')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS pr,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'tr')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS tr,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pt')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS pt
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              DESC 
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d CCM" % len(ans)
    
    for an in ans:
      try:        
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          CCM_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          CCM_DATA.add(an.id)

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk 

        pregnancy_pk = None
        child_pk = None
        child_number = None
        birth_date = None
        muac = float(an.muac) if an.muac else 0.0

        intervention = 'aa'
        if an.aa: intervention = 'aa'
        if an.pr: intervention = 'pr'
        if an.tr: intervention = 'tr'
        if an.pt: intervention = 'pt'
    
        symptom_ib = 'ib' if an.symptom_ib  else None 
        symptom_db = 'db' if an.symptom_db  else None 
        symptom_di = 'di' if an.symptom_di  else None 
        symptom_ma = 'ma' if an.symptom_ma  else None 
        symptom_np = 'np' if an.symptom_np  else None 
        symptom_oi = 'oi' if an.symptom_oi  else None
        symptom_pc = 'pc' if an.symptom_pc  else None 
        symptom_nv = 'nv' if an.symptom_nv  else None  

        symptom_np = None if (symptom_ib or symptom_db or symptom_di or symptom_ma or 
            symptom_oi or symptom_pc or symptom_nv ) else 'np'

        curr_symptom = {
            'symptom_ib': symptom_ib,
            'symptom_db': symptom_db,
            'symptom_di': symptom_di,
            'symptom_ma': symptom_ma,
            'symptom_np': symptom_np,
            'symptom_oi': symptom_oi,
            'symptom_pc': symptom_pc,
            'symptom_nv': symptom_nv,
        }

        filters = filters_of_dict_keys(curr_symptom)
        ccm_created_at = an.created - datetime.timedelta(days = 2)
        filters.update( {"created_at > %s" : ccm_created_at})
    
        if an.birth_date:
          birth_date = an.birth_date
          child_number = int(an.child_number) if an.child_number else fetch_parity(national_id) + 1
          birth = fetch_birth(national_id, birth_date, child_number)
          if birth:
            child_pk = birth.indexcol
            filters.update({'child_pk = %s': child_pk})
          ccm = fetch_ccm(national_id, filters)
          if not birth:
            birth = dummy_birth(enduser, mother, birth_date, child_number)
            birth = fetch_birth(national_id, birth_date, child_number)
          if ccm:
            indexcol = ccm.indexcol
          
          child_pk = birth.indexcol
          pregnancy_pk = birth.pregnancy_pk      
          
        else:
          CCM_DATA.add(an.id)
        
        TEXT = "%(keyword)s %(national_id)s %(child_number)02d %(birth_date)s %(curr_symptom)s %(intervention)s MUAC%(muac)s" % {
                                                       'keyword': 'CCM', 'national_id':national_id,
                                                       'child_number': child_number,
                                                       'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year),
                                                       'curr_symptom': only_values_of_dict(curr_symptom),
                                   'intervention': intervention, 'muac': muac
                                                         }
        message = TEXT
        is_valid = True
        
        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'child_number': child_number,
          'birth_date': birth_date,
          'pregnancy_pk': pregnancy_pk,
          'child_pk': child_pk,

          'symptom_ib': symptom_ib,
            'symptom_db': symptom_db,
            'symptom_di': symptom_di,
            'symptom_ma': symptom_ma,
            'symptom_np': symptom_np,
            'symptom_oi': symptom_oi,
            'symptom_pc': symptom_pc,
            'symptom_nv': symptom_nv,
          
          'intervention' : intervention,
          'muac' : muac,
          
          'message' : message,
          'is_valid' : is_valid
        }

        #print FLDS, an.id
        p = migrate(table='ccm', fields = FLDS)          
      except Exception, e:
        CCM_DATA.add(an.id)
        print e 

    
      CCM['CCM'] = list(CCM_DATA)
      #write(CCM, CCM_FILE)         
  except Exception, e:
    print e

  return True


def migrate_cmrs():
  try:
    CMR = load(CMR_FILE)
    CMR_DATA = set(CMR.get('CMR'))
    RP_ID = INC_ID; TYPE_ID = 6
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.date AS birth_date,
                          ubuzima_report.created,
                      (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_number')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_number,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ib')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ib,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'db')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_db,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'di')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_di,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ma')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ma,
                  (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'np')
						            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_np,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'oi')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_oi,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pc')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_pc,
		            (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nv')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_nv,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'aa')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS aa,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pr')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS pr,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'tr')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS tr,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'pt')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS pt,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cw')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS cw,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cs')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS cs
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              DESC 
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d CMR" % len(ans)
    
    for an in ans:
      try:        
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          CMR_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          CMR_DATA.add(an.id)

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk 

        pregnancy_pk = None
        child_pk = None
        child_number = None
        birth_date = None
        ccm_pk = None

        intervention = 'aa'
        health_status = 'cw'
        if an.aa: intervention = 'aa'
        if an.pr: intervention = 'pr'
        if an.tr: intervention = 'tr'
        if an.pt: intervention = 'pt'
    
        if an.cw: health_status = 'cw'
        if an.cs: health_status = 'cs'

        symptom_ib = 'ib' if an.symptom_ib  else None 
        symptom_db = 'db' if an.symptom_db  else None 
        symptom_di = 'di' if an.symptom_di  else None 
        symptom_ma = 'ma' if an.symptom_ma  else None 
        symptom_np = 'np' if an.symptom_np  else None 
        symptom_oi = 'oi' if an.symptom_oi  else None
        symptom_pc = 'pc' if an.symptom_pc  else None 
        symptom_nv = 'nv' if an.symptom_nv  else None  

        symptom_np = None if (symptom_ib or symptom_db or symptom_di or symptom_ma or 
            symptom_oi or symptom_pc or symptom_nv ) else 'np'

        curr_symptom = {
            'symptom_ib': symptom_ib,
            'symptom_db': symptom_db,
            'symptom_di': symptom_di,
            'symptom_ma': symptom_ma,
            'symptom_np': symptom_np,
            'symptom_oi': symptom_oi,
            'symptom_pc': symptom_pc,
            'symptom_nv': symptom_nv,
        }

        filters = filters_of_dict_keys(curr_symptom)
        cmr_created_at = an.created - datetime.timedelta(days = 2)
        filters.update( {"created_at > %s" : cmr_created_at})
    
        if an.birth_date:
          birth_date = an.birth_date
          child_number = int(an.child_number) if an.child_number else fetch_parity(national_id) + 1
          birth = fetch_birth(national_id, birth_date, child_number)
          if not birth:
            birth = dummy_birth(enduser, mother, birth_date, child_number)
            birth = fetch_birth(national_id, birth_date, child_number)

          child_pk = birth.indexcol
          filters.update({'child_pk = %s': child_pk})
                    
          child_pk = birth.indexcol
          pregnancy_pk = birth.pregnancy_pk      
          
        else:
          CMR_DATA.add(an.id)
        
        TEXT = "%(keyword)s %(national_id)s %(child_number)02d %(birth_date)s %(curr_symptom)s %(intervention)s %(health_status)s" % {
                                                       'keyword': 'CMR', 'national_id':national_id,
                                                       'child_number': child_number,
                                                       'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year),
                                                       'curr_symptom': only_values_of_dict(curr_symptom),
                                   'intervention': intervention, 'health_status': health_status
                                                         }
        message = TEXT
        is_valid = True
        
        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'child_number': child_number,
          'birth_date': birth_date,
          'pregnancy_pk': pregnancy_pk,
          'child_pk': child_pk,
          'ccm_pk': ccm_pk,

          'symptom_ib': symptom_ib,
            'symptom_db': symptom_db,
            'symptom_di': symptom_di,
            'symptom_ma': symptom_ma,
            'symptom_np': symptom_np,
            'symptom_oi': symptom_oi,
            'symptom_pc': symptom_pc,
            'symptom_nv': symptom_nv,
          
          'intervention' : intervention,
          'health_status' : health_status,
          
          'message' : message,
          'is_valid' : is_valid
        }
    
        ccm = fetch_ccm(national_id, filters)
        if not ccm:
          ccm = dummy_ccm(FLDS, curr_symptom)
          ccm = fetch_ccm(national_id, filters)
        FLDS['ccm_pk'] = ccm.indexcol
        filters.update({"ccm_pk = %s": FLDS['ccm_pk']})            
        cmr = fetch_cmr(national_id, filters)          
        if cmr:
          FLDS['indexcol'] = cmr.indexcol

        #print FLDS, an.id
        p = migrate(table='cmr', fields = FLDS)          
      except Exception, e:
        CMR_DATA.add(an.id)
        print e 

    
      CMR['CMR'] = list(CMR_DATA)
      #write(CMR, CMR_FILE)         
  except Exception, e:
    print e

  return True

def dummy_ccm(flds, curr_symptom):

  child_number = flds.get('child_number')
  birth_date = flds.get('birth_date')
  flds['muac'] = 0.0
  flds['message'] =  "%(keyword)s %(national_id)s %(child_number)02d %(birth_date)s %(curr_symptom)s %(intervention)s MUAC%(muac)s" % {
                                                             'keyword': 'CCM', 'national_id':flds.get('national_id'),
                                                             'child_number': child_number, 
                                                     'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year),
                                                             'curr_symptom': only_values_of_dict(curr_symptom),
                                                             'intervention': flds['intervention'], 'muac': flds['muac']
                                                                 }

  flds.pop('health_status')
  flds.pop('ccm_pk')
  flds['created_at'] = flds.get('created_at') - datetime.timedelta(days = 1)
  flds['is_valid'] = False
  #print "FIELDS: ", flds
  if len(only_values_of_dict(curr_symptom).strip()) > 0: p = migrate(table='ccm', fields = flds)
  return True


def migrate_cbns():
  try:
    CBN = load(CBN_FILE)
    CBN_DATA = set(CBN.get('CBN'))
    RP_ID = INC_ID; TYPE_ID = 3
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.date AS birth_date,
                          ubuzima_report.created,
                      (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_number')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_number,
                      (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_height')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_height,
                     (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_weight')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_weight,
                     (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'muac')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS muac,                      
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ebf')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS ebf,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cbf')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS cbf,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nb')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS nb
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              DESC 
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d CBN" % len(ans)
    
    for an in ans:
      try:        
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          CBN_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          CBN_DATA.add(an.id)

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk 

        pregnancy_pk = None
        child_pk = None
        child_number = None
        birth_date = None
        child_weight = float(an.child_weight) if an.child_weight else 0.0
        child_height = float(an.child_height) if an.child_height else 0.0
        muac = float(an.muac) if an.muac else 0.0

        breastfeeding = 'ebf'
        if an.ebf: breastfeeding = 'ebf'
        if an.cbf: breastfeeding = 'cf'
        if an.nb: breastfeeding = 'nb'
    
        cbn_created_at = an.created - datetime.timedelta(days = 30)
        filters = {"created_at > %s" : cbn_created_at}
    
        if an.birth_date:
          birth_date = an.birth_date
          child_number = int(an.child_number) if an.child_number else fetch_parity(national_id) + 1
          birth = fetch_birth(national_id, birth_date, child_number)
          if birth:
            child_pk = birth.indexcol
            filters.update({'child_pk = %s': child_pk})
          cbn = fetch_cbn(national_id, filters)
          if not birth:
            birth = dummy_birth(enduser, mother, birth_date, child_number)
            birth = fetch_birth(national_id, birth_date, child_number)
          if cbn:
            indexcol = cbn.indexcol
          
          child_pk = birth.indexcol
          pregnancy_pk = birth.pregnancy_pk      
          
        else:
          CBN_DATA.add(an.id)
        
        TEXT = "%(keyword)s %(national_id)s %(child_number)02d %(birth_date)s %(breastfeeding)s WT%(child_weight)s MUAC%(muac)s" % {
                                                       'keyword': 'CBN', 'national_id':national_id,
                                                       'child_number': child_number,
                                                       'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year),
                                                       'breastfeeding': breastfeeding, 'child_weight': child_weight, 'muac': muac
                                                         }
        message = TEXT
        is_valid = True
        
        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'child_number': child_number,
          'birth_date': birth_date,
          'pregnancy_pk': pregnancy_pk,
          'child_pk': child_pk,

          'breastfeeding' : breastfeeding,
          'child_weight': child_weight,
          'child_height': child_height,
          'muac' : muac,
          
          'message' : message,
          'is_valid' : is_valid
        }

        #print FLDS, an.id
        p = migrate(table='nutrition', fields = FLDS)          
      except Exception, e:
        CBN_DATA.add(an.id)
        print e 

    
      CBN['CBN'] = list(CBN_DATA)
      #write(CBN, CBN_FILE)         
  except Exception, e:
    print e

  return True

def migrate_chis():
  try:
    CHI = load(CHI_FILE)
    CHI_DATA = set(CHI.get('CHI'))
    RP_ID = INC_ID; TYPE_ID = 5
    QRY = """
              SELECT
		            ubuzima_report.id,
                            (SELECT national_id FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS chw_nid,
                            (SELECT telephone_moh FROM chws_reporter WHERE chws_reporter.id = ubuzima_report.reporter_id) AS telephone_moh,
                            (SELECT national_id FROM ubuzima_patient WHERE ubuzima_patient.id = ubuzima_report.patient_id) AS national_id,
                            ubuzima_report.date AS birth_date,
                          ubuzima_report.created,
                      (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_number')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_number,
                      (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'child_weight')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS child_weight,
                     (SELECT ubuzima_field.value FROM ubuzima_field 
                      INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'muac')
                      WHERE ubuzima_field.report_id = ubuzima_report.id) AS muac,                      
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'v1')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS v1,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'v2')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS v2,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'v3')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS v3,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'v4')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS v4,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'v5')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS v5,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'v6')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS v6,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'vc')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS vc,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'vi')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS vi,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'nv')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS nv,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ib')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_ib,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'db')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_db,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				            INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'np')
				            WHERE ubuzima_field.report_id = ubuzima_report.id) AS symptom_np,
                (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'ho')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS ho,
		                  (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'or')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS route,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hp')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS hp,
		                  (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'hc')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS hc,
                      (SELECT ubuzima_field.id FROM ubuzima_field 
				                  INNER JOIN ubuzima_fieldtype ON ( ubuzima_fieldtype.id = ubuzima_field.type_id AND ubuzima_fieldtype.key = 'cl')
				                  WHERE ubuzima_field.report_id = ubuzima_report.id) AS cl
                  
              FROM 
                  ubuzima_report
              INNER JOIN
                  chws_reporter ON ( chws_reporter.id = ubuzima_report.reporter_id )
              INNER JOIN
                  ubuzima_patient ON ( ubuzima_patient.id = ubuzima_report.patient_id ) 
              WHERE
                  ubuzima_report.type_id = %s AND ubuzima_report.id > %s  
              ORDER BY
                  (created)
              DESC 
          """
    QRY = QRY % (TYPE_ID, RP_ID)
    ans = fetch_data(MCONN1, QRY)
    print "Try Moving %d CHI" % len(ans)
    
    for an in ans:
      try:        
        indexcol = None
        enduser = fetch_enduser(an.chw_nid, an.telephone_moh)
        if not enduser:
          CHI_DATA.add(an.id)

        migrate_mother(an, enduser)
        mother = fetch_mother(an.national_id)
        
        if not mother:
          CHI_DATA.add(an.id)

        created_at = an.created
        updated_at = an.created
        user_phone = enduser.telephone
        user_pk = enduser.indexcol
        national_id = mother.national_id
        mother_pk = mother.indexcol
        nation_pk = enduser.nation_pk
        province_pk = enduser.province_pk
        district_pk = enduser.district_pk
        referral_facility_pk = enduser.referral_facility_pk
        facility_pk = enduser.facility_pk
        sector_pk = enduser.sector_pk
        cell_pk = enduser.cell_pk
        village_pk = enduser.village_pk 

        pregnancy_pk = None
        child_pk = None
        child_number = None
        birth_date = None
        child_weight = float(an.child_weight) if an.child_weight else 0.0
        muac = float(an.muac) if an.muac else 0.0

        location = 'hc'
        if (an.hc  or an.cl ):  location = 'hc'
        if an.route: location = 'or' 
        if an.ho: location = 'ho'  
        if an.hp: location = 'hp'
        
        vaccine = 'v1'
        if an.v1: vaccine = 'v1'
        if an.v2: vaccine = 'v2'
        if an.v3: vaccine = 'v3'
        if an.v4: vaccine = 'v4'
        if an.v5: vaccine = 'v5'
        if an.v6: vaccine = 'v6'

        vaccine_status = 'vi'
        if an.vi: vaccine_status = 'vi'
        if an.vc: vaccine_status = 'vc'
        if an.nv: vaccine_status = 'nv'

        symptom_ib = 'ib' if an.symptom_ib  else None 
        symptom_db = 'db' if an.symptom_db  else None 
        symptom_np = 'np' if an.symptom_np  else None  

        symptom_np = None if (symptom_ib or symptom_db) else 'np'

        curr_symptom = {
            'symptom_ib': symptom_ib,
            'symptom_db': symptom_db,
            'symptom_np': symptom_np,
        }
    
        chi_created_at = an.created - datetime.timedelta(days = 30)
        filters = {"created_at > %s" : chi_created_at}
    
        if an.birth_date:
          birth_date = an.birth_date
          child_number = int(an.child_number) if an.child_number else fetch_parity(national_id) + 1
          birth = fetch_birth(national_id, birth_date, child_number)
          if birth:
            child_pk = birth.indexcol
            filters.update({'child_pk = %s': child_pk})
          chi = fetch_chi(national_id, filters)
          if not birth:
            birth = dummy_birth(enduser, mother, birth_date, child_number)
            birth = fetch_birth(national_id, birth_date, child_number)
          if chi:
            indexcol = chi.indexcol
          
          child_pk = birth.indexcol
          pregnancy_pk = birth.pregnancy_pk      
          
        else:
          CHI_DATA.add(an.id)
        
        TEXT = "%(keyword)s %(national_id)s %(child_number)02d %(birth_date)s %(vaccine)s %(vaccine_status)s %(curr_symptom)s %(location)s WT%(child_weight)s MUAC%(muac)s" % {
                                                       'keyword': 'CHI', 'national_id':national_id,
                                                       'child_number': child_number,
                                                       'birth_date': "%02d.%02d.%04d" % (birth_date.day, birth_date.month, birth_date.year),
                                                       'vaccine': vaccine, "vaccine_status": vaccine_status,
                                                        'curr_symptom': only_values_of_dict(curr_symptom),
                                                       'location': location, 'child_weight': child_weight, 'muac': muac
                                                         }
        message = TEXT
        is_valid = True
        
        FLDS =  {
          'indexcol' : indexcol,
          'created_at' : created_at,
          'updated_at' : updated_at,
          'national_id' : national_id,
          'mother_pk' : mother_pk,
          'user_phone' : user_phone,
          'user_pk' : user_pk,
          'nation_pk' : nation_pk,
          'province_pk' : province_pk,
          'district_pk' : district_pk,
          'referral_facility_pk' : referral_facility_pk,
          'facility_pk' : facility_pk,
          'sector_pk' : sector_pk,
          'cell_pk' : cell_pk,
          'village_pk' : village_pk,

          'child_number': child_number,
          'birth_date': birth_date,
          'pregnancy_pk': pregnancy_pk,
          'child_pk': child_pk,
          'vaccine': vaccine,
          'vaccine_status': vaccine_status,

          'symptom_ib': symptom_ib,
          'symptom_db': symptom_db,
          'symptom_np': symptom_np,

          'location' : location,
          'child_weight': child_weight,
          'muac' : muac,
          
          'message' : message,
          'is_valid' : is_valid
        }

        #print FLDS, an.id
        p = migrate(table='childhealth', fields = FLDS)          
      except Exception, e:
        CHI_DATA.add(an.id)
        print e 

    
      CHI['CHI'] = list(CHI_DATA)
      #write(CHI, CHI_FILE)         
  except Exception, e:
    print e

  return True
