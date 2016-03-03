import ctypes as C
from ctypes import POINTER
from . import AllJoynMeta, AllJoynObject, MsgArg

# Wrapper for file AboutProxy.h

# Typedefs
# struct _alljoyn_aboutproxy_handle * alljoyn_aboutproxy


class AboutProxy(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'Create': (u'alljoyn_aboutproxy_create',
                             (u'alljoyn_aboutproxy', C.c_void_p),
                             ((u'void*', C.c_void_p),
                                 (u'const char *', C.c_char_p),
                                 (u'uint', C.c_uint))),
                 
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
                                               (u'void*', POINTER(POINTER(MsgArg.AlljoynMsgArg))))),

                 u'GetVersion': (u'alljoyn_aboutproxy_getversion',
                                 (u'QStatus', C.c_uint),
                                 ((u'alljoyn_aboutproxy', C.c_void_p),
                                     (u'int *', POINTER(C.c_int))))}

    def __init__(self, bus, busName, sessionId):
        super(AboutProxy, self).__init__()
        self.handle = self._Create(bus.handle, busName, sessionId)

    def __del__(self):
        self._Destroy(self.handle)

    # Wrapper Methods
    def GetObjectDescription(self):
        handle = MsgArg.MsgArg._Create()
        self._GetObjectDescription(self.handle, C.byref(handle))  # int
        return MsgArg.MsgArg(handle=handle)

    def GetAboutData(self, language, data):
        return self._GetAboutData(self.handle, language, data)  # const char *,int

    def GetVersion(self, version):
        return self._GetVersion(self.handle, version)  # int *


AboutProxy.bind_functions_to_cls()