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
            "duplicate_chi": { "en": "Child Number %(chino)s, born on %(dob)s has already been report as CHI %(nid)s",
						"rw": "Nimero %(chino)s y'uyu mwana, wavutse kuri %(dob)s, na %(nid)s yaratanzwe kuri iyi raporo yerekeye ubuzima bw'umwana.", "fr": ""},
            "birth_date_mismatch": {"en": "The date of birth (date)of this child is not matching the date of delivery (date) in BIR report",
				"rw": "Itariki y'amavuko itandukanye n'iyo watanze muri raporo yo kuvuka", "fr": ""}
            
			},

    "vaccine": {
			"missing_vaccine": {"en": "Vaccination series is missing", "rw": "Harabura ikimenyetso cy'inkingo", "fr": ""},
			"invalid_vaccine": {"en": "Please be sure that you have entered the appropriate Vaccination Series Code. It should be V1, V2, V3, V4, V5 or V6",
			"rw": "Suzuma neza niba wakoresheje ikimenyetso nyacyo ku ikingira(V1, V2, V3, V4, V5 or V6). Ntabwo byemewe gukoresha ibimenyetso birenze kimwe.", "fr": ""},
            "duplicate_vaccine_visit": { "en": "You have already reported V%(visit)s for this child before",
						"rw": "Ubutumwa ku rukingo V%(visit)s warabutanze kuri uyu mwana", "fr": ""},            
            "invalid_sequence": { "en": "Vaccination code V%(visit)s cannot be reported unless V%(pre_visit)s is reported",
						"rw": "Ikimenyetso ku nkingo V%(visit)s ntikigomba gutangwa ikikibanziriza V%(pre_visit)s kitaratangwa", "fr": ""},
			},

    "vaccine_completion": {
			"missing_vaccine_completion": {"en": "Vaccination series completion status is missing", 
                                            "rw": "Harabura ikimenyetso ku mwana yahawe inkingo zose z'uwo munsi", "fr": ""},
			"invalid_vaccine_completion": {"en": "Please be sure that you have entered the appropriate Vaccination Completion Status Code. It should be VC, VI or NV",
						"rw": "Reba ko wakoresheje ikimenyetso gikwiye ku mwana wahawe inkingo zose z'uwo munsi (VC, VI cyangwa NV)", "fr": ""},
            "duplicate_vaccine_completion": { "en": "%(vaccine_completion)s Code has already been reported for V#",
						"rw": "Ubutumwa bwo gusubira kwipimisha ku nshuro ya %(vaccine_completion)s warabutanzeVC Code has already been reported for V#", "fr": ""},
			},


	"current_symptoms": {
				"missing_current_symptoms": {"en": "Current Symptoms are missing", "rw": "Ntiwagaragaje ikimenyetso cy'ibibazo umwana afite", "fr": ""},
				"invalid_current_symptom": {"en": "Please check that you have the correct type of current symptom or symptoms in the appropriate place in your CHI Report. These can be NP, IB and DB. If you have more than 1 they must be separated by a space.", 
							"rw": "Reba ko wakoresheje ikimenyetso gikwiye ku bibazo umwana afite :NP, IB cyangwa DB. Iyo birenze kimwe siga akanya hagati", "fr": ""},
				"incoherent_jam_np_symptom": {"en":"If NP is reported then other codes can't be reported as Current Symptoms", 
							"rw": "Iyo ukoresheje ikimenyetso NP, ntakindi kimenyetso gikoreshwa", "fr": ""},
                "duplicate_symptom": { "en": "These codes: %(codes)s are duplicated and shall be reported only once",
						"rw": "Nta kimenyetso kigomba kwandikwa 2 mu butumwa bumwe: %(codes)s", "fr": ""},
		},

	"location": {
			"missing_location": {"en": "Location Is missing", "rw": "Harabura aho umwana aherereye", "fr": ""},
			"invalid_location": {"en": "Please be sure that you have entered the appropriate Child Health Report location. It should be HO, HP,HC or CL.",
						"rw": "Reba ko wakoresheje ikimenyetso gikwiye (HO, HP cyangwa HC )", "fr": ""}
			},

    "child_weight": {
				"missing_child_weight": {"en": "Child weight Is missing", "rw": "Harabura ibiro by'umwana" , "fr": ""},
				"invalid_child_weight": {
		"en": "Please be sure you have entered the child weight without units of KG. It should include be in the format of WT#.# or WT#.# and between 1 & 25 with having no comma.",
				      "rw": "Ibiro by'umwana bigomba kwandikwa muri ubu buryo (WT# cyangwa WT#.#) kandi ibiro bigomba kuba hagati ya 1 na 25", "fr": ""}
				},

    "muac": {
			"missing_muac": {"en": "MUAC Is missing", "rw": "Harabura ikimenyetso cya MUAC" , "fr": ""},
			"invalid_muac": {
	"en": "Please be sure you have entered the MUAC without units of Cm. It should include be in the format of MUAC## or MUAC##.# and between 06&26 with having no comma.",
			      "rw": "Reba ko wakoresheje ikimenyetso gikwiye cya MUAC. Ibipimo bigomba kuba hagati ya 06-26", "fr": ""}
			}
	}	



