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
				"missing_current_symptoms": {"en": "Current Symptoms are missing", "rw": "Harabura ibimenyetso kuri iyi nda", "fr": ""},
				"invalid_current_symptom": {"en": "Please check that you have the correct type of current symptom or symptoms in the appropriate place in your RISK Report. These can be VO, PC, OE, NS, MA, JA, FP, FE, DS, DI, SA, RB, HY, CH, and AF. If you have more than 1 they must be separated by a space.", 
							"rw": "Ku bimenyetso by'ibibazo kuri iyi nda, hitamo muri ibi: VO, PC, OE, NS, MA, JA, FP, FE, DS, DI, SA, RB, NP, HY, CH, AF, iyo birenze kimwe siga akanya hagati", "fr": ""},
				"incoherent_np_symptom": {"en":"NP can't be reported as RISK", 
							"rw": "Ikimenyetso cya NP ntigitangwa ku butumwa bw'ibimenyetso mpuruza", "fr": ""}
		},

	"location": {
			"missing_location": {"en": "Location Is missing", "rw": "Harabura aho umubyeyi aherereye", "fr": ""},
			"invalid_location": {"en": "Please be sure that you have entered the appropriate RISK location. It should be HO, OR.",
						"rw": "Aho umubyeyi aherereye hagomba kuba mu rugo cyangwa mu nzira (HO,OR).", "fr": ""}
			},
	
	"mother_weight": {
				"missing_mother_weight": {"en": "Mother weight Is missing", "rw": "Harabura ibiro by'umubyeyi" , "fr": ""},
				"invalid_mother_weight": {
		"en": "The weight of the mother should be in the format of WT##,WT##.#, WT### or WT###. #. Please double check if you have provided correct weight.",
				      "rw": "Ibiro by'umubyeyi bigomba kwandikwa kuri ubu buryo: WT##, WT##.#, WT### or WT###.#", "fr": ""}
				}
	}	



