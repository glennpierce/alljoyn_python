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
from . import AllJoynMeta, AllJoynObject


# Wrapper for file BusListener.h

class BusListenerHandle(C.c_void_p):
    pass

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

    def __init__(self, callback_data=None):

        super(BusListener, self).__init__()

        self.callback_structure = BusListenerCallBacks()

        self.callback_data = callback_data

        self.callback_structure.ListenerRegistered = BusListenerListenerRegisteredFuncType(
            BusListener._OnListenerRegisteredCallBack)

        self.callback_structure.ListenerUnregistered = BusListenerListenerUnregisteredFuncType(
            BusListener._OnListenerUnregisteredCallback)

        self.callback_structure.FoundAdvertisedName = BusListenerFoundAdvertisedNameFuncType(
            BusListener._OnFoundAdvertisedNameCallBack)

        self.callback_structure.LostAdvertisedName = BusListenerLostAdvertisedNameFuncType(
            BusListener._OnLostAdvertisedNameCallBack)

        self.callback_structure.NameOwnerChanged = BusListenerNameOwnerChangedFuncType(
            BusListener._OnNameOwnerChangedCallBack)

        self.callback_structure.BusStopping = BusListenerBusStoppingFuncType(
            BusListener._OnBusStoppingCallBack)

        self.callback_structure.BusDisconnected = BusListenerBusDisconnectedFuncType(
            BusListener._OnBusDisconnectedCallBack)

        self.callback_structure.PropertyChanged = BusListenerBusPropChangedFuncType(
            BusListener._OnPropertyChangedCallBack)

        print "self.unique_id", self.unique_id
        self.handle = self._Create(C.byref(self.callback_structure), self.unique_id)

    def __del__(self):
        if self.handle:
            return self._Destroy(self.handle)

    # Wrapper Methods

    @staticmethod
    def _OnListenerRegisteredCallBack(context, bus):
        print "context", context, "bus", bus
        self = AllJoynObject.unique_instances[context]
        self.OnListenerRegisteredCallBack(self.callback_data, bus)

    @staticmethod
    def _OnListenerUnregisteredCallback(context):
        self = AllJoynObject.unique_instances[context]
        self.OnListenerUnregisteredCallback(self.callback_data)

    @staticmethod
    def _OnFoundAdvertisedNameCallBack(context, name, transport, name_prefix):
        self = AllJoynObject.unique_instances[context]
        self.OnFoundAdvertisedNameCallBack(self.callback_data, name, transport, name_prefix)

    @staticmethod
    def _OnLostAdvertisedNameCallBack(context, name, transport, name_prefix):
        self = AllJoynObject.unique_instances[context]
        self.OnLostAdvertisedNameCallBack(self.callback_data, name, transport, name_prefix)

    @staticmethod
    def _OnNameOwnerChangedCallBack(context, bus_name, previous_owner, new_owner):
        self = AllJoynObject.unique_instances[context]
        self.OnNameOwnerChangedCallBack(self.callback_data, bus_name, previous_owner, new_owner)

    @staticmethod
    def _OnBusStoppingCallBack(context):
        self = AllJoynObject.unique_instances[context]
        self.OnBusStoppingCallBack(self.callback_data)

    @staticmethod
    def _OnBusDisconnectedCallBack(context):
        self = AllJoynObject.unique_instances[context]
        self.OnBusDisconnectedCallBack(self.callback_data)

    @staticmethod
    def _OnPropertyChangedCallBack(context, property_name, property_value):
        self = AllJoynObject.unique_instances[context]
        self.OnPropertyChangedCallBack(self.callback_data, property_name, property_value)

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
