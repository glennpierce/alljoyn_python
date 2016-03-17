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
import types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import *
import MsgArg

# Wrapper for file AboutData.h

# Typedefs
# struct _alljoyn_aboutdata_handle * alljoyn_aboutdata

if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE


class AboutData(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'Create': (u'alljoyn_aboutdata_create',
                             (u'alljoyn_aboutdata', AboutDataHandle),
                             ((u'const char *', C.c_char_p),)),

                 u'CreateEmpty': (u'alljoyn_aboutdata_create_empty',
                                  (u'alljoyn_aboutdata', AboutDataHandle),
                                  ()),

                 u'CreateFromMsgARG': (u'alljoyn_aboutdata_createfrommsgarg',
                                       (u'QStatus', C.c_uint),
                                       ((u'alljoyn_aboutdata', AboutDataHandle),
                                           (u'const int', C.c_int),
                                           (u'const char *', C.c_char_p))),

                 u'CreateFromXML': (u'alljoyn_aboutdata_createfromxml',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_aboutdata', AboutDataHandle),
                                        (u'const char *', C.c_char_p))),

                 u'CreateFull': (u'alljoyn_aboutdata_create_full',
                                 (u'alljoyn_aboutdata', AboutDataHandle),
                                 ((u'const void*', C.c_void_p), (u'const char *', C.c_char_p))),

                 u'Destroy': (u'alljoyn_aboutdata_destroy',
                              (u'void', None),
                              ((u'alljoyn_aboutdata', AboutDataHandle),)),

                 u'GetAJSoftwareVersion': (u'alljoyn_aboutdata_getajsoftwareversion',
                                           (u'QStatus', C.c_uint),
                                           ((u'alljoyn_aboutdata', AboutDataHandle),
                                               (u'char **', POINTER(C.c_char_p)))),

                 u'GetAPPID': (u'alljoyn_aboutdata_getappid',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_aboutdata', AboutDataHandle),
                                   (u'int **', POINTER(POINTER(C.c_int))),
                                   (u'int *', POINTER(C.c_int)))),

                 u'GetAppName': (u'alljoyn_aboutdata_getappname',
                                 (u'QStatus', C.c_uint),
                                 ((u'alljoyn_aboutdata', AboutDataHandle),
                                     (u'char **', POINTER(C.c_char_p)),
                                     (u'const char *', C.c_char_p))),

                 u'GetAboutData': (u'alljoyn_aboutdata_getaboutdata',
                                   (u'QStatus', C.c_uint),
                                   ((u'alljoyn_aboutdata', AboutDataHandle),
                                       (u'alljoyn_msgarg', C.c_void_p),
                                       (u'const char *', C.c_char_p))),

                 u'GetAnnouncedAboutData': (u'alljoyn_aboutdata_getannouncedaboutdata',
                                            (u'QStatus', C.c_uint),
                                            ((u'alljoyn_aboutdata', AboutDataHandle),
                                                (u'alljoyn_msgarg', C.c_void_p))),

                 u'GetDateOfManufacture': (u'alljoyn_aboutdata_getdateofmanufacture',
                                           (u'QStatus', C.c_uint),
                                           ((u'alljoyn_aboutdata', AboutDataHandle),
                                               (u'char **', POINTER(C.c_char_p)))),

                 u'GetDefaultLanguage': (u'alljoyn_aboutdata_getdefaultlanguage',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_aboutdata', AboutDataHandle),
                                             (u'char **', POINTER(C.c_char_p)))),

                 u'GetDescription': (u'alljoyn_aboutdata_getdescription',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_aboutdata', AboutDataHandle),
                                         (u'char **', POINTER(C.c_char_p)),
                                         (u'const char *', C.c_char_p))),

                 u'GetDeviceId': (u'alljoyn_aboutdata_getdeviceid',
                                  (u'QStatus', C.c_uint),
                                  ((u'alljoyn_aboutdata', AboutDataHandle),
                                      (u'char **', POINTER(C.c_char_p)))),

                 u'GetDeviceName': (u'alljoyn_aboutdata_getdevicename',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_aboutdata', AboutDataHandle),
                                        (u'char **', POINTER(C.c_char_p)),
                                        (u'const char *', C.c_char_p))),


                 u'GetField': (u'alljoyn_aboutdata_getfield',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_aboutdata', AboutDataHandle), (u'const char *', C.c_char_p),
                                   (u'alljoyn_msgarg*', POINTER(MsgArg.MsgArgHandle)),
                                   (u'const char *', C.c_char_p))),


                 u'GetFieldSignature': (u'alljoyn_aboutdata_getfieldsignature',
                                        (u'const char *', C.c_char_p),
                                        ((u'alljoyn_aboutdata', AboutDataHandle),
                                            (u'const char *', C.c_char_p))),

                 u'GetFields': (u'alljoyn_aboutdata_getfields', (u'int', C.c_int),
                                ((u'alljoyn_aboutdata', AboutDataHandle), (u'const char **', POINTER(C.c_char_p)),
                                 (u'int', C.c_int))),

                 u'GetHardwareVersion': (u'alljoyn_aboutdata_gethardwareversion',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_aboutdata', AboutDataHandle),
                                          (u'char **', POINTER(C.c_char_p)))),

                 u'GetManufacturer': (u'alljoyn_aboutdata_getmanufacturer',
                                      (u'QStatus', C.c_uint),
                                      ((u'alljoyn_aboutdata', AboutDataHandle),
                                          (u'char **', POINTER(C.c_char_p)),
                                          (u'const char *', C.c_char_p))),

                 u'GetModelNumber': (u'alljoyn_aboutdata_getmodelnumber',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_aboutdata', AboutDataHandle),
                                         (u'char **', POINTER(C.c_char_p)))),

                 u'GetSoftwareVersion': (u'alljoyn_aboutdata_getsoftwareversion',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_aboutdata', AboutDataHandle),
                                             (u'char **', POINTER(C.c_char_p)))),

                 u'GetSupportURL': (u'alljoyn_aboutdata_getsupporturl',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_aboutdata', AboutDataHandle),
                                        (u'char **', POINTER(C.c_char_p)))),

                 u'GetSupportedLanguages': (u'alljoyn_aboutdata_getsupportedlanguages',
                                            (u'int', C.c_int),
                                            ((u'alljoyn_aboutdata', AboutDataHandle),
                                                (u'const char **', POINTER(C.c_char_p)),
                                                (u'int', C.c_int))),

                 u'IsFieldAnnounced': (u'alljoyn_aboutdata_isfieldannounced',
                                       (u'int', C.c_int),
                                       ((u'alljoyn_aboutdata', AboutDataHandle),
                                           (u'const char *', C.c_char_p))),

                 u'IsFieldLocalized': (u'alljoyn_aboutdata_isfieldlocalized',
                                       (u'int', C.c_int),
                                       ((u'alljoyn_aboutdata', AboutDataHandle),
                                           (u'const char *', C.c_char_p))),

                 u'IsFieldRequired': (u'alljoyn_aboutdata_isfieldrequired',
                                      (u'int', C.c_int),
                                      ((u'alljoyn_aboutdata', AboutDataHandle),
                                          (u'const char *', C.c_char_p))),

                 u'IsValid': (u'alljoyn_aboutdata_isvalid',
                              (u'int', C.c_int),
                              ((u'alljoyn_aboutdata', AboutDataHandle),
                                  (u'const char *', C.c_char_p))),

                 u'SetAppId': (u'alljoyn_aboutdata_setappid',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_aboutdata', AboutDataHandle),
                                   (u'const int *', POINTER(C.c_ubyte)),
                                   (u'const int', C.c_int))),

                 u'SetAppIdFromString': (u'alljoyn_aboutdata_setappid_fromstring',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_aboutdata', AboutDataHandle),
                                             (u'const char *', C.c_char_p))),

                 u'SetAppName': (u'alljoyn_aboutdata_setappname',
                                 (u'QStatus', C.c_uint),
                                 ((u'alljoyn_aboutdata', AboutDataHandle),
                                     (u'const char *', C.c_char_p),
                                     (u'const char *', C.c_char_p))),

                 u'SetDateOfManufacture': (u'alljoyn_aboutdata_setdateofmanufacture',
                                           (u'QStatus', C.c_uint),
                                           ((u'alljoyn_aboutdata', AboutDataHandle),
                                               (u'const char *', C.c_char_p))),

                 u'SetDefaultLanguage': (u'alljoyn_aboutdata_setdefaultlanguage',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_aboutdata', AboutDataHandle),
                                             (u'const char *', C.c_char_p))),

                 u'SetDescription': (u'alljoyn_aboutdata_setdescription',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_aboutdata', AboutDataHandle),
                                         (u'const char *', C.c_char_p),
                                         (u'const char *', C.c_char_p))),

                 u'SetDeviceId': (u'alljoyn_aboutdata_setdeviceid',
                                  (u'QStatus', C.c_uint),
                                  ((u'alljoyn_aboutdata', AboutDataHandle),
                                      (u'const char *', C.c_char_p))),

                 u'SetDeviceName': (u'alljoyn_aboutdata_setdevicename',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_aboutdata', AboutDataHandle),
                                        (u'const char *', C.c_char_p),
                                        (u'const char *', C.c_char_p))),

                 u'SetField': (u'alljoyn_aboutdata_setfield',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_aboutdata', AboutDataHandle),
                                   (u'const char *', C.c_char_p),
                                   (u'alljoyn_msgarg', C.c_void_p),
                                   (u'const char *', C.c_char_p))),

                 u'SetHardwareVersion': (u'alljoyn_aboutdata_sethardwareversion',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_aboutdata', AboutDataHandle),
                                             (u'const char *', C.c_char_p))),

                 u'SetManufacturer': (u'alljoyn_aboutdata_setmanufacturer',
                                      (u'QStatus', C.c_uint),
                                      ((u'alljoyn_aboutdata', AboutDataHandle),
                                          (u'const char *', C.c_char_p),
                                          (u'const char *', C.c_char_p))),

                 u'SetModelNumber': (u'alljoyn_aboutdata_setmodelnumber',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_aboutdata', AboutDataHandle),
                                         (u'const char *', C.c_char_p))),

                 u'SetSoftwareVersion': (u'alljoyn_aboutdata_setsoftwareversion',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_aboutdata', AboutDataHandle),
                                             (u'const char *', C.c_char_p))),

                 u'SetSupportURL': (u'alljoyn_aboutdata_setsupporturl',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_aboutdata', AboutDataHandle),
                                        (u'const char *', C.c_char_p))),

                 u'SetSupportedLanguage': (u'alljoyn_aboutdata_setsupportedlanguage',
                                           (u'QStatus', C.c_uint),
                                           ((u'alljoyn_aboutdata', AboutDataHandle),
                                               (u'const char *', C.c_char_p)))}

    def __init__(self, msgarg=None, language="en"):
        super(AboutData, self).__init__()

        if msgarg:
            self.handle = self._CreateFull(msgarg.handle, language)
        else:
            self.handle = self._Create(language)

    def __del__(self):
        if self.handle:
            self._Destroy(self.handle)

    # Wrapper Methods

    def CreateFromXML(self, aboutDataXml):
        return self._CreateFromXML(self.handle, aboutDataXml)  # const char *

    def IsValid(self, language):
        return self._IsValid(self.handle, language)  # const char *

    def CreateFromMsgArg(self, arg, language):
        return self._CreateFromMsgArg(self.handle, arg, language)  # const int,const char *

    def SetAppId(self, app_id):
        array = (C.c_ubyte * len(app_id))(*app_id)
        return self._SetAppId(self.handle, array, len(app_id))  # const int *,const int

    def SetAppIdFromString(self, appId):
        return self._SetAppIdFromString(self.handle, appId)  # const char *

    def GetAppId(self, appId, num):
        return self._GetAppId(self.handle, appId, num)  # int **,int *

    def SetDefaultLanguage(self, defaultLanguage):
        return self._SetDefaultLanguage(self.handle, defaultLanguage)  # const char *

    def GetDefaultLanguage(self):
        defaultLanguage = C.c_char_p()
        self._GetDefaultLanguage(self.handle, C.byref(defaultLanguage))  # char **
        return defaultLanguage.value

    def SetDeviceName(self, deviceName, language):
        return self._SetDeviceName(self.handle, deviceName, language)  # const char *,const char *

    def GetDeviceName(self, language="en"):
        deviceName = C.c_char_p()
        self._GetDeviceName(self.handle, C.byref(deviceName), language)  # char **,const char *
        return deviceName.value

    def SetDeviceId(self, device_id):
        return self._SetDeviceId(self.handle, device_id)  # const char *

    def GetDeviceId(self):
        deviceId = C.c_char_p()
        self._GetDeviceId(self.handle, C.byref(deviceId))  # char **
        return deviceId.value

    def SetAppName(self, appName, language):
        return self._SetAppName(self.handle, appName, language)  # const char *,const char *

    def GetAppName(self, language="en"):
        app_name = C.c_char_p()
        self._GetAppName(self.handle, C.byref(app_name))  # char **
        return app_name.value

    def SetManufacturer(self, manufacturer, language):
        return self._SetManufacturer(self.handle, manufacturer, language)  # const char *,const char *

    def GetManufacturer(self, language="en"):
        manufacturer = C.c_char_p()
        self._GetManufacturer(self.handle, C.byref(manufacturer))  # char **
        return manufacturer.value

    def SetModelNumber(self, modelNumber):
        return self._SetModelNumber(self.handle, modelNumber)  # const char *

    def GetModelNumber(self):
        modelNumber = C.c_char_p()
        self._GetModelNumber(self.handle, C.byref(modelNumber))  # char **
        return modelNumber.value

    def SetSupportedLanguage(self, language):
        return self._SetSupportedLanguage(self.handle, language)  # const char *

    def GetSupportedLanguages(self):
        size = self._GetSupportedLanguages(self.handle, None, 0)
        # array of allocated char*
        array = (C.c_char_p * size)()
        self._GetSupportedLanguages(self.handle, array, size)  # const char **,int
        return [a for a in array]

    def SetDescription(self, description, language):
        return self._SetDescription(self.handle, description, language)  # const char *,const char *

    def GetDescription(self, language="en"):
        description = C.c_char_p()
        self._GetDescription(self.handle, C.byref(description))  # char **
        return description.value

    def SetDateOfManufacture(self, date_of_manufacture):
        return self._SetDateOfManufacture(self.handle, date_of_manufacture)  # const char *

    def GetDateOfManufacture(self):
        date_of_manufacture = C.c_char_p()
        self._GetDateOfManufacture(self.handle, C.byref(date_of_manufacture))  # char **
        return date_of_manufacture.value

    def SetSoftwareVersion(self, software_version):
        return self._SetSoftwareVersion(self.handle, software_version)  # const char *

    def GetSoftwareVersion(self, software_version):
        software_version = C.c_char_p()
        self._GetSoftwareVersion(self.handle, C.byref(software_version))  # char **
        return software_version.value

    def GetAJSoftwareVersion(self, aj_software_version):
        aj_software_version = C.c_char_p()
        self._GetAJSoftwareVersion(self.handle, C.byref(aj_software_version))  # char **
        return aj_software_version.value

    def SetHardwareVersion(self, hardware_version):
        return self._SetHardwareVersion(self.handle, hardware_version)  # const char *

    def GetHardwareVersion(self, hardware_version):
        hardware_version = C.c_char_p()
        self._GetHardwareVersion(self.handle, C.byref(hardware_version))  # char **
        return hardware_version.value

    def SetSupportURL(self, support_url):
        return self._SetSupportURL(self.handle, support_url)  # const char *

    def GetSupportURL(self, support_url):
        support_url = C.c_char_p()
        self._GetSupportURL(self.handle, C.byref(support_url))  # char **
        return support_url.value

    def SetField(self, name, value, language):
        return self._SetField(self.handle, name, value, language)  # const char *,int,const char *

    def GetField(self, name, language=None):
        handle = MsgArg.MsgArg._Create()
        self._GetField(self.handle, name, C.byref(handle), language)
        return MsgArg.MsgArg.FromHandle(handle)

    def GetFields(self):
        count = self._GetFields(self.handle, None, 0)
        array = (C.c_char_p * count)()
        self._GetFields(self.handle, array, count)  # const char **, int
        return [a for a in array]

    def GetAboutData(self, language):
        msgArg = C.c_void_p()
        self._GetAboutData(self.handle, C.byref(msgArg), language)  # int,const char *
        return msgArg

    def GetAnnouncedAboutData(self):
        msgArg = C.c_void_p()
        self._GetAnnouncedAboutData(self.handle, C.byref(msgArg))  # int
        return msgArg

    def IsFieldRequired(self, fieldName):
        return self._IsFieldRequired(self.handle, fieldName)  # const char *

    def IsFieldAnnounced(self, fieldName):
        return self._IsFieldAnnounced(self.handle, fieldName)  # const char *

    def IsFieldLocalized(self, fieldName):
        return self._IsFieldLocalized(self.handle, fieldName)  # const char *

    def GetFieldSignature(self, fieldName):
        return self._GetFieldSignature(self.handle, fieldName)  # const char *


AboutData.bind_functions_to_cls()
