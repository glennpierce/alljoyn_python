# Copyright Glenn Pierce. All rights reserved.
#
#    Permission to use, copy, modify, and/or distribute this software for any
#    purpose with or without fee is hereby granted, provided that the above
#    copyright notice and this permission notice appear in all copies.
#
#    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#    WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#    MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#    ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#    WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#    ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#    OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


import sys, types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject
# Wrapper for file SessionPortListener.h

# Typedefs
# struct _alljoyn_sessionportlistener_handle * alljoyn_sessionportlistener
# int (int *) QCC_BOOL
# void (*)(const void *, int, int, const char *) alljoyn_sessionportlistener_sessionjoined_ptr
# struct alljoyn_sessionportlistener_callbacks alljoyn_sessionportlistener_callbacks


if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE
    
SessionPortListenerSessionJoinedFuncType = CallbackType(None, C.c_void_p, C.c_int, C.c_int, C.c_char_p) # context sessionPort id joiner

SessionPortListenerAcceptSessionJoinerFuncType = CallbackType(C.c_ubyte, C.c_void_p, C.c_int, C.c_char_p, C.c_void_p) # context sessionPort joiner, opts


class SessionPortListenerCallBacks(C.Structure):
    _fields_ = [
                ("AcceptSessionJoiner", POINTER(SessionPortListenerAcceptSessionJoinerFuncType)),
                ("SessionJoined", POINTER(SessionPortListenerSessionJoinedFuncType)),
    ]



class SessionPortListener(AllJoynObject):
    
    __metaclass__ = AllJoynMeta
    
    _cmethods = {u'Create': (u'alljoyn_sessionportlistener_create',
                     (u'alljoyn_sessionportlistener', C.c_void_p),
                    ((u'const alljoyn_sessionportlistener_callbacks *', POINTER(SessionPortListenerCallBacks)),
                     (u'const void *', C.c_void_p))),
                 
                 u'Destroy': (u'alljoyn_sessionportlistener_destroy', (u'void', None),
                    ((u'alljoyn_sessionportlistener', C.c_void_p),))}
    
    def __init__(self, callback_data=None):

        super(SessionPortListener, self).__init__()

        self.callback_structure = SessionPortListenerCallBacks()

        self.callback_data = callback_data

        self.callback_structure.AcceptSessionJoiner = SessionPortListenerAcceptSessionJoinerFuncType(SessionListener._OnAcceptSessionJoinerCallBack)
        
        self.callback_structure.SessionJoined = SessionPortListenerSessionJoinedFuncType(SessionListener._OnSessionJoinedCallback)
        
        self.handle = self._Create(C.byref(self.callback_structure), self.unique_id)

    def __del__(self):
        if self.handle:
            return self._Destroy(self.handle)
        
    @staticmethod
    def _OnAcceptSessionJoinerCallBack(context, session_port, joiner, opts):
        self = AllJoynObject.unique_instances[context]
        self.OnAcceptSessionJoinerCallBack(self.callback_data, sessionId, reason)

    @staticmethod
    def _OnSessionJoinedCallback(context, session_port, session_id, joiner):
        self = AllJoynObject.unique_instances[context]
        self.OnSessionJoinedCallback(self.callback_data, sessionId, uniqueName)

    def _OnAcceptSessionJoinerCallBack(self, context, sessionId, reason):
        pass

    def _OnSessionJoinedCallback(self, context, sessionId, uniqueName):
        pass

    
SessionPortListener.bind_functions_to_cls()
