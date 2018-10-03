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
			"birth_date_lesser_lmp": {"en": "Date of Birth for this patient should be greater than PRE.LastMenstrualPeriod",
				"rw": "Itariki y'amavuko igomba kuba iruta itariki yanyuma y'imihango", "fr": ""},
            "duplicate_birth": { "en": "Child Number %(chino)s, born on %(dob)s has already been report as BIR %(nid)s",
						"rw": "Nimero %(chino)s y'uyu mwana, wavutse kuri %(dob)s yaratanzwe kuri uwo mubyeyi %(nid)s.", "fr": ""},

            
			},

    "gender": {
			"missing_gender": {"en": "Gender Is missing", "rw": "Harabura ikimenyetso kigaragaza hungu cyangwa kobwa", "fr": ""},
			"invalid_gender": {"en": "Please be sure that you have entered the appropriate Gender Code. It should be BO or GI",
						"rw": "Suzuma neza niba wakoresheje ikimenyetso nyacyo ku gitsina cy'umwana(BO cyangwa GI)", "fr": ""}
			},

	"current_symptoms": {
				"missing_current_symptoms": {"en": "Current Symptoms are missing", "rw": "Harabura ibimenyetso by'ibibazo", "fr": ""},
				"invalid_current_symptom": {"en": "Please check that you have the correct type of current symptom or symptoms in the appropriate place in your Birth Report. These can be RB, NP, AF, CI, CM and PM. If you have more than 1 they must be separated by a space.", 
							"rw": "Ku bimenyetso by'ibibazo , hitamo muri ibi: RB, NP, AF, CI, CM cyangwa PM, iyo birenze kimwe siga akanya hagati", "fr": ""},
				"incoherent_np_symptom": {"en":"If NP is reported then other codes can't be reported as Current Symptoms", 
							"rw": "Iyo ukoresheje ikimenyetso NP, ntakindi kimenyetso gikoreshwa", "fr": ""},
                "duplicate_symptom": { "en": "These codes: %(codes)s are duplicated and shall be reported only once",
						"rw": "Nta kimenyetso kigomba kwandikwa 2 mu butumwa bumwe: %(codes)s", "fr": ""},
		},

	"location": {
			"missing_location": {"en": "Location Is missing", "rw": "Harabura aho yabyariye", "fr": ""},
			"invalid_location": {"en": "Please be sure that you have entered the appropriate Birthlocation. It should be HO, HP, OR, HC or CL.",
						"rw": "Aho yabyariye hagomba kuba(HO, OR,HP,HC)", "fr": ""}
			},

	"breastfeeding": {
			"missing_breastfeeding": {"en": "Breastfeeding Is missing", "rw": "Harabura ikimenyetso cyo konsa mu isaha ya mbere y'amavuko", "fr": ""},
			"invalid_breastfeeding": {"en": "Please be sure that you have entered the appropriate Breastfeeding Code. It should be BF1 or NB",
						"rw": "Reba ko wakoresheje ikimenyetso cyo konsa gikwiye (NB cyangwa BF1)", "fr": ""}
			},	

    "child_weight": {
				"missing_child_weight": {"en": "Child weight Is missing", "rw": "Harabura ibiro by'umwana" , "fr": ""},
				"invalid_child_weight": {
		"en": "Please be sure you have entered the child weight without units of KG. It should include be in the format of WT#.# or WT#.# and between 1 &9.9 with having no comma.",
				      "rw": "Ibiro by'umwana bigomba kwandikwa muri ubu buryo (WT# cyangwa WT#.#) kandi ibiro bigomba kuba hagati ya 1 na 9.9", "fr": ""}
				}
	}	



