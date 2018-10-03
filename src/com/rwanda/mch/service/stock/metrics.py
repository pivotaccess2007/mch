#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"



DRUGS = {
             "AL1": { "en": "Art Lumefantrine 6x1" , "rw": "Art Lumefantrine 6x1", "fr": "Art Lumefantrine 6x1" },
            "AL2": { "en": "Art Lumefantrine 6x2" , "rw": "Art Lumefantrine 6x2", "fr": "Art Lumefantrine 6x2" },
            "AL3": { "en": "Art Lumefantrine 6x3" , "rw": "Art Lumefantrine 6x3", "fr": "Art Lumefantrine 6x3" },
            "AL4": { "en": "Art Lumefantrine 6x4" , "rw": "Art Lumefantrine 6x4", "fr": "Art Lumefantrine 6x4" },
            "ARS": { "en": "Artesunate Suppository" , "rw": "Artesunate Suppository", "fr": "Artesunate Suppository" },
            "TDR": { "en": "Rapid Diagnostic  Test" , "rw": "TDR", "fr": "Test de diagnostic rapide" }

            }


RESPONSE = {
            "invalid_code": {"en": "Invalid Code %(codes)s or sequence for malaria drug stock out report.",
						    "rw": "Kodi %(codes)s utanze ntibaho, cyangwa byanditse nabi, kuri raporo y'imiti ya malariya yashize.", "fr": ""},
            "unknown_error": {"en": "Unknown Error",
						        "rw": "Ubutumwa ntibusobanutse", "fr": ""},
            "SO": {"en": "Thank you! Malaria drugs/TDR stock out report submitted successfully.",
                    "rw": "MURAKOZE, ubutumwa ku kibazo cy'imiti cyangwa TDR ya malariya yashize turabubonye.", "fr": ""},
		    "SS": {"en": "Thank you! Malaria drugs/TDR stock out result report submitted successfully.",
                        "rw": "Murakoze ubutumwa ku gisubizo cy'imiti cyangwa TDR, ya malariya, mwakiriye turabubonye.", "fr": ""},
		    "RSO": {"en": "Thank you! Malaria drugs/TDR stock out risk report submitted successfully.",
                    "rw": "MURAKOZE, ubutumwa ku kibazo cy'imiti cyangwa TDR ya malariya yenda gushira turabubonye.", "fr": ""},
            "invalid_report": {"en": "Invalid severe malaria report.",
						        "rw": "Raporo ya malariya y'igikatu yanditse nabi.", "fr": ""},
            "missing_drugs": {"en": "Drugs are missing", "rw": "Ntutubwiye imiti", "fr": ""},
            }


HELP  =  { "SO" : {"en" : "The correct format message is: SO DRUG_CODES('TDR', 'ARS', 'AL4', 'AL2', 'AL3', 'AL1')", 
	                      "rw": "Andika: SO IBIMENYETSO_BY_IMITI('TDR', 'ARS', 'AL4', 'AL2', 'AL3', 'AL1')"
		                },

            "SS" : {"en" : "The correct format message is: SS DRUG_CODES('TDR', 'ARS', 'AL4', 'AL2', 'AL3', 'AL1')", 
	                      "rw": "Andika: SS IBIMENYETSO_BY_IMITI('TDR', 'ARS', 'AL4', 'AL2', 'AL3', 'AL1')"
		                },

            "RSO" : {"en" : "The correct format message is: RSO DRUG_CODES('TDR', 'ARS', 'AL4', 'AL2', 'AL3', 'AL1')", 
	                      "rw": "Andika: RSO IBIMENYETSO_BY_IMITI('TDR', 'ARS', 'AL4', 'AL2', 'AL3', 'AL1')"
		                },

        }
