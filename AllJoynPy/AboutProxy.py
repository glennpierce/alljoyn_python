import sys, types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject

# Wrapper for file AboutProxy.h

# Typedefs
# struct _alljoyn_aboutproxy_handle * alljoyn_aboutproxy

class AboutProxy(AllJoynObject):
    
    __metaclass__ = AllJoynMeta
    
    _cmethods = {u'Create': (u'alljoyn_aboutproxy_create',
                 (u'alljoyn_aboutproxy', C.c_void_p),
                 ((u'int', C.c_int),
                  (u'const char *', C.c_char_p),
                  (u'int', C.c_int))),
                  u'Destroy': (u'alljoyn_aboutproxy_destroy',
                    (u'void', None),
                    ((u'alljoyn_aboutproxy', C.c_void_p),)),
                  u'GetAboutData': (u'alljoyn_aboutproxy_getaboutdata',
                   (u'QStatus', C.c_uint),
                   ((u'alljoyn_aboutproxy', C.c_void_p),
                    (u'const char *', C.c_char_p),
                    (u'int', C.c_int))),
                  u'GetObjectDescription': (u'alljoyn_aboutproxy_getobjectdescription',
                   (u'QStatus', C.c_uint),
                   ((u'alljoyn_aboutproxy', C.c_void_p),
                    (u'int', C.c_int))),
                  u'GetVersion': (u'alljoyn_aboutproxy_getversion',
                   (u'QStatus', C.c_uint),
                   ((u'alljoyn_aboutproxy', C.c_void_p),
                    (u'int *', 'POINTER(C.c_int)')))}
    
    def __init__(self):
        pass
        
    def __del__(self):
        #self.AboutProxyDestroy(self.handle)
        pass

    # Wrapper Methods

    def Create(self, busName,sessionId):
        return self._Create(self.handle,busName,sessionId) # const char *,int

    def Destroy(self):
        return self._Destroy(self.handle)

    def GetObjectDescription(self, objectDesc):
        return self._GetObjectDescription(self.handle,objectDesc) # int

    def GetAboutData(self, language,data):
        return self._GetAboutData(self.handle,language,data) # const char *,int

    def GetVersion(self, version):
        return self._GetVersion(self.handle,version) # int *

    

AboutProxy.bind_functions_to_cls()