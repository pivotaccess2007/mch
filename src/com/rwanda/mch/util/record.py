#!/usr/bin/env python
# encoding: utf-8
# vim: ts=2 expandtab

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

##
## The only file to use orm directly
## 

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

from util.mch_connection import MCONN, MCONN1, PCONN, orm, INC_ID, GESTATION
import sha
import datetime


CHWS_PERFORMANCE_HEADERS = [ 'surname', 'given_name', 'telephone', 'date_of_birth', 'national_id', 'role_name', 'location_level_name',
                             'email', 'province_name', 'district_name', 'referral_name',  'facility_name', 'sector_name',
                             'cell_name', 'village_name',
                             'pre', 'anc', 'dep', 'ref', 'risk', 'res', 'red', 'rar', 'bir',
                             'nbc', 'pnc', 'ccm', 'cmr', 'cbn', 'chi', 'smn', 'smr', 'rso', 'so', 'ss'
                            ]

CHWS_HEADERS  = [  'surname', 'given_name', 'telephone', 'date_of_birth', 'national_id', 'role_name', 'location_level_name',
                   'email', 'province_name', 'district_name', 'referral_name',  'facility_name', 'sector_name',
                   'cell_name', 'village_name'
                  ]

class Record(object):
 def __init__(self, cursor, registro):
  for (attr, val) in zip((d[0] for d in cursor.description), registro) :
   setattr(self, attr, val)

def fetch_columns(table):
  ans = orm.ORM.fetch_columns(table)
  return ans

def fetch_data(connection, query_string):
  curseur = connection.cursor()
  curseur.execute(query_string)
  ans = []
  for row in curseur.fetchall() :
    r = Record(curseur, row)
    ans.append(r)
    curseur.close()
  return ans

def fetch_orm_data(orm_query):
  ans = []
  for an in orm_query.list():
    r = Record(an.query.cursor, an.value)
    ans.append(r)
  return ans

def fetch_record(orm_query):
  an = None
  for an in orm_query.list():
    r = Record(an.query.cursor, an.value)
    an = r
    return an
  return an

def fetch_nation(code):
  QRY = orm.ORM.query('nation', {'code = %s': code})
  return fetch_record(QRY)

def fetch_province(code):
  QRY = orm.ORM.query('province', {'code = %s': code})
  return fetch_record(QRY)

def fetch_district(code):
  QRY = orm.ORM.query('district', {'code = %s': code})
  return fetch_record(QRY)

def fetch_sector(code):
  QRY = orm.ORM.query('sector', {'code = %s': code})
  return fetch_record(QRY)

def fetch_cell(code):
  QRY = orm.ORM.query('cell', {'code = %s': code})
  return fetch_record(QRY)

def fetch_village(code):
  QRY = orm.ORM.query('village', {'code = %s': code})
  return fetch_record(QRY)

def fetch_facility(code):
  QRY = orm.ORM.query('facility', {'code = %s': code})
  return fetch_record(QRY)

def fetch_facility_code(name):
  QRY = orm.ORM.query('facility', {"lower(name) LIKE %s ": name, 'facility_type_pk = %s' : 8}, cols = ['code'])
  #print QRY.query
  return fetch_record(QRY)

def fetch_education_level(code):
  QRY = orm.ORM.query('education_level', {'code = %s': code})
  return fetch_record(QRY)

def fetch_location_level(code):
  QRY = orm.ORM.query('location_level', {'code = %s': code})
  return fetch_record(QRY)

def fetch_simcard(msisdn):
  QRY = orm.ORM.query('simcard', {'msisdn = %s': msisdn})
  return fetch_record(QRY)

def fetch_role(code):
  QRY = orm.ORM.query('role', {'code = %s': code})
  return fetch_record(QRY)

def get_role(pk):
  QRY = orm.ORM.query('role', {'indexcol = %s': pk})
  return fetch_record(QRY)

def fetch_privilege(code):
  QRY = orm.ORM.query('privilege', {'code = %s': code})
  return fetch_record(QRY)

def fetch_by_id(table, pk):
  QRY = orm.ORM.query(table, {'indexcol = %s': pk})
  return fetch_record(QRY)

def fetch_assigned_privilege(pk, user_pk, role_pk):
  flts = {'privilege_pk = %s': pk}
  if user_pk: flts.update({'user_pk = %s': user_pk})
  if role_pk: flts.update({'role_pk = %s': role_pk})
  QRY = orm.ORM.query('user_privilege', flts)
  ##print QRY.query
  return fetch_record(QRY)

def fetch_gender(code):
  QRY = orm.ORM.query('gender', {'code = %s': code})
  return fetch_record(QRY)

def fetch_language(code):
  QRY = orm.ORM.query('language', {'code = %s': code})
  return fetch_record(QRY)

def fetch_roles(filters = {}):
  QRY = orm.ORM.query('role', filters)
  return fetch_orm_data(QRY)

def fetch_user_privileges(user):
  QRY = orm.ORM.query('user_privilege', {'user_pk = %s OR role_pk = %s': (user.indexcol, user.role_pk)})
  privs = fetch_orm_data(QRY)
  QRY = orm.ORM.query('privilege', { 'indexcol IN %s': (x.privilege_pk for x in privs) } )
  return fetch_orm_data(QRY)

def fetch_users_ids_with_privilege(filters = {}):
  QRY = orm.ORM.query('user_privilege', cols = ['user_pk'], filters = filters)
  return fetch_orm_data(QRY)

def fetch_privileges(filters = {}):
  QRY = orm.ORM.query('privilege', filters)
  return fetch_orm_data(QRY)

def fetch_languages():
  QRY = orm.ORM.query('language', {})
  return fetch_orm_data(QRY)

def fetch_genders():
  QRY = orm.ORM.query('gender', {})
  return fetch_orm_data(QRY)

def fetch_education_levels(filters = {}):
  QRY = orm.ORM.query('education_level', filters )
  return fetch_orm_data(QRY)

def fetch_enduser(national_id, telephone):
  QRY = orm.ORM.query('enduser', {'national_id = %s': national_id, 'telephone = %s': telephone })
  return fetch_record(QRY)

def fetch_ambulance(telephone):
  subs = [{('name', 'referral_facility'): ('facility', 'referral_facility_pk')}, {('code', 'referral_facility') : ('facility', 'referral_facility_pk')}]
  joins = [
            {'name': ('nation', 'nation_pk')}, {'code' : ('nation', 'nation_pk')},
            {'name': ('province', 'province_pk')}, {'code' : ('province', 'province_pk')},
            {'name': ('district', 'district_pk')}, {'code' : ('district', 'district_pk')},
            {'name': ('facility', 'facility_pk')}, {'code' : ('facility', 'facility_pk')}          
          ]
  QRY = orm.ORM.query('ambulance', {'telephone = %s': telephone }, subs = subs, joins = joins)
  return fetch_record(QRY)

def fetch_mother(national_id):
  QRY = orm.ORM.query('mother', {'national_id = %s': national_id})
  return fetch_record(QRY)

def fetch_pregnancy(national_id, lmp):
  QRY = orm.ORM.query('pregnancy', {'national_id = %s': national_id, 'lmp = %s': lmp})
  return fetch_record(QRY)

def fetch_report(table, pk):
    QRY = orm.ORM.query(table, {'indexcol = %s': pk})
    return fetch_record(QRY)

def fetch_duplicate_report(table, filters):
    ##print table, filters
    QRY = orm.ORM.query(table, filters)
    #print QRY.query
    return fetch_orm_data(QRY)

def fetch_report_codes(keyword):
  QRY = orm.ORM.query('smscode', {'smskey = %s': keyword})
  return fetch_orm_data(QRY)  

def fetch_report_pregnancy(national_id, preg_start, preg_end):
  QRY = orm.ORM.query('pregnancy', {'national_id = %s': national_id, 'lmp > %s': preg_start, 'lmp < %s': preg_end } , sort=('lmp', False))
  return fetch_record(QRY)

def fetch_birth(national_id, birth_date, child_number):
  QRY = orm.ORM.query('birth', {'national_id = %s': national_id, 'birth_date = %s': birth_date, 'child_number = %s': child_number })
  return fetch_record(QRY)

def fetch_birth_pregnancy(pregnancy_pk):
  QRY = orm.ORM.query('birth', {'pregnancy_pk = %s': pregnancy_pk })
  return fetch_record(QRY)  

def fetch_gravidity(national_id):
  QRY = orm.ORM.query('pregnancy', {'national_id = %s': national_id}, cols = ['COUNT(*) AS gravidity'] )
  records = fetch_record(QRY)
  return records.gravidity

def fetch_parity(national_id):
  QRY = orm.ORM.query('birth', {'national_id = %s': national_id}, cols = ['COUNT(*) AS parity'] )
  records = fetch_record(QRY)
  return records.parity

def fetch_refusal(national_id, created_at):
  QRY = orm.ORM.query('refusal', {'national_id = %s': national_id, 'created_at > %s': created_at } )
  return fetch_record(QRY)

def fetch_mother_departure(national_id, created_at):
  QRY = orm.ORM.query('departure', {'national_id = %s': national_id, 'created_at > %s': created_at } )
  return fetch_record(QRY)

def fetch_child_departure(national_id, birth_date, child_number):
  QRY = orm.ORM.query('departure', {'national_id = %s': national_id, 'birth_date = %s': birth_date, 'child_number = %s': child_number })
  return fetch_record(QRY)

def fetch_ancvisit(national_id, pregnancy_pk, anc_visit):
  QRY = orm.ORM.query('ancvisit', {'national_id = %s': national_id, 'pregnancy_pk = %s': pregnancy_pk, 'anc_visit = %s': anc_visit })
  return fetch_record(QRY)

def fetch_redalert(national_id, filters = {}):
  filters.update({'national_id = %s': national_id})
  QRY = orm.ORM.query('redalert', filters, sort=('created_at', False))
  ##print QRY.query
  return fetch_record(QRY)

def fetch_risk(national_id, filters = {}):
  filters.update({'national_id = %s': national_id})
  QRY = orm.ORM.query('risk', filters, sort=('created_at', False))
  return fetch_record(QRY)

def fetch_redresult(national_id, red_pk, filters = {}):
  filters.update({'red_pk = %s': red_pk, 'national_id = %s': national_id})
  QRY = orm.ORM.query('redresult', filters, sort=('created_at', False))
  ##print QRY.query
  return fetch_record(QRY)

def fetch_riskresult(national_id, risk_pk, filters = {}):
  filters.update({'risk_pk = %s': risk_pk, 'national_id = %s': national_id})
  QRY = orm.ORM.query('riskresult', filters, sort=('created_at', False))
  return fetch_record(QRY)

def fetch_mother_death(national_id, created_at):
  QRY = orm.ORM.query('death', {'national_id = %s': national_id, 'created_at > %s': created_at } )
  return fetch_record(QRY)

def fetch_child_death(national_id, birth_date, child_number):
  QRY = orm.ORM.query('death', {'national_id = %s': national_id, 'birth_date = %s': birth_date, 'child_number = %s': child_number })
  return fetch_record(QRY) 

def fetch_nbcvisit(national_id, birth_date, child_number, nbc_visit):
  QRY = orm.ORM.query('nbcvisit', {'national_id = %s': national_id, 'birth_date = %s': birth_date,
                                   'child_number = %s': child_number, 'lower(nbc_visit) LIKE %s': '%%%s%%' % nbc_visit.lower() })
  return fetch_record(QRY)

def fetch_delivery(national_id, birth_date):
  QRY = orm.ORM.query('birth', {'national_id = %s': national_id, 'birth_date = %s': birth_date })
  return fetch_record(QRY)

def fetch_pncvisit(national_id, delivery_date, pnc_visit):
  QRY = orm.ORM.query('pncvisit', {'national_id = %s': national_id, 'delivery_date = %s': delivery_date,
                                   'lower(pnc_visit) LIKE %s': '%%%s%%' % pnc_visit })
  return fetch_record(QRY)

def fetch_ccm(national_id, filters = {}):
  filters.update({'national_id = %s': national_id})
  QRY = orm.ORM.query('ccm', filters, sort=('created_at', False))
  return fetch_record(QRY)

def fetch_cmr(national_id, filters = {}):
  filters.update({'national_id = %s': national_id})
  QRY = orm.ORM.query('cmr', filters, sort=('created_at', False))
  return fetch_record(QRY)

def fetch_cbn(national_id, filters = {}):
  filters.update({'national_id = %s': national_id})
  QRY = orm.ORM.query('nutrition', filters, sort=('created_at', False))
  ##print QRY.query
  return fetch_record(QRY)

def fetch_chi(national_id, filters = {}):
  filters.update({'national_id = %s': national_id})
  QRY = orm.ORM.query('childhealth', filters, sort=('created_at', False))
  return fetch_record(QRY)

def fetch_sm(national_id, filters = {}):
  filters.update({'national_id = %s': national_id})
  QRY = orm.ORM.query('malaria', filters, sort=('created_at', False))
  return fetch_record(QRY)

def fetch_st(national_id, filters = {}):
  filters.update({'national_id = %s': national_id})
  QRY = orm.ORM.query('stock', filters, sort=('created_at', False))
  return fetch_record(QRY)

def fetch_enderror(user_phone, error_code, created_at):
  filters.update({'user_phone = %s': user_phone, 'error_code = %s': error_code, 'created_at = %s': created_at})
  QRY = orm.ORM.query('enderror', filters)
  return fetch_record(QRY)

def fetch_resources():
  QRY = orm.ORM.query('endresource', {})
  return fetch_record(QRY)

def fetch_resource(code):
  QRY = orm.ORM.query('endresource', {'code = %s': code})
  return fetch_record(QRY)

def fetch_download(user_pk, filename):
  QRY = orm.ORM.query('download', {'user_pk = %s': user_pk, 'filename = %s': filename})
  return fetch_record(QRY)

def fetch_download_by_id(byid):
  QRY = orm.ORM.query('download', {'indexcol = %s': byid})
  return fetch_record(QRY)  

def fetch_smsfield(code, smsreport):
  QRY = orm.ORM.query('smsfield', {'code = %s': code, 'sms_report_pk = %s': smsreport})
  return fetch_record(QRY)

def fetch_smsreport(code):
  QRY = orm.ORM.query('endresource', {'code = %s': code})
  return fetch_record(QRY)

def fetch_active_backend( name = 'kannel-smpp' ):
  QRY = orm.ORM.query('rapidsms_backend', { 'name = %s': name })
  return fetch_record(QRY)

def fetch_active_connection(telephone, backend):
  QRY = orm.ORM.query('rapidsms_connection', {'identity = %s': telephone, 'backend_id = %s': backend.id})
  return fetch_record(QRY)


def fetch_current_pregnancy( national_id, nine_months_ago ):
  QRY = orm.ORM.query('pregnancy', {'national_id = %s' : national_id, 'lmp >= %s' : nine_months_ago } , sort = ('lmp', False) )
  return fetch_record(QRY)
 
def fetch_current_child(national_id, child_number, birth_date ):
  QRY = orm.ORM.query('birth', {'national_id = %s' : national_id, 'child_number = %s': child_number, 'birth_date = %s' : birth_date } )
  return fetch_record(QRY) 

def fetch_current_mother_death( national_id ):
  QRY = orm.ORM.query('death', {'national_id = %s' : national_id , "lower(death_code) LIKE '%%md%%' " : ''}, sort = ('created_at', False))
  return fetch_record(QRY) 

def fetch_current_child_death( national_id, child_number, birth_date ):
  QRY = orm.ORM.query('death', {'national_id = %s' : national_id, 'child_number = %s': child_number, 'birth_date = %s' : birth_date,
                                "lower(death_code) LIKE '%%nd%%' OR lower(death_code) LIKE '%%cd%%' " : ''}, sort = ('created_at', False))
  return fetch_record(QRY)
 
def fetch_current_pregnancy_miscarriage( pregnancy_pk ):
  QRY = orm.ORM.query('death', {'pregnancy_pk = %s' : pregnancy_pk , 
                                "lower(death_code) LIKE '%%mcc%%' OR lower(death_code) LIKE '%%sbd%%' " : ''}, sort = ('created_at', False) )
  an = fetch_record(QRY)
  if not an:
    QRY1 = orm.ORM.query('redalert', {'pregnancy_pk = %s' : pregnancy_pk , 
                                  "lower(red_symptom_mc) LIKE '%%mc%%' " : ''}, sort = ('created_at', False) )
    an = fetch_record(QRY1)
  
  return an

## START FILTERING DATA

def filter_data(table, filters = {}, subs = [], joins = [] , sort = ()):
  if table:
    QRY = orm.ORM.query(table, filters, joins = joins, subs = subs, sort = sort)
    ##print QRY.query
    return fetch_orm_data(QRY)
  return None

def fetch_location_levels(filters = {}):
  QRY = orm.ORM.query('location_level', filters)
  return fetch_orm_data(QRY)

def fetch_villages(filters = {}):
  joins = [
          {'name': ('nation', 'nation_pk')}, {'code' : ('nation', 'nation_pk')},
          {'name': ('province', 'province_pk')}, {'code' : ('province', 'province_pk')},
          {'name': ('district', 'district_pk')}, {'code' : ('district', 'district_pk')},
          {'name': ('sector', 'sector_pk')}, {'code' : ('sector', 'sector_pk')},
          {'name': ('cell', 'cell_pk')}, {'code' : ('cell', 'cell_pk')}
          ]
  #N.B: sometimes the filters has village_pk, which is not in this table
  # then change this to indexcol
  if filters.get('village_pk = %s'):
    filters['indexcol = %s'] = filters['village_pk = %s']
    filters.pop('village_pk = %s') 
  QRY = orm.ORM.query('village', filters, joins = joins)
  ##print QRY.query
  return fetch_orm_data(QRY)

def fetch_cells(filters = {}):
  joins = [
          {'name': ('nation', 'nation_pk')}, {'code' : ('nation', 'nation_pk')},
          {'name': ('province', 'province_pk')}, {'code' : ('province', 'province_pk')},
          {'name': ('district', 'district_pk')}, {'code' : ('district', 'district_pk')},
          {'name': ('sector', 'sector_pk')}, {'code' : ('sector', 'sector_pk')}
          ]
  #N.B: sometimes the filters has village_pk, which is not in this table
  # then change this to indexcol
  if filters.get('cell_pk = %s'):
    filters['indexcol = %s'] = filters['cell_pk = %s']
    filters.pop('cell_pk = %s') 
  QRY = orm.ORM.query('cell', filters, joins = joins)
  ##print QRY.query
  return fetch_orm_data(QRY)


def fetch_sectors(filters = {}):
  joins = [
          {'name': ('nation', 'nation_pk')}, {'code' : ('nation', 'nation_pk')},
          {'name': ('province', 'province_pk')}, {'code' : ('province', 'province_pk')},
          {'name': ('district', 'district_pk')}, {'code' : ('district', 'district_pk')}
          ]
  #N.B: sometimes the filters has village_pk, which is not in this table
  # then change this to indexcol
  if filters.get('sector_pk = %s'):
    filters['indexcol = %s'] = filters['sector_pk = %s']
    filters.pop('sector_pk = %s') 
  QRY = orm.ORM.query('sector', filters, joins = joins)
  ##print QRY.query
  return fetch_orm_data(QRY)


def fetch_districts(filters = {}):
  joins = [
          {'name': ('nation', 'nation_pk')}, {'code' : ('nation', 'nation_pk')},
          {'name': ('province', 'province_pk')}, {'code' : ('province', 'province_pk')},
          ]
  #N.B: sometimes the filters has village_pk, which is not in this table
  # then change this to indexcol
  if filters.get('district_pk = %s'):
    filters['indexcol = %s'] = filters['district_pk = %s']
    filters.pop('district_pk = %s') 
  QRY = orm.ORM.query('district', filters, joins = joins)
  ##print QRY.query
  return fetch_orm_data(QRY)

def fetch_provinces(filters = {}):
  joins = [
          {'name': ('nation', 'nation_pk')}, {'code' : ('nation', 'nation_pk')},
          ]
  #N.B: sometimes the filters has village_pk, which is not in this table
  # then change this to indexcol
  if filters.get('province_pk = %s'):
    filters['indexcol = %s'] = filters['province_pk = %s']
    filters.pop('province_pk = %s') 
  QRY = orm.ORM.query('province', filters, joins = joins)
  ##print QRY.query
  return fetch_orm_data(QRY)

def fetch_facilities(filters = {}):
  #factype = fetch_location_level('HC')
  #filters.update({'facility_type_pk = %s': factype.indexcol})
  subs = [{('name', 'referral'): ('facility', 'referral_facility_pk')}, {('code', 'referral') : ('facility', 'referral_facility_pk')}]
  joins = [
          {'name': ('nation', 'nation_pk')}, {'code' : ('nation', 'nation_pk')},
          {'name': ('province', 'province_pk')}, {'code' : ('province', 'province_pk')},
          {'name': ('district', 'district_pk')}, {'code' : ('district', 'district_pk')},
          {'name': ('sector', 'sector_pk')}, {'code' : ('sector', 'sector_pk')},
          {'name': ('cell', 'cell_pk')}, {'code' : ('cell', 'cell_pk')},
          {'name': ('village', 'village_pk')}, {'code' : ('village', 'village_pk')},
          {'name': ('location_level', 'facility_type_pk')}, {'code' : ('location_level', 'facility_type_pk')}
          ]
  QRY = orm.ORM.query('facility', filters, joins = joins, subs = subs)
  ##print "FACILITIES: ", filters
  ##print QRY.query
  return fetch_orm_data(QRY)

def fetch_referral_facilities(filters = {}):
  factype = fetch_location_level('HD')
  filters.update({'facility_type_pk = %s': factype.indexcol})
  subs = [{('name', 'referral'): ('facility', 'referral_facility_pk')}, {('code', 'referral') : ('facility', 'referral_facility_pk')}]
  joins = [
          {'name': ('nation', 'nation_pk')}, {'code' : ('nation', 'nation_pk')},
          {'name': ('province', 'province_pk')}, {'code' : ('province', 'province_pk')},
          {'name': ('district', 'district_pk')}, {'code' : ('district', 'district_pk')},
          {'name': ('sector', 'sector_pk')}, {'code' : ('sector', 'sector_pk')},
          {'name': ('cell', 'cell_pk')}, {'code' : ('cell', 'cell_pk')},
          {'name': ('village', 'village_pk')}, {'code' : ('village', 'village_pk')},
          {'name': ('location_level', 'facility_type_pk')}, {'code' : ('location_level', 'facility_type_pk')}
          ]
  QRY = orm.ORM.query('facility', filters, joins = joins, subs = subs)
  ##print QRY.query
  return fetch_orm_data(QRY)

def fetch_user(email, passwd):
    them = orm.ORM.query('enduser', {'email = %s': email})
    if them.count() < 1:
      return None
    for him in them.list():
      slt = him['salt']
      shp = sha.sha('%s%s' % (slt, passwd)).hexdigest()
      if shp == him['passwd']:
        filters = {'email = %s': him['email'], 'passwd = %s' : him['passwd'], 'indexcol = %s': him['indexcol']}
        user = fetch_users(filters)
        if user: return user[0]
    return None

def fetch_active_user(telephone):
    filters = {'telephone = %s': telephone, 'is_active': ''}
    user = fetch_users(filters)
    if user: return user[0]
    return None

def fetch_user_by_email(email):
    filters = {'email = %s': email, 'is_active': ''}
    user = fetch_users(filters)
    if user: return user[0]
    return None

def fetch_user_by_nid_phone(national_id, telephone):
    filters = {'telephone = %s': telephone, 'national_id = %s': national_id, 'is_active': ''}
    user = fetch_users(filters)
    if user: return user[0]
    return None


def fetch_users(filters = {}):
  
  joins = [
          {'name': ('nation', 'nation_pk')}, {'code' : ('nation', 'nation_pk')},
          {'name': ('province', 'province_pk')}, {'code' : ('province', 'province_pk')},
          {'name': ('district', 'district_pk')}, {'code' : ('district', 'district_pk')},
          {'name': ('sector', 'sector_pk')}, {'code' : ('sector', 'sector_pk')},
          {'name': ('cell', 'cell_pk')}, {'code' : ('cell', 'cell_pk')},
          {'name': ('village', 'village_pk')}, {'code' : ('village', 'village_pk')},
          {'msin': ('simcard', 'simcard_pk')}, {'msisdn' : ('simcard', 'simcard_pk')},
          {'name': ('gender', 'sex_pk')}, {'code' : ('gender', 'sex_pk')},
          {'name': ('education_level', 'education_level_pk')}, {'code' : ('education_level', 'education_level_pk')},
          {'name': ('language', 'language_pk')}, {'code' : ('language', 'language_pk')},
          {'name': ('role', 'role_pk')}, {'code' : ('role', 'role_pk')},
          {'name': ('location_level', 'location_level_pk')}, {'code' : ('location_level', 'location_level_pk')},
          {'name': ('facility', 'facility_pk')}, {'code' : ('facility', 'facility_pk')},
          #{('name', 'referral') : ('facility', 'referral_facility_pk')}, {('code', 'referral') : ('facility', 'referral_facility_pk')}
          
          ]

  subs = [{('name', 'referral'): ('facility', 'referral_facility_pk')}, {('code', 'referral') : ('facility', 'referral_facility_pk')}]
  QRY = orm.ORM.query('enduser', filters, cols = ['indexcol', 'created_at', 'updated_at', 'simcard_pk', 'telephone', 'national_id', 'surname', 'given_name', 'date_of_birth', 'sex_pk', 'education_level_pk', 'language_pk', 'join_date', 'email', 'role_pk', 'location_level_pk', 'nation_pk', 'province_pk', 'district_pk', 'referral_facility_pk', 'facility_pk', 'sector_pk', 'cell_pk', 'village_pk', 'last_seen', 'is_active', 'is_correct'], joins = joins, subs = subs)
  ##print QRY.query
  return fetch_orm_data(QRY)


def fetch_summary(table, cnds, cols, exts):
  cnds.update({'is_valid': ""})
  QRY = orm.ORM.query( table, cnds, cols = cols, extended = exts )
  ##print QRY.query
  return fetch_orm_data(QRY)

def fetch_users_summary(table, cnds, cols, exts):
  QRY = orm.ORM.query( table, cnds, cols = cols, extended = exts )
  ##print QRY.query
  return fetch_orm_data(QRY)

def fetch_table(table, cnds, cols):
  cnds.update({'is_valid': ""})
  subs = [{('name', 'referral'): ('facility', 'referral_facility_pk')}, {('code', 'referral') : ('facility', 'referral_facility_pk')}]
  joins = [
          {'name': ('nation', 'nation_pk')}, {'code' : ('nation', 'nation_pk')},
          {'name': ('province', 'province_pk')}, {'code' : ('province', 'province_pk')},
          {'name': ('district', 'district_pk')}, {'code' : ('district', 'district_pk')},
          {'name': ('sector', 'sector_pk')}, {'code' : ('sector', 'sector_pk')},
          {'name': ('cell', 'cell_pk')}, {'code' : ('cell', 'cell_pk')},
          {'name': ('village', 'village_pk')}, {'code' : ('village', 'village_pk')},
          #{'msin': ('simcard', 'simcard_pk')}, {'msisdn' : ('simcard', 'simcard_pk')},
          #{'name': ('gender', 'sex_pk')}, {'code' : ('gender', 'sex_pk')},
          #{'name': ('education_level', 'education_level_pk')}, {'code' : ('education_level', 'education_level_pk')},
          #{'name': ('language', 'language_pk')}, {'code' : ('language', 'language_pk')},
          #{'name': ('role', 'role_pk')}, {'code' : ('role', 'role_pk')},
          #{'name': ('location_level', 'location_level_pk')}, {'code' : ('location_level', 'location_level_pk')},
          {'name': ('facility', 'facility_pk')}, {'code' : ('facility', 'facility_pk')},
          #{('name', 'referral') : ('facility', 'referral_facility_pk')}, {('code', 'referral') : ('facility', 'referral_facility_pk')}
          
          ]
  QRY = orm.ORM.query( table, cnds, cols = cols, joins = joins, subs = subs, sort=('created_at', False))
  ##print QRY.query
  #return fetch_orm_data(QRY)
  return QRY


def fetch_table_users(table, cnds, cols):
  
  joins = [
          {'name': ('nation', 'nation_pk')}, {'code' : ('nation', 'nation_pk')},
          {'name': ('province', 'province_pk')}, {'code' : ('province', 'province_pk')},
          {'name': ('district', 'district_pk')}, {'code' : ('district', 'district_pk')},
          {'name': ('sector', 'sector_pk')}, {'code' : ('sector', 'sector_pk')},
          {'name': ('cell', 'cell_pk')}, {'code' : ('cell', 'cell_pk')},
          {'name': ('village', 'village_pk')}, {'code' : ('village', 'village_pk')},
          {'msin': ('simcard', 'simcard_pk')}, {'msisdn' : ('simcard', 'simcard_pk')},
          {'name': ('gender', 'sex_pk')}, {'code' : ('gender', 'sex_pk')},
          {'name': ('education_level', 'education_level_pk')}, {'code' : ('education_level', 'education_level_pk')},
          {'name': ('language', 'language_pk')}, {'code' : ('language', 'language_pk')},
          {'name': ('role', 'role_pk')}, {'code' : ('role', 'role_pk')},
          {'name': ('location_level', 'location_level_pk')}, {'code' : ('location_level', 'location_level_pk')},
          {'name': ('facility', 'facility_pk')}, {'code' : ('facility', 'facility_pk')},
          #{('name', 'referral') : ('facility', 'referral_facility_pk')}, {('code', 'referral') : ('facility', 'referral_facility_pk')}
          
          ]

  subs = [{('name', 'referral'): ('facility', 'referral_facility_pk')}, {('code', 'referral') : ('facility', 'referral_facility_pk')}]
  QRY = orm.ORM.query('enduser', cnds, cols = ['indexcol', 'created_at', 'updated_at', 'simcard_pk', 'telephone', 'national_id', 'surname', 'given_name', 'date_of_birth', 'sex_pk', 'education_level_pk', 'language_pk', 'join_date', 'email', 'role_pk', 'location_level_pk', 'nation_pk', 'province_pk', 'district_pk', 'referral_facility_pk', 'facility_pk', 'sector_pk', 'cell_pk', 'village_pk', 'last_seen', 'is_active', 'is_correct'], joins = joins, subs = subs)
  ##print QRY.query
  return QRY


def fetch_table_by_location(table, cnds, cols, group_by):
  cnds.update({'is_valid': ""})
  subs = []
  if 'province_pk' in group_by: subs += [{"name": ('province', 'province_pk')}]
  if 'district_pk' in group_by: subs += [{"name": ('district', 'district_pk')}]
  if 'referral_facility_pk' in group_by: subs += [{("name", "referral_facility"): ('facility', 'referral_facility_pk')}]
  if 'facility_pk' in group_by: subs += [{"name": ('facility', 'facility_pk')}]
  QRY = orm.ORM.query( table, cnds, cols = cols, subs = subs, group_by = group_by )
  ##print QRY.query
  return fetch_orm_data(QRY)


def fetch_location(type_code, pk):
  if type_code == 'NATION': return fetch_record(orm.ORM.query('nation', {'indexcol = %s' : pk })) 
  if type_code == 'PRV': return fetch_record(orm.ORM.query('province', {'indexcol = %s' : pk })) 
  if type_code == 'DST': return fetch_record(orm.ORM.query('district', {'indexcol = %s' : pk })) 
  if type_code == 'NRH': return fetch_record(orm.ORM.query('facility', {'indexcol = %s' : pk })) 
  if type_code == 'MH': return fetch_record(orm.ORM.query('facility', {'indexcol = %s' : pk })) 
  if type_code == 'HD': return fetch_record(orm.ORM.query('facility', {'indexcol = %s' : pk })) 
  if type_code == 'HP': return fetch_record(orm.ORM.query('facility', {'indexcol = %s' : pk })) 
  if type_code == 'HC': return fetch_record(orm.ORM.query('facility', {'indexcol = %s' : pk })) 
  if type_code == 'CL': return fetch_record(orm.ORM.query('facility', {'indexcol = %s' : pk })) 
  if type_code == 'SEC': return fetch_record(orm.ORM.query('sector', {'indexcol = %s' : pk }))
  if type_code == 'CEL': return fetch_record(orm.ORM.query('cell', {'indexcol = %s' : pk })) 
  if type_code == 'VIL': return fetch_record(orm.ORM.query('village', {'indexcol = %s' : pk }))
  return None


def fetch_users_per_level(level_code = None, pk = None, chw = None):
  filters = {}
  level = fetch_location_level(level_code)
  if not pk and level: return fetch_users(filters = {"location_level_pk = %s": level.indexcol })
  if level_code == 'NATION' and level:
    return fetch_users(filters = {'nation_pk = %s': pk, "location_level_pk = %s": level.indexcol }) 
  if level_code == 'PRV' and level:
    return fetch_users(filters = {'province_pk = %s': pk, "location_level_pk = %s": level.indexcol }) 
  if level_code == 'DST' and level:
    return fetch_users(filters = {'district_pk = %s': pk, "location_level_pk = %s": level.indexcol }) 
  if level_code == 'NRH' and level:
    return fetch_users(filters = {'facility_pk = %s': pk, "location_level_pk = %s": level.indexcol }) 
  if level_code == 'MH' and level:
    return fetch_users(filters = {'facility_pk = %s': pk, "location_level_pk = %s": level.indexcol }) 
  if level_code == 'HD' and level:
    return fetch_users(filters = {'facility_pk = %s': pk, "location_level_pk = %s": level.indexcol }) 
  if level_code == 'HP' and level:
    return fetch_users(filters = {'facility_pk = %s': pk, "location_level_pk = %s": level.indexcol }) 
  if level_code == 'HC' and level:
    return fetch_users(filters = {'facility_pk = %s': pk, "location_level_pk = %s": level.indexcol }) 
  if level_code == 'CL' and level:
    return fetch_users(filters = {'facility_pk = %s': pk, "location_level_pk = %s": level.indexcol }) 
  if level_code == 'SEC' and level:
    return fetch_users(filters = {'sector_pk = %s': pk, "location_level_pk = %s": level.indexcol })
  if level_code == 'CEL' and level:
    return fetch_users(filters = {'cell_pk = %s': pk, "location_level_pk = %s": level.indexcol }) 
  if level_code == 'VIL' and level:
    return fetch_users(filters = {'village_pk = %s': pk, "location_level_pk = %s": level.indexcol })
  return chw


def fetch_users_per_level_and_role(level_code = None, role_code = None, pk = None, chw = None):
  filters = {}
  level = fetch_location_level(level_code)
  role  = fetch_role(role_code)
  if not pk and level and role: return fetch_users(filters = {"location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol })
  if level_code == 'NATION' and level:
    return fetch_users(filters = {'nation_pk = %s': pk, "location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol }) 
  if level_code == 'PRV' and level:
    return fetch_users(filters = {'province_pk = %s': pk, "location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol }) 
  if level_code == 'DST' and level:
    return fetch_users(filters = {'district_pk = %s': pk, "location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol }) 
  if level_code == 'NRH' and level:
    return fetch_users(filters = {'facility_pk = %s': pk, "location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol }) 
  if level_code == 'MH' and level:
    return fetch_users(filters = {'facility_pk = %s': pk, "location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol }) 
  if level_code == 'HD' and level:
    return fetch_users(filters = {'referral_facility_pk = %s': pk, "location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol }) 
  if level_code == 'HP' and level:
    return fetch_users(filters = {'facility_pk = %s': pk, "location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol }) 
  if level_code == 'HC' and level:
    return fetch_users(filters = {'facility_pk = %s': pk, "location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol }) 
  if level_code == 'CL' and level:
    return fetch_users(filters = {'facility_pk = %s': pk, "location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol }) 
  if level_code == 'SEC' and level:
    return fetch_users(filters = {'sector_pk = %s': pk, "location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol })
  if level_code == 'CEL' and level:
    return fetch_users(filters = {'cell_pk = %s': pk, "location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol }) 
  if level_code == 'VIL' and level:
    return fetch_users(filters = {'village_pk = %s': pk, "location_level_pk = %s": level.indexcol, "role_pk = %s" : role.indexcol })
  return chw


def migrate(table, fields):
  try:
    orm.ORM.postgres.rollback()
    p = orm.ORM.store(table, fields)
    orm.ORM.postgres.commit()
    ##print "TABLE: ", table, p
    return True
  except Exception, e:
    #print e
    orm.ORM.postgres.rollback()
    orm.ORM.postgres.commit()
  return False



def fetch_db_record(table, indexcol):
  cols = orm.ORM.fetch_columns(table)#; #print cols
  subs = joins = []
  if 'referral_facility_pk' in cols:
    subs = [{('name', 'referral_facility'): ('facility', 'referral_facility_pk')},
             {('code', 'referral_facility') : ('facility', 'referral_facility_pk')}]
  if 'user_pk' in cols:
    joins.append({'surname': ('enduser', 'user_pk')})
    joins.append({'given_name' : ('enduser', 'user_pk')})
  if 'nation_pk' in cols:
    joins.append({'name': ('nation', 'nation_pk')})
    joins.append({'code' : ('nation', 'nation_pk')})
  if 'province_pk' in cols:
    joins.append({'name': ('province', 'province_pk')})
    joins.append({'code' : ('province', 'province_pk')})
  if 'district_pk' in cols:
    joins.append({'name': ('district', 'district_pk')})
    joins.append({'code' : ('district', 'district_pk')})
  if 'sector_pk' in cols:
    joins.append({'name': ('sector', 'sector_pk')})
    joins.append({'code' : ('sector', 'sector_pk')})
  if 'cell_pk' in cols:
    joins.append({'name': ('cell', 'cell_pk')})
    joins.append({'code' : ('cell', 'cell_pk')})
  if 'village_pk' in cols:
    joins.append({'name': ('village', 'village_pk')})
    joins.append({'code' : ('village', 'village_pk')})
  if 'simcard_pk' in cols:
    joins.append({'msin': ('simcard', 'simcard_pk')})
    joins.append({'msisdn' : ('simcard', 'simcard_pk')})
  if 'sex_pk' in cols or 'gender_pk' in cols:
    joins.append({'name': ('gender', 'sex_pk')})
    joins.append({'code' : ('gender', 'sex_pk')})
  if 'education_level_pk' in cols:
    joins.append({'name': ('education_level', 'education_level_pk')})
    joins.append({'code' : ('education_level', 'education_level_pk')})
  if 'language_pk' in cols:
    joins.append({'name': ('language', 'language_pk')})
    joins.append({'code' : ('language', 'language_pk')})
  if 'role_pk' in cols:
    joins.append({'name': ('role', 'role_pk')})
    joins.append({'code' : ('role', 'role_pk')})
  if 'location_level_pk' in cols:
    joins.append({'name': ('location_level', 'location_level_pk')})
    joins.append({'code' : ('location_level', 'location_level_pk')})
  if 'facility_pk' in cols:
    joins.append({'name': ('facility', 'facility_pk')})
    joins.append({'code' : ('facility', 'facility_pk')})          
          
  QRY = orm.ORM.query( table, {'indexcol = %s': indexcol}, cols = cols, joins = joins, subs = subs )
  rcd = fetch_orm_data(QRY)[0]
  return rcd


def fetch_table_cols(table, filters, cols = []):
  QRY = orm.ORM.query( table, filters, cols = cols )
  ##print QRY.query
  return fetch_orm_data(QRY)

def fetch_table_cols_qry(table, filters, cols = []):
  QRY = orm.ORM.query( table, filters, cols = cols )
  ##print QRY.query
  return QRY

def fetch_facility_table(table, filters, cols):
  subs = [{('name', 'referral'): ('facility', 'referral_facility_pk')}, {('code', 'referral') : ('facility', 'referral_facility_pk')}]
  joins = [
          {'name': ('nation', 'nation_pk')}, {'code' : ('nation', 'nation_pk')},
          {'name': ('province', 'province_pk')}, {'code' : ('province', 'province_pk')},
          {'name': ('district', 'district_pk')}, {'code' : ('district', 'district_pk')},
          {'name': ('sector', 'sector_pk')}, {'code' : ('sector', 'sector_pk')},
          {'name': ('cell', 'cell_pk')}, {'code' : ('cell', 'cell_pk')},
          {'name': ('village', 'village_pk')}, {'code' : ('village', 'village_pk')},
          {'name': ('location_level', 'facility_type_pk')}, {'code' : ('location_level', 'facility_type_pk')}
          ]
  QRY = orm.ORM.query(table, filters, joins = joins, subs = subs)
  ##print QRY.query
  return QRY


def fetch_user_reports(start, end, user):
  #DUMMY IT FIRST
  QRY = orm.ORM.query('refusal')
  QRY.query = """

              SELECT created_at, message FROM pregnancy WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM ancvisit WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM departure WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM refusal WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM risk WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM riskresult WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM redalert WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM redresult WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM birth WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM nbcvisit WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM pncvisit WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM ccm WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM cmr WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM nutrition WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM childhealth WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM malaria WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM stock WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s
              UNION
              SELECT created_at, message FROM death WHERE created_at >= '%(start)s' AND created_at <= '%(end)s' AND user_pk = %(user)s

              """ % {'start': start, 'end': end, 'user': user.indexcol}
  return QRY


def fetch_users_performance(filters):

  PRE   = orm.ORM.query('pregnancy', filters, cols = ['user_pk', 'COUNT(*) AS pre'], group_by = ['user_pk'])
  ANC   = orm.ORM.query('ancvisit', filters, cols = ['user_pk', 'COUNT(*) AS anc'], group_by = ['user_pk'])
  DEP   = orm.ORM.query('departure', filters, cols = ['user_pk', 'COUNT(*) AS dep'], group_by = ['user_pk'])
  REF   = orm.ORM.query('refusal', filters, cols = ['user_pk', 'COUNT(*) AS ref'], group_by = ['user_pk'])
  RISK  = orm.ORM.query('risk', filters, cols = ['user_pk', 'COUNT(*) AS risk'], group_by = ['user_pk'])
  RES   = orm.ORM.query('riskresult', filters, cols = ['user_pk', 'COUNT(*) AS res'], group_by = ['user_pk'])
  RED   = orm.ORM.query('redalert', filters, cols = ['user_pk', 'COUNT(*) AS red'], group_by = ['user_pk'])
  RAR   = orm.ORM.query('redresult', filters, cols = ['user_pk', 'COUNT(*) AS rar'], group_by = ['user_pk'])
  BIR   = orm.ORM.query('birth', filters, cols = ['user_pk', 'COUNT(*) AS bir'], group_by = ['user_pk'])
  NBC   = orm.ORM.query('nbcvisit', filters, cols = ['user_pk', 'COUNT(*) AS nbc'], group_by = ['user_pk'])
  PNC   = orm.ORM.query('pncvisit', filters, cols = ['user_pk', 'COUNT(*) AS pnc'], group_by = ['user_pk'])
  CCM   = orm.ORM.query('ccm', filters, cols = ['user_pk', 'COUNT(*) AS ccm'], group_by = ['user_pk'])
  CMR   = orm.ORM.query('cmr', filters, cols = ['user_pk', 'COUNT(*) AS cmr'], group_by = ['user_pk'])
  CBN   = orm.ORM.query('nutrition', filters, cols = ['user_pk', 'COUNT(*) AS cbn'], group_by = ['user_pk'])
  CHI   = orm.ORM.query('childhealth', filters, cols = ['user_pk', 'COUNT(*) AS chi'], group_by = ['user_pk'])

  smn_filters = {'lower(keyword) = %s': 'smn'}
  smn_filters.update(filters)
  SMN   = orm.ORM.query('malaria', smn_filters, cols = ['user_pk', 'COUNT(*) AS smn'], group_by = ['user_pk'])
  smr_filters = {'lower(keyword) = %s': 'smr'}
  smr_filters.update(filters)
  SMR   = orm.ORM.query('malaria', smr_filters, cols = ['user_pk', 'COUNT(*) AS smr'], group_by = ['user_pk'])
  rso_filters = {'lower(keyword) = %s': 'rso'}
  rso_filters.update(filters)
  RSO   = orm.ORM.query('stock', rso_filters, cols = ['user_pk', 'COUNT(*) AS rso'], group_by = ['user_pk'])
  so_filters = {'lower(keyword) = %s': 'so'}
  so_filters.update(filters)
  SO    = orm.ORM.query('stock', so_filters, cols = ['user_pk', 'COUNT(*) AS so'], group_by = ['user_pk'])
  ss_filters = {'lower(keyword) = %s': 'ss'}
  ss_filters.update(filters)
  SS    = orm.ORM.query('stock', ss_filters, cols = ['user_pk', 'COUNT(*) AS ss'], group_by = ['user_pk'])

  DTH   = orm.ORM.query('death', filters, cols = ['user_pk', 'COUNT(*) AS dth'], group_by = ['user_pk'])
  ##print filters
  
  ans = [ fetch_orm_data(PRE)   +  
          fetch_orm_data(ANC)   +
          fetch_orm_data(DEP)   +
          fetch_orm_data(REF)   +
          fetch_orm_data(RISK)  +
          fetch_orm_data(RES)   +
          fetch_orm_data(RED)   +
          fetch_orm_data(RAR)   +
          fetch_orm_data(BIR)   + 
          fetch_orm_data(NBC)   + 
          fetch_orm_data(PNC)   +
          fetch_orm_data(CCM)   + 
          fetch_orm_data(CMR)   + 
          fetch_orm_data(CBN)   + 
          fetch_orm_data(CHI)   + 
          fetch_orm_data(SMN)   + 
          fetch_orm_data(SMR)   + 
          fetch_orm_data(RSO)   + 
          fetch_orm_data(SO)    + 
          fetch_orm_data(SS)    + 
          fetch_orm_data(DTH)
        ]

  if ans: ans = ans[0]

  return ans

def fetch_users_performance_per_role(filters):

  PRE   = orm.ORM.query('pregnancy', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS pre'], group_by = ['role_pk',  'user_pk '])
  ANC   = orm.ORM.query('ancvisit', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS anc'], group_by = ['role_pk',  'user_pk '])
  DEP   = orm.ORM.query('departure', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS dep'], group_by = ['role_pk',  'user_pk '])
  REF   = orm.ORM.query('refusal', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS ref'], group_by = ['role_pk',  'user_pk '])
  RISK  = orm.ORM.query('risk', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS risk'], group_by = ['role_pk',  'user_pk '])
  RES   = orm.ORM.query('riskresult', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS res'], group_by = ['role_pk',  'user_pk '])
  RED   = orm.ORM.query('redalert', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS red'], group_by = ['role_pk',  'user_pk '])
  RAR   = orm.ORM.query('redresult', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS rar'], group_by = ['role_pk',  'user_pk '])
  BIR   = orm.ORM.query('birth', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS bir'], group_by = ['role_pk',  'user_pk '])
  NBC   = orm.ORM.query('nbcvisit', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS nbc'], group_by = ['role_pk',  'user_pk '])
  PNC   = orm.ORM.query('pncvisit', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS pnc'], group_by = ['role_pk',  'user_pk '])
  CCM   = orm.ORM.query('ccm', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS ccm'], group_by = ['role_pk',  'user_pk '])
  CMR   = orm.ORM.query('cmr', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS cmr'], group_by = ['role_pk',  'user_pk '])
  CBN   = orm.ORM.query('nutrition', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS cbn'], group_by = ['role_pk',  'user_pk '])
  CHI   = orm.ORM.query('childhealth', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS chi'], group_by = ['role_pk',  'user_pk '])

  smn_filters = {'lower(keyword) = %s': 'smn'}
  smn_filters.update(filters)
  SMN   = orm.ORM.query('malaria', smn_filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS smn'], group_by = ['role_pk',  'user_pk '])
  smr_filters = {'lower(keyword) = %s': 'smr'}
  smr_filters.update(filters)
  SMR   = orm.ORM.query('malaria', smr_filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS smr'], group_by = ['role_pk',  'user_pk '])
  rso_filters = {'lower(keyword) = %s': 'rso'}
  rso_filters.update(filters)
  RSO   = orm.ORM.query('stock', rso_filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS rso'], group_by = ['role_pk',  'user_pk '])
  so_filters = {'lower(keyword) = %s': 'so'}
  so_filters.update(filters)
  SO    = orm.ORM.query('stock', so_filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS so'], group_by = ['role_pk',  'user_pk '])
  ss_filters = {'lower(keyword) = %s': 'ss'}
  ss_filters.update(filters)
  SS    = orm.ORM.query('stock', ss_filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS ss'], group_by = ['role_pk',  'user_pk '])

  DTH   = orm.ORM.query('death', filters, cols = ['role_pk',  'user_pk ', 'COUNT(*) AS dth'], group_by = ['role_pk',  'user_pk '])
  ##print filters
  
  ans = [ fetch_orm_data(PRE)   +  
          fetch_orm_data(ANC)   +
          fetch_orm_data(DEP)   +
          fetch_orm_data(REF)   +
          fetch_orm_data(RISK)  +
          fetch_orm_data(RES)   +
          fetch_orm_data(RED)   +
          fetch_orm_data(RAR)   +
          fetch_orm_data(BIR)   + 
          fetch_orm_data(NBC)   + 
          fetch_orm_data(PNC)   +
          fetch_orm_data(CCM)   + 
          fetch_orm_data(CMR)   + 
          fetch_orm_data(CBN)   + 
          fetch_orm_data(CHI)   + 
          fetch_orm_data(SMN)   + 
          fetch_orm_data(SMR)   + 
          fetch_orm_data(RSO)   + 
          fetch_orm_data(SO)    + 
          fetch_orm_data(SS)    + 
          fetch_orm_data(DTH)
        ]

  if ans: ans = ans[0]

  return ans


def fetch_seen_users(filters):
  """from util.record import *
from underscore import _ as UNDERSCORE
import datetime
end  = datetime.date.today() 
start = end - datetime.timedelta(days = 360)
filters = {'created_at >= %s': start, 'created_at <= %s': end}
users = fetch_users()
headers, records = map_users_performance(users, filters)
ans = fetch_users_performance(filters)
user = fetch_active_user('+250788660270')
filters = {'created_at >= %s': start, 'created_at <= %s': end}
nat = fetch_user_reports(start, end, user)
users = fetch_users()
seens = UNDERSCORE(ans).chain().indexBy(lambda x, *args: x.user_pk).map(lambda x, *args: x.user_pk).sortBy().value()"""

  return


def map_users_performance(users, filters):
  from underscore import _ as UNDERSCORE
  ans = fetch_users_performance(filters)
  headers  = [ 'surname', 'given_name', 'telephone', 'date_of_birth', 'national_id', 'role_name', 'location_level_name', 'email', 'province_name', 'district_name', 'referral_name',  'facility_name', 'sector_name', 'cell_name', 'village_name', 'pre', 'anc', 'dep', 'ref', 'risk', 'res', 'red', 'rar']
  
  for r in users:
    set_report_count('pre', r,
         UNDERSCORE(ans).chain().filter(lambda x, *args: x.user_pk == r.indexcol and hasattr(x, 'pre')).map(lambda x, *args: x).sortBy().value()
        )
    set_report_count('anc', r,
         UNDERSCORE(ans).chain().filter(lambda x, *args: x.user_pk == r.indexcol and hasattr(x, 'anc')).map(lambda x, *args: x).sortBy().value()
         )
    set_report_count('dep', r,
         UNDERSCORE(ans).chain().filter(lambda x, *args: x.user_pk == r.indexcol and hasattr(x, 'dep')).map(lambda x, *args: x).sortBy().value()
         )
    set_report_count('ref', r,
         UNDERSCORE(ans).chain().filter(lambda x, *args: x.user_pk == r.indexcol and hasattr(x, 'ref')).map(lambda x, *args: x).sortBy().value()
         )
    set_report_count('risk', r,
         UNDERSCORE(ans).chain().filter(lambda x, *args: x.user_pk == r.indexcol and hasattr(x, 'risk')).map(lambda x, *args: x).sortBy().value()
         )
    set_report_count('res', r,
         UNDERSCORE(ans).chain().filter(lambda x, *args: x.user_pk == r.indexcol and hasattr(x, 'res')).map(lambda x, *args: x).sortBy().value()
         )
    set_report_count('red', r,
         UNDERSCORE(ans).chain().filter(lambda x, *args: x.user_pk == r.indexcol and hasattr(x, 'red')).map(lambda x, *args: x).sortBy().value()
         )
    set_report_count('rar', r,
         UNDERSCORE(ans).chain().filter(lambda x, *args: x.user_pk == r.indexcol and hasattr(x, 'rar')).map(lambda x, *args: x).sortBy().value()
         )
     
  return headers, users

def set_report_count(header, record, an):
  try:
    if len(an) > 0: setattr( record, header, getattr(an[0], header) )
    else: setattr( record, header, 0 )
  except Exception, e:
    try:  setattr( record, header, 0 )
    except Exception, ex: pass    
    pass 
  return True


def fetch_reporting_users(filters):
  """ We based on reports loading, but later we should base on last seen for userdash page """

  active_asm      = []
  active_binome   = []
  inactive_asm    = []
  inactive_binome = []
  
  return active_asm, active_binome, inactive_asm, inactive_binome


def update_reports_with_role():
  users = fetch_users()
  for user in users:
    QRY = orm.ORM.query('refusal', {'user_pk = %s': user.indexcol})
    QRY.query = """

              SELECT indexcol, 'pregnancy' AS tablename FROM pregnancy WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'ancvisit' AS tablename FROM ancvisit WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'departure' AS tablename FROM departure WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'refusal' AS tablename FROM refusal WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'risk' AS tablename FROM risk WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'riskresult' AS tablename FROM riskresult WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'redalert' AS tablename FROM redalert WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'redresult' AS tablename FROM redresult WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'birth' AS tablename FROM birth WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'nbcvisit' AS tablename FROM nbcvisit WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'pncvisit' AS tablename FROM pncvisit WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'ccm' AS tablename FROM ccm WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'cmr' AS tablename FROM cmr WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'nutrition' AS tablename FROM nutrition WHERE user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'childhealth' AS tablename FROM childhealth WHERE  user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'malaria' AS tablename FROM malaria WHERE  user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'stock' AS tablename FROM stock WHERE  user_pk = %(user)s AND role_pk IS NULL
              UNION
              SELECT indexcol, 'death' AS tablename FROM death WHERE user_pk = %(user)s AND role_pk IS NULL

              """ % {'user': user.indexcol}

    ans = fetch_orm_data(QRY)
    
    for an in ans:
      migrate(an.tablename, {'indexcol': an.indexcol, 'role_pk': user.role_pk})


def update_15_days_ago_reports_with_role():
  """ Just update 15 days reports with role_pk """
  today = datetime.datetime.now()
  days_15_ago = today - datetime.timedelta(days = 15)
  QRY = orm.ORM.query('refusal', {'user_pk = %s': 1})
  QRY.query = """

            SELECT pregnancy.indexcol, 
                  (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = pregnancy.user_pk) AS role, 'pregnancy' AS tablename 
                  FROM pregnancy WHERE pregnancy.created_at >= '%(days_15_ago)s' AND pregnancy.role_pk IS NULL
            UNION
            SELECT ancvisit.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = ancvisit.user_pk) AS role, 'ancvisit' AS tablename  
                  FROM ancvisit WHERE ancvisit.created_at >= '%(days_15_ago)s' AND ancvisit.role_pk IS NULL
            UNION
            SELECT departure.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = departure.user_pk) AS role, 'departure' AS tablename  
                  FROM departure WHERE departure.created_at >= '%(days_15_ago)s' AND departure.role_pk IS NULL
            UNION
            SELECT refusal.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = refusal.user_pk) AS role, 'refusal' AS tablename  
                  FROM refusal WHERE refusal.created_at >= '%(days_15_ago)s' AND refusal.role_pk IS NULL
            UNION
            SELECT risk.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = risk.user_pk) AS role, 'risk' AS tablename  
                  FROM risk WHERE risk.created_at >= '%(days_15_ago)s' AND risk.role_pk IS NULL
            UNION
            SELECT riskresult.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = riskresult.user_pk) AS role, 'riskresult' AS tablename  
                  FROM riskresult WHERE riskresult.created_at >= '%(days_15_ago)s' AND riskresult.role_pk IS NULL
            UNION
            SELECT redalert.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = redalert.user_pk) AS role, 'redalert' AS tablename  
                  FROM redalert WHERE redalert.created_at >= '%(days_15_ago)s' AND redalert.role_pk IS NULL
            UNION
            SELECT redresult.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = redresult.user_pk) AS role, 'redresult' AS tablename  
                  FROM redresult WHERE redresult.created_at >= '%(days_15_ago)s' AND redresult.role_pk IS NULL
            UNION
            SELECT birth.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = birth.user_pk) AS role, 'birth' AS tablename  
                  FROM birth WHERE birth.created_at >= '%(days_15_ago)s' AND birth.role_pk IS NULL
            UNION
            SELECT nbcvisit.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = nbcvisit.user_pk) AS role, 'nbcvisit' AS tablename  
                  FROM nbcvisit WHERE nbcvisit.created_at >= '%(days_15_ago)s' AND nbcvisit.role_pk IS NULL
            UNION
            SELECT pncvisit.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = pncvisit.user_pk) AS role, 'pncvisit' AS tablename  
                  FROM pncvisit WHERE pncvisit.created_at >= '%(days_15_ago)s' AND pncvisit.role_pk IS NULL
            UNION
            SELECT ccm.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = ccm.user_pk) AS role, 'ccm' AS tablename  
                  FROM ccm WHERE ccm.created_at >= '%(days_15_ago)s' AND ccm.role_pk IS NULL
            UNION
            SELECT cmr.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = cmr.user_pk) AS role, 'cmr' AS tablename  
                  FROM cmr WHERE cmr.created_at >= '%(days_15_ago)s' AND cmr.role_pk IS NULL
            UNION
            SELECT nutrition.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = nutrition.user_pk) AS role, 'nutrition' AS tablename  
                  FROM nutrition WHERE nutrition.created_at >= '%(days_15_ago)s' AND nutrition.role_pk IS NULL
            UNION
            SELECT childhealth.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = childhealth.user_pk) AS role, 'childhealth' AS tablename  
                  FROM childhealth WHERE childhealth.created_at >= '%(days_15_ago)s' AND childhealth.role_pk IS NULL
            UNION
            SELECT malaria.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = malaria.user_pk) AS role, 'malaria' AS tablename  
                  FROM malaria WHERE malaria.created_at >= '%(days_15_ago)s' AND malaria.role_pk IS NULL
            UNION
            SELECT stock.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = stock.user_pk) AS role, 'stock' AS tablename  
                  FROM stock WHERE stock.created_at >= '%(days_15_ago)s' AND stock.role_pk IS NULL
            UNION
            SELECT death.indexcol, 
                   (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = death.user_pk) AS role, 'death' AS tablename  
                  FROM death WHERE death.created_at >= '%(days_15_ago)s' AND death.role_pk IS NULL

            """ % {'days_15_ago': days_15_ago} 

  ans = fetch_orm_data(QRY)
    
  for an in ans:
    migrate(an.tablename, {'indexcol': an.indexcol, 'role_pk': an.role})

  return ans


