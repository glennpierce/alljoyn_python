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
# Wrapper for file Session.h


ALLJOYN_SESSION_PORT_ANY = 0
ALLJOYN_SESSION_ID_ALL_HOSTED = -1
ALLJOYN_TRAFFIC_TYPE_MESSAGES = 0x01   # Session carries message traffic
ALLJOYN_TRAFFIC_TYPE_RAW_UNRELIABLE = 0x02   # Session carries an unreliable (lossy) byte stream
ALLJOYN_TRAFFIC_TYPE_RAW_RELIABLE = 0x04   # Session carries a reliable byte stream
ALLJOYN_PROXIMITY_ANY = 0xFF  # Accept any proximity options
ALLJOYN_PROXIMITY_PHYSICAL = 0x01  # Limit the session to the same physical device
ALLJOYN_PROXIMITY_NETWORK = 0x02  # Limit the session to network proximity


class SessionOpts(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'Cmp': (u'alljoyn_sessionopts_cmp',
                          (u'int', C.c_int),
                          ((u'const alljoyn_sessionopts', SessionOptsHandle),
                              (u'const alljoyn_sessionopts', SessionOptsHandle))),

                 u'Create': (u'alljoyn_sessionopts_create',
                             (u'alljoyn_sessionopts', SessionOptsHandle),
                             ((u'int', C.c_int),
                                 (u'int', C.c_int),
                                 (u'int', C.c_int),
                                 (u'int', C.c_int))),

                 u'Destroy': (u'alljoyn_sessionopts_destroy',
                              (u'void', None),
                              ((u'alljoyn_sessionopts', SessionOptsHandle),)),

                 u'GetMultiPoint': (u'alljoyn_sessionopts_get_multipoint',
                                    (u'int', C.c_int),
                                    ((u'const alljoyn_sessionopts', SessionOptsHandle),)),

                 u'GetProximity': (u'alljoyn_sessionopts_get_proximity',
                                   (u'int', C.c_int),
                                   ((u'const alljoyn_sessionopts', SessionOptsHandle),)),

                 u'GetTraffic': (u'alljoyn_sessionopts_get_traffic',
                                 (u'int', C.c_int),
                                 ((u'const alljoyn_sessionopts', SessionOptsHandle),)),

                 u'GetTransports': (u'alljoyn_sessionopts_get_transports',
                                    (u'int', C.c_int),
                                    ((u'const alljoyn_sessionopts', SessionOptsHandle),)),

                 u'IsCompatible': (u'alljoyn_sessionopts_iscompatible',
                                   (u'int', C.c_int),
                                   ((u'const alljoyn_sessionopts', SessionOptsHandle),
                                       (u'const alljoyn_sessionopts', SessionOptsHandle))),

                 u'SetMultiPoint': (u'alljoyn_sessionopts_set_multipoint',
                                    (u'void', None),
                                    ((u'alljoyn_sessionopts', SessionOptsHandle),
                                        (u'int', C.c_int))),

                 u'SetProximity': (u'alljoyn_sessionopts_set_proximity',
                                   (u'void', None),
                                   ((u'alljoyn_sessionopts', SessionOptsHandle),
                                       (u'int', C.c_int))),

                 u'SetTraffic': (u'alljoyn_sessionopts_set_traffic',
                                 (u'void', None),
                                 ((u'alljoyn_sessionopts', SessionOptsHandle),
                                     (u'int', C.c_int))),

                 u'SetTransports': (u'alljoyn_sessionopts_set_transports',
                                    (u'void', None),
                                    ((u'alljoyn_sessionopts', SessionOptsHandle),
                                        (u'int', C.c_int)))}

    def __init__(self, traffic, isMultipoint, proximity, transports):
        super(SessionOpts, self).__init__()

        # extern AJ_API alljoyn_sessionopts AJ_CALL alljoyn_sessionopts_create(uint8_t traffic, QCC_BOOL isMultipoint,
        # uint8_t proximity, alljoyn_transportmask transports);
        self.handle = self._Create(traffic, isMultipoint, proximity, transports)  # int,int,int

    def __del__(self):
        return self._Destroy(self.handle)

    def GetTraffic(self):
        return self._GetTraffic(self.handle)

    def SetTraffic(self, traffic):
        return self._SetTraffic(self.handle, traffic)  # int

    def GetMultiPoint(self):
        return self._GetMultiPoint(self.handle)

    def SetMultiPoint(self, isMultipoint):
        return self._SetMultiPoint(self.handle, isMultipoint)  # int

    def GetProximity(self):
        return self._GetProximity(self.handle)

    def SetProximity(self, proximity):
        return self._SetProximity(self.handle, proximity)  # int

    def GetTransports(self):
        return self._GetTransports(self.handle)

    def SetTransports(self, transports):
        return self._SetTransports(self.handle, transports)  # int

    def IsCompatible(self, other):
        return self._IsCompatible(self.handle, other)  # const alljoyn_sessionopts

    def Cmp(self, other):
        return self._Cmp(self.handle, other)  # const alljoyn_sessionopts


SessionOpts.bind_functions_to_cls()
