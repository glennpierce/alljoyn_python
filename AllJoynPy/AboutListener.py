import sys, types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject
# Wrapper for file AboutListener.h

# Typedefs
# struct _alljoyn_aboutlistener_handle * alljoyn_aboutlistener
# void (*)(const void *, const char *, int, int, const int, const int) alljoyn_about_announced_ptr
# struct alljoyn_aboutlistener_callback alljoyn_aboutlistener_callback

if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE
    
AboutAnnouncedFuncType = CallbackType(None, C.c_void_p, C.c_char_p, C.c_int, C.c_int, C.c_int, C.c_int) # context busName version port objectDescriptionArg aboutDataArg


class AboutListenerCallBack(C.Structure):
    _fields_ = [
                ("AboutListenerAnnounced", POINTER(AboutAnnouncedFuncType))
               ]


class AboutListener(AllJoynObject):
    
    __metaclass__ = AllJoynMeta
    
    _cmethods = {u'Create': (u'alljoyn_aboutlistener_create', (u'alljoyn_aboutlistener', 'C.c_void_p'), 
                            ((u'const alljoyn_aboutlistener_callback *', 'POINTER(AboutListenerCallBack)'),
                            (u'const void *', 'C.c_void_p'))),
                 u'Destroy': (u'alljoyn_aboutlistener_destroy', (u'void', None), ((u'alljoyn_aboutlistener', 'C.c_void_p'),))}
    
    def __init__(self, callback, context):
        self.bind_functions()
        self.handle = self._Create(callback, context)
        
    def __del__(self):
        self._Destroy(self.handle)
   
