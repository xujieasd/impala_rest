##############################################################################
# functions for common util                                                  #
# mainly handle arg type convert or element check                            #
##############################################################################

import parm

def bool_to_string(value):
    if value is True:
        return 'TRUE'
    else:
        return 'FALSE'

def ensure_single_word(str):
    strs = str.split(" ")
    if len(strs) != 1:
        return False
    return True

def type_to_string(t):
    if t == parm.TYPE_ADJUST:
        return "adjust"
    elif t == parm.TYPE_COMMON:
        return "common"
    else:
        return "invalid type"

def unicode_to_int(x):
    try:
        int_x = int(x)
    except Exception, err:
        return x
    else:
        return int_x