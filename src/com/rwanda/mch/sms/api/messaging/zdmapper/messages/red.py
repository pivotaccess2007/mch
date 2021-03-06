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
            "duplicate_birth": { "en": "Child Number %(chino)s, born on %(dob)s has already been report as BIR %(nid)s",
						"rw": "Nimero %(chino)s y'uyu mwana, wavutse kuri %(dob)s yaratanzwe kuri uwo mubyeyi %(nid)s.", "fr": ""},

            
			},

	"red_symptoms": {
				"missing_red_symptoms": {"en": "Current Symptoms are missing", "rw": "Harabura ibimenyetso simusiga", "fr": ""},
				"invalid_red_symptom": {"en": "Please check that you have the correct type of current symptom or symptoms in the appropriate place in your Red Alert Report. These can be AP, CO, HE, LA, MC, PA, PS, SC, SL and UN. If you have more than 1 they must be separated by a space.", 
							"rw": "Ku bimenyetso simusiga, hitamo muri ibi: AP, CO,HE,LA, MC, PA, PS,SC,SL,UN, SHB, SFH,COP, HFP, SBP, SHP,BSP, CON, WU, HBT, LBT, CDG, YS, NUF, NCB, IUC, RV, ADS, NSC, NBF, NHE, SP, iyo birenze kimwe siga akanya hagati", "fr": ""},
				"incoherent_red_np_symptom": {"en":"NP can't be reported as Red Alert", 
							"rw": "Ikimenyetso cya NP ntigitangwa ku butumwa bw'ibimenyetso simusiga", "fr": ""}
		},

	"location": {
			"missing_location": {"en": "Location Is missing", "rw": "Harabura aho umubyeyi cyangwa umwana aherereye", "fr": ""},
			"invalid_location": {"en": "Please be sure that you have entered the appropriate Red Alert location. It should be HO or OR. A women already in HC or HP can't be in Red alert",
						"rw": "Aho umubyeyi cyangwa umwana aherereye hagomba kuba mu rugo cyangwa mu nzira (HO,OR)", "fr": ""}
			},
	
	"mother_weight": {
				"missing_mother_weight": {"en": "Mother weight Is missing", "rw": "Harabura ibiro by'umubyeyi" , "fr": ""},
				"invalid_mother_weight": {
		"en": "The weight of the mother should be in the format of WT##,WT##.#, WT### or WT###. #. Please double check if you have provided correct weight.",
				      "rw": "Ibiro by'umubyeyi bigomba kwandikwa kuri ubu buryo: WT##, WT##.#, WT### or WT###.#", "fr": ""}
				},

    "child_weight": {
				"missing_child_weight": {"en": "Child weight Is missing", "rw": "Harabura ibiro by'umwana" , "fr": ""},
				"invalid_child_weight": {
		"en": "Please be sure you have entered the child weight without units of KG. It should include be in the format of WT## or WT##.# and between 1 &25 with having no comma.",
				      "rw": "Ibiro by'umwana bigomba kwandikwa muri ubu buryo (WT# cyangwa WT#.#) kandi ibiro bigomba kuba hagati ya 1 na 25", "fr": ""}
				}
	}	



