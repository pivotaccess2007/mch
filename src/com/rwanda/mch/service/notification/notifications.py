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

from util.record import fetch_users_per_level, fetch_users_per_level_and_role, fetch_users_ids_with_privilege, fetch_privilege, fetch_location_level, fetch_role, fetch_users
from model.enduser import Enduser


class Notification(object):

  def __init__(self, message = "RSMS Notification", chw = None, national_id = None, drugs = None, symptom = None, ntype = "Notification"):
    """ message is always a dict with three language as keys """
    self.chw      = chw
    self.message  = message
    self.national_id  = national_id
    self.drugs        = drugs
    self.symptom    = symptom
    self.ntype = ntype

  def notify_level(self, level_code, role_code, location_pk):
    """ level codes :  'NATION', 'PRV', 'DST', 'NRH', 'MH', 'HD', 'HP', 'HC', 'CL', 'SEC', 'CEL', 'VIL' """
    try:
      unsent = []
      users = []
      if level_code and role_code and location_pk:
        #print "HERE", level_code, role_code, location_pk
        users = fetch_users_per_level_and_role(level_code = level_code, role_code = role_code, pk = location_pk)
      elif level_code and location_pk:
        #print "HERE", level_code, location_pk
        users = fetch_users_per_level(level_code = level_code, pk = location_pk)
      else:
        #print "HERE", level_code
        users = fetch_users_per_level(level_code = level_code)
      print [(u.telephone, u.role_name, u.facility_name) for u in users]
      for u in users:
        try:
          #print u.__dict__
          message = self.format_message(u)
          sent = False
          if level_code == 'HQ':
            print "Destination %s, Email: %s" % (u.email, message)
            sent = Enduser.send_email(self.ntype, email, message)
          else:
            print "Destination %s, SMS: %s" % (u.telephone, message)
            sent = Enduser.send_message(u.telephone, message)
          
          if not sent:
            unsent.append(u.telephone)
        except Exception, e:
          print "SEND MESSAGE TO USER: ", e
        continue
      #print "UNSENT : ", unsent
      return True
    except Exception, e:
      print "NOTIF_LEVEL", e
    return False

  def notify_level_by_email(self, level_code, role_code, location_pk):
    """ level codes :  'NATION', 'PRV', 'DST', 'NRH', 'MH', 'HD', 'HP', 'HC', 'CL', 'SEC', 'CEL', 'VIL' """
    try:
      unsent = []
      users = []
      if level_code and role_code and location_pk:
        #print "HERE", level_code, role_code, location_pk
        users = fetch_users_per_level_and_role(level_code = level_code, role_code = role_code, pk = location_pk)
      elif level_code and location_pk:
        #print "HERE", level_code, location_pk
        users = fetch_users_per_level(level_code = level_code, pk = location_pk)
      else:
        #print "HERE", level_code
        users = fetch_users_per_level(level_code = level_code)
      print [u.email for u in users]
      for u in users:
        try:
          #print u.__dict__
          message = self.format_message(u)
          #print "Destination %s, Email: %s" % (u.email, message)
          sent = Enduser.send_email(self.ntype, u.email, message)
          if not sent:
            unsent.append(u.email)
        except Exception, e:
          print "SEND MESSAGE TO USER: ", e
        continue
      #print "UNSENT : ", unsent
      return True
    except Exception, e:
      print "NOTIF_LEVEL", e
    return False

  def notify_level_per_privilege(self,level_code = None,role_code = None,privilege_code = None,location_pk = None, chw_pk = None, sms = True ):
    u = None    
    try:
      users_ids = []
      filters = {}
      #print level_code, privilege_code
      if level_code:
        level = fetch_location_level(level_code)
        if level: filters.update({'location_level_pk = %s': level.indexcol})

      if role_code:
        role  = fetch_role(role_code)
        if role:  filters.update({'role_pk = %s': role.indexcol})

      if location_pk:
        if level_code == 'NATION': filters.update({'nation_pk = %s': location_pk})
        if level_code == 'PRV': filters.update({'province_pk = %s': location_pk }) 
        if level_code == 'DST': filters.update({'district_pk = %s': location_pk })
        if level_code == 'NRH': filters.update({'facility_pk = %s': location_pk })
        if level_code == 'MH':  filters.update({'facility_pk = %s': location_pk })
        if level_code == 'HD':  filters.update({'referral_facility_pk = %s': location_pk })
        if level_code == 'HP':  filters.update({'facility_pk = %s': location_pk })
        if level_code == 'HC':  filters.update({'facility_pk = %s': location_pk })
        if level_code == 'CL':  filters.update({'facility_pk = %s': location_pk })
        if level_code == 'SEC': filters.update({'sector_pk = %s': location_pk })
        if level_code == 'CEL': filters.update({'cell_pk = %s': location_pk })
        if level_code == 'VIL': filters.update({'village_pk = %s': location_pk })

      if chw_pk:
        filters.update({'indexcol = %s': chw_pk})

      if privilege_code:
        privilege = fetch_privilege(privilege_code)
        users_ids = fetch_users_ids_with_privilege(filters = {'privilege_pk = %s' : privilege.indexcol})

      unsent  = []
      users   = fetch_users(filters = filters)
      
      for u in users:
        #print [ x.__dict__ for x in users_ids], [u.indexcol for u in users]
        if u.indexcol in [ x.user_pk for x in users_ids]:
          try:
            #print self.message, u.indexcol, u.telephone
            message = self.format_message(u)
            sent = False
            if not sms:
              #print "Destination %s, Email: %s" % (u.email, message)
              sent = Enduser.send_email(self.ntype, email, message)
            else:
              #print "Destination %s, SMS: %s" % (u.telephone, message)
              sent = Enduser.send_message(u.telephone, message)
            
            if not sent:
              unsent.append(u.telephone)
          except Exception, ex:
            print "SEND MESSAGE TO USER: %s" % ex, self.chw.sector_name
            continue
          
        else:
          continue
      return True
    except Exception, e:
      print "NOTIFY_LEVEL_PRIVILEGE : %s" % e
    return False


  def format_message(self, user):
    try:
      #print self.message
      keys = {}
      loc_str = ""
      if user:
        #print user.indexcol, user.telephone, user.referral_name
        loc_str = "Sector: %s, cell: %s, village: %s" if user.language_code.lower() == 'en' else "Murenge: %s, Akagari: %s, Umudugudu: %s"
        message = self.message.get(user.language_code.lower())
      if self.chw:
        keys.update({"phone": self.chw.telephone})
      if self.national_id:
        keys.update({'patient': self.national_id})
        keys.update({"nid": self.national_id})

      if self.drugs:
        keys.update({"drugs": self.drugs})

      if self.symptom:
        keys.update({"symptom": self.format_symptom(user)})

      if self.chw:
        keys.update({'chw': self.chw.telephone})
        keys.update({'district': self.chw.district_name})
        keys.update({'sector': self.chw.sector_name})
        keys.update({ 'cell': self.chw.cell_name})
        keys.update({ 'village': self.chw.village_name})
        keys.update({'location': loc_str % (self.chw.sector_name, self.chw.cell_name, self.chw.village_name) })
     
      #print " MESSAGE AND KEYS: ", self.message, keys
      if keys: return message % keys
      return self.message      
    except Exception, e:
      print "FORMAT MESSAGE : %" % e
    return self.message

  def format_symptom(self, user):
    try:
      symptom = ", ".join(getattr(s, 'name_%s'%user.language_code.lower()) for s in self.symptom)
      return symptom
    except Exception, e:
      print "FORMAT SYMPTOM : %s" % e
    return ""
  
  

  


