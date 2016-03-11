import sys
import types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject, MsgArg
# Wrapper for file AboutListener.h

# Typedefs
# struct _alljoyn_aboutlistener_handle * alljoyn_aboutlistener
# void (*)(const void *, const char *, int, int, const int, const int) alljoyn_about_announced_ptr
# struct alljoyn_aboutlistener_callback alljoyn_aboutlistener_callback

class AboutListenerHandle(C.c_void_p): 
    pass
    
if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE

# context busName version port objectDescriptionArg aboutDataArg
AboutAnnouncedFuncType = CallbackType(None, C.c_void_p, C.c_char_p, C.c_int, C.c_int, MsgArg.MsgArgHandle, MsgArg.MsgArgHandle)


class AboutListenerCallBack(C.Structure):
    _fields_ = [
        ("AboutListenerAnnounced", AboutAnnouncedFuncType)
    ]


class AboutListener(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'Create': (u'alljoyn_aboutlistener_create', (u'alljoyn_aboutlistener', AboutListenerHandle),
                             ((u'const alljoyn_aboutlistener_callback *', POINTER(AboutListenerCallBack)),
                              (u'const void *', C.c_void_p))),
                 u'Destroy': (u'alljoyn_aboutlistener_destroy', (u'void', None), 
                            ((u'alljoyn_aboutlistener', AboutListenerHandle),))}

    def __init__(self, callback_data=None):
        super(AboutListener, self).__init__()

        self.callback_structure = AboutListenerCallBack()

        self.callback_data = callback_data

        self.callback_structure.AboutListenerAnnounced = AboutAnnouncedFuncType(AboutListener._OnAboutListenerCallBack)

        # We pass the id of self tothe callback here as the context so we can get self in the callback.
        # Usuall ctypes would handle the self magic but in this case the ptr is stuck into a structure
        # and ctypes does not then do the magic
        # print ctypes.cast(ctypes.c_longlong(id(a)).value, ctypes.py_object).value
        #self.handle = self._Create(C.byref(callback_structure), C.c_void_p(id(self)))
        #self.unique = C.c_int(self.unique_id)
        self.handle = self._Create(C.byref(self.callback_structure), self.unique_id)

    def __del__(self):
        self._Destroy(self.handle)

    @staticmethod
    def _OnAboutListenerCallBack(context, busName, version, port, objectDescriptionArg, aboutDataArg):
        self = AllJoynObject.unique_instances[context]
        self.OnAboutListenerCallBack(self.callback_data, busName, version, port, MsgArg.MsgArg.FromHandle(objectDescriptionArg), \
                                     MsgArg.MsgArg.FromHandle(aboutDataArg))

    def OnAboutListenerCallBack(self, context, busName, version, port, objectDescriptionArg, aboutDataArg):
        pass


AboutListener.bind_functions_to_cls()
