#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"


import re, sys, os
from optparse import OptionParser
from service.reminder.reminders import Reminder


def smn_15_reminder_main(args):
    cmd = Reminder(reminder_type = "SMN", ntype = "Severe Malaria Notification Reminder")
    nots = cmd.get_severe_malaria_notifications_15_mins_ago()
    cmd.send_reminders(nots, level_code = 'HC', role_code = 'CLN')
    cmd.send_reminders(nots, level_code = 'HC', role_code = 'HOHC' )
    cmd.send_reminders(nots, level_code = 'HD', role_code = 'LOG' )
    cmd.send_reminders(nots, level_code = 'HD', role_code = 'SUP' )
    cmd.send_reminders(nots, level_code = 'HD', role_code = 'CSUP' )
    #cmd.send_reminders(nots, level_code = 'NATION', role_code = 'HQ')
    return 0

sys.exit(smn_15_reminder_main(sys.argv))

