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
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject

# Wrapper for file InterfaceDescription.h
ALLJOYN_PROP_ACCESS_READ = 1  # Read Access type
ALLJOYN_PROP_ACCESS_WRITE = 2  # Write Access type
ALLJOYN_PROP_ACCESS_RW = 3  # Read-Write Access type


ALLJOYN_MEMBER_ANNOTATE_NO_REPLY = 1  # No reply annotate flag
ALLJOYN_MEMBER_ANNOTATE_DEPRECATED = 2  # Deprecated annotate flag
ALLJOYN_MEMBER_ANNOTATE_SESSIONCAST = 4  # Sessioncast annotate flag
ALLJOYN_MEMBER_ANNOTATE_SESSIONLESS = 8  # Sessionless annotate flag
ALLJOYN_MEMBER_ANNOTATE_UNICAST = 16  # Unicast annotate flag
ALLJOYN_MEMBER_ANNOTATE_GLOBAL_BROADCAST = 32  # Global broadcast annotate flag


@unique
class SecurityPolicy(Enum):
    AJ_IFC_SECURITY_INHERIT = 0
    AJ_IFC_SECURITY_REQUIRED = 1
    AJ_IFC_SECURITY_OFF = 2


if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE


class InterfaceDescriptionMember(C.Structure):
    _fields_ = [
        ("Iface", C.c_void_p),
        ("MemberType", C.c_uint),
        ("Name", C.c_char_p),
        ("Signature", C.c_char_p),
        ("ReturnSignature", C.c_char_p),
        ("ArgNames", C.c_char_p),
        ("Internal_Member", C.c_void_p)
    ]


class InterfaceDescriptionProperty(C.Structure):
    _fields_ = [
        ("Name", C.c_char_p),
        ("Signature", C.c_char_p),
        ("Access", C.c_ubyte),
        ("Internal_Property", C.c_void_p)
    ]


class InterfaceDescriptionHandle(C.c_void_p):
    pass


class InterfaceDescription(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'Activate': (u'alljoyn_interfacedescription_activate',
                               (u'void', None),
                               ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),)),
                 u'AddAnnotation': (u'alljoyn_interfacedescription_addannotation',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                        (u'const char *', C.c_char_p),
                                        (u'const char *', C.c_char_p))),

                 u'AddMember': (u'alljoyn_interfacedescription_addmember',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                    (u'int', C.c_int),
                                    (u'const char *', C.c_char_p),
                                    (u'const char *', C.c_char_p),
                                    (u'const char *', C.c_char_p),
                                    (u'const char *', C.c_char_p),
                                    (u'int', C.c_int))),
                 u'AddMemberAnnotation': (u'alljoyn_interfacedescription_addmemberannotation',
                                          (u'QStatus', C.c_uint),
                                          ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                              (u'const char *', C.c_char_p),
                                              (u'const char *', C.c_char_p),
                                              (u'const char *', C.c_char_p))),
                 u'AddMethod': (u'alljoyn_interfacedescription_addmethod',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                    (u'const char *', C.c_char_p),
                                    (u'const char *', C.c_char_p),
                                    (u'const char *', C.c_char_p),
                                    (u'const char *', C.c_char_p),
                                    (u'int', C.c_int),
                                    (u'const char *', C.c_char_p))),

                 u'AddProperty': (u'alljoyn_interfacedescription_addproperty',
                                  (u'QStatus', C.c_uint),
                                  ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                      (u'const char *', C.c_char_p),
                                      (u'const char *', C.c_char_p),
                                      (u'int', C.c_int))),

                 u'AddPropertyAnnotation': (u'alljoyn_interfacedescription_addpropertyannotation',
                                            (u'QStatus', C.c_uint),
                                            ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                                (u'const char *', C.c_char_p),
                                                (u'const char *', C.c_char_p),
                                                (u'const char *', C.c_char_p))),
                 u'AddSignal': (u'alljoyn_interfacedescription_addsignal',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                    (u'const char *', C.c_char_p),
                                    (u'const char *', C.c_char_p),
                                    (u'const char *', C.c_char_p),
                                    (u'int', C.c_int),
                                    (u'const char *', C.c_char_p))),
                 u'EQL': (u'alljoyn_interfacedescription_eql',
                          (u'int', C.c_int),
                          ((u'const alljoyn_interfacedescription', C.c_void_p),
                              (u'const alljoyn_interfacedescription', C.c_void_p))),
                 u'GetAnnotation': (u'alljoyn_interfacedescription_getannotation',
                                    (u'int', C.c_int),
                                    ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                     (u'const char *', C.c_char_p),
                                     (u'char *', C.c_char_p),
                                     (u'int *', POINTER(C.c_int)))),
                 u'GetAnnotationAtIndex': (u'alljoyn_interfacedescription_getannotationatindex',
                                           (u'void', None),
                                           ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                            (u'int', C.c_int),
                                            (u'char *', C.c_char_p),
                                            (u'int *', POINTER(C.c_int)),
                                            (u'char *', C.c_char_p),
                                            (u'int *', POINTER(C.c_int)))),
                 u'GetAnnotationsCount': (u'alljoyn_interfacedescription_getannotationscount',
                                          (u'int', C.c_int),
                                          ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),)),
                 u'GetMember': (u'alljoyn_interfacedescription_getmember',
                                (u'int', C.c_int),
                                ((u'const alljoyn_interfacedescription', C.c_void_p),
                                 (u'const char *', C.c_char_p),
                                 (u'alljoyn_interfacedescription_member *',
                                  POINTER(InterfaceDescriptionMember)))),
                 u'GetMemberAnnotation': (u'alljoyn_interfacedescription_getmemberannotation',
                                          (u'int', C.c_int),
                                          ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                           (u'const char *', C.c_char_p),
                                           (u'const char *', C.c_char_p),
                                           (u'char *', C.c_char_p),
                                           (u'int *', POINTER(C.c_int)))),
                 u'GetMembers': (u'alljoyn_interfacedescription_getmembers',
                                 (u'int', C.c_int),
                                 ((u'const alljoyn_interfacedescription', C.c_void_p),
                                  (u'alljoyn_interfacedescription_member *',
                                   POINTER(InterfaceDescriptionMember)),
                                  (u'int', C.c_int))),
                 u'GetMethod': (u'alljoyn_interfacedescription_getmethod',
                                (u'int', C.c_int),
                                ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                 (u'const char *', C.c_char_p),
                                 (u'alljoyn_interfacedescription_member *',
                                  POINTER(InterfaceDescriptionMember)))),
                 u'GetName': (u'alljoyn_interfacedescription_getname',
                              (u'const char *', C.c_char_p),
                              ((u'const alljoyn_interfacedescription', C.c_void_p),)),
                 u'GetProperties': (u'alljoyn_interfacedescription_getproperties',
                                    (u'int', C.c_int),
                                    ((u'const alljoyn_interfacedescription', C.c_void_p),
                                     (u'alljoyn_interfacedescription_property *',
                                      POINTER(InterfaceDescriptionProperty)),
                                     (u'int', C.c_int))),
                 u'GetProperty': (u'alljoyn_interfacedescription_getproperty',
                                  (u'int', C.c_int),
                                  ((u'const alljoyn_interfacedescription', C.c_void_p),
                                   (u'const char *', C.c_char_p),
                                   (u'alljoyn_interfacedescription_property *',
                                    POINTER(InterfaceDescriptionProperty)))),
                 u'GetPropertyAnnotation': (u'alljoyn_interfacedescription_getpropertyannotation',
                                            (u'int', C.c_int),
                                            ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                             (u'const char *', C.c_char_p),
                                             (u'const char *', C.c_char_p),
                                             (u'char *', C.c_char_p),
                                             (u'int *', POINTER(C.c_int)))),
                 u'GetSecurityPolicy': (u'alljoyn_interfacedescription_getsecuritypolicy',
                                        (u'alljoyn_interfacedescription_securitypolicy', C.c_uint),
                                        ((u'const alljoyn_interfacedescription',
                                          C.c_void_p),)),
                 u'GetSignal': (u'alljoyn_interfacedescription_getsignal',
                                (u'int', C.c_int),
                                ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                 (u'const char *', C.c_char_p),
                                 (u'alljoyn_interfacedescription_member *',
                                  POINTER(InterfaceDescriptionMember)))),
                 u'HasMember': (u'alljoyn_interfacedescription_hasmember',
                                (u'int', C.c_int),
                                ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                 (u'const char *', C.c_char_p),
                                 (u'const char *', C.c_char_p),
                                 (u'const char *', C.c_char_p))),
                 u'HasProperties': (u'alljoyn_interfacedescription_hasproperties',
                                    (u'int', C.c_int),
                                    ((u'const alljoyn_interfacedescription', C.c_void_p),)),
                 u'HasProperty': (u'alljoyn_interfacedescription_hasproperty',
                                  (u'int', C.c_int),
                                  ((u'const alljoyn_interfacedescription', C.c_void_p),
                                   (u'const char *', C.c_char_p))),

                 u'Introspect': (u'alljoyn_interfacedescription_introspect',
                                 (u'size_t', C.c_size_t),
                                 ((u'const alljoyn_interfacedescription', InterfaceDescriptionHandle),
                                  (u'char *', C.c_char_p),
                                  (u'size_t', C.c_size_t),
                                  (u'size_t', C.c_size_t))),

                 u'IsSecure': (u'alljoyn_interfacedescription_issecure',
                               (u'int', C.c_int),
                               ((u'const alljoyn_interfacedescription', C.c_void_p),)),
                 u'MemberEQL': (u'alljoyn_interfacedescription_member_eql',
                                (u'int', C.c_int),
                                ((u'const alljoyn_interfacedescription_member',
                                  POINTER(InterfaceDescriptionMember)),
                                 (u'const alljoyn_interfacedescription_member',
                                  POINTER(InterfaceDescriptionMember)))),
                 u'MemberGetAnnotation': (u'alljoyn_interfacedescription_member_getannotation',
                                          (u'int', C.c_int),
                                          ((u'alljoyn_interfacedescription_member',
                                            POINTER(InterfaceDescriptionMember)),
                                           (u'const char *', C.c_char_p),
                                           (u'char *', C.c_char_p),
                                           (u'int *', POINTER(C.c_int)))),
                 u'MemberGetAnnotationAtIndex': (u'alljoyn_interfacedescription_member_getannotationatindex',
                                                 (u'void', None),
                                                 ((u'alljoyn_interfacedescription_member',
                                                   POINTER(InterfaceDescriptionMember)),
                                                  (u'int', C.c_int),
                                                  (u'char *', C.c_char_p),
                                                  (u'int *', POINTER(C.c_int)),
                                                  (u'char *', C.c_char_p),
                                                  (u'int *', POINTER(C.c_int)))),
                 u'MemberGetAnnotationsCount': (u'alljoyn_interfacedescription_member_getannotationscount',
                                                (u'int', C.c_int),
                                                ((u'alljoyn_interfacedescription_member',
                                                  POINTER(InterfaceDescriptionMember)),)),
                 u'PropertyEql': (u'alljoyn_interfacedescription_property_eql',
                                  (u'int', C.c_int),
                                  ((u'const alljoyn_interfacedescription_property',
                                    POINTER(InterfaceDescriptionProperty)),
                                   (u'const alljoyn_interfacedescription_property',
                                    POINTER(InterfaceDescriptionProperty)))),
                 u'PropertyGetAnnotation': (u'alljoyn_interfacedescription_property_getannotation',
                                            (u'int', C.c_int),
                                            ((u'alljoyn_interfacedescription_property',
                                              POINTER(InterfaceDescriptionProperty)),
                                             (u'const char *', C.c_char_p),
                                             (u'char *', C.c_char_p),
                                             (u'int *', POINTER(C.c_int)))),
                 u'PropertyGetAnnotationAtIndex': (u'alljoyn_interfacedescription_property_getannotationatindex',
                                                   (u'void', None),
                                                   ((u'alljoyn_interfacedescription_property',
                                                     POINTER(InterfaceDescriptionProperty)),
                                                    (u'int', C.c_int),
                                                    (u'char *', C.c_char_p),
                                                    (u'int *', POINTER(C.c_int)),
                                                    (u'char *', C.c_char_p),
                                                    (u'int *', POINTER(C.c_int)))),
                 u'PropertyGetAnnotationsCount': (u'alljoyn_interfacedescription_property_getannotationscount',
                                                  (u'int', C.c_int),
                                                  ((u'alljoyn_interfacedescription_property',
                                                    POINTER(InterfaceDescriptionProperty)),))}

    def __init__(self, handle):
        self.handle = handle

    def __del__(self):
        pass

    # Wrapper Methods

    def MemberGetAnnotationsCount(self):
        return self._MemberGetAnnotationsCount(self.handle)

    def MemberGetAnnotationAtIndex(self, index, name, name_size, value, value_size):
        # int,char *,int *,char *,int *
        return self._MemberGetAnnotationAtIndex(self.handle, index, name, name_size, value, value_size)

    def MemberGetAnnotation(self, name, value, value_size):
        return self._MemberGetAnnotation(self.handle, name, value, value_size)  # const char *,char *,int *

    def PropertyGetAnnotationsCount(self):
        return self._PropertyGetAnnotationsCount(self.handle)

    def PropertyGetAnnotationAtIndex(self, index, name, name_size, value, value_size):
        # int,char *,int *,char *,int *
        return self._PropertyGetAnnotationAtIndex(self.handle, index, name, name_size, value, value_size)

    def PropertyGetAnnotation(self, name, value, value_size):
        return self._PropertyGetAnnotation(self.handle, name, value, value_size)  # const char *,char *,int *

    def Activate(self):
        return self._Activate(self.handle)

    def AddAnnotation(self, name, value):
        return self._AddAnnotation(self.handle, name, value)  # const char *,const char *

    def GetAnnotation(self, name, value, value_size):
        return self._GetAnnotation(self.handle, name, value, value_size)  # const char *,char *,int *

    def GetAnnotationsCount(self):
        return self._GetAnnotationsCount(self.handle)

    def GetAnnotationAtIndex(self, index, name, name_size, value, value_size):
        # int,char *,int *,char *,int *
        return self._GetAnnotationAtIndex(self.handle, index, name, name_size, value, value_size)

    def GetMember(self, name):
        member = InterfaceDescriptionMember()
        self._GetMember(self.handle, name, C.byref(member))  # const char *, alljoyn_interfacedescription_member *
        return C.pointer(member)

    def AddMember(self, message_type, name, inputSig, outSig, argNames, annotation):
        # int,const char *,const char *,const char *,const char *,int
        return self._AddMember(self.handle, message_type.value, name, inputSig, outSig, argNames, annotation)

    def AddMemberAnnotation(self, member, name, value):
        return self._AddMemberAnnotation(self.handle, member, name, value)  # const char *,const char *,const char *

    def GetMemberAnnotation(self, member, name, value, value_size):
        # const char *,const char *,char *,int *
        return self._GetMemberAnnotation(self.handle, member, name, value, value_size)

    def GetMembers(self, members, numMembers):
        return self._GetMembers(self.handle, members, numMembers)  # alljoyn_interfacedescription_member *,int

    def HasMember(self, name, inSig, outSig):
        return self._HasMember(self.handle, name, inSig, outSig)  # const char *,const char *,const char *

    def AddMethod(self, name, inputSig, outSig, argNames, annotation, accessPerms):
        # const char *,const char *,const char *,const char *,int,const char *
        return self._AddMethod(self.handle, name, inputSig, outSig, argNames, annotation, accessPerms)

    def GetMethod(self, name, member):
        return self._GetMethod(self.handle, name, member)  # const char *,alljoyn_interfacedescription_member *

    def AddSignal(self, name, sig, argNames, annotation, accessPerms):
        # const char *,const char *,const char *,int,const char *
        return self._AddSignal(self.handle, name, sig, argNames, annotation, accessPerms)

    def GetSignal(self, name, member):
        return self._GetSignal(self.handle, name, member)  # const char *,alljoyn_interfacedescription_member *

    def GetProperty(self, name, property):
        return self._GetProperty(self.handle, name, property)  # const char *,alljoyn_interfacedescription_property *

    def GetProperties(self, props, numProps):
        return self._GetProperties(self.handle, props, numProps)  # alljoyn_interfacedescription_property *,int

    def AddProperty(self, name, signature, access):
        return self._AddProperty(self.handle, name, signature, access)  # const char *,const char *,int

    def AddPropertyAnnotation(self, property, name, value):
        return self._AddPropertyAnnotation(self.handle, property, name, value)  # const char *,const char *,const char *

    def GetPropertyAnnotation(self, property, name, value, str_size):
        # const char *,const char *,char *,int *
        return self._GetPropertyAnnotation(self.handle, property, name, value, str_size)

    def HasProperty(self, name):
        return self._HasProperty(self.handle, name)  # const char *

    def HasProperties(self):
        return self._HasProperties(self.handle)

    def GetName(self):
        return self._GetName(self.handle)

    def Introspect(self, indent=2):
        size = self._Introspect(self.handle, None, 0, indent)  # char *,int,int
        buf = C.create_string_buffer(size)
        self._Introspect(self.handle, buf, size, indent)  # char *,int,int
        return buf.value

    def IsSecure(self):
        return self._IsSecure(self.handle)

    def GetSecurityPolicy(self):
        return self._GetSecurityPolicy(self.handle)

    def EQL(self, other):
        return self._EQL(self.handle, other)  # const alljoyn_interfacedescription

    def MemberEQL(self, other):
        return self._MemberEQL(self.handle, other)  # const alljoyn_interfacedescription_member

    def PropertyEql(self, other):
        return self._PropertyEql(self.handle, other)  # const alljoyn_interfacedescription_property


InterfaceDescription.bind_functions_to_cls()
