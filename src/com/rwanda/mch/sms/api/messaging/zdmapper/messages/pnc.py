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
				"rw": "Inomero y'Indangamuntu igomba kuba igizwe n'imibare gusa udasize akanya", "fr": ""}
		},

	"pnc_visit": {
			"missing_pnc_visit": { "en": "Number of PNC visit Is missing", "rw": "Harabura inshuro z'isurwa ry'umubyeyi", "fr": ""},
			"invalid_pnc_visit": {  "en": "Please be sure that you have entered the appropriate PNC Code. It should be PNC1, PNC2, PNC3, PNC4 or PNC5", 
						"rw": "Suzuma neza niba wakoresheje ikimenyetso nyacyo kw'isura ry'umubyeyi(PNC1, PNC2, PNC3, PNC4 cyangwa PNC5)", "fr": ""},
			"duplicate_pnc_visit": { "en": "You have already reported PNC%(pnc_visit)s for this patient before",
						"rw": "Icyo kimenyetso PNC%(pnc_visit)s ku isura ry'umubyeyi wagitanze kuri raporo y'uyu mubyeyi", "fr": ""},
			"invalid_sequence": { "en": "PNC report for PNC%(visit)s cannot be reported unless PNC%(visit)s is reported",
						"rw": "Raporo kw'isura ry'umubyeyi PNC%(visit)s ntigomba gutangwa iyibanziriza PNC%(pre_visit)s itaratanzwe", "fr": ""},
            "outrange_pnc_visit":  {    "en": "PNC report can only be reported if Current Date-Dob is less than or equal to 28 days",
                                        "rw": "Raporo kw'isura ry'umubyeyi rigomba kutarenza iminsi 28 umwana avutse", "fr": ""
                                        }
		},
    "pnc1": {
			"missing_pnc1": { "en": "You did not tell us if the patient has received PNC1, use 'YES' or 'NO'",
                                "rw": "Ntabwo watubwiye niba uyu muntu yarakorewe PNC1, koresha iri jambo 'YEGO' cyangwa 'OYA'", "fr": ""},
			"invalid_pnc1": {  "en": "Please be sure that you have entered the appropriate PNC1 Code. It should be YES, NO",
                     "rw": "Suzuma neza niba wakoresheje ikimenyetso nyacyo kuri PNC1, kigomba kuba kimwe muri ibi(YEGO cyangwa OYA)", "fr": ""}
        },

    "delivery_date": {
			"missing_delivery_date": {"en": "Date of delivery Is missing", "rw": "Harabura itariki yabyariyeho", "fr": ""},
            "misformat_birth_date": {"en": "Date of delivery should be in this format dd.mm.yyyy",
				    "rw": "Itariki yabyariyeho yandikwa muri ubu buryo(itariki. Ukwezi. Umwaka)", "fr": ""},
		    "delivery_date_greater_currentdate": {"en": "Date of delivery should be equal to or less then current date",
                                "rw": "Itariki yabyariyeho igomba kuba itarenze iy'uyu munsi.", "fr": ""},
            "missing_delivery": {"en": "No delivery report found for this date %(dob)s",
                                 "rw": "Harabura raporo yo kubyara kuri iyo tariki %(dob)s utanze", "fr": ""},
            },

	"current_symptoms": {
				"missing_current_symptoms": {"en": "Current Symptoms are missing", "rw": "Harabura ibimenyetso by'ibibazo", "fr": ""},
				"invalid_current_symptom": {"en": "Please check that you have the correct type of current symptom or symptoms in the appropriate place in your PNC message. These can be VO, PC, OE, NS, MA, JA, FP, FE, DS, DI, SA, RB, NP, HY and CH. If you have more than 1 they must be separated by a space.", 
							"rw": "Ku bimenyetso by'ibibazo , hitamo muri ibi: VO, PC, OE, NS, MA, JA, FP, FE, DS, DI, SA, RB, NP, HY cyangwa CH, iyo birenze kimwe siga akanya hagati", "fr": ""},
				"incoherent_np_symptom": {"en":"if NP is reported then other codes can't be reported as Current Symptoms", 
							"rw": "Iyo ukoresheje ikimenyetso NP, ntakindi kimenyetso gikoreshwa", "fr": ""},
                "duplicate_symptom": { "en": "These codes: %(codes)s are duplicated and shall be reported only once",
						"rw": "Nta kimenyetso kigomba kwandikwa 2 mu butumwa bumwe: %(codes)s", "fr": ""},
		},

    "intervention": {
			"missing_intervention": {"en": "Intervention Code Is missing", "rw": "Harabura ikimenyetso cy'ubutabazi umubyeyi yahawe", "fr": ""},
			"invalid_intervention": {"en": "Please be sure that you have entered the appropriate PNC intervention code. It should be AA or PR.",
						"rw": "Reba ko wakoresheje ikimenyetso cy'ubutabazi gikwiye (AA cyangwa PR)", "fr": ""}
			},
    
    "mother_status": {
			"missing_mother_status": {"en": "Mother Status Is missing", "rw": "Harabura ikimenyetso cy'uko umubyeyi amerewe", "fr": ""},
			"invalid_mother_status": {"en": "Please be sure that you have entered the appropriate Mother Status Code. It should be MW or MS",
						"rw": "Reba ko wakoresheje ikimenyetso cy'uko umubyeyi amerewe gikwiye (MW cyangwa MS)", "fr": ""}
			}
	}	



