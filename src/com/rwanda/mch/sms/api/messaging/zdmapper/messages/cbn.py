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
            "duplicate_cbn": { "en": "Child Number %(chino)s, born on %(dob)s has already been report as CBN %(nid)s",
						"rw": "Nimero %(chino)s y'uyu mwana, wavutse kuri %(dob)s, na %(nid)s yaratanzwe ku mirire n'imikurire ye muri uku kwezi", "fr": ""},
            "birth_date_mismatch": {"en": "The date of birth (date)of this child is not matching the date of delivery (date) in BIR report",
				"rw": "Itariki y'amavuko itandukanye n'iyo watanze muri raporo yo kuvuka", "fr": ""}
            
			},

    "breastfeeding": {
			"missing_breastfeeding": {"en": "Breastfeeding Is missing", "rw": "Harabura ikimenyetso cyo konsa", "fr": ""},
			"invalid_breastfeeding": {"en": "Please be sure that you have entered the appropriate Breastfeeding Code. It should be EBF, NB or CF",
						"rw": "Reba ko wakoresheje ikimenyetso cyo konsa gikwiye (EBF,NB cyangwa CF)", "fr": ""}
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



