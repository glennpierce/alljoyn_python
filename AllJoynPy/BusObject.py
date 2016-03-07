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
    
BusObjectRegistrationFuncType = CallbackType(None, C.c_void_p) # context
BusObjectPropertyGetFuncType = CallbackType(C.c_uint, C.c_void_p, C.c_char_p, C.c_char_p, C.c_void_p msgarg)  # context, ifcName, propName, val
BusObjectPropertySetFuncType = CallbackType(C.c_uint, C.c_void_p, C.c_char_p, C.c_char_p, C.c_void_p msgarg)  # context, ifcName, propName, val


class BusObjectCallBacks(C.Structure):
    _fields_ = [
                ("PropertyGet", POINTER(BusObjectPropertyGetFuncType)),
                ("PropertySet", POINTER(BusObjectPropertySetFuncType)),
                ("ObjectRegistered", POINTER(BusObjectRegistrationFuncType)),
                ("ObjectUnregistered", POINTER(BusObjectRegistrationFuncType))
               ]

class BusObjectMethodEntry(C.Structure):
    _fields_ = [
                ("Member", POINTER(constunknown_fix)),
                ("MethodHandler", POINTER(alljoyn_messagereceiver_methodhandler_ptrunknown_fix))
               ]



class BusObject(AllJoynObject):
    
    __metaclass__ = AllJoynMeta
    
    _cmethods = {u'AddInterface': (u'alljoyn_busobject_addinterface',
                   (u'QStatus', 'C.c_uint'),
                   ((u'alljoyn_busobject', 'C.c_void_p'),
                    (u'const int', 'C.c_int'))),
                 u'AddInterfaceAnnounced': (u'alljoyn_busobject_addinterface_announced',
                                            (u'QStatus', 'C.c_uint'),
                                            ((u'alljoyn_busobject', 'C.c_void_p'),
                                             (u'const int', 'C.c_int'))),
                 u'AddMethodHandler': (u'alljoyn_busobject_addmethodhandler',
                                       (u'QStatus', 'C.c_uint'),
                                       ((u'alljoyn_busobject', 'C.c_void_p'),
                                        (u'const int', 'C.c_int'),
                                        (u'int', 'C.c_int'),
                                        (u'void *', 'C.c_void_p'))),
                 u'AddMethodHandlers': (u'alljoyn_busobject_addmethodhandlers',
                                        (u'QStatus', 'C.c_uint'),
                                        ((u'alljoyn_busobject', 'C.c_void_p'),
                                         (u'const alljoyn_busobject_methodentry *',
                                          u'POINTER(BusObjectMethodEntry)'),
                                         (u'int', 'C.c_int'))),
                 u'CancelSessionLessMessage': (u'alljoyn_busobject_cancelsessionlessmessage',
                                               (u'QStatus', 'C.c_uint'),
                                               ((u'alljoyn_busobject', 'C.c_void_p'),
                                                (u'const int', 'C.c_int'))),
                 u'CancelSessionLessMessageSerial': (u'alljoyn_busobject_cancelsessionlessmessage_serial',
                                                     (u'QStatus', 'C.c_uint'),
                                                     ((u'alljoyn_busobject', 'C.c_void_p'),
                                                      (u'int', 'C.c_int'))),
                 u'Create': (u'alljoyn_busobject_create',
                             (u'alljoyn_busobject', 'C.c_void_p'),
                             ((u'const char *', 'C.c_char_p'),
                              (u'int', 'C.c_int'),
                              (u'const alljoyn_busobject_callbacks *',
                               u'POINTER(BusObjectCallBacks)'),
                              (u'const void *', 'C.c_void_p'))),
                 u'Destroy': (u'alljoyn_busobject_destroy',
                              (u'void', None),
                              ((u'alljoyn_busobject', 'C.c_void_p'),)),
                 u'EmitPropertiesChanged': (u'alljoyn_busobject_emitpropertieschanged',
                                            (u'void', None),
                                            ((u'alljoyn_busobject', 'C.c_void_p'),
                                             (u'const char *', 'C.c_char_p'),
                                             (u'const char **', 'POINTER(C.c_char_p)'),
                                             (u'int', 'C.c_int'),
                                             (u'int', 'C.c_int'))),
                 u'EmitPropertyChanged': (u'alljoyn_busobject_emitpropertychanged',
                                          (u'void', None),
                                          ((u'alljoyn_busobject', 'C.c_void_p'),
                                           (u'const char *', 'C.c_char_p'),
                                           (u'const char *', 'C.c_char_p'),
                                           (u'int', 'C.c_int'),
                                           (u'int', 'C.c_int'))),
                 u'GetAnnouncedInterfaceNames': (u'alljoyn_busobject_getannouncedinterfacenames',
                                                 (u'int', 'C.c_int'),
                                                 ((u'alljoyn_busobject', 'C.c_void_p'),
                                                  (u'const char **', 'POINTER(C.c_char_p)'),
                                                  (u'int', 'C.c_int'))),
                 u'GetBusAttachment': (u'alljoyn_busobject_getbusattachment',
                                       (u'const int', 'C.c_int'),
                                       ((u'alljoyn_busobject', 'C.c_void_p'),)),
                 u'GetName': (u'alljoyn_busobject_getname',
                              (u'int', 'C.c_int'),
                              ((u'alljoyn_busobject', 'C.c_void_p'),
                               (u'char *', 'C.c_char_p'),
                               (u'int', 'C.c_int'))),
                 u'GetPath': (u'alljoyn_busobject_getpath',
                              (u'const char *', 'C.c_char_p'),
                              ((u'alljoyn_busobject', 'C.c_void_p'),)),
                 u'IsSecure': (u'alljoyn_busobject_issecure',
                               (u'int', 'C.c_int'),
                               ((u'alljoyn_busobject', 'C.c_void_p'),)),
                 u'MethodReplyARGS': (u'alljoyn_busobject_methodreply_args',
                                      (u'QStatus', 'C.c_uint'),
                                      ((u'alljoyn_busobject', 'C.c_void_p'),
                                       (u'int', 'C.c_int'),
                                       (u'const int', 'C.c_int'),
                                       (u'int', 'C.c_int'))),
                 u'MethodReplyErr': (u'alljoyn_busobject_methodreply_err',
                                     (u'QStatus', 'C.c_uint'),
                                     ((u'alljoyn_busobject', 'C.c_void_p'),
                                      (u'int', 'C.c_int'),
                                      (u'const char *', 'C.c_char_p'),
                                      (u'const char *', 'C.c_char_p'))),
                 u'MethodReplyStatus': (u'alljoyn_busobject_methodreply_status',
                                        (u'QStatus', 'C.c_uint'),
                                        ((u'alljoyn_busobject', 'C.c_void_p'),
                                         (u'int', 'C.c_int'),
                                         (u'QStatus', 'C.c_uint'))),
                 u'SetAnnounceFlag': (u'alljoyn_busobject_setannounceflag',
                                      (u'QStatus', 'C.c_uint'),
                                      ((u'alljoyn_busobject', 'C.c_void_p'),
                                       (u'const int', 'C.c_int'),
                                       (u'int', 'C.c_int'))),
                 u'Signal': (u'alljoyn_busobject_signal',
                             (u'QStatus', 'C.c_uint'),
                             ((u'alljoyn_busobject', 'C.c_void_p'),
                              (u'const char *', 'C.c_char_p'),
                              (u'int', 'C.c_int'),
                              (u'const int', 'C.c_int'),
                              (u'const int', 'C.c_int'),
                              (u'int', 'C.c_int'),
                              (u'int', 'C.c_int'),
                              (u'int', 'C.c_int'),
                              (u'int', 'C.c_int')))}
        
    
    def __init__(self, callback_data=None):

        super(SessionListener, self).__init__()

        self.callback_structure = SessionListenerCallBacks()

        self.callback_data = callback_data

        self.callback_structure.SessionLost = SessionListenerSessionLostFuncType(SessionListener._OnSessionLostCallBack)
        self.callback_structure.SessionMemberAdded = SessionListenerSessionMemberAddedFuncType(
            SessionListener._OnSessionMemberAddedCallback)
        self.callback_structure.SessionMemberRemoved = SessionListenerSessionMemberRemovedFuncType(
            SessionListener._OnSessionMemberRemovedCallBack)

        self.handle = self._Create(C.byref(self.callback_structure), self.unique_id)

    def __del__(self):
        if self.handle:
            return self._Destroy(self.handle)

    # Wrapper Methods

    def Create(self, isPlaceholder,callbacks_in,context_in):
        return self._Create(self.handle,isPlaceholder,callbacks_in,context_in) # int,const alljoyn_busobject_callbacks *,const void *

    def Destroy(self):
        return self._Destroy(self.handle)

    def GetPath(self):
        return self._GetPath(self.handle)

    def EmitPropertyChanged(self, ifcName,propName,val,id):
        return self._EmitPropertyChanged(self.handle,ifcName,propName,val,id) # const char *,const char *,int,int

    def EmitPropertiesChanged(self, ifcName,propNames,numProps,id):
        return self._EmitPropertiesChanged(self.handle,ifcName,propNames,numProps,id) # const char *,const char **,int,int

    def GetName(self, buffer,bufferSz):
        return self._GetName(self.handle,buffer,bufferSz) # char *,int

    def AddInterface(self, iface):
        return self._AddInterface(self.handle,iface) # const int

    def AddMethodHandler(self, member,handler,context):
        return self._AddMethodHandler(self.handle,member,handler,context) # const int,int,void *

    def AddMethodHandlers(self, entries,numEntries):
        return self._AddMethodHandlers(self.handle,entries,numEntries) # const alljoyn_busobject_methodentry *,int

    def MethodReplyARGS(self, msg,args,numArgs):
        return self._MethodReplyARGS(self.handle,msg,args,numArgs) # int,const int,int

    def MethodReplyErr(self, msg,error,errorMessage):
        return self._MethodReplyErr(self.handle,msg,error,errorMessage) # int,const char *,const char *

    def MethodReplyStatus(self, msg,status):
        return self._MethodReplyStatus(self.handle,msg,status) # int,QStatus

    def GetBusAttachment(self):
        return self._GetBusAttachment(self.handle)

    def Signal(self, destination,sessionId,signal,args,numArgs,timeToLive,flags,msg):
        return self._Signal(self.handle,destination,sessionId,signal,args,numArgs,timeToLive,flags,msg) # const char *,int,const int,const int,int,int,int,int

    def CancelSessionLessMessageSerial(self, serialNumber):
        return self._CancelSessionLessMessageSerial(self.handle,serialNumber) # int

    def CancelSessionLessMessage(self, msg):
        return self._CancelSessionLessMessage(self.handle,msg) # const int

    def IsSecure(self):
        return self._IsSecure(self.handle)

    def GetAnnouncedInterfaceNames(self, interfaces,numInterfaces):
        return self._GetAnnouncedInterfaceNames(self.handle,interfaces,numInterfaces) # const char **,int

    def SetAnnounceFlag(self, iface,isAnnounced):
        return self._SetAnnounceFlag(self.handle,iface,isAnnounced) # const int,int

    def AddInterfaceAnnounced(self, iface):
        return self._AddInterfaceAnnounced(self.handle,iface) # const int

    


sys.modules[__name__] = BusObject()  # See https://mail.python.org/pipermail/python-ideas/2012-May/014969.html
