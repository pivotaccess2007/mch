#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4

##
##
## @author UWANTWALI ZIGAMA Didier
## d.zigama@pivotaccess.com/zigdidier@gmail.com
##

__author__="Zigama Didier"
__date__ ="$Nov 22, 2017 1:29:30 PM$"

from util.record import *

def update_record(query):
    return orm.ORM.zdquery(query)

def get_mothers():
    mothers = filter_data('mother', sort = ('indexcol', False))
    return mothers

def get_children():
    children = filter_data('birth', sort = ('birth_date', False))
    return children

def get_previous_and_recent_pregnancy(mother):
    prev, rec = None, None
    pregs   = filter_data('pregnancy', {'mother_pk = %s': mother.indexcol }, sort = ('lmp', False))
    if pregs:
        rec      = pregs[0]
        prev     = pregs[1:len(pregs)][0] if pregs[1:len(pregs)] else None
    return (prev, rec)

def get_previous_and_recent_cbn(child):
    prev, rec = None, None
    cbns   = filter_data('nutrition', {'mother_pk = %s': mother.indexcol }, sort = ('lmp', False))
    if cbns:
        rec      = cbns[0]
        prev     = cbns[1:len(cbns)][0] if cbns[1:len(cbns)] else None
    if not rec: rec = child
    return (prev, rec)

def build_mother(mother):
    prev, rec = get_previous_and_recent_pregnancy(mother)
    qry  = """ """
    if prev and rec:
        #q_rec_lmp = "UPDATE mother SET recent_lmp = '%s' WHERE indexcol = %s " % (rec.lmp, mother.indexcol)
        #q_rec_mw = "UPDATE mother SET recent_mother_weight =  %s WHERE indexcol = %s" % (rec.mother_weight, mother.indexcol)        
        #q_rec_mh = "UPDATE mother SET recent_mother_height =  %s WHERE indexcol = %s" % (rec.mother_height, mother.indexcol)
        #q_rec_bmi = "UPDATE mother SET recent_bmi =  %s WHERE indexcol = %s" % (rec.bmi, mother.indexcol)
        #q_rec_muac = "UPDATE mother SET recent_muac =  %s WHERE indexcol = %s" % (rec.muac, mother.indexcol)

        qry = """
                UPDATE mother SET recent_lmp = '%(recent_lmp)s',
                                    recent_mother_weight =  %(recent_mother_weight)s,
                                    recent_mother_height =  %(recent_mother_height)s,
                                    recent_bmi =  %(recent_bmi)s,
                                    recent_muac =  %(recent_muac)s,
                                    previous_lmp = '%(previous_lmp)s',
                                    previous_mother_weight =  %(previous_mother_weight)s,
                                    previous_mother_height =  %(previous_mother_height)s,
                                    previous_bmi =  %(previous_bmi)s,
                                    previous_muac =  %(previous_muac)s  WHERE indexcol = %(indexcol)s """ % { 
                 'indexcol': mother.indexcol,
                 'recent_lmp': rec.lmp,
                 'recent_mother_weight': rec.mother_weight,
                 'recent_mother_height': rec.mother_height,
                 'recent_bmi': rec.bmi,
                 'recent_muac': rec.muac,
                 'previous_lmp': prev.lmp,
                 'previous_mother_weight': prev.mother_weight,
                 'previous_mother_height': prev.mother_height,
                 'previous_bmi': prev.bmi,
                 'previous_muac': prev.muac
                 }
        #print q_rec_lmp, q_rec_mw, q_rec_mh, q_rec_bmi, q_rec_muac
        #update_record(q_rec_lmp)
        #update_record(q_rec_mw)
        #update_record(q_rec_mh)
        #update_record(q_rec_bmi)
        #update_record(q_rec_muac)    
    else:
        #q_prev_lmp = "UPDATE mother SET previous_lmp = '%s' WHERE indexcol = %s " % (prev.lmp, mother.indexcol)
        #q_prev_mw = "UPDATE mother SET previous_mother_weight = %s WHERE indexcol = %s" % (prev.mother_weight, mother.indexcol)
        #q_prev_mh = "UPDATE mother SET previous_mother_height =  %s WHERE indexcol = %s" % (prev.mother_height, mother.indexcol)
        #q_prev_bmi = "UPDATE mother SET previous_bmi =  %s WHERE indexcol = %s" % (prev.bmi, mother.indexcol)
        #q_prev_muac = "UPDATE mother SET previous_muac =  %s WHERE indexcol = %s" % (prev.muac, mother.indexcol)
        #print q_prev_lmp, q_prev_mw, q_prev_mh, q_prev_bmi, q_prev_muac
        #update_record(q_prev_lmp)
        #update_record(q_prev_mw)
        #update_record(q_prev_mh)
        #update_record(q_prev_bmi)
        #update_record(q_prev_muac)

        qry = """
                UPDATE mother SET recent_lmp = '%(recent_lmp)s',
                                    recent_mother_weight =  %(recent_mother_weight)s,
                                    recent_mother_height =  %(recent_mother_height)s,
                                    recent_bmi =  %(recent_bmi)s,
                                    recent_muac =  %(recent_muac)s,
                                    previous_lmp = '%(previous_lmp)s',
                                    previous_mother_weight =  %(previous_mother_weight)s,
                                    previous_mother_height =  %(previous_mother_height)s,
                                    previous_bmi =  %(previous_bmi)s,
                                    previous_muac =  %(previous_muac)s  WHERE indexcol = %(indexcol)s """ % { 
                 'indexcol': mother.indexcol,
                 'recent_lmp': rec.lmp,
                 'recent_mother_weight': rec.mother_weight,
                 'recent_mother_height': rec.mother_height,
                 'recent_bmi': rec.bmi,
                 'recent_muac': rec.muac,
                 'previous_lmp': None,
                 'previous_mother_weight': None,
                 'previous_mother_height': None,
                 'previous_bmi': None,
                 'previous_muac': None
                 }

     
    update_record(qry)
    return True

def build_mothers():
    mothers = get_mothers()

    for mother in mothers:
        try:
            build_mother(mother)    
        except Exception, e:
            print e#, mother.__dict__
            continue

    return True


def build_child(child):
    prev, rec = get_previous_and_recent_cbn(child)
    qry  = """ """
    if prev and rec:
        qry = """
                UPDATE birth SET recent_breastfeeding = '%(recent_breastfeeding)s',
                                    recent_child_weight =  %(recent_child_weight)s,
                                    recent_child_height =  %(recent_child_height)s,
                                    recent_bmi =  %(recent_bmi)s,
                                    recent_muac =  %(recent_muac)s,
                                    previous_child_weight =  %(previous_child_weight)s,
                                    previous_child_height =  %(previous_child_height)s,
                                    previous_bmi =  %(previous_bmi)s,
                                    previous_muac =  %(previous_muac)s  WHERE indexcol = %(indexcol)s """ % { 
                 'indexcol': child.indexcol,
                 'recent_breastfeeding': rec.breastfeeding,
                 'recent_child_weight': rec.child_weight,
                 'recent_child_height': rec.child_height,
                 'recent_bmi': rec.bmi,
                 'recent_muac': rec.muac,
                 'previous_child_weight': prev.child_weight,
                 'previous_child_height': prev.child_height,
                 'previous_bmi': prev.bmi,
                 'previous_muac': prev.muac
                 }
            
    else:
        qry = """
                UPDATE birth SET recent_breastfeeding = '%(recent_breastfeeding)s',
                                    recent_child_weight =  %(recent_child_weight)s,
                                    recent_child_height =  %(recent_child_height)s,
                                    recent_bmi =  %(recent_bmi)s,
                                    recent_muac =  %(recent_muac)s,
                                    previous_child_weight =  %(previous_child_weight)s,
                                    previous_child_height =  %(previous_child_height)s,
                                    previous_bmi =  %(previous_bmi)s,
                                    previous_muac =  %(previous_muac)s  WHERE indexcol = %(indexcol)s """ % { 
                 'indexcol': child.indexcol,
                 'recent_breastfeeding': rec.breastfeeding,
                 'recent_child_weight': rec.child_weight,
                 'recent_child_height': rec.child_height,
                 'recent_bmi': rec.bmi,
                 'recent_muac': rec.muac,
                 'previous_child_weight': None,
                 'previous_child_height': None,
                 'previous_bmi': None,
                 'previous_muac': None
                 }

     
    update_record(qry)
    return True


def build_children():
    children = get_children()

    for child in children:
        try:
            build_child(child)    
        except Exception, e:
            print e#, child.__dict__
            continue

    return True
        
        
