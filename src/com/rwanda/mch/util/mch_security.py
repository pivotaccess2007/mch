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


import random
import sha
import jwt
import datetime

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from util.mch_connection import SALT_STRENGTH, AUTH_HOME, SECRET, GESTATION, NBC_GESTATION, PNC_GESTATION, TRACKING_DAYS
from util.record import fetch_user, fetch_villages, fetch_facilities, fetch_user_by_email, fetch_provinces, fetch_districts, fetch_sectors, fetch_cells, fetch_user_privileges, fetch_privileges
from exception.mch_critical_error import MchCriticalError


class MchSecurity:

  @staticmethod
  def get_auth_pages(user):
    # TODO custom home page
    home_page = AUTH_HOME
    pages = {'home': home_page}
    privs = fetch_user_privileges(user)
    for p in privs: pages.update({p.code: p.url})
    #TODO a list of pages you are allowed to access, to be populated at every login
    # Then update pages
    return pages

  @staticmethod
  def get_user_level(user):
    level = fetch_location_levels(filters = {})    
    return villages

  @staticmethod
  def get_privileges():
    pages = {}
    privs =  fetch_privileges()
    for p in privs: pages.update({p.code: p})
    return pages

  @staticmethod
  def get_user_village_level_filter(user):
    level_filter = None
    if user.location_level_code == 'NATION':  level_filter = {'nation_pk = %s' : user.nation_pk } 
    if user.location_level_code == 'PRV':  level_filter = {'province_pk = %s' : user.province_pk } 
    if user.location_level_code == 'DST':  level_filter = {'district_pk = %s' : user.district_pk } 
    if user.location_level_code == 'NRH':  level_filter = {'referral_facility_pk = %s' : user.referral_facility_pk } 
    if user.location_level_code == 'MH':  level_filter = {'referral_facility_pk = %s' : user.referral_facility_pk } 
    if user.location_level_code == 'HD':  level_filter = {'referral_facility_pk = %s' : user.referral_facility_pk } 
    if user.location_level_code == 'HP':  level_filter = {'referral_facility_pk = %s' : user.referral_facility_pk } 
    if user.location_level_code == 'HC':  level_filter = {'facility_pk = %s' : user.facility_pk } 
    if user.location_level_code == 'CL':  level_filter = {'facility_pk = %s' : user.facility_pk } 
    if user.location_level_code == 'SEC':  level_filter = {'sector_pk = %s' : user.sector_pk }
    if user.location_level_code == 'CEL':  level_filter = {'cell_pk = %s' : user.cell_pk } 
    if user.location_level_code == 'VIL':  level_filter = {'village_pk = %s' : user.village_pk }  
    return level_filter

  @staticmethod
  def get_user_facility_level_filter(user):
    level_filter = None
    if user.location_level_code == 'NATION':  level_filter = {'nation_pk = %s' : user.nation_pk } 
    if user.location_level_code == 'PRV':  level_filter = {'province_pk = %s' : user.province_pk } 
    if user.location_level_code == 'DST':  level_filter = {'district_pk = %s' : user.district_pk } 
    if user.location_level_code == 'NRH':  level_filter = {'referral_facility_pk = %s' : user.referral_facility_pk } 
    if user.location_level_code == 'MH':  level_filter = {'referral_facility_pk = %s' : user.referral_facility_pk } 
    if user.location_level_code == 'HD':  level_filter = {'referral_facility_pk = %s' : user.referral_facility_pk } 
    if user.location_level_code == 'HP':  level_filter = {'referral_facility_pk = %s' : user.referral_facility_pk } 
    if user.location_level_code == 'HC':  level_filter = {'indexcol = %s' : user.facility_pk } 
    if user.location_level_code == 'CL':  level_filter = {'indexcol = %s' : user.facility_pk } 
    if user.location_level_code == 'SEC':  level_filter = {'indexcol = %s' : user.facility_pk }
    if user.location_level_code == 'CEL':  level_filter = {'indexcol = %s' : user.facility_pk } 
    if user.location_level_code == 'VIL':  level_filter = {'indexcol = %s' : user.facility_pk }  
    return level_filter

  @staticmethod
  def get_user_facility_level_filter_keys(user):
    level_filter = None
    if user.location_level_code == 'NATION':  level_filter = ['nation_pk', user.nation_pk ] 
    if user.location_level_code == 'PRV':  level_filter = ['province_pk' , user.province_pk ] 
    if user.location_level_code == 'DST':  level_filter = ['district_pk' , user.district_pk ] 
    if user.location_level_code == 'NRH':  level_filter = ['referral_facility_pk' , user.referral_facility_pk ] 
    if user.location_level_code == 'MH':  level_filter = ['referral_facility_pk' , user.referral_facility_pk ] 
    if user.location_level_code == 'HD':  level_filter = ['referral_facility_pk' , user.referral_facility_pk ] 
    if user.location_level_code == 'HP':  level_filter = ['referral_facility_pk' , user.referral_facility_pk]  
    if user.location_level_code == 'HC':  level_filter = ['indexcol' , user.facility_pk ] 
    if user.location_level_code == 'CL':  level_filter = ['indexcol' , user.facility_pk ] 
    if user.location_level_code == 'SEC':  level_filter = ['indexcol' , user.facility_pk ]
    if user.location_level_code == 'CEL':  level_filter = ['indexcol' , user.facility_pk ] 
    if user.location_level_code == 'VIL':  level_filter = ['indexcol' , user.facility_pk ]  
    return level_filter

  @staticmethod
  def get_auth_filter_locations(user, loctype, locparentid):
    locs = []
    if loctype == 'prv':
      filters = {'nation_pk = %s': locparentid}
      if user.location_level_code in ['PRV', 'DST', 'HD', 'HC', 'SEC', 'CEL', 'VIL']:  filters.update({'province_pk = %s' : user.province_pk })
      locs = fetch_provinces(filters)
    if loctype == 'dst':
      filters = {'province_pk = %s': locparentid}
      if user.location_level_code in ['DST', 'HD', 'HC', 'SEC', 'CEL', 'VIL']:  filters.update({'district_pk = %s' : user.district_pk })
      locs = fetch_districts(filters)
    if loctype == 'hd':
      filters = {'district_pk = %s': locparentid}
      if user.location_level_code in ['HD', 'HC', 'SEC', 'CEL', 'VIL']:  filters.update({'indexcol = %s' : user.referral_facility_pk })
      locs = fetch_referral_facilities(filters)
    if loctype == 'hc':
      filters = {'referral_facility_pk = %s': locparentid}
      if user.location_level_code in ['HC', 'SEC', 'CEL', 'VIL']:  filters.update({'indexcol = %s' : user.facility_pk })
      locs = fetch_facilities(filters)
    if loctype == 'sec':
      filters = {'district_pk = %s': locparentid}
      if user.location_level_code in ['SEC', 'CEL', 'VIL']:  filters.update({'sector_pk = %s' : user.sector_pk })
      locs = fetch_sectors(filters)
    if loctype == 'cel':
      filters = {'sector_pk = %s': locparentid}
      if user.location_level_code in ['CEL', 'VIL']:  filters.update({'cell_pk = %s' : user.cell_pk })
      locs = fetch_cells(filters) 
    if loctype == 'vil':
      filters = {'cell_pk = %s': locparentid}
      if user.location_level_code == 'VIL':  filters.update({'village_pk = %s' : user.village_pk })
      locs = fetch_villages(filters) 
    return locs

  @staticmethod
  def get_auth_villages(user):
    villages = []
    level_filter = MchSecurity.get_user_village_level_filter(user)
    ##print level_filter 
    villages = fetch_villages(level_filter)
    return villages

  @staticmethod
  def get_auth_facilities(user):    
    facilities = []
    level_filter = MchSecurity.get_user_facility_level_filter(user)
    ##print level_filter 
    facilities = fetch_facilities(level_filter)
    return facilities

  @staticmethod
  def get_auth_location(user, flts):
    prv = flts.get('province')
    if user and not prv: prv = user.province_pk if user.location_level_code == "PRV" else None
    dst = flts.get('district')
    if user and not dst: dst = user.district_pk if user.location_level_code == 'DST' else None
    hc  = flts.get('hc')
    if user and not hc:  hc = user.facility_pk if user.location_level_code in ['HC', 'CL'] else None
    hp  = flts.get('hp')
    if user and not hp:  hp = user.referral_facility_pk if user.location_level_code in ['HP', 'HD', 'MH'] else None
    sec = flts.get('sec')
    if user and not sec:  sec = user.sector_pk if user.location_level_code == 'SEC' else None
    cel = flts.get('cel')
    if user and not cel:  cel = user.cell_pk if user.location_level_code == 'CEL' else None
    vil = flts.get('vil')
    if user and not vil:  vil = user.village_pk if user.location_level_code == 'VIL' else None 
    
    return {'province_pk': prv, 'district_pk': dst, 'facility_pk': hc,
            'referral_facility_pk': hp, 'sector_pk': sec, 'cell_pk': cel, 'village_pk': vil}

  @staticmethod
  def generatedPassword(passwd):
    salt  = str(random.random()).join([str(random.random()) for x in range(SALT_STRENGTH)])
    rslt  = sha.sha('%s%s' % (salt, passwd))
    return [salt, rslt.hexdigest()]

  @staticmethod
  def kdf(turashize):
    gakire = PBKDF2HMAC(
           algorithm=hashes.SHA256(),
           length=32,
           salt=turashize,
           iterations=100000,
           backend=default_backend()
       )
    return gakire

  @staticmethod
  def get_otp(email):
    try:
      otp = random.randrange(0, 1000000, 2)
      payload = {
                  'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*1),
                  'email': email, 
                  'otp': otp
                }
      user = MchSecurity.get_user_by_email(email)
      return [user, otp, jwt.encode( payload, SECRET, algorithm='HS256' )]
    except Exception, e:
      #print e
      pass
    return None

  @staticmethod
  def get_user_by_email(email):
    try:
      user = fetch_user_by_email(email)
      return user
    except Exception, e:
      #print e
      pass
    return None
    

  @staticmethod
  def verify_otp(tkn, otp):
    try:
      payload = jwt.decode(tkn , SECRET, algorithm='HS256')
      ##print payload, otp, payload.get('otp'), type(otp), type(payload.get('otp'))
      if str(payload.get('otp')) == str(otp): return True
      return False
    except Exception, e:
      #print e
      pass
    return False

  @staticmethod
  def generatedToken(email, passwd):
    token = None
    try:
      payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*12),
                'email': email, 
                'passwd': passwd
                }
      tkn = jwt.encode( payload, SECRET, algorithm='HS256' )
      formatter = Fernet(base64.urlsafe_b64encode(MchSecurity.kdf(SECRET).derive(SECRET)))
      token = formatter.encrypt(tkn)
      ##print "TOKEN: ", token
    except Exception, e:
      pass#;#print e
    return token

  @staticmethod
  def validateToken(token):
    try:
      ktkn = base64.urlsafe_b64encode(MchSecurity.kdf(SECRET).derive(SECRET))
      ftkn  = Fernet(ktkn)
      valid = jwt.decode( ftkn.decrypt(token), SECRET, algorithm='HS256' )
      if valid:
        return valid
    except Exception, e:
      pass#; #print "VALIDATING: \n", e
    return None

  @staticmethod
  def createUser(enduser):
     
    if enduser.telephone is None: 
      raise  MchCriticalError("National ID should not be null if you need to be RapidSMS Rwanda User")
    if enduser.national_id is None: 
      raise  MchCriticalError("Telephone should not be null if you need to be RapidSMS Rwanda User")
    if enduser.email is None: 
      raise  MchCriticalError("Email should not be null if you need to be RapidSMS Rwanda User")
    if enduser.passwd is None: 
      raise  MchCriticalError("Password should not be null if you need to be RapidSMS Rwanda User")
    if enduser.role is None: 
      raise  MchCriticalError("Role should not be null if you need to be RapidSMS Rwanda User")
    
    """print {
           'telephone' : enduser.telephone,
           'national_id' : enduser.national_id,
           'role_pk': enduser.role_pk,
           'email' : enduser.email,
           'salt' : salt,
           'passwd': passwd
           }

    orm.ORM.store('enduser', {
                                }
                  )"""
    
    return True


  @staticmethod
  def authenticateUser(email = None, passwd = None, token = None):
    try:
      ##print "EMAIL: %s, PASSWD: %s , TOKEN: %s" % (email, passwd, token)
      if token:
        login = MchSecurity.validateToken(token)
        email = login.get('email')
        passwd = login.get('passwd')
      him = fetch_user(email, passwd)
      if him:
        ##print "HIM: ", him.__dict__
        return him
    except Exception, e:
      pass#; #print "\nLOGIN: \n", e, "\n"
    return None


