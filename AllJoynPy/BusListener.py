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
from . import *


# Wrapper for file BusListener.h

if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE


BusListenerListenerRegisteredFuncType = CallbackType(None, C.c_void_p, C.c_void_p)  # context bus

BusListenerListenerUnregisteredFuncType = CallbackType(None, C.c_void_p)  # context

BusListenerFoundAdvertisedNameFuncType = CallbackType(
    None, C.c_void_p, C.c_char_p, C.c_int, C.c_char_p)  # context name transport namePrefix

BusListenerLostAdvertisedNameFuncType = CallbackType(
    None, C.c_void_p, C.c_char_p, C.c_int, C.c_char_p)  # context name transport namePrefix

BusListenerNameOwnerChangedFuncType = CallbackType(
    None, C.c_void_p, C.c_char_p, C.c_char_p, C.c_char_p)  # context busName previousOwner newOwner

BusListenerBusStoppingFuncType = CallbackType(None, C.c_void_p)  # context

BusListenerBusDisconnectedFuncType = CallbackType(None, C.c_void_p)  # context

BusListenerBusPropChangedFuncType = CallbackType(None, C.c_void_p, C.c_char_p, C.c_int)  # context prop_name prop_value


class BusListenerCallBacks(C.Structure):
    _fields_ = [
        ("ListenerRegistered", BusListenerListenerRegisteredFuncType),
        ("ListenerUnregistered", BusListenerListenerUnregisteredFuncType),
        ("FoundAdvertisedName", BusListenerFoundAdvertisedNameFuncType),
        ("LostAdvertisedName", BusListenerLostAdvertisedNameFuncType),
        ("NameOwnerChanged", BusListenerNameOwnerChangedFuncType),
        ("BusStopping", BusListenerBusStoppingFuncType),
        ("BusDisconnected", BusListenerBusDisconnectedFuncType),
        ("PropertyChanged", BusListenerBusPropChangedFuncType), ]


class BusListener(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'Create': (u'alljoyn_buslistener_create',
                             (u'alljoyn_buslistener', BusListenerHandle),
                             ((u'const alljoyn_buslistener_callbacks *', POINTER(BusListenerCallBacks)),
                                 (u'const void *', C.c_void_p))),

                 u'Destroy': (u'alljoyn_buslistener_destroy',
                              (u'void', None),
                              ((u'alljoyn_buslistener', BusListenerHandle),))}

    def __init__(self, context=None):

        super(BusListener, self).__init__()

        self.callback_structure = BusListenerCallBacks()

        self.callback_structure.ListenerRegistered = self._OnListenerRegisteredCallBack()
        self.callback_structure.ListenerUnregistered = self._OnListenerUnregisteredCallback()
        self.callback_structure.FoundAdvertisedName = self._OnFoundAdvertisedNameCallBack()
        self.callback_structure.LostAdvertisedName = self._OnLostAdvertisedNameCallBack()
        self.callback_structure.NameOwnerChanged = self._OnNameOwnerChangedCallBack()
        self.callback_structure.BusStopping = self._OnBusStoppingCallBack()
        self.callback_structure.BusDisconnected = self._OnBusDisconnectedCallBack()
        self.callback_structure.PropertyChanged = self._OnPropertyChangedCallBack()

        self.handle = self._Create(C.byref(self.callback_structure), context)

    def __del__(self):
        if self.handle:
            self._Destroy(self.handle)

    # Wrapper Methods

    def _OnListenerRegisteredCallBack(self):
        def func(context, bus):
          self.OnListenerRegisteredCallBack(context, bus)
        return BusListenerListenerRegisteredFuncType(func)

    def _OnListenerUnregisteredCallback(self):
        def func(context):
          self.OnListenerUnregisteredCallback(context)
        return BusListenerListenerUnregisteredFuncType(func)

    def _OnFoundAdvertisedNameCallBack(self):
        def func(context, name, transport, name_prefix):
          self.OnFoundAdvertisedNameCallBack(context, name, transport, name_prefix)
        return BusListenerFoundAdvertisedNameFuncType(func)
   
    def _OnLostAdvertisedNameCallBack(self):
        def func(context, name, transport, name_prefix):
          self.OnLostAdvertisedNameCallBack(context, name, transport, name_prefix)
        return BusListenerLostAdvertisedNameFuncType(func)
   
    def _OnNameOwnerChangedCallBack(self):
        def func(context, bus_name, previous_owner, new_owner):
          self.OnNameOwnerChangedCallBack(context, bus_name, previous_owner, new_owner)
        return BusListenerNameOwnerChangedFuncType(func)

    def _OnBusStoppingCallBack(self):
        def func(context):
          self.OnBusStoppingCallBack(context)
        return BusListenerBusStoppingFuncType(func)

    def _OnBusDisconnectedCallBack(self):
        def func(context):
          self.OnBusDisconnectedCallBack(context)
        return BusListenerBusDisconnectedFuncType(func)

    def _OnPropertyChangedCallBack(self):
        def func(context, property_name, property_value):
          self.OnPropertyChangedCallBack(context, property_name, property_value)
        return BusListenerBusPropChangedFuncType(func)

    def OnListenerRegisteredCallBack(self, context, bus):
        pass

    def OnListenerUnregisteredCallback(self, context):
        pass

    def OnFoundAdvertisedNameCallBack(self, context, name, transport, name_prefix):
        pass

    def OnLostAdvertisedNameCallBack(self, context, name, transport, name_prefix):
        pass

    def OnNameOwnerChangedCallBack(self, context, bus_name, previous_owner, new_owner):
        pass

    def OnBusStoppingCallBack(self, context):
        pass

    def OnBusDisconnectedCallBack(self, context):
        pass

    def OnPropertyChangedCallBack(self, context, property_name, property_value):
        pass


BusListener.bind_functions_to_cls()
