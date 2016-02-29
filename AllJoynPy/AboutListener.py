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
    
AboutAnnouncedFuncType = CallbackType(None, C.c_void_p, C.c_char_p, C.c_int, C.c_int, C.c_void_p, C.c_void_p) # context busName version port objectDescriptionArg aboutDataArg


class AboutListenerCallBack(C.Structure):
    _fields_ = [
                ("AboutListenerAnnounced", AboutAnnouncedFuncType)
               ]

class AboutListener(AllJoynObject):

    __metaclass__ = AllJoynMeta
    
    _cmethods = {u'Create': (u'alljoyn_aboutlistener_create', (u'alljoyn_aboutlistener', 'C.c_void_p'), 
                            ((u'const alljoyn_aboutlistener_callback *', 'POINTER(AboutListener.AboutListenerCallBack)'),
                            (u'const void *', 'C.c_void_p'))),
                 u'Destroy': (u'alljoyn_aboutlistener_destroy', (u'void', None), ((u'alljoyn_aboutlistener', 'C.c_void_p'),))}
    
    def __init__(self, callback=None):
        self.bind_functions()
        callback_structure = AboutListenerCallBack()
        
        if callback:
            callback_structure.AboutListenerAnnounced = AboutAnnouncedFuncType(callback)
        else:
            callback_structure.AboutListenerAnnounced = AboutAnnouncedFuncType(AboutListener._OnAboutListenerCallBack)
        
        # We pass the id of self tothe callback here as the context so we can get self in the callback.
        # Usuall ctypes would handle the self magic but in this case the ptr is stuck into a structure
        # and ctypes does not then do the magic
        # print ctypes.cast(ctypes.c_longlong(id(a)).value, ctypes.py_object).value
        self.handle = self._Create(C.byref(callback_structure), C.c_void_p(id(self)))
            
    def __del__(self):
        self._Destroy(self.handle)
   
    @staticmethod
    def _OnAboutListenerCallBack(context, busName, version, port, objectDescriptionArg, aboutDataArg):
        self = C.cast(context, C.py_object).value
        self.OnAboutListenerCallBack(context, busName, version, port, objectDescriptionArg, aboutDataArg)
        
    def OnAboutListenerCallBack(self, context, busName, version, port, objectDescriptionArg, aboutDataArg):
        pass
