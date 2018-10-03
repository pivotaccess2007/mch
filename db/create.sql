--
-- RapidSMS Rwanda - PostgreSQL database structure
--

-- Developed by PIVOT ACCESS LTD
-- @author UWANTWALI ZIGAMA Didier
-- d.zigama@pivotaccess.com/zigdidier@gmail.com
--
--

-- RapidSMS Rwanda - Tracking maternal and < 5 children health to prevent unnecessary deaths 
--
-- The system is primarily used by Community Health Workers -- CHWs; using mobile phones
-- And Ministry of Health of Rwanda to analyze the information collected by CHWs
--
--

CREATE TABLE module (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE
);

INSERT INTO module (created_at, updated_at, name, code) VALUES (current_timestamp, current_timestamp, 'SMS Report', 'SMS');
INSERT INTO module (created_at, updated_at, name, code) VALUES (current_timestamp, current_timestamp, 'Reminder', 'REM');
INSERT INTO module (created_at, updated_at, name, code) VALUES (current_timestamp, current_timestamp, 'End User', 'USR');
INSERT INTO module (created_at, updated_at, name, code) VALUES (current_timestamp, current_timestamp, 'Messaging', 'MSG');
INSERT INTO module (created_at, updated_at, name, code) VALUES (current_timestamp, current_timestamp, 'Dashboard', 'WUI');
INSERT INTO module (created_at, updated_at, name, code) VALUES (current_timestamp, current_timestamp, 'Integration', 'API');
INSERT INTO module (created_at, updated_at, name, code) VALUES (current_timestamp, current_timestamp, 'Notification', 'NOTI');

CREATE TABLE endresource (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    url text,
    code text NOT NULL UNIQUE,
    rw text,
    en text,
    fr text,
    field_separator text,
    syntax_regex text, 
    case_sensitive boolean,
    in_use boolean,
    module_pk integer NOT NULL
);

INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Pregnancy', 'PRE', 'Ugusama', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 
		VALUES (current_timestamp, current_timestamp, 'Antenatal Consultation', 'ANC', 'Ukwipimisha', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Refusal', 'REF', 'Ukwanga', ' ', TRUE, TRUE, '', 1);

INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Red Alert', 'RED', 'Ibibazo simusiga', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 		VALUES   (current_timestamp, current_timestamp, 'Red Alert Result', 'RAR', 'Igisubizo ku bibazo simusiga', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Risk', 'RISK', 'Ibibazo mpuruza', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 			VALUES   (current_timestamp, current_timestamp, 'Risk Result', 'RES', 'Igisubizo ku bibazo mpuruza', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Departure', 'DEP', 'Ukwimuka', ' ', TRUE, TRUE, '', 1);

INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Birth', 'BIR', 'Ukuvuka', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 			VALUES   (current_timestamp, current_timestamp, 'Postnatal Care', 'PNC', 'Isurwa ry''umubyeyi', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 			VALUES   (current_timestamp, current_timestamp, 'Newborn Care', 'NBC', 'Isurwa ry''uruhinja', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Child Health', 'CHI', 'Ugukingira', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 
		VALUES (current_timestamp, current_timestamp, 'Community Based Nutrition','CBN', 'Imirire', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk)
	VALUES (current_timestamp, current_timestamp, 'Community Case Management', 'CCM', 'Ukuvura abana', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 
	VALUES (current_timestamp, current_timestamp, 'Case Management Response', 'CMR', 'Iherezo ry''uburwayi', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Death', 'DTH', 'Urupfu', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, url, case_sensitive, in_use, syntax_regex, module_pk) 
			VALUES   (current_timestamp, current_timestamp, 'Home', 'INDEX', 'Ahabanza', '/', TRUE, TRUE, '', 5);

INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Severe Malaria', 'SMN', 'Malaria', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Severe Malaria Result', 'SMR', 'Malaria', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Risk Of Stock Out', 'RSO', 'Sitoke', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Stock out', 'SO', 'Sitoke', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Stock Supplied', 'SS', 'Sitoke', ' ', TRUE, TRUE, '', 1);
INSERT INTO endresource (created_at, updated_at, name, code, rw, field_separator, case_sensitive, in_use, syntax_regex, module_pk) 				VALUES   (current_timestamp, current_timestamp, 'Who', 'WHO', 'Ninde', ' ', TRUE, TRUE, '', 1);

UPDATE  endresource SET en = name ;


CREATE TABLE privilege(
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    code text NOT NULL UNIQUE,
    name text,
    url  text,
    endresource_pk integer
);

CREATE TABLE user_privilege(
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    privilege_pk integer,
    role_pk integer,
    user_pk integer
);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'REDNOTI', 'Receive red alert notification', '/dashboards/reddash', 4);
INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'SMNNOTI', 'Receive malaria case notification', '/dashboards/malariadash', 18);
INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'HOME', 'Home Page', '/dashboards/home', 17);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'SMN', 'Severe Malaria', '/dashboards/malariadash', 18);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'STOCK', 'Drug Stock-Out', '/dashboards/stockdash', 22);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'DIAG', 'Diagnosis Form', '/dashboards/diagnosisdash', 18);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'PRE', 'Information on mothers and pregnancies', '/dashboards/predash', 1);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'NBC', 'Information on newborns', '/dashboards/nbcdash', 11);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'CBN', 'Information on child nutrition', '/dashboards/nutrdash', 13);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'PNC', 'Information postal natal care', '/dashboards/pncdash', 10);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'CCM', 'Information on CCM', '/dashboards/ccmdash', 14);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'CHI', 'Information on Vaccination', '/dashboards/vaccindash', 12);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'RED', 'Information on red alerts', '/dashboards/reddash', 4);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'DTH', 'Information on deaths', '/dashboards/deathdash', 16);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'USER', 'Information on users and activities', '/dashboards/userdash', 23);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'REPORT', 'Information on reports', '/dashboards/reportsdash', 17);

INSERT INTO privilege (created_at, updated_at, code, name, url, endresource_pk) VALUES   (current_timestamp, current_timestamp, 'ADMIN', 'Information on system administartion', '/dashboards/adminsite', 17);

CREATE TABLE smsfield(
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    code text NOT NULL,
    name_en text,
    category_en text,
    name_rw text,
    category_rw text,
    prefix text,
    description text NOT NULL,
    type_of_value text,
    upper_case boolean NOT NULL,
    lower_case boolean NOT NULL,
    minimum_value double precision,
    maximum_value double precision,
    minimum_length double precision,
    maximum_length double precision,
    position_after_sms_keyword smallint NOT NULL,
    depends_on_value_of_pk integer,
    dependency text,
    allowed_value_list text,
    only_allow_one boolean NOT NULL,
    required boolean NOT NULL, 
    sms_report_pk integer NOT NULL
    
);


CREATE TABLE smscode(
	indexcol SERIAL NOT NULL,
	created_at timestamp without time zone DEFAULT now() NOT NULL,
	updated_at timestamp without time zone,
	code text NOT NULL,
	prefix text,
	position integer NOT NULL,
	smskey text NOT NULL,
	name_en text,
	name_fr text,
	name_rw text,
        is_value boolean DEFAULT FALSE	
);


CREATE TABLE role (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE
);

--
--
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (1, current_timestamp, current_timestamp, 'ASM', 'ASM');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (2, current_timestamp, current_timestamp, 'Binome', 'BINOME');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (3, current_timestamp, current_timestamp, 'Supervisor', 'SUP');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (4, current_timestamp, current_timestamp, 'Monitor Evaluator', 'MNE');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (5, current_timestamp, current_timestamp, 'Data Manager', 'DTM');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (6, current_timestamp, current_timestamp, 'Hospital Director', 'HODI');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (7, current_timestamp, current_timestamp, 'Ambulance Coordinator', 'AMBC');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (8, current_timestamp, current_timestamp, 'Chief of Supervisors', 'CSUP');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (9, current_timestamp, current_timestamp, 'Chief of Drivers', 'CDRV');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (10, current_timestamp, current_timestamp, 'Chief of Emergency', 'CEMG');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (11, current_timestamp, current_timestamp, 'Chief of Maternity', 'CMAT');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (12, current_timestamp, current_timestamp, 'Chief of Nursing', 'CNUR');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (13, current_timestamp, current_timestamp, 'Chief of Medical Staff', 'CMEDI');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (14, current_timestamp, current_timestamp, 'Administrator', 'ADMIN');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (15, current_timestamp, current_timestamp, 'Headquarter Staff', 'HQ');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (16, current_timestamp, current_timestamp, 'Head of HC', 'HOHC');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (17, current_timestamp, current_timestamp, 'Clinician', 'CLN');
-- INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (18, current_timestamp, current_timestamp, 'Logistics', 'LOG');
--
--

INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (1, current_timestamp, current_timestamp, 'ASM', 'ASM');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (2, current_timestamp, current_timestamp, 'Binome', 'BINOME');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (3, current_timestamp, current_timestamp, 'Cell Coordinator', 'CECO');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (4, current_timestamp, current_timestamp, 'Supervisor', 'SUP');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (5, current_timestamp, current_timestamp, 'Monitor & Evaluator', 'MNE');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (6, current_timestamp, current_timestamp, 'Data Manager', 'DTM');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (7, current_timestamp, current_timestamp, 'Logistics', 'LOG');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (8, current_timestamp, current_timestamp, 'Head of Health Centre', 'HOHC');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (9, current_timestamp, current_timestamp, 'Clinician', 'CLN');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (10, current_timestamp, current_timestamp, 'Director of Nursing', 'DNUR');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (11, current_timestamp, current_timestamp, 'Clinical Director', 'DCLN');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (12, current_timestamp, current_timestamp, 'Hospital Director General', 'HODI');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (13, current_timestamp, current_timestamp, 'Headquarter Staff', 'HQ');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (14, current_timestamp, current_timestamp, 'Administrator', 'ADMIN');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (15, current_timestamp, current_timestamp, 'Director of Health Unity', 'DHU');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (16, current_timestamp, current_timestamp, 'Pharmacy Data Manager', 'PDM');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (17, current_timestamp, current_timestamp, 'Pharmacy Director', 'PHD');
INSERT INTO role (indexcol, created_at, updated_at, name, code) VALUES (18, current_timestamp, current_timestamp, 'Environmental Health office', 'EHO');



CREATE TABLE education_level (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE 
);

INSERT INTO education_level (indexcol, created_at, updated_at, name, code) VALUES (1, current_timestamp, current_timestamp, 'Primary', 'P');
INSERT INTO education_level (indexcol, created_at, updated_at, name, code) VALUES (2, current_timestamp, current_timestamp, 'Secondary', 'S');
INSERT INTO education_level (indexcol, created_at, updated_at, name, code) VALUES (3, current_timestamp, current_timestamp, 'University', 'U');
INSERT INTO education_level (indexcol, created_at, updated_at, name, code) VALUES (4, current_timestamp, current_timestamp, 'None', 'N');


CREATE TABLE location_level (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE 
);


INSERT INTO location_level (indexcol, created_at, updated_at, name, code) VALUES (1, current_timestamp, current_timestamp, 'Nation', 'NATION');
INSERT INTO location_level (indexcol, created_at, updated_at, name, code) VALUES (2, current_timestamp, current_timestamp, 'Province', 'PRV');
INSERT INTO location_level (indexcol, created_at, updated_at, name, code) VALUES (3, current_timestamp, current_timestamp, 'District', 'DST');
INSERT INTO location_level (indexcol, created_at, updated_at, name, code) VALUES (4, current_timestamp, current_timestamp, 'National Referral Hospital', 'NRH');
INSERT INTO location_level (indexcol, created_at, updated_at, name, code) VALUES (5, current_timestamp, current_timestamp, 'Military Hospital', 'MH');
INSERT INTO location_level (indexcol, created_at, updated_at, name, code) VALUES (6, current_timestamp, current_timestamp, 'District Hospital', 'HD');
INSERT INTO location_level (indexcol, created_at, updated_at, name, code) VALUES (7, current_timestamp, current_timestamp, 'Hospital', 'HP');
INSERT INTO location_level (indexcol, created_at, updated_at, name, code) VALUES (8, current_timestamp, current_timestamp, 'Health Centre', 'HC');
INSERT INTO location_level (indexcol, created_at, updated_at, name, code) VALUES (9, current_timestamp, current_timestamp, 'Clinic', 'CL');
INSERT INTO location_level (indexcol, created_at, updated_at, name, code) VALUES (10, current_timestamp, current_timestamp, 'Sector', 'SEC');
INSERT INTO location_level (indexcol, created_at, updated_at, name, code) VALUES (11, current_timestamp, current_timestamp, 'Cell', 'CEL');
INSERT INTO location_level (indexcol, created_at, updated_at, name, code) VALUES (12, current_timestamp, current_timestamp, 'Village', 'VIL');


CREATE TABLE language (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE,
    description text 
);


INSERT INTO language (indexcol, created_at, updated_at, name, code) VALUES (1, current_timestamp, current_timestamp, 'Kinyarwanda', 'RW');
INSERT INTO language (indexcol, created_at, updated_at, name, code) VALUES (2, current_timestamp, current_timestamp, 'English', 'EN');
INSERT INTO language (indexcol, created_at, updated_at, name, code) VALUES (3, current_timestamp, current_timestamp, 'Français', 'FR');


CREATE TABLE gender (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE 
);


INSERT INTO gender (indexcol, created_at, updated_at, name, code) VALUES (1, current_timestamp, current_timestamp, 'Male', 'M');
INSERT INTO gender (indexcol, created_at, updated_at, name, code) VALUES (2, current_timestamp, current_timestamp, 'Female', 'F');

CREATE TABLE nation (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE,
    latitude float,
    longitude float
);


INSERT INTO nation (indexcol, created_at, updated_at, name, code, latitude, longitude) VALUES (1, current_timestamp, current_timestamp, 'Rwanda', 'RW', -1.9499500, 30.0588500);


CREATE TABLE province (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE,
    nation_pk integer,
    latitude float,
    longitude float
);


CREATE TABLE district (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE,
    nation_pk integer,
    province_pk integer,
    latitude float,
    longitude float
);


CREATE TABLE sector (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    latitude float,
    longitude float
);


CREATE TABLE cell (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    sector_pk integer,
    latitude float,
    longitude float
);


CREATE TABLE village (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    sector_pk integer,
    cell_pk integer,
    latitude float,
    longitude float
);


CREATE TABLE facility (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    name text NOT NULL,
    code text NOT NULL UNIQUE,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_type_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,
    latitude float,
    longitude float
);



CREATE TABLE simcard (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    spn text NOT NULL,
    mcc text NOT NULL,
    mnc text NOT NULL,
    msin text NOT NULL,
    msisdn text NOT NULL UNIQUE
);


COMMENT ON COLUMN simcard.spn IS  'Service Provider Name - e.g: MTN ';
COMMENT ON COLUMN simcard.mcc IS  'Mobile Country Code - e.g: 250 ';
COMMENT ON COLUMN simcard.mnc IS  'Mobile Network Code - e.g: 78 ';
COMMENT ON COLUMN simcard.msin IS 'Mobile subscriber identification number - e.g: 8660270';
COMMENT ON COLUMN simcard.msisdn IS 'Mobile Station International Subscriber Directory Number - e.g: +250788660270';

INSERT INTO simcard (indexcol, created_at, updated_at, spn, mcc, mnc, msin, msisdn) VALUES (1, current_timestamp, current_timestamp, 'MTN', '250', '78', '8660270', '+250788660270');

CREATE TABLE enduser (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    simcard_pk integer,
    telephone character varying(13) NOT NULL,
    national_id character varying(16) NOT NULL UNIQUE,
    surname text,
    given_name text,
    date_of_birth timestamp without time zone,
    sex_pk integer, 
    education_level_pk integer,
    language_pk integer,
    join_date timestamp without time zone,
    email text,
    salt text,
    passwd text,
    role_pk integer,
    location_level_pk integer, 
    nation_pk integer,
    province_pk integer,
    district_pk integer,    
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,          
    last_seen timestamp without time zone,
    is_active boolean,
    is_correct boolean
);

CREATE TABLE mother(
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    telephone text,
    national_id character varying(16) NOT NULL UNIQUE ,
    user_phone text,
    user_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer
);


CREATE TABLE pregnancy (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    lmp timestamp without time zone,
    anc2_date timestamp without time zone,
    gravidity integer,
    parity integer,

    prev_pregnancy_gs text,
    prev_pregnancy_hd text,
    prev_pregnancy_kx text,
    prev_pregnancy_lz text,
    prev_pregnancy_mu text,
    prev_pregnancy_nr text,
    prev_pregnancy_ol text,
    prev_pregnancy_rm text,
    prev_pregnancy_yg text,
    prev_pregnancy_yj text,    

    symptom_af text,
    symptom_ch text,
    symptom_di text,
    symptom_ds text,
    symptom_fe text,
    symptom_fp text,
    symptom_hy text,
    symptom_ja text,
    symptom_ma text,
    symptom_np text,
    symptom_ns text,
    symptom_oe text,
    symptom_pc text,
    symptom_sa text,
    symptom_rb text,
    symptom_vo text,    
	
    location text,
    mother_weight double precision,
    mother_height integer,
    
    toilet text,
    handwash text,    
    
    bmi double precision DEFAULT 0.0,
    muac double precision,
    message text,
    is_valid boolean
);


CREATE TABLE birth (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    birth_date timestamp without time zone,
    child_number integer,
    pregnancy_pk integer,
    sex_pk integer,
    sex text,

    symptom_af text,
    symptom_ci text,
    symptom_cm text,
    symptom_pm text,
    symptom_np text,
    symptom_rb text,  
	
    location text,
    breastfeeding text,
    child_weight double precision,

    message text,
    is_valid boolean
);


CREATE TABLE refusal (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    message text,
    is_valid boolean

);

CREATE TABLE ancvisit (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    anc_date timestamp without time zone,
    pregnancy_pk integer,
    anc_visit text,

    symptom_af text,
    symptom_ch text,
    symptom_di text,
    symptom_ds text,
    symptom_fe text,
    symptom_fp text,
    symptom_hy text,
    symptom_ja text,
    symptom_ma text,
    symptom_np text,
    symptom_ns text,
    symptom_oe text,
    symptom_pc text,
    symptom_sa text,
    symptom_rb text,
    symptom_vo text,    
	
    location text,
    mother_weight double precision,
    muac double precision,

    message text,
    is_valid boolean
);


CREATE TABLE risk (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    pregnancy_pk integer,
    
    symptom_af text,
    symptom_ch text,
    symptom_di text,
    symptom_ds text,
    symptom_fe text,
    symptom_fp text,
    symptom_hy text,
    symptom_ja text,
    symptom_ma text,
    symptom_ns text,
    symptom_oe text,
    symptom_pc text,
    symptom_sa text,
    symptom_rb text,
    symptom_vo text,    
	
    location text,
    mother_weight double precision,

    message text,
    is_valid boolean
);

CREATE TABLE riskresult (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    pregnancy_pk integer,
    risk_pk integer,
    
    symptom_af text,
    symptom_ch text,
    symptom_di text,
    symptom_ds text,
    symptom_fe text,
    symptom_fp text,
    symptom_hy text,
    symptom_ja text,
    symptom_ma text,
    symptom_ns text,
    symptom_oe text,
    symptom_pc text,
    symptom_sa text,
    symptom_rb text,
    symptom_vo text,    
	
    location text,
    intervention text,
    health_status text,

    message text,
    is_valid boolean
);

CREATE TABLE redalert (
	indexcol SERIAL NOT NULL,
	created_at timestamp without time zone DEFAULT now() NOT NULL,
	updated_at timestamp without time zone,

	user_phone text,
	user_pk integer,
	national_id text,
	mother_pk integer,
	nation_pk integer,
	province_pk integer,
	district_pk integer,
	referral_facility_pk integer,
	facility_pk integer,
	sector_pk integer,
	cell_pk integer,
	village_pk integer,

	birth_date timestamp without time zone,
	child_number integer,
	pregnancy_pk integer,
	child_pk integer,
    
    	red_symptom_ap text,
	red_symptom_co text,
	red_symptom_he text,
	red_symptom_la text,
	red_symptom_mc text,
	red_symptom_pa text,
	red_symptom_ps text,
	red_symptom_sc text,
	red_symptom_sl text,
	red_symptom_un text,    
	red_symptom_shb text,
	red_symptom_sfh text,
	red_symptom_cop text,
	red_symptom_hfp text,
	red_symptom_sbp text,
	red_symptom_shp text,
	red_symptom_bsp text,
	red_symptom_con text,
	red_symptom_wu text,
	red_symptom_hbt text,
	red_symptom_lbt text,
	red_symptom_nt text,
	red_symptom_cdg text,
	red_symptom_ys text,
	red_symptom_rsb text,
	red_symptom_iuc text,
	red_symptom_ncb text,
	red_symptom_rv text,
	red_symptom_ads text,
	red_symptom_nsc text,
	red_symptom_nbf text,
	red_symptom_sp text,
	red_symptom_nhe text,
	red_symptom_nuf text,
	
	location text,
	mother_weight double precision,
	child_weight double precision,

	message text,
	is_valid boolean
);


CREATE TABLE redresult (
	indexcol SERIAL NOT NULL,
	created_at timestamp without time zone DEFAULT now() NOT NULL,
	updated_at timestamp without time zone,

	user_phone text,
	user_pk integer,
	national_id text,
	mother_pk integer,
	nation_pk integer,
	province_pk integer,
	district_pk integer,
	referral_facility_pk integer,
	facility_pk integer,
	sector_pk integer,
	cell_pk integer,
	village_pk integer,

	emergency_date timestamp without time zone,
	red_pk integer,

	birth_date timestamp without time zone,
	child_number integer,
	pregnancy_pk integer,
	child_pk integer,
	
    
    	red_symptom_ads text,
	red_symptom_cdg text,
	red_symptom_co text,
	red_symptom_con text,
	red_symptom_hbt text,
	red_symptom_hfp text,
	red_symptom_iuc text,
	red_symptom_lbt text,
	red_symptom_mc text,
	red_symptom_nbf text,
	red_symptom_ncb text,
	red_symptom_nhe text,
	red_symptom_nsc text,
	red_symptom_nuf text,
	red_symptom_pa text,
	red_symptom_ps text,
	red_symptom_rv text,
	red_symptom_sbp text,
	red_symptom_sfh text,
	red_symptom_shb text,
	red_symptom_shp text,
	red_symptom_sp text,
	red_symptom_wu text,
	red_symptom_ys text,
	red_symptom_ap text,
	red_symptom_bsp text,
	red_symptom_cop text,
	red_symptom_he text,
	red_symptom_la text,
	red_symptom_sc text,
	red_symptom_sl text,
	red_symptom_un text,    
	
	location text,
	intervention text,
	health_status text,

	message text,
	is_valid boolean
);

CREATE TABLE departure (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    birth_date timestamp without time zone,
    child_number integer,
    pregnancy_pk integer,
    child_pk integer,

    message text,
    is_valid boolean
);


CREATE TABLE death (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    birth_date timestamp without time zone,
    child_number integer,
    pregnancy_pk integer,
    child_pk integer,

    location text,
    death_code text,

    message text,
    is_valid boolean
);


CREATE TABLE nbcvisit (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    birth_date timestamp without time zone,
    child_number integer,
    pregnancy_pk integer,
    child_pk integer,
    nbc_visit text,

    symptom_af text,
    symptom_ci text,
    symptom_cm text,
    symptom_np text,
    symptom_pm text,
    symptom_rb text,    
	
    breastfeeding text,
    intervention text,
    health_status text,

    message text,
    is_valid boolean
);

CREATE TABLE pncvisit (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    delivery_date timestamp without time zone,
    pregnancy_pk integer,
    child_pk integer,
    pnc_visit text,

    symptom_ch text,
    symptom_di text,
    symptom_ds text,
    symptom_fe text,
    symptom_fp text,
    symptom_hy text,
    symptom_ja text,
    symptom_ma text,
    symptom_np text,
    symptom_ns text,
    symptom_oe text,
    symptom_pc text,
    symptom_sa text,
    symptom_rb text,
    symptom_vo text,    
	
    intervention text,
    health_status text,

    message text,
    is_valid boolean
);

CREATE TABLE childhealth (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    birth_date timestamp without time zone,
    child_number integer,
    pregnancy_pk integer,
    child_pk integer,
    vaccine text,
    vaccine_status text,

    symptom_ib text,
    symptom_db text,
    symptom_np text,  
	
    location text,
    child_weight double precision,
    muac double precision,

    message text,
    is_valid boolean
);


CREATE TABLE nutrition (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    birth_date timestamp without time zone,
    child_number integer,
    pregnancy_pk integer,
    child_pk integer, 
	
    breastfeeding text,
    child_weight double precision,
    child_height double precision,
    muac double precision,

    message text,
    is_valid boolean
);


CREATE TABLE ccm (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    birth_date timestamp without time zone,
    child_number integer,
    pregnancy_pk integer,
    child_pk integer,
 
    symptom_ib text,
    symptom_db text,
    symptom_di text,
    symptom_ma text,
    symptom_np text,
    symptom_oi text,
    symptom_pc text,
    symptom_nv text,    
	
    intervention text,
    muac double precision,

    message text,
    is_valid boolean
);

CREATE TABLE cmr (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    national_id text,
    mother_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    birth_date timestamp without time zone,
    child_number integer,
    pregnancy_pk integer,
    child_pk integer,
    ccm_pk integer,

    symptom_ib text,
    symptom_db text,
    symptom_di text,
    symptom_ma text,
    symptom_np text,
    symptom_oi text,
    symptom_pc text,
    symptom_nv text,    
	
    intervention text,
    health_status text,

    message text,
    is_valid boolean
);


CREATE TABLE malaria (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    role_pk integer,
    national_id text,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    keyword text,
    symptom_dhm text,
    symptom_nfm text,
    symptom_jam text,
    symptom_rdm text,
    symptom_hem text,
    symptom_com text,
    symptom_unm text,
    symptom_scm text,
    symptom_prm text,
    symptom_anm text,
    symptom_rvm text,
    symptom_wum text,

    drug_tdr text,
    drug_ars text,
    drug_al4 text,
    drug_al2 text,
    drug_al3 text,
    drug_al1 text,
    drug_ndm text,

    intervention_pr text,
    intervention_na text,
    intervention_ca text,
    intervention_al text,
    intervention_at text,
    location text,
    status text,
    facility_response text,
    result boolean,
    notif integer,
    refused boolean,

    given_name text,
    surname text,
    telephone text,
    household text,
    sex_pk integer,
    date_of_birth timestamp without time zone,
    age integer,
    is_pregnant boolean,

    has_gone_hc boolean,
    hc_regno_code text,
    has_gone_hc_pk integer,
    hc_arrival_datetime timestamp without time zone,
    hc_user_pk integer, 
    hc_tdr_result text,
    hc_bs_result text,
    hc_hemoglobin text,
    hc_blood_glucose text,
    hc_blood_group text,
    hc_pretransfer_treatment text,
    hc_transfered boolean,
    hc_ambulance boolean, 
    hc_ambulance_departure timestamp without time zone,
    hc_death boolean,
        
    has_gone_hd boolean,
    hd_regno_code text,
    has_gone_hd_pk integer,
    hd_arrival_datetime timestamp without time zone,
    hd_user_pk integer,
    hd_final_diagnostics text,
    hd_patient_status text,

    is_alive boolean,
    is_dead boolean,

    message text,
     
    is_valid boolean DEFAULT TRUE

);

CREATE TABLE stock (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    role_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    keyword text,
    drug_tdr text,
    drug_ars text,
    drug_al4 text,
    drug_al2 text,
    drug_al3 text,
    drug_al1 text,

    message text,
    is_valid boolean DEFAULT TRUE

);

CREATE TABLE migration_status (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    nation integer,
    nation_count integer,
    province integer,
    province_count integer,
    district integer,
    district_count integer,
    sector integer,
    sector_count integer,
    cell integer,
    cell_count integer,
    village integer,
    village_count integer,
    hospital integer,
    hospital_count integer,
    health_centre integer,
    health_centre_count integer,
    reporter integer,
    reporter_count integer,
    pre integer,
    pre_count integer,
    bir integer,
    bir_count integer,
    anc integer,
    anc_count integer,
    risk integer,
    risk_count integer,
    res integer,
    res_count integer,
    rar integer,
    rar_count integer,
    red integer,
    red_count integer,
    dep integer,
    dep_count integer,
    refusal integer,
    refusal_count integer,
    chi integer,
    chi_count integer,
    nbc integer,
    nbc_count integer,
    pnc integer,
    pnc_count integer,
    dth integer,
    dth_count integer,
    ccm integer,
    ccm_count integer,
    cmr integer,
    cmr_count integer,
    cbn integer,
    cbn_count integer
);



CREATE TABLE enderror (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    message text,
    error_code text,
    is_valid boolean DEFAULT TRUE

);

CREATE TABLE download (

    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,

    user_phone text,
    user_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,

    description text,
    filename text,
    filters text,
    start_date timestamp without time zone, 
    end_date timestamp without time zone,
    status text DEFAULT 'PROCESSING',
    is_valid boolean DEFAULT TRUE

);

CREATE TABLE bulk_sms (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    message text NOT NULL,
    to_group text,
    user_phone text,
    user_pk integer,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,
    is_valid boolean DEFAULT TRUE	
    
);

CREATE TABLE ambulance (
    indexcol SERIAL NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone,
    coordinator text,
    simcard_pk integer,
    telephone text NOT NULL,
    nation_pk integer,
    province_pk integer,
    district_pk integer,
    referral_facility_pk integer,
    facility_pk integer,
    sector_pk integer,
    cell_pk integer,
    village_pk integer,
    is_valid boolean DEFAULT TRUE	
    
);
    

ALTER TABLE ancvisit ADD COLUMN lmp timestamp without time zone;
UPDATE ancvisit SET lmp = (SELECT lmp FROM pregnancy WHERE pregnancy.indexcol = ancvisit.pregnancy_pk);

ALTER TABLE mother ADD COLUMN previous_lmp timestamp without time zone;
ALTER TABLE mother ADD COLUMN recent_lmp timestamp without time zone;
ALTER TABLE mother ADD COLUMN previous_mother_weight double precision;
ALTER TABLE mother ADD COLUMN previous_mother_height integer;
ALTER TABLE mother ADD COLUMN recent_mother_weight double precision;
ALTER TABLE mother ADD COLUMN recent_mother_height integer;
ALTER TABLE mother ADD COLUMN previous_bmi double precision DEFAULT 0.0;
ALTER TABLE mother ADD COLUMN recent_bmi double precision DEFAULT 0.0;
ALTER TABLE mother ADD COLUMN previous_muac double precision DEFAULT 0.0;
ALTER TABLE mother ADD COLUMN recent_muac double precision DEFAULT 0.0;
ALTER TABLE mother ADD COLUMN is_valid boolean DEFAULT TRUE;

ALTER TABLE birth ADD COLUMN recent_breastfeeding text;
ALTER TABLE birth ADD COLUMN previous_child_weight double precision;
ALTER TABLE birth ADD COLUMN previous_child_height integer;
ALTER TABLE birth ADD COLUMN recent_child_weight double precision;
ALTER TABLE birth ADD COLUMN recent_child_height integer;
ALTER TABLE birth ADD COLUMN previous_bmi double precision DEFAULT 0.0;
ALTER TABLE birth ADD COLUMN recent_bmi double precision DEFAULT 0.0;
ALTER TABLE birth ADD COLUMN previous_muac double precision DEFAULT 0.0;
ALTER TABLE birth ADD COLUMN recent_muac double precision DEFAULT 0.0;
ALTER TABLE birth ADD COLUMN weight_for_age double precision DEFAULT 0.0;
ALTER TABLE birth ADD COLUMN height_for_age double precision DEFAULT 0.0;
ALTER TABLE birth ADD COLUMN weight_for_height double precision DEFAULT 0.0;


UPDATE smsfield SET category_en = 'Location' WHERE code = 'or';
ALTER TABLE redalert ADD COLUMN red_symptom_rsb text;
ALTER TABLE redresult ADD COLUMN red_symptom_rsb text;
ALTER TABLE redalert ADD COLUMN red_symptom_nt text;
ALTER TABLE redresult ADD COLUMN red_symptom_nt text;

ALTER TABLE malaria ADD COLUMN given_name text;
ALTER TABLE malaria ADD COLUMN surname text;
ALTER TABLE malaria ADD COLUMN telephone text;
ALTER TABLE malaria ADD COLUMN household text;
ALTER TABLE malaria ADD COLUMN sex_pk integer;
ALTER TABLE malaria ADD COLUMN date_of_birth timestamp without time zone;
ALTER TABLE malaria ADD COLUMN age integer;
ALTER TABLE malaria ADD COLUMN is_pregnant boolean;

ALTER TABLE malaria ADD COLUMN has_gone_hc boolean;
ALTER TABLE malaria ADD COLUMN has_gone_hc_pk integer;
ALTER TABLE malaria ADD COLUMN hc_arrival_datetime timestamp without time zone;
ALTER TABLE malaria ADD COLUMN hc_user_pk integer; 
ALTER TABLE malaria ADD COLUMN hc_tdr_result text;
ALTER TABLE malaria ADD COLUMN hc_bs_result text;
ALTER TABLE malaria ADD COLUMN hc_hemoglobin text;
ALTER TABLE malaria ADD COLUMN hc_blood_glucose text;
ALTER TABLE malaria ADD COLUMN hc_blood_group text;
ALTER TABLE malaria ADD COLUMN hc_pretransfer_treatment text;
ALTER TABLE malaria ADD COLUMN hc_transfered boolean;
ALTER TABLE malaria ADD COLUMN hc_ambulance boolean; 
ALTER TABLE malaria ADD COLUMN hc_ambulance_departure timestamp without time zone;
ALTER TABLE malaria ADD COLUMN hc_death boolean;

ALTER TABLE malaria ADD COLUMN hd_arrival_datetime timestamp without time zone;
ALTER TABLE malaria ADD COLUMN hd_user_pk integer;
ALTER TABLE malaria ADD COLUMN hd_final_diagnostics text;
ALTER TABLE malaria ADD COLUMN hd_patient_status text;


UPDATE smsfield SET position_after_sms_keyword = smsfield.position_after_sms_keyword + 1 WHERE smsfield.sms_report_pk = (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'PNC');

UPDATE smsfield SET position_after_sms_keyword = 1 WHERE smsfield.sms_report_pk = (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'PNC') AND code = 'nid';

UPDATE smsfield SET allowed_value_list = 'pnc2;pnc3;pnc4;pnc5' WHERE smsfield.sms_report_pk = (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'PNC') AND position_after_sms_keyword = 3;

UPDATE smsfield SET position_after_sms_keyword = 2 WHERE smsfield.sms_report_pk = (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'PNC') AND position_after_sms_keyword = 3;

UPDATE smsfield SET position_after_sms_keyword = 3, code='yego', allowed_value_list='yego;oya' WHERE smsfield.sms_report_pk = (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'PNC') AND code = 'pnc1';


INSERT INTO smsfield (created_at, updated_at, code, name_en, category_en, name_rw, category_rw, prefix, description, type_of_value, upper_case, lower_case, minimum_value, maximum_value, minimum_length, maximum_length, position_after_sms_keyword, depends_on_value_of_pk, dependency, allowed_value_list, only_allow_one, required, sms_report_pk) VALUES (current_timestamp, current_timestamp, 'oya', 'First PNC', 'Number of Standard PNC', 'Gusura umubyeyi wabyaye bwa mbere mu rugo', 'Inshuro umubyeyi wabyaye asuwe mu rugo', '', 'First PNC', 'string', FALSE, FALSE, NULL, NULL, 4, 4, 3, NULL, '', 'yego;oya', TRUE, TRUE, (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'PNC'));


INSERT INTO smsfield (created_at, updated_at, code, name_en, category_en, name_rw, category_rw, prefix, description, type_of_value, upper_case, lower_case, minimum_value, maximum_value, minimum_length, maximum_length, position_after_sms_keyword, depends_on_value_of_pk, dependency, allowed_value_list, only_allow_one, required, sms_report_pk) VALUES (current_timestamp, current_timestamp, 'pnc4', 'Fourth PNC', 'Number of Standard PNC', 'Gusura umubyeyi wabyaye bwa kane mu rugo', 'Inshuro umubyeyi wabyaye asuwe mu rugo', '', 'Fourth PNC', 'string', FALSE, FALSE, NULL, NULL, 4, 4, 2, NULL, '', 'pnc2;pnc3;pnc4;pnc5', TRUE, TRUE, (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'PNC'));



INSERT INTO smsfield (created_at, updated_at, code, name_en, category_en, name_rw, category_rw, prefix, description, type_of_value, upper_case, lower_case, minimum_value, maximum_value, minimum_length, maximum_length, position_after_sms_keyword, depends_on_value_of_pk, dependency, allowed_value_list, only_allow_one, required, sms_report_pk) VALUES (current_timestamp, current_timestamp, 'pnc5', 'Fifth PNC', 'Number of Standard PNC', 'Gusura umubyeyi wabyaye bwa gatanu mu rugo', 'Inshuro umubyeyi wabyaye asuwe mu rugo', '', 'Fifth PNC', 'string', FALSE, FALSE, NULL, NULL, 4, 4, 2, NULL, '', 'pnc2;pnc3;pnc4;pnc5', TRUE, TRUE, (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'PNC'));


UPDATE smsfield SET position_after_sms_keyword = smsfield.position_after_sms_keyword + 1 WHERE smsfield.sms_report_pk = (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'NBC');

UPDATE smsfield SET position_after_sms_keyword = 1 WHERE smsfield.sms_report_pk = (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'NBC') AND code = 'nid';

UPDATE smsfield SET allowed_value_list = 'nbc2;nbc3;nbc4;nbc5' WHERE smsfield.sms_report_pk = (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'NBC') AND position_after_sms_keyword = 4;

UPDATE smsfield SET position_after_sms_keyword = 2 WHERE smsfield.sms_report_pk = (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'NBC') AND position_after_sms_keyword = 3;

UPDATE smsfield SET position_after_sms_keyword = 3 WHERE smsfield.sms_report_pk = (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'NBC') AND position_after_sms_keyword = 4;

UPDATE smsfield SET position_after_sms_keyword = 4, code='yego', allowed_value_list='yego;oya' WHERE smsfield.sms_report_pk = (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'NBC') AND code = 'nbc1';


INSERT INTO smsfield (created_at, updated_at, code, name_en, category_en, name_rw, category_rw, prefix, description, type_of_value, upper_case, lower_case, minimum_value, maximum_value, minimum_length, maximum_length, position_after_sms_keyword, depends_on_value_of_pk, dependency, allowed_value_list, only_allow_one, required, sms_report_pk) VALUES (current_timestamp, current_timestamp, 'oya', 'First NBC', 'Number of Standard NBC', 'Gusura uruhinja bwa mbere mu rugo', 'Inshuro uruhinja rusuwe mu rugo', '', 'First NBC', 'string', FALSE, FALSE, NULL, NULL, 4, 4, 4, NULL, '', 'yego;oya', TRUE, TRUE, (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'NBC'));

UPDATE smsfield SET position_after_sms_keyword = smsfield.position_after_sms_keyword + 1 WHERE smsfield.sms_report_pk = (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'NBC' AND position_after_sms_keyword > 5);

INSERT INTO smsfield (created_at, updated_at, code, name_en, category_en, name_rw, category_rw, prefix, description, type_of_value, upper_case, lower_case, minimum_value, maximum_value, minimum_length, maximum_length, position_after_sms_keyword, depends_on_value_of_pk, dependency, allowed_value_list, only_allow_one, required, sms_report_pk) VALUES (current_timestamp, current_timestamp, 'yego', 'Polio1, Penta1, PCV1, Rota1', 'Vaccination', 'Polio1, Penta1, PCV1, Rota1', 'Inkingo', '', 'Polio1, Penta1, PCV1, Rota1', 'string', FALSE, FALSE, NULL, NULL, 4, 4, 6, NULL, '', 'yego;oya', TRUE, TRUE, (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'NBC'));

INSERT INTO smsfield (created_at, updated_at, code, name_en, category_en, name_rw, category_rw, prefix, description, type_of_value, upper_case, lower_case, minimum_value, maximum_value, minimum_length, maximum_length, position_after_sms_keyword, depends_on_value_of_pk, dependency, allowed_value_list, only_allow_one, required, sms_report_pk) VALUES (current_timestamp, current_timestamp, 'oya', 'Polio1, Penta1, PCV1, Rota1', 'Vaccination', 'Polio1, Penta1, PCV1, Rota1', 'Inkingo', '', 'Polio1, Penta1, PCV1, Rota1', 'string', FALSE, FALSE, NULL, NULL, 4, 4, 6, NULL, '', 'yego;oya', TRUE, TRUE, (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'NBC'));


ALTER TABLE pregnancy ADD column role_pk integer;
ALTER TABLE ancvisit ADD COLUMN role_pk integer;
ALTER TABLE refusal ADD COLUMN role_pk integer;
ALTER TABLE redalert ADD COLUMN role_pk integer;
ALTER TABLE redresult ADD COLUMN role_pk integer;
ALTER TABLE risk ADD COLUMN role_pk integer;
ALTER TABLE riskresult ADD COLUMN role_pk integer;
ALTER TABLE departure ADD COLUMN role_pk integer;
ALTER TABLE birth ADD COLUMN role_pk integer;
ALTER TABLE pncvisit ADD COLUMN role_pk integer;
ALTER TABLE nbcvisit ADD COLUMN role_pk integer;
ALTER TABLE childhealth ADD COLUMN role_pk integer;
ALTER TABLE nutrition ADD COLUMN role_pk integer;
ALTER TABLE ccm ADD COLUMN role_pk integer;
ALTER TABLE cmr ADD COLUMN role_pk integer;
ALTER TABLE death ADD COLUMN role_pk integer;
ALTER TABLE malaria ADD COLUMN role_pk integer;
ALTER TABLE stock ADD COLUMN role_pk integer;


UPDATE  pregnancy SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  ancvisit SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  refusal SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  redalert SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  redresult SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  risk SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  riskresut SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  departure SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  birth SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  pncvisit SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  nbcvisit SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  childhealth SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  nutrition SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  ccm SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  cmr SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  death SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  malaria SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);
UPDATE  stock SET role_pk = (SELECT enduser.role_pk FROM enduser WHERE enduser.indexcol = user_pk);


-- ALREADY EXISTS
-- INSERT INTO smsfield (created_at, updated_at, code, name_en, category_en, name_rw, category_rw, prefix, description, type_of_value, upper_case, lower_case, minimum_value, maximum_value, minimum_length, maximum_length, position_after_sms_keyword, depends_on_value_of_pk, dependency, allowed_value_list, only_allow_one, required, sms_report_pk) VALUES (current_timestamp, current_timestamp, 'nbc5', 'Fifth NBC', 'Number of Standard NBC', 'Gusura uruhinja bwa gatanu mu rugo', 'Inshuro uruhinja rusuwe mu rugo', '', 'Fifth NBC', 'string', FALSE, FALSE, NULL, NULL, 4, 4, 3, NULL, '', 'nbc2;nbc3;nbc4;nbc5', TRUE, TRUE, (SELECT endresource.indexcol FROM endresource WHERE endresource.code = 'NBC'));







