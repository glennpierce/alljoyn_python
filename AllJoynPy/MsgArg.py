import sys
import types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject
# Wrapper for file MsgArg.h


class AlljoynMsgArg(C.Structure):
    _fields_ = []


@unique
class TypeId(Enum):
    ALLJOYN_INVALID = 0
    ALLJOYN_Array = 97
    ALLJOYN_BOOLEAN = 98
    ALLJOYN_DOUBLE = 100
    ALLJOYN_DICT_ENTRY = 101
    ALLJOYN_SIGNATURE = 103
    ALLJOYN_HANDLE = 104
    ALLJOYN_Int32 = 105
    ALLJOYN_Int16 = 110
    ALLJOYN_OBJECT_PATH = 111
    ALLJOYN_UInt16 = 113
    ALLJOYN_STRUCT = 114
    ALLJOYN_STRING = 115
    ALLJOYN_UInt64 = 116
    ALLJOYN_UInt32 = 117
    ALLJOYN_VARIANT = 118
    ALLJOYN_Int64 = 120
    ALLJOYN_BYTE = 121
    ALLJOYN_STRUCT_OPEN = 40
    ALLJOYN_STRUCT_CLOSE = 41
    ALLJOYN_DICT_ENTRY_OPEN = 123
    ALLJOYN_DICT_ENTRY_CLOSE = 125
    ALLJOYN_BOOLEAN_Array = 25185
    ALLJOYN_DOUBLE_Array = 25697
    ALLJOYN_Int32_Array = 26977
    ALLJOYN_Int16_Array = 28257
    ALLJOYN_UInt16_Array = 29025
    ALLJOYN_UInt64_Array = 29793
    ALLJOYN_UInt32_Array = 30049
    ALLJOYN_Int64_Array = 30817
    ALLJOYN_BYTE_Array = 31073
    ALLJOYN_WILDCARD = 42


# Typedefs
# struct _alljoyn_msgarg_handle * alljoyn_msgarg
# enum alljoyn_typeid alljoyn_typeid


class MsgArg(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'ArrayCreate': (u'alljoyn_msgarg_array_create',
                                  (u'alljoyn_msgarg', C.c_void_p),
                                  ((u'int', C.c_int),)),

                 u'ArrayElement': (u'alljoyn_msgarg_array_element',
                                   (u'alljoyn_msgarg', C.c_void_p),
                                   ((u'alljoyn_msgarg', C.c_void_p), (u'int', C.c_int))),

                 u'ArrayGet': (u'alljoyn_msgarg_array_get',
                               (u'QStatus', C.c_uint),
                               ((u'const alljoyn_msgarg', C.c_void_p),
                                   (u'int', C.c_int),
                                   (u'const char *', C.c_char_p))),

                 u'ArraySet': (u'alljoyn_msgarg_array_set',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_msgarg', C.c_void_p),
                                   (u'int *', POINTER(C.c_int)),
                                   (u'const char *', C.c_char_p))),

                 u'ArraySetOffset': (u'alljoyn_msgarg_array_set_offset',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', C.c_void_p),
                                         (u'int', C.c_int),
                                         (u'int *', POINTER(C.c_int)),
                                         (u'const char *', C.c_char_p))),

                 u'ArraySignature': (u'alljoyn_msgarg_array_signature',
                                     (u'int', C.c_int),
                                     ((u'alljoyn_msgarg', C.c_void_p),
                                         (u'int', C.c_int),
                                         (u'char *', C.c_char_p),
                                         (u'int', C.c_int))),

                 u'ArrayToString': (u'alljoyn_msgarg_array_tostring',
                                    (u'int', C.c_int),
                                    ((u'const alljoyn_msgarg', C.c_void_p),
                                        (u'int', C.c_int),
                                        (u'char *', C.c_char_p),
                                        (u'int', C.c_int),
                                        (u'int', C.c_int))),

                 u'Clear': (u'alljoyn_msgarg_clear',
                            (u'void', None),
                            ((u'alljoyn_msgarg', C.c_void_p),)),

                 u'Clone': (u'alljoyn_msgarg_clone',
                            (u'void', None),
                            ((u'alljoyn_msgarg', C.c_void_p),
                                (u'const alljoyn_msgarg', C.c_void_p))),

                 u'Copy': (u'alljoyn_msgarg_copy',
                           (u'alljoyn_msgarg', C.c_void_p),
                           ((u'const alljoyn_msgarg', C.c_void_p),)),

                 u'Create': (u'alljoyn_msgarg_create', (u'alljoyn_msgarg', POINTER(AlljoynMsgArg)), ()),

                 u'CreateAndSet': (u'alljoyn_msgarg_create_and_set',
                                   (u'alljoyn_msgarg', C.c_void_p),
                                   ((u'const char *', C.c_char_p),)),

                 u'Destroy': (u'alljoyn_msgarg_destroy', (u'void', None),
                              ((u'alljoyn_msgarg', POINTER(AlljoynMsgArg)),)),

                 u'Equal': (u'alljoyn_msgarg_equal',
                            (u'int', C.c_int),
                            ((u'alljoyn_msgarg', C.c_void_p),
                             (u'alljoyn_msgarg', C.c_void_p))),

                 # u'Get': (u'alljoyn_msgarg_get',
                 #         (u'QStatus', C.c_uint), ((u'alljoyn_msgarg', C.c_void_p), (u'const char *', C.c_char_p))),

                 u'GetArrayElement': (u'alljoyn_msgarg_get_array_element',
                                      (u'void', None),
                                      ((u'const alljoyn_msgarg', C.c_void_p),
                                       (u'int', C.c_int),
                                       (u'alljoyn_msgarg *', POINTER(C.c_void_p)))),

                 u'GetArrayElementSignature': (u'alljoyn_msgarg_get_array_elementsignature',
                                               (u'const char *', C.c_char_p),
                                               ((u'const alljoyn_msgarg', C.c_void_p),
                                                (u'int', C.c_int))),

                 u'GetArrayNumberOfElements': (u'alljoyn_msgarg_get_array_numberofelements',
                                               (u'int', C.c_int),
                                               ((u'const alljoyn_msgarg', C.c_void_p),)),





                 u'GetDictElement': (u'alljoyn_msgarg_getdictelement',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', C.c_void_p),
                                      (u'const char *', C.c_char_p))),


                 u'GetBool': (u'alljoyn_msgarg_get_bool',
                              (u'QStatus', C.c_uint),
                              ((u'const alljoyn_msgarg', C.c_void_p),
                               (u'int *', POINTER(C.c_byte)))),

                 u'GetUInt8': (u'alljoyn_msgarg_get_uint8',
                               (u'QStatus', C.c_uint),
                               ((u'const alljoyn_msgarg', C.c_void_p),
                                (u'int *', POINTER(C.c_ubyte)))),

                 u'GetInt16': (u'alljoyn_msgarg_get_int16',
                               (u'QStatus', C.c_uint),
                               ((u'const alljoyn_msgarg', C.c_void_p),
                                (u'int *', POINTER(C.c_short)))),

                 u'GetUInt16': (u'alljoyn_msgarg_get_uint16',
                                (u'QStatus', C.c_uint),
                                ((u'const alljoyn_msgarg', C.c_void_p),
                                 (u'int *', POINTER(C.c_ushort)))),

                 u'GetInt32': (u'alljoyn_msgarg_get_int32',
                               (u'QStatus', C.c_uint),
                               ((u'const alljoyn_msgarg', C.c_void_p),
                                (u'int *', POINTER(C.c_int)))),

                 u'GetUInt32': (u'alljoyn_msgarg_get_uint32',
                                (u'QStatus', C.c_uint),
                                ((u'const alljoyn_msgarg', C.c_void_p),
                                 (u'int *', POINTER(C.c_uint)))),

                 u'GetInt64': (u'alljoyn_msgarg_get_int64',
                               (u'QStatus', C.c_uint),
                               ((u'const alljoyn_msgarg', C.c_void_p),
                                (u'int *', POINTER(C.c_longlong)))),

                 u'GetUInt64': (u'alljoyn_msgarg_get_uint64',
                                (u'QStatus', C.c_uint),
                                ((u'const alljoyn_msgarg', C.c_void_p),
                                 (u'int *', POINTER(C.c_ulonglong)))),


                 u'GetDouble': (u'alljoyn_msgarg_get_double',
                                (u'QStatus', C.c_uint),
                                ((u'const alljoyn_msgarg', C.c_void_p),
                                 (u'double *', POINTER(C.c_double)))),




                 u'GetKey': (u'alljoyn_msgarg_getkey',
                             (u'alljoyn_msgarg', C.c_void_p),
                             ((u'alljoyn_msgarg', C.c_void_p),)),

                 u'GetMember': (u'alljoyn_msgarg_getmember',
                                (u'alljoyn_msgarg', C.c_void_p),
                                ((u'alljoyn_msgarg', C.c_void_p), (u'int', C.c_int))),

                 u'GetNumMembers': (u'alljoyn_msgarg_getnummembers',
                                    (u'int', C.c_int),
                                    ((u'alljoyn_msgarg', C.c_void_p),)),

                 u'GetObjectPath': (u'alljoyn_msgarg_get_objectpath',
                                    (u'QStatus', C.c_uint),
                                    ((u'const alljoyn_msgarg', C.c_void_p),
                                     (u'char **', POINTER(C.c_char_p)))),

                 u'GetSignature': (u'alljoyn_msgarg_get_signature',
                                   (u'QStatus', C.c_uint),
                                   ((u'const alljoyn_msgarg', C.c_void_p),
                                    (u'char **', POINTER(C.c_char_p)))),

                 u'GetString': (u'alljoyn_msgarg_get_string',
                                (u'QStatus', C.c_uint),
                                ((u'const alljoyn_msgarg', POINTER(AlljoynMsgArg)),
                                 (u'char **', POINTER(C.c_char_p)))),

                 u'GetType': (u'alljoyn_msgarg_gettype',
                              (u'alljoyn_typeid', C.c_uint),
                              ((u'alljoyn_msgarg', C.c_void_p),)),


                 u'GetBoolArray': (u'alljoyn_msgarg_get_bool_array',
                                   (u'QStatus', C.c_uint),
                                   ((u'const alljoyn_msgarg', C.c_void_p),
                                    (u'int *', POINTER(C.c_int)),
                                    (u'int *', POINTER(C.c_int)))),


                 u'GetDoubleArray': (u'alljoyn_msgarg_get_double_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'const alljoyn_msgarg', C.c_void_p),
                                      (u'int *', POINTER(C.c_int)),
                                      (u'double *', POINTER(C.c_double)))),



                 u'GetInt16Array': (u'alljoyn_msgarg_get_int16_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'const alljoyn_msgarg', C.c_void_p),
                                     (u'int *', POINTER(C.c_int)),
                                     (u'int *', POINTER(C.c_short)))),

                 u'GetInt32Array': (u'alljoyn_msgarg_get_int32_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'const alljoyn_msgarg', C.c_void_p),
                                     (u'int *', POINTER(C.c_int)),
                                     (u'int *', POINTER(C.c_int)))),

                 u'GetInt64Array': (u'alljoyn_msgarg_get_int64_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'const alljoyn_msgarg', C.c_void_p),
                                     (u'int *', POINTER(C.c_int)),
                                     (u'int *', POINTER(C.c_longlong)))),

                 u'GetUInt16Array': (u'alljoyn_msgarg_get_uint16_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'const alljoyn_msgarg', C.c_void_p),
                                      (u'int *', POINTER(C.c_int)),
                                      (u'int *', POINTER(C.c_ushort)))),

                 u'GetUInt32Array': (u'alljoyn_msgarg_get_uint32_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'const alljoyn_msgarg', C.c_void_p),
                                      (u'int *', POINTER(C.c_int)),
                                      (u'int *', POINTER(C.c_uint)))),


                 u'GetUInt64Array': (u'alljoyn_msgarg_get_uint64_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'const alljoyn_msgarg', C.c_void_p),
                                      (u'int *', POINTER(C.c_int)),
                                      (u'int *', POINTER(C.c_ulonglong)))),


                 u'GetUInt8Array': (u'alljoyn_msgarg_get_uint8_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'const alljoyn_msgarg', C.c_void_p),
                                     (u'int *', POINTER(C.c_int)),
                                     (u'int *', POINTER(C.c_ubyte)))),

                 # u'GetValue': (u'alljoyn_msgarg_getvalue',
                 #               (u'alljoyn_msgarg', C.c_void_p),
                 #               ((u'alljoyn_msgarg', C.c_void_p),)),

                 u'GetVariant': (u'alljoyn_msgarg_get_variant',
                                 (u'QStatus', C.c_uint),
                                 ((u'const alljoyn_msgarg', C.c_void_p),
                                  (u'alljoyn_msgarg', C.c_void_p))),

                 u'GetVariantArray': (u'alljoyn_msgarg_get_variant_array',
                                      (u'QStatus', C.c_uint),
                                      ((u'const alljoyn_msgarg', C.c_void_p),
                                       (u'const char *', C.c_char_p),
                                       (u'int *', POINTER(C.c_int)),
                                       (u'alljoyn_msgarg *', POINTER(C.c_void_p)))),

                 u'HasSignature': (u'alljoyn_msgarg_hassignature',
                                   (u'int', C.c_int),
                                   ((u'alljoyn_msgarg', C.c_void_p),
                                    (u'const char *', C.c_char_p))),

                 u'Set': (u'alljoyn_msgarg_set',
                          (u'QStatus', C.c_uint),
                          ((u'alljoyn_msgarg', C.c_void_p),
                           (u'const char *', C.c_char_p))),

                 u'SetAndStabilize': (u'alljoyn_msgarg_set_and_stabilize',
                                      (u'QStatus', C.c_uint),
                                      ((u'alljoyn_msgarg', C.c_void_p),
                                       (u'const char *', C.c_char_p))),

                 u'SetBool': (u'alljoyn_msgarg_set_bool',
                              (u'QStatus', C.c_uint),
                              ((u'alljoyn_msgarg', C.c_void_p), (u'int', C.c_int))),

                 u'SetBoolArray': (u'alljoyn_msgarg_set_bool_array',
                                   (u'QStatus', C.c_uint),
                                   ((u'alljoyn_msgarg', C.c_void_p),
                                    (u'int', C.c_int),
                                    (u'int *', POINTER(C.c_int)))),

                 u'SetDictEntry': (u'alljoyn_msgarg_setdictentry',
                                   (u'QStatus', C.c_uint),
                                   ((u'alljoyn_msgarg', C.c_void_p),
                                    (u'alljoyn_msgarg', C.c_void_p),
                                    (u'alljoyn_msgarg', C.c_void_p))),

                 u'SetDouble': (u'alljoyn_msgarg_set_double',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_msgarg', C.c_void_p),
                                 (u'double', C.c_double))),

                 u'SetDoubleArray': (u'alljoyn_msgarg_set_double_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', C.c_void_p),
                                      (u'int', C.c_int),
                                      (u'double *', POINTER(C.c_double)))),

                 u'SetInt16': (u'alljoyn_msgarg_set_int16',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_msgarg', C.c_void_p), (u'int', C.c_int))),

                 u'SetInt16Array': (u'alljoyn_msgarg_set_int16_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_msgarg', C.c_void_p),
                                     (u'int', C.c_int),
                                     (u'int *', POINTER(C.c_int)))),

                 u'SetInt32': (u'alljoyn_msgarg_set_int32',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_msgarg', C.c_void_p), (u'int', C.c_int))),

                 u'SetInt32Array': (u'alljoyn_msgarg_set_int32_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_msgarg', C.c_void_p),
                                     (u'int', C.c_int),
                                     (u'int *', POINTER(C.c_int)))),

                 u'SetInt64': (u'alljoyn_msgarg_set_int64',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_msgarg', C.c_void_p), (u'int', C.c_int))),

                 u'SetInt64Array': (u'alljoyn_msgarg_set_int64_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_msgarg', C.c_void_p),
                                     (u'int', C.c_int),
                                     (u'int *', POINTER(C.c_int)))),

                 u'SetObjectPath': (u'alljoyn_msgarg_set_objectpath',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_msgarg', C.c_void_p),
                                     (u'const char *', C.c_char_p))),

                 u'SetObjectPathArray': (u'alljoyn_msgarg_set_objectpath_array',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_msgarg', C.c_void_p),
                                          (u'int', C.c_int),
                                          (u'const char **', POINTER(C.c_char_p)))),

                 u'SetSignature': (u'alljoyn_msgarg_set_signature',
                                   (u'QStatus', C.c_uint),
                                   ((u'alljoyn_msgarg', C.c_void_p),
                                    (u'const char *', C.c_char_p))),

                 u'SetSignatureArray': (u'alljoyn_msgarg_set_signature_array',
                                        (u'QStatus', C.c_uint),
                                        ((u'alljoyn_msgarg', C.c_void_p),
                                         (u'int', C.c_int),
                                         (u'const char **', POINTER(C.c_char_p)))),

                 u'SetString': (u'alljoyn_msgarg_set_string',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_msgarg', C.c_void_p),
                                 (u'const char *', C.c_char_p))),

                 u'SetStringArray': (u'alljoyn_msgarg_set_string_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', C.c_void_p),
                                      (u'int', C.c_int),
                                      (u'const char **', POINTER(C.c_char_p)))),

                 u'SetUInt16': (u'alljoyn_msgarg_set_uint16',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_msgarg', C.c_void_p), (u'int', C.c_int))),

                 u'SetUInt16Array': (u'alljoyn_msgarg_set_uint16_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', C.c_void_p),
                                      (u'int', C.c_int),
                                      (u'int *', POINTER(C.c_int)))),

                 u'SetUInt32': (u'alljoyn_msgarg_set_uint32',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_msgarg', C.c_void_p), (u'int', C.c_int))),

                 u'SetUInt32Array': (u'alljoyn_msgarg_set_uint32_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', C.c_void_p),
                                      (u'int', C.c_int),
                                      (u'int *', POINTER(C.c_int)))),

                 u'SetUInt64': (u'alljoyn_msgarg_set_uint64',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_msgarg', C.c_void_p), (u'int', C.c_int))),

                 u'SetUInt64Array': (u'alljoyn_msgarg_set_uint64_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', C.c_void_p),
                                      (u'int', C.c_int),
                                      (u'int *', POINTER(C.c_int)))),

                 u'SetUInt8': (u'alljoyn_msgarg_set_uint8',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_msgarg', C.c_void_p), (u'int', C.c_int))),

                 u'SetUInt8Array': (u'alljoyn_msgarg_set_uint8_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_msgarg', C.c_void_p),
                                     (u'int', C.c_int),
                                     (u'int *', POINTER(C.c_int)))),

                 u'SetStruct': (u'alljoyn_msgarg_setstruct',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_msgarg', C.c_void_p),
                                 (u'alljoyn_msgarg', C.c_void_p),
                                 (u'int', C.c_int))),

                 u'Signature': (u'alljoyn_msgarg_signature', (u'int', C.c_int),
                                ((u'alljoyn_msgarg', C.c_void_p), (u'char *', C.c_char_p), (u'size_t', C.c_size_t))),

                 u'Stabilize': (u'alljoyn_msgarg_stabilize',
                                (u'void', None),
                                ((u'alljoyn_msgarg', C.c_void_p),)),

                 u'ToString': (u'alljoyn_msgarg_tostring',
                               (u'int', C.c_int),
                               ((u'alljoyn_msgarg', C.c_void_p),
                                (u'char *', C.c_char_p),
                                (u'int', C.c_int),
                                (u'int', C.c_int)))}

    def __init__(self, handle=None):
        if handle:
            self.handle = handle
        else:
            self.handle = self._Create()

    def __del__(self):
        if self.handle:
            pass
            # self._Destroy(self.handle)
            # print "destroyed"

    # Wrapper Methods

    @staticmethod
    def Create():
        return MsgArg._Create()

    def CreateAndSet(self):
        return self._CreateAndSet(self.handle)

    def ArrayCreate(self):
        return self._ArrayCreate(self.handle)

    def ArrayElement(self, index):
        return self._ArrayElement(self.handle, index)  # int

    def Set(self, signature):
        return self._Set(self.handle, signature)  # const char *

    def Get(self, signature):
        return self._Get(self.handle, signature)  # const char *

    def Copy(self):
        return self._Copy(self.handle)

    def Clone(self, source):
        return self._Clone(self.handle, source)  # const alljoyn_msgarg

    def Equal(self, rhv):
        return self._Equal(self.handle, rhv)  # alljoyn_msgarg

    def ArraySet(self, numArgs, signature):
        return self._ArraySet(self.handle, numArgs, signature)  # int *,const char *

    def ArrayGet(self, numArgs, signature):
        return self._ArrayGet(self.handle, numArgs, signature)  # int,const char *

    def ToString(self, str, buf, indent):
        #buf = C.create_string_buffer(size)
        return self._ToString(self.handle, str, buf, indent)  # char *,int,int

    def ArrayToString(self, numArgs, str, buf, indent):
        return self._ArrayToString(self.handle, numArgs, str, buf, indent)  # int,char *,int,int

    def Signature(self):
        size = self._Signature(self.handle, None, 0)
        buf = C.create_string_buffer(size)
        self._Signature(self.handle, buf, size)  # char *,int
        return buf.value.strip()

    def ArraySignature(self, numValues, str, buf):
        return self._ArraySignature(self.handle, numValues, str, buf)  # int,char *,int

    def HasSignature(self, signature):
        return self._HasSignature(self.handle, signature)  # const char *

    def GetDictElement(self, elemSig):
        return self._GetDictElement(self.handle, elemSig)  # const char *

    def GetType(self):
        return self._GetType(self.handle)

    def Clear(self):
        return self._Clear(self.handle)

    def Stabilize(self):
        return self._Stabilize(self.handle)

    def ArraySetOffset(self, argOffset, numArgs, signature):
        return self._ArraySetOffset(self.handle, argOffset, numArgs, signature)  # int,int *,const char *

    def SetAndStabilize(self, signature):
        return self._SetAndStabilize(self.handle, signature)  # const char *

    # def SetValue(self, value):

    def Get(self, signature, *args):
        pass
        #printf.argtypes = [c_char_p, c_char_p, c_int, c_double]
        #printf("String '%s', Int %d, Double %f\n", "Hi", 10, 2.2)
        # String 'Hi', Int 10, Double 2.200000

    def GetSingleCompleteValue(self):
        # See https://dbus.freedesktop.org/doc/dbus-specification.html
        # https://dbus.freedesktop.org/releases/dbus-python/dbus-python-0.83.2.tar.gz
        # STRUCT, Array, VARIANT, and DICT_ENTRY. container types
        sig = self.Signature()

        if len(sig) == 1:
            # Return basic type
            first_ch = sig[0]
            ctype = sig_map[first_ch][0]()
            method = sig_map[first_ch][1]
            method(self.handle, ctype, C.byref(ctype))
            return ctype.value
        elif len(sig) == 2:
            first_ch = sig[0]
            sec_ch = sig[1]

            if first_ch == 'a':

                

                length = C.c_int()
                array = (sig_map[sec_ch][0] * 1)()
                method = sig_map[sec_ch][3]
                method(self.handle, C.byref(length), array)


                print "sec_ch", sec_ch
                print "length", length.value
                print "type", sig_map[sec_ch][0]
                print "method", sig_map[sec_ch]

                # print "real size", length.value
                # Call again getting the real number of elements
                array = (sig_map[sec_ch][0] * length.value)()
                method(self.handle, C.byref(length), array)
                print "array", array
                l = []
                return [a for a in array]

    # def GetVariant(self, v):
    # return self._GetVariant(self.handle,v) # alljoyn_msgarg

    def GetVariantArray(self, signature, length, av):
        return self._GetVariantArray(self.handle, signature, length, av)  # const char *,int *,alljoyn_msgarg *

    def GetArrayNumberOfElements(self):
        return self._GetArrayNumberOfElements(self.handle)

    def GetArrayElement(self, index, element):
        return self._GetArrayElement(self.handle, index, element)  # int,alljoyn_msgarg *

    def GetArrayElementSignature(self, index):
        return self._GetArrayElementSignature(self.handle, index)  # int

    def GetKey(self):
        return self._GetKey(self.handle)

    def GetValue(self):
        return self._GetValue(self.handle)

    def SetDictEntry(self, key, value):
        return self._SetDictEntry(self.handle, key, value)  # alljoyn_msgarg,alljoyn_msgarg

    def SetsTRUCT(self, struct_members, num_members):
        return self._SetsTRUCT(self.handle, struct_members, num_members)  # alljoyn_msgarg,int

    def GetNumMembers(self):
        return self._GetNumMembers(self.handle)

    def GetMember(self, index):
        return self._GetMember(self.handle, index)  # int


MsgArg.bind_functions_to_cls()


sig_map = {
    "y": (C.c_ubyte, MsgArg._GetUInt8, MsgArg._SetUInt8, MsgArg._GetUInt8Array, MsgArg._SetUInt8Array),
    "b": (C.c_byte, MsgArg._GetBool, MsgArg._SetBool, MsgArg._GetBoolArray, MsgArg._SetBoolArray),
    "n": (C.c_short, MsgArg._GetInt16, MsgArg._SetInt16, MsgArg._GetInt16Array, MsgArg._SetInt16Array),
    "q": (C.c_ushort, MsgArg._GetUInt16, MsgArg._SetUInt16, MsgArg._GetUInt16Array, MsgArg._SetUInt16Array),
    "i": (C.c_int, MsgArg._GetInt32, MsgArg._SetInt32, MsgArg._GetInt32Array, MsgArg._SetInt32Array),
    "u": (C.c_uint, MsgArg._GetUInt32, MsgArg._SetUInt32, MsgArg._GetUInt32Array, MsgArg._SetUInt32Array),
    "x": (C.c_longlong, MsgArg._GetInt64, MsgArg._SetInt64, MsgArg._GetInt64Array, MsgArg._SetInt64Array),
    "t": (C.c_ulonglong, MsgArg._GetUInt64, MsgArg._SetUInt64, MsgArg._GetUInt64Array, MsgArg._SetUInt64Array),
    "d": (C.c_double, MsgArg._GetDouble, MsgArg._SetDouble, MsgArg._GetDoubleArray, MsgArg._SetDoubleArray),
    "s": (C.c_char_p, MsgArg._GetString, MsgArg._SetString, None, None),
    #"o": (C.c_char_p, MsgArg._GetObjectPath, MsgArg._SetObjectPath, MsgArg._SetObjectPathArray, MsgArg._GetObjectPathArray),
    #"g": (C.c_char_p, MsgArg._GetSignature, MsgArg._SetSignature, MsgArg._SetSignatureArray, MsgArg._GetSignatureArray),
}
