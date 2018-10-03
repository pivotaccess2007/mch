#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

from sms.api.messaging.smsparser import *
from sms.api.messaging.smsprocessor import *
from model.enduser import Enduser
from sms.api.messagelog.models import Message
from rapidsms.models import Connection
from sms.api.messaging.persister import Persister

#identity = '+250782904295' #ASM
#identity = '+250782923741' #BINOME
identity = '+250788660270'
chw      = Enduser.get_active_user(identity)
REPORTS =  [
('PRE' , 'pre 1199270180887099 09.12.2017 10.09.2018 5 1 GS rm yg ol ma vo oe ns HC wt80.6 ht180 to hw muac14.5 0788660270'),
('DEP'  , 'DEP 1234007890123457'),
('DEP_CHILD'  , 'DEP 1234567890123457 01 09.01.2015'),
('REF'  , 'REF 0234567890123457'),
('ANC'  , 'ANC 5234567899124999 05.07.2015 anc2 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF hc wt65.5 muac12.5'),
('RISK'  , 'RISK 0788660270010918 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF or wt70'),
('RES'  , 'RES 0788660270010918 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF hp AA MW'),
('RED' , 'RED 0788660270010918 AP CO HE LA MC PA PS SC SL UN shb sfh OR wt55.5'),
('RED_CHILD' , 'RED 0788660270010918 01 13.01.2015 AP CO HE LA MC PA PS SC SL UN shb sfh OR wt5.5'),
('RAR' , 'RAR 0788660270010918 AP CO HE LA MC PA PS SC SL UN HO AL MW'),
('RAR_CHILD' , 'RAR 0788660270010918 01 13.01.2015 AP CO HE LA MC PA PS SC SL UN HO AL CW'),
('BIR'  , 'BIR 0788660270010918 01 04.09.2018 BO SB RB AF CI CM IB DB PM hp NB wt2.5'),
('CBN' , 'CBN 0788660270010918 01 04.09.2018 EBF WT4.1 MUAC6.6'),
('CHI' , 'CHI 0788660270010918 01 04.09.2018 V2 VI AF CI HO WT4.5 MUAC5.4'),
('CHI_CHILD' , 'CHI 0788660270010918 01 04.09.2018 NV HO WT4.5 MUAC5.4'),
('DTH' , 'DTH 0788660270010918 01 04.09.2018 HO ND'),
('DTH_CHILD' , 'DTH 0788660270010918 HO MD'),
('NBC' , 'NBC 0788660270010918 01 NBC3 OYA 09.09.2015 OYA SB RB AF CI CM FE HY JA NS PM NB PR CS'),
('PNC' , 'PNC 0788660270010918 PNC2 OYA 09.09.2015 VO PC OE NS MA JA FP FE DS DI SA RB HY CH AF PR MW'),
('CCM' , 'CCM 0788660270010918 01 04.09.2018 PC MA DI OI  PR MUAC5.2'),
('CMR' , 'CMR 0788660270010918 01 04.09.2018 PC MA DI OI  PR CW'),
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

an = REPORTS[3]
text = an[1]
resp = read_fields(text)
smsdict = resp[2]
codes = resp[1]
report = resp[0]
errors = resp[3]
connection = Connection.objects.get(identity = identity, backend_id = 1)
message, created = Message.objects.get_or_create( text  = text, direction = 'I', connection = connection, date = datetime.datetime.now() )

rectifier = Rectifier(chw, message, report, codes, smsdict, errors)

rectifier.validate_reporter() ## out of this area
rectifier.validate_nid(position = 1)
rectifier.validate_duplicate_report()


print rectifier.errors

cbn = Persister(rectifier).save()
