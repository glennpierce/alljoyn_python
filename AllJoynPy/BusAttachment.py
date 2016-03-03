import sys
import ctypes as C
from ctypes import POINTER
from . import AllJoynMeta, AllJoynObject
# Wrapper for file BusAttachment.h

# Typedefs
# struct _alljoyn_busattachment_handle * alljoyn_busattachment
# void (*)(int, int, const int, void *) alljoyn_busattachment_joinsessioncb_ptr
# void (*)(int, int, void *) alljoyn_busattachment_setlinktimeoutcb_ptr

if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE

BusAttachmentSetLinkTimeoutCBFuncType = CallbackType(None, C.c_int, C.c_int, C.c_void_p)  # status timeout context
BusAttachmentJoinSessionCBFuncType = CallbackType(
    None, C.c_int, C.c_int, C.c_int, C.c_void_p)  # status sessionId opts context


class BusAttachment(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'AddLogOnEntry': (u'alljoyn_busattachment_addlogonentry',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_busattachment', C.c_void_p),
                                        (u'const char *', C.c_char_p),
                                        (u'const char *', C.c_char_p),
                                        (u'const char *', C.c_char_p))),
                 u'AddMatch': (u'alljoyn_busattachment_addmatch',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_busattachment', C.c_void_p),
                                   (u'const char *', C.c_char_p))),
                 u'AdvertiseName': (u'alljoyn_busattachment_advertisename',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_busattachment', C.c_void_p),
                                        (u'const char *', C.c_char_p),
                                        (u'int', C.c_int))),
                 u'BindSessionPort': (u'alljoyn_busattachment_bindsessionport',
                                      (u'QStatus', C.c_uint),
                                      ((u'alljoyn_busattachment', C.c_void_p),
                                          (u'int *', POINTER(C.c_int)),
                                          (u'const int', C.c_int),
                                          (u'int', C.c_int))),
                 u'CancelAdvertiseName': (u'alljoyn_busattachment_canceladvertisename',
                                          (u'QStatus', C.c_uint),
                                          ((u'alljoyn_busattachment', C.c_void_p),
                                              (u'const char *', C.c_char_p),
                                              (u'int', C.c_int))),
                 u'CancelFindAdvertisedName': (u'alljoyn_busattachment_cancelfindadvertisedname',
                                               (u'QStatus', C.c_uint),
                                               ((u'alljoyn_busattachment', C.c_void_p),
                                                   (u'const char *', C.c_char_p))),
                 u'CancelFindAdvertisedNameByTransport': (u'alljoyn_busattachment_cancelfindadvertisednamebytransport',
                                                          (u'QStatus', C.c_uint),
                                                          ((u'alljoyn_busattachment',
                                                            C.c_void_p),
                                                              (u'const char *', C.c_char_p),
                                                              (u'int', C.c_int))),
                 u'CancelWhoImplementsInterface': (u'alljoyn_busattachment_cancelwhoimplements_interface',
                                                   (u'QStatus', C.c_uint),
                                                   ((u'alljoyn_busattachment', C.c_void_p),
                                                       (u'const char *', C.c_char_p))),
                 u'CancelWhoImplementsInterfaces': (u'alljoyn_busattachment_cancelwhoimplements_interfaces',
                                                    (u'QStatus', C.c_uint),
                                                    ((u'alljoyn_busattachment',
                                                      C.c_void_p),
                                                        (u'const char **',
                                                         POINTER(C.c_char_p)),
                                                        (u'int', C.c_int))),
                 u'ClearKeys': (u'alljoyn_busattachment_clearkeys',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_busattachment', C.c_void_p),
                                    (u'const char *', C.c_char_p))),
                 u'ClearKeysTore': (u'alljoyn_busattachment_clearkeystore',
                                    (u'void', None),
                                    ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'Connect': (u'alljoyn_busattachment_connect',
                              (u'QStatus', C.c_uint),
                              ((u'alljoyn_busattachment', C.c_void_p),
                                  (u'const char *', C.c_char_p))),
                 u'Create': (u'alljoyn_busattachment_create',
                             (u'alljoyn_busattachment', C.c_void_p),
                             ((u'const char *', C.c_char_p), (u'int', C.c_int))),
                 u'CreateConcurrency': (u'alljoyn_busattachment_create_concurrency',
                                        (u'alljoyn_busattachment', C.c_void_p),
                                        ((u'const char *', C.c_char_p),
                                            (u'int', C.c_int),
                                            (u'int', C.c_int))),
                 u'CreateInterface': (u'alljoyn_busattachment_createinterface',
                                      (u'QStatus', C.c_uint),
                                      ((u'alljoyn_busattachment', C.c_void_p),
                                          (u'const char *', C.c_char_p),
                                          (u'int *', POINTER(C.c_int)))),
                 u'CreateInterfaceSecure': (u'alljoyn_busattachment_createinterface_secure',
                                            (u'QStatus', C.c_uint),
                                            ((u'alljoyn_busattachment', C.c_void_p),
                                                (u'const char *', C.c_char_p),
                                                (u'int *', POINTER(C.c_int)),
                                                (u'int', C.c_int))),
                 u'CreateInterfacesFromXML': (u'alljoyn_busattachment_createinterfacesfromxml',
                                              (u'QStatus', C.c_uint),
                                              ((u'alljoyn_busattachment', C.c_void_p),
                                                  (u'const char *', C.c_char_p))),
                 u'DeleteInterface': (u'alljoyn_busattachment_deleteinterface',
                                      (u'QStatus', C.c_uint),
                                      ((u'alljoyn_busattachment', C.c_void_p),
                                          (u'int', C.c_int))),
                 u'Destroy': (u'alljoyn_busattachment_destroy',
                              (u'void', None),
                              ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'Disconnect': (u'alljoyn_busattachment_disconnect',
                                 (u'QStatus', C.c_uint),
                                 ((u'alljoyn_busattachment', C.c_void_p),
                                     (u'const char *', C.c_char_p))),
                 u'EnableConcurrentCallbacks': (u'alljoyn_busattachment_enableconcurrentcallbacks',
                                                (u'void', None),
                                                ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'EnablePeerSecurity': (u'alljoyn_busattachment_enablepeersecurity',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_busattachment', C.c_void_p),
                                             (u'const char *', C.c_char_p),
                                             (u'int', C.c_int),
                                             (u'const char *', C.c_char_p),
                                             (u'int', C.c_int))),

                 u'EnablePeerSecurityWithPermissionConfigurationListener':
                 (u'alljoyn_busattachment_enablepeersecuritywithpermissionconfigurationlistener',
                  (u'QStatus',
                   C.c_uint),
                  ((u'alljoyn_busattachment',
                    C.c_void_p),
                   (u'const char *',
                    C.c_char_p),
                   (u'int',
                    C.c_int),
                   (u'const char *',
                    C.c_char_p),
                   (u'int',
                    C.c_int),
                   (u'int',
                    C.c_int))),

                 u'FindAdvertisedName': (u'alljoyn_busattachment_findadvertisedname',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_busattachment', C.c_void_p),
                                             (u'const char *', C.c_char_p))),
                 u'FindAdvertisedNameByTransport': (u'alljoyn_busattachment_findadvertisednamebytransport',
                                                    (u'QStatus', C.c_uint),
                                                    ((u'alljoyn_busattachment',
                                                      C.c_void_p),
                                                        (u'const char *', C.c_char_p),
                                                        (u'int', C.c_int))),
                 u'GetAllJoyNDEBUGOBJ': (u'alljoyn_busattachment_getalljoyndebugobj',
                                         (u'const int', C.c_int),
                                         ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'GetAllJoyNPROXYOBJ': (u'alljoyn_busattachment_getalljoynproxyobj',
                                         (u'const int', C.c_int),
                                         ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'GetConcurrency': (u'alljoyn_busattachment_getconcurrency',
                                     (u'int', C.c_int),
                                     ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'GetConnectSpec': (u'alljoyn_busattachment_getconnectspec',
                                     (u'const char *', C.c_char_p),
                                     ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'GetDBUSPROXYOBJ': (u'alljoyn_busattachment_getdbusproxyobj',
                                      (u'const int', C.c_int),
                                      ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'GetGlobalGUIDSTRING': (u'alljoyn_busattachment_getglobalguidstring',
                                          (u'const char *', C.c_char_p),
                                          ((u'const alljoyn_busattachment', C.c_void_p),)),
                 u'GetInterface': (u'alljoyn_busattachment_getinterface',
                                   (u'const int', C.c_int),
                                   ((u'alljoyn_busattachment', C.c_void_p),
                                       (u'const char *', C.c_char_p))),
                 u'GetInterfaces': (u'alljoyn_busattachment_getinterfaces',
                                    (u'int', C.c_int),
                                    ((u'const alljoyn_busattachment', C.c_void_p),
                                        (u'const int *', POINTER(C.c_int)),
                                        (u'int', C.c_int))),
                 u'GetKeyExpiration': (u'alljoyn_busattachment_getkeyexpiration',
                                       (u'QStatus', C.c_uint),
                                       ((u'alljoyn_busattachment', C.c_void_p),
                                           (u'const char *', C.c_char_p),
                                           (u'int *', POINTER(C.c_int)))),
                 u'GetPeerGUID': (u'alljoyn_busattachment_getpeerguid',
                                  (u'QStatus', C.c_uint),
                                  ((u'alljoyn_busattachment', C.c_void_p),
                                      (u'const char *', C.c_char_p),
                                      (u'char *', C.c_char_p),
                                      (u'int *', POINTER(C.c_int)))),
                 u'GetTimesTamp': (u'alljoyn_busattachment_gettimestamp',
                                   (u'int', C.c_int),
                                   ()),
                 u'GetUniqueName': (u'alljoyn_busattachment_getuniquename',
                                    (u'const char *', C.c_char_p),
                                    ((u'const alljoyn_busattachment', C.c_void_p),)),
                 u'IsConnected': (u'alljoyn_busattachment_isconnected',
                                  (u'int', C.c_int),
                                  ((u'const alljoyn_busattachment', C.c_void_p),)),
                 u'IsPeerSecurityEnabled': (u'alljoyn_busattachment_ispeersecurityenabled',
                                            (u'int', C.c_int),
                                            ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'IsStarted': (u'alljoyn_busattachment_isstarted',
                                (u'int', C.c_int),
                                ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'IsStopping': (u'alljoyn_busattachment_isstopping',
                                 (u'int', C.c_int),
                                 ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'Join': (u'alljoyn_busattachment_join',
                           (u'QStatus', C.c_uint),
                           ((u'alljoyn_busattachment', C.c_void_p),)),

                 #QStatus AJ_CALL alljoyn_busattachment_joinsession(alljoyn_busattachment bus, const char* sessionHost,
                 #alljoyn_sessionport sessionPort, alljoyn_sessionlistener listener,
                 #alljoyn_sessionid* sessionId, alljoyn_sessionopts opts);
                 u'JoinSession': (u'alljoyn_busattachment_joinsession',
                                  (u'QStatus', C.c_uint),
                                  ((u'alljoyn_busattachment', C.c_void_p),
                                      (u'const char *', C.c_char_p),
                                      (u'int', C.c_uint16),
                                      (u'void *', C.c_void_p),
                                      (u'uint *', POINTER(C.c_uint)),
                                      (u'int', C.c_void_p))),
                 u'JoinSessionAsYNC': (u'alljoyn_busattachment_joinsessionasync',
                                       (u'QStatus', C.c_uint),
                                       ((u'alljoyn_busattachment', C.c_void_p),
                                           (u'const char *', C.c_char_p),
                                           (u'int', C.c_int),
                                           (u'int', C.c_int),
                                           (u'const int', C.c_int),
                                           (u'alljoyn_busattachment_joinsessioncb_ptr',
                                            POINTER(BusAttachmentJoinSessionCBFuncType)),
                                           (u'void *', C.c_void_p))),
                 u'LeaveSession': (u'alljoyn_busattachment_leavesession',
                                   (u'QStatus', C.c_uint),
                                   ((u'alljoyn_busattachment', C.c_void_p),
                                       (u'int', C.c_int))),
                 u'NameHasOwner': (u'alljoyn_busattachment_namehasowner',
                                   (u'QStatus', C.c_uint),
                                   ((u'alljoyn_busattachment', C.c_void_p),
                                       (u'const char *', C.c_char_p),
                                       (u'int *', POINTER(C.c_int)))),
                 u'Ping': (u'alljoyn_busattachment_ping',
                           (u'QStatus', C.c_uint),
                           ((u'alljoyn_busattachment', C.c_void_p),
                               (u'const char *', C.c_char_p),
                               (u'int', C.c_int))),
                 u'RegisterAboutListener': (u'alljoyn_busattachment_registeraboutlistener',
                                            (u'void', None),
                                            ((u'alljoyn_busattachment', C.c_void_p),
                                                (u'alljoyn_aboutlistener', C.c_void_p))),
                 u'RegisterBusListener': (u'alljoyn_busattachment_registerbuslistener',
                                          (u'void', None),
                                          ((u'alljoyn_busattachment', C.c_void_p),
                                              (u'int', C.c_int))),
                 u'RegisterBusObject': (u'alljoyn_busattachment_registerbusobject',
                                        (u'QStatus', C.c_uint),
                                        ((u'alljoyn_busattachment', C.c_void_p),
                                            (u'int', C.c_int))),
                 u'RegisterBusObjectSecure': (u'alljoyn_busattachment_registerbusobject_secure',
                                              (u'QStatus', C.c_uint),
                                              ((u'alljoyn_busattachment', C.c_void_p),
                                                  (u'int', C.c_int))),
                 u'RegisterKeysToreListener': (u'alljoyn_busattachment_registerkeystorelistener',
                                               (u'QStatus', C.c_uint),
                                               ((u'alljoyn_busattachment', C.c_void_p),
                                                   (u'int', C.c_int))),
                 u'RegisterSignalHandler': (u'alljoyn_busattachment_registersignalhandler',
                                            (u'QStatus', C.c_uint),
                                            ((u'alljoyn_busattachment', C.c_void_p),
                                                (u'int', C.c_int),
                                                (u'const int', C.c_int),
                                                (u'const char *', C.c_char_p))),
                 u'RegisterSignalHandlerWithRule': (u'alljoyn_busattachment_registersignalhandlerwithrule',
                                                    (u'QStatus', C.c_uint),
                                                    ((u'alljoyn_busattachment',
                                                      C.c_void_p),
                                                        (u'int', C.c_int),
                                                        (u'const int', C.c_int),
                                                        (u'const char *', C.c_char_p))),
                 u'ReleaseName': (u'alljoyn_busattachment_releasename',
                                  (u'QStatus', C.c_uint),
                                  ((u'alljoyn_busattachment', C.c_void_p),
                                      (u'const char *', C.c_char_p))),
                 u'ReloadKeysTore': (u'alljoyn_busattachment_reloadkeystore',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'RemoveMatch': (u'alljoyn_busattachment_removematch',
                                  (u'QStatus', C.c_uint),
                                  ((u'alljoyn_busattachment', C.c_void_p),
                                      (u'const char *', C.c_char_p))),
                 u'RemoveSessionMember': (u'alljoyn_busattachment_removesessionmember',
                                          (u'QStatus', C.c_uint),
                                          ((u'alljoyn_busattachment', C.c_void_p),
                                              (u'int', C.c_int),
                                              (u'const char *', C.c_char_p))),
                 u'RequestName': (u'alljoyn_busattachment_requestname',
                                  (u'QStatus', C.c_uint),
                                  ((u'alljoyn_busattachment', C.c_void_p),
                                      (u'const char *', C.c_char_p),
                                      (u'int', C.c_int))),
                 u'SecureConnection': (u'alljoyn_busattachment_secureconnection',
                                       (u'QStatus', C.c_uint),
                                       ((u'alljoyn_busattachment', C.c_void_p),
                                           (u'const char *', C.c_char_p),
                                           (u'int', C.c_int))),
                 u'SecureConnectionAsYNC': (u'alljoyn_busattachment_secureconnectionasync',
                                            (u'QStatus', C.c_uint),
                                            ((u'alljoyn_busattachment', C.c_void_p),
                                                (u'const char *', C.c_char_p),
                                                (u'int', C.c_int))),
                 u'SetDaemonDebug': (u'alljoyn_busattachment_setdaemondebug',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_busattachment', C.c_void_p),
                                         (u'const char *', C.c_char_p),
                                         (u'int', C.c_int))),
                 u'SetKeyExpiration': (u'alljoyn_busattachment_setkeyexpiration',
                                       (u'QStatus', C.c_uint),
                                       ((u'alljoyn_busattachment', C.c_void_p),
                                           (u'const char *', C.c_char_p),
                                           (u'int', C.c_int))),
                 u'SetLinkTimeout': (u'alljoyn_busattachment_setlinktimeout',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_busattachment', C.c_void_p),
                                         (u'int', C.c_int),
                                         (u'int *', POINTER(C.c_int)))),
                 u'SetLinkTimeoutAsYNC': (u'alljoyn_busattachment_setlinktimeoutasync',
                                          (u'QStatus', C.c_uint),
                                          ((u'alljoyn_busattachment', C.c_void_p),
                                              (u'int', C.c_int),
                                              (u'int', C.c_int),
                                              (u'alljoyn_busattachment_setlinktimeoutcb_ptr',
                                               POINTER(BusAttachmentSetLinkTimeoutCBFuncType)),
                                              (u'void *', C.c_void_p))),
                 u'SetSessionListener': (u'alljoyn_busattachment_setsessionlistener',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_busattachment', C.c_void_p),
                                             (u'int', C.c_int),
                                             (u'int', C.c_int))),
                 u'Start': (u'alljoyn_busattachment_start',
                            (u'QStatus', C.c_uint),
                            ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'Stop': (u'alljoyn_busattachment_stop',
                           (u'QStatus', C.c_uint),
                           ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'UNREGISTERABOUTLISTENER': (u'alljoyn_busattachment_unregisteraboutlistener',
                                              (u'void', None),
                                              ((u'alljoyn_busattachment', C.c_void_p),
                                                  (u'int', C.c_int))),
                 u'UNREGISTERALLABOUTLISTENERS': (u'alljoyn_busattachment_unregisterallaboutlisteners',
                                                  (u'void', None),
                                                  ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'UNREGISTERALLHANDLERS': (u'alljoyn_busattachment_unregisterallhandlers',
                                            (u'QStatus', C.c_uint),
                                            ((u'alljoyn_busattachment', C.c_void_p),)),
                 u'UNREGISTERBUSLISTENER': (u'alljoyn_busattachment_unregisterbuslistener',
                                            (u'void', None),
                                            ((u'alljoyn_busattachment', C.c_void_p),
                                                (u'int', C.c_int))),
                 u'UNREGISTERBUSOBJECT': (u'alljoyn_busattachment_unregisterbusobject',
                                          (u'void', None),
                                          ((u'alljoyn_busattachment', C.c_void_p),
                                              (u'int', C.c_int))),
                 u'UNREGISTERSIGNALHANDLER': (u'alljoyn_busattachment_unregistersignalhandler',
                                              (u'QStatus', C.c_uint),
                                              ((u'alljoyn_busattachment', C.c_void_p),
                                                  (u'int', C.c_int),
                                                  (u'const int', C.c_int),
                                                  (u'const char *', C.c_char_p))),
                 u'UNREGISTERSIGNALHANDLERWITHRULE': (u'alljoyn_busattachment_unregistersignalhandlerwithrule',
                                                      (u'QStatus', C.c_uint),
                                                      ((u'alljoyn_busattachment',
                                                        C.c_void_p),
                                                          (u'int', C.c_int),
                                                          (u'const int', C.c_int),
                                                          (u'const char *', C.c_char_p))),
                 u'UnbindSessionPort': (u'alljoyn_busattachment_unbindsessionport',
                                        (u'QStatus', C.c_uint),
                                        ((u'alljoyn_busattachment', C.c_void_p),
                                            (u'int', C.c_int))),
                 u'WhoImplementsInterface': (u'alljoyn_busattachment_whoimplements_interface',
                                             (u'QStatus', C.c_uint),
                                             ((u'alljoyn_busattachment', C.c_void_p),
                                                 (u'const char *', C.c_char_p))),
                 u'WhoImplementsInterfaces': (u'alljoyn_busattachment_whoimplements_interfaces',
                                              (u'QStatus', C.c_uint),
                                              ((u'alljoyn_busattachment', C.c_void_p),
                                                  (u'const char **', POINTER(C.c_char_p)),
                                                  (u'int', C.c_int)))}

    def __init__(self, application_name, allow_remote_mesages=True):
        super(BusAttachment, self).__init__()
        self.handle = self._Create(application_name, int(allow_remote_mesages))

    def __del__(self):
        self._Destroy(self.handle)

    # Wrapper Methods

    def Create(self, allowRemoteMessages):
        return self._Create(self.handle, allowRemoteMessages)  # int

    def CreateConcurrency(self, allowRemoteMessages, concurrency):
        return self._CreateConcurrency(self.handle, allowRemoteMessages, concurrency)  # int,int

    def Destroy(self):
        return self._Destroy(self.handle)

    def Start(self):
        return self._Start(self.handle)

    def Stop(self):
        return self._Stop(self.handle)

    def Join(self):
        return self._Join(self.handle)

    def GetConcurrency(self):
        return self._GetConcurrency(self.handle)

    def GetConnectSpec(self):
        return self._GetConnectSpec(self.handle)

    def EnableConcurrentCallBacks(self):
        return self._EnableConcurrentCallbacks(self.handle)

    def CreateInterface(self, name, iface):
        return self._CreateInterface(self.handle, name, iface)  # const char *,int *

    def CreateInterfaceSecure(self, name, iface, secPolicy):
        return self._CreateInterfaceSecure(self.handle, name, iface, secPolicy)  # const char *,int *,int

    def Connect(self, connectSpec):
        return self._Connect(self.handle, connectSpec)  # const char *

    def RegisterBusListener(self, listener):
        return self._RegisterBusListener(self.handle, listener)  # int

    def UNREGISTERBUSLISTENER(self, listener):
        return self._UNREGISTERBUSLISTENER(self.handle, listener)  # int

    def FindAdvertisedName(self, namePrefix):
        return self._FindAdvertisedName(self.handle, namePrefix)  # const char *

    def FindAdvertisedNameByTransport(self, namePrefix, transports):
        return self._FindAdvertisedNameByTransport(self.handle, namePrefix, transports)  # const char *,int

    def CancelFindAdvertisedName(self, namePrefix):
        return self._CancelFindAdvertisedName(self.handle, namePrefix)  # const char *

    def CancelFindAdvertisedNameByTransport(self, namePrefix, transports):
        return self._CancelFindAdvertisedNameByTransport(self.handle, namePrefix, transports)  # const char *,int

    def AdvertiseName(self, name, transports):
        return self._AdvertiseName(self.handle, name, transports)  # const char *,int

    def CancelAdvertiseName(self, name, transports):
        return self._CancelAdvertiseName(self.handle, name, transports)  # const char *,int

    def GetInterface(self, name):
        return self._GetInterface(self.handle, name)  # const char *

    #QStatus AJ_CALL alljoyn_busattachment_joinsession(alljoyn_busattachment bus, const char* sessionHost,
                          #alljoyn_sessionport sessionPort, alljoyn_sessionlistener listener,
                          #alljoyn_sessionid* sessionId, alljoyn_sessionopts opts);
    def JoinSession(self, sessionHost, sessionPort, listener, opts):
        # const char *,int,int,int *,int
        session_id = C.c_uint()
        self._JoinSession(self.handle, sessionHost, sessionPort, listener.handle, C.byref(session_id), opts.handle)
        return session_id.value

    def JoinSessionAsYNC(self, sessionHost, sessionPort, listener, opts, callback, context):
        # const char *,int,int,const int,alljoyn_busattachment_joinsessioncb_ptr,void *
        return self._JoinSessionAsYNC(self.handle, sessionHost, sessionPort, listener, opts, callback, context)

    def RegisterBusObject(self, obj):
        return self._RegisterBusObject(self.handle, obj)  # int

    def RegisterBusObjectSecure(self, obj):
        return self._RegisterBusObjectSecure(self.handle, obj)  # int

    def UNREGISTERBUSOBJECT(self, object):
        return self._UNREGISTERBUSOBJECT(self.handle, object)  # int

    def RequestName(self, requestedName, flags):
        return self._RequestName(self.handle, requestedName, flags)  # const char *,int

    def ReleaseName(self, name):
        return self._ReleaseName(self.handle, name)  # const char *

    def BindSessionPort(self, sessionPort, opts, listener):
        return self._BindSessionPort(self.handle, sessionPort, opts, listener)  # int *,const int,int

    def UnbindSessionPort(self, sessionPort):
        return self._UnbindSessionPort(self.handle, sessionPort)  # int

    def EnablePeerSecurity(self, authMechanisms, listener, keyStoreFileName, isShared):
        # const char *,int,const char *,int
        return self._EnablePeerSecurity(self.handle, authMechanisms, listener, keyStoreFileName, isShared)

    def EnablePeerSecurityWithPermissionConfigurationListener(self, authMechanisms, authListener,
                                                              keyStoreFileName, isShared,
                                                              permissionConfigurationListener):
        # const char *,int,const char *,int,int
        return self._EnablePeerSecurityWithPermissionConfigurationListener(self.handle, authMechanisms,
                                                                           authListener, keyStoreFileName,
                                                                           isShared, permissionConfigurationListener)

    def IsPeerSecurityEnabled(self):
        return self._IsPeerSecurityEnabled(self.handle)

    def CreateInterfacesFromXML(self, xml):
        return self._CreateInterfacesFromXML(self.handle, xml)  # const char *

    def GetInterfaces(self, ifaces, numIfaces):
        return self._GetInterfaces(self.handle, ifaces, numIfaces)  # const int *,int

    def DeleteInterface(self, iface):
        return self._DeleteInterface(self.handle, iface)  # int

    def IsStarted(self):
        return self._IsStarted(self.handle)

    def IsStopping(self):
        return self._IsStopping(self.handle)

    def IsConnected(self):
        return self._IsConnected(self.handle)

    def Disconnect(self, unused):
        return self._Disconnect(self.handle, unused)  # const char *

    def GetDBUSPROXYOBJ(self):
        return self._GetDBUSPROXYOBJ(self.handle)

    def GetAllJoyNPROXYOBJ(self):
        return self._GetAllJoyNPROXYOBJ(self.handle)

    def GetAllJoyNDEBUGOBJ(self):
        return self._GetAllJoyNDEBUGOBJ(self.handle)

    def GetUniqueName(self):
        return self._GetUniqueName(self.handle)

    def GetGlobalGUIDSTRING(self):
        return self._GetGlobalGUIDSTRING(self.handle)

    def RegisterSignalHandler(self, signal_handler, member, srcPath):
        return self._RegisterSignalHandler(self.handle, signal_handler, member, srcPath)  # int,const int,const char *

    def RegisterSignalHandlerWithRule(self, signal_handler, member, matchRule):
        # int,const int,const char *
        return self._RegisterSignalHandlerWithRule(self.handle, signal_handler, member, matchRule)

    def UNREGISTERSIGNALHANDLER(self, signal_handler, member, srcPath):
        return self._UNREGISTERSIGNALHANDLER(self.handle, signal_handler, member, srcPath)  # int,const int,const char *

    def UNREGISTERSIGNALHANDLERWITHRULE(self, signal_handler, member, matchRule):
        # int,const int,const char *
        return self._UNREGISTERSIGNALHANDLERWITHRULE(self.handle, signal_handler, member, matchRule)

    def UNREGISTERALLHANDLERS(self):
        return self._UNREGISTERALLHANDLERS(self.handle)

    def RegisterKeysToreListener(self, listener):
        return self._RegisterKeysToreListener(self.handle, listener)  # int

    def ReloadKeysTore(self):
        return self._ReloadKeysTore(self.handle)

    def ClearKeysTore(self):
        return self._ClearKeysTore(self.handle)

    def ClearKeys(self, guid):
        return self._ClearKeys(self.handle, guid)  # const char *

    def SetKeyExpiration(self, guid, timeout):
        return self._SetKeyExpiration(self.handle, guid, timeout)  # const char *,int

    def GetKeyExpiration(self, guid, timeout):
        return self._GetKeyExpiration(self.handle, guid, timeout)  # const char *,int *

    def AddLogOnEntry(self, authMechanism, userName, password):
        # const char *,const char *,const char *
        return self._AddLogOnEntry(self.handle, authMechanism, userName, password)

    def AddMatch(self, rule):
        return self._AddMatch(self.handle, rule)  # const char *

    def RemoveMatch(self, rule):
        return self._RemoveMatch(self.handle, rule)  # const char *

    def SetSessionListener(self, sessionId, listener):
        return self._SetSessionListener(self.handle, sessionId, listener)  # int,int

    def LeaveSession(self, sessionId):
        return self._LeaveSession(self.handle, sessionId)  # int

    def SecureConnection(self, name, forceAuth):
        return self._SecureConnection(self.handle, name, forceAuth)  # const char *,int

    def SecureConnectionAsYNC(self, name, forceAuth):
        return self._SecureConnectionAsYNC(self.handle, name, forceAuth)  # const char *,int

    def RemoveSessionMember(self, sessionId, memberName):
        return self._RemoveSessionMember(self.handle, sessionId, memberName)  # int,const char *

    def SetLinkTimeout(self, sessionid, linkTimeout):
        return self._SetLinkTimeout(self.handle, sessionid, linkTimeout)  # int,int *

    def SetLinkTimeoutAsYNC(self, sessionid, linkTimeout, callback, context):
        # int,int,alljoyn_busattachment_setlinktimeoutcb_ptr,void *
        return self._SetLinkTimeoutAsYNC(self.handle, sessionid, linkTimeout, callback, context)

    def NameHasOwner(self, name, hasOwner):
        return self._NameHasOwner(self.handle, name, hasOwner)  # const char *,int *

    def GetPeerGUID(self, name, guid, guidSz):
        return self._GetPeerGUID(self.handle, name, guid, guidSz)  # const char *,char *,int *

    def SetDaemonDebug(self, module, level):
        return self._SetDaemonDebug(self.handle, module, level)  # const char *,int

    def GetTimesTamp(self):
        return self._GetTimesTamp(self.handle)

    def Ping(self, name, timeout):
        return self._Ping(self.handle, name, timeout)  # const char *,int

    def RegisterAboutListener(self, aboutListener):
        return self._RegisterAboutListener(self.handle, aboutListener.handle)  # alljoyn_aboutlistener

    def UNREGISTERABOUTLISTENER(self, aboutListener):
        return self._UNREGISTERABOUTLISTENER(self.handle, aboutListener)  # int

    def UNREGISTERALLABOUTLISTENERS(self):
        return self._UNREGISTERALLABOUTLISTENERS(self.handle)

    # def WhoImplementsInterfaces(self, implementsInterfaces, numberInterfaces):
    def WhoImplementsInterfaces(self, interfaces):
        array = (C.c_char_p * len(interfaces))()
        array[:] = interfaces
        #lib.external_C(array, len(interfaces))
        # implementsInterfaces, numberInterfaces
        return self._WhoImplementsInterfaces(self.handle, array, len(interfaces))  # const char **,int

    def WhoImplementsInterface(self, implementsInterface):
        return self._WhoImplementsInterface(self.handle, implementsInterface)  # const char *

    def CancelWhoImplementsInterfaces(self, implementsInterfaces, numberInterfaces):
        # const char **,int
        return self._CancelWhoImplementsInterfaces(self.handle, implementsInterfaces, numberInterfaces)

    def CancelWhoImplementsInterface(self, implementsInterface):
        return self._CancelWhoImplementsInterface(self.handle, implementsInterface)  # const char *


BusAttachment.bind_functions_to_cls()
