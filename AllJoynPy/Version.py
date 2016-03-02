import sys, types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject


# Wrapper for file version.h
class AllJoyn(AllJoynObject):
    
    __metaclass__ = AllJoynMeta
    
    _cmethods = {u'GetBuildInfo': (u'alljoyn_getbuildinfo', (u'const char *', C.c_char_p), ()),
                 u'GetNumericVersion': (u'alljoyn_getnumericversion', (u'int', C.c_int), ()),
                 u'GetVersion': (u'alljoyn_getversion', (u'const char *', C.c_char_p), ())}

    def __del__(self):
        #self.AllJoynDestroy(self.handle)
        pass



AllJoyn.bind_functions_to_cls()

sys.modules[__name__] = AllJoyn()  # See https://mail.python.org/pipermail/python-ideas/2012-May/014969.html
