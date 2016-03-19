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
from . import *

# Wrapper for file AboutObj.h

if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE


class AboutObject(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'Announce': (u'alljoyn_aboutobj_announce', (u'QStatus', C.c_uint),
                               (((u'alljoyn_aboutobj', AboutObjectHandle)),
                                (u'int', C.c_int), (u'void*', C.c_void_p))),

                 u'AnnounceUsingDataListener': (u'alljoyn_aboutobj_announce_using_datalistener',
                                                (u'QStatus', C.c_uint),
                                                (((u'alljoyn_aboutobj', AboutObjectHandle)),
                                                    (u'int', C.c_int),
                                                    (u'void*', C.c_void_p))),

                 u'Create': (u'alljoyn_aboutobj_create',
                             ((u'alljoyn_aboutobj', AboutObjectHandle)),
                             ((u'void*', C.c_void_p), (u'uint', C.c_uint))),

                 u'Destroy': (u'alljoyn_aboutobj_destroy', (u'void', None),
                              (((u'alljoyn_aboutobj', AboutObjectHandle)),)),

                 u'UnAnnounce': (u'alljoyn_aboutobj_unannounce', (u'QStatus', C.c_uint),
                                 (((u'alljoyn_aboutobj', AboutObjectHandle)),))
                 }

    def __init__(self, bus, isAnnounced):
        self.handle = self._Create(bus.handle, isAnnounced.value)

    def __del__(self):
        return self._Destroy(self.handle)

    # Wrapper Methods

    def Announce(self, sessionPort, aboutData):
        return self._Announce(self.handle, sessionPort, aboutData.handle)  # int,int

    def AnnounceUsingDataListener(self, sessionPort, aboutListener):
        return self._AnnounceUsingDataListener(self.handle, sessionPort, aboutListener.handle)  # int,int

    def UnAnnounce(self):
        return self._UnAnnounce(self.handle)


AboutObject.bind_functions_to_cls()
