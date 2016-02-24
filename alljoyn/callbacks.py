#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes as C
import os, sys
from types import IntType
from constants import *
from ctypes import POINTER

from sys import platform as _platform

if _platform == 'win32':
    DLL_CALLCONV = C.WINFUNCTYPE
else:
    DLL_CALLCONV = C.CFUNCTYPE


if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE

VOID    = C.c_void_p
INT     = C.c_int
UINT32  = C.c_uint32
BOOL    = C.c_long
BYTE    = C.c_ubyte
WORD    = C.c_ushort
DWORD   = C.c_ulong
LONG    = C.c_long



#typedef void (AJ_CALL * alljoyn_buslistener_listener_registered_ptr)(const void* context, alljoyn_busattachment bus);
#typedef void (AJ_CALL * alljoyn_buslistener_listener_unregistered_ptr)(const void* context);
#typedef void (AJ_CALL * alljoyn_buslistener_found_advertised_name_ptr)(const void* context, const char* name, alljoyn_transportmask transport, const char* namePrefix);
#typedef void (AJ_CALL * alljoyn_buslistener_lost_advertised_name_ptr)(const void* context, const char* name, alljoyn_transportmask transport, const char* namePrefix);
#typedef void (AJ_CALL * alljoyn_buslistener_name_owner_changed_ptr)(const void* context, const char* busName, const char* previousOwner, const char* newOwner);
#typedef void (AJ_CALL * alljoyn_buslistener_bus_stopping_ptr)(const void* context);
#typedef void (AJ_CALL * alljoyn_buslistener_bus_disconnected_ptr)(const void* context);
#typedef void (AJ_CALL * alljoyn_buslistener_bus_prop_changed_ptr)(const void* context, const char* prop_name, alljoyn_msgarg prop_value);





#class BusListenerCallbacks(C.Structure):
    #_fields_ = [("BusListenerRegistered",
                    #CallbackType(None, C.c_void_p, C.c_void_p)),                 # const void* context, alljoyn_busattachment bus
                #("BusListenerUnRegistered",
                    #CallbackType(None, C.c_void_p)),                             # const void* context
                #("BusListenerFoundAdvertisedName", 
                    #CallbackType(None, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p)), # const void* context, const char* name, alljoyn_transportmask transport, const char* namePrefix
                #("BusListenerLostAdvertisedName", 
                    #CallbackType(None, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p)), # const void* context, const char* name, alljoyn_transportmask transport, const char* namePrefix
                #("BusListenerNameOwnerChanged", 
                    #CallbackType(None, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p)), # const void* context, const char* busName, const char* previousOwner, const char* newOwner
                #("BusListenerBusStopping", 
                    #CallbackType(None, C.c_void_p)),                                     # const void* context
                #("BusListenerBusDisconnected", 
                    #CallbackType(None, C.c_void_p)),                                     # const void* context
                #("BusListenerBusPropertyChanged", 
                    #CallbackType(None, C.c_void_p, C.c_void_p, C.c_void_p))             # const void* context, const char* prop_name, alljoyn_msgarg prop_value
               #]


#class BusListenerCallbacks(C.Structure):
    #_fields_ = [("BusListenerRegistered",
                    #POINTER(CallbackType(None, C.c_void_p, C.c_void_p))),                 # const void* context, alljoyn_busattachment bus
                #("BusListenerUnRegistered",
                    #POINTER(CallbackType(None, C.c_void_p))),                             # const void* context
                #("BusListenerFoundAdvertisedName", 
                    #POINTER(CallbackType(None, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p))), # const void* context, const char* name, alljoyn_transportmask transport, const char* namePrefix
                #("BusListenerLostAdvertisedName", 
                    #POINTER(CallbackType(None, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p))), # const void* context, const char* name, alljoyn_transportmask transport, const char* namePrefix
                #("BusListenerNameOwnerChanged", 
                    #POINTER(CallbackType(None, C.c_void_p, C.c_void_p, C.c_void_p, C.c_void_p))), # const void* context, const char* busName, const char* previousOwner, const char* newOwner
                #("BusListenerBusStopping", 
                    #POINTER(CallbackType(None, C.c_void_p))),                                     # const void* context
                #("BusListenerBusDisconnected", 
                    #POINTER(CallbackType(None, C.c_void_p))),                                     # const void* context
                #("BusListenerBusPropertyChanged", 
                    #POINTER(CallbackType(None, C.c_void_p, C.c_void_p, C.c_void_p)))             # const void* context, const char* prop_name, alljoyn_msgarg prop_value
               #]



#typedef struct {
#    
#    
#    alljoyn_buslistener_listener_registered_ptr listener_registered;
#
#    alljoyn_buslistener_listener_unregistered_ptr listener_unregistered;
#
#    alljoyn_buslistener_found_advertised_name_ptr found_advertised_name;
#
#    alljoyn_buslistener_lost_advertised_name_ptr lost_advertised_name;
#
#    alljoyn_buslistener_name_owner_changed_ptr name_owner_changed;
#
#    alljoyn_buslistener_bus_stopping_ptr bus_stopping;
#
#    alljoyn_buslistener_bus_disconnected_ptr bus_disconnected;
#
#    alljoyn_buslistener_bus_prop_changed_ptr property_changed;
#    
#} alljoyn_buslistener_callbacks;



#BusattachmentCreateinterface

#class InterfaceDescription(Structure):
#     pass

"""

class BusAttachment(Structure):
     pass
     
     

'alljoyn_busattachment': 'POINTER(BusAttachment)',
                             'alljoyn_proxybusobject': 'C.c_void_p',
                             'alljoyn_aboutdata': 'C.c_void_p',
                             'alljoyn_aboutdatalistener': 'C.c_void_p',
                             'alljoyn_abouticonproxy': 'C.c_void_p',
                             'alljoyn_authlistener': 'C.c_void_p',
                             'const alljoyn_interfacedescription': 'C.c_void_p',
                             'alljoyn_sessionid': 'C.c_uint32',
                             'alljoyn_msgarg': 'C.c_void_p',
                             'alljoyn_aboutobjectdescription': 'C.c_void_p',
                             'alljoyn_abouticonobj': 'C.c_void_p',
                             'alljoyn_aboutlistener': 'C.c_void_p',
                             'alljoyn_buslistener': 'C.c_void_p',
                             'alljoyn_busobject': 'C.c_void_p',
                             'const alljoyn_proxybusobject': 'C.c_void_p',
                             'alljoyn_abouticon': 'C.c_void_p',
                             'alljoyn_aboutobj': 'C.c_void_p',
                             'alljoyn_aboutproxy': 'C.c_void_p',
                             'alljoyn_credentials': 'C.c_void_p',
                             'alljoyn_pinglistener': 'C.c_void_p',
                             'alljoyn_sessionopts': 'C.c_void_p',
                             'alljoyn_transportmask': 'C.c_void_p',
                             'alljoyn_sessionlistener': 'C.c_void_p',
                             'alljoyn_sessionportlistener': 'C.c_void_p',
                             'const alljoyn_busattachment': 'C.c_void_p',
                             'alljoyn_observerlistener': 'C.c_void_p',
                             'alljoyn_observer': 'C.c_void_p',
                             'alljoyn_messagetype': 'C.c_uint32',
                             'alljoyn_message': 'C.c_void_p',
                             'alljoyn_typeid': 'C.c_int32',
                             'alljoyn_autopinger': 'C.c_int32',
                              'alljoyn_interfacedescription_securitypolicy': 'C.c_int32',



#alljoyn_sessionlistener_callbacks
class SessionListenerCallbacks(Structure):
    _fields_ = [("SessionListenerSessionLost",
                    CallbackType(CO.VOID, ALLJOYN_SESSION_ID, SessionLostReasonEnum.CTYPE())),     # context, session_id, reason     #   alljoyn_sessionlistener_sessionlost_ptr session_lost;
                ("SessionListenerMemberAdded",
                    CallbackType(CO.VOID, ALLJOYN_SESSION_ID, C.c_char_p))     # context, session_id, unique_name      #   alljoyn_sessionlistener_sessionmemberadded_ptr session_member_added;
                ("SessionListenerMemberRemoved", 
                    CallbackType(CO.VOID, ALLJOYN_SESSION_ID, C.c_char_p))        # context,  ALLJOYN_SESSION_ID (alljoyn_sessionid), unique_name  #   alljoyn_sessionlistener_sessionmemberremoved_ptr session_member_removed;






class SessionListenerCallbacks(Structure):
    _fields_ = [("SessionListenerSessionLost",
                    CallbackType(CO.VOID, ALLJOYN_SESSION_ID, SessionLostReasonEnum.CTYPE())),     # context, session_id, reason     #   alljoyn_sessionlistener_sessionlost_ptr session_lost;
                ("SessionListenerMemberAdded",
                    CallbackType(CO.VOID, ALLJOYN_SESSION_ID, C.c_char_p))     # context, session_id, unique_name      #   alljoyn_sessionlistener_sessionmemberadded_ptr session_member_added;
                ("SessionListenerMemberRemoved", 
                    CallbackType(CO.VOID, ALLJOYN_SESSION_ID, C.c_char_p))        # context,  ALLJOYN_SESSION_ID (alljoyn_sessionid), unique_name  #   alljoyn_sessionlistener_sessionmemberremoved_ptr session_member_removed;



class SessionListenerCallbacks(Structure):
    _fields_ = [("SessionListenerSessionLost",
                    CallbackType(CO.VOID, ALLJOYN_SESSION_ID, SessionLostReasonEnum.CTYPE())),     # context, session_id, reason     #   alljoyn_sessionlistener_sessionlost_ptr session_lost;
                ("SessionListenerMemberAdded",
                    CallbackType(CO.VOID, ALLJOYN_SESSION_ID, C.c_char_p))     # context, session_id, unique_name      #   alljoyn_sessionlistener_sessionmemberadded_ptr session_member_added;
                ("SessionListenerMemberRemoved", 
                    CallbackType(CO.VOID, ALLJOYN_SESSION_ID, C.c_char_p))        # context,  ALLJOYN_SESSION_ID (alljoyn_sessionid), unique_name  #   alljoyn_sessionlistener_sessionmemberremoved_ptr session_member_removed;



class SessionListenerCallbacks(Structure):
    _fields_ = [("SessionListenerSessionLost",
                    CallbackType(CO.VOID, ALLJOYN_SESSION_ID, SessionLostReasonEnum.CTYPE())),     # context, session_id, reason     #   alljoyn_sessionlistener_sessionlost_ptr session_lost;
                ("SessionListenerMemberAdded",
                    CallbackType(CO.VOID, ALLJOYN_SESSION_ID, C.c_char_p))     # context, session_id, unique_name      #   alljoyn_sessionlistener_sessionmemberadded_ptr session_member_added;
                ("SessionListenerMemberRemoved", 
                    CallbackType(CO.VOID, ALLJOYN_SESSION_ID, C.c_char_p))        # context,  ALLJOYN_SESSION_ID (alljoyn_sessionid), unique_name  #   alljoyn_sessionlistener_sessionmemberremoved_ptr session_member_removed;




typedef struct {

    alljoyn_aboutdatalistener_getaboutdata_ptr about_datalistener_getaboutdata;
    
    alljoyn_aboutdatalistener_getannouncedaboutdata_ptr about_datalistener_getannouncedaboutdata;
} alljoyn_aboutdatalistener_callbacks;



typedef struct {
    
    alljoyn_about_announced_ptr about_listener_announced;
} alljoyn_aboutlistener_callback;


typedef struct {

    alljoyn_authlistener_requestcredentials_ptr request_credentials;

    alljoyn_authlistener_verifycredentials_ptr verify_credentials;

    alljoyn_authlistener_securityviolation_ptr security_violation;

    alljoyn_authlistener_authenticationcomplete_ptr authentication_complete;
} alljoyn_authlistener_callbacks;


typedef struct {

    alljoyn_authlistener_requestcredentialsasync_ptr request_credentials;

    alljoyn_authlistener_verifycredentialsasync_ptr verify_credentials;

    alljoyn_authlistener_securityviolation_ptr security_violation;

    alljoyn_authlistener_authenticationcomplete_ptr authentication_complete;

} alljoyn_authlistenerasync_callbacks;


typedef struct {

    alljoyn_autopinger_destination_found_ptr destination_found;

    alljoyn_autopinger_destination_lost_ptr destination_lost;
} alljoyn_pinglistener_callback;




typedef struct {

    alljoyn_busobject_prop_get_ptr property_get;

    alljoyn_busobject_prop_set_ptr property_set;

    alljoyn_busobject_object_registration_ptr object_registered;

    alljoyn_busobject_object_registration_ptr object_unregistered;
} alljoyn_busobject_callbacks;


typedef struct {
    const alljoyn_interfacedescription_member* member;
    alljoyn_messagereceiver_methodhandler_ptr method_handler;
} alljoyn_busobject_methodentry;



typedef struct {
    alljoyn_interfacedescription iface;
    alljoyn_messagetype memberType;
    const char* name;
    const char* signature;
    const char* returnSignature;
    const char* argNames;

    const void* internal_member;
} alljoyn_interfacedescription_member;


typedef struct {
    const char* name;
    const char* signature;
    uint8_t access;

    const void* internal_property;
} alljoyn_interfacedescription_property;


typedef struct {

    alljoyn_keystorelistener_loadrequest_ptr load_request;

    alljoyn_keystorelistener_storerequest_ptr store_request;
} alljoyn_keystorelistener_callbacks;



typedef struct {

    alljoyn_observer_object_discovered_ptr object_discovered;

    alljoyn_observer_object_lost_ptr object_lost;
    alljoyn_observer_object_lost_ptr object_lost;
} alljoyn_observerlistener_callback;


typedef struct {

    alljoyn_permissionconfigurationlistener_factoryreset_ptr factory_reset;


    alljoyn_permissionconfigurationlistener_policychanged_ptr policy_changed;
} alljoyn_permissionconfigurationlistener_callbacks;




typedef struct {

    alljoyn_sessionportlistener_acceptsessionjoiner_ptr accept_session_joiner;

    alljoyn_sessionportlistener_sessionjoined_ptr session_joined;
} alljoyn_sessionportlistener_callbacks;


"""










#class AllJoynCallbacks:
#
#
#    # alljoyn_sessionlistener_create  returns  alljoyn_sessionlistener
#    def SessionListenerCreate(callbacks, context)  # const alljoyn_sessionlistener_callbacks* callbacks ,const void* context
#        self.__lib.alljoyn_message_parseargs.restype = C.c_uint
#        self.__lib.alljoyn_message_parseargs.argtypes = [POINTER(SessionListenerCallbacks), C.c_char_p]
#        return alljoyn_sessionlistener_create(callbacks, context)
        
    
