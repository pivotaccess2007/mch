#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"


KEYS = {

        "WUM": { "en": "Coma", "rw" : "Guhwera/ guta ubwenge bikabije( utabasha kwinyeganyeza)", "fr": ""},
        "NFM": { "en": "Inability to drink or suckle", "rw": "Ntashobora kunywa cyangwa konka no kurya", "fr": ""},
        "RVM": { "en": "Vomiting" , "rw": "Kuruka", "fr": "" },
        "COM": { "en": "Convulsions ( >= 2 convulsions in 24 hours)", "rw" : "Kugagara", "fr": ""},
        "UNM": { "en": "Lethargy and unconsciousness", "rw": "Gutubwenge", "fr": ""},
        "PRM": { "en": "Prostration (extreme weakness, failure to be upright or walk)",
                 "rw": "Gucika intege cyane,  kutabasha guhagarara cg kugenda", "fr": ""},
        "SCM": { "en": "Altered level of consciousness (somnolence, unconsciousness or deep coma)", "rw": "Guhondobera", "fr": ""},
        "RDM": { "en": "Respiratory distress (respiratory acidosis) Acute pulmonary edema (radiological)",
                 "rw": "Ahumeka bimugoye /Aniha", "fr": ""},
        "HEM": { "en": "Spontaneous hemorrhages (or disseminated intravascular coagulation - DIVC)",
                 "rw": "Kuva amaraso mu myenge itandukanye y`umubiri (mu kanwa, mu mazuru, mu matwi,  kwihagarika amaras) ntakame.",
                 "fr": ""},  
        "JAM": { "en": "Jaundice (yellow coloration of the conjunctival membranes) Hemoglobinuria (coca cola or dark urine)",
                 "rw": "Umubiri wabaye umuhondo/kwihagarika inkari zisa na coca", "fr": ""},
        "ANM": { "en": "Anemia", "rw": "Yerurutse ibiganza", "fr": ""},
        "DHM": { "en": "Severe dehydration, cardiovascular collapse or shock",
                 "rw": "Amaso yahenengeye cg umubiri ukuruwe ntusubirayo", "fr": ""},
        
    }

DRUGS = {
            "AL1": { "en": "Art Lumefantrine 6x1" , "rw": "Art Lumefantrine 6x1", "fr": "Art Lumefantrine 6x1" },
            "AL2": { "en": "Art Lumefantrine 6x2" , "rw": "Art Lumefantrine 6x2", "fr": "Art Lumefantrine 6x2" },
            "AL3": { "en": "Art Lumefantrine 6x3" , "rw": "Art Lumefantrine 6x3", "fr": "Art Lumefantrine 6x3" },
            "AL4": { "en": "Art Lumefantrine 6x4" , "rw": "Art Lumefantrine 6x4", "fr": "Art Lumefantrine 6x4" },
            "ARS": { "en": "Artesunate Suppository" , "rw": "Artesunate Suppository", "fr": "Artesunate Suppository" },
            "TDR": { "en": "Rapid Diagnostic  Test" , "rw": "TDR", "fr": "Test de diagnostic rapide" },
            "NDM": { "en": "No malaria drug given", "rw": "Nta miti yahawe", "fr": ""},

            }

LOCATION = {
            "HO": { "en": "Home", "rw": "Murugo", "fr": ""},
            "HC": { "en": "At Health Faciliy", "rw": "Kukigonderabuzima", "fr": ""},
            "HP": { "en": "At Hospital", "rw": "Kubitaro", "fr": ""},
            }

INTERVENTION = {

                "PR": { "en": "Patient Directly Referred", "rw": "Yahise yoherezwa ku ivuriro ako kanya", "fr": ""},
                "CA": { "en": "CHW Advice", "rw": "Yahawe inama n'umujyanama w'ubuzima", "fr": ""},
                "AL": { "en": "Ambulance Late", "rw": "Ambulance yatinze", "fr": ""},
                "AT": { "en": "Ambulance on Time", "rw": "Ambulance yahagereye ku gihe", "fr": ""},
                "NA": { "en": "No Ambulance Response", "rw": "Ambulance ntiyaje", "fr": ""},

                }

FACILITY_RESPONSE_STATUS = {
                "NR": { "en": "No response from HC", "rw": "Ntasubiza butumwa ryavuye kukigonderabuzima", "fr": ""},
                "RR": { "en": "Response Received from HC", "rw": "Umujyanama Yakiriye isubiza rivuye kukigonderabuzima", "fr": ""},
                }

STATUS = {
            "PS": { "en": "Patient Sick", "rw": "ikimenyesto cyokurwara", "fr": ""},
            "DTH": { "en": "Death Notification", "rw": "ikimenyetso cy'urupfu", "fr": ""}            
            }


RESPONSE = {
            "invalid_code": {"en": "Invalid Code %(codes)s or sequence for severe malaria report.",
						        "rw": "Kodi %(codes)s utanze ntibaho, cyangwa byanditse nabi, kuri raporo ya malariya y'igikatu.", "fr": ""},
            "invalid_sequence": {"en": "Invalid sequence for %(codes)s in malaria report.",
						        "rw": "Kodi %(codes)s yanditse mu mwanya utari uwayo  muri raporo ya malariya y'igikatu.", "fr": ""},
            "unknown_error": {"en": "Unknown Error",
						        "rw": "Ubutumwa ntibusobanutse", "fr": ""},
            "SMR": {"en": "Thank you! Severe malaria result report for patient(%(nid)s) submitted successfully.",
                        "rw": "Murakoze ubutumwa ku gisubizo cya malariya y'igikatu bw'uwo murwayi(%(nid)s) turabubonye.", "fr": ""}, 
		    "SMN": {"en": "Thank you! Severe malaria report for patient(%(nid)s) submitted successfully.",
                    "rw": "MURAKOZE, ubutumwa ku kibazo cya malariya y'igikatu bw'uwo murwayi(%(nid)s) turabubonye.", "fr": ""},

            "unresponded_report": {"en": "You have another non-responded severe malaria report for this patient %(nid)s",
						"rw": "Hari indi raporo ya malaria utatubwiye uko byagenze kuri uyu mubyeyi %(nid)s", "fr": ""},

            "report_to_respond" : {"en": "This patient %(nid)s does not have any severe malaria report to respond to."
						, "rw": "Raporo ku gisubizo cya malaria ntiyatangwa nta raporo ya malaria y'igikatu yatanzwe kuri uyu murwayi %(nid)s" ,
                         "fr": ""},
            "invalid_report": {"en": "Invalid severe malaria report.",
						        "rw": "Raporo ya malariya y'igikatu yanditse nabi.", "fr": ""},
            "missing_drugs": {"en": "Drugs are missing", "rw": "Ntutubwiye niba wamuhaye imiti", "fr": ""},
            "missing_symptoms": {"en": "Symptoms are missing", "rw": "Ntutubwiye ibimenyetso afite", "fr": ""},
            "missing_location": {"en": "Location Is missing", "rw": "Harabura aho umurwayi aherereye", "fr": ""},
            "missing_intervention": {"en": "Intervention Code Is missing", "rw": "Harabura ikimenyetso cy'ubutabazi yahawe", "fr": ""},
            "missing_status": {"en": "Patient Status Is missing", "rw": "Harabura ikimenyetso cy'uko umurwayi amerewe", "fr": ""},
            "missing_response": {"en": "HC response is missing", "rw": "Harabura kumenya niba ikigo nderabuzima baguhamagaye.", "fr": ""},
            "invalid_nid": {"en": "Patient ID must be 16 digits of national ID Or (10 digits of CHW Phone Number + 6 digits of ddmmyy",
				            "rw": "Inomero y'Indangamuntu igomba kuba igizwe n'imibare 16 gusa udasize akanya, yikore ubanza telefoni, itariki, ukwezi n'umwaka", 
                            "fr": ""},
            "nid_missing": {"en": "Patient ID Is missing", "rw": "Harabura nimero y'indangamuntu", "fr": ""},

            }


HELP  =  { "SMN" : {"en" : "The correct format message is: SMN NID MALARIYA_SYMPTOMS('DHM', 'NFM', 'JAM', 'RDM', 'HEM', 'COM', 'UNM', 'SCM', 'PRM', 'ANM', 'RVM', 'WUM') DRUGS_CODE('TDR', 'ARS', 'AL4', 'AL2', 'AL3', 'AL1')", 
	                      "rw": "Andika: SMN INDANGAMUNTU IBIMENYETSO_BY_IBIBAZO('DHM', 'NFM', 'JAM', 'RDM', 'HEM', 'COM', 'UNM', 'SCM', 'PRM', 'ANM', 'RVM', 'WUM') KODI_Y_IMITI('TDR', 'ARS', 'AL4', 'AL2', 'AL3', 'AL1')"
		                },

            "SMR" : {"en" : "The correct format message is: SMR NID MALARIYA_SYMPTOMS('DHM', 'NFM', 'JAM', 'RDM', 'HEM', 'COM', 'UNM', 'SCM', 'PRM', 'ANM', 'RVM', 'WUM') INTERVENTION_CODE('PR', 'NA', 'CA', 'AL', 'AT') LOCATION_CODE('HC', 'HP', 'HO') PATIENT_STATUS('PS', 'DTH') FACILITY_RESPONSE_STATUS('NR', 'RR')", 
	                      "rw": "Andika: SMR INDANGAMUNTU IBIMENYETSO_BY_IBIBAZO('DHM', 'NFM', 'JAM', 'RDM', 'HEM', 'COM', 'UNM', 'SCM', 'PRM', 'ANM', 'RVM', 'WUM') UBUTABAZI_BWAKOZWE('PR', 'NA', 'CA', 'AL', 'AT') AHO_AHEREREYE('HC', 'HP', 'HO') UKO_AMEZE('PS', 'DTH') UBUFASHA_BWA_MUGANGA('NR', 'RR')"
		                },

        }

