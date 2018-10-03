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
from controller.main import RSMSRWController
from model.stock import Stock
from util import queries
from util.mch_util import makecol, makedict

class StockController(RSMSRWController):

    def __init__(self, navb):
        navb.gap= timedelta(days = 0)## USE THIS GAP OF ZERO DAYS TO DEFAULT TO CURRENT SITUATION
        self.navb = navb

    def get_total(self):
        cnds    = self.navb.conditions()
        exts = {}
        cols = ['COUNT(*) AS total'] 
        total = Stock.fetch_stock(cnds, cols, exts)[0]
        return total

    def get_stats(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : '',
                     "(created_at) <= '%s'" % (self.navb.finish) : ''})
        exts    = {}
        attrs   = [(makecol(x[0]), x[1]) for x in queries.STOCK_DATA['attrs']]
        exts.update(dict([(makecol(x[0]), ('COUNT(*)', x[0])) for x in queries.STOCK_DATA['attrs']]))#;print exts
        cols    = ['COUNT(*) AS total']
        nat     = Stock.fetch_stock(cnds, cols, exts)
        #print attrs, "NAT: ", nat[0].__dict__
        return [attrs, nat]

    def get_tables(self):
        cnds    = self.navb.conditions()
        cnds.update({"(created_at) >= '%s'" % (self.navb.start) : '',
                     "(created_at) <= '%s'" % (self.navb.finish) : ''})
        exts = {}
        cnds, markup, cols = self.navb.neater_tables(cnds = cnds, extras = [
                                              ('province_pk', 'Province'),
                                              ('district_pk', 'District'),
                                              ('referral_facility_pk', 'Hospital'),
                                              ('facility_pk', 'Health Centre'),
                                              ('sector_pk', 'Sector'),
                                              ('cell_pk', 'Cell'),
                                              ('village_pk', 'Village'),
                                              ('user_phone',              'Reporter Phone'),                                          
                                              ('created_at', 'Submission Datetime'),
                                              ('indexcol', 'Message')
                                            ])

        markup.update({'drugs': lambda x, _, __: '%s' % (Stock.get_report_drugs(x)) })
        markup.update({'message': lambda x, _, __: '%s' % (Stock.get_report_details(x)) })
        markup.update({'indexcol': lambda x, _, __: '<a href="/dashboards/report?tbl=so&id=%s">View</a>' % (x), })
        
    
        DESCRI = []
        STOCKDICT = makedict(queries.STOCK_DATA['attrs'])
        INDICS = []
        attrs = []
        group = "Stock"
        title = "Stock Notifications"
        sc      = self.navb.kw.get('subcat')
        if self.navb.kw.get('subcat') and self.navb.kw.get('subcat') in [makecol(x[0]) for x in queries.STOCK_DATA['attrs']]:
            cnds.update({queries.STOCK_DATA['query_str']: ''})
            cnds.update({ STOCKDICT[self.navb.kw.get('subcat')][0] : ''})
            INDICS = [STOCKDICT[self.navb.kw.get('subcat')]]

        dcols = [x[0] for x in cols]
        nat = Stock.fetch_log_stock(cnds, dcols)
        #DESCRI.append((group, title))
        desc  = 'Stock-out cases%s' % (' (%s)' % (self.navb.find_descr(DESCRI + [(makecol(x[0]), x[1]) for x in INDICS],
                                                                        sc or self.navb.kw.get('subcat')
                                                                    ) 
					                            )
                                    ) 
        #print title, group, attrs, "NAT: ", nat[0].__dict__
        return (title, desc, group, attrs, markup, cols, nat)
