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

import sys, traceback
import ctypes as C
from ctypes import POINTER
from . import *
import InterfaceDescription, MsgArg, Message, MessageReceiver

# Wrapper for file BusObject.h

# Typedefs
# struct _alljoyn_busobject_handle * alljoyn_busobject
# int (int *) QStatus
# int (*)(const void *, const char *, const char *, int) alljoyn_busobject_prop_set_ptr
# void (*)(const void *) alljoyn_busobject_object_registration_ptr
# struct alljoyn_busobject_callbacks alljoyn_busobject_callbacks
# struct alljoyn_busobject_methodentry alljoyn_busobject_methodentry

if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE


BusObjectRegistrationFuncType = CallbackType(None, C.c_void_p)  # context

BusObjectPropertyGetFuncType = CallbackType(
    C.c_uint, C.c_void_p, C.c_char_p, C.c_char_p, MsgArg.MsgArgHandle)  # context, ifcName, propName, val

BusObjectPropertySetFuncType = CallbackType(
    C.c_uint, C.c_void_p, C.c_char_p, C.c_char_p, MsgArg.MsgArgHandle)  # context, ifcName, propName, val


class BusObjectCallBacks(C.Structure):
    _fields_ = [
        ("PropertyGet", BusObjectPropertyGetFuncType),
        ("PropertySet", BusObjectPropertySetFuncType),
        ("ObjectRegistered", BusObjectRegistrationFuncType),
        ("ObjectUnregistered", BusObjectRegistrationFuncType)

        #("Instance", C.c_void_p),
    ]


class BusObjectMethodEntry(C.Structure):
    _fields_ = [
        ("Member", POINTER(InterfaceDescription.InterfaceDescriptionMember)),
        ("MethodHandler", MessageReceiver.MessageReceiverMethodHandlerFuncType)
    ]


class BusObject(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'AddInterface': (u'alljoyn_busobject_addinterface',
                                   (u'QStatus', C.c_uint),
                                   ((u'alljoyn_busobject', BusObjectHandle),
                                       (u'const void*', InterfaceDescription.InterfaceDescriptionHandle))),

                 u'AddInterfaceAnnounced': (u'alljoyn_busobject_addinterface_announced',
                                            (u'QStatus', C.c_uint),
                                            ((u'alljoyn_busobject', BusObjectHandle),
                                                (u'const int', C.c_int))),

                 u'AddMethodHandler': (u'alljoyn_busobject_addmethodhandler',
                                       (u'QStatus', C.c_uint),
                                       ((u'alljoyn_busobject', BusObjectHandle),
                                           (u'const int', C.c_int),
                                           (u'int', C.c_int),
                                           (u'void *', C.c_void_p))),
                 u'AddMethodHandlers': (u'alljoyn_busobject_addmethodhandlers',
                                        (u'QStatus', C.c_uint),
                                        ((u'alljoyn_busobject', BusObjectHandle),
                                            (u'const alljoyn_busobject_methodentry *',
                                             POINTER(BusObjectMethodEntry)),
                                            (u'size_t', C.c_size_t))),
                 u'CancelSessionLessMessage': (u'alljoyn_busobject_cancelsessionlessmessage',
                                               (u'QStatus', C.c_uint),
                                               ((u'alljoyn_busobject', BusObjectHandle),
                                                   (u'const int', C.c_int))),
                 u'CancelSessionLessMessageSerial': (u'alljoyn_busobject_cancelsessionlessmessage_serial',
                                                     (u'QStatus', C.c_uint),
                                                     ((u'alljoyn_busobject', BusObjectHandle),
                                                         (u'int', C.c_int))),
                 u'Create': (u'alljoyn_busobject_create',
                             (u'alljoyn_busobject', BusObjectHandle),
                             ((u'const char *', C.c_char_p),
                                 (u'int', C.c_int),
                                 (u'const alljoyn_busobject_callbacks *',
                                  POINTER(BusObjectCallBacks)),
                                 (u'const void *', C.c_void_p))),
                 u'Destroy': (u'alljoyn_busobject_destroy',
                              (u'void', None),
                              ((u'alljoyn_busobject', BusObjectHandle),)),
                 u'EmitPropertiesChanged': (u'alljoyn_busobject_emitpropertieschanged',
                                            (u'void', None),
                                            ((u'alljoyn_busobject', BusObjectHandle),
                                             (u'const char *', C.c_char_p),
                                             (u'const char **', POINTER(C.c_char_p)),
                                             (u'int', C.c_int),
                                             (u'int', C.c_int))),
                 u'EmitPropertyChanged': (u'alljoyn_busobject_emitpropertychanged',
                                          (u'void', None),
                                          ((u'alljoyn_busobject', BusObjectHandle),
                                           (u'const char *', C.c_char_p),
                                           (u'const char *', C.c_char_p),
                                           (u'int', C.c_int),
                                           (u'int', C.c_int))),
                 u'GetAnnouncedInterfaceNames': (u'alljoyn_busobject_getannouncedinterfacenames',
                                                 (u'int', C.c_int),
                                                 ((u'alljoyn_busobject', BusObjectHandle),
                                                  (u'const char **', POINTER(C.c_char_p)),
                                                  (u'int', C.c_int))),
                 u'GetBusAttachment': (u'alljoyn_busobject_getbusattachment',
                                       (u'const int', C.c_int),
                                       ((u'alljoyn_busobject', BusObjectHandle),)),
                 u'GetName': (u'alljoyn_busobject_getname',
                              (u'int', C.c_int),
                              ((u'alljoyn_busobject', BusObjectHandle),
                               (u'char *', C.c_char_p),
                               (u'int', C.c_int))),
                 u'GetPath': (u'alljoyn_busobject_getpath',
                              (u'const char *', C.c_char_p),
                              ((u'alljoyn_busobject', BusObjectHandle),)),
                 u'IsSecure': (u'alljoyn_busobject_issecure',
                               (u'int', C.c_int),
                               ((u'alljoyn_busobject', BusObjectHandle),)),


                 u'MethodReplyArgs': (u'alljoyn_busobject_methodreply_args',
                                      (u'QStatus', C.c_uint),
                                      ((u'alljoyn_busobject', BusObjectHandle),
                                       (u'void*', Message.MessageHandle),
                                       (u'void*', MsgArg.MsgArgHandle),
                                       (u'size_t', C.c_size_t))),

                 u'MethodReplyErr': (u'alljoyn_busobject_methodreply_err',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_busobject', BusObjectHandle),
                                      (u'int', C.c_int),
                                      (u'const char *', C.c_char_p),
                                      (u'const char *', C.c_char_p))),
                 u'MethodReplyStatus': (u'alljoyn_busobject_methodreply_status',
                                        (u'QStatus', C.c_uint),
                                        ((u'alljoyn_busobject', BusObjectHandle),
                                         (u'int', C.c_int),
                                         (u'QStatus', C.c_uint))),
                 u'SetAnnounceFlag': (u'alljoyn_busobject_setannounceflag',
                                      (u'QStatus', C.c_uint),
                                      ((u'alljoyn_busobject', BusObjectHandle),
                                       (u'void*', C.c_void_p),
                                       (u'int', C.c_int))),
                 u'Signal': (u'alljoyn_busobject_signal',
                             (u'QStatus', C.c_uint),
                             ((u'alljoyn_busobject', BusObjectHandle),
                              (u'const char *', C.c_char_p),
                              (u'int', C.c_int),
                              (u'const int', C.c_int),
                              (u'const int', C.c_int),
                              (u'int', C.c_int),
                              (u'int', C.c_int),
                              (u'int', C.c_int),
                              (u'int', C.c_int)))}

    def __init__(self, path, is_place_holder=False, context=None, setup_callbacks=True):
        super(BusObject, self).__init__()

        if setup_callbacks:
          self.callback_structure = BusObjectCallBacks()

          self.callback_structure.PropertyGet = self._OnPropertyGetCallBack()
          self.callback_structure.PropertySet = self._OnPropertySetCallback()
          self.callback_structure.ObjectRegistered = self._OnObjectRegisteredCallBack()
          self.callback_structure.ObjectUnregistered = self._OnObjectUnregisteredCallBack()

          self.handle = BusObject._Create(path, int(is_place_holder), C.byref(self.callback_structure), context)

    def __del__(self):
        if self.handle:
            pass
            # Todo When can this be called
            #self._Destroy(self.handle)

    @classmethod
    def FromHandle(cls, handle):
        assert type(handle) == BusObjectHandle
        instance = cls(BusObject._GetPath(handle), False, None, setup_callbacks=False)
        instance.handle = handle
        return instance

    def _OnPropertyGetCallBack(self):
        def func(context, ifcName, propName, val):
          self.OnPropertyGetCallBack(context, ifcName, propName, val)
        return BusObjectPropertyGetFuncType(func)

    def _OnPropertySetCallback(self):
        def func(context, ifcName, propName, val):
          self.OnPropertySetCallback(context, ifcName, propName, val)
        return BusObjectPropertySetFuncType(func)

    def _OnObjectRegisteredCallBack(self):
        def func(context):
          self.OnObjectRegisteredCallBack(context)
        return BusObjectRegistrationFuncType(func)

    def _OnObjectUnregisteredCallBack(self):
        def func(context):
          self.OnObjectUnRegisteredCallBack(context)
        return BusObjectRegistrationFuncType(func)
  
    def OnPropertyGetCallBack(self, context, ifcName, propName, val):
        pass

    def OnPropertySetCallBack(self, context, ifcName, propName, val):
        pass

    def OnObjectRegisteredCallBack(self, context):
        pass

    def OnObjectUnRegisteredCallBack(self, context):
        pass

    # Wrapper Methods

    def GetPath(self):
        return self._GetPath(self.handle)

    def EmitPropertyChanged(self, ifcName, propName, val, id):
        return self._EmitPropertyChanged(self.handle, ifcName, propName, val, id)  # const char *,const char *,int,int

    def EmitPropertiesChanged(self, ifcName, propNames, numProps, id):
        # const char *,const char **,int,int
        return self._EmitPropertiesChanged(self.handle, ifcName, propNames, numProps, id)

    def GetName(self, buffer, bufferSz):
        return self._GetName(self.handle, buffer, bufferSz)  # char *,int

    def AddInterface(self, iface):
        return self._AddInterface(self.handle, iface.handle)  # const int

    def AddMethodHandler(self, member, handler, context):
        return self._AddMethodHandler(self.handle, member, handler, context)  # const int,int,void *

    def AddMethodHandlers(self, entries):
        array = (BusObjectMethodEntry * len(entries))()
        array[:] = entries
        return self._AddMethodHandlers(self.handle, array, len(entries))

    def MethodReplyArgs(self, msg, args, num_args):
        return self._MethodReplyArgs(self.handle, msg.handle, args.handle, num_args)

    def MethodReplyErr(self, msg, error, errorMessage):
        # int,const char *,const char *
        return self._MethodReplyErr(self.handle, msg, error, errorMessage)

    def MethodReplyStatus(self, msg, status):
        return self._MethodReplyStatus(self.handle, msg, status)  # int,QStatus

    def GetBusAttachment(self):
        return self._GetBusAttachment(self.handle)

    def Signal(self, destination, sessionId, signal, args, numArgs, timeToLive, flags, msg):
        # const char *,int,const int,const int,int,int,int,int
        return self._Signal(self.handle, destination, sessionId, signal, args, numArgs, timeToLive, flags, msg)

    def CancelSessionLessMessageSerial(self, serialNumber):
        return self._CancelSessionLessMessageSerial(self.handle, serialNumber)  # int

    def CancelSessionLessMessage(self, msg):
        return self._CancelSessionLessMessage(self.handle, msg)  # const int

    def IsSecure(self):
        return self._IsSecure(self.handle)

    def GetAnnouncedInterfaceNames(self, interfaces, numInterfaces):
        # const char **,int
        return self._GetAnnouncedInterfaceNames(self.handle, interfaces, numInterfaces)

    def SetAnnounceFlag(self, iface, isAnnounced):
        # const int,int
        return self._SetAnnounceFlag(self.handle, iface.handle, isAnnounced.value)

    def AddInterfaceAnnounced(self, iface):
        return self._AddInterfaceAnnounced(self.handle, iface)  # const int


BusObject.bind_functions_to_cls()
