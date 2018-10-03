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

    "child_number": {
			"missing_child_number": {"en": "Child Number Is missing", "rw": "Harabura nimero y'umwana", "fr": ""},
			"invalid_child_number": {"en": "Please check you have the correct child number. This number should be a 2 digit number, the first digit is always 0 and second digit varies between 1-6",
						"rw": "Nimero y'umwana igomba kuba iri hagati ya 01 na 06", "fr": ""}
			},

	"birth_date": {
			"missing_birth_date": {"en": "Date of delivery Is missing", "rw": "Harabura itariki y'amavuko", "fr": ""},
            "misformat_birth_date": {"en": "Date of delivery should be in this format dd.mm.yyyy",
				    "rw": "Itariki y'amavuko yandikwa muri ubu buryo(itariki. Ukwezi. Umwaka)", "fr": ""},
		    "birth_date_greater_currentdate": {"en": "Date of delivery should be equal to or less then current date",
			                                "rw": "Itariki y'amavuko igomba kuba itarenze iy'uyu munsi.", "fr": ""},
            "duplicate_ccm": { "en": "Child Number ## has already been report as CCM on this date",
						"rw": "Iyo nimero y'umwana yarakoreshejwe kuri raporo yo kuvura", "fr": ""},
			"birth_date_mismatch": {"en": "The date of birth (date)of this child is not matching the date of delivery (date) in BIR report",
				"rw": "Itariki y'amavuko itandukanye n'iyo watanze muri raporo yo kuvuka", "fr": ""}	
            
			},

	"current_symptoms": {
				"missing_current_symptoms": {"en": "Current Symptoms are missing", "rw": "Harabura ibimenyetso by'ibibazo", "fr": ""},
				"invalid_current_symptom": {"en": "Please check that you have the correct type of current symptom or symptoms in the appropriate place in your CCM message. These can be DI, MA, PC, OI, NP, IB, DB and NV. If you have more than 1 they must be separated by a space.", 
							"rw": "Ku bimenyetso by'ibibazo , hitamo muri ibi: DI, MA, PC, OI, NP, IB, DB and NV, iyo birenze kimwe siga akanya hagati", "fr": ""},
				"incoherent_np_symptom": {"en":"If NP is reported then other codes can't be reported as Current Symptoms", 
							"rw": "Iyo ukoresheje ikimenyetso NP, ntakindi kimenyetso gikoreshwa", "fr": ""},
                "duplicate_symptom": { "en": "These codes: %(codes)s are duplicated and shall be reported only once",
						"rw": "Nta kimenyetso kigomba kwandikwa 2 mu butumwa bumwe: %(codes)s", "fr": ""},
		},

    "intervention": {
			"missing_intervention": {"en": "Intervention Code Is missing", "rw": "Harabura ikimenyetso cy'ubutabazi umwana yahawe", "fr": ""},
			"invalid_intervention": {"en": "Please be sure that you have entered the appropriate Intervention Code. It should be PT, PR, TR or AA",
						"rw": "Reba ko wakoresheje ikimenyetso cy'ubutabazi gikwiye (PT, PR, TR cyangwa AA)", "fr": ""}
			},
    
    "child_status": {
			"missing_mother_status": {"en": "Child Status Is missing", "rw": "Harabura ikimenyetso cy'uko umwana amerewe", "fr": ""},
			"invalid_mother_status": {"en": "Please be sure that you have entered the appropriate Child Status Code. It should be CW or CS",
						"rw": "Koresha kimwe muri ibi bimenyetso by'uko umwana amerewe(CW,CS)", "fr": ""}
			}
	}	



