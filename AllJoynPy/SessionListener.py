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

import sys
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import *

# Wrapper for file SessionListener.h

@unique
class SessionLostReason(Enum):
    ALLJOYN_SESSIONLOST_INVALID = 0
    ALLJOYN_SESSIONLOST_REMOTE_END_LEFT_SESSION = 1
    ALLJOYN_SESSIONLOST_REMOTE_END_CLOSED_ABRUPTLY = 2
    ALLJOYN_SESSIONLOST_REMOVED_BY_BINDER = 3
    ALLJOYN_SESSIONLOST_LINK_TIMEOUT = 4
    ALLJOYN_SESSIONLOST_REASON_OTHER = 5


if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE


# typedef void (AJ_CALL * alljoyn_sessionlistener_sessionlost_ptr)(const
# void* context, alljoyn_sessionid sessionId, alljoyn_sessionlostreason
# reason);
SessionListenerSessionLostFuncType = CallbackType(None, C.c_void_p, C.c_uint, C.c_uint)  # context sessionId reason

# typedef void (AJ_CALL *
# alljoyn_sessionlistener_sessionmemberadded_ptr)(const void* context,
# alljoyn_sessionid sessionId, const char* uniqueName);
SessionListenerSessionMemberAddedFuncType = CallbackType(
    None, C.c_void_p, C.c_uint, C.c_char_p)  # context sessionId uniqueName

# typedef void (AJ_CALL *
# alljoyn_sessionlistener_sessionmemberremoved_ptr)(const void* context,
# alljoyn_sessionid sessionId, const char* uniqueName);
SessionListenerSessionMemberRemovedFuncType = CallbackType(
    None, C.c_void_p, C.c_uint, C.c_char_p)  # context sessionId uniqueName


class SessionListenerCallBacks(C.Structure):
    _fields_ = [
        ("SessionLost", SessionListenerSessionLostFuncType),
        ("SessionMemberAdded", SessionListenerSessionMemberAddedFuncType),
        ("SessionMemberRemoved", SessionListenerSessionMemberRemovedFuncType)
    ]


class SessionListener(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'Create': (u'alljoyn_sessionlistener_create', (u'alljoyn_sessionlistener', SessionListenerHandle),
                             ((u'const alljoyn_sessionlistener_callbacks *', POINTER(SessionListenerCallBacks)),
                              (u'const void *', C.c_void_p))),

                 u'Destroy': (u'alljoyn_sessionlistener_destroy', (u'void', None), 
                            ((u'alljoyn_sessionlistener', SessionListenerHandle),))}

    def __init__(self, context=None):

        super(SessionListener, self).__init__()

        self.callback_structure = SessionListenerCallBacks()

        self.callback_structure.SessionLost = self._OnSessionLostCallBack()
        self.callback_structure.SessionMemberAdded = self._OnSessionMemberAddedCallback()    
        self.callback_structure.SessionMemberRemoved = self._OnSessionMemberRemovedCallBack()

        self.handle = self._Create(C.byref(self.callback_structure), None)

    def __del__(self):
        if self.handle:
            return self._Destroy(self.handle)

    def _OnSessionLostCallBack(self):
        def func(context, sessionId, reason):
          self.OnSessionLostCallBack(context, sessionId, SessionLostReason(reason))
        return SessionListenerSessionLostFuncType(func)

    def _OnSessionMemberAddedCallback(self):
        def func(context, sessionId, uniqueName):
          self.OnSessionMemberAddedCallback(context, sessionId, uniqueName)
        return SessionListenerSessionMemberAddedFuncType(func)

    def _OnSessionMemberRemovedCallBack(self):
        def func(context, sessionId, uniqueName):
          self.OnSessionMemberRemovedCallBack(ccontext, sessionId, uniqueName)
        return SessionListenerSessionMemberRemovedFuncType(func)

    def OnSessionLostCallBack(self, context, sessionId, reason):
        pass

    def OnSessionMemberAddedCallback(self, context, sessionId, uniqueName):
        pass

    def OnSessionMemberRemovedCallBack(self, context, sessionId, uniqueName):
        pass

SessionListener.bind_functions_to_cls()
