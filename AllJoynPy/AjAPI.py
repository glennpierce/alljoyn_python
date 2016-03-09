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

# Wrapper for file AjAPI.h

@unique
class AnnounceFlag(Enum):
    UNANNOUNCED = 0
    ANNOUNCED = 1


# Typedefs
# int QCC_BOOL
# enum alljoyn_about_announceflag alljoyn_about_announceflag


if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE
    

class Unity(AllJoynObject):
    
    __metaclass__ = AllJoynMeta
    
    _cmethods = {u'DeferredCallBacksProcess': (u'alljoyn_unity_deferred_callbacks_process',
                               (u'int', C.c_int),
                               ()),
                 u'SetDeferredCallBackMainThreadOnly': (u'alljoyn_unity_set_deferred_callback_mainthread_only',
                                                        (u'void', None),
                                                        ((u'QCC_BOOL', C.c_int),))}
    
    def __init__(self):
        pass
        
    def __del__(self):
        #self.UnityDestroy(self.handle)
        pass

    # Wrapper Methods

    def DeferredCallBacksProcess(self):
        return self._DeferredCallBacksProcess(self.handle)

    def SetDeferredCallBackMainThreadOnly(self):
        return self._SetDeferredCallBackMainThreadOnly(self.handle)

    


Unity.bind_functions_to_cls()
