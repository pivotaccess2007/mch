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

    
	"location": {
			"missing_location": {"en": "Location Is missing", "rw": "Harabura aho yapfiriye", "fr": ""},
			"invalid_location": {"en": "Please be sure that you have entered the appropriate Birth location. It should be HO, HP, OR, HC or CL.",
						"rw": "Reba ko wakoresheje ikimenyetso gikwiye (HO,HP,OR cyangwa HC)", "fr": ""}
			},

	"death": {
			"missing_death": {"en": "Death code Is missing", "rw": "Harabura ikimenyetso cy'uwapfuye", "fr": ""},
			"invalid_death": {"en": "Please be sure that you have entered the appropriate Death Code. It should be MD, SBD,CD, or ND",
						"rw": "Reba ko wakoresheje ikimenyetso gikwiye (MD, CD, SBD cyangwa ND)", "fr": ""},
            "outrange_nd_death":  {    "en": "ND code can only be reported if Death Date-Dob is less than or equal to 28 days",
                                        "rw": "Ikimenyetso ND gitangwa gusa iyo umwana apfuye atarengeje iminsi 28", "fr": ""
                                        },
            "outrange_md_death":  {    "en": "MD code can only be reported if death occurs from the time of conception up to 42 days after birth",
                                        "rw": "Ikimenyetso MD gitangwa gusa iyo umubyeyi apfuye atwite kugeza ku minsi 42 abyaye", "fr": ""
                                        },
            "outrange_cd_death":  {    "en": "CD code can only be reported if Death Date-DoB is greater than 28 days and less than 5 years",
                                        "rw": "Ikimenyetso CD gitangwa gusa iyo umwana apfuye afite hagati y'ukwezi n'imyaka 5", "fr": ""
                                        },
            
			}
	}	



