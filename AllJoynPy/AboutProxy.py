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

import ctypes as C
from ctypes import POINTER
from . import *
import MsgArg

# Wrapper for file AboutProxy.h


class AboutProxy(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'Create': (u'alljoyn_aboutproxy_create',
                             (u'alljoyn_aboutproxy', AboutProxyHandle),
                             ((u'void*', C.c_void_p),
                                 (u'const char *', C.c_char_p),
                                 (u'uint', C.c_uint))),

                 u'Destroy': (u'alljoyn_aboutproxy_destroy',
                              (u'void', None),
                              ((u'alljoyn_aboutproxy', AboutProxyHandle),)),

                 u'GetAboutData': (u'alljoyn_aboutproxy_getaboutdata',
                                   (u'QStatus', C.c_uint),
                                   ((u'alljoyn_aboutproxy', AboutProxyHandle),
                                       (u'const char *', C.c_char_p),
                                       (u'void*', MsgArg.MsgArgHandle))),

                 u'GetObjectDescription': (u'alljoyn_aboutproxy_getobjectdescription',
                                           (u'QStatus', C.c_uint),
                                           ((u'alljoyn_aboutproxy', AboutProxyHandle),
                                               (u'void*', (MsgArg.MsgArgHandle)))),

                 u'GetVersion': (u'alljoyn_aboutproxy_getversion',
                                 (u'QStatus', C.c_uint),
                                 ((u'alljoyn_aboutproxy', AboutProxyHandle),
                                     (u'uint16 *', POINTER(C.c_ushort))))}

    def __init__(self, bus, busName, sessionId):
        super(AboutProxy, self).__init__()
        self.handle = self._Create(bus.handle, busName, sessionId)

    def __del__(self):
        self._Destroy(self.handle)

    # Wrapper Methods
    def GetObjectDescription(self):
        handle = MsgArg.MsgArg._Create()
        self._GetObjectDescription(self.handle, handle)  # int
        return MsgArg.MsgArg.FromHandle(handle)

    def GetAboutData(self, language="en"):
        handle = MsgArg.MsgArg._Create()
        self._GetAboutData(self.handle, language, handle)  # const char *,int
        return MsgArg.MsgArg.FromHandle(handle)

    def GetVersion(self):
        version = C.c_ushort()
        self._GetVersion(self.handle, C.byref(version))  # int *
        return version.value


AboutProxy.bind_functions_to_cls()