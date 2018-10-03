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

	"current_symptoms": {
				"missing_current_symptoms": {"en": "Reported Symptoms are missing", "rw": "Harabura ikimenyetso cy'ibibazo yari afite", "fr": ""},
				"invalid_current_symptom": {"en": "Please check that you have the correct type of reported symptom or symptoms in the appropriate place in your Result Report. These can be VO, PC, OE, NS, MA, JA, FP, FE, DS, DI, SA, RB, HY, CH, and AF. If you have more than 1 they must be separated by a space.", 
							"rw": "Ku bimenyetso by'ibibazo kuri iyi nda, hitamo muri ibi: VO, PC, OE, NS, MA, JA, FP, FE, DS, DI, SA, RB, NP, HY, CH, AF, iyo birenze kimwe siga akanya hagati", "fr": ""},
				"incoherent_np_symptom": {"en":"NP can't be reported as RISK Result", 
							"rw": "Ikimenyetso cya NP ntigitangwa ku butumwa bw'ibimenyetso mpuruza", "fr": ""}
		},

	"location": {
			"missing_location": {"en": "Location Is missing", "rw": "Harabura aho umubyeyi aherereye", "fr": ""},
			"invalid_location": {"en": "Please be sure that you have entered the appropriate Result Report location. It should be HO, HP, OR, HC.",
						"rw": "Aho umubyeyi aherereye hagomba kuba(HO,HP,HC, OR)", "fr": ""}
			},
	
	"intervention": {
			"missing_intervention": {"en": "Intervention Code Is missing", "rw": "Harabura ikimenyetso cy'ubutabazi yahawe", "fr": ""},
			"invalid_intervention": {"en": "Please be sure that you have entered the appropriate Result Report intervention code. It should be AA or PR.",
						"rw": "Koresha kimwe muri ibi bimenyetso ku butabazi yahawe(AA,PR)", "fr": ""}
			},
    "mother_status": {
			"missing_mother_status": {"en": "Mother Status Is missing", "rw": "Harabura ikimenyetso cy'uko umubyeyi amerewe", "fr": ""},
			"invalid_mother_status": {"en": "Please be sure that you have entered the appropriate Mother Status Code. It should be MW or MS",
						"rw": "Koresha kimwe muri ibi bimenyetso by'uko umubyeyi amerewe(MW,MS)", "fr": ""}
			}
	}	



