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

	"anc_date": {
			"anc_date_missing": {"en": "Date of ANC visit Is missing", "rw":"Harabura itariki yipimishirijeho","fr": ""},
			"misformat_anc_date" : {"en": "Please provide Date of ANC visit in this format dd.mm.yyyy",
				"rw": "Itariki yipimishirijeho yandikwa muri ubu buryo(itariki. Ukwezi. Umwaka)", "fr": ""},
			"anc_date_greater_currentdate": {"en": "Date of ANC visit can't be a future date", 
				"rw": "Itariki yipimishirijeho igomba kuba uyu munsi cyangwa mbere yaho )", "fr": ""},
			"anc_date_later_edd": {"en": "Date of ANC visit for this patient should be less than PRE.LastMenstrualPeriod+9 Months(Date)",
				"rw": "Itariki yipimishirijeho igomba kuba itarengeje amezi 9 uhereye ku itariki yanyuma y'imihango", "fr": ""},
			"anc_date_lesser_lmp": {"en": "Date of ANC visit for this patient should be greater than PRE.LastMenstrualPeriod",
				"rw": "Itariki yipimishirijeho igomba kuba iruta itariki yanyuma y'imihango", "fr": ""},
            "anc_date_lesser_lastanc": {"en": "Date() of this ANC visit of this patient should be greater than the date() of last ANC visit", 
                                            "rw": "Itariki yipimishirijeho ku nshuro ya 3 cyangwa 4 igomba kuba iruta iyo aheruka kwipishirizaho", "fr": ""}			
			},

	"anc_visit": {
			"missing_anc_visit": { "en": "Number of ANC visit Is missing", "rw": "Harabura umubare w'inshuro yipimishije (ANC2, ANC3, ANC4)", "fr": ""},
			"invalid_anc_visit": {  "en": "Number of ANC visit can either be ANC2, ANC3 or ANC4", 
						"rw": "Ikimenyetso cyo gusubira kwipimisha kigomba kubakimwe muri ibi(ANC2, ANC3, ANC4)", "fr": ""},
			"duplicate_anc_visit": { "en": "You have already reported ANC%(visit)s for this patient before",
						"rw": "Ubutumwa bwo gusubira kwipimisha ku nshuro ya %(visit)s warabutanze", "fr": ""},
			"invalid_sequence": { "en": "ANC%(visit)s can't be reported unless ANC%(pre_visit)s has been reported",
						"rw": "Ntushobora gutanga ubutumwa bwo gusubira kwipimisha ANC%(visit)s utaratanze ubububanziriza ANC%(pre_visit)s ", "fr": ""}
		},

	"current_symptoms": {
				"missing_current_symptoms": {"en": "Current Symptoms are missing", "rw": "Harabura ibimenyetso kuri iyi nda", "fr": ""},
				"invalid_current_symptom": {"en": "Please check that you have the correct type of current symptom or symptoms in the appropriate place in your ANC message. These can be VO, PC, OE, NS, MA, JA, FP, FE, DS, DI, SA, RB, NP, HY, CH, and AF. If you have more than 1 they must be separated by a space.", 
							"rw": "Ku bimenyetso by'ibibazo kuri iyi nda, hitamo muri ibi: VO, PC, OE, NS, MA,JA, FP, FE, DS, DI, SA, RB, NP, HY, CH, AF, iyo birenze kimwe siga akanya hagati", "fr": ""},
                "duplicate_symptom": { "en": "These codes: %(codes)s are duplicated and shall be reported only once",
						"rw": "Nta kimenyetso kigomba kwandikwa 2 mu butumwa bumwe: %(codes)s", "fr": ""},
				"incoherent_jam_np_symptom": {"en":"If NP is reported then other codes can't be reported as Current Symptoms", 
							"rw": "Iyo ukoresheje ikimenyetso NP, ntakindi kimenyetso gikoreshwa ku bibazo kuri iyi nda", "fr": ""}
		},

	"location": {
			"missing_location": {"en": "Location Is missing", "rw": "Harabura aho yipimishirije", "fr": ""},
			"invalid_location": {"en": "Please be sure that you have entered the appropriate ANC location. It should be HP or HC.",
						"rw": "Aho umubyeyi yipimishirije hagomba kuba ku bitaro cyangwa ikigonderabuzima gusa", "fr": ""}
			},
	
	"mother_weight": {
				"missing_mother_weight": {"en": "Mother weight Is missing", "rw": "Harabura ibiro by'umubyeyi" , "fr": ""},
				"invalid_mother_weight": {
		"en": "The weight of the mother should be in the format of WT##,WT##.#, WT### or WT###. #. Please double check if you have provided correct weight.",
				      "rw": "Ibiro by'umubyeyi bigomba kwandikwa kuri ubu buryo: WT##, WT##.#, WT### or WT###.#", "fr": ""}
				},

    "muac": {
			"missing_muac": {"en": "MUAC Is missing", "rw": "Harabura ikimenyetso cya MUAC" , "fr": ""},
			"invalid_muac": {
	              "en": "Please be sure you have entered the MUAC without units of Cm. It should include be in the format of MUAC## or MUAC##.# and having no comma.",
			      "rw": "Reba ko wakoresheje ikimenyetso gikwiye cya MUAC.", "fr": ""}
			}

	}	



