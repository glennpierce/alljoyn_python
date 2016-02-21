#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes as C
import os, sys
from types import IntType
from enum import Enum, unique

from sys import platform as _platform

if _platform == 'win32':
    DLL_CALLCONV = C.WINFUNCTYPE
else:
    DLL_CALLCONV = C.CFUNCTYPE


"""
Internal types
"""
VOID    = C.c_void_p
INT     = C.c_int
BOOL    = C.c_long
BYTE    = C.c_ubyte
WORD    = C.c_ushort
DWORD   = C.c_ulong
LONG    = C.c_long





"""
alljoyn_aboutdata = C.c_void_p;


typedef struct _alljoyn_aboutdatalistener_handle* alljoyn_aboutdatalistener;


typedef struct _alljoyn_abouticon_handle* alljoyn_abouticon;


typedef struct _alljoyn_abouticonobj_handle* alljoyn_abouticonobj;


typedef struct _alljoyn_abouticonproxy_handle* alljoyn_abouticonproxy;


typedef struct _alljoyn_aboutlistener_handle* alljoyn_aboutlistener;


typedef struct _alljoyn_aboutobjectdescription_handle* alljoyn_aboutobjectdescription;

typedef struct _alljoyn_aboutobj_handle* alljoyn_aboutobj;


typedef struct _alljoyn_aboutproxy_handle* alljoyn_aboutproxy;



typedef struct _alljoyn_authlistener_handle*                alljoyn_authlistener;

typedef struct _alljoyn_credentials_handle*                 alljoyn_credentials;





typedef struct _alljoyn_pinglistener_handle* alljoyn_pinglistener;



typedef struct _alljoyn_autopinger_handle* alljoyn_autopinger;


typedef struct _alljoyn_busattachment_handle*               alljoyn_busattachment;


typedef struct _alljoyn_buslistener_handle*                 alljoyn_buslistener;

typedef struct _alljoyn_busattachment_handle*               alljoyn_busattachment;



typedef struct _alljoyn_busobject_handle*                   alljoyn_busobject;


typedef struct _alljoyn_interfacedescription_handle*        alljoyn_interfacedescription;




AJ_API QCC_BOOL AJ_CALL alljoyn_interfacedescription_getmemberannotation(alljoyn_interfacedescription iface ,const char* member ,const char* name ,char* value ,size_t* value_size);



typedef struct _alljoyn_keystore_handle*                    alljoyn_keystore;


typedef struct _alljoyn_keystorelistener_handle*            alljoyn_keystorelistener;


typedef struct _alljoyn_busattachment_handle*               alljoyn_busattachment;






typedef struct _alljoyn_busobject_handle*                   alljoyn_busobject;




typedef struct _alljoyn_msgarg_handle* alljoyn_msgarg;


typedef struct _alljoyn_proxybusobject_ref_handle* alljoyn_proxybusobject_ref;





typedef struct _alljoyn_observerlistener_handle* alljoyn_observerlistener;




typedef struct _alljoyn_observer_handle* alljoyn_observer;


typedef struct _alljoyn_permissionconfigurationlistener_handle* alljoyn_permissionconfigurationlistener;


typedef struct _alljoyn_proxybusobject_handle*              alljoyn_proxybusobject;

typedef struct _alljoyn_busattachment_handle*               alljoyn_busattachment;



typedef struct _alljoyn_sessionopts_handle*                 alljoyn_sessionopts;




typedef struct _alljoyn_sessionlistener_handle*             alljoyn_sessionlistener;


typedef struct _alljoyn_sessionportlistener_handle*         alljoyn_sessionportlistener;
"""



