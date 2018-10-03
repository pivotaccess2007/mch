#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

import os.path

from decimal import *
from decimal import Decimal
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
import locale
import os
import types
import json
import re
from util.record import *
import random
from xlrd import open_workbook ,cellname,XL_CELL_NUMBER,XLRDError, xldate_as_tuple
from model.enduser import Enduser
import datetime
from underscore import _ as UNDERSCORE
from util import queries
import xlsxwriter


class MchUtil:
    
    @staticmethod
    def checkFileExistence(path):
        return os.path.exists(path)

    @staticmethod
    def getRatingWeight(configs, rating):

        for record in configs:
            if(record.gf_rating == rating):
                return record.rating_weight

        return None

    @staticmethod
    def mchHtmlEscape(html):
        """
        Escapes the string to it's correct html code, for display on fusion charts
        """
        s = mark_safe(force_unicode(html).replace('&', '%26amp;').replace('<', '%26lt;').replace('>', '%26gt;').replace('"', '%26quot;').replace("'", '%26apos;'))

        return mark_safe(s).encode('ascii', 'xmlcharrefreplace')

    @staticmethod
    def numberFormat(num, places=0):
        """Format a number according to locality and given places"""
        locale.setlocale(locale.LC_ALL, locale.getdefaultlocale()[0] + '.' + locale.getdefaultlocale()[1])
        return locale.format("%.*f", (places, num), 1)

def json_encode(data):
    """
    The main issues with django's default json serializer is that properties that
    had been added to a object dynamically are being ignored (and it also has
    problems with some models).
    """

    from django.db import models
    from django.utils import simplejson as json
    from django.core.serializers.json import DateTimeAwareJSONEncoder

    def _any(data):
        ret = None
        if type(data) is types.ListType:
            ret = _list(data)
        elif type(data) is types.DictType:
            ret = _dict(data)
        elif isinstance(data, Decimal):
            # json.dumps() cant handle Decimal
            ret = str(data)
        elif isinstance(data, models.query.QuerySet):
            # Actually its the same as a list ...
            ret = _list(data)
        elif isinstance(data, models.Model):
            ret = _model(data)
        else:
            ret = data
        return ret

    def _model(data):
        ret = {}
        # If we only have a model, we only want to encode the fields.
        for f in data._meta.fields:
            ret[f.attname] = _any(getattr(data, f.attname))
        # And additionally encode arbitrary properties that had been added.
        #fields = dir(data.__class__) + ret.keys()
        #add_ons = [k for k in dir(data) if k not in fields]
        #for k in add_ons:
            #ret[k] = _any(getattr(data, k))
        return ret

    def _list(data):
        ret = []
        for v in data:
            ret.append(_any(v))
        return ret

    def _dict(data):
        ret = {}
        for k, v in data.items():
            ret[k] = _any(v)
        return ret

    ret = _any(data)

    return json.dumps(ret, cls=DateTimeAwareJSONEncoder)

def write(data, filename):
    with open(filename, 'w') as output:
        json.dump(data, output)
        return True
    return False

def load(filename):
    with open(filename, 'r') as input:
        data = json.load(input)
        return data
    return False


def colincomments(s):
  if s.__contains__("/*") and s.__contains__("*/"):
    index_start = s.index("/*")
    index_end = s.index("*/")
    return s[index_start:index_end].replace("/*", '').replace("*/", '').replace(' ', '')
  return s

def average(nom, den):
  if den > 0:
    ans =  "%.2f%s" % (float(nom)*100/float(den), '%')
  else: ans = "0.00"
  return ans

def makecol(s):
  #Use name in comments
  s = colincomments(s)
  # Remove invalid characters
  s = re.sub('[^0-9a-zA-Z_]', '', s)
  # Remove leading characters until we find a letter or underscore
  s = re.sub('^[^a-zA-Z_]+', '', s)
  return s.lower()

def replaceincol(v, rv):
  return v % rv

def replaceindictcol(dictv, rv):
  for m in dictv.keys():
    x = dictv[m]
    x = ( x[0] % rv if x[0].__contains__("%s") else x[0], x[1] )
    dictv[m] = x
  return dictv
  
def makedict(x):
 ans = {}
 for y in x: ans[makecol(y[0])] = (y[0], y[1])
 return ans

def first_cap(s):
  if not s: return s
  return ' '.join([x[0].upper() + x[1:] for x in re.split(r'\s+', s)])

def give_me_cols(rows):
  cols = []
  data = []
  left_cols = ['province_pk', 'province_name', 'district_pk', 'district_name',
                'referral_facility_pk', 'referral_facility_name', 'facility_pk', 'facility_name', 'total']
  for row in rows:
    row = row.__dict__#;print row    
    if row.get('province_pk') and 'province_pk' not in cols:
      cols.insert(0, 'province_pk')
      cols.insert(1, 'province_name')
    if row.get('district_pk') and 'district_pk' not in cols:
      cols.insert(2, 'district_pk')
      cols.insert(3, 'district_name')
    if row.get('referral_facility_pk') and 'referral_facility_pk' not in cols:
      cols.insert(4, 'referral_facility_pk')
      cols.insert(5, 'referral_facility_name')
    if row.get('facility_pk') and 'facility_pk' not in cols:
      cols.insert(6, 'facility_pk')
      cols.insert(7, 'facility_name')
    if row.get('total') and 'total' not in cols:
      cols.insert(8, 'total')
      
    for k in row.keys():
      #print k, cols
      if k not in left_cols and k not in cols: cols.append(k)#; print "OUR KEY: ", k
    
    data.append([{ col : row[col]} for col in cols ])
  #print cols, data 
  return [ cols, data ]


def give_me_table(qry_result, user_locs, INDICS = [], LOCS = {}):

  indics = [ makecol(x) for x in [y[0] for y in INDICS] ]
  locs = get_initial_locations(user_locs, LOCS = LOCS)#; print locs
  heads = get_heading_cols(HEADERS = indics, LOCS = LOCS)  
  data = get_initial_data( heads = heads, indics_cols = indics, locs = locs)
  #print len(data), len(locs)
  index = 0
  
  for qs in qry_result:

    if type(qs) == Record:
      d = give_me_cols(qry_result)
      heads = d[0]
      data = d[1]
      break
    else:
      #print len(qry_result)      
      if index < len(qry_result):        
        d = give_me_cols(qry_result[index])
        cols = d[0]
        rows = d[1]
        
        for row in rows:
          try:
            col = cols[len(cols) - 1]#;print cols
            dt = match_me(data, row, len(cols) - 1 )#;print dt
            if dt:
                for d in dt:
                  if d.items()[0][0] == col:  d.update(row[cols.index(col)])
          except IndexError, e:
            continue
        
        index += 1
  
  #print heads, data       
  return {'heads' : heads, 'data' : data}

def match_me(data, row, col_index):
  index = len(data)
  dt = []
  for dt in data:
    if dt[:col_index] == row[:col_index]:
      #print dt, row, col_index
      break
  return dt

## Initialize everything by zero
def get_heading_cols( HEADERS = [], LOCS = {}):
  locs = []
  if LOCS.get('nation') or LOCS.get('nation') is None:  locs += ['province_pk', 'province_name']
  if LOCS.get('province'):  locs += ['district_pk', 'district_name']
  if LOCS.get('district'):  locs += ['referral_facility_pk', 'referral_facility_name']
  if LOCS.get('hospital'):  locs += ['facility_pk', 'facility_name']
  if LOCS.get('location'):
    if 'facility_pk' not in locs and 'facility_name' not in locs: locs += ['facility_pk', 'facility_name']
  cols = locs + HEADERS
  return cols

def get_initial_data(heads = [] , indics_cols = [], locs = []):
  data = []
  for loc in locs:
    dt = []
    loc = loc.__dict__    
    #print loc 
    if 'province_pk' in heads and loc.get('province_pk') and loc.get('province_name'):
      dt.insert(0, {'province_pk': loc['province_pk']})
      dt.insert(1, {'province_name': loc['province_name']})

    if 'district_pk' in heads and loc.get('district_pk') and loc.get('district_name'):
      dt.insert(2, {'district_pk': loc['district_pk']})
      dt.insert(3, {'district_name': loc['district_name']})

    if 'referral_facility_pk' in heads and loc.get('location_level_code') and loc.get('location_level_code') == 'HD':
      dt.insert(4, {'referral_facility_pk': loc['indexcol']})
      dt.insert(5, {'referral_facility_name': loc['name']})

    if 'facility_pk' in heads and loc.get('location_level_code') and loc.get('location_level_code') == 'HC':
      dt.insert(4, {'referral_facility_pk': loc['referral_facility_pk']})
      dt.insert(5, {'referral_facility_name': loc['referral_name']})
      dt.insert(6, {'facility_pk': loc['indexcol']})
      dt.insert(7, {'facility_name': loc['name']})

    for col in indics_cols: dt.insert( len(dt) + indics_cols.index(col), {col: 0})#; print indics_cols.index(col), col, dt

    data.append(dt) #; print dt 
     
  return data


def get_initial_locations(user_locs, LOCS = {}):

  locs = user_locs.get('provinces')
  locsy = []  
  if LOCS.get('nation'):
    locs = user_locs.get('provinces')
    locsy = UNDERSCORE(locs).chain().filter(lambda x, *args: x.nation_pk == int(LOCS.get('nation'))
                            ).map(lambda x, *args: x).sortBy().value()
    #print locs, locsy

  if LOCS.get('province'):
    locs = user_locs.get('districts')
    locsy = UNDERSCORE(locs).chain().filter(lambda x, *args: x.province_pk == int(LOCS.get('province'))
                            ).map(lambda x, *args: x).sortBy().value()
    #print len(locs), locsy, LOCS.get('province'), locs, locsy

  if LOCS.get('district'):
    locs = user_locs.get('hospitals')
    locsy = UNDERSCORE(locs).chain().filter(lambda x, *args: x.district_pk == int(LOCS.get('district'))
                            ).filter(lambda x, *args: x.location_level_code == 'HD'
                            ).map(lambda x, *args: x).sortBy().value()#;print locsy[0].__dict__,len(locsy), len(locs)

  if LOCS.get('hospital'):
    locs = user_locs.get('facilities')
    locsy = UNDERSCORE(locs).chain().filter(lambda x, *args: x.referral_facility_pk == int(LOCS.get('hospital'))
                             ).filter(lambda x, *args: x.location_level_code == 'HC'
                             ).map(lambda x, *args: x).sortBy().value()
  if LOCS.get('location'):
    locs = user_locs.get('facilities')
    locsy = UNDERSCORE(locs).chain().filter(lambda x, *args: x.indexcol == int(LOCS.get('location'))
                             ).map(lambda x, *args: x).sortBy().value()

  #print locsy

  if not locsy:
    return locs
  
  return locsy

"""
from util.mch_util import *
register_users()
"""

def make_excel_date(vdt, book):
    try:
        #print "TYPE DATE: %s" % type(vdt), vdt
        try:
            vdt_array = re.split(r'[`\-=~!@#$%^&*()_+\[\]{};\'\\:"|<,./<>?]', vdt)
            vdt_date = datetime.date(int(vdt_array[2]), int(vdt_array[1]), int(vdt_array[0]))
            return vdt_date
        except Exception, ex:
            new_vdt = int('%d' % vdt)
            #print "NEW DATE: ", xldate_as_tuple( new_vdt, book.datemode)
            vdt_date = datetime.datetime(* xldate_as_tuple( new_vdt, book.datemode))
            #print "NEW DATE ", vdt_date
            return vdt_date
    except Exception, e:
        #print e
        pass
    return None

def make_excel_str(vst):
    try:
        try:
            new_vst = '%d' % vst
            return new_vst.strip()
        except Exception, ex:
            new_vst = '%s' % vst
            return new_vst.strip()
    except Exception, e:
        #print e
        pass
    return None

def register_datamanagers(filepath = "db/datamanagers.xls", sheetname = "Users",
                    role_codes = ["DTM"], villages = []):

    try:
        book = open_workbook(filepath)
        sheet = book.sheet_by_name(sheetname)
        
        for row_index in range(sheet.nrows):
            try:
                if row_index < 1: continue
                surname         = make_excel_str(sheet.cell(row_index, 1).value)
                given_name      = make_excel_str(sheet.cell(row_index, 2).value)
                phone           = make_excel_str(sheet.cell(row_index, 3).value)
                dob             = make_excel_date(sheet.cell(row_index, 4).value, book)
                nid             = make_excel_str(sheet.cell(row_index, 5).value)
                email           = make_excel_str(sheet.cell(row_index, 7).value)
                district_name   = make_excel_str(sheet.cell(row_index, 9).value)
                hospital_name   = make_excel_str(sheet.cell(row_index, 10).value)
                sector_name     = make_excel_str(sheet.cell(row_index, 12).value)
                facility_name   = make_excel_str(sheet.cell(row_index, 11).value)
                cell_name       = make_excel_str(sheet.cell(row_index, 13).value) 
                village_name    = make_excel_str(sheet.cell(row_index, 14).value)
                sexcode         = 'F' if nid.strip()[5] == 7 else 'M'
                
                
                
                #print surname, given_name, phone, dob, nid, email, district_name, hospital_name, sector_name, facility_name, cell_name, village_name, sexcode
                role            = fetch_role(code = "DTM")
                sex             = fetch_gender(code = sexcode)

                user_area_level = fetch_location_level(code = "HD")
                district        = fetch_districts({'lower(name) LIKE %s': '%%%s%%' % district_name.lower() })[0]
                hospital        = fetch_referral_facilities({'lower(name) LIKE %s': '%%%s%%' % hospital_name.split(' ')[0].strip().lower(),
                                                             'district_pk = %s': district.indexcol})[0]
                sector          = fetch_sectors({'lower(name) LIKE %s': '%%%s%%' % sector_name.strip().lower(),
                                                             'district_pk = %s': district.indexcol})[0]
                #facility        = fetch_facilities({'lower(name) LIKE %s': facility_name.split(' ')[0].strip().lower(),
                #                                             'district_pk = %s': district.indexcol,
                #                                             'referral_facility_pk = %s': hospital.indexcol,
                #                                             'sector_pk = %s': sector.indexcol })[0]
                facility        = fetch_facilities({'district_pk = %s': district.indexcol,
                                                             'referral_facility_pk = %s': hospital.indexcol,
                                                             'sector_pk = %s': sector.indexcol })[0]
                
                cell            = fetch_cells({'lower(name) LIKE %s': '%%%s%%' % cell_name.split(' ')[0].strip().lower(),
                                                             'district_pk = %s': district.indexcol,
                                                             'sector_pk = %s': sector.indexcol })[0]
                village         = fetch_villages({'lower(name) LIKE %s': '%%%s%%' % village_name.split(' ')[0].strip().lower(),
                                                             'district_pk = %s': district.indexcol,
                                                             'sector_pk = %s': sector.indexcol,
                                                             'cell_pk = %s': cell.indexcol })[0]
                edu_level       = fetch_education_level(code = "U")
                djoin           = datetime.date.today()
                language        = fetch_language(code = "RW")
                

                if not nid or nid.strip() =="": nid = "123456%s" % phone[0:10]
 
                #print "DATA: ","\t", phone,"\t", nid,"\t", surname,"\t", given_name,"\t", role.name,"\t", sex.name, "\t", user_area_level.name, "\t", village.name, "\t", facility.name, "\t", edu_level.name, "\t", dob, "\t", djoin, "\t", language.code
                
                formdata = {    
                                    "telephone": phone, 
                                    "national_id":  nid,
                                    "email":      email,
                                    "surname":      surname,
                                    "given_name":   given_name,
                                    "sex_pk":   sex.indexcol,
                                    "role_pk":  role.indexcol,
                                    "education_level_pk":    edu_level.indexcol,
                                    "date_of_birth" :  dob, 
                                    "join_date": djoin,
                                    "language_pk": language.indexcol,
                                    "nation_pk": district.nation_pk,
                                    "province_pk": district.province_pk,
                                    "district_pk": district.indexcol,
                                    "referral_facility_pk": hospital.indexcol,
                                    "facility_pk" : facility.indexcol,
                                    "location_level_pk": user_area_level.indexcol,                            
                                    "sector_pk": sector.indexcol,
                                    "cell_pk": cell.indexcol,
                                    "village_pk": village.indexcol,
                                    "is_active": True,
                                    "is_correct": True

                                }
            
                #print "DATA: ", formdata              
                message, user = Enduser.get_or_create(formdata)
                #print message, user.__dict__
            except Exception, e:
                print "ROW INDEX: ", e
                continue
            
    except Exception, e:
        print e
    return True

def register_users(filepath = "db/users.xls", sheetname = "Users",
                    role_codes = ["BINOME", "CSUP", "CNUR", "CLN", "HOHC", "LOG", "HQ"], villages = ["0507090104", "0507100507"]):

    try:
        book = open_workbook(filepath)
        sheet = book.sheet_by_name(sheetname)
        
        for row_index in range(sheet.nrows):
            try:
                if row_index < 1: continue
                phone = sheet.cell(row_index, 8).value
                nid   = sheet.cell(row_index, 7).value
                names = sheet.cell(row_index, 4).value
                surname = given_name = ""
                role    = fetch_role(code = random.choice(role_codes))
                sex     = fetch_gender(code = random.choice(["F", "M"]))
                user_area_level = fetch_location_level(code = "VIL")
                village =   fetch_village(code = random.choice(villages))
                fosa    =   "453" if village.code == "0507100507" else "1101" 
                facility =  fetch_facility(code = fosa)
                edu_level = fetch_education_level(code = "U")
                dob       = datetime.date.today() - datetime.timedelta(days = 365*35)
                djoin     = datetime.date.today()
                language    = fetch_language(code = "RW")
                if names:
                    names   = names.split(" ") 
                    if len(names) > 1:
                        surname = names[0]
                        given_name = " ".join(names[1:])
                    else:
                        surname = names[0]

                if role.code == "HQ":
                    user_area_level = fetch_location_level(code = "NATION")
                    language    = fetch_language(code = "EN")
                elif role.code == "CSUP" or role.code == "CNUR" or role.code == "LOG":
                    user_area_level = fetch_location_level(code = "HD")
                    language    = fetch_language(code = "EN")
                elif role.code == "CLN" or role.code == "HOHC":
                    user_area_level = fetch_location_level(code = "HC")
                    language    = fetch_language(code = "EN")
                else:
                    user_area_level = user_area_level

                if not nid or nid.strip() =="": nid = "123456%s" % phone
 
                #print "DATA: ","\t", phone,"\t", nid,"\t", surname,"\t", given_name,"\t", role.name,"\t", sex.name, "\t", user_area_level.name, "\t", village.name, "\t", facility.name, "\t", edu_level.name, "\t", dob, "\t", djoin, "\t", language.code
                
                formdata = {    
                                    "telephone": phone, 
                                    "national_id":  nid,
                                    "email":      None,
                                    "surname":      surname,
                                    "given_name":   given_name,
                                    "sex_pk":   sex.indexcol,
                                    "role_pk":  role.indexcol,
                                    "education_level_pk":    edu_level.indexcol,
                                    "date_of_birth" :  dob, 
                                    "join_date": djoin,
                                    "language_pk": language.indexcol,
                                    "nation_pk": village.nation_pk,
                                    "province_pk": village.province_pk,
                                    "district_pk": village.district_pk,
                                    "referral_facility_pk": facility.referral_facility_pk,
                                    "facility_pk" : facility.indexcol,
                                    "location_level_pk": user_area_level.indexcol,                            
                                    "sector_pk": village.sector_pk,
                                    "cell_pk": village.cell_pk,
                                    "village_pk": village.indexcol,
                                    "is_active": True,
                                    "is_correct": True

                                }
            
                #print "DATA: ", formdata                
                message, user = Enduser.get_or_create(formdata)
                #print message, user.__dict__
            except Exception, e:
                #print "ROW INDEX: ", e
                continue
            
    except Exception, e:
        pass
        #print e
    return True

def register_users_random(filepath = "db/NYAMATA_Compiled List_2nd Session.xls", sheetname = "Users",
                    role_codes = ["BINOME", "SUP", "DNUR", "CLN", "HOHC", "LOG", "HQ"], villages = ["0507090104", "0507100507"]):

    try:
        book = open_workbook(filepath)
        sheet = book.sheet_by_name(sheetname)
        
        for row_index in range(sheet.nrows):
            try:
                if row_index < 1: continue
                email = sheet.cell(row_index, 5).value
                phone = sheet.cell(row_index, 4).value
                nid   = sheet.cell(row_index, 3).value
                names = sheet.cell(row_index, 1).value
                surname = given_name = ""
                role    = fetch_role(code = random.choice(role_codes))
                sex     = fetch_gender(code = random.choice(["F", "M"]))
                user_area_level = fetch_location_level(code = "VIL")
                village =   fetch_village(code = random.choice(villages))
                fosa    =   "453" if village.code == "0507100507" else "1101" 
                facility =  fetch_facility(code = fosa)
                edu_level = fetch_education_level(code = "U")
                dob       = datetime.date.today() - datetime.timedelta(days = 365*35)
                djoin     = datetime.date.today()
                language    = fetch_language(code = "RW")
                if names:
                    names   = names.split(" ") 
                    if len(names) > 1:
                        surname = names[0]
                        given_name = " ".join(names[1:])
                    else:
                        surname = names[0]

                if role.code == "HQ":
                    user_area_level = fetch_location_level(code = "NATION")
                    language    = fetch_language(code = "EN")
                elif role.code == "DNUR" or role.code == "LOG":
                    user_area_level = fetch_location_level(code = "HD")
                    language    = fetch_language(code = "EN")
                elif role.code == "CLN" or role.code == "SUP":
                    user_area_level = fetch_location_level(code = random.choice(["HC", "HD"]))
                    language    = fetch_language(code = "EN")
                elif role.code == "HOHC":
                    user_area_level = fetch_location_level(code = "HC")
                    language    = fetch_language(code = "EN")
                else:
                    user_area_level = user_area_level

                if not nid or nid.strip() =="": nid = "123456%s" % phone
 
                #print "DATA: ","\t", phone,"\t", nid,"\t", surname,"\t", given_name,"\t", role.name,"\t", sex.name, "\t", user_area_level.name, "\t", village.name, "\t", facility.name, "\t", edu_level.name, "\t", dob, "\t", djoin, "\t", language.code
                
                formdata = {    
                                    "telephone": phone, 
                                    "national_id":  nid,
                                    "email":      None,
                                    "surname":      surname,
                                    "given_name":   given_name,
                                    "sex_pk":   sex.indexcol,
                                    "role_pk":  role.indexcol,
                                    "education_level_pk":    edu_level.indexcol,
                                    "date_of_birth" :  dob, 
                                    "join_date": djoin,
                                    "language_pk": language.indexcol,
                                    "nation_pk": village.nation_pk,
                                    "province_pk": village.province_pk,
                                    "district_pk": village.district_pk,
                                    "referral_facility_pk": facility.referral_facility_pk,
                                    "facility_pk" : facility.indexcol,
                                    "location_level_pk": user_area_level.indexcol,                            
                                    "sector_pk": village.sector_pk,
                                    "cell_pk": village.cell_pk,
                                    "village_pk": village.indexcol,
                                    "is_active": True,
                                    "is_correct": True

                                }
            
                #print "DATA: ", formdata                
                message, user = Enduser.get_or_create(formdata)
                #print message, user.__dict__
            except Exception, e:
                print "ROW INDEX: ", e
                continue
            
    except Exception, e:
        print e
    return True


def register_nyamata_users_1(filepath = "db/nyamata_users_1.xls", sheetname = "Users",
                    role_codes = ["BINOME", "ASM"], villages = ["0507090104"]):

    try:
        book = open_workbook(filepath)
        sheet = book.sheet_by_name(sheetname)
        
        for row_index in range(sheet.nrows):
            try:
                if row_index < 6: continue
                phone = sheet.cell(row_index, 5).value
                nid   = sheet.cell(row_index, 4).value
                names = sheet.cell(row_index, 1).value
                surname = given_name = ""
                role    = fetch_role(code = random.choice(role_codes))
                sex     = fetch_gender(code = random.choice(["F", "M"]))
                user_area_level = fetch_location_level(code = "VIL")
                village =   fetch_village(code = random.choice(villages))
                fosa    =   "453" if village.code == "0507100507" else "1101" 
                facility =  fetch_facility(code = fosa)
                edu_level = fetch_education_level(code = "U")
                dob       = datetime.date.today() - datetime.timedelta(days = 365*35)
                djoin     = datetime.date.today()
                language    = fetch_language(code = "RW")
                if names:
                    names   = names.split(" ") 
                    if len(names) > 1:
                        surname = names[0]
                        given_name = " ".join(names[1:])
                    else:
                        surname = names[0]

                if role.code == "HQ":
                    user_area_level = fetch_location_level(code = "NATION")
                    language    = fetch_language(code = "EN")
                elif role.code == "CSUP" or role.code == "CNUR" or role.code == "LOG":
                    user_area_level = fetch_location_level(code = "HD")
                    language    = fetch_language(code = "EN")
                elif role.code == "CLN" or role.code == "HOHC":
                    user_area_level = fetch_location_level(code = "HC")
                    language    = fetch_language(code = "EN")
                else:
                    user_area_level = user_area_level

                if not nid or nid.strip() =="": nid = "123456%s" % phone
 
                print "DATA: ","\t", phone,"\t", nid,"\t", surname,"\t", given_name,"\t", role.name,"\t", sex.name, "\t", user_area_level.name, "\t", village.name, "\t", facility.name, "\t", edu_level.name, "\t", dob, "\t", djoin, "\t", language.code
                
                formdata = {    
                                    "telephone": phone, 
                                    "national_id":  nid,
                                    "email":      None,
                                    "surname":      surname,
                                    "given_name":   given_name,
                                    "sex_pk":   sex.indexcol,
                                    "role_pk":  role.indexcol,
                                    "education_level_pk":    edu_level.indexcol,
                                    "date_of_birth" :  dob, 
                                    "join_date": djoin,
                                    "language_pk": language.indexcol,
                                    "nation_pk": village.nation_pk,
                                    "province_pk": village.province_pk,
                                    "district_pk": village.district_pk,
                                    "referral_facility_pk": facility.referral_facility_pk,
                                    "facility_pk" : facility.indexcol,
                                    "location_level_pk": user_area_level.indexcol,                            
                                    "sector_pk": village.sector_pk,
                                    "cell_pk": village.cell_pk,
                                    "village_pk": village.indexcol,
                                    "is_active": True,
                                    "is_correct": True

                                }
            
                #print "DATA: ", formdata                
                message, user = Enduser.get_or_create(formdata)
                #print message, user.__dict__
            except Exception, e:
                print "ROW INDEX: ", e
                continue
            
    except Exception, e:
        print e
    return True


def register_users_session2(filepath = "db/Session2.xls", sheetname = "Users",
                    role_codes = ["BINOME", "SUP", "DNUR", "CLN", "HOHC", "LOG", "HQ"], villages = ["0507090104", "0507100507"]):

    try:
        book = open_workbook(filepath)
        sheet = book.sheet_by_name(sheetname)
        
        for row_index in range(sheet.nrows):
            try:
                if row_index < 3: continue
                hpfosa  = '%d' % sheet.cell(row_index, 8).value
                facfosa = '%d' % sheet.cell(row_index, 11).value
                email   = sheet.cell(row_index, 5).value
                phone   = sheet.cell(row_index, 4).value
                nid     = sheet.cell(row_index, 3).value
                crole   = sheet.cell(row_index, 2).value
                crolen = 'BINOME'
                clevel = 'VIL'
                if crole.strip() == 'CHW': crolen = 'BINOME'
                if crole.strip() == 'CHW Supervisor at HC': crolen, clevel = 'SUP', 'HC'
                if crole.strip() == 'Clinician at DH': crolen, clevel = 'CLN', 'HD'
                if crole.strip() == 'Clinician at HC': crolen, clevel = 'CLN', 'HC'
                names = sheet.cell(row_index, 1).value
                surname = given_name = ""
                role    = fetch_role(code = crolen)
                sex     = fetch_gender(code = random.choice(["F", "M"]))
                user_area_level = fetch_location_level(code = clevel)
                facility =  fetch_facility(code = facfosa)
                hpfacility =  fetch_facility(code = hpfosa)
                village =   fetch_villages({'sector_pk = %s' : facility.sector_pk})[0]
                try:
                    vname_l  = sheet.cell(row_index, 13).value
                    vname_ll = vname_l.strip().split(" ")
                    vname    = "%%%s%%" % vname_ll[0]
                    nvillage = fetch_villages({'sector_pk = %s' : facility.sector_pk, 'name LIKE %s' : vname })[0]
                    if nvillage: village = nvillage
                except: pass
                edu_level = fetch_education_level(code = "U")
                dob       = datetime.date.today() - datetime.timedelta(days = 365*35)
                djoin     = datetime.date.today()
                language    = fetch_language(code = "RW")
                if names:
                    names   = names.split(" ") 
                    if len(names) > 1:
                        surname = names[0]
                        given_name = " ".join(names[1:])
                    else:
                        surname = names[0]

                if not nid or nid.strip() == "" or len(nid) !=16: nid = "123456%s" % phone
 
                #print "DATA: ","\t", phone,"\t", nid,"\t", surname,"\t", given_name,"\t", role.name,"\t", sex.name, "\t", user_area_level.name, "\t", village.name, "\t", facility.name, "\t", hpfacility.name, "\t", edu_level.name, "\t", dob, "\t", djoin, "\t", language.code
                
                formdata = {    
                                    "telephone": phone, 
                                    "national_id":  nid,
                                    "email":      email.strip(),
                                    "surname":      surname,
                                    "given_name":   given_name,
                                    "sex_pk":   sex.indexcol,
                                    "role_pk":  role.indexcol,
                                    "education_level_pk":    edu_level.indexcol,
                                    "date_of_birth" :  dob, 
                                    "join_date": djoin,
                                    "language_pk": language.indexcol,
                                    "nation_pk": village.nation_pk,
                                    "province_pk": village.province_pk,
                                    "district_pk": village.district_pk,
                                    "referral_facility_pk": hpfacility.indexcol,
                                    "facility_pk" : facility.indexcol,
                                    "location_level_pk": user_area_level.indexcol,                            
                                    "sector_pk": village.sector_pk,
                                    "cell_pk": village.cell_pk,
                                    "village_pk": village.indexcol,
                                    "is_active": True,
                                    "is_correct": True

                                }
            
                #print "DATA: ", formdata                
                message, user = Enduser.get_or_create(formdata)
                #print message, user.__dict__
            except Exception, e:
                print "ROW INDEX: ", e
                continue
            
    except Exception, e:
        print e
    return True


def parse_codes(report, record, CODES = {}):
    message = ""
    try:
        fields = []
        message = record.message
        for k in record.__dict__.keys():
            try:
                if CODES:
                    field = getattr(record, k)
                    value = CODES.get(field)
                    fields.append(value.get('en'))
                else:
                    field = fetch_smsfield(getattr(record, k), report.indexcol)
                    fields.append(field.name_en)
            except Exception, e:
                #print k, e
                continue
        message = ", ".join(fields) 
    except Exception, e:
        #print e
        pass
    return message

def parse_record_keys(record):
    cols = []
    try:
        cols = record.__dict__.keys()    
    except Exception, e:
        #print e
        pass    
    return cols


def translate_record(record, col):
    v = ""
    try:    
        coltr = col.replace('_pk', '_name')
        v = getattr(record, coltr)
    except Exception, e:
        #print e
        pass
    return v

def parse_record_value(record, col):
    v = ""
    try:
        v = getattr(record, col)
        if type(v) == bool: v = "Yes" if v == True else "No"
        if col.find('_pk') >=0 : v = translate_record(record, col)
    except Exception, e:
        #print e
        pass
    return v

def parse_report_cols(record):
    #print record
    report = {}
    try:
        #print record
        cols = parse_record_keys(record); #print cols
        report.update({"IDENTITY_COLS": []})
        for col in queries.IDENTITY_COLS:
            if col[0] in cols:
                colvalue = parse_record_value(record, col[0])
                if colvalue:    report['IDENTITY_COLS'].append( (col[0], col[1], colvalue ) )
                else:
                    continue

        report.update({"HC_COLS": []})
        for col in queries.HC_COLS:
            if col[0] in cols:
                colvalue = parse_record_value(record, col[0])
                if colvalue:    report['HC_COLS'].append( (col[0], col[1], colvalue ) )
                else:
                    continue

        report.update({"HD_COLS": []})
        for col in queries.HD_COLS:
            if col[0] in cols:
                colvalue = parse_record_value(record, col[0])
                if colvalue:    report['HD_COLS'].append( (col[0], col[1], colvalue ) )
                else:
                    continue

        report.update({"SYMPTOMS_COLS": []})
        for col in queries.SYMPTOMS_COLS:
            if col[0] in cols:
                colvalue = parse_record_value(record, col[0])
                if colvalue:    report['SYMPTOMS_COLS'].append( (col[0], col[1], colvalue ) )
                else:
                    continue 

        report.update({"DRUGS_COLS": []})
        for col in queries.DRUGS_COLS:
            if col[0] in cols:
                colvalue = parse_record_value(record, col[0])
                if colvalue:    report['DRUGS_COLS'].append( (col[0], col[1], colvalue ) )
                else:
                    continue 

        report.update({"INTERVENTION_COLS": []})
        for col in queries.INTERVENTION_COLS:
            if col[0] in cols:
                colvalue = parse_record_value(record, col[0])
                if colvalue:    report['INTERVENTION_COLS'].append( (col[0], col[1], colvalue ) )
                else:
                    continue

        report.update({"STATUS_COLS": []})
        for col in queries.STATUS_COLS:
            if col[0] in cols:
                colvalue = parse_record_value(record, col[0]); print colvalue
                if colvalue and colvalue !='No':    report['STATUS_COLS'].append( (col[0], col[1], colvalue ) )
                else:
                    continue 
           
    except Exception, e:
        #print e
        pass
    return report


def process_import_file(import_file, user_pk, upload_time):
    # Although this just counts the file length, it demonstrates
    # how to read large files in chunks instead of all at once.
    # CherryPy reads the uploaded file into a temporary file;
    # myFile.file.read reads from that.
    d = upload_time
    filename = 'frontend/static/uploads/file%s_%s%s%s%s%s%s%s_%s' % (user_pk, d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond, import_file.filename)
    size = 0
    whole_data = bytearray() # Neues Bytearray
    while True:
        data = import_file.file.read(8192)
        whole_data += data # Save data chunks in ByteArray whole_data

        if not data:
            break
        size += len(data)

        written_file = open(filename, "wb") # open file in write bytes mode
        written_file.write(whole_data) # write file

    return (size, filename, import_file.content_type)


def upload_users_indb(filepath, sheetname = "Users"):

    try:
        book    = open_workbook(filepath)
        sheet   = book.sheet_by_name(sheetname)
        file_errors  = []
        for row_index in range(sheet.nrows):
            try:
                errors = []
                formdata = {
                            "is_active": True,
                            "is_correct": True
                            }
                if row_index < 1: continue
                try:
                    surname         = make_excel_str(sheet.cell(row_index, 1).value)
                    formdata.update({"surname":      surname})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid surname', '%s' % e.message ))
                try:
                    given_name      = make_excel_str(sheet.cell(row_index, 2).value)
                    formdata.update({"given_name":   given_name})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid given name', '%s' % e.message ))
                try:
                    phone           = make_excel_str(sheet.cell(row_index, 3).value)
                    formdata.update({"telephone": phone})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid telephone', '%s' % e.message ))
                try:
                    dob             = make_excel_date(sheet.cell(row_index, 4).value, book)
                    formdata.update({"date_of_birth" :  dob})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid date of birth', '%s' % e.message ))
                try:
                    nid             = make_excel_str(sheet.cell(row_index, 5).value)
                    if not nid or nid.strip() =="": nid = "123456%s" % phone[0:10]
                    formdata.update({"national_id":  nid})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid national id', '%s' % e.message ))                
                try:
                    role_name       = make_excel_str(sheet.cell(row_index, 6).value)
                    role            = fetch_roles({'lower(name) LIKE %s': '%%%s%%' % role_name.strip().lower() } )[0]
                    formdata.update({"role_pk":  role.indexcol})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid post/function', '%s' % e.message ))

                try:
                    area_level     = make_excel_str(sheet.cell(row_index, 7).value)
                    user_area_level = fetch_location_levels({'lower(name) LIKE %s': '%%%s%%' % area_level.strip().lower() })[0]
                    formdata.update({"location_level_pk": user_area_level.indexcol})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid catchment area', '%s' % e.message ))

                try:
                    email           = make_excel_str(sheet.cell(row_index, 8).value)
                    formdata.update({"email":      email})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid email', '%s' % e.message ))

                try:
                    district_name   = make_excel_str(sheet.cell(row_index, 10).value)
                    district        = fetch_districts({'lower(name) LIKE %s': '%%%s%%' % district_name.lower() })[0]
                    formdata.update({"district_pk": district.indexcol,
                                     "nation_pk": district.nation_pk,
                                     "province_pk": district.province_pk})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid district', '%s' % e.message ))

                try:
                    hospital_name   = make_excel_str(sheet.cell(row_index, 11).value)
                    hospital        = fetch_referral_facilities({'lower(name) LIKE %s': '%%%s%%' % hospital_name.split(' ')[0].strip().lower(),
                                                             'district_pk = %s': formdata.get('district_pk')})[0]
                    formdata.update({"referral_facility_pk": hospital.indexcol})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid district hospital', '%s' % e.message ))

                try:
                    sector_name     = make_excel_str(sheet.cell(row_index, 13).value)
                    sector          = fetch_sectors({'lower(name) LIKE %s': '%%%s%%' % sector_name.strip().lower(),
                                                             'district_pk = %s': formdata.get('district_pk')})[0]
                    formdata.update({"sector_pk": sector.indexcol})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid sector', '%s' % e.message ))

                try:
                    facility_name   = make_excel_str(sheet.cell(row_index, 12).value)
                    facility        = fetch_facilities({'lower(name) LIKE %s': facility_name.split(' ')[0].strip().lower(),
                                                             'district_pk = %s': formdata.get('district_pk'),
                                                             'referral_facility_pk = %s': formdata.get('referral_facility_pk'),
                                                             'sector_pk = %s': formdata.get('sector_pk') })[0]
                    formdata.update({"facility_pk" : facility.indexcol})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid health centre', '%s' % e.message ))

                try:
                    cell_name       = make_excel_str(sheet.cell(row_index, 14).value)
                    cell            = fetch_cells({'lower(name) LIKE %s': '%%%s%%' % cell_name.split(' ')[0].strip().lower(),
                                                             'district_pk = %s': formdata.get('district_pk'),
                                                             'sector_pk = %s': formdata.get('sector_pk') })[0]
                    formdata.update({"cell_pk": cell.indexcol})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid cell', '%s' % e.message )) 
                try:
                    village_name    = make_excel_str(sheet.cell(row_index, 15).value)
                    village         = fetch_villages({'lower(name) LIKE %s': '%%%s%%' % village_name.split(' ')[0].strip().lower(),
                                                             'district_pk = %s': formdata.get('district_pk'),
                                                             'sector_pk = %s': formdata.get('sector_pk'),
                                                             'cell_pk = %s': formdata.get('cell_pk') })[0]
                    formdata.update({"village_pk": village.indexcol})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid village', '%s' % e.message ))

                try:
                    sexcode         = 'F' if nid.strip()[5] == 7 else 'M'
                    sex             = fetch_gender(code = sexcode)
                    formdata.update({"sex_pk":   sex.indexcol})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid sex', '%s' % e.message ))

                try:
                    edu_level       = fetch_education_level(code = "U")
                    formdata.update({"education_level_pk":    edu_level.indexcol})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid education level', '%s' % e.message ))

                try:
                    djoin           = datetime.date.today()
                    formdata.update({"join_date": djoin})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid joining date', '%s' % e.message ))

                try:
                    language        = fetch_language(code = "RW")
                    formdata.update({"language_pk": language.indexcol})
                except Exception, e:
                    errors.append( (row_index + 1, 'Invalid language', '%s' % e.message ))
            
                #print "DATA: ", formdata
                if len(errors) > 0:
                    who = ''
                    try:    who = '%s %s' % (make_excel_str(sheet.cell(row_index, 1).value), make_excel_str(sheet.cell(row_index, 2).value) )
                    except: pass
                    file_errors.append({'row': row_index, 'who': who, 'errors': errors})
                else:               
                    message, user = Enduser.get_or_create(formdata)
                    #print message, user.__dict__
            except Exception, ex1:
                #print "ROW INDEX: ", ex1
                file_errors.append({'row': row_index, 'who': '', 'errors': [('All', 'Invalid data', ex1.message)] })
                continue
            
    except Exception, ex2:
        file_errors.append({'row': 'All', 'who': 'All', 'errors': [('All', 'Invalid file template', ex2.message)] })
        #print ex2
    return file_errors


def export_data_to_xlsx(headers, records, filename = 'exports.xlsx'):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('frontend/static/files/%s' % filename)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})

    # Write some data headers.
    row = 0
    col = 0
    worksheet.write(row, col, "No", bold)
    col = 1
    for h in headers:
        nh = h.replace('_', ' ')
        worksheet.write(row, col, nh.upper(), bold)
        col += 1

    # Start from the first cell below the headers.
    # And write our records in the worksheet of the filename
    row = 1
    for r in records:
        nr = r.__dict__
        col = 0
        worksheet.write(row, col, row, bold)
        col = 1
        for h in headers:
            if h in ['date_of_birth', 'created_at', 'lmp']: worksheet.write(row, col, nr.get(h),  date_format)
            else:   worksheet.write(row, col, nr.get(h))
            col += 1
            
        row += 1
    
    
    return filename


def export_performance_to_xlsx(headers, records, filename = 'exports.xlsx', ans = []):

    from underscore import _ as UNDERSCORE    

    #seens = UNDERSCORE(ans).chain().groupBy(lambda x, *args: x.user_pk).map(lambda x, *args: x).sortBy().value()

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('frontend/static/files/%s' % filename)
    worksheet = workbook.add_worksheet()

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})
    date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})


    # Write some data headers.
    row = 0
    col = 0
    worksheet.write(row, col, "No", bold)
    col = 1
    for h in headers:
        nh = h.replace('_', ' ')
        worksheet.write(row, col, nh.upper(), bold)
        col += 1

    # Start from the first cell below the headers.
    # And write our records in the worksheet of the filename
    
    row = 1
    """
    for s in seens:
        r = UNDERSCORE(records).chain().find(lambda x, *args: x.indexcol == s[0].user_pk).value()
        nr = r.__dict__
        for k in s:  nr.update(k.__dict__)
        col = 0
        worksheet.write(row, col, row, bold)
        col = 1
        for h in headers:
            worksheet.write(row, col, nr.get(h) or 0)
            col += 1      
            
        row += 1
    """
    
    for r in records:
        nr = r.__dict__
        rpts = UNDERSCORE(ans).chain().filter(lambda x, *args: x.user_pk == r.indexcol).map(lambda x, *args: x).sortBy().value()
        for rpt in rpts:  nr.update(rpt.__dict__)
        col = 0
        worksheet.write(row, col, row, bold)
        col = 1
        for h in headers:
            if h in ['date_of_birth', 'created_at', 'lmp']: worksheet.write(row, col, nr.get(h) or 0,  date_format)
            else:   worksheet.write(row, col, nr.get(h) or 0)
            col += 1      
            
        row += 1  
    
    
    return filename


