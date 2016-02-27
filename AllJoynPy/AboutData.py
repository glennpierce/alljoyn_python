#!/usr/bin/python
# -*- coding: utf-8 -*-
import types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from AllJoyn import AllJoynMeta, AllJoynObject


# Wrapper for file AboutData.h

# Typedefs
# struct _alljoyn_aboutdata_handle * alljoyn_aboutdata

class AboutData(AllJoynObject):

    __metaclass__ = AllJoynMeta

    __methods = [
        (u'alljoyn_aboutdata_create', (u'alljoyn_aboutdata',
         'C.c_void_p'), ((u'const char *', 'C.c_char_p'), )),
        (u'alljoyn_aboutdata_create_full', (u'alljoyn_aboutdata',
         'C.c_void_p'), ((u'const int', 'C.c_int32_t'), )),
        (u'alljoyn_aboutdata_create_full', (u'alljoyn_aboutdata',
         'C.c_void_p'), ((u'const int', 'C.c_int32_t'), (u'const char *'
         , 'C.c_char_p'))),
        (u'alljoyn_aboutdata_destroy', (u'void', 'as'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_createfromxml', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_createfromxml', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_isvalid', (u'int', 'C.c_int32_t'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_isvalid', (u'int', 'C.c_int32_t'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_createfrommsgarg', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_createfrommsgarg', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'const int', 'C.c_int32_t'))),
        (u'alljoyn_aboutdata_createfrommsgarg', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'const int', 'C.c_int32_t'), (u'const char *', 'C.c_char_p'
         ))),
        (u'alljoyn_aboutdata_setappid', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setappid', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const int *',
         'POINTER(C.c_int32)'))),
        (u'alljoyn_aboutdata_setappid', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const int *',
         'POINTER(C.c_int32)'), (u'const int', 'C.c_int32_t'))),
        (u'alljoyn_aboutdata_setappid_fromstring', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setappid_fromstring', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_getappid', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getappid', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'int **',
         'POINTER(POINTER(C.c_int32))'))),
        (u'alljoyn_aboutdata_getappid', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'int **',
         'POINTER(POINTER(C.c_int32))'), (u'int *', 'POINTER(C.c_int32)'
         ))),
        (u'alljoyn_aboutdata_setdefaultlanguage', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setdefaultlanguage', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_getdefaultlanguage', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getdefaultlanguage', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'char **', 'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_setdevicename', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setdevicename', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_setdevicename', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'), (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_getdevicename', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getdevicename', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'char **',
         'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_getdevicename', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'char **',
         'POINTER(C.c_char_p)'), (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_setdeviceid', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setdeviceid', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_getdeviceid', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getdeviceid', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'char **',
         'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_setappname', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setappname', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_setappname', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'), (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_getappname', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getappname', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'char **',
         'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_getappname', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'char **',
         'POINTER(C.c_char_p)'), (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_setmanufacturer', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setmanufacturer', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_setmanufacturer', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'), (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_getmanufacturer', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getmanufacturer', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'char **',
         'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_getmanufacturer', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'char **',
         'POINTER(C.c_char_p)'), (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_setmodelnumber', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setmodelnumber', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_getmodelnumber', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getmodelnumber', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'char **',
         'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_setsupportedlanguage', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setsupportedlanguage', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_getsupportedlanguages', (u'int',
         'C.c_int32_t'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getsupportedlanguages', (u'int',
         'C.c_int32_t'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'const char **', 'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_getsupportedlanguages', (u'int',
         'C.c_int32_t'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'const char **', 'POINTER(C.c_char_p)'), (u'int',
         'C.c_int32_t'))),
        (u'alljoyn_aboutdata_setdescription', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setdescription', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_setdescription', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'), (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_getdescription', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getdescription', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'char **',
         'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_getdescription', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'char **',
         'POINTER(C.c_char_p)'), (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_setdateofmanufacture', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setdateofmanufacture', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_getdateofmanufacture', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getdateofmanufacture', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'char **', 'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_setsoftwareversion', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setsoftwareversion', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_getsoftwareversion', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getsoftwareversion', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'char **', 'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_getajsoftwareversion', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getajsoftwareversion', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'char **', 'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_sethardwareversion', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_sethardwareversion', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_gethardwareversion', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_gethardwareversion', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'char **', 'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_setsupporturl', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setsupporturl', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_getsupporturl', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getsupporturl', (u'QStatus', 'C.c_uint32'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'char **',
         'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_setfield', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_setfield', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_setfield', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'), (u'int', 'C.c_int32_t'))),
        (u'alljoyn_aboutdata_setfield', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'), (u'int', 'C.c_int32_t'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_getfield', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getfield', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_getfield', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'), (u'int *', 'POINTER(C.c_int32)'))),
        (u'alljoyn_aboutdata_getfield', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'), (u'int *', 'POINTER(C.c_int32)'),
         (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_getfields', (u'int', 'C.c_int32_t'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getfields', (u'int', 'C.c_int32_t'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char **',
         'POINTER(C.c_char_p)'))),
        (u'alljoyn_aboutdata_getfields', (u'int', 'C.c_int32_t'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char **',
         'POINTER(C.c_char_p)'), (u'int', 'C.c_int32_t'))),
        (u'alljoyn_aboutdata_getaboutdata', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getaboutdata', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'int', 'C.c_int32_t'
         ))),
        (u'alljoyn_aboutdata_getaboutdata', (u'QStatus', 'C.c_uint32'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'int', 'C.c_int32_t'
         ), (u'const char *', 'C.c_char_p'))),
        (u'alljoyn_aboutdata_getannouncedaboutdata', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getannouncedaboutdata', (u'QStatus',
         'C.c_uint32'), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'int',
         'C.c_int32_t'))),
        (u'alljoyn_aboutdata_isfieldrequired', (u'int', 'C.c_int32_t'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_isfieldrequired', (u'int', 'C.c_int32_t'),
         ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_isfieldannounced', (u'int', 'C.c_int32_t'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_isfieldannounced', (u'int', 'C.c_int32_t'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_isfieldlocalized', (u'int', 'C.c_int32_t'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_isfieldlocalized', (u'int', 'C.c_int32_t'
         ), ((u'alljoyn_aboutdata', 'C.c_void_p'), (u'const char *',
         'C.c_char_p'))),
        (u'alljoyn_aboutdata_getfieldsignature', (u'const char *',
         'C.c_char_p'), ((u'alljoyn_aboutdata', 'C.c_void_p'), )),
        (u'alljoyn_aboutdata_getfieldsignature', (u'const char *',
         'C.c_char_p'), ((u'alljoyn_aboutdata', 'C.c_void_p'),
         (u'const char *', 'C.c_char_p'))),
        ]

    # def __init__(self, defaultLanguage, arg=None):
    #    if not arg:
    #        self.handle = self.AboutdataCreate(defaultLanguage)
    #    else:
    #        self.handle = self.AboutdataCreateFull(arg, defaultLanguage)

    def __del__(self):
        self.AboutDataDestroy(self.handle)


