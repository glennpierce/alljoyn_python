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
import types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import *
# Wrapper for file MsgArg.h


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
                                  (u'alljoyn_msgarg', MsgArgHandle),
                                  ((u'int', C.c_int),)),

                 u'ArrayElement': (u'alljoyn_msgarg_array_element',
                                   (u'alljoyn_msgarg', MsgArgHandle),
                                   ((u'alljoyn_msgarg', MsgArgHandle), (u'size_t', C.c_size_t))),

                 u'ArrayGet': (u'alljoyn_msgarg_array_get',
                               (u'QStatus', C.c_uint),
                               ((u'const alljoyn_msgarg', MsgArgHandle),
                                   (u'int', C.c_int),
                                   (u'const char *', C.c_char_p))),

                 # u'ArraySet': (u'alljoyn_msgarg_array_set',
                 #               (u'QStatus', C.c_uint),
                 #               ((u'alljoyn_msgarg', MsgArgHandle),
                 #                   (u'size_t *', POINTER(C.c_size_t)),
                 #                   (u'const char *', C.c_char_p))),

                 u'ArraySetOffset': (u'alljoyn_msgarg_array_set_offset',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', MsgArgHandle),
                                         (u'int', C.c_int),
                                         (u'int *', POINTER(C.c_int)),
                                         (u'const char *', C.c_char_p))),

                 u'ArraySignature': (u'alljoyn_msgarg_array_signature',
                                     (u'int', C.c_int),
                                     ((u'alljoyn_msgarg', MsgArgHandle),
                                         (u'int', C.c_int),
                                         (u'char *', C.c_char_p),
                                         (u'int', C.c_int))),

                 u'ArrayToString': (u'alljoyn_msgarg_array_tostring',
                                    (u'int', C.c_int),
                                    ((u'const alljoyn_msgarg', MsgArgHandle),
                                        (u'int', C.c_int),
                                        (u'char *', C.c_char_p),
                                        (u'int', C.c_int),
                                        (u'int', C.c_int))),

                 u'Clear': (u'alljoyn_msgarg_clear',
                            (u'void', None),
                            ((u'alljoyn_msgarg', MsgArgHandle),)),

                 u'Clone': (u'alljoyn_msgarg_clone',
                            (u'void', None),
                            ((u'alljoyn_msgarg', MsgArgHandle),
                                (u'const alljoyn_msgarg', MsgArgHandle))),

                 u'Copy': (u'alljoyn_msgarg_copy',
                           (u'alljoyn_msgarg', MsgArgHandle),
                           ((u'const alljoyn_msgarg', MsgArgHandle),)),

                 u'Create': (u'alljoyn_msgarg_create', (u'alljoyn_msgarg', MsgArgHandle), []),

                 u'CreateAndSet': (u'alljoyn_msgarg_create_and_set',
                                   (u'alljoyn_msgarg', MsgArgHandle),
                                   ((u'const char *', C.c_char_p),)),

                 u'Destroy': (u'alljoyn_msgarg_destroy', (u'void', None),
                              ((u'alljoyn_msgarg', MsgArgHandle),)),

                 u'Equal': (u'alljoyn_msgarg_equal',
                            (u'int', C.c_int),
                            ((u'alljoyn_msgarg', MsgArgHandle),
                             (u'alljoyn_msgarg', MsgArgHandle))),

                 u'GetArrayElement': (u'alljoyn_msgarg_get_array_element',
                                      (u'void', None),
                                      ((u'const alljoyn_msgarg', MsgArgHandle),
                                       (u'int', C.c_int),
                                       (u'alljoyn_msgarg *', POINTER(C.c_void_p)))),

                 u'GetArrayElementSignature': (u'alljoyn_msgarg_get_array_elementsignature',
                                               (u'const char *', C.c_char_p),
                                               ((u'const alljoyn_msgarg', MsgArgHandle),
                                                (u'int', C.c_int))),

                 u'GetArrayNumberOfElements': (u'alljoyn_msgarg_get_array_numberofelements',
                                               (u'int', C.c_int),
                                               ((u'const alljoyn_msgarg', MsgArgHandle),)),

                 u'GetDictElement': (u'alljoyn_msgarg_getdictelement',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', MsgArgHandle),
                                      (u'const char *', C.c_char_p))),


                 u'GetBool': (u'alljoyn_msgarg_get_bool',
                              (u'QStatus', C.c_uint),
                              ((u'const alljoyn_msgarg', MsgArgHandle),
                               (u'int *', POINTER(C.c_byte)))),

                 u'GetUInt8': (u'alljoyn_msgarg_get_uint8',
                               (u'QStatus', C.c_uint),
                               ((u'const alljoyn_msgarg', MsgArgHandle),
                                (u'int *', POINTER(C.c_ubyte)))),

                 u'GetInt16': (u'alljoyn_msgarg_get_int16',
                               (u'QStatus', C.c_uint),
                               ((u'const alljoyn_msgarg', MsgArgHandle),
                                (u'int *', POINTER(C.c_short)))),

                 u'GetUInt16': (u'alljoyn_msgarg_get_uint16',
                                (u'QStatus', C.c_uint),
                                ((u'const alljoyn_msgarg', MsgArgHandle),
                                 (u'int *', POINTER(C.c_ushort)))),

                 u'GetInt32': (u'alljoyn_msgarg_get_int32',
                               (u'QStatus', C.c_uint),
                               ((u'const alljoyn_msgarg', MsgArgHandle),
                                (u'int *', POINTER(C.c_int)))),

                 u'GetUInt32': (u'alljoyn_msgarg_get_uint32',
                                (u'QStatus', C.c_uint),
                                ((u'const alljoyn_msgarg', MsgArgHandle),
                                 (u'int *', POINTER(C.c_uint)))),

                 u'GetInt64': (u'alljoyn_msgarg_get_int64',
                               (u'QStatus', C.c_uint),
                               ((u'const alljoyn_msgarg', MsgArgHandle),
                                (u'int *', POINTER(C.c_longlong)))),

                 u'GetUInt64': (u'alljoyn_msgarg_get_uint64',
                                (u'QStatus', C.c_uint),
                                ((u'const alljoyn_msgarg', MsgArgHandle),
                                 (u'int *', POINTER(C.c_ulonglong)))),

                 u'GetDouble': (u'alljoyn_msgarg_get_double',
                                (u'QStatus', C.c_uint),
                                ((u'const alljoyn_msgarg', MsgArgHandle),
                                 (u'double *', POINTER(C.c_double)))),

                 u'GetKey': (u'alljoyn_msgarg_getkey',
                             (u'alljoyn_msgarg', MsgArgHandle),
                             ((u'alljoyn_msgarg', MsgArgHandle),)),

                 u'GetMember': (u'alljoyn_msgarg_getmember',
                                (u'alljoyn_msgarg', MsgArgHandle),
                                ((u'alljoyn_msgarg', MsgArgHandle), (u'int', C.c_int))),

                 u'GetNumMembers': (u'alljoyn_msgarg_getnummembers',
                                    (u'int', C.c_int),
                                    ((u'alljoyn_msgarg', MsgArgHandle),)),

                 u'GetObjectPath': (u'alljoyn_msgarg_get_objectpath',
                                    (u'QStatus', C.c_uint),
                                    ((u'const alljoyn_msgarg', MsgArgHandle),
                                     (u'char **', POINTER(C.c_char_p)))),

                 u'GetSignature': (u'alljoyn_msgarg_get_signature',
                                   (u'QStatus', C.c_uint),
                                   ((u'const alljoyn_msgarg', MsgArgHandle),
                                    (u'char **', POINTER(C.c_char_p)))),

                 u'GetString': (u'alljoyn_msgarg_get_string',
                                (u'QStatus', C.c_uint),
                                ((u'const alljoyn_msgarg', MsgArgHandle),
                                 (u'char **', POINTER(C.c_char_p)))),

                 u'GetType': (u'alljoyn_msgarg_gettype',
                              (u'alljoyn_typeid', C.c_uint),
                              ((u'alljoyn_msgarg', MsgArgHandle),)),

                 u'GetBoolArray': (u'alljoyn_msgarg_get_bool_array',
                                   (u'QStatus', C.c_uint),
                                   ((u'const alljoyn_msgarg', MsgArgHandle),
                                    (u'size_t *', POINTER(C.c_int)),
                                    (u'int *', POINTER(C.c_int)))),

                 u'GetUInt8Array': (u'alljoyn_msgarg_get_uint8_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'const alljoyn_msgarg', MsgArgHandle),
                                     (u'size_t *', POINTER(C.c_size_t)),
                                     (u'int *', POINTER(POINTER(C.c_ubyte))))),

                 u'GetInt16Array': (u'alljoyn_msgarg_get_int16_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'const alljoyn_msgarg', MsgArgHandle),
                                     (u'size_t *', POINTER(C.c_size_t)),
                                     (u'int *', POINTER(C.c_short)))),

                 u'GetInt32Array': (u'alljoyn_msgarg_get_int32_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'const alljoyn_msgarg', MsgArgHandle),
                                     (u'size_t *', POINTER(C.c_size_t)),
                                     (u'int *', POINTER(C.c_int)))),

                 u'GetInt64Array': (u'alljoyn_msgarg_get_int64_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'const alljoyn_msgarg', MsgArgHandle),
                                     (u'size_t *', POINTER(C.c_size_t)),
                                     (u'int *', POINTER(C.c_longlong)))),

                 u'GetUInt16Array': (u'alljoyn_msgarg_get_uint16_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'const alljoyn_msgarg', MsgArgHandle),
                                      (u'size_t *', POINTER(C.c_size_t)),
                                      (u'int *', POINTER(C.c_ushort)))),

                 u'GetUInt32Array': (u'alljoyn_msgarg_get_uint32_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'const alljoyn_msgarg', MsgArgHandle),
                                      (u'size_t *', POINTER(C.c_size_t)),
                                      (u'int *', POINTER(C.c_uint)))),

                 u'GetUInt64Array': (u'alljoyn_msgarg_get_uint64_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'const alljoyn_msgarg', MsgArgHandle),
                                      (u'size_t *', POINTER(C.c_size_t)),
                                      (u'int *', POINTER(C.c_ulonglong)))),

                 u'GetDoubleArray': (u'alljoyn_msgarg_get_double_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'const alljoyn_msgarg', MsgArgHandle),
                                      (u'size_t *', POINTER(C.c_size_t)),
                                      (u'double *', POINTER(C.c_double)))),
   
#                 u'GetStringArray': (u'alljoyn_msgarg_get',
#                                     (u'QStatus', C.c_uint),
#                                     ((u'const alljoyn_msgarg', MsgArgHandle),
#                                      (u'char *', C.c_char_p),
#                                      (u'int *', POINTER(C.c_int)),
#                                      (u'msgarg *',POINTER(POINTER(AlljoynMsgArg))))),
                 
                 # u'GetValue': (u'alljoyn_msgarg_getvalue',
                 #               (u'alljoyn_msgarg', MsgArgHandle),
                 #               ((u'alljoyn_msgarg', MsgArgHandle),)),

                 u'GetVariant': (u'alljoyn_msgarg_get_variant',
                                 (u'QStatus', C.c_uint),
                                 ((u'const alljoyn_msgarg', MsgArgHandle),
                                  (u'alljoyn_msgarg', MsgArgHandle))),

                 u'GetVariantArray': (u'alljoyn_msgarg_get_variant_array',
                                      (u'QStatus', C.c_uint),
                                      ((u'const alljoyn_msgarg', MsgArgHandle),
                                       (u'const char *', C.c_char_p),
                                       (u'int *', POINTER(C.c_int)),
                                       (u'alljoyn_msgarg *', POINTER(C.c_void_p)))),

                 u'HasSignature': (u'alljoyn_msgarg_hassignature',
                                   (u'int', C.c_int),
                                   ((u'alljoyn_msgarg', MsgArgHandle),
                                    (u'const char *', C.c_char_p))),

#                 u'Set': (u'alljoyn_msgarg_set',
#                          (u'QStatus', C.c_uint),
#                          ((u'alljoyn_msgarg', MsgArgHandle),
#                           (u'const char *', C.c_char_p))),

                 u'SetAndStabilize': (u'alljoyn_msgarg_set_and_stabilize',
                                      (u'QStatus', C.c_uint),
                                      ((u'alljoyn_msgarg', MsgArgHandle),
                                       (u'const char *', C.c_char_p))),

                 

                 u'SetBoolArray': (u'alljoyn_msgarg_set_bool_array',
                                   (u'QStatus', C.c_uint),
                                   ((u'alljoyn_msgarg', MsgArgHandle),
                                    (u'int', C.c_int),
                                    (u'int *', POINTER(C.c_int)))),

                 u'SetDictEntry': (u'alljoyn_msgarg_setdictentry',
                                   (u'QStatus', C.c_uint),
                                   ((u'alljoyn_msgarg', MsgArgHandle),
                                    (u'alljoyn_msgarg', MsgArgHandle),
                                    (u'alljoyn_msgarg', MsgArgHandle))),

                 u'SetBool': (u'alljoyn_msgarg_set_bool',
                              (u'QStatus', C.c_uint),
                              ((u'alljoyn_msgarg', MsgArgHandle), (u'int', C.c_int))),
                 
                 
                 u'SetUInt8': (u'alljoyn_msgarg_set_uint8',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_msgarg', MsgArgHandle), (u'int', C.c_int))),
                 
                 u'SetInt16': (u'alljoyn_msgarg_set_int16',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_msgarg', MsgArgHandle), (u'int', C.c_int))),
                 
                 u'SetUInt16': (u'alljoyn_msgarg_set_uint16',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_msgarg', MsgArgHandle), (u'int', C.c_int))),

                 u'SetUInt32': (u'alljoyn_msgarg_set_uint32',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_msgarg', MsgArgHandle), (u'int', C.c_int))),
                 
                 u'SetInt32': (u'alljoyn_msgarg_set_int32',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_msgarg', MsgArgHandle), (u'int', C.c_int))),
                 
                 u'SetInt64': (u'alljoyn_msgarg_set_int64',
                               (u'QStatus', C.c_uint),
                               ((u'alljoyn_msgarg', MsgArgHandle), (u'int', C.c_longlong))),
                 
                 u'SetUInt64': (u'alljoyn_msgarg_set_uint64',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_msgarg', MsgArgHandle), (u'int', C.c_int))),
                 
                 u'SetDouble': (u'alljoyn_msgarg_set_double',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_msgarg', MsgArgHandle),
                                 (u'double', C.c_double))),

                 u'SetDoubleArray': (u'alljoyn_msgarg_set_double_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', MsgArgHandle),
                                      (u'int', C.c_int),
                                      (u'double *', POINTER(C.c_double)))),

                 u'SetInt16Array': (u'alljoyn_msgarg_set_int16_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_msgarg', MsgArgHandle),
                                     (u'int', C.c_int),
                                     (u'int *', POINTER(C.c_int)))),

                 u'SetInt32Array': (u'alljoyn_msgarg_set_int32_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_msgarg', MsgArgHandle),
                                     (u'int', C.c_int),
                                     (u'int *', POINTER(C.c_int)))),
       
                 u'SetInt64Array': (u'alljoyn_msgarg_set_int64_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_msgarg', MsgArgHandle),
                                     (u'int', C.c_int),
                                     (u'int *', POINTER(C.c_int)))),

                 u'SetObjectPath': (u'alljoyn_msgarg_set_objectpath',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_msgarg', MsgArgHandle),
                                     (u'const char *', C.c_char_p))),

                 u'SetObjectPathArray': (u'alljoyn_msgarg_set_objectpath_array',
                                         (u'QStatus', C.c_uint),
                                         ((u'alljoyn_msgarg', MsgArgHandle),
                                          (u'int', C.c_int),
                                          (u'const char **', POINTER(C.c_char_p)))),

                 u'SetSignature': (u'alljoyn_msgarg_set_signature',
                                   (u'QStatus', C.c_uint),
                                   ((u'alljoyn_msgarg', MsgArgHandle),
                                    (u'const char *', C.c_char_p))),

                 u'SetSignatureArray': (u'alljoyn_msgarg_set_signature_array',
                                        (u'QStatus', C.c_uint),
                                        ((u'alljoyn_msgarg', MsgArgHandle),
                                         (u'int', C.c_int),
                                         (u'const char **', POINTER(C.c_char_p)))),

                 u'SetString': (u'alljoyn_msgarg_set_string',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_msgarg', MsgArgHandle),
                                 (u'const char *', C.c_char_p))),

                 u'SetStringArray': (u'alljoyn_msgarg_set_string_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', MsgArgHandle),
                                      (u'int', C.c_int),
                                      (u'const char **', POINTER(C.c_char_p)))),
                 
                 u'SetUInt16Array': (u'alljoyn_msgarg_set_uint16_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', MsgArgHandle),
                                      (u'int', C.c_int),
                                      (u'int *', POINTER(C.c_int)))),

                 u'SetUInt32Array': (u'alljoyn_msgarg_set_uint32_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', MsgArgHandle),
                                      (u'int', C.c_int),
                                      (u'int *', POINTER(C.c_int)))),

                 u'SetUInt64Array': (u'alljoyn_msgarg_set_uint64_array',
                                     (u'QStatus', C.c_uint),
                                     ((u'alljoyn_msgarg', MsgArgHandle),
                                      (u'int', C.c_int),
                                      (u'int *', POINTER(C.c_int)))),

                 u'SetUInt8Array': (u'alljoyn_msgarg_set_uint8_array',
                                    (u'QStatus', C.c_uint),
                                    ((u'alljoyn_msgarg', MsgArgHandle),
                                     (u'int', C.c_int),
                                     (u'int *', POINTER(C.c_int)))),

                 u'SetStruct': (u'alljoyn_msgarg_setstruct',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_msgarg', MsgArgHandle),
                                 (u'alljoyn_msgarg', MsgArgHandle),
                                 (u'int', C.c_int))),

                 u'Signature': (u'alljoyn_msgarg_signature', (u'int', C.c_int),
                                ((u'alljoyn_msgarg', MsgArgHandle), (u'char *', C.c_char_p), (u'size_t', C.c_size_t))),

                 u'Stabilize': (u'alljoyn_msgarg_stabilize',
                                (u'void', None),
                                ((u'alljoyn_msgarg', MsgArgHandle),)),

                 u'ToString': (u'alljoyn_msgarg_tostring',
                               (u'int', C.c_int),
                               ((u'alljoyn_msgarg', MsgArgHandle),
                                (u'char *', C.c_char_p),
                                (u'int', C.c_int),
                                (u'int', C.c_int)))}


    def __init__(self):
        self.handle = self._Create()

    def __del__(self):
        if self.handle:
          pass
          #print traceback.print_stack()
          #self._Destroy(self.handle)
  
    @classmethod
    def FromHandle(cls, handle):
        assert type(handle) == MsgArgHandle
        instance = cls()
        instance.handle = handle

        return instance
        

    def Destroy(self):
      self._Destroy(self.handle)

    # Wrapper Methods
    def CreateAndSet(self):
        return self._CreateAndSet(self.handle)

    @classmethod
    def ArrayCreate(cls, number_of_elements):
        instance = cls()
        instance.handle = MsgArg._ArrayCreate(number_of_elements)
        return instance

    def ArrayElement(self, index):
        return MsgArg.FromHandle(self._ArrayElement(self.handle, index)) 

    def Copy(self):
        return MsgArg(self._Copy(self.handle))

    def Clone(self, source):
        return self._Clone(self.handle, source)  # const alljoyn_msgarg

    def Equal(self, rhv):
        return self._Equal(self.handle, rhv)  # alljoyn_msgarg

  
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
        return buf.value

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
    
    @classmethod
    def NumericListReturnMarshaller(cls, handle, signature):
        length = C.c_size_t()
        method = sig_map[signature][3]
        ctype = sig_map[signature][0]
        p = C.pointer(ctype())
        method(handle, C.byref(length), C.byref(p))
        l = []
        for i in range(length.value):
            l.append(p[i])
        return l
    
    @classmethod
    def StringListReturnMarshaller(cls, handle, signature):
        return cls._GetStringArray(handle)
    
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
                marshaller =  sig_map[sec_ch][5]
                return marshaller(self.handle, sec_ch)
            else:
                raise AttributeError("GetSingleCompleteValue only supports simple types and arrays of simple types")
                
    def SetSingleCompleteValue(self, signature, value):
        if len(sig) == 1:
            # Return basic type
            first_ch = sig[0]
            ctype = sig_map[first_ch][0]()
            method = sig_map[first_ch][2]
            return method(self.handle, ctype, value)
        elif len(sig) == 2:
            first_ch = sig[0]
            sec_ch = sig[1]

            if first_ch == 'a':
                marshaller =  sig_map[sec_ch][5]
                return marshaller(self.handle, sec_ch)
            else:
                raise AttributeError("GetSingleCompleteValue only supports simple types and arrays of simple types")
        

    @classmethod
    def _Set(cls, handle, signature, ctypes_list, argument_list):
        # expects list of args as ctypes and the arguments themselves

        #if len(ctypes_list) != len(argument_list):
        #    raise AttributeError("Wrong number of parameters") 

        method = AllJoynObject._lib.alljoyn_msgarg_set
        method.restype = C.c_uint
        method.argtypes = ([C.c_void_p, C.c_char_p] + ctypes_list)
        arguments = [handle, signature] + argument_list
        return AllJoynObject.QStatusToException(method(*arguments))
        
    def Set(self, signature, ctypes_list, argument_list):
        return self._Set(self.handle, signature, ctypes_list, argument_list)
    
    @classmethod
    def _ArraySet(cls, handle, num_args, signature, ctypes_list, argument_list):
        # expects list of args as ctypes and the arguments themselves

        # QStatus alljoyn_msgarg_array_set(alljoyn_msgarg args, size_t* numArgs, const char* signature, ...);

        if len(ctypes_list) != len(argument_list):
            raise AttributeError("Wrong number of parameters") 

        method = AllJoynObject._lib.alljoyn_msgarg_array_set
        method.restype = C.c_uint
        size = C.c_size_t(num_args)
        method.argtypes = ([MsgArgHandle, POINTER(C.c_size_t), C.c_char_p] + ctypes_list)
        arguments = [handle, C.byref(size), signature] + argument_list

        return AllJoynObject.QStatusToException(method(*arguments))

    def ArraySet(self, num_args, signature, ctypes_list, argument_list):
        return self._ArraySet(self.handle, num_args, signature, ctypes_list, argument_list)  

    @classmethod
    def _Get(cls, handle, signature, ctypes_list, argument_list):
        # expects list of args as ctypes and the arguments themselves

        if len(ctypes_list) != len(argument_list):
            raise AttributeError("Wrong number of parameters") 

        method = AllJoynObject._lib.alljoyn_msgarg_get
        method.restype = C.c_uint
        method.argtypes = ([MsgArgHandle, C.c_char_p] + ctypes_list)
        arguments = [handle, signature] + argument_list
        return AllJoynObject.QStatusToException(method(*arguments))

    def Get(self, signature, ctypes_list, argument_list):
        return self._Get(self.handle, signature, ctypes_list, argument_list)
    
    @classmethod
    def _GetStringArray(cls, handle):
        length = C.c_size_t()
        msgarg_handle = cls._Create()
        cls._Get(handle, "as", [POINTER(C.c_size_t), POINTER(MsgArgHandle)], [C.byref(length), C.byref(msgarg_handle)])
        msgarg = MsgArg.FromHandle(msgarg_handle)   
        result = []

        for i in range(length.value):
            stringRet = C.c_char_p()
            msgarg.ArrayElement(i).Get("s", [POINTER(C.c_char_p)], [C.byref(stringRet)])
            result.append(stringRet.value)

        return result
     
    def GetStringArray(self):
        return self._GetStringArray(self.handle)

    def SetString(self, string):
        return self._SetString(self.handle, C.create_string_buffer(string).raw)

    def GetString(self):
        #buf = C.create_string_buffer(100)
        buf = C.c_char_p()
        #self._GetString(self.handle, C.byref(buf))
        self._GetString(self.handle, buf)

        return buf.value

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

    def SetStruct(self, struct_members, num_members):
        return self._SetStruct(self.handle, struct_members, num_members)  # alljoyn_msgarg,int

    def GetNumMembers(self):
        return self._GetNumMembers(self.handle)

    def GetMember(self, index):
        return self._GetMember(self.handle, index)  # int

    def SetBool(self, value):
        return self._SetBool(self.handle, value)

    def GetBool(self):
        value = C.c_byte()
        self._GetBool(self.handle, C.byref(value))
        return value.value

    def GetInt32(self):
        value = C.c_int32()
        self._GetInt32(self.handle, C.byref(value))
        return value.value

    def SetInt16(self, value):
        return self._SetInt16(self.handle, value)

    def GetInt16(self):
        value = C.c_short()
        self._GetInt16(self.handle, C.byref(value))
        return value.value

    def SetInt64(self, value):
        return self._SetInt64(self.handle, value)

    def SetDouble(self, value):
        return self._SetDouble(self.handle, value)

MsgArg.bind_functions_to_cls()


sig_map = {
    "y": (C.c_ubyte, MsgArg._GetUInt8, MsgArg._SetUInt8, MsgArg._GetUInt8Array, MsgArg._SetUInt8Array, MsgArg.NumericListReturnMarshaller),
    "b": (C.c_byte, MsgArg._GetBool, MsgArg._SetBool, MsgArg._GetBoolArray, MsgArg._SetBoolArray, MsgArg.NumericListReturnMarshaller),
    "n": (C.c_short, MsgArg._GetInt16, MsgArg._SetInt16, MsgArg._GetInt16Array, MsgArg._SetInt16Array, MsgArg.NumericListReturnMarshaller),
    "q": (C.c_ushort, MsgArg._GetUInt16, MsgArg._SetUInt16, MsgArg._GetUInt16Array, MsgArg._SetUInt16Array, MsgArg.NumericListReturnMarshaller),
    "i": (C.c_int, MsgArg._GetInt32, MsgArg._SetInt32, MsgArg._GetInt32Array, MsgArg._SetInt32Array, MsgArg.NumericListReturnMarshaller),
    "u": (C.c_uint, MsgArg._GetUInt32, MsgArg._SetUInt32, MsgArg._GetUInt32Array, MsgArg._SetUInt32Array, MsgArg.NumericListReturnMarshaller),
    "x": (C.c_longlong, MsgArg._GetInt64, MsgArg._SetInt64, MsgArg._GetInt64Array, MsgArg._SetInt64Array, MsgArg.NumericListReturnMarshaller),
    "t": (C.c_ulonglong, MsgArg._GetUInt64, MsgArg._SetUInt64, MsgArg._GetUInt64Array, MsgArg._SetUInt64Array, MsgArg.NumericListReturnMarshaller),
    "d": (C.c_double, MsgArg._GetDouble, MsgArg._SetDouble, MsgArg._GetDoubleArray, MsgArg._SetDoubleArray, MsgArg.NumericListReturnMarshaller),
    "s": (C.c_char_p, MsgArg._GetString, MsgArg._SetString, MsgArg._GetStringArray, None, MsgArg.StringListReturnMarshaller),
    #"o": (C.c_char_p, MsgArg._GetObjectPath, MsgArg._SetObjectPath, MsgArg._SetObjectPathArray, MsgArg._GetObjectPathArray),
    #"g": (C.c_char_p, MsgArg._GetSignature, MsgArg._SetSignature, MsgArg._SetSignatureArray, MsgArg._GetSignatureArray),
}
