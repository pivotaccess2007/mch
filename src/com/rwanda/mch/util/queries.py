#!/usr/bin/env python
# encoding: utf-8
# vim: ts=2 expandtab

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

##
## The only file to use orm directly
## 




NO_RISK = {'attrs': 
			[('prev_pregnancy_gs IS NULL', 'Previous Obstetric Surgery'), 
			 ('prev_pregnancy_mu IS NULL', 'Multiples'),
			 ('prev_pregnancy_hd IS NULL', 'Previous Home Delivery'), 
			 ('prev_pregnancy_rm IS NULL', 'Repetiive Miscarriage'),
			 ('prev_pregnancy_ol IS NULL', 'Old Age (Over 35)'),
			 ('prev_pregnancy_yg IS NULL', 'Young Age (Under 18)'),
			 ('prev_pregnancy_kx IS NULL', 'Previous Convulsion'),
			 ('prev_pregnancy_yj IS NULL', 'Previous Serious Conditions'),
			 ('prev_pregnancy_lz IS NULL', 'Previous Hemorrhaging/Bleeding'),
			 ('symptom_vo IS NULL', 'Vomiting'),
			 ('symptom_pc IS NULL', 'Pneumonia'),
			 ('symptom_oe IS NULL', 'Oedema'),
			 ('symptom_ns IS NULL', 'Neck Stiffness'),
			 ('symptom_ma IS NULL', 'Malaria'),
			 ('symptom_ja IS NULL', 'Jaundice'),
			 ('symptom_fp IS NULL', 'Fraccid Paralysis'),
			 ('symptom_fe IS NULL', 'Fever'),
			 ('symptom_ds IS NULL', 'Chronic Disease'),
			 ('symptom_di IS NULL', 'Diarrhea'),
			 ('symptom_sa IS NULL', 'Severe Anemia'),
			 ('symptom_rb IS NULL', 'Rapid Breathing'),
			 ('symptom_hy IS NULL', 'Hypothermia'),
			 ('symptom_ch IS NULL', 'Coughing'),
			 ('symptom_af IS NULL', 'Abnormal Fontinel'),
			], 
	'query_str': 
		'prev_pregnancy_gs IS NULL AND prev_pregnancy_mu IS NULL AND prev_pregnancy_hd IS NULL AND prev_pregnancy_rm IS NULL AND prev_pregnancy_ol IS NULL AND prev_pregnancy_yg IS NULL AND prev_pregnancy_kx IS NULL AND prev_pregnancy_yj IS NULL AND prev_pregnancy_lz IS NULL AND symptom_vo IS NULL AND symptom_pc IS NULL AND symptom_oe IS NULL AND symptom_ns IS NULL AND symptom_ma IS NULL AND symptom_ja IS NULL AND symptom_fp IS NULL AND symptom_fe IS NULL AND symptom_ds IS NULL AND symptom_di IS NULL AND symptom_sa IS NULL AND symptom_rb IS NULL AND symptom_hy IS NULL AND symptom_ch IS NULL AND symptom_af IS NULL'
		}

RISK = { 'attrs': 
			[('symptom_vo IS NOT NULL', 'Vomiting'),
			 ('symptom_pc IS NOT NULL', 'Pneumonia'),
			 ('symptom_oe IS NOT NULL', 'Oedema'),
			 ('symptom_ns IS NOT NULL', 'Neck Stiffness'),
			 ('symptom_ma IS NOT NULL', 'Malaria'),
			 ('symptom_ja IS NOT NULL', 'Jaundice'),
			 ('symptom_fp IS NOT NULL', 'Fraccid Paralysis'),
			 ('symptom_fe IS NOT NULL', 'Fever'),
			 ('symptom_ds IS NOT NULL', 'Chronic Disease'),
			 ('symptom_di IS NOT NULL', 'Diarrhea'),
			 ('symptom_sa IS NOT NULL', 'Severe Anemia'),
			 ('symptom_rb IS NOT NULL', 'Rapid Breathing'),
			 ('symptom_hy IS NOT NULL', 'Hypothermia'),
			 ('symptom_ch IS NOT NULL', 'Coughing'),
			 ('symptom_af IS NOT NULL', 'Abnormal Fontinel'),
			], 
	'query_str': 
		'(symptom_vo IS NOT NULL OR symptom_pc IS NOT NULL OR symptom_oe IS NOT NULL OR symptom_ns IS NOT NULL OR symptom_ma IS NOT NULL OR symptom_ja IS NOT NULL OR symptom_fp IS NOT NULL OR symptom_fe IS NOT NULL OR symptom_ds IS NOT NULL OR symptom_di IS NOT NULL OR symptom_sa IS NOT NULL OR symptom_rb IS NOT NULL OR symptom_hy IS NOT NULL OR symptom_ch IS NOT NULL OR symptom_af IS NOT NULL) AND NOT (prev_pregnancy_gs IS NOT NULL OR prev_pregnancy_mu IS NOT NULL OR prev_pregnancy_hd IS NOT NULL OR prev_pregnancy_rm IS NOT NULL OR prev_pregnancy_ol IS NOT NULL OR prev_pregnancy_yg IS NOT NULL OR prev_pregnancy_kx IS NOT NULL OR prev_pregnancy_yj IS NOT NULL OR prev_pregnancy_lz IS NOT NULL)'
		}

HIGH_RISK = { 'attrs': 
			[('prev_pregnancy_gs IS NOT NULL', 'Previous Obstetric Surgery'), 
			 ('prev_pregnancy_mu IS NOT NULL', 'Multiples'),
			 ('prev_pregnancy_hd IS NOT NULL', 'Previous Home Delivery'), 
			 ('prev_pregnancy_rm IS NOT NULL', 'Repetitive Miscarriage'),
			 ('prev_pregnancy_ol IS NOT NULL', 'Old Age (Over 35)'),
			 ('prev_pregnancy_yg IS NOT NULL', 'Young Age (Under 18)'),
			 ('prev_pregnancy_kx IS NOT NULL', 'Previous Convulsion'),
			 ('prev_pregnancy_yj IS NOT NULL', 'Previous Serious Conditions'),
			 ('prev_pregnancy_lz IS NOT NULL', 'Previous Hemorrhaging/Bleeding'),
			], 
		'query_str': 
		'prev_pregnancy_gs IS NOT NULL OR prev_pregnancy_mu IS NOT NULL OR prev_pregnancy_hd IS NOT NULL OR prev_pregnancy_rm IS NOT NULL OR prev_pregnancy_ol IS NOT NULL OR prev_pregnancy_yg IS NOT NULL OR prev_pregnancy_kx IS NOT NULL OR prev_pregnancy_yj IS NOT NULL OR prev_pregnancy_lz IS NOT NULL'

	}

TOILET={"attrs": [
                  (u"lower(toilet) = 'to'", u'With toilet'),
				          (u"lower(toilet) = 'nt'", u'Without toilet')
                  ],
        'query_str':"((lower(toilet) = 'nt') OR (lower(toilet) = 'to'))"
        }

HANDWASH={"attrs": [
                  (u"lower(handwash) = 'to'", u'With handwashing'),
				          (u"lower(handwash) = 'nt'", u'Without handwashing')
                  ],
        'query_str':"((lower(handwash) = 'hw') OR (lower(handwash) = 'nh'))"
        }



DELIVERY_DATA = {
		'attrs': [
				(u"lower(location) = 'hp'", u'At Hospital'),
				(u"lower(location) = 'hc'", u'At Health Centre'),
				(u"lower(location) = 'or'", u'En Route'),
				(u"lower(location) = 'ho'", u'At home'),
									
			],

		'query_str':"((lower(location) = 'hp') OR (lower(location) = 'hc') OR (lower(location) = 'or') OR (lower(location) = 'ho'))",
		
		}


ANC_DATA = { 
	'attrs': [
			("lower(anc_visit) = 'anc2'", 'ANC2'),
			("lower(anc_visit) = 'anc3'", 'ANC3'),
			("lower(anc_visit) = 'anc4'", 'ANC4'),
			("lower(anc_visit) = 'anc2' AND (lmp + INTERVAL '150 days') <= anc_date", 'Standard ANC2'),
			("lower(anc_visit) = 'anc3' AND (lmp + INTERVAL '180 days') <= anc_date", 'Standard ANC3'),
			("lower(anc_visit) = 'anc4' AND (lmp + INTERVAL '270 days') <= anc_date", 'Standard ANC4')
		],

	'query_str': "( (lower(anc_visit) = 'anc2') OR (lower(anc_visit) = 'anc3') OR (lower(anc_visit) = 'anc4') )"

	}


MALARIA_DATA = { 
	'attrs': [
			("has_gone_hc", 'Received at HC'),
			("has_gone_hd", 'Received at DH'),
			("is_alive", 'Is Alive'),
			("lower(hd_patient_status) = 'cured'", 'Cured'),
			("lower(hd_patient_status) = 'referred'", "Referred"),
      ("is_dead", 'Is Dead'),
      ("age < 6", 'Under 5 years old'),
      ("age > 5", 'Above 5 years old'),
      ("is_pregnant", 'Pregnant Women'),
      ("sex_pk=2", 'Female'),
      ("sex_pk=1", 'Male'),
      ("hc_pretransfer_treatment IS NOT NULL", "Pre-transfer treated"),
      ("lower(hc_tdr_result) = 'positive' ", 'RDT Positive(TDR +)'),
      ("lower(hc_bs_result) = 'positive' ", 'BS Positive(GE +)'),
      ("symptom_anm IS NOT NULL", 'Anemia'),
      ("lower(hd_final_diagnostics) LIKE '%%malaria cerebral%%'", 'Severe malaria cerebral form'),
      ("lower(hd_final_diagnostics) LIKE '%%malaria anemic%%'", 'Severe malaria anemic form'),
      ("lower(hd_final_diagnostics) LIKE '%%malaria with other complication%%'", 'Severe malaria with other complication'),
      ("lower(hd_final_diagnostics) LIKE '%%malaria with other comorbidities%%'", 'Simple malaria with other comorbidities'),
      ("lower(hd_final_diagnostics) LIKE '%%malaria not confirmed%%'", 'Malaria not confirmed'),      
      
		],

   'query_str': ""

	}

STOCK_DATA = { 
	'attrs': [
			("lower(keyword) = 'rso'", 'Risk of stock out'),
      ("lower(keyword) = 'so'", 'Stock out'),
			("lower(keyword) = 'ss'", 'Stock supplied'),
		],

   'query_str': "( (lower(keyword) = 'rso') OR (lower(keyword) = 'so') OR (lower(keyword) = 'ss') )"

	}


NBC_DATA = {
		
		'NBC': {
			'attrs':[
					("lower(nbc_visit) = 'nbc1'", 'NBC1'),
					("lower(nbc_visit) = 'nbc2'", 'NBC2'),
					("lower(nbc_visit) = 'nbc3'", 'NBC3'),
					("lower(nbc_visit) = 'nbc4'", 'NBC4'),
					("lower(nbc_visit) = 'nbc5'", 'NBC5')
					]
			},

		'NO_RISK': { 	'attrs': [
						('symptom_af IS NULL', 'Abnormal Fontinel'),
						('symptom_ci IS NULL', 'Cord Infection'),
						('symptom_cm IS NULL', 'Congenital Malformation'),
						("lower(breastfeeding) != 'nb' ", 'Not Breastfeeding'),
						('symptom_rb IS NULL', 'Rapid Breathing'),
						('symptom_pm IS NULL', 'Premature'),
					],
				'query_str': "((symptom_af IS NULL) AND (symptom_ci IS NULL) AND (symptom_cm IS NULL) AND (lower(breastfeeding) != 'nb') AND  (symptom_rb IS NULL) AND (symptom_pm IS NULL) )"
				},

		'RISK':	{
					'attrs': [
							('symptom_af IS NOT NULL', 'Abnormal Fontinel'),
							('symptom_ci IS NOT NULL', 'Cord Infection'),
							('symptom_cm IS NOT NULL', 'Congenital Malformation'),
							("lower(breastfeeding) = 'nb' ", 'Not Breastfeeding')
							],
					'query_str': "((symptom_af IS NOT NULL) OR (symptom_ci IS NOT NULL) OR (symptom_cm IS NOT NULL) OR (lower(breastfeeding) = 'nb')) AND NOT ((symptom_rb IS NOT NULL) OR (symptom_pm IS NOT NULL))"
	
				},
		'HIGH_RISK':	{
					'attrs': [ 
							('symptom_rb IS NOT NULL', 'Rapid Breathing'),
							('symptom_pm IS NOT NULL', 'Premature'),							

							],
					'query_str': '((symptom_rb IS NOT NULL) OR (symptom_pm IS NOT NULL))'
				}
		
		}



PNC_DATA = {

		'PNC': {

			'attrs': [("lower(pnc_visit) = 'pnc1'", 'PNC1'),
			          ("lower(pnc_visit) = 'pnc2'", 'PNC2'),
			          ("lower(pnc_visit) = 'pnc3'", 'PNC3'),
			          ("lower(pnc_visit) = 'pnc4'", 'PNC4'),
			          ("lower(pnc_visit) = 'pnc5'", 'PNC5')
              ]
			},
	
		'NO_RISK': {
			   'attrs':	[
						(u'symptom_ch IS NULL', u'Coughing'), 
						(u'symptom_di IS NULL', u'Diarhea'),
						(u'symptom_ds IS NULL', u'Chronic Disease'),
						(u'symptom_fe IS NULL', u'Fever'), 
						(u'symptom_fp IS NULL', u'Fraccid Paralysis'),
						(u'symptom_hy IS NULL', u'Hypothermia'), 
						(u'symptom_ja IS NULL', u'Jaundice'),
						(u'symptom_ma IS NULL', u'Malaria'),
            (u'symptom_ns IS NULL', u'Neck Stiffness'),
						(u'symptom_oe IS NULL', u'Edema'),
						(u'symptom_pc IS NULL', u'Pneumonia'),
						(u'symptom_sa IS NULL', u'Severe Anemia'),
						(u'symptom_rb IS NULL', u'Rapid Breathing'), 
						(u'symptom_vo IS NULL', u'Vomiting'),
						],

			   'query_str': '((symptom_ch IS NULL) AND (symptom_hy IS NULL) AND (symptom_rb IS NULL) AND (symptom_sa IS NULL) AND (symptom_ds IS NULL) AND (symptom_fe IS NULL) AND (symptom_fp IS NULL) AND (symptom_ja IS NULL) AND (symptom_ns IS NULL) AND (symptom_oe IS NULL) AND (symptom_pc IS NULL) AND (symptom_vo IS NULL) AND (symptom_di IS NULL) AND (symptom_ma IS NULL))'
			},

		'RISK': {
			   'attrs':	[
						(u'symptom_ch IS NOT NULL', u'Coughing'), 
						(u'symptom_hy IS NOT NULL', u'Hypothermia'), 
						(u'symptom_rb IS NOT NULL', u'Rapid Breathing'), 
						(u'symptom_sa IS NOT NULL', u'Severe Anemia'),
						(u'symptom_ds IS NOT NULL', u'Chronic Disease'),
						(u'symptom_fe IS NOT NULL', u'Fever'), 
						(u'symptom_fp IS NOT NULL', u'Fraccid Paralysis'),
						(u'symptom_ja IS NOT NULL', u'Jaundice'),
						(u'symptom_ns IS NOT NULL', u'Neck Stiffness'),
						(u'symptom_oe IS NOT NULL', u'Edema'),
						(u'symptom_pc IS NOT NULL', u'Pneumonia'),
						(u'symptom_vo IS NOT NULL', u'Vomiting'),
						(u'symptom_di IS NOT NULL', u'Diarhea'),
						(u'symptom_ma IS NOT NULL', u'Malaria'),
					],

			   'query_str': '( (symptom_ch IS NOT NULL) OR (symptom_hy IS NOT NULL) OR (symptom_rb IS NOT NULL) OR (symptom_sa IS NOT NULL) OR (symptom_ds IS NOT NULL) OR (symptom_fe IS NOT NULL) OR (symptom_fp IS NOT NULL) OR (symptom_ja IS NOT NULL) OR (symptom_ns IS NOT NULL) OR (symptom_oe IS NOT NULL) OR (symptom_pc IS NOT NULL) OR (symptom_vo IS NOT NULL) OR (symptom_di IS NOT NULL) OR (symptom_ma IS NOT NULL) )'

		}
	}

CCM_DATA = {
		'attrs': [
            (u'symptom_di IS NOT NULL', u'Diarrhea'),
						(u'symptom_ma IS NOT NULL', u'Malaria'),
            (u'symptom_oi IS NOT NULL', u'Other Illness'),
            (u'symptom_pc IS NOT NULL', u'Pneumonia'),
            (u'symptom_nv IS NOT NULL', u'Unimmunized Child')											
					],

		'query_str': '((symptom_oi IS NOT NULL) OR (symptom_di IS NOT NULL) OR (symptom_ma IS NOT NULL) OR (symptom_pc IS NOT NULL) OR (symptom_nv IS NOT NULL))'
		
		}

CMR_DATA = {
		'attrs': [
						(u"lower(intervention) = 'pt' ", u'Patient Treated'),
						(u"lower(intervention) = 'pr' ", u'Patient Directly Referred'),
						(u"lower(intervention) = 'tr' ", u'Patient Referred After Treatment'),
						(u"lower(intervention) = 'aa' ", u'Binome/ASM Advice'),
											
					],

		'query_str': " ((symptom_oi IS NOT NULL) OR (symptom_di IS NOT NULL) OR (symptom_ma IS NOT NULL) OR (symptom_pc IS NOT NULL) OR (symptom_nv IS NOT NULL)) AND ((lower(intervention) = 'pt') OR (lower(intervention) = 'pr') OR (lower(intervention) = 'tr') OR (lower(intervention) = 'aa'))"
		
		}



VAC_DATA = {
		'VAC_SERIES': {

				'attrs': [
						(u"lower(vaccine) = 'v1'", u'BCG, PO'),
						(u"lower(vaccine) = 'v2'", u'P1, Penta1, PCV1, Rota1'),
						(u"lower(vaccine) = 'v3'", u'P2, Penta2, PCV2, Rota2'),
						(u"lower(vaccine) = 'v4'", u'P3, Penta3, PCV3, Rota3'),
						(u"lower(vaccine) = 'v5'", u'Measles1, Rubella'),
						(u"lower(vaccine) = 'v6'", u'Measles2'),					
					],
		
				'query_str': "((lower(vaccine) = 'v1') OR (lower(vaccine) = 'v2') OR (lower(vaccine) = 'v3') OR (lower(vaccine) = 'v4') OR (lower(vaccine) = 'v5') OR (lower(vaccine) = 'v6'))"
			},

		'VAC_COMPLETION': {

					'attrs': [
							(u"lower(vaccine_status) = 'vc'", u'Vaccine Complete'),
							(u"lower(vaccine_status) = 'vi'", u'Vaccine Incomplete'),
							(u"lower(vaccine_status) = 'nv'", u'Unimmunized Child'),				
						],
			
					'query_str': "((lower(vaccine_status) = 'vc') OR (lower(vaccine_status) = 'vi') OR (lower(vaccine_status) = 'nv'))"
			},



		}

CHILD_NUTR = {		
		'nb': ("lower(breastfeeding) = 'nb' OR lower(recent_breastfeeding) = 'nb'", u'Not Breastfeeding'),
		'ebf': ("lower(recent_breastfeeding) = 'ebf'", u'Exclusive Breastfeeding'),
		'cf': ("lower(recent_breastfeeding) = 'cf'", u'Complementary Feeding'),
		'bf1':    ("lower(breastfeeding) = 'bf1'", u'Breastfeeding Within 1 hour'),
		'stunting': (u'height_for_age < -2', u'Stunting'),
		'underweight': (u'weight_for_age < -2', u'Underweight'),
		'wasting':     (u'weight_for_height < -2', u'Wasting'),
		'lostweight':('previous_child_weight > recent_child_weight', 'Lost Weight'),
		'falteringweight':('previous_child_weight = recent_child_weight', 'Faltering Weight'),
		'gainedweight':('previous_child_weight < recent_child_weight', 'Gained Weight'),
		'muacred': ('recent_muac < 11.5 AND recent_muac != 0.0', 'MUAC < 11.5 cm'),
		'muacyellow': ('(recent_muac >= 11.5 AND recent_muac < 12.5)  AND recent_muac != 0.0', 'MUAC 11.5 - 12.5 cm'),
		'muacgreen': ('recent_muac > 12.5  AND recent_muac != 0.0', 'MUAC > 12.5 cm'),

		}

MOTHER_NUTR = {		
		'mother_height_less_145': ("recent_mother_height < 145", u'Proportion of pregnant women with height <150cm at 1st ANC'),
		'mother_weight_less_50': ("recent_mother_weight < 50", u'Proportion of pregnant women with weight < 50kg'),
		'bmi_less_18_dot_5': (" recent_bmi < 18.5", u'Proportion of pregnant women with BMI <18.5 at 1st ANC'),
		'lostweight':('previous_mother_weight > recent_mother_weight', 'Lost Weight'),
		'falteringweight':('previous_mother_weight = recent_mother_weight', 'Faltering Weight'),
		'gainedweight':('previous_mother_weight < recent_mother_weight', 'Gained Weight'),
		'mmuacred': ('recent_muac < 18.5 AND recent_muac != 0.0', 'MUAC < 18.5 cm'),
		'mmuacyellow': ('(recent_muac >= 18.5 AND recent_muac < 21.0)  AND recent_muac != 0.0', 'MUAC 18.5 - 21.0 cm'),
		'mmuacgreen': ('recent_muac > 21.0  AND recent_muac != 0.0', 'MUAC > 21.0 cm'),

		}


DEATH_DATA = {
		          'attrs': [
						          
                        [(u"lower(death_code) = 'md'", u'Maternal Death'),[ 
						            (u"lower(location) = 'hp' AND lower(death_code) = 'md'", u'At Hospital'),
						            (u"lower(location) = 'hc' AND lower(death_code) = 'md'", u'At Health Centre'),
						            (u"lower(location) = 'or' AND lower(death_code) = 'md'", u'En Route'),
						            (u"lower(location) = 'ho' AND lower(death_code) = 'md'", u'At home')]],

                        [(u"lower(death_code) = 'nd'", u'Newborn Death'), [
                        (u"lower(location) = 'hp' AND lower(death_code) = 'nd'", u'At Hospital'),
						            (u"lower(location) = 'hc' AND lower(death_code) = 'nd'", u'At Health Centre'),
						            (u"lower(location) = 'or' AND lower(death_code) = 'nd'", u'En Route'),
						            (u"lower(location) = 'ho' AND lower(death_code) = 'nd'", u'At home')]],

                        [(u"lower(death_code) = 'cd'", u'Child Death'), [
                        (u"lower(location) = 'hp' AND lower(death_code) = 'cd'", u'At Hospital'),
						            (u"lower(location) = 'hc' AND lower(death_code) = 'cd'", u'At Health Centre'),
						            (u"lower(location) = 'or' AND lower(death_code) = 'cd'", u'En Route'),
						            (u"lower(location) = 'ho' AND lower(death_code) = 'cd'", u'At home')]],
                        
                        [(u"lower(death_code) = 'sbd'", u'Stillborn Death'), [
                        (u"lower(location) = 'hp' AND lower(death_code) = 'sbd'", u'At Hospital'),
						            (u"lower(location) = 'hc' AND lower(death_code) = 'sbd'", u'At Health Centre'),
						            (u"lower(location) = 'or' AND lower(death_code) = 'sbd'", u'En Route'),
						            (u"lower(location) = 'ho' AND lower(death_code) = 'sbd'", u'At home')]],

                        [(u"lower(death_code) = 'mcc'", u'Miscarriage Completed'), [
                        (u"lower(location) = 'hp' AND lower(death_code) = 'mcc'", u'At Hospital'),
						            (u"lower(location) = 'hc' AND lower(death_code) = 'mcc'", u'At Health Centre'),
						            (u"lower(location) = 'or' AND lower(death_code) = 'mcc'", u'En Route'),
						            (u"lower(location) = 'ho' AND lower(death_code) = 'mcc'", u'At home')]]					
					          ]
		    }

RED_DATA = {

		'attrs': [
				(u'red_symptom_ap IS NOT NULL', u'Acute Abd Pain Early Pregnancy') ,
				(u'red_symptom_co IS NOT NULL', u'Convulsions') ,
				(u'red_symptom_he IS NOT NULL', u'Hemorrhaging/Bleeding') ,
				(u'red_symptom_la IS NOT NULL', u'Mother in Labor at Home') ,
				(u'red_symptom_mc IS NOT NULL', u'Miscarriage') ,
				(u'red_symptom_pa IS NOT NULL', u'Premature Contraction') ,
				(u'red_symptom_ps IS NOT NULL', u'Labour with Previous C-Section') ,
				(u'red_symptom_sc IS NOT NULL', u'Serious Condition but Unknown') ,
				(u'red_symptom_sl IS NOT NULL', u'Stroke during Labor') ,
				(u'red_symptom_un IS NOT NULL', u'Unconscious'),
				( u'red_symptom_shb IS NOT NULL', u'Severe headache and/or blurry vision' ),
          ( u'red_symptom_sfh IS NOT NULL', u'Swollen feet and hand' ), 
				 ( u'red_symptom_bsp IS NOT NULL', u'Bad/foul smelling vaginal discharge' ), 
				 ( u'red_symptom_wu IS NOT NULL', u'Weak or unconscious or unresponsive to touch' ), 
				 ( u'red_symptom_hbt IS NOT NULL', u'High body temperature' ), 
				 ( u'red_symptom_lbt IS NOT NULL', u'Low body temperature or cold' ), 
				 ( u'red_symptom_cdg IS NOT NULL', u'Chest in-drawing or gasping' ), 
				 ( u'red_symptom_cop IS NOT NULL', u'Convulsions or is unconscious' ), 
				 ( u'red_symptom_hfp IS NOT NULL', u'High fever' ), 
				 ( u'red_symptom_con IS NOT NULL', u'Convulsion or fit' ), 
				 ( u'red_symptom_sbp IS NOT NULL', u'Sever bleeding' ), 
				 ( u'red_symptom_nuf IS NOT NULL', u'Not able to feed since birth/stopped feeding well' ), 
				 ( u'red_symptom_ncb IS NOT NULL', u'Umbilical cord bleeding' ), 
				 ( u'red_symptom_iuc IS NOT NULL', u'Infected umbilical cord' ), 
				 ( u'red_symptom_rv IS NOT NULL', u'Repeated Vomiting ' ), 
				 ( u'red_symptom_ads IS NOT NULL', u'Abdominal distension and stool arrest' ), 
				 ( u'red_symptom_nsc IS NOT NULL', u'Non stop crying' ), 
				 ( u'red_symptom_nbf IS NOT NULL', u'Bulging fontanel ' ), 
				 ( u'red_symptom_nhe IS NOT NULL', u'Hemorrhage ' ), 
				 ( u'red_symptom_ys IS NOT NULL', u'Yellow soles' ), 
				 ( u'red_symptom_sp IS NOT NULL', u'Skin pustules' ),  
			],

		}

RAR_DATA = {

		'attrs': [
				(u"lower(intervention) = 'al'", u'Ambulance Late') ,
				(u"lower(intervention) = 'at'", u'Ambulance on Time') ,
				(u"lower(intervention) = 'na'", u'No Ambulance Response') ,
        ],

      'outs': [
				(u"lower(health_status) = 'mw'", u'Mother Well(OK)') ,
				(u"lower(health_status) = 'ms'", u'Mother Sick') ,
        (u"lower(health_status) = 'cw'", u'Child Well(OK)') ,
				(u"lower(health_status) = 'cs'", u'Child Sick') ,
			],

		

		}


ERROR_PRONE_DATA = {
                'attrs': [
				                  (u"lower(error_code) = 'sender_not_registered' OR lower(error_code) = 'sender_not_connected'",
                            u'Sender not registered') ,
				                  (u"lower(error_code) != 'sender_not_registered' AND lower(error_code) != 'sender_not_connected'",
                            u'Invalid Report'),
                          ]
                 }


IDENTITY_COLS = [   ('indexcol', 'ID'),
                    ('created_at', 'Creation Date'),
                    ('updated_at', 'Modification Date'),
                    ('user_phone', 'Telephone'),
                    ('user_pk', 'Names'),
                    ('national_id', 'NID'),
                    ('nation_pk', 'Country'),
                    ('province_pk', 'Province'),
                    ('district_pk', 'District'),
                    ('referral_facility_pk', 'District Hospital'),
                    ('facility_pk', 'Health Centre'),
                    ('sector_pk', 'Sector'),
                    ('cell_pk', 'Cell'),
                    ('village_pk', 'Village'),
                  ]

SYMPTOMS_COLS = [
                  ('symptom_dhm', 'Severe dehydration, cardiovascular collapse or shock'),
                  ('symptom_nfm', 'Inability to drink or suckle'),
                  ('symptom_jam', 'Jaundice (yellow coloration of the conjunctival membranes) Hemoglobinuria (coca cola or dark urine)'),
                  ('symptom_rdm', 'Respiratory distress (respiratory acidosis) Acute pulmonary edema (radiological)'),
                  ('symptom_hem', 'Spontaneous hemorrhages (or disseminated intravascular coagulation - DIVC)'),
                  ('symptom_com', 'Convulsions ( >= 2 convulsions in 24 hours)'),
                  ('symptom_unm', 'Lethargy and unconsciousness'),
                  ('symptom_scm', 'Altered level of consciousness (somnolence, unconsciousness or deep coma)'),
                  ('symptom_prm', 'Prostration (extreme weakness, failure to be upright or walk)'),
                  ('symptom_anm', 'Anemia'),
                  ('symptom_rvm', 'Vomiting'),
                  ('symptom_wum', 'Coma'),
                  ]

DRUGS_COLS  =   [
                  ('drug_tdr', 'Rapid Diagnostic  Test'),
                  ('drug_ars', 'Artesunate Suppository'),
                  ('drug_al4', 'Art Lumefantrine 6x4'),
                  ('drug_al3', 'Art Lumefantrine 6x3'),
                  ('drug_al2', 'Art Lumefantrine 6x2'),
                  ('drug_al1', 'Art Lumefantrine 6x1'),
                  ('drug_ndm', 'No malaria drug given'),
                  ]

INTERVENTION_COLS = [
                        ('intervention_pr', 'Patient Directly Referred'),
                        ('intervention_na', 'No Ambulance Response'),
                        ('intervention_ca', 'CHW Advice'),
                        ('intervention_al', 'Ambulance Late'),
                        ('intervention_at', 'Ambulance on Time'),                      
                        ]


STATUS_COLS = [
                ('status', 'Patient Status'),
                ('is_alive', 'Is alive'),
                ('is_dead', 'Is dead'),
                
                ]




HC_COLS = [
                ('has_gone_hc', 'Received at HC'),
                ('hc_regno_code', 'HC RegNO/Code'),
                ('firstname', 'Firstname'),
                ('surname', 'Surname'),
                ('telephone', 'Patient Telephone'),
                ('household', 'Head of Household'),
                ('gender_pk', 'Sex'),
                ('date_of_birth', 'Date of Birth'),
                ('age', 'Age'),
                ('is_pregnant', 'Pregnant'),
                ('hc_ambulance', 'Ambulance provided at HC'),
                ('given_name', 'Given name'),
                ('sex_pk', 'Sex'),
                ('hc_arrival_datetime', 'Arrival datetime at HC'),
                ('hc_user_pk', 'Clinician at HC'),
                ('hc_tdr_result', 'TDR result'),
                ('hc_bs_result', 'BS result'),
                ('hc_hemoglobin', 'Hemoglobin'),
                ('hc_blood_glucose', 'Blood glucose'),
                ('hc_blood_group', 'Blood group'),
                ('hc_pretransfer_treatment', 'Pretransfer Treatment'),
                ('hc_transfered', 'Transfered to HD'),
                ('hc_ambulance_departure', 'Ambulance Departure'),
                ('hc_death', 'Death at HC'),

            ]

HD_COLS = [
                ('has_gone_hd', 'Received at HD'),
                ('hd_regno_code', 'HD RegNO/Code'),
                ('has_gone_hd_pk', 'HD'),
                ('hd_arrival_datetime', 'Arrival datetime at HD'),
                ('hd_user_pk', 'Clinician at HD'),
                ('hd_final_diagnostics', 'Final diagnostics at HD'),
                ('hd_patient_status', 'Patient status at HD'),
                ('hd_death', 'Death at HD'), 

          ]

EXTRA_COLS = [
                ('location', 'Patient Location'),
                
                ('facility_response', 'Response From HC/HD'),
                ('result', 'CHW Response'),
                ('notif', 'Notification'),
                ('has_gone_hc', 'Received at HC'),
                ('has_gone_hc_pk', 'HC'),

                ('firstname', 'Firstname'),
                ('surname', 'Surname'),
                ('telephone', 'Patient Telephone'),
                ('household', 'Head of Household'),
                ('gender_pk', 'Sex'),
                ('date_of_birth', 'Date of Birth'),
                ('age', 'Age'),
                ('is_pregnant', 'Pregnant'),
                ('hc_ambulance', 'Ambulance provided at HC'),
                ('given_name', 'Given name'),
                ('sex_pk', 'Sex'),
                ('hc_arrival_datetime', 'Arrival datetime at HC'),
                ('hc_user_pk', 'Clinician at HC'),
                ('hc_tdr_result', 'TDR result'),
                ('hc_bs_result', 'BS result'),
                ('hc_hemoglobin', 'Hemoglobin'),
                ('hc_blood_glucose', 'Blood glucose'),
                ('hc_blood_group', 'Blood group'),
                ('hc_pretransfer_treatment', 'Pretransfer Treatment'),
                ('hc_transfered', 'Transfered to HD'),
                ('hc_ambulance_departure', 'Ambulance Departure'),
                ('hc_death', 'Death at HC'),
              
                ('has_gone_hd', 'Received at HD'),
                ('has_gone_hd_pk', 'HD'),
                ('hd_arrival_datetime', 'Arrival datetime at HD'),
                ('hd_user_pk', 'Clinician at HD'),
                ('hd_final_diagnostics', 'Final diagnostics at HD'),
                ('hd_patient_status', 'Patient status at HD'),
                ('hd_death', 'Death at HD'),                
                
                ('keyword', 'Keyword'),
                ('message', 'Message'),
                

        ]

ERROR_PRONE_DATA = {
                      'attrs': [
                                ("lower(error_code) LIKE '%%sender_not_registered%%'", 'User Registration'),
                                ("lower(error_code) NOT LIKE '%%sender_not_registered%%'", 'Invalid Report'),
                               ],
                      'query_str': ''

                    }




