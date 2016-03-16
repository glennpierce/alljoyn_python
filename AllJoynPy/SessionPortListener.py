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
import types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import *
# Wrapper for file SessionPortListener.h

if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE


SessionPortListenerAcceptSessionJoinerFuncType = CallbackType(
    C.c_int, C.c_void_p, C.c_ushort, C.c_char_p, C.c_void_p)  # context sessionPort joiner, opts

SessionPortListenerSessionJoinedFuncType = CallbackType(
    None, C.c_void_p, C.c_ushort, C.c_uint, C.c_char_p)  # context sessionPort id joiner

class SessionPortListenerCallBacks(C.Structure):
    _fields_ = [
        ("AcceptSessionJoiner", SessionPortListenerAcceptSessionJoinerFuncType),
        ("SessionJoined", SessionPortListenerSessionJoinedFuncType),
    ]


class SessionPortListener(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'Create': (u'alljoyn_sessionportlistener_create',
                             (u'alljoyn_sessionportlistener', SessionPortListenerHandle),
                             ((u'const alljoyn_sessionportlistener_callbacks *', POINTER(SessionPortListenerCallBacks)),
                                 (u'const void *', C.c_void_p))),

                 u'Destroy': (u'alljoyn_sessionportlistener_destroy', (u'void', None),
                              ((u'alljoyn_sessionportlistener', SessionPortListenerHandle),))}

    def __init__(self, context=None):

        super(SessionPortListener, self).__init__()

        self.callback_structure = SessionPortListenerCallBacks()

        self.callback_structure.AcceptSessionJoiner = self._OnAcceptSessionJoinerCallBack()
        self.callback_structure.SessionJoined = self._OnSessionJoinedCallback()

        self.handle = self._Create(C.byref(self.callback_structure), context)

    def __del__(self):
        if self.handle:
            return self._Destroy(self.handle)

    def _OnAcceptSessionJoinerCallBack(self):
        def func(context, session_port, joiner, opts):
          return self.OnAcceptSessionJoinerCallBack(context, session_port, joiner, opts)
        return SessionPortListenerAcceptSessionJoinerFuncType(func)

    def _OnSessionJoinedCallback(self):
        def func(context, session_port, session_id, joiner):
          self.OnSessionJoinedCallback(context, session_port, session_id, joiner)
        return SessionPortListenerSessionJoinedFuncType(func)

    def OnAcceptSessionJoinerCallBack(self, context, session_port, joiner, opts):
        return 1

    def OnSessionJoinedCallback(self, context, session_port, session_id, joiner):
        pass


SessionPortListener.bind_functions_to_cls()
