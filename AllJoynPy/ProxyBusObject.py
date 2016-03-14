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
from . import AllJoynMeta, AllJoynObject, Message, BusAttachment, InterfaceDescription, MsgArg

# Wrapper for file ProxyBusObject.h


class ProxyBusHandle(C.c_void_p):
    pass

if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE

ProxyBusObjectListenerIntroSpecTCBFuncType = CallbackType(None, C.c_int, C.c_void_p, C.c_void_p)  # status obj context
ProxyBusObjectListenerGetAllPropertiesCBFuncType = CallbackType(
    None, C.c_int, C.c_void_p, C.c_int, C.c_void_p)  # status obj values context
ProxyBusObjectListenerPropertiesChangedFuncType = CallbackType(
    None, C.c_void_p, C.c_char_p, C.c_int, C.c_int, C.c_void_p)  # obj ifaceName changed invalidated context
ProxyBusObjectListenerGetPropertyCBFuncType = CallbackType(
    None, C.c_int, C.c_void_p, C.c_int, C.c_void_p)  # status obj value context
ProxyBusObjectListenerSetPropertyCBFuncType = CallbackType(None, C.c_int, C.c_void_p, C.c_void_p)  # status obj context


class ProxyBusObject(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'AddChild': (u'alljoyn_proxybusobject_addchild',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                   (u'const alljoyn_proxybusobject', C.c_void_p))),
                 u'AddInterface': (u'alljoyn_proxybusobject_addinterface',
                                   (u'QStatus', C.c_uint),
                                   ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                       (u'const void*', InterfaceDescription.InterfaceDescriptionHandle))),
                 u'AddInterfaceByName': (u'alljoyn_proxybusobject_addinterface_by_name',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                             (u'const char *', C.c_char_p))),
                 u'Copy': (u'alljoyn_proxybusobject_copy',
                           (u'alljoyn_proxybusobject', ProxyBusHandle),
                           ((u'const alljoyn_proxybusobject', C.c_void_p),)),

                 u'Create': (u'alljoyn_proxybusobject_create',
                             (u'alljoyn_proxybusobject', ProxyBusHandle),
                             ((u'alljoyn_busattachment', C.c_void_p),
                                 (u'const char *', C.c_char_p),
                                 (u'const char *', C.c_char_p),
                                 (u'int', C.c_int))),

                 u'CreateSecure': (u'alljoyn_proxybusobject_create_secure',
                                   (u'alljoyn_proxybusobject', ProxyBusHandle),
                                   ((u'alljoyn_busattachment', BusAttachment.BusAttachmentHandle),
                                       (u'const char *', C.c_char_p),
                                       (u'const char *', C.c_char_p),
                                       (u'int', C.c_int))),
                 u'Destroy': (u'alljoyn_proxybusobject_destroy',
                              (u'void', None),
                              ((u'alljoyn_proxybusobject', ProxyBusHandle),)),
                 u'EnablePropertyCaching': (u'alljoyn_proxybusobject_enablepropertycaching',
                                            (u'void', None),
                                            ((u'alljoyn_proxybusobject', ProxyBusHandle),)),
                 u'GetAllProperties': (u'alljoyn_proxybusobject_getallproperties',
                                       (u'QStatus', C.c_uint),
                                       ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                           (u'const char *', C.c_char_p),
                                           (u'int', C.c_int))),
                 u'GetAllPropertiesAsYNC': (u'alljoyn_proxybusobject_getallpropertiesasync',
                                            (u'QStatus', C.c_uint),
                                            ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                                (u'const char *', C.c_char_p),
                                                (u'alljoyn_proxybusobject_listener_getallpropertiescb_ptr',
                                                 POINTER(ProxyBusObjectListenerGetAllPropertiesCBFuncType)),
                                                (u'int', C.c_int),
                                                (u'void *', C.c_void_p))),
                 u'GetChild': (u'alljoyn_proxybusobject_getchild',
                               (u'alljoyn_proxybusobject', ProxyBusHandle),
                               ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                   (u'const char *', C.c_char_p))),
                 u'GetChildren': (u'alljoyn_proxybusobject_getchildren',
                                  (u'int', C.c_int),
                                  ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                      (u'alljoyn_proxybusobject *', POINTER(C.c_void_p)),
                                      (u'int', C.c_int))),
                 u'GetInterface': (u'alljoyn_proxybusobject_getinterface',
                                   (u'const void*', InterfaceDescription.InterfaceDescriptionHandle),
                                   ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                       (u'const char *', C.c_char_p))),
                 u'GetInterfaces': (u'alljoyn_proxybusobject_getinterfaces',
                                    (u'int', C.c_int),
                                    ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                        (u'const int *', POINTER(C.c_int)),
                                        (u'int', C.c_int))),
                 u'GetPath': (u'alljoyn_proxybusobject_getpath',
                              (u'const char *', C.c_char_p),
                              ((u'alljoyn_proxybusobject', ProxyBusHandle),)),
                 u'GetProperty': (u'alljoyn_proxybusobject_getproperty',
                                  (u'QStatus', C.c_uint),
                                  ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                      (u'const char *', C.c_char_p),
                                      (u'const char *', C.c_char_p),
                                      (u'int', C.c_int))),
                 u'GetPropertyAsync': (u'alljoyn_proxybusobject_getpropertyasync',
                                       (u'QStatus', C.c_uint),
                                       ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                           (u'const char *', C.c_char_p),
                                           (u'const char *', C.c_char_p),
                                           (u'alljoyn_proxybusobject_listener_getpropertycb_ptr',
                                            POINTER(ProxyBusObjectListenerGetPropertyCBFuncType)),
                                           (u'int', C.c_int),
                                           (u'void *', C.c_void_p))),
                 u'GetServiceName': (u'alljoyn_proxybusobject_getservicename',
                                     (u'const char *', C.c_char_p),
                                     ((u'alljoyn_proxybusobject', ProxyBusHandle),)),
                 u'GetSessionId': (u'alljoyn_proxybusobject_getsessionid',
                                   (u'int', C.c_int),
                                   ((u'alljoyn_proxybusobject', ProxyBusHandle),)),
                 u'GetUniqueName': (u'alljoyn_proxybusobject_getuniquename',
                                    (u'const char *', C.c_char_p),
                                    ((u'alljoyn_proxybusobject', ProxyBusHandle),)),
                 u'ImplementsInterface': (u'alljoyn_proxybusobject_implementsinterface',
                                          (u'int', C.c_int),
                                          ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                              (u'const char *', C.c_char_p))),
                 u'IntrospectRemoteObject': (u'alljoyn_proxybusobject_introspectremoteobject',
                                             (u'QStatus', C.c_uint),
                                             ((u'alljoyn_proxybusobject', ProxyBusHandle),)),
                 u'IntrospectRemoteObjectASync': (u'alljoyn_proxybusobject_introspectremoteobjectasync',
                                                  (u'QStatus', C.c_uint),
                                                  ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                                      (u'alljoyn_proxybusobject_listener_introspectcb_ptr',
                                                       POINTER(ProxyBusObjectListenerIntroSpecTCBFuncType)),
                                                      (u'void *', C.c_void_p))),
                 u'IsSecure': (u'alljoyn_proxybusobject_issecure',
                               (u'int', C.c_int),
                               ((u'alljoyn_proxybusobject', ProxyBusHandle),)),
                 u'IsValid': (u'alljoyn_proxybusobject_isvalid',
                              (u'int', C.c_int),
                              ((u'alljoyn_proxybusobject', ProxyBusHandle),)),

                 u'MethodCall': (u'alljoyn_proxybusobject_methodcall',
                                 (u'QStatus', C.c_uint),
                                 ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                     (u'const char *', C.c_char_p),  # iface_name
                                     (u'const char *', C.c_char_p),  # method_name
                                     (u'const void*', MsgArg.MsgArgHandle,  # args
                                      (u'int', C.c_int),        # number arguments
                                      (u'void*', Message.MessageHandle),   # reply_msg
                                      (u'int', C.c_int),    # timeout
                                      (u'int', C.c_int)))),  # flags

                 u'MethodCallAsync': (u'alljoyn_proxybusobject_methodcallasync',
                                      (u'QStatus', C.c_uint),
                                      ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                          (u'const char *', C.c_char_p),
                                          (u'const char *', C.c_char_p),
                                          (u'int', C.c_int),
                                          (u'const int', C.c_int),
                                          (u'int', C.c_int),
                                          (u'void *', C.c_void_p),
                                          (u'int', C.c_int),
                                          (u'int', C.c_int))),
                 u'MethodCallAsyncMember': (u'alljoyn_proxybusobject_methodcallasync_member',
                                            (u'QStatus', C.c_uint),
                                            ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                                (u'const int', C.c_int),
                                                (u'int', C.c_int),
                                                (u'const int', C.c_int),
                                                (u'int', C.c_int),
                                                (u'void *', C.c_void_p),
                                                (u'int', C.c_int),
                                                (u'int', C.c_int))),
                 u'MethodCallMember': (u'alljoyn_proxybusobject_methodcall_member',
                                       (u'QStatus', C.c_uint),
                                       ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                           (u'const int', C.c_int),
                                           (u'const int', C.c_int),
                                           (u'int', C.c_int),
                                           (u'int', C.c_int),
                                           (u'int', C.c_int),
                                           (u'int', C.c_int))),


                 u'MethodCallMemberNoReply': (u'alljoyn_proxybusobject_methodcall_member_noreply',
                                              (u'QStatus', C.c_uint),
                                              ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                                  (u'const int', C.c_int),
                                                  (u'const int', C.c_int),
                                                  (u'int', C.c_int),
                                                  (u'int', C.c_int))),

                 u'MethodCallNoReply': (u'alljoyn_proxybusobject_methodcall_noreply',
                                        (u'QStatus', C.c_uint),
                                        ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                            (u'const char *', C.c_char_p),
                                            (u'const char *', C.c_char_p),
                                            (u'const void*', MsgArg.MsgArgHandle),
                                            (u'int', C.c_size_t),
                                            (u'uint', C.c_uint))),

                 u'ParseXml': (u'alljoyn_proxybusobject_parsexml',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                   (u'const char *', C.c_char_p),
                                   (u'const char *', C.c_char_p))),

                 u'RegisterPropertiesChangedListener': (u'alljoyn_proxybusobject_registerpropertieschangedlistener',
                                                        (u'QStatus', C.c_uint),
                                                        ((u'alljoyn_proxybusobject',
                                                          C.c_void_p),
                                                            (u'const char *', C.c_char_p),
                                                            (u'const char **',
                                                             POINTER(C.c_char_p)),
                                                            (u'int', C.c_int),
                                                            (u'alljoyn_proxybusobject_listener_propertieschanged_ptr',
                                                             POINTER(ProxyBusObjectListenerPropertiesChangedFuncType)),
                                                            (u'void *', C.c_void_p))),
                 u'RemoveChild': (u'alljoyn_proxybusobject_removechild',
                                  (u'QStatus', C.c_uint),
                                  ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                      (u'const char *', C.c_char_p))),
                 u'SecureConnection': (u'alljoyn_proxybusobject_secureconnection',
                                       (u'QStatus', C.c_uint),
                                       ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                           (u'int', C.c_int))),
                 u'SecureConnectionAsYNC': (u'alljoyn_proxybusobject_secureconnectionasync',
                                            (u'QStatus', C.c_uint),
                                            ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                                (u'int', C.c_int))),
                 u'SetProperty': (u'alljoyn_proxybusobject_setproperty',
                                  (u'QStatus', C.c_uint),
                                  ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                      (u'const char *', C.c_char_p),
                                      (u'const char *', C.c_char_p),
                                      (u'int', C.c_int))),
                 u'SetPropertyAsYNC': (u'alljoyn_proxybusobject_setpropertyasync',
                                       (u'QStatus', C.c_uint),
                                       ((u'alljoyn_proxybusobject', ProxyBusHandle),
                                           (u'const char *', C.c_char_p),
                                           (u'const char *', C.c_char_p),
                                           (u'int', C.c_int),
                                           (u'alljoyn_proxybusobject_listener_setpropertycb_ptr',
                                            POINTER(ProxyBusObjectListenerSetPropertyCBFuncType)),
                                           (u'int', C.c_int),
                                           (u'void *', C.c_void_p))),

                 u'UnregisterPropertiesChangedListener': (u'alljoyn_proxybusobject_unregisterpropertieschangedlistener',
                                                          (u'QStatus', C.c_uint),
                                                          ((u'alljoyn_proxybusobject',
                                                            C.c_void_p),
                                                              (u'const char *', C.c_char_p),
                                                              (u'alljoyn_proxybusobject_listener_propertieschanged_ptr',
                                                               POINTER(ProxyBusObjectListenerPropertiesChangedFuncType))))}

    def __init__(self, bus_attatchment, service, path, session_id):
        super(ProxyBusObject, self).__init__()
        self.handle = self._Create(bus_attatchment.handle, service, path, session_id)  # const char *,const char *,int

    def __del__(self):
        self._Destroy(self.handle)

    # Wrapper Methods

    def Create(self, service, path, sessionId):
        return self._Create(self.handle, service, path, sessionId)  # const char *,const char *,int

    def CreateSecure(self, service, path, sessionId):
        return self._CreateSecure(self.handle, service, path, sessionId)  # const char *,const char *,int

    def Destroy(self):
        return self._Destroy(self.handle)

    def AddInterface(self, iface):
        return self._AddInterface(self.handle, iface.handle)  # const int

    def AddInterfaceByName(self, name):
        return self._AddInterfaceByName(self.handle, name)  # const char *

    def GetChildren(self, children, numChildren):
        return self._GetChildren(self.handle, children, numChildren)  # alljoyn_proxybusobject *,int

    def GetChild(self, path):
        return self._GetChild(self.handle, path)  # const char *

    def AddChild(self, child):
        return self._AddChild(self.handle, child)  # const alljoyn_proxybusobject

    def RemoveChild(self, path):
        return self._RemoveChild(self.handle, path)  # const char *

    def IntrospectRemoteObject(self):
        return self._IntrospectRemoteObject(self.handle)

    def IntrospectRemoteObjectASync(self, callback, context):
        # alljoyn_proxybusobject_listener_introspectcb_ptr,void *
        return self._IntrospectRemoteObjectASync(self.handle, callback, context)

    def GetProperty(self, iface, property, value):
        return self._GetProperty(self.handle, iface, property, value)  # const char *,const char *,int

    def GetPropertyAsync(self, iface, property, callback, timeout, context):
        # const char *,const char *,alljoyn_proxybusobject_listener_getpropertycb_ptr,int,void *
        return self._GetPropertyAsync(self.handle, iface, property, callback, timeout, context)

    def GetAllProperties(self, iface, values):
        return self._GetAllProperties(self.handle, iface, values)  # const char *,int

    def GetAllPropertiesAsYNC(self, iface, callback, timeout, context):
        # const char *,alljoyn_proxybusobject_listener_getallpropertiescb_ptr,int,void *
        return self._GetAllPropertiesAsYNC(self.handle, iface, callback, timeout, context)

    def SetProperty(self, iface, property, value):
        return self._SetProperty(self.handle, iface, property, value)  # const char *,const char *,int

    def RegisterPropertiesChangedListener(self, iface, properties, numProperties, callback, context):
        # const char *,const char **,int,alljoyn_proxybusobject_listener_propertieschanged_ptr,void *
        return self._RegisterPropertiesChangedListener(self.handle, iface, properties, numProperties, callback, context)

    def UnregisterPropertiesChangedListener(self, iface, callback):
        # const char *,alljoyn_proxybusobject_listener_propertieschanged_ptr
        return self._UnregisterPropertiesChangedListener(self.handle, iface, callback)

    def SetPropertyAsYNC(self, iface, property, value, callback, timeout, context):
        # const char *,const char
        return self._SetPropertyAsYNC(self.handle, iface, property, value, callback, timeout, context)

    def MethodCall(self, ifaceName, methodName, args, numArgs, replyMsg, timeout, flags):
        # array = None
        # if len(args) > 0:
        #     array = (MsgArg.MsgArgHandle * len(args))()
        #     array[:] = [a.handle for a in args]
        #     print "array", array
        # reply_handle = replyMsg or None
        args_handle = args.handle if args else None
        reply_handle = replyMsg.handle if replyMsg else None
        # const char *,const char *,const int,int,int,int,int
        return self._MethodCall(self.handle, ifaceName, methodName, args_handle, numArgs, reply_handle, timeout, flags)

    def MethodCallMember(self, method, args, numArgs, replyMsg, timeout, flags):
        # const int,const int,int,int,int,int
        return self._MethodCallMember(self.handle, method, args, numArgs, replyMsg, timeout, flags)

    def MethodCallNoReply(self, ifaceName, methodName, args, numArgs, flags):
        args_handle = args.handle or None
        return self._MethodCallNoReply(self.handle, ifaceName, methodName, args_handle, numArgs, flags)

    def MethodCallMemberNoReply(self, method, args, numArgs, flags):
        return self._MethodCallMemberNoReply(self.handle, method, args, numArgs, flags)  # const int,const int,int,int

    def MethodCallAsync(self, ifaceName, methodName, replyFunc, args, numArgs, context, timeout, flags):
        # const char *,const char *,int,const int,int,void *,int,int
        return self._MethodCallAsync(self.handle, ifaceName, methodName, replyFunc, args, numArgs, context, timeout, flags)

    def MethodCallAsyncMember(self, method, replyFunc, args, numArgs, context, timeout, flags):
        # const int,int,const int,int,void *,int,int
        return self._MethodCallAsyncMember(self.handle, method, replyFunc, args, numArgs, context, timeout, flags)

    def ParseXml(self, xml, identifier):
        return self._ParseXml(self.handle, xml, identifier)  # const char *,const char *

    def SecureConnection(self, forceAuth):
        return self._SecureConnection(self.handle, forceAuth)  # int

    def SecureConnectionAsYNC(self, forceAuth):
        return self._SecureConnectionAsYNC(self.handle, forceAuth)  # int

    def GetInterface(self, iface):
        return InterfaceDescription.InterfaceDescription(self._GetInterface(self.handle, iface))  # const char *

    def GetInterfaces(self, ifaces, numIfaces):
        return self._GetInterfaces(self.handle, ifaces, numIfaces)  # const int *,int

    def GetPath(self):
        return self._GetPath(self.handle)

    def GetServiceName(self):
        return self._GetServiceName(self.handle)

    def GetUniqueName(self):
        return self._GetUniqueName(self.handle)

    def GetSessionId(self):
        return self._GetSessionId(self.handle)

    def ImplementsInterface(self, iface):
        return self._ImplementsInterface(self.handle, iface)  # const char *

    def Copy(self):
        return self._Copy(self.handle)

    def IsValid(self):
        return self._IsValid(self.handle)

    def IsSecure(self):
        return self._IsSecure(self.handle)

    def EnablePropertyCaching(self):
        return self._EnablePropertyCaching(self.handle)


ProxyBusObject.bind_functions_to_cls()
