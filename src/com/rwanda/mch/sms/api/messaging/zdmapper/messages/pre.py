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
		"preg_duplicated_nid": {"en": 
					"This Patient ID has already been used for registration of pregnancy, Please report if something happened to this pregnancy",
					"rw": "Iyo ndangamuntu yakoreshejwe kuwundi mubyeyi", "fr": ""},
		"invalid_nid": {"en": "Patient ID must be 16 digits of national ID Or (10 digits of CHW Phone Number + 6 digits of ddmmyy",
				"rw": "Inomero y'Indangamuntu igomba kuba igizwe n'imibare gusa udasize akanya", "fr": ""}
		},

	"lmp" : { "lmp_missing": { "en": "Last menstrual period Is missing", "rw": "Harabura itariki ya nyuma y'imihango", "fr": ""},
		  "misformat_lmp": {"en": "Last menstrual period should be in this format dd.mm.yyyy",
				    "rw": "Itariki ya nyuma y'imihango yandikwa muri ubu buryo(Itariki.Ukwezi.Umwaka)", "fr": ""},
		  "lmp_greater_currentdate": {"en": "Last menstrual period date should be less than current date",
			"rw": "Itariki yanyuma y'imihango igomba kuba mbere y'itariki y'uyu munsi", "fr": ""},
		 "lmp_earlier_9months": {"en":"The last menstrual period can't be earlier than Current date-9 months (Date), Kindly check the date again and resubmit it",
					  "rw": "Itariki yanyuma y'imihango ntigomba kuba mbere y'amezi 9 ashize. Kosora wongere wohereze", "fr":""}
		},
	"anc2_date": {
			"anc2_date_missing": {"en": "Second ANC Is missing", "rw":"Harabura itariki yo gusubira kwisuzumisha","fr": ""},
			"misformat_anc2_date" : {"en": "Please provide Second ANC Appointment Date in this format dd.mm.yyyy",
				"rw": "Itariki yo gusubira kwisuzumisha yandikwa muri ubu buryo(Itariki.Ukwezi.Umwaka)", "fr": ""},
			"anc2_lesser_currentdate": {"en": "Second ANC Date should be greater than current date", 
				"rw": "Andika neza, itariki yo gusubira kwisuzumisha yararenze", "fr": ""},
			"anc2_date_later_edd": {"en": "Second ANC Date should not be later than Expected Delivery Date(Date)",
				"rw": "Itariki yo gusubira kwisuzumisha ntigomba kurenga itariki y'agateganyo yo kubyara)", "fr": ""}			
			},
	"gravidity": {
			"gravidity_missing" : { "en": "Gravidity/or Parity Is missing", "rw": "Haraburamo umubare w'inshuro yasamye cyangwa imbyaro","fr": ""},
			"gravidity_not_between_1_30" : {"en":"Gravidity and Parity should be between 1 and 30", 
							"rw": "Umubare w'inshuro yasamye cyangwa imbyaro bigomba kuba hagati ya 1 na 30" ,"fr": ""},
			"misformat_gravidity" : {"en": "Only numbers are allowed to be provided in Gravidity and Parity",
						  "rw": "Koresha imibare gusa ku umubare w'inshuro yasamye cyangwa imbyaro","fr": ""},
		"mismatch_gravidity_record" : { "en": "The system already has registered %(pregs)d of pregnancies for %(nid)s, Gravidity should be more than %(pregs)d",
						"rw": "Umubyeyi ufite iyi ndangamuntu: %(nid)s inshuro yasamye zigomba kuba hejuru ya: %(pregs)d","fr": ""}
			},

	"parity": {
			"missing_parity": {"en": "Parity/or Gravidity Is missing", "rw": "Haraburamo umubare w'inshuro yasamye cyangwa imbyaro" , "fr": ""},
			"misformat_parity": {"en": "Only numbers are allowed to be provided in Parity and Gravidity",
						"rw": "Koresha imibare gusa ku umubare w'inshuro yasamye cyangwa imbyaro" , "fr": ""},
			"outrange_parity": {"en": "Parity should be less than gravidity number", "rw": "Umubare w'imbyaro ugomba kuba munsi y'inshuro yasamye" , "fr": ""}

			},

	"previous_symptoms": {
			"missing_previous_symptoms": { "en": "Previous pregnancy symptom Is missing", "rw": "Harabura ibimenyetso ku inda zayibanjirije", "fr": ""},
			"gravidity_mismatch_symptoms": { "en": "NR should be reported as Previous Symptom if Gravidity is 1",
				 "rw": "Umubyeyi usamye bwa 1, ibimenyetso kunda zayibanjirije ni NR", "fr": ""},
			"invalid_previous_symptom": {  "en": "One or more previous pregnancy symptoms do not match. These can be GS, MU, HD, RM, OL, YG, NR, KX, YJ, LZ and if you have more than 1 symptoms, they must be separated by a space.", 
						"rw": "Ku bimenyetso by'ibibazo yagize ku nda zayibanjirije, hitamo muri ibi: GS, MU, HD, RM, OL, YG, KX, NR, YJ, LZ, iyo birenze kimwe siga akanya hagati", "fr": ""},
			"miscarriage_mismatch": { "en": "RM can only be reported for women with at least 3 miscarriages",
						"rw": "Ikimenyetso RM gikoreshwa gusa ku mubyeyi  wakuyemo inda nibura inshuro 3. Hindura ikimenyetso cyangwa urebe niba utibeshye ku nshuro yasamye cyangwa imbyaro"
, "fr": ""},
			"duplicate_symptom": { "en": "These codes: %(codes)s are duplicated and shall be reported only once",
						"rw": "Nta kimenyetso kigomba kwandikwa 2 mu butumwa bumwe: %(codes)s", "fr": ""},
			"incoherent_jam_nr_symptom": { "en": "If NR is reported then other codes can't be reported as Previous Symptoms",
						    "rw": "Iyo ukoresheje ikimenyetso NR, ntakindi kimenyetso gikoreshwa ku bibazo ku nda zayibanjirije", "fr": ""}
	
		},

	"current_symptoms": {
				"missing_current_symptoms": {"en": "Current pregnancy symptom Is missing", "rw": "Harabura ibimenyetso kuri iyi nda", "fr": ""},
				"invalid_current_symptom": {"en": "One or more reported symptoms in Current pregnancy symptoms do not match.  These can be VO, PC, OE, NS, MA, JA, FP, FE, DS, DI, SA, RB, NP, HY, CH, AF and if you have more than 1 symptoms, they must be separated by a space.", 
							"rw": "Ku bimenyetso by'ibibazo kuri iyi nda, hitamo muri ibi: VO, PC, OE, NS, MA, JA, FP, FE, DS, DI, SA, RB, NP, HY, CH, AF, iyo birenze kimwe siga akanya hagati", "fr": ""},
                "duplicate_symptom": { "en": "These codes: %(codes)s are duplicated and shall be reported only once",
						"rw": "Nta kimenyetso kigomba kwandikwa 2 mu butumwa bumwe: %(codes)s", "fr": ""},
				"incoherent_jam_np_symptom": {"en":"if NP is reported then other codes can't be reported as Current Symptoms", 
							"rw": "Iyo ukoresheje ikimenyetso NP, ntakindi kimenyetso gikoreshwa ku bibazo kuri iyi nda", "fr": ""}
		},

	"location": {
			"missing_location": {"en": "Location Is missing", "rw": "Harabura aho umubyeyi yipimishirije", "fr": ""},
			"invalid_location": {"en": "Please be sure that you have entered the appropriate PRE location. It should be HP or HC.",
						"rw": "Aho umubyeyi yipimishirije hagomba kuba ku bitaro cyangwa ikigonderabuzima gusa", "fr": ""}
			},
	
	"mother_weight": {
				"missing_mother_weight": {"en": "Mother weight Is missing", "rw": "Harabura ibiro by'umubyeyi" , "fr": ""},
				"invalid_mother_weight": {
		"en": "The weight of the mother should be in the format of WT##,WT##.#, WT### or WT###. #. Please double check if you have provided correct weight.",
				      "rw": "Ibiro by'umubyeyi bigomba kwandikwa kuri ubu buryo: WT##, WT##.#, WT### or WT###.#", "fr": ""}
				},
	"mother_height": {
				"missing_mother_height": {"en": "Mother height Is missing", "rw": "Harabura uburebure bw'umubyeyi" , "fr": ""},
				"invalid_mother_height": {
						"en": "The height should be in the format of HT## or HT###. Please double check if you have provided correct height.",
						"rw": "Uburebure bw'umubyeyi bigomba kwandikwa kuri ubu buryo: HT## cyangwa HT### ", "fr": ""}
				},

	"toilet": { "missing_toilet": {"en": "Toilet code Is missing", "rw": "Harabura ikimenyetso cy'ubwiherero", "fr": ""},
		    "invalid_toilet": {"en": "Please be sure that you have entered the appropriate Toilet code. It should be TO or NT.",
					"rw": "Ku bwiherero hakoreshwa kimwe muri ibi bimenyetso: TO, NT", "fr": ""}
		},
	"handwashing": { 
			"missing_handwashing": {"en": "Hand wash code Is missing", "rw": "Harabura ikimenyetso cya kandagirukarabe", "fr": ""},
			"invalid_handwashing": {"en": "Please be sure that you have entered the appropriate Hand wash code. It should be HW or NH.",
						"rw" : "Kuri kandagirukarabe hakoreshwa kimwe muri ibi bimenyetso: HW, NH", "fr": ""}
			},

    "muac": {
			"missing_muac": {"en": "MUAC Is missing", "rw": "Harabura ikimenyetso cya MUAC" , "fr": ""},
			"invalid_muac": {
	              "en": "Please be sure you have entered the MUAC without units of Cm. It should include be in the format of MUAC## or MUAC##.# and having no comma.",
			      "rw": "Reba ko wakoresheje ikimenyetso gikwiye cya MUAC.", "fr": ""}
			},
    "mother_phone": { "invalid_phone": {"en": "The provided phone number is not a valid phone number", 
				            "rw": "Nimero ya telefoni wakoresheje ntabwo yanditse neza nk numero ya telefoni.", "fr": ""}
                    }

	}	



