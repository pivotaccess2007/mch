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

##
##
## make sure need to remember details
## just run the following
## ./rw.py webservice frontend/{html,static} /static
##
##


try:
  activate_this = '/livemas/mch/rwanda/bin/activate_this.py'
  execfile(activate_this, dict(__file__=activate_this))
  print "SUCCESS 1 ACTIVATING PROD ENV"
except Exception, e1:
  print "ERROR 1 ACTIVATING PROD ENV: ", e1
  try:
      activate_this = '/home/rapidsmsrw/mch/rwanda/bin/activate_this.py'
      execfile(activate_this, dict(__file__=activate_this))
      print "SUCCESS 2 ACTIVATING TEST ENV"
  except Exception, e2:
    print "ERROR 2 ACTIVATING TEST ENV: ", e2
    try:      
      activate_this = '/home/aidspan/projects/python/livemas/mch/rwanda/bin/activate_this.py'
      execfile(activate_this, dict(__file__=activate_this))
      print "SUCCESS 3 ACTIVATING LOCAL ENV"
    except Exception, e3:
      print "ERROR 3 ACTIVATING LOCAL ENV: ", e3

import os, sys

def mchmain(argv):
  if len(argv) < 2:
    sys.stderr.write('%s operation [args]\n' % (argv[0], ))
    return 1
  elmod = __import__(argv[1])
  yes   = True
  try:
    yes = elmod.mch_init(argv[1:])
  except AttributeError:
    # sys.stderr.write('The MCH component “%s” lacks mch_init\n' % (argv[1], ))
    pass
  if yes:
    try:
      ans = elmod.mch_main(argv[1:])
      try:
        elmod.mch_clean()
      except AttributeError:
        pass
      return ans
    except AttributeError, e:
      sys.stderr.write('The MCH component “%s” lacks mch_main\n' % (argv[1], ))
      raise e
  return 2

if __name__ == '__main__':
  for sp in ['src/com/rwanda/mch/scripts',
             'src/com/rwanda/mch'] + [x for x in os.getenv('MCH_PATHS', '').split(':') if x]:
    sys.path.insert(0, os.path.join(os.getcwd(), sp))
  sys.exit(mchmain(sys.argv))
