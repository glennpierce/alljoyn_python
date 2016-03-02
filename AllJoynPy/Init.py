import sys, types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject
# Wrapper for file Init.h

class AllJoynInit(AllJoynObject):
    
    __metaclass__ = AllJoynMeta
    
    _cmethods = {u'Init': (u'alljoyn_init', (u'QStatus', C.c_uint), ()),
                 u'Shutdown': (u'alljoyn_shutdown', (u'QStatus', C.c_uint), ())}
    
    def __init__(self):
        #self.bind_functions()
        pass
        
    def __del__(self):
        #self.AllJoynDestroy(self.handle)
        pass


AllJoynInit.bind_functions_to_cls()

sys.modules[__name__] = AllJoynInit()  # See https://mail.python.org/pipermail/python-ideas/2012-May/014969.html
