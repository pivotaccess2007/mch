import os

PSQL_HOST = '127.0.0.1'
PSQL_PORT = 5480
PSQL_DATABASE = 'rapidsmsrw'
PSQL_USER = 'rapidsmsrw'
PSQL_PASSWORD = 'rapidsmsrw'

'
MySQL_HOST = '127.0.0.1'
MySQL_PORT = 3380
MySQL_DATABASE = 'rapidsmsrw'
MySQL_USER = 'rapidsmsrw'
MySQL_PASSWORD = 'rapidsmsrw'


MySQL_HOST1 = '127.0.0.1'
MySQL_PORT1 = 3380
MySQL_DATABASE1 = 'rapidsmsrw'
MySQL_USER1 = 'rapidsmsrw'
MySQL_PASSWORD1 = 'rapidsmsrw'

INC_ID = 15505788 


WEBAPP          = 'mch'
TRACKING_DAYS	= 2100
GESTATION       = 270
NBC_GESTATION   = 28
PNC_GESTATION   = 42
ANC_GAP         = 90
BMI_MIN         = 19
BMI_MAX         = 25
MIN_WEIGHT      = 45
MAX_WEIGHT      = 65
SALT_STRENGTH   = 2
SECRET 		= "hjkjlkjlkl;k" 
AUTH_HOME       = '/dashboards/home'
PREGNANCY_TRIMESTER = [ (0, 90), (91, 180), (181, 270) ]
FACILITIES = []

# ref : (table, sort column)
# Default sort column (None) is: report_date
EXPORT_KEYS     = {
  '_'       : ('rw_pregnancies', None),
  'patient' : ('rw_mothers', 'indangamuntu'),
  'child' : ('rw_children', 'indexcol'),
  'chw': ('chws_reporter', None)
}

APP_DATA  = {
  'indicators'  : [
    {'name':'Reporting',
      'title' : 'Reports and Reporters',
      'ref'   : 'reporting'},
    {'name':'Pregnant Women',
      'ref':'mothers'},
    {'name':'Pregnancies',
      'ref':'pregnancies'},
    {'name':'Babies',
      'ref':'babies'},
    {'name':'Expected Deliveries',
      'ref':'delivs'},
    {'name':'Severe Malaria',
      'title' : 'Severe Malaria Notifications',
      'ref'   : 'malariadash'}
    # {'name':'Red Alerts',
    #   'ref':'alerts'},
    #{'name':'Admins',
    #  'ref':'admins'},
    # {'name':'Sanitation',
    #   'title' : 'Toilets and Water',
    #   'ref'   : 'sanitation'}
  ],
  'rindicators'  : [
    {'name':'Ante-Natal',
      'ref':'anc'},
    {'name':'Birth Reports',
      'ref':'birthreport'},
    {'name':'Pregnancies',
      'ref':'pregnancy'},
    {'name':'Deliveries',
      'ref':'delivery'},
    {'name':'New-Born Care',
      'ref':'nbc'},
    {'name':'Vaccinations',
      'ref':'vaccination'},
    {'name':'Nutrition',
      'ref':'nutrition'},
    {'name':'Child Health',
      'ref':'childhealth'},
    {'name':'CCM',
      'title' : 'Community Case Management',
      'ref'   : 'ccm'},
    {'name':'PNC',
      'title' : 'Post-Natal Care',
      'ref'   : 'pnc'},
    {'name':'Red Alerts',
      'title' : 'Red Alerts',
      'ref'   : 'redalert'},
    {'name':'Death',
      'title' : 'Death Reports',
      'ref'   : 'death'},	
    {'name':'Severe Malaria',
      'title' : 'Severe Malaria Notifications',
      'ref'   : 'malariadash'}
  ]
}
