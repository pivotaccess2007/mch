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

	"emergency_date": {
			"missing_emergency_date": {"en": "Date of emergency Is missing", "rw":"Harabura itariki ibimenyetso simusiga byatangiweho","fr": ""},
			"misformat_emergency_date" : {"en": "Date of emergency should be in this format dd.mm.yyyy",
				"rw": "Itariki ya RED yatangiweho yandikwa muri ubu buryo(itariki. Ukwezi.Umwaka)", "fr": ""},
			"emergency_date_greater_currentdate": {"en": "Date of emergency should be equal to or less then current date", 
				"rw": "Itariki ya RED yatangiweho igomba gusa n'iyatanzwe muri RAR", "fr": ""},
			"emergency_date_mismatch_report_date": {"en": "Date of Emergency does not match the Date of Red Alert",
				"rw": "Itariki ya RED yatangiweho igomba gusa n'iyatanzwe muri RAR", "fr": ""}		
			},

	"red_symptoms": { 
				"missing_red_symptoms": {"en": "Reported Symptoms are missing", "rw": "Harabura ibimenyetso simusiga yari afite", "fr": ""},
				"invalid_red_symptom": {"en": "Please check that you have the correct type of reported symptom or symptoms in the appropriate place in your Red Alert Result Report. These can be AP, CO,HE,LA, MC, PA, PS,SC,SL,UN, SHB, SFH,COP, HFP, SBP, SHP,BSP, CON, WU, HBT, LBT, CDG, YS, NUF, NCB, IUC, RV, ADS, NSC, NBF, NHE, SP. If you have more than 1 they must be separated by a space.", 
							"rw": "Andika neza ikimenyetso watanze muri RED, hitamo muri ibi: AP, CO,HE,LA, MC, PA, PS,SC,SL,UN, SHB, SFH,COP, HFP, SBP, SHP,BSP, CON, WU, HBT, LBT, CDG, YS, NUF, NCB, IUC, RV, ADS, NSC, NBF, NHE, SP, iyo birenze kimwe siga akanya hagati", "fr": ""},
				"incoherent_red_np_symptom": {"en":"NP can't be reported as Red Alert", 
							"rw": "Ikimenyetso cya NP ntigitangwa ku butumwa bw'ibimenyetso simusiga", "fr": ""}
		},

	"location": {
			"missing_location": {"en": "Location Is missing", "rw": "Harabura aho umwana cyangwa umubyeyi aherereye", "fr": ""},
			"invalid_location": {"en": "Please be sure that you have entered the appropriate Red Alert Result location. It should be HO, HP, HC.",
						"rw": "Aho umubyeyi cyangwa umwana aherereye hagomba kuba(HO, HP, HC)", "fr": ""}
			},
	
	"intervention": {
			"missing_intervention": {"en": "Intervention Code Is missing", "rw": "Harabura ikimenyetso cy'ubutabazi yahawe", "fr": ""},
			"invalid_intervention": {"en": "Please be sure that you have entered the appropriate Intervention Code. It should be AL, AT or NA",
						"rw": "Ikimenyetso cy'ubutabazi yahawe kigomba kuba(AL,AT cyangwa NA)", "fr": ""}
			},
    "mother_status": {
			"missing_mother_status": {"en": "Mother Status Is missing", "rw": "Harabura ikimenyetso cy'uko umubyeyi amerewe", "fr": ""},
			"invalid_mother_status": {"en": "Please be sure that you have entered the appropriate Mother Status Code. It should be MW or MS",
						"rw": "Koresha kimwe muri ibi bimenyetso by'uko umubyeyi amerewe(MW,MS)", "fr": ""}
			},
    "child_status": {
			"missing_child_status": {"en": "Child Status Is missing", "rw": "Harabura ikimenyetso cy'uko umwana amerewe", "fr": ""},
			"invalid_child_status": {"en": "Please be sure that you have entered the appropriate Child Status Code. It should be CW or CS",
						"rw": "Koresha kimwe muri ibi bimenyetso by'uko umwana amerewe(CW,CS)", "fr": ""}
			}
	}	



