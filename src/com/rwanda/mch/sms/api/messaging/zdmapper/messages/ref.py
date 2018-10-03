#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##


MESSAGES =  {
	"nid": {
		"patient_nid_missing": {"en": "Patient ID Is missing", "rw": "Harabura nimero y'indangamuntu", "fr": ""},
		"nid_not_16digits": {"en": "Patient ID must be 16 digits of national ID Or (10 digits of CHW Phone Number + 6 digits of ddmmyy)",
				"rw": "Imibare y'indangamuntu igomba kuba 16", "fr": ""},
		"phone_mismatch": {"en": "The provided phone number in Patient ID does not match your number", 
				"rw": "Nimero ya telefoni wakoresheje ukora indangamuntu ntikubaruyeho", "fr": ""},
		"misformat_dated_nid": {"en": "The provided ddmmyy in Patient ID does not match the format",
				"rw": "Uburyo wanditse itariki ukora indangamuntu sibwo(banza telefoni, itariki, ukwezi n'umwaka)", "fr": ""},
		"outrange_dated_nid": {"en": "The provided ddmmyy in patient ID should either be current date or it should be in the range of (Current Date-5)",
				"rw": "Itariki wanditse ukora indangamuntu siyo(igomba kuba iy'uyu munsi cyangwa umwe mu minsi 5 ishize)", "fr": ""},
		
		"invalid_nid": {"en": "Patient ID must be 16 digits of national ID Or (10 digits of CHW Phone Number + 6 digits of ddmmyy",
				"rw": "Inomero y'Indangamuntu igomba kuba igizwe n'imibare gusa udasize akanya", "fr": ""},
        "ref_duplicated_nid":{ "en": "Refusal report for ID%(nid)s has already been submitted",
             "rw": "Iyo ndangamuntu %(nid)s yakoreshejwe kuwundi mubyeyi", "fr": ""
            },
        "preg_not_exists_nid": { "en": "This Patient ID Number %(nid)s does not exist in the system. You can only send refusal report for registered women",
                                "rw": "Iyo ndangamuntu %(nid)s nta mubyeyi dufite muri sisitemu uyifite",
                                "fr": ""
                }
		}
	}
