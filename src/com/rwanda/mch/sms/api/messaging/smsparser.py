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


from underscore import _ as UNDERSCORE
from util.record import  fetch_report_codes, fetch_resource
import re


REGEXES = { 

"PRE": "pre\s+(\d+)\s+([0-9.]+)\s+([0-9.]+)\s+([0-9]+)\s+([0-9]+)\s+(.*)\s+(hp|hc)\s+(wt\d+\.?\d)\s+(ht\d+\.?\d)\s+(to|nt)\s+(hw|nh)\s+(muac\d+\.?\d)\s?(.*)",

"DEP": "dep\s+(\d+)\s?(.*)",
"DEP_CHILD": "dep\s+(\d+)\s+([0-9]+)\s+([0-9.]+)\s?(.*)",
 
"REF": "ref\s+(\d+)\s?(.*)",

"ANC": "anc\s+(\d+)\s+([0-9.]+)\s+(anc2|anc3|anc4)\s+(.*)\s+(hp|hc)\s+(wt\d+\.?\d)\s+(muac\d+\.?\d)\s?(.*)",

"RISK": "risk\s+(\d+)\s+(.*)\s+(ho|or)\s+(wt\d+\.?\d)\s?(.*)",
"RES": "res\s+(\d+)\s+(.*)\s+(hp|ho|or|hc)\s+(pr|aa)\s+(mw|ms)\s?(.*)",

"RED": "red\s+(\d+)\s+(.*)\s+(ho|or)\s+(wt\d+\.?\d)\s?(.*)",
"RED_CHILD": "red\s+(\d+)\s+([0-9]+)\s+([0-9.]+)\s+(.*)\s+(ho|or)\s+(wt\d+\.?\d)\s?(.*)",

"RAR": "rar\s+(\d+)\s+(.*)\s+(hp|hc|ho|or)\s+(al|at|na)\s+(mw|ms|cw|cs)\s?(.*)",
"RAR_CHILD": "rar\s+(\d+)\s+([0-9]+)\s+([0-9.]+)\s+(.*)\s+(hp|hc|ho|or)\s+(al|at|na)\s+(mw|ms|cw|cs)\s?(.*)",

"BIR": "bir\s+(\d+)\s+([0-9]+)\s+([0-9.]+)\s+(bo|gi)\s+(.*)\s+(ho|hp|or|hc)\s+(nb|bf1)\s+(wt\d+\.?\d)\s?(.*)",

"NBC": "nbc\s+(\d+)\s+([0-9]+)\s+(nbc2|nbc3|nbc4|nbc5)\s+(yego|oya)\s+([0-9.]+)\s+(yego|oya)\s+(.*)\s+(nb|ebf)\s+(pr|aa)\s+(cw|cs)\s?(.*)",

"PNC": "pnc\s+(\d+)\s+(pnc2|pnc3|pnc4|pnc5)\s+(yego|oya)\s+([0-9.]+)\s(.*)\s+(pr|aa)\s+(mw|ms)\s?(.*)",

"CHI": "chi\s+(\d+)\s+([0-9]+)\s+([0-9.]+)\s+(v2|v3|v4|v5|v6)\s+(vc|vi)\s+(.*)\s+(ho|hp|hc)\s+(wt\d+\.?\d)\s+(muac\d+\.?\d)\s?(.*)",
"CHI_CHILD": "chi\s+(\d+)\s+([0-9]+)\s+([0-9.]+)\s+(nv)\s+(ho|hp|hc)\s+(wt\d+\.?\d)\s+(muac\d+\.?\d)\s?(.*)",

"CCM": "ccm\s+(\d+)\s+([0-9]+)\s+([0-9.]+)\s+(.*)\s+(pr|aa|pt|tr)\s+(muac\d+\.?\d)\s?(.*)",

"CMR": "cmr\s+(\d+)\s+([0-9]+)\s+([0-9.]+)\s+(.*)\s+(pr|aa|pt|tr)\s+(cw|cs)\s?(.*)",

"CBN": "cbn\s+(\d+)\s+([0-9]+)\s+([0-9.]+)\s+(nb|ebf|cf)\s+(wt\d+\.?\d)\s+(muac\d+\.?\d)\s?(.*)",

"DTH": "dth\s+(\d+)\s+(hp|hc|or|ho)\s+(md|sbd|mcc)\s?(.*)",
"DTH_CHILD": "dth\s+(\d+)\s+([0-9]+)\s+([0-9.]+)\s+(hp|hc|or|ho)\s+(nd|cd)\s?(.*)",

"SMN": "smn\s+(\d+)\s+(.*)",

"SMR": "smr\s+(\d+)\s+(.*)\s+(pr|na|ca|al|at)\s+(ho|hc|hp)\s+(ps|dth)\s+(nr|rr)\s?(.*)",

"RSO": "rso\s+(.*)",

"SO": "so\s+(.*)",

"SS": "ss\s+(.*)",

"WHO": "who\s?(.*)"

            }


def read_multi(codem, rem_pp, group = ""):
 res = []
 for rp in rem_pp:
  if rp.strip().lower() in [c.code.strip().lower() for c in codem]: res.append(rp)
  else:
   break
 if group and not res:
  for gr in group.split():
   if gr.strip().lower() in [c.code.strip().lower() for c in codem]: res.append(gr)
   else: break
 return res

def process_fields(text):
  report, codes, sms_dict, error = None, [], {}, set()
  try:
    keyword = text.split()[0]
    report  = fetch_resource(keyword.upper()) 
    codes = fetch_report_codes(keyword.upper())
    sms_dict = { "single": re.search( REGEXES.get(keyword.upper()) , text, re.IGNORECASE )   }
    if REGEXES.get('%s_CHILD' % keyword.upper()):
      sms_dict.update({ "child": re.search( REGEXES.get('%s_CHILD' % keyword.upper()) , text, re.IGNORECASE )   })

    codes_pos = UNDERSCORE(codes).groupBy(lambda x, *args: x.position)
    maxp = max([k for k in codes_pos.keys()])
    minp = min([k for k in codes_pos.keys()]) 

    #pp = sms_dict.get('single')
    #if not pp: pp = sms_dict.get('child')
    #if pp:
    #  i = 1
    #  while i <= len(pp.groups()):
    #    sms_dict.update({i : pp.group(i)})
    #    i += 1
    #else:
      # TODO
    ## if at that position only 1 code is allowed and not a value, set it and continue
    ## if more codes are allowed and are values, read them and append to dict position
    ## and resume to the position current read in parts
    pp = text.split()    
    i = minp
    temp_index = i
    while i <= maxp:
      codem = codes_pos.get(i)
      pi = ""
      try:  pi = pp[temp_index]
      except Exception, e: pass
      #print i, temp_index, pi
      if codem:
        code = codem[0]
        if len(codem) == 1 and not code.is_value:
          temp_index += 1
          sms_dict.update({i: pi})
        elif len(codem) == 1 and code.is_value:
          temp_index += 1
          sms_dict.update({i: pi})
        elif len(codem) > 1:          
          temp = pp[temp_index:]
          found = []
          for t in temp:
            if t.lower() in [ci.code.lower() for ci in codem]:
              found.append(t)
            else:
              ## continue reading until next correct
              next_codem = codes_pos.get(i+1)
              if next_codem:
                next_code = next_codem[0]
                if t.lower() in [nci.code.lower() for nci in next_codem] or not next_code.is_value: pass
                else:
                  errors_t = []
                  for et in temp[len(found):]:
                    if et.lower() not in [nci.code.lower() for nci in next_codem + codem]: errors_t.append(et)
                    elif et.lower() in [ci.code.lower() for ci in codem]: found.append(et) 
                    else: break
                  temp_index += len(errors_t)
                  for ete in errors_t: error.add(ete) 
              break

          temp_index += len(found)            
          #print i, temp_index, temp, found
          sms_dict.update({i: ' '.join(found) })
      i += 1

  except Exception, e:
    pass

  return report, codes, sms_dict, error

"""  
  p = pp[i ]
  codem = codes_pos.get(i)
  if codem:
   code = codem[0]
   if len(codem) == 1 and not code.is_value:
    sms_dict.update({i: p})
   elif len(codem) == 1 and code.is_value and code.code.strip().lower() == p.strip().lower():
    sms_dict.update({i: p})
   elif len(codem) > 1:
    sdva  = sms_dict.get('single')
    cdva  = sms_dict.get('child')
    dva = cdva.group(i) if cdva else sdva.group(i) if sdva else None
    #read but if temp is empty, we need to check in the pattern, at the same position
    # if still if still empty we continue putting these invalides
    temp = read_multi(codem, pp[i:], group = dva)
    #print "POS: ", i, pp[i:], temp   
    if len(temp) > 1:
     #pp[ i: i + len(temp)] = []
     pp[i] = ' '.join(temp) 
     sms_dict.update({i: pp[i]})
    elif len(temp) == 1:
     #pp[i+1] = []
     pp[i] = ' '.join(temp)
     sms_dict.update({i: pp[i]})
    else:
     #print temp, p, i
     pass
  else:
   pass
  i += 1
 return sms_dict

"""

def read_fields(text):
 pp = text.split()
 keyword = pp[0]
 report  = fetch_resource(keyword.upper()) 
 codes = fetch_report_codes(keyword.upper())
 sms_dict = { "single": re.search( REGEXES.get(keyword.upper()) , text, re.IGNORECASE )   }
 if REGEXES.get('%s_CHILD' % keyword.upper()):
  sms_dict.update({ "child": re.search( REGEXES.get('%s_CHILD' % keyword.upper()) , text, re.IGNORECASE )   })
 error = set()
 temp  = []
 i = 0
 for p in pp:
  position = i
  ## check possible codes at position
  values = UNDERSCORE(codes).chain().filter(lambda x, *args: x.position == i).map(lambda x, *args: x.code.lower()).sortBy().value()
  codem   = UNDERSCORE(codes).chain().filter(lambda x, *args: x.code.lower() == p.lower()
	                                ).map(lambda x, *args: x).sortBy().value()
  ## check if this part is not the last in SMS parts
  if pp.index(p) == len(pp) - 1:
   #print "LAST", p, temp, values
   temp_set = set([x.lower() for x in temp])
   if temp:
    ## check if possible codes and temporary codes contains the last code
    if p.lower() in values and temp_set.issubset(set(values)):
     #print p, temp
     if p not in temp: temp.append(p)
    sms_dict.update({i: ' '.join(temp)})
    if p not in temp: sms_dict.update({i+1: p})
   else:
    ## the last part is not part of possible codes and temporary codes
    sms_dict.update({i: p})
   continue   
  if codem:
   code = codem[0]
   ## many codes allowed at this position, with one of them is the current part
   if code.code.lower() in values and len(values) > 1:
    temp.append(p)
    continue
   ## only one code is allowed here and it is this part
   if code.code.lower() in values and len(values) == 1:
    temp = []
    sms_dict.update({i: p})
   ## This code is not part of possible codes at this position
   if code.code.lower() not in values:
    ## is this code allowed to this position
    #print p, code.code.lower(), pp[i], temp
    if code.position == i: sms_dict.update({i: p})
    elif code.position == i+1:
     if temp:
      sms_dict.update({i: ' '.join(temp)})
     i=code.position
     temp = []
     if len(values) > 1:
      temp.append(p)
      continue
    else:
     #print p, temp
     error.add( ( p, pp[i]) ) 
     continue      
  else:
   # code is not understood as a static value, it might be a variable value
   if temp:
    sms_dict.update({i: ' '.join(temp)})
    sms_dict.update({i+1: p})
    i+= 1
   else:
    sms_dict.update({i: p})
   temp = []
  i += 1
 return report, codes, sms_dict, error


"""TEST """
"""
from sms.api.messaging.smsparser import *
from sms.api.messaging.smsprocessor import *
from model.enduser import Enduser
from sms.api.messagelog.models import Message
from rapidsms.models import Connection
from sms.api.messaging.persister import Persister

identity = '+250782904295' #ASM
#identity = '+250782923741' #BINOME
#identity = +250788660270
chw      = Enduser.get_active_user(identity)
REPORTS =  [
('PRE' , 'pre 1199270180887099 09.12.2017 10.09.2018 5 1 GS rm yg ol ma vo oe ns HC wt80.6 ht180 to hw muac14.5 0788660270'),
('DEP'  , 'DEP 1234007890123457'),
('DEP_CHILD'  , 'DEP 1234567890123457 01 09.01.2015'),
('REF'  , 'REF 0234567890123457'),
('ANC'  , 'ANC 5234567899124999 05.07.2015 anc2 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF hc wt65.5 muac12.5'),
('RISK'  , 'RISK 1234567890123090 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF or wt70'),
('RES'  , 'RES 1234567890123090 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF hp AA MW'),
('RED' , 'RED 1234567890123090 AP CO HE LA MC PA PS SC SL UN shb sfh OR wt55.5'),
('RED_CHILD' , 'RED 1234567890123090 01 13.01.2015 AP CO HE LA MC PA PS SC SL UN shb sfh OR wt55.5'),
('RAR' , 'RAR 1234567890123090 AP CO HE LA MC PA PS SC SL UN HO AL MW'),
('RAR_CHILD' , 'RAR 1234567890123090 01 13.01.2015 AP CO HE LA MC PA PS SC SL UN HO AL CW'),
('BIR'  , 'BIR 1234567890123090 01 09.09.2015 BO SB RB AF CI CM IB DB PM hp NB wt2.5'),
('CBN' , 'CBN 1234567890123090 01 09.09.2015 EBF HT45 WT4.1 MUAC4.6'),
('CHI' , 'CHI 1234567890123090 01 09.09.2015 V2 VI AF CI HO WT4.5 MUAC5.4'),
('CHI_CHILD' , 'CHI 1234567890123090 01 09.09.2015 NV HO WT4.5 MUAC5.4'),
('DTH' , 'DTH 1234567890123090 01 09.09.2015 HO ND'),
('DTH_CHILD' , 'DTH 1234567890123090 HO MD'),
('NBC' , 'NBC 1234567890123090 01 NBC3 OYA 09.09.2015 OYA SB RB AF CI CM FE HY JA NS PM NB PR CS'),
('PNC' , 'PNC 1234567890123090 PNC2 OYA 09.09.2015 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF PR MW'),
('CCM' , 'CCM 1234567890123090 01 09.09.2015 PC MA DI OI  PR MUAC5.2'),
('CMR' , 'CMR 1234567890123090 01 09.09.2015 PC MA DI OI  PR CW'),
('SMN' , 'SMN 1197458698761535 DHM NFM RDM HEM COM UNM NDM SCM PRM ANM RVM WUM TDR ARS AL4 AL2 AL3'),
('SMR' , 'SMR 1197458698761530 DHM NFM JAM SCM PRM ANM RVM WUM PR HO DTH NR'),
('RSO' , 'RSO TDR AL1 AL2'),
('SO' , 'SO TDR AL1 AL2'),
('SS' , 'SS TDR AL1 AL2'),
('WHO' , 'WHO'),
]

#for an in REPORTS:
 #resp = read_fields(an[1])
 #print resp
 #ans = resp[0]
 #ans.get('single').groups()

an = REPORTS[0]
text = an[1]
resp = read_fields(text)
smsdict = resp[2]
codes = resp[1]
report = resp[0]
errors = resp[3]
connection = Connection.objects.get(identity = identity)
message, created = Message.objects.get_or_create( text  = text, direction = 'I', connection = connection, date = datetime.datetime.now() )

rectifier = Rectifier(chw, message, report, codes, smsdict, errors)

rectifier.validate_reporter() ## out of this area
rectifier.validate_nid()
rectifier.validate_lmp()
rectifier.validate_anc2_date()
rectifier.validate_gravidity()
rectifier.validate_parity()
rectifier.validate_previous_symptoms()
rectifier.validate_current_symptoms()
rectifier.validate_location()
rectifier.validate_weight(position = 9, key = 'mother_weight', errcode = "missing_mother_weight")
rectifier.validate_height(position = 10, key = 'mother_height', errcode = "missing_mother_height")
rectifier.validate_unique_codes(position = 11, key = 'toilet', errcodes = ["missing_toilet", "invalid_toilet"] )
rectifier.validate_unique_codes(position = 12, key = 'handwashing', errcodes = ["missing_handwashing", "invalid_handwashing"] )
rectifier.validate_muac()
rectifier.mother_has_phone()
rectifier.invalid_sms_codes()
rectifier.validate_current_pregnancy()


print rectifier.errors

report = Persister(rectifier).save()

print resp
ans = resp[0]
groups = ans.get('single').groups()
print groups

"""
