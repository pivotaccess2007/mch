#!/usr/bin/env python
# encoding: utf-8
# vim: ts=2 expandtab

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

import re, sys, os
from optparse import OptionParser
from util.migrations import *


def handle(args, options):
  
  parser = OptionParser()
  parser.add_option("-T", "--TYPE", dest="type",
                  help="Specify report type to migrate")
  # TODO
  #parser.add_option("-D", "--ID", dest="report_id",
  #                help="Specify report ID to migrate")
  (options, args) = parser.parse_args()
  options = options.__dict__
  def gun():
    once  = True
    while once:
      once  = single_handle(args, options) and options.get('REPEAT', not once)

  if options.get('BACKGROUND'):
    chp = os.fork()
    if chp:
      print 'Background:', chp
      return
    gun()
  else:
    gun()

def single_handle(args, options): 
  if options.get('type') == 'NATION':  migrate_nations()
  if options.get('type') == 'PRV':  migrate_provinces()
  if options.get('type') == 'DST':  migrate_districts()
  if options.get('type') == 'SEC':  migrate_sectors()
  if options.get('type') == 'CEL':  migrate_cells()
  if options.get('type') == 'VIL':  migrate_villages()
  if options.get('type') == 'HP':  migrate_hospitals()
  if options.get('type') == 'HC':  migrate_healthcentres()
  if options.get('type') == 'SIM':  migrate_simcards()
  if options.get('type') == 'CHW':  migrate_reporters()
  if options.get('type') == 'PRE':  migrate_pregnancies()
  if options.get('type') == 'BIR':  migrate_births()
  if options.get('type') == 'REF':  migrate_refusals()
  if options.get('type') == 'DEP':  migrate_departures() 
  if options.get('type') == 'ANC':  migrate_ancvisits()
  if options.get('type') == 'RISK':  migrate_risks()
  if options.get('type') == 'RED':  migrate_redalerts()
  if options.get('type') == 'RES':  migrate_riskresults()
  if options.get('type') == 'RAR':  migrate_redresults() 
  if options.get('type') == 'DTH':  migrate_deaths()
  if options.get('type') == 'NBC':  migrate_nbcvisits()
  if options.get('type') == 'PNC':  migrate_pncvisits()
  if options.get('type') == 'CCM':  migrate_ccms()
  if options.get('type') == 'CMR':  migrate_cmrs() 
  if options.get('type') == 'CBN':  migrate_cbns()
  if options.get('type') == 'CHI':  migrate_chis()  
  return True


def migrator_main(args):
  handle(args, os.environ)
  return 0

sys.exit(migrator_main(sys.argv))

