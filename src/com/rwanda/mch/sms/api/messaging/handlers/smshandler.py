#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


##DJANGO LIBRARY
from django.utils.translation import activate, get_language
from django.utils.translation import ugettext as _
from django.conf import settings
import sys, traceback
from datetime import datetime

###DEVELOPED APPS
from sms.api.messaging.utils import get_appropriate_response, SMSReport
from sms.api.messaging.handlers.smsreportkeywordhandler import SMSReportKeywordHandler, Enduser
from rapidsms.conf import settings as RAPIDSMS_SETTINGS
from sms.api.messaging.smsparser import read_fields, process_fields
from sms.api.messaging.smsprocessor import Rectifier
from sms.api.messaging.controls import CONTROLS
from sms.api.messaging.persister import Persister
from service.malaria.sm import SM
from service.stock.st import ST
from service.notification.who import WHO
from model.enderror import Enderror

from sms.api.messaging.zdmapper.messages.common import COMMON_MESSAGES
from sms.api.messagelog.models import Message


DEFAULT_LANGUAGE_ISO = settings.DEFAULT_LANGUAGE_ISO
RAPIDSMS_SETTINGS.DEFAULT_RESPONSE = "RAPIDSMS RWANDA 1000 , Ntabwo ishoboye gusobanukirwa n'ubutumwa bwawe"

class SMSReportHandler (SMSReportKeywordHandler):
    """
    RAPIDSMS RWANDA 1000 Handler
    """

    keyword = settings.DEFINED_REPORTS
    
    def filter(self):
        """ CHECK IF WE HAVE A CONNECTION FOR THE SENDER """
        if not getattr(msg, 'connection', None):
            #print "ERROR OF CHW CONNECTION "
            self.respond(get_appropriate_response( msg = self.msg, DEFAULT_LANGUAGE_ISO = self.language,
                                                     message_type = 'sender_not_connected')[1])
            return True 
    def help(self):
        try:
            sms_report = SMSReport.objects.get(keyword = self.sms_report_keyword)
            self.respond(get_appropriate_response( msg = self.msg, DEFAULT_LANGUAGE_ISO = self.language,
                                                     key = 'help', message_type = sms_report.keyword)[1])
        except Exception, e:
            self.respond(get_appropriate_response( msg = self.msg, DEFAULT_LANGUAGE_ISO = 'rw', message_type = 'unknown_error')[1])

    def handle(self, text):
        try:
            response_msg = self.yemeze(self.msg)
            self.respond(response_msg)
            #Enduser.send_message(self.reporter.telephone, response_msg)#; print response_msg
            #outgoing = Message(connection = self.msg.connection, date = datetime.now(),
            #                     transferred = True, direction = 'O', text = response_msg)
            #outgoing.save()
        except Exception, e:
            #print e
            self.respond(get_appropriate_response( msg = self.msg, DEFAULT_LANGUAGE_ISO = self.language, message_type = 'unknown_error')[1])
        return True

    def yemeze(self, message):
        response_msg = "Ikosa, reba ko wanditse ubutumwa neza wongera ugerageze."
        try:
            text = message.text
            #resp = read_fields(text)
            resp = process_fields(text)
            smsdict = resp[2]
            codes = resp[1]
            report = resp[0]
            errors = resp[3]
            
            if self.sms_report_keyword in ['SMN', 'SMR', 'RSO', 'SO', 'SS', 'WHO']:
                
                if self.sms_report_keyword in ['SMN', 'SMR']:
                    sm = SM(self.reporter, text)
                    response1 = sm.process()
                    response_msg = sm.get_response()#;print response1
                    return response_msg
                elif self.sms_report_keyword in ['RSO', 'SO', 'SS']:
                    st = ST(self.reporter, text)                
                    response2 = st.process()
                    response_msg = st.get_response()#;print response2
                    return response_msg
                elif self.sms_report_keyword in ['WHO']:
                    who = WHO(self.reporter, text)                
                    response3 = who.process()
                    response_msg = who.get_response()#;print response3, response_msg
                    return response_msg
                else: pass

            if ( smsdict.get('single') is None and smsdict.get('child') is None) or errors:
                try:
                    response_msg = COMMON_MESSAGES.get('invalid').get('invalid_sequence').get(self.language) % {'err': ''.joins(errors)}
                    
                except Exception, e:
                    pass
                    
            cs = {}
            
            rectifier = Rectifier(self.reporter, message, report, codes, smsdict, errors)
            ## validate reporter rights
            rectifier.validate_reporter()
            if rectifier.errors:
                cs['error'] = rectifier.errors
                if cs['error']:
                    rcds = Enderror.record_enderrors(self.reporter, text, cs['error'])
                    ans = [ c[1]  for c in cs['error'] if c[1] ]
                    response_msg = ", ".join("%s" % msg  for msg in set(ans) )
                    return response_msg
                else:
                    pass
                
            controller = CONTROLS.get(self.sms_report_keyword)(rectifier)
            #print "HERE", controller.errors

            try:    cs['error'] = controller.errors
            except Exception, e: pass

            #print cs
            if cs['error']:
                rcds = Enderror.record_enderrors(self.reporter, text, cs['error'])
                ans = [ c[1]  for c in cs['error'] if c[1] ]
                response_msg = ", ".join("%s" % msg  for msg in set(ans) )
                return response_msg
            
            else:
                # We need to save report in DB
                persister = Persister(controller).save()
                #print persister.__dict__
                if persister.pointeur:
                    Enduser.update_user_info({'national_id': self.reporter.national_id,
                                             'telephone': self.reporter.telephone,
                                             'last_seen': message.date
                                            })
                    response_msg = get_appropriate_response( msg = self.msg, DEFAULT_LANGUAGE_ISO = self.language, key = 'success',
                                                         message_type = self.sms_report_keyword
                                                    )[1]
                else:
                    response_msg = get_appropriate_response( msg = self.msg, DEFAULT_LANGUAGE_ISO = self.language,
                                                             message_type = 'unknown_error')[1]

                return response_msg         
        except Exception, e:
            pass      
        return response_msg

