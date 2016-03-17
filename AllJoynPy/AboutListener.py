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
import MsgArg
# Wrapper for file AboutListener.h

# Typedefs
# struct _alljoyn_aboutlistener_handle * alljoyn_aboutlistener
# void (*)(const void *, const char *, int, int, const int, const int) alljoyn_about_announced_ptr
# struct alljoyn_aboutlistener_callback alljoyn_aboutlistener_callback

    
if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE

# context busName version port objectDescriptionArg aboutDataArg
AboutAnnouncedFuncType = CallbackType(None, C.c_void_p, C.c_char_p, C.c_ushort, C.c_ushort, MsgArg.MsgArgHandle, MsgArg.MsgArgHandle)


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

    def __init__(self, context=None):
        super(AboutListener, self).__init__()

        self.callback_structure = AboutListenerCallBack()

        # Usually ctypes would handle the self magic but in this case the ptr is stuck into a structure
        # and ctypes does not then do the magic
        self.callback_structure.AboutListenerAnnounced = self._OnAboutListenerCallBack()

        self.handle = self._Create(C.byref(self.callback_structure), context)

    def __del__(self):
        self._Destroy(self.handle)

    def _OnAboutListenerCallBack(self):
        def func(context, busName, version, port, objectDescriptionArg, aboutDataArg):
          self.OnAboutListenerCallBack(context, busName, version, port, MsgArg.MsgArg.FromHandle(objectDescriptionArg),
            MsgArg.MsgArg.FromHandle(aboutDataArg))
        return AboutAnnouncedFuncType(func)

    def OnAboutListenerCallBack(self, context, busName, version, port, objectDescriptionArg, aboutDataArg):
        pass


AboutListener.bind_functions_to_cls()
