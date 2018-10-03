#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"


from datetime import datetime, timedelta
import urllib2, urlparse
import re

from util.mch_security import MchSecurity, GESTATION
from underscore import _ as UNDERSCORE
from util.record import fetch_location, fetch_table_cols, fetch_facilities
from util.mch_util import first_cap


class MchLocation:
  def __init__(self, loc, tp, nav, lmt, ttl, chop  = None):
    self.location   = loc
    self.loctype    = tp
    self.navigator  = nav
    self.title      = ttl
    self.limits     = lmt
    self.chop       = chop

  def __unicode__(self):
    nom = self.location.name
    return u'%s %s' % (nom if not self.chop else self.chop(nom), self.title)

  @property
  def name(self):
    nom = self.location.name
    return nom if not self.chop else self.chop(nom)

  def link(self, ref):
    pcs, qrs  = self.navigator.pre_link(self.navigator.link(ref))
    for l in self.limits:
      try:              del qrs[l]
      except KeyError:  pass
    return urlparse.urlunsplit((pcs[0], pcs[1], pcs[2], '&'.join(['%s=%s' % (k, urllib2.quote(qrs[k])) for k in qrs if qrs[k]]), pcs[4]))

class MchAuth:
  def __init__(self, email=None, password = None, token = None, facilities = []):
    self.usern  = email
    self.pwd = password
    self.token   = token
    self.facilities = facilities   

  def login(self):
    user = self.get_user()    
    if user:
        token =  MchSecurity.generatedToken(self.usern, self.pwd)
        ##print "TOKEN: \n", token, "\n", self.usern, "\n", user.__dict__, "\n"
    else:
        token = None
    return token

  def get_user(self):
    user = MchSecurity.authenticateUser(email = self.usern, passwd = self.pwd, token = self.token)
    return user

  def username(self):
    return self.usern
  
  def auth_pages(self, user):
    return MchSecurity.get_auth_pages(user)

  def auth_villages(self):
    return MchSecurity.get_auth_villages(self.user)

  def auth_filter_locations(self, loctype, locparentid):
    self.user = self.get_user()
    return MchSecurity.get_auth_filter_locations(self.user, loctype, locparentid)

  def auth_facilities(self):
    try:
        ##print "FAC: ", len(self.facilities)
        tot = fetch_table_cols('facility', {}, cols = ['COUNT(*) AS value'])[0]
        if len(self.facilities) != tot.value:
            self.facilities = fetch_facilities()
        if self.facilities:
            KEYS = MchSecurity.get_user_facility_level_filter_keys(self.user)
            ##print "KEYS: ", KEYS
            FACS = UNDERSCORE(self.facilities).chain().filter(lambda x, *args: getattr(x, KEYS[0]) == KEYS[1]
                                              ).indexBy(lambda x, *args: x.indexcol).map(lambda x, *args: x).sortBy().value()
            ##print "AUTH FACS: ", len(FACS)
            return FACS
            ##print "TURI KUHARENGA"
        else: pass
        return MchSecurity.get_auth_facilities(self.user)
    except Exception, e:
        #print "NO FACILITIES ASSIGNED TO USER : %s" % self.user.usern
        pass
    return []

class MchNavigation:
  def __init__(self, auth, *args, **kw):
    self.args   = args
    self.kw     = kw
    self.auth   = auth
    td          = datetime.today()
    self.sta    = datetime(year = td.year, month = td.month, day = td.day, 
                            hour = 0, minute = 0, second = 0, microsecond = 0)
    self.fin    = datetime(year = td.year, month = td.month, day = td.day, 
                            hour = td.hour, minute = td.minute, second = td.second, microsecond = td.microsecond)
    self.gap    = timedelta(days = 1000 - 1)
    self.privileges  =  MchSecurity.get_privileges()
    self.auth_pages  = {}

  def locs(self):
    locs = {}
    try:
        self.user = self.auth.get_user()
        self.auth.user = self.user
        self.auth_pages = self.auth.auth_pages(self.user)
        ## Villages need to be loaded from cell not from start.
        ## else where use navigation fx
        self.villages = []#self.auth.auth_villages()
        self.facilities = self.auth.auth_facilities()
        locs.update({'urls': self.auth_pages})
        locs.update({'villages': self.villages})
        locs.update({'cells': UNDERSCORE(self.villages).chain().indexBy(lambda x, *args: x.cell_pk).map(lambda x, *args: x).sortBy().value()})
        locs.update({'sectors': UNDERSCORE(self.villages).chain().indexBy(lambda x, *args: x.sector_pk).map(lambda x, *args: x).sortBy().value()})
        locs.update({'facilities' :  self.facilities})
        locs.update({'nations' :  UNDERSCORE(self.facilities).chain().indexBy(lambda x, *args: x.nation_pk).map(lambda x, *args: x).sortBy().value()})
        locs.update({'provinces' : UNDERSCORE(self.facilities).chain().indexBy(lambda x, *args: x.province_pk).map(lambda x, *args: x).sortBy().value()})
        locs.update({'districts' : UNDERSCORE(self.facilities).chain().indexBy(lambda x, *args: x.district_pk).map(lambda x, *args: x).sortBy().value()})
        locs.update({'hospitals' :  
                        UNDERSCORE(self.facilities).chain().filter(lambda x, *args:x.location_level_code == 'HD'
                                              ).indexBy(lambda x, *args: x.indexcol).map(lambda x, *args: x).sortBy().value()})
        locs.update({'hcs': UNDERSCORE(self.facilities).chain().filter(lambda x, *args:x.location_level_code == 'HC'
                                              ).indexBy(lambda x, *args: x.indexcol).map(lambda x, *args: x).sortBy().value()})
        #print "KEYS: %s" % locs.keys()
    except Exception, e:
        pass
    return locs  

  def pages(self, qry, limit = 20):
    tot, etc  = divmod(qry.count(), limit)
    if etc:
      tot = tot + 1
    cpg = int(self.kw.get('page', '0'))
    crg = cpg * limit
    pgs = xrange(tot)
    return (cpg, (crg, crg + limit), pgs)

  def __unicode__(self):
    them  = self.listing
    them.reverse() 
    ##print "NAVIGATION: ", [unicode(x) for x in them], "CONDITIONS: ", self.conditions()
    return ', '.join([unicode(x) for x in them])

  @property
  def listing(self):
    dem = [MchLocation(self.nation(), 'nation', self, ['province', 'district', 'hd', 'hc', 'page'], '')]
    pcs = {
      'province':{
        'area'  : lambda _: self.province(prv=_),
        'miss'  :['district', 'hd', 'hc'],
        'title' : 'Province',
        'trx'   : lambda x: first_cap(re.sub(u' PROVINCE', '', x).lower())
      },
      'district':{
        'area'  : lambda _: self.district(dst=_),
        'miss'  : ['hd', 'hc'],
        'title' : 'District'
      },
      'hd':{
        'area'  : lambda _: self.hd(hd=_),
        'miss'  : ['hc'],
        'title' : 'Hospital'
      },
      'hc':{
        'area'  : lambda _: self.hc(hc=_),
        'miss'  : [],
        'title' : 'Health Centre'
      }
    }

    for pc in [(self.kw.get('province'), 'province'),
               (self.kw.get('district'), 'district'),
               (self.kw.get('hd'), 'hd'),
               (self.kw.get('hc'), 'hc')]:
      if pc[0]: 
        it  = pcs[pc[1]]#;#print "HERE: ", pc[0], pc[1], it['area'](pc[0])
        dem.append(MchLocation(it['area'](pc[0]), pc[1], self, it['miss'], it['title'], it['trx'] if 'trx' in it else None))
    
    return dem

  def defaul_location(self):
    gat = fetch_location('NATION', 1)
    return gat 

  def nation(self):
    gat = fetch_location('NATION', 1)
    return gat

  def province(self, prv = None):
    gat = fetch_location('PRV', prv)
    return gat

  def district(self, dst = None):
    gat = fetch_location('DST', dst)
    return gat

  def sector(self, sec = None):
    gat = fetch_location('SEC', sec)
    return gat

  def cell(self, cell = None):
    gat = fetch_location('CEL', cell)
    return gat

  def village(self, vill = None):
    gat = fetch_location('VIL', vill)
    return gat

  def hd(self, hd = None):
    gat = fetch_location('HD', hd)
    return gat

  def hc(self, hc = None):
    gat = fetch_location('HC', hc)
    return gat

  @property
  def start(self):
    gat = self.kw.get('start', '')
    if not gat:
      return self.sta
    return self.make_time(gat)

  @property
  def finish_date(self):
    return self.text_date(self.finish)

  @property
  def start_date(self):
    return self.text_date(self.start)

  def text_date(self, dt):
    return dt.strftime('%d/%m/%Y')

  @property
  def finish(self):
    st = self.kw.get('start', '')
    gat = self.kw.get('finish', '')
    if not gat or gat == st:
      return self.fin
    return self.make_time(gat)

  def make_time(self, txt):
    '''dd/mm/yyyy'''
    pcs = [int(x) for x in re.split(r'\D', txt)]
    if len(pcs) == 5: return datetime(year = pcs[2], month = pcs[1], day = pcs[0], hour=pcs[3], minute= pcs[4])
    return datetime(year = pcs[2], month = pcs[1], day = pcs[0])

  def conditions(self, tn = None, ini = None, cols = []):
    ans = ini.conditions() if ini else {}
    if tn and tn in cols:
      ans.update({
        (tn + ' >= %s')  : self.start,
        (tn + ' <= %s')  : self.finish
      })
    if self.auth.user:
        lvl = MchSecurity.get_auth_location(self.auth.user, self.kw)
        if lvl.get('sector_pk'): ans.update({'sector_pk = %s': lvl.get('sector_pk')})
        if lvl.get('cell_pk'): ans.update({'cell_pk = %s': lvl.get('cell_pk')})
        if lvl.get('village_pk'): ans.update({'village_pk = %s': lvl.get('village_pk')})
        if lvl.get('facility_pk'): ans.update({'facility_pk = %s': lvl.get('facility_pk')})
        if lvl.get('referral_facility_pk'): ans.update({'referral_facility_pk = %s': lvl.get('referral_facility_pk')})
        if lvl.get('district_pk'): ans.update({'district_pk = %s': lvl.get('district_pk')})
        if lvl.get('province_pk'): ans.update({'province_pk = %s': lvl.get('province_pk')})
    else:
        pass    
    return ans

  def pre_link(self, url):
    pcs = urlparse.urlsplit(url)
    qrs = urlparse.parse_qs(pcs[3])
    qrs.update(self.kw)
    return (pcs, qrs)

  def link(self, url, **kw):
    if not self.kw and not kw:
      return url
    pcs, qrs  = self.pre_link(url)
    miss      = kw.pop('minus', [])
    qrs.update(kw)
    return urlparse.urlunsplit((pcs[0], pcs[1], pcs[2], '&'.join(['%s=%s' % (k, urllib2.quote(str(qrs[k]))) for k in qrs if qrs[k] and (not k in miss)]), pcs[4]))


  def find_descr(self, desc, key):
    for k, d in desc:
      if k == key: return d
    return ''

  def edd(self, x):
    ##print "EDD: ", x
    return (x+timedelta(days=GESTATION)).date()

  def locname(self, name, y):
    try:
        ##print y, name
        return y[name]
    except: pass
    return ''

  def neater_tables(self, cnds = {} , sorter = 'created_at', basics = [], extras = []):
    return self.tables_in_general(cnds, sorter, basics, extras)

  def tables_in_general(self, cnds = {} , sorter = 'created_at', basics = [
      ('indexcol',          'Report ID'),
      ('created_at',       'Date'),
      ('user_phone',    'Reporter'),
      ('user_pk',       'Reporter ID')
        ], extras = []):

    markup  = {
      #'national_id': lambda x, _, __: '<a href="/tables/patient?pid=%s">%s</a>' % (x, x),
      'village_pk': lambda x, y, __: '%s' % (self.locname('village_name', y), ),
      'cell_pk': lambda x, y, __: '%s' % (self.locname('cell_name', y), ),
      'sector_pk': lambda x, y, __: '%s' % (self.locname('sector_name', y), ),
      'facility_pk': lambda x, y, __: '%s' % (self.locname('facility_name', y), ),
      'referral_facility_pk': lambda x, y, __: '%s' % (self.locname('referral_name', y), ),
      'district_pk': lambda x, y, __: '%s' % (self.locname('district_name', y), ),
      'province_pk': lambda x, y, __: '%s' % (self.locname('province_name', y), ),
      'gravidity': lambda x, _, __: '%s' % (int(x) if x else 0),
      'parity': lambda x, _, __: '%s' % (int(x) if x else 0),
      'lmp': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'recent_lmp': lambda x, _, __: '%s' % (datetime.date(x) if x else ''),
      'edd': lambda x, _, __: '%s' % (self.edd(x) if x else ''),
      'created_at': lambda x, _, __: '%s %s:%s:%s' % ((datetime.date(x), x.hour, x.minute, x.second)  if x else ('','','','')),
      
    }

    kw = self.kw
    pid     = kw.get('pid')
    tid     = kw.get( 'id')
    if pid:
      cnds.update({'national_id = %s': pid})
    elif tid:
      cnds.update({'indexcol  = %s':  tid})
    else:
      cnds.update(self.conditions(tn = sorter))
    cols  = (extras + basics
                # TODO verify log table
                #+ (([] if 'province' in kw else [('province_pk',       'Province')]) +
                # ([] if 'district' in kw else [('district_pk',       'District')]) +
                # ([] if 'hd' in kw else [('referral_facility_pk',  'Hospital') ]) +
                # ([] if 'hc' in kw else [('facility_pk',  'Health Centre'), ]))
            )
    return (cnds, markup, cols)

class RSMSRWController():
    
    def __init__(self, auth):
        self.auth    = auth        

    def navigate(self, auth, *args, **kw):
        navb    = MchNavigation(auth, *args, **kw)
        locs    = navb.locs()
        return [navb, locs]


