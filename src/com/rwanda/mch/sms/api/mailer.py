#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from django.conf import settings

# Import smtplib for the actual sending function
import smtplib

MESSAGE = """From: From RapidSMS <%(from)s>
To: User <%(to)s>
Subject: %(subject)s

%(message)s
"""

class Mailer(object):
    help = "To send Email"	
	
    def send_email(self, subject, to, text):
	
        try:
            sender = settings.FROM_EMAIL
            receivers = [to]

            message = MESSAGE % {"from": sender, "to": to, "subject": subject, "message": text}

            try:
               smtpObj = smtplib.SMTP('localhost')
               #smtpObj.starttls()
               smtpObj.sendmail(sender, receivers, message)         
               print "Successfully sent email"
            except SMTPException:
               print "Error: unable to send email"            

            return True
        except Exception, e:
            print e
            return False
