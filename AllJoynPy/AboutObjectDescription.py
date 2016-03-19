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

# Wrapper for file AboutObjectDescription.h

class AboutObjectDescriptionHandle(C.c_void_p):
    pass

class AboutObjectDescription(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'Clear': (u'alljoyn_aboutobjectdescription_clear',
                            (u'void', None),
                            (((u'alljoyn_aboutobjectdescription', AboutObjectDescriptionHandle)),)),

                 u'Create': (u'alljoyn_aboutobjectdescription_create',
                             ((u'alljoyn_aboutobjectdescription', AboutObjectDescriptionHandle)),
                             ()),

                 u'CreateFromMsgARG': (u'alljoyn_aboutobjectdescription_createfrommsgarg',
                                       (u'QStatus', C.c_uint),
                                       (((u'alljoyn_aboutobjectdescription', AboutObjectDescriptionHandle)),
                                           (u'const void*', MsgArg.MsgArgHandle))),

                 u'CreateFull': (u'alljoyn_aboutobjectdescription_create_full',
                                 ((u'alljoyn_aboutobjectdescription', AboutObjectDescriptionHandle)), 
                                 ((u'const void*', C.c_void_p),)),

                 u'Destroy': (u'alljoyn_aboutobjectdescription_destroy', (u'void', None),
                              (((u'alljoyn_aboutobjectdescription', AboutObjectDescriptionHandle)),)),

                 u'GetInterfacePaths': (u'alljoyn_aboutobjectdescription_getinterfacepaths',
                                        (u'int', C.c_int),
                                        (((u'alljoyn_aboutobjectdescription', AboutObjectDescriptionHandle)),
                                         (u'const char *', C.c_char_p),
                                         (u'const char **', POINTER(C.c_char_p)),
                                         (u'int', C.c_int))),

                 u'GetInterfaces': (u'alljoyn_aboutobjectdescription_getinterfaces',
                                    (u'int', C.c_int),
                                    (((u'alljoyn_aboutobjectdescription', AboutObjectDescriptionHandle)),
                                     (u'const char *', C.c_char_p),
                                     (u'const char **', POINTER(C.c_char_p)),
                                     (u'int', C.c_int))),

                 u'GetMsgARG': (u'alljoyn_aboutobjectdescription_getmsgarg',
                                (u'QStatus', C.c_uint),
                                (((u'alljoyn_aboutobjectdescription', AboutObjectDescriptionHandle)),
                                 (u'int', C.c_int))),

                 u'GetPaths': (u'alljoyn_aboutobjectdescription_getpaths',
                               (u'int', C.c_int),
                               (((u'alljoyn_aboutobjectdescription', AboutObjectDescriptionHandle)),
                                (u'const char **', POINTER(C.c_char_p)),
                                (u'int', C.c_int))),

                 u'HasInterface': (u'alljoyn_aboutobjectdescription_hasinterface',
                                   (u'int', C.c_int),
                                   (((u'alljoyn_aboutobjectdescription', AboutObjectDescriptionHandle)),
                                    (u'const char *', C.c_char_p))),

                 u'HasInterfaceAtPath': (u'alljoyn_aboutobjectdescription_hasinterfaceatpath',
                                         (u'int', C.c_int),
                                         (((u'alljoyn_aboutobjectdescription', AboutObjectDescriptionHandle)),
                                          (u'const char *', C.c_char_p),
                                          (u'const char *', C.c_char_p))),

                 u'HasPath': (u'alljoyn_aboutobjectdescription_haspath',
                              (u'int', C.c_int),
                              (((u'alljoyn_aboutobjectdescription', AboutObjectDescriptionHandle)),
                                  (u'const char *', C.c_char_p)))}

    def __init__(self, msgarg=None):
        super(AboutObjectDescription, self).__init__()

        if msgarg:
            self.handle = self._Create()
            self._CreateFromMsgARG(self.handle, msgarg.handle)
        else:
            self.handle = self._Create()

    def __del__(self):
        if self.handle:
            self._Destroy(self.handle)

    # Wrapper Methods

    # def CreateFull(cls, msgarg):
    #    return self._CreateFull(msgarg)

    # def CreateFromMsgARG(self, msgarg):
    #    return self._CreateFromMsgARG(self.handle, msgarg)

    # def Destroy(self):
    #    return self._Destroy(self.handle)

    def GetPaths(self):
        count = self._GetPaths(self.handle, None, 0)
        array = (C.c_char_p * count)()
        self._GetPaths(self.handle, array, count)  # const char **, int
        return [str(a) for a in array]

    def GetInterfaces(self, path):
        count = self._GetInterfaces(self.handle, path, None, 0)
        array = (C.c_char_p * count)()
        self._GetInterfaces(self.handle, path, array, count)  # const char **, int
        return [str(a).strip() for a in array]

    def GetInterfacePaths(self, interfaceName):
        count = self._GetInterfacePaths(self.handle, interfaceName, None, 0)
        array = (C.c_char_p * count)()
        self._GetInterfacePaths(self.handle, interfaceName, array, count)  # const char *,const char **,int
        return [str(a).strip() for a in array]

    def Clear(self):
        return self._Clear(self.handle)

    def HasPath(self, path):
        return self._HasPath(self.handle, path)  # const char *

    def HasInterface(self, interfaceName):
        return self._HasInterface(self.handle, interfaceName)  # const char *

    def HasInterfaceAtPath(self, path, interfaceName):
        return self._HasInterfaceAtPath(self.handle, path, interfaceName)  # const char *,const char *

    def GetMsGARG(self, msgArg):
        return self._GetMsGARG(self.handle, msgArg)  # int


AboutObjectDescription.bind_functions_to_cls()
