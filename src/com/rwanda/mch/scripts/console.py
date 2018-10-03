#!/usr/bin/env python
# encoding: utf-8
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

import os, sys
import code
import readline
import rlcompleter


objects = {}
readline.set_completer(rlcompleter.Completer(objects).complete)
readline.parse_and_bind("tab:complete")


def mch_main(argv):
  pcks  = os.path.join(os.getcwd(), 'src/com/rwanda/mch')
  env   = os.environ
  env.update({'PYTHONPATH': pcks})
  argl  = argv
  argl.append(env)
  code.interact(local=objects)
  return os.execlpe('python', *argl)

if __name__ == '__main__':
  bottom  = sys.exit(mch_main(sys.argv))

