#!  /usr/bin/env python
# encoding: utf-8
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

import sys
import cherrypy
import re
import urllib2, urlparse
from jinja2 import Environment, FileSystemLoader
import json

from controller.main import MchAuth, RSMSRWController
from controller.pregnancies import PregnancyController
from controller.births import BirthController
from controller.ancvisits import AncvisitController
from controller.nbcvisits import NbcvisitController
from controller.pncvisits import PncvisitController
from controller.ccms import CCMController
from controller.childhealths import ChildhealthController
from controller.nutritions import NutritionController
from controller.deaths import DeathController
from controller.redalerts import RedalertController
from controller.endusers import EnduserController
from controller.roles import RoleController
from controller.privileges import PrivilegeController
from controller.ambulances import AmbulanceController
from controller.facilities import FacilityController
from controller.malarias import MalariaController
from controller.stocks import StockController
from controller.reports import ReportController
from controller.admins import AdminController
from controller.downloads import DownloadController
from controller.enderrors import EnderrorController

from util.jsonify import CustomEncoder



reload(sys)
sys.setdefaultencoding("utf-8")


def get_display(value):
 if type(value) == bool:
  if value == True: return 'Yes'
  elif value == False: return 'No'
  else: return ''
 elif value is None: return ''
 else: return value
 return value

def get_link(link, key, value):
    result = re.search('%s=(.*|\d+\"|&)' % (key), link)
    if result:
        new_link =  link.replace(result.group(0) , '%s=%s%s' % (key,value, result.group(1)))
        ##print new_link 
        return "%s" % (new_link)
    return link

def neat_numbers(num):
  pcs = divided_num(str(num), 3)
  return ','.join(pcs)

def make_date(dt):
  return dt.strftime('%d/%m/%Y')

def first_cap(s):
  if not s: return s
  return ' '.join([x[0].upper() + x[1:] for x in re.split(r'\s+', s)])

def divided_num(num, mx = 3):
  if len(num) < (mx + 1):
    return [num]
  lft = num[0:-3]
  rgt = num[-3:]
  return divided_num(lft) + [rgt]

def report_summary(row):
  ans = []#read_record_row(row, orm)
  return ','.join(an for an in ans)


class Application:
  def __init__(self, templates, statics, static_path, app_data,FACILITIES, **kw):
    self.templates    = templates
    self.statics      = statics
    self.static_path  = static_path
    self.kw           = kw
    self.app_data     = app_data
    self.facilities   = FACILITIES
    self.jinja        = Environment(loader = FileSystemLoader(templates))
    self.jinja.filters.update({
      'neat_numbers'  : neat_numbers,
      'get_display'  : get_display,
      'report_summary': report_summary,
      'get_link': get_link,
      'make_date': make_date 
    })
    
    self._cp_config = {'request.error_response': self.internal_error}

  def ctrl(self, email, token):
    auth = MchAuth(email = email, token = token, facilities = self.facilities)
    if not auth.token:
        raise cherrypy.HTTPRedirect('/')
    ctrl = RSMSRWController(auth)
    return [ctrl, ctrl.auth]
    
  def match(self, url):
    got = url[1:].replace('/', '_') or 'index'
    sys.stderr.write('%40s:\t%s\n' % (url, got))
    return url[1:].replace('/', '_') or 'index'

  def dynamised(self, chart, mapping = {}, *args, **kw):
    info  = {}
    info.update({
      'ref'           : re.sub(r'_table$', '', chart),
      'args'          : kw,
      'nav'           : mapping.get('navb', None),
      'static_path'   : self.static_path
    })
    info.update(self.app_data)
    info.update(kw)
    mapping.pop('self', None)
    #mapping['locs'] = json.dumps(mapping.get('locs'), cls=CustomEncoder)
    info.update({'display': mapping})
    return self.jinja.get_template('%s.html' % (chart, )).render(*args, **info)

  def internal_error(self):
    path = urlparse.urlparse(cherrypy.request.__dict__.get('headers').get('Referer')).path
    raise cherrypy.HTTPRedirect(path)

  @cherrypy.expose
  def default(self, *args, **kwargs):
    #raise cherrypy.HTTPRedirect("/dashboards/errorpage")
    return self.dashboards_errorpage()
    """return ("This is a catch all page, it can handle any URL that you throw. "
                "If there is no match in any other previous handler this "
                "is going to be executed: <br/>"
                "<pre>args: %s \nkwargs: %s</pre>" % (args, kwargs))
    """

  @cherrypy.expose
  def index(self, *args, **kw):
    flash = cherrypy.session.pop('flash', '')
    user  = cherrypy.session.get('user', '')
    user  = cherrypy.session.get('token', '')
    user  = cherrypy.session.get('email', '')
    return self.dynamised('index', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_home(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token')) 
    ##print "USERNAME: ", auth.username()
    return self.dynamised('home', mapping = locals(), *args, **kw)


  @cherrypy.expose
  @cherrypy.tools.json_out()
  @cherrypy.tools.json_in()
  def login(self):
    try:
        credentials = cherrypy.request.json
        email = credentials.get("email")
        password = credentials.get("password")
        token = credentials.get("token")
        if not ((email and password) or token):
            return {"code": 400, "message": "Invalid Credentials, please provide your email and password."}   
        auth = MchAuth(email = email, password = password, token = token)
        if hasattr(auth, 'token') and auth.token:
            return {"code": 200, "message": "User has been successfully authenticated!", "token": token}    
        return {"code": 401, "message": "User could not be authenticated, please contact RBC-MoH staff"}
    except:
        return {"code": 400, "message": "Invalid Request or Missing required parameters"}

  @cherrypy.expose
  def authentication(self, *args, **kw):
    eml                       = kw.get('addr')
    pwd                       = kw.get('pwd')
    tkn                       = kw.get('token')
    auth                     = MchAuth(email = eml, password = pwd, token = tkn)
    token                    = auth.login()
    cherrypy.session['user']  = eml
    if kw.get('resetpwd'):
       raise cherrypy.HTTPRedirect('/dashboards/resetpwd') 
    if kw.get('logout'):
      cherrypy.session.pop('email', '')
      cherrypy.session.pop('token', '')
      raise cherrypy.HTTPRedirect('/')
    if token:
      cherrypy.session['email'] = eml
      cherrypy.session['token'] = token
    else:
      cherrypy.session['flash'] = 'Access Denied'
      raise cherrypy.HTTPRedirect('/')
    if kw.get('next'):
      raise cherrypy.HTTPRedirect(kw.get('next'))
    raise cherrypy.HTTPRedirect(auth_pages.get('HOME'))


  @cherrypy.expose
  def locs(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs = ctrl.navigate(auth, *args, **kw)
    my_locs = json.dumps(locs, cls=CustomEncoder)
    ##print my_locs
    return my_locs

  @cherrypy.expose
  def filter_locs(self, loctype, locparentid,  *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    ##print "PARAMS: ", loctype, locparentid, auth.__dict__
    locs = auth.auth_filter_locations(loctype, locparentid)
    my_locs = json.dumps(locs, cls=CustomEncoder)
    ##print my_locs
    return my_locs

  @cherrypy.expose
  def dashboards_errorpage(self, *args, **kw):
    token = cherrypy.session.get('token')
    email = cherrypy.session.get('email')
    if not token:
        cherrypy.session['flash'] = 'Access Denied'
        raise cherrypy.HTTPRedirect('/')
    if not email:
        cherrypy.session['flash'] = 'Invalid Credentials, please provide your email and password.'
        raise cherrypy.HTTPRedirect('/')

    ctrl, auth    = self.ctrl(email, token)
    navb, locs    = ctrl.navigate(auth, *args, **kw)    
    return self.dynamised('error', mapping = locals(), *args, **kw)



#######
######### START OF DASHBOARD PAGES
#######

  @cherrypy.expose
  def dashboards_predash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    ##print navb.auth_pages
    if not navb.auth_pages.get('PRE'):
        priv = navb.privileges.get('PRE'); #print "PRIV", priv
        return self.dynamised('noprivilege', mapping = locals(), *args, **kw) 
    pregctrl = PregnancyController(navb)
    total   = pregctrl.get_total()
    title, group, attrs, nat = pregctrl.get_stats()    
    return self.dynamised('predash', mapping = locals(), *args, **kw) 

  @cherrypy.expose
  def tables_predash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    pregctrl = PregnancyController(navb)
    total   = pregctrl.get_total()
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS = pregctrl.get_tables()    
    return self.dynamised('predash_table', mapping = locals(), *args, **kw) 

  @cherrypy.expose
  def dashboards_deliverynotdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)#;#print "LOCS: ", locs
    pregctrl = PregnancyController(navb)
    title, group, attrs, nat, details = pregctrl.get_deilivery_notifications()    
    return self.dynamised('deliverynotdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_deliverynotdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)#;#print "LOCS: ", locs
    pregctrl = PregnancyController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS = pregctrl.get_deilivery_notifications_tables()    
    return self.dynamised('deliverynotdash_table', mapping = locals(), *args, **kw) 

  @cherrypy.expose
  def dashboards_deliverydash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    birctrl = BirthController(navb)
    attrs, nat     = birctrl.get_stats()
    return self.dynamised('deliverydash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_deliverydash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    birctrl = BirthController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS  = birctrl.get_tables()
    return self.dynamised('deliverydash_table', mapping = locals(), *args, **kw) 

  @cherrypy.expose
  def dashboards_ancdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    ancctrl = AncvisitController(navb)
    attrs, pre, nat     = ancctrl.get_stats()
    return self.dynamised('ancdash', mapping = locals(), *args, **kw) 

  @cherrypy.expose
  def tables_ancdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    ancctrl = AncvisitController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS = ancctrl.get_tables()
    return self.dynamised('ancdash_table', mapping = locals(), *args, **kw) 

  @cherrypy.expose
  def dashboards_nbcdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    if not navb.auth_pages.get('NBC'):
        priv = navb.privileges.get('NBC'); #print "PRIV", priv
        return self.dynamised('noprivilege', mapping = locals(), *args, **kw) 
    nbcctrl = NbcvisitController(navb)
    title, group, attrs, nat = nbcctrl.get_stats()
    return self.dynamised('nbcdash', mapping = locals(), *args, **kw) 

  @cherrypy.expose
  def tables_nbcdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    nbcctrl = NbcvisitController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS = nbcctrl.get_tables()
    return self.dynamised('nbcdash_table', mapping = locals(), *args, **kw) 

  @cherrypy.expose
  def dashboards_pncdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    if not navb.auth_pages.get('PNC'):
        priv = navb.privileges.get('PNC'); #print "PRIV", priv
        return self.dynamised('noprivilege', mapping = locals(), *args, **kw)
    pncctrl = PncvisitController(navb)
    title, group, attrs, nat = pncctrl.get_stats()
    return self.dynamised('pncdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_pncdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    pncctrl = PncvisitController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS = pncctrl.get_tables()
    return self.dynamised('pncdash_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_ccmdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    if not navb.auth_pages.get('CCM'):
        priv = navb.privileges.get('CCM'); #print "PRIV", priv
        return self.dynamised('noprivilege', mapping = locals(), *args, **kw)
    ccmctrl = CCMController(navb)
    ccm_attrs, cmr_attrs, ccm, cmr     = ccmctrl.get_stats()
    return self.dynamised('ccmdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_ccmdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    ccmctrl = CCMController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS     = ccmctrl.get_tables()
    return self.dynamised('ccmdash_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_vaccindash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    if not navb.auth_pages.get('CHI'):
        priv = navb.privileges.get('CHI'); #print "PRIV", priv
        return self.dynamised('noprivilege', mapping = locals(), *args, **kw)
    vaccinctrl    = ChildhealthController(navb)
    vac_comps_attrs, vac_series_attrs, nat     = vaccinctrl.get_stats()
    return self.dynamised('vaccindash', mapping = locals(), *args, **kw) 

  @cherrypy.expose
  def tables_vaccindash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    vaccinctrl    = ChildhealthController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS     = vaccinctrl.get_tables()
    return self.dynamised('vaccindash_table', mapping = locals(), *args, **kw) 

  @cherrypy.expose
  def dashboards_nutrdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    if not navb.auth_pages.get('CBN'):
        priv = navb.privileges.get('CBN'); #print "PRIV", priv
        return self.dynamised('noprivilege', mapping = locals(), *args, **kw)
    nutrctrl = NutritionController(navb)
    chi_nutr, pre_nutr     = nutrctrl.get_stats()
    return self.dynamised('nutrdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_nutrdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    nutrctrl = NutritionController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS     = nutrctrl.get_tables()
    return self.dynamised('nutrdash_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_reddash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    if not navb.auth_pages.get('RED'):
        priv = navb.privileges.get('RED'); #print "PRIV", priv
        return self.dynamised('noprivilege', mapping = locals(), *args, **kw)
    redctrl = RedalertController(navb)
    red_attrs, rar_attrs, rar_outs, red, rar     = redctrl.get_stats()
    return self.dynamised('reddash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_reddash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    redctrl = RedalertController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS     = redctrl.get_tables()
    return self.dynamised('reddash_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_deathdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    if not navb.auth_pages.get('DTH'):
        priv = navb.privileges.get('DTH'); #print "PRIV", priv
        return self.dynamised('noprivilege', mapping = locals(), *args, **kw)
    dthctrl = DeathController(navb)
    attrs, attrs_bylocs, nat     = dthctrl.get_stats()
    return self.dynamised('deathdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_deathdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    dthctrl = DeathController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS     = dthctrl.get_tables()
    return self.dynamised('deathdash_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_reportsdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    if not navb.auth_pages.get('REPORT'):
        priv = navb.privileges.get('REPORT'); #print "PRIV", priv
        return self.dynamised('noprivilege', mapping = locals(), *args, **kw)
    reportctrl = ReportController(navb)
    attrs, data, total     = reportctrl.get_stats()
    return self.dynamised('reportsdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_report(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    reportctrl = ReportController(navb)
    report     = reportctrl.get_report()
    return self.dynamised('report', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_reportsdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    reportctrl = ReportController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS    = reportctrl.get_tables()
    return self.dynamised('reportsdash_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_reminderdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    remctrl = ReminderController(navb)
    attrs, pre, nat     = remctrl.get_stats()
    return self.dynamised('reminderdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_reminderdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    remctrl = ReminderController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS   = remctrl.get_tables()
    return self.dynamised('reminderdash_table', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def dashboards_userdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    if not navb.auth_pages.get('USER'):
        priv = navb.privileges.get('USER'); #print "PRIV", priv
        return self.dynamised('noprivilege', mapping = locals(), *args, **kw)
    userctrl      = EnduserController(navb)
    attrs, avg, nat    = userctrl.get_stats()
    return self.dynamised('userdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_activate(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    userctrl      = EnduserController(navb)
    message, user = userctrl.activate()
    return self.dynamised('user', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_groupmessage(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    userctrl      = EnduserController(navb)
    roles, message    = userctrl.group_messaging()
    return self.dynamised('groupmessage', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_seachupdateuser(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    userctrl      = EnduserController(navb)
    return self.dynamised('searchuser', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_userdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    userctrl      = EnduserController(navb)
    title, desc, group, attrs, markup, cols, nat    = userctrl.get_tables()
    ##print nat.query
    return self.dynamised('userdash_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_registeruser(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    userctrl      = EnduserController(navb)
    genders, roles, education_levels, area_levels, langs, message, user       = userctrl.register_user()
    nat = userctrl.get_total()
    return self.dynamised('registeruser', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_updateuser(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    userctrl      = EnduserController(navb)
    sectors, cells, villages, genders, roles, education_levels, area_levels, langs, message, user       = userctrl.update_user()
    nat = userctrl.get_total()
    return self.dynamised('updateuser', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_usersearch(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    userctrl      = EnduserController(navb)
    users          = userctrl.get_users()
    return self.dynamised('search', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_usertrail(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    userctrl      = EnduserController(navb)
    users          = userctrl.get_users()
    return self.dynamised('usertrail', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_chwupload(self, *args, **kw):
    ctrl, auth      = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs      = ctrl.navigate(auth, *args, **kw)
    userctrl        = EnduserController(navb)
    if navb.kw.get('template'):
        lnk = '/static/files/upload_template.xls'
        raise cherrypy.HTTPRedirect(lnk)
    errors, message  = userctrl.upload_users()
    return self.dynamised('uploaduser', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_adminsite(self, *args, **kw):
    ctrl, auth      = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs      = ctrl.navigate(auth, *args, **kw)
    if not navb.auth_pages.get('ADMIN'):
        priv = navb.privileges.get('ADMIN'); #print "PRIV", priv
        return self.dynamised('noprivilege', mapping = locals(), *args, **kw)
    adminctrl        = AdminController(navb)
    return self.dynamised('admins', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_ambulance(self, *args, **kw):
    ctrl, auth      = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs      = ctrl.navigate(auth, *args, **kw)
    ambctrl        = AmbulanceController(navb)
    message, amb = None, None
    if navb.kw.get("amb_facility") and navb.kw.get('telephone_moh'):
        message, amb = ambctrl.register_ambulance()

    nat, attrs    = ambctrl.get_stats()    
    ##print nat[0]
    return self.dynamised('ambulance', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_facilities(self, *args, **kw):
    ctrl, auth      = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs      = ctrl.navigate(auth, *args, **kw) 
    facctrl        = FacilityController(navb)
    message, fac, factype = None, None, navb.kw.get('factype')
    if navb.kw.get("facname") and navb.kw.get('faccode'):
        message, fac, facs = facctrl.register_facility()
        if facs:    self.facilities = facs

    nat, attrs    = facctrl.get_stats()    
    ##print nat[0]
    return self.dynamised('facilities', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_roles(self, *args, **kw):
    ctrl, auth      = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs      = ctrl.navigate(auth, *args, **kw) 
    rolectrl        = RoleController(navb)
    message, role = None, None
    #print navb.kw
    if navb.kw.get("rolename") and navb.kw.get('rolecode'):
        message, role = rolectrl.register_role()

    nat, attrs    = rolectrl.get_stats()    
    ##print nat[0]
    return self.dynamised('roles', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_privileges(self, *args, **kw):
    ctrl, auth      = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs      = ctrl.navigate(auth, *args, **kw) 
    privctrl        = PrivilegeController(navb)
    message, assigned_privileges = None, []
    if navb.kw.get("privileges") and ( navb.kw.get('role') or navb.kw.get('telephone') ):
        #print navb.kw
        message, assigned_privileges = privctrl.register_privileges()

    roles, privileges, nat, attrs    = privctrl.get_stats() 
       
    ##print nat[0]
    return self.dynamised('privileges', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def tables_ambulance(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    ambctrl      = AmbulanceController(navb)
    title, desc, group, attrs, markup, cols, nat    = ambctrl.get_tables()
    ##print nat.query
    return self.dynamised('ambulance_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_facilities(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    facctrl      = FacilityController(navb)
    factype = navb.kw.get('factype')
    title, desc, group, attrs, markup, cols, nat    = facctrl.get_tables()
    ##print nat.query
    return self.dynamised('facilities_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_roles(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    rolectrl      = RoleController(navb)
    title, desc, group, attrs, markup, cols, nat    = rolectrl.get_tables()
    ##print nat.query
    return self.dynamised('roles_table', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def dashboards_diagnosisdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    smctrl        = MalariaController(navb)
    report, locs, user, genders, area_levels, message, received   = smctrl.register_diagnosis()
    if received is True:
        ##print received, report.__dict__, report
        lnk = '/dashboards/report?tbl=smn&id=%s' % report.indexcol#; #print lnk
        raise cherrypy.HTTPRedirect(lnk)
    return self.dynamised('diagnosis', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_patientdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    smctrl        = MalariaController(navb)
    nid, desc, nat, cols, markup, message  = smctrl.get_patient_logs()
    ##print nat, cols, type(markup), message
    return self.dynamised('patient_trail', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_malariadash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    ##print navb.auth_pages
    if not navb.auth_pages.get('SMN'):
        priv = navb.privileges.get('SMN'); #print "PRIV", priv
        return self.dynamised('error', mapping = locals(), *args, **kw) 
    smctrl      = MalariaController(navb)
    attrs, nat          = smctrl.get_stats()
    return self.dynamised('malariadash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def dashboards_stockdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    if not navb.auth_pages.get('STOCK'):
        priv = navb.privileges.get('STOCK'); #print "PRIV", priv
        return self.dynamised('noprivilege', mapping = locals(), *args, **kw)
    stctrl      = StockController(navb)
    attrs, nat          = stctrl.get_stats()
    return self.dynamised('stockdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_malariadash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    smctrl      = MalariaController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS = smctrl.get_tables()
    ##print title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS
    return self.dynamised('malariadash_table', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_stockdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    stctrl      = StockController(navb)
    title, desc, group, attrs, markup, cols, nat = stctrl.get_tables()
    return self.dynamised('stockdash_table', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def resetpwd(self, *args, **kw):
    email = kw.get('addr')
    otp = kw.get('otp')
    tkn = kw.get('tkn')
    new_passwd = kw.get('pwd')
    ##print email, otp, tkn, new_passwd
    changed   = EnduserController.change_password(email, tkn, otp, new_passwd)
    if not changed: cherrypy.session['flash'] = "You cannot change your password now, contact system administration"
    else:
        success = "You have successfully changed your password, then login"        
    return self.dynamised('index', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def forgotpwd(self, *args, **kw):
    email = kw.get('email')#;#print "RESET EMAIL: ", email, kw, args
    tkn, otp      = EnduserController.reset_password(email)
    if not otp:
        error = "You may not change your password now, OTP seems not sent, contact system administrator"
    if not tkn:
        cherrypy.session['flash'] = "You cannot change your password now, your email seems invalid, contact system administrator"
        raise cherrypy.HTTPRedirect('/')
    return self.dynamised('forgotpwd', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def dashboards_exportsdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    dwnctrl      = DownloadController(navb)
    message, download = dwnctrl.download_file()
    if download:
        if download.status == 'COMPLETE':
            message = "File is ready."
            lnk = '/static/files/%s' % download.filename
            raise cherrypy.HTTPRedirect(lnk)
        else:
            message = "File is still being processing. Please copy and save download link for checking later or wait ..."
    if navb.kw.get('more'):
        raise cherrypy.HTTPRedirect('/tables/exportsdash')  
    return self.dynamised('exportsdash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_exportsdash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    dwnctrl      = DownloadController(navb)
    message, download = dwnctrl.download_file()
    if download:
        if download.status == 'COMPLETE':
            message = "File is ready."
            lnk = '/static/files/%s' % download.filename
            raise cherrypy.HTTPRedirect(lnk)
        else:
            message = "File is still being processing. Please copy and save download link for checking later or wait ..."
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS = dwnctrl.get_tables()
    return self.dynamised('exportsdash_table', mapping = locals(), *args, **kw)


  @cherrypy.expose
  def dashboards_errordash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    errctrl = EnderrorController(navb)
    attrs, avg, nat     = errctrl.get_stats()
    return self.dynamised('errordash', mapping = locals(), *args, **kw)

  @cherrypy.expose
  def tables_errordash(self, *args, **kw):
    ctrl, auth    = self.ctrl(cherrypy.session.get('email'), cherrypy.session.get('token'))
    navb, locs    = ctrl.navigate(auth, *args, **kw)
    errctrl = EnderrorController(navb)
    title, desc, group, attrs, markup, cols, nat, tabular, locateds, INDICS_HEADERS  = errctrl.get_tables()
    return self.dynamised('errordash_table', mapping = locals(), *args, **kw)


#######
######### END OF DASHBOARD PAGES
#######
    

