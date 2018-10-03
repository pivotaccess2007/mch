#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from sms import config
from sms.api.messaging.models import SMSReport, SMSReportField
from sms.api.messaging.zdmapper.messages import common
from model.enderror import Enderror

def get_sms_report_parts(sms_report = None , text = None, DEFAULT_LANGUAGE_ISO = 'rw'):
    """
        You need to return appropriate sms, per appropriate position
    """
    sms_parts = [] ## Store parts of appropriate SMS
    try:
        p = text.split(sms_report.field_separator)### use defined SMS separator to split our sms into parts
        ans = []###store parts that has data
        i = 0 ## i position in parts
        while i < len(p):
            an = p[i]
            if an:
                ans.append(an.strip())
            i += 1
        ### Push all our parts into correct position based on the SMSReport of the Database
        sms_parts = ans
    except Exception, e:
        return e
        
    return sms_parts


def putme_in_sms_reports(sms_report = None, sms_parts = None, DEFAULT_LANGUAGE_ISO = 'rw'):
    positioned_sms = []
    i = 0
    fields = SMSReportField.objects.filter(sms_report = sms_report)
    ##DO I exists as a key the SMSReport?? Then push me to the right position, else leave me where the CHW choose to report me
    while i < len(sms_parts):
        val = sms_parts[i]
        found = False
        try:
            for fp in fields:
                #print val, fp
                ### get in field the ones with key 
                if ( val == fp.key or val.lower() == fp.key ) and i == fp.position_after_sms_keyword:
                    #print val, fp, i, fp.position_after_sms_keyword
                    positioned_sms = get_my_position(sms_report, positioned_sms, fp, val)
                    #print positioned_sms
                    found = True
                    break
                elif ( val == fp.key or val.lower() == fp.key ) and i != fp.position_after_sms_keyword:
                    #print val, fp, i, fp.position_after_sms_keyword
                    positioned_sms = get_my_position(sms_report, positioned_sms, fp, val, i)
                    #print positioned_sms
                    found = True
                    break
                ### get field with prefix based on data
                elif fp.prefix:
                    if val.__contains__(fp.prefix) or val.__contains__(fp.prefix.upper()):
                        #print val, fp, i, fp.position_after_sms_keyword
                        positioned_sms = get_my_position(sms_report, positioned_sms, fp, val)
                        #print positioned_sms
                        found = True                        
                        break
           
            ### if not found get field at the position then
            if found == False:
                #print val
                sf = SMSReportField.objects.filter(sms_report = sms_report, position_after_sms_keyword = i)
                key = ''
                if sf.count() > 1:
                    key = val
                elif sf.count() == 1:
                    key = sf[0].key#; print sf
                positioned_sms.append({'position': i, 'value': val, 'key': key })            
                
        except Exception, e:
            print e, val
        i += 1 
    return positioned_sms
        

def get_my_position(sms_report, positioned_sms, fp, val, index_of_val = None, DEFAULT_LANGUAGE_ISO = 'rw'):
    found = False
    if len(positioned_sms) > 0:         
        for ps in positioned_sms:
            fps_at_index = sms_report.smsreportfield_set.filter(position_after_sms_keyword = index_of_val)
            if index_of_val and val.strip().lower() in [ x.key for x in fps_at_index]:
                    #print index_of_val, val, fp.position_after_sms_keyword
                    positioned_sms.insert(index_of_val, {'position': index_of_val, 'value': val, 'key': fp.key})
                    found = True
                    break   
            elif ps['position'] == int(fp.position_after_sms_keyword) :
                new_val = '%s%s%s' % ( ps['value'], sms_report.field_separator, val)
                key_val = ps['key']
                if fp.key in key_val.split(sms_report.field_separator): pass
                else:
                    #print ps['position'], fp.key, fp.position_after_sms_keyword
                    key_val = '%s%s%s' % ( ps['key'], sms_report.field_separator, fp.key )
                positioned_sms[positioned_sms.index(ps)] = {'position': int(fp.position_after_sms_keyword), 'value': new_val, 'key': key_val}
                found = True
                break
            else:
                continue
        if found == False  :
            positioned_sms.append({'position': int(fp.position_after_sms_keyword), 'value': val, 'key': fp.key })
    else  :
        positioned_sms.append({'position': int(fp.position_after_sms_keyword), 'value': val, 'key': fp.key })

    return positioned_sms

def get_appropriate_response( msg = None, DEFAULT_LANGUAGE_ISO = 'rw', key = 'invalid', message_type = 'unknown_error' ):
    try:
        if msg is not None:
            err = Enderror(msg.connection.identity, message_type, msg.text)
            err.save() 
        rsp = message_type, common.COMMON_MESSAGES.get(key).get(message_type).get(DEFAULT_LANGUAGE_ISO)
        #print rsp
        return rsp
    except Exception, e:
        return ["unknown_error", "Kosora ubutumwa bwawe wongere ugerageze %s" % e]

#from sms.api.messaging.utils import *
#sms = SMSReport.objects.get(pk = 1)
#text = 'PRE            1198270072829064                 25.08.2013           11.11.2013        03 02        NR GS YG NP MA DI CL HP WT64.0 HT115 TO NT NH HW 0788660270'
#p = get_sms_report_parts(sms, text)
#pp = putme_in_sms_reports(sms, p)
    
