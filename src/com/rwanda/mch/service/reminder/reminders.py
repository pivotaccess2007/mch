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

from util.record import filter_data, fetch_active_user
from service.message.messages import REMINDER
from service.notification.notifications import Notification
import datetime


class Reminder(object):
  
  def __init__(self, message = "RSMS Reminder", chw = None, national_id = None, reminder_type = "SMN", ntype = "Reminder"):
    """ message is always a dict with three language as keys """
    self.chw      = chw
    self.message  = message
    self.national_id  = national_id
    self.ntype = ntype
    self.reminder_type = reminder_type

  def send_reminders(self, nots, level_code = None, role_code = None, location_pk = None, reminder_type = 'SMN', ntype = "Reminder"):
    try:
      for nt in nots:
        #print nt.__dict__
        try:      
          if hasattr(nt, 'user_phone'): self.chw = fetch_active_user(nt.user_phone)
          if hasattr(nt, 'national_id'): self.national_id = nt.national_id
          message = REMINDER.get(reminder_type)
          cmd = Notification( message = message, chw = self.chw, national_id = self.national_id, ntype = ntype)
          if level_code and role_code and self.chw and not location_pk: cmd.notify_level(level_code, role_code, self.chw.facility_pk )
          if level_code and role_code and location_pk: cmd.notify_level(level_code, role_code, location_pk )
          elif level_code and role_code and not self.chw: cmd.notify_level(level_code, role_code, None )
          else: cmd.notify_level(level_code, None, None ) 
        except Exception, e:
          print "SEND REMINDER MESSAGE : ", e
        continue
      return True
    except Exception, e:
      print "SEND REM: ", e
    return False
  
  def get_severe_malaria_notifications_15_mins_ago(self):
      try:
        start, end = datetime.datetime.now() - datetime.timedelta(minutes=15), datetime.datetime.now()
        nots = filter_data('malaria', filters = {"keyword = %s": 'SMN', "created_at >= %s ": start, "created_at <= %s ": end})
        return nots
      except Exception, e:
        print "SMN REM 15 MINS AGO: ", e
      return []
