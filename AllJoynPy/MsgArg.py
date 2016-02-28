import sys, types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject
# Wrapper for file MsgArg.h

@unique
class TypeId(Enum):
    ALLJOYN_INVALID = 0
    ALLJOYN_ARRAY = 97
    ALLJOYN_BOOLEAN = 98
    ALLJOYN_DOUBLE = 100
    ALLJOYN_DICT_ENTRY = 101
    ALLJOYN_SIGNATURE = 103
    ALLJOYN_HANDLE = 104
    ALLJOYN_INT32 = 105
    ALLJOYN_INT16 = 110
    ALLJOYN_OBJECT_PATH = 111
    ALLJOYN_UINT16 = 113
    ALLJOYN_STRUCT = 114
    ALLJOYN_STRING = 115
    ALLJOYN_UINT64 = 116
    ALLJOYN_UINT32 = 117
    ALLJOYN_VARIANT = 118
    ALLJOYN_INT64 = 120
    ALLJOYN_BYTE = 121
    ALLJOYN_STRUCT_OPEN = 40
    ALLJOYN_STRUCT_CLOSE = 41
    ALLJOYN_DICT_ENTRY_OPEN = 123
    ALLJOYN_DICT_ENTRY_CLOSE = 125
    ALLJOYN_BOOLEAN_ARRAY = 25185
    ALLJOYN_DOUBLE_ARRAY = 25697
    ALLJOYN_INT32_ARRAY = 26977
    ALLJOYN_INT16_ARRAY = 28257
    ALLJOYN_UINT16_ARRAY = 29025
    ALLJOYN_UINT64_ARRAY = 29793
    ALLJOYN_UINT32_ARRAY = 30049
    ALLJOYN_INT64_ARRAY = 30817
    ALLJOYN_BYTE_ARRAY = 31073
    ALLJOYN_WILDCARD = 42


# Typedefs
# struct _alljoyn_msgarg_handle * alljoyn_msgarg
# enum alljoyn_typeid alljoyn_typeid


if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE
    


class MsgArg(AllJoynObject):
    
    __metaclass__ = AllJoynMeta
    
    _cmethods = {u'ArrayCreate': (u'alljoyn_msgarg_array_create',
                  (u'alljoyn_msgarg', 'C.c_void_p'),
                  ((u'int', 'C.c_int'),)),
 u'ArrayElement': (u'alljoyn_msgarg_array_element',
                   (u'alljoyn_msgarg', 'C.c_void_p'),
                   ((u'alljoyn_msgarg', 'C.c_void_p'), (u'int', 'C.c_int'))),
 u'ArrayGet': (u'alljoyn_msgarg_array_get',
               (u'QStatus', 'C.c_uint'),
               ((u'const alljoyn_msgarg', 'C.c_void_p'),
                (u'int', 'C.c_int'),
                (u'const char *', 'C.c_char_p'))),
 u'ArraySet': (u'alljoyn_msgarg_array_set',
               (u'QStatus', 'C.c_uint'),
               ((u'alljoyn_msgarg', 'C.c_void_p'),
                (u'int *', 'POINTER(C.c_int)'),
                (u'const char *', 'C.c_char_p'))),
 u'ArraySetOffset': (u'alljoyn_msgarg_array_set_offset',
                     (u'QStatus', 'C.c_uint'),
                     ((u'alljoyn_msgarg', 'C.c_void_p'),
                      (u'int', 'C.c_int'),
                      (u'int *', 'POINTER(C.c_int)'),
                      (u'const char *', 'C.c_char_p'))),
 u'ArraySignature': (u'alljoyn_msgarg_array_signature',
                     (u'int', 'C.c_int'),
                     ((u'alljoyn_msgarg', 'C.c_void_p'),
                      (u'int', 'C.c_int'),
                      (u'char *', 'C.c_char_p'),
                      (u'int', 'C.c_int'))),
 u'ArrayToString': (u'alljoyn_msgarg_array_tostring',
                    (u'int', 'C.c_int'),
                    ((u'const alljoyn_msgarg', 'C.c_void_p'),
                     (u'int', 'C.c_int'),
                     (u'char *', 'C.c_char_p'),
                     (u'int', 'C.c_int'),
                     (u'int', 'C.c_int'))),
 u'Clear': (u'alljoyn_msgarg_clear',
            (u'void', None),
            ((u'alljoyn_msgarg', 'C.c_void_p'),)),
 u'Clone': (u'alljoyn_msgarg_clone',
            (u'void', None),
            ((u'alljoyn_msgarg', 'C.c_void_p'),
             (u'const alljoyn_msgarg', 'C.c_void_p'))),
 u'Copy': (u'alljoyn_msgarg_copy',
           (u'alljoyn_msgarg', 'C.c_void_p'),
           ((u'const alljoyn_msgarg', 'C.c_void_p'),)),
 u'Create': (u'alljoyn_msgarg_create', (u'alljoyn_msgarg', 'C.c_void_p'), ()),
 u'CreateAndSet': (u'alljoyn_msgarg_create_and_set',
                   (u'alljoyn_msgarg', 'C.c_void_p'),
                   ((u'const char *', 'C.c_char_p'),)),
 u'Destroy': (u'alljoyn_msgarg_destroy',
              (u'void', None),
              ((u'alljoyn_msgarg', 'C.c_void_p'),)),
 u'Equal': (u'alljoyn_msgarg_equal',
            (u'int', 'C.c_int'),
            ((u'alljoyn_msgarg', 'C.c_void_p'),
             (u'alljoyn_msgarg', 'C.c_void_p'))),
 u'Get': (u'alljoyn_msgarg_get',
          (u'QStatus', 'C.c_uint'),
          ((u'alljoyn_msgarg', 'C.c_void_p'),
           (u'const char *', 'C.c_char_p'))),
 u'GetArrayElement': (u'alljoyn_msgarg_get_array_element',
                      (u'void', None),
                      ((u'const alljoyn_msgarg', 'C.c_void_p'),
                       (u'int', 'C.c_int'),
                       (u'alljoyn_msgarg *', 'POINTER(C.c_void_p)'))),
 u'GetArrayElementSignature': (u'alljoyn_msgarg_get_array_elementsignature',
                               (u'const char *', 'C.c_char_p'),
                               ((u'const alljoyn_msgarg', 'C.c_void_p'),
                                (u'int', 'C.c_int'))),
 u'GetArrayNumberOfElements': (u'alljoyn_msgarg_get_array_numberofelements',
                               (u'int', 'C.c_int'),
                               ((u'const alljoyn_msgarg', 'C.c_void_p'),)),
 u'GetBooL': (u'alljoyn_msgarg_get_bool',
              (u'QStatus', 'C.c_uint'),
              ((u'const alljoyn_msgarg', 'C.c_void_p'),
               (u'int *', 'POINTER(C.c_int)'))),
 u'GetBooLARRAY': (u'alljoyn_msgarg_get_bool_array',
                   (u'QStatus', 'C.c_uint'),
                   ((u'const alljoyn_msgarg', 'C.c_void_p'),
                    (u'int *', 'POINTER(C.c_int)'),
                    (u'int *', 'POINTER(C.c_int)'))),
 u'GetDICTELEMENT': (u'alljoyn_msgarg_getdictelement',
                     (u'QStatus', 'C.c_uint'),
                     ((u'alljoyn_msgarg', 'C.c_void_p'),
                      (u'const char *', 'C.c_char_p'))),
 u'GetDouble': (u'alljoyn_msgarg_get_double',
                (u'QStatus', 'C.c_uint'),
                ((u'const alljoyn_msgarg', 'C.c_void_p'),
                 (u'double *', 'POINTER(C.c_double)'))),
 u'GetDoubleArray': (u'alljoyn_msgarg_get_double_array',
                     (u'QStatus', 'C.c_uint'),
                     ((u'const alljoyn_msgarg', 'C.c_void_p'),
                      (u'int *', 'POINTER(C.c_int)'),
                      (u'double *', 'POINTER(C.c_double)'))),
 u'GetInT16': (u'alljoyn_msgarg_get_int16',
               (u'QStatus', 'C.c_uint'),
               ((u'const alljoyn_msgarg', 'C.c_void_p'),
                (u'int *', 'POINTER(C.c_int)'))),
 u'GetInT16ARRAY': (u'alljoyn_msgarg_get_int16_array',
                    (u'QStatus', 'C.c_uint'),
                    ((u'const alljoyn_msgarg', 'C.c_void_p'),
                     (u'int *', 'POINTER(C.c_int)'),
                     (u'int *', 'POINTER(C.c_int)'))),
 u'GetInT32': (u'alljoyn_msgarg_get_int32',
               (u'QStatus', 'C.c_uint'),
               ((u'const alljoyn_msgarg', 'C.c_void_p'),
                (u'int *', 'POINTER(C.c_int)'))),
 u'GetInT32ARRAY': (u'alljoyn_msgarg_get_int32_array',
                    (u'QStatus', 'C.c_uint'),
                    ((u'const alljoyn_msgarg', 'C.c_void_p'),
                     (u'int *', 'POINTER(C.c_int)'),
                     (u'int *', 'POINTER(C.c_int)'))),
 u'GetInT64': (u'alljoyn_msgarg_get_int64',
               (u'QStatus', 'C.c_uint'),
               ((u'const alljoyn_msgarg', 'C.c_void_p'),
                (u'int *', 'POINTER(C.c_int)'))),
 u'GetInT64ARRAY': (u'alljoyn_msgarg_get_int64_array',
                    (u'QStatus', 'C.c_uint'),
                    ((u'const alljoyn_msgarg', 'C.c_void_p'),
                     (u'int *', 'POINTER(C.c_int)'),
                     (u'int *', 'POINTER(C.c_int)'))),
 u'GetKey': (u'alljoyn_msgarg_getkey',
             (u'alljoyn_msgarg', 'C.c_void_p'),
             ((u'alljoyn_msgarg', 'C.c_void_p'),)),
 u'GetMember': (u'alljoyn_msgarg_getmember',
                (u'alljoyn_msgarg', 'C.c_void_p'),
                ((u'alljoyn_msgarg', 'C.c_void_p'), (u'int', 'C.c_int'))),
 u'GetNuMMEMBERS': (u'alljoyn_msgarg_getnummembers',
                    (u'int', 'C.c_int'),
                    ((u'alljoyn_msgarg', 'C.c_void_p'),)),
 u'GetObjectPath': (u'alljoyn_msgarg_get_objectpath',
                    (u'QStatus', 'C.c_uint'),
                    ((u'const alljoyn_msgarg', 'C.c_void_p'),
                     (u'char **', 'POINTER(C.c_char_p)'))),
 u'GetSignature': (u'alljoyn_msgarg_get_signature',
                   (u'QStatus', 'C.c_uint'),
                   ((u'const alljoyn_msgarg', 'C.c_void_p'),
                    (u'char **', 'POINTER(C.c_char_p)'))),
 u'GetString': (u'alljoyn_msgarg_get_string',
                (u'QStatus', 'C.c_uint'),
                ((u'const alljoyn_msgarg', 'C.c_void_p'),
                 (u'char **', 'POINTER(C.c_char_p)'))),
 u'GetType': (u'alljoyn_msgarg_gettype',
              (u'alljoyn_typeid', 'C.c_uint'),
              ((u'alljoyn_msgarg', 'C.c_void_p'),)),
 u'GetUINT16': (u'alljoyn_msgarg_get_uint16',
                (u'QStatus', 'C.c_uint'),
                ((u'const alljoyn_msgarg', 'C.c_void_p'),
                 (u'int *', 'POINTER(C.c_int)'))),
 u'GetUINT16ARRAY': (u'alljoyn_msgarg_get_uint16_array',
                     (u'QStatus', 'C.c_uint'),
                     ((u'const alljoyn_msgarg', 'C.c_void_p'),
                      (u'int *', 'POINTER(C.c_int)'),
                      (u'int *', 'POINTER(C.c_int)'))),
 u'GetUINT32': (u'alljoyn_msgarg_get_uint32',
                (u'QStatus', 'C.c_uint'),
                ((u'const alljoyn_msgarg', 'C.c_void_p'),
                 (u'int *', 'POINTER(C.c_int)'))),
 u'GetUINT32ARRAY': (u'alljoyn_msgarg_get_uint32_array',
                     (u'QStatus', 'C.c_uint'),
                     ((u'const alljoyn_msgarg', 'C.c_void_p'),
                      (u'int *', 'POINTER(C.c_int)'),
                      (u'int *', 'POINTER(C.c_int)'))),
 u'GetUINT64': (u'alljoyn_msgarg_get_uint64',
                (u'QStatus', 'C.c_uint'),
                ((u'const alljoyn_msgarg', 'C.c_void_p'),
                 (u'int *', 'POINTER(C.c_int)'))),
 u'GetUINT64ARRAY': (u'alljoyn_msgarg_get_uint64_array',
                     (u'QStatus', 'C.c_uint'),
                     ((u'const alljoyn_msgarg', 'C.c_void_p'),
                      (u'int *', 'POINTER(C.c_int)'),
                      (u'int *', 'POINTER(C.c_int)'))),
 u'GetUINT8': (u'alljoyn_msgarg_get_uint8',
               (u'QStatus', 'C.c_uint'),
               ((u'const alljoyn_msgarg', 'C.c_void_p'),
                (u'int *', 'POINTER(C.c_int)'))),
 u'GetUINT8ARRAY': (u'alljoyn_msgarg_get_uint8_array',
                    (u'QStatus', 'C.c_uint'),
                    ((u'const alljoyn_msgarg', 'C.c_void_p'),
                     (u'int *', 'POINTER(C.c_int)'),
                     (u'int *', 'POINTER(C.c_int)'))),
 u'GetValue': (u'alljoyn_msgarg_getvalue',
               (u'alljoyn_msgarg', 'C.c_void_p'),
               ((u'alljoyn_msgarg', 'C.c_void_p'),)),
 u'GetVariant': (u'alljoyn_msgarg_get_variant',
                 (u'QStatus', 'C.c_uint'),
                 ((u'const alljoyn_msgarg', 'C.c_void_p'),
                  (u'alljoyn_msgarg', 'C.c_void_p'))),
 u'GetVariantArray': (u'alljoyn_msgarg_get_variant_array',
                      (u'QStatus', 'C.c_uint'),
                      ((u'const alljoyn_msgarg', 'C.c_void_p'),
                       (u'const char *', 'C.c_char_p'),
                       (u'int *', 'POINTER(C.c_int)'),
                       (u'alljoyn_msgarg *', 'POINTER(C.c_void_p)'))),
 u'HasSignature': (u'alljoyn_msgarg_hassignature',
                   (u'int', 'C.c_int'),
                   ((u'alljoyn_msgarg', 'C.c_void_p'),
                    (u'const char *', 'C.c_char_p'))),
 u'Set': (u'alljoyn_msgarg_set',
          (u'QStatus', 'C.c_uint'),
          ((u'alljoyn_msgarg', 'C.c_void_p'),
           (u'const char *', 'C.c_char_p'))),
 u'SetAndStabILIZE': (u'alljoyn_msgarg_set_and_stabilize',
                      (u'QStatus', 'C.c_uint'),
                      ((u'alljoyn_msgarg', 'C.c_void_p'),
                       (u'const char *', 'C.c_char_p'))),
 u'SetBooL': (u'alljoyn_msgarg_set_bool',
              (u'QStatus', 'C.c_uint'),
              ((u'alljoyn_msgarg', 'C.c_void_p'), (u'int', 'C.c_int'))),
 u'SetBooLARRAY': (u'alljoyn_msgarg_set_bool_array',
                   (u'QStatus', 'C.c_uint'),
                   ((u'alljoyn_msgarg', 'C.c_void_p'),
                    (u'int', 'C.c_int'),
                    (u'int *', 'POINTER(C.c_int)'))),
 u'SetDICTENTRY': (u'alljoyn_msgarg_setdictentry',
                   (u'QStatus', 'C.c_uint'),
                   ((u'alljoyn_msgarg', 'C.c_void_p'),
                    (u'alljoyn_msgarg', 'C.c_void_p'),
                    (u'alljoyn_msgarg', 'C.c_void_p'))),
 u'SetDouble': (u'alljoyn_msgarg_set_double',
                (u'QStatus', 'C.c_uint'),
                ((u'alljoyn_msgarg', 'C.c_void_p'),
                 (u'double', 'C.c_double'))),
 u'SetDoubleArray': (u'alljoyn_msgarg_set_double_array',
                     (u'QStatus', 'C.c_uint'),
                     ((u'alljoyn_msgarg', 'C.c_void_p'),
                      (u'int', 'C.c_int'),
                      (u'double *', 'POINTER(C.c_double)'))),
 u'SetInT16': (u'alljoyn_msgarg_set_int16',
               (u'QStatus', 'C.c_uint'),
               ((u'alljoyn_msgarg', 'C.c_void_p'), (u'int', 'C.c_int'))),
 u'SetInT16ARRAY': (u'alljoyn_msgarg_set_int16_array',
                    (u'QStatus', 'C.c_uint'),
                    ((u'alljoyn_msgarg', 'C.c_void_p'),
                     (u'int', 'C.c_int'),
                     (u'int *', 'POINTER(C.c_int)'))),
 u'SetInT32': (u'alljoyn_msgarg_set_int32',
               (u'QStatus', 'C.c_uint'),
               ((u'alljoyn_msgarg', 'C.c_void_p'), (u'int', 'C.c_int'))),
 u'SetInT32ARRAY': (u'alljoyn_msgarg_set_int32_array',
                    (u'QStatus', 'C.c_uint'),
                    ((u'alljoyn_msgarg', 'C.c_void_p'),
                     (u'int', 'C.c_int'),
                     (u'int *', 'POINTER(C.c_int)'))),
 u'SetInT64': (u'alljoyn_msgarg_set_int64',
               (u'QStatus', 'C.c_uint'),
               ((u'alljoyn_msgarg', 'C.c_void_p'), (u'int', 'C.c_int'))),
 u'SetInT64ARRAY': (u'alljoyn_msgarg_set_int64_array',
                    (u'QStatus', 'C.c_uint'),
                    ((u'alljoyn_msgarg', 'C.c_void_p'),
                     (u'int', 'C.c_int'),
                     (u'int *', 'POINTER(C.c_int)'))),
 u'SetObjectPath': (u'alljoyn_msgarg_set_objectpath',
                    (u'QStatus', 'C.c_uint'),
                    ((u'alljoyn_msgarg', 'C.c_void_p'),
                     (u'const char *', 'C.c_char_p'))),
 u'SetObjectPathArray': (u'alljoyn_msgarg_set_objectpath_array',
                         (u'QStatus', 'C.c_uint'),
                         ((u'alljoyn_msgarg', 'C.c_void_p'),
                          (u'int', 'C.c_int'),
                          (u'const char **', 'POINTER(C.c_char_p)'))),
 u'SetSignature': (u'alljoyn_msgarg_set_signature',
                   (u'QStatus', 'C.c_uint'),
                   ((u'alljoyn_msgarg', 'C.c_void_p'),
                    (u'const char *', 'C.c_char_p'))),
 u'SetSignatureArray': (u'alljoyn_msgarg_set_signature_array',
                        (u'QStatus', 'C.c_uint'),
                        ((u'alljoyn_msgarg', 'C.c_void_p'),
                         (u'int', 'C.c_int'),
                         (u'const char **', 'POINTER(C.c_char_p)'))),
 u'SetString': (u'alljoyn_msgarg_set_string',
                (u'QStatus', 'C.c_uint'),
                ((u'alljoyn_msgarg', 'C.c_void_p'),
                 (u'const char *', 'C.c_char_p'))),
 u'SetStringArray': (u'alljoyn_msgarg_set_string_array',
                     (u'QStatus', 'C.c_uint'),
                     ((u'alljoyn_msgarg', 'C.c_void_p'),
                      (u'int', 'C.c_int'),
                      (u'const char **', 'POINTER(C.c_char_p)'))),
 u'SetUINT16': (u'alljoyn_msgarg_set_uint16',
                (u'QStatus', 'C.c_uint'),
                ((u'alljoyn_msgarg', 'C.c_void_p'), (u'int', 'C.c_int'))),
 u'SetUINT16ARRAY': (u'alljoyn_msgarg_set_uint16_array',
                     (u'QStatus', 'C.c_uint'),
                     ((u'alljoyn_msgarg', 'C.c_void_p'),
                      (u'int', 'C.c_int'),
                      (u'int *', 'POINTER(C.c_int)'))),
 u'SetUINT32': (u'alljoyn_msgarg_set_uint32',
                (u'QStatus', 'C.c_uint'),
                ((u'alljoyn_msgarg', 'C.c_void_p'), (u'int', 'C.c_int'))),
 u'SetUINT32ARRAY': (u'alljoyn_msgarg_set_uint32_array',
                     (u'QStatus', 'C.c_uint'),
                     ((u'alljoyn_msgarg', 'C.c_void_p'),
                      (u'int', 'C.c_int'),
                      (u'int *', 'POINTER(C.c_int)'))),
 u'SetUINT64': (u'alljoyn_msgarg_set_uint64',
                (u'QStatus', 'C.c_uint'),
                ((u'alljoyn_msgarg', 'C.c_void_p'), (u'int', 'C.c_int'))),
 u'SetUINT64ARRAY': (u'alljoyn_msgarg_set_uint64_array',
                     (u'QStatus', 'C.c_uint'),
                     ((u'alljoyn_msgarg', 'C.c_void_p'),
                      (u'int', 'C.c_int'),
                      (u'int *', 'POINTER(C.c_int)'))),
 u'SetUINT8': (u'alljoyn_msgarg_set_uint8',
               (u'QStatus', 'C.c_uint'),
               ((u'alljoyn_msgarg', 'C.c_void_p'), (u'int', 'C.c_int'))),
 u'SetUINT8ARRAY': (u'alljoyn_msgarg_set_uint8_array',
                    (u'QStatus', 'C.c_uint'),
                    ((u'alljoyn_msgarg', 'C.c_void_p'),
                     (u'int', 'C.c_int'),
                     (u'int *', 'POINTER(C.c_int)'))),
 u'SetsTRUCT': (u'alljoyn_msgarg_setstruct',
                (u'QStatus', 'C.c_uint'),
                ((u'alljoyn_msgarg', 'C.c_void_p'),
                 (u'alljoyn_msgarg', 'C.c_void_p'),
                 (u'int', 'C.c_int'))),
 u'Signature': (u'alljoyn_msgarg_signature',
                (u'int', 'C.c_int'),
                ((u'alljoyn_msgarg', 'C.c_void_p'),
                 (u'char *', 'C.c_char_p'),
                 (u'int', 'C.c_int'))),
 u'StabILIZE': (u'alljoyn_msgarg_stabilize',
                (u'void', None),
                ((u'alljoyn_msgarg', 'C.c_void_p'),)),
 u'ToString': (u'alljoyn_msgarg_tostring',
               (u'int', 'C.c_int'),
               ((u'alljoyn_msgarg', 'C.c_void_p'),
                (u'char *', 'C.c_char_p'),
                (u'int', 'C.c_int'),
                (u'int', 'C.c_int')))}
    
    def __init__(self):
        self.handle = None
        
    def __del__(self):
        if self.handle:
            self._Destroy(self.handle)

    # Wrapper Methods

    def Create(self):
        return self._Create(self.handle)

    def CreateAndSet(self):
        return self._CreateAndSet(self.handle)

    def Destroy(self):
        return self._Destroy(self.handle)

    def ArrayCreate(self):
        return self._ArrayCreate(self.handle)

    def ArrayElement(self, index):
        return self._ArrayElement(self.handle,index) # int

    def Set(self, signature):
        return self._Set(self.handle,signature) # const char *

    def Get(self, signature):
        return self._Get(self.handle,signature) # const char *

    def Copy(self):
        return self._Copy(self.handle)

    def Clone(self, source):
        return self._Clone(self.handle,source) # const alljoyn_msgarg

    def Equal(self, rhv):
        return self._Equal(self.handle,rhv) # alljoyn_msgarg

    def ArraySet(self, numArgs,signature):
        return self._ArraySet(self.handle,numArgs,signature) # int *,const char *

    def ArrayGet(self, numArgs,signature):
        return self._ArrayGet(self.handle,numArgs,signature) # int,const char *

    def ToString(self, str,buf,indent):
        return self._ToString(self.handle,str,buf,indent) # char *,int,int

    def ArrayToString(self, numArgs,str,buf,indent):
        return self._ArrayToString(self.handle,numArgs,str,buf,indent) # int,char *,int,int

    def Signature(self, str,buf):
        return self._Signature(self.handle,str,buf) # char *,int

    def ArraySignature(self, numValues,str,buf):
        return self._ArraySignature(self.handle,numValues,str,buf) # int,char *,int

    def HasSignature(self, signature):
        return self._HasSignature(self.handle,signature) # const char *

    def GetDICTELEMENT(self, elemSig):
        return self._GetDICTELEMENT(self.handle,elemSig) # const char *

    def GetType(self):
        return self._GetType(self.handle)

    def Clear(self):
        return self._Clear(self.handle)

    def StabILIZE(self):
        return self._StabILIZE(self.handle)

    def ArraySetOffset(self, argOffset,numArgs,signature):
        return self._ArraySetOffset(self.handle,argOffset,numArgs,signature) # int,int *,const char *

    def SetAndStabILIZE(self, signature):
        return self._SetAndStabILIZE(self.handle,signature) # const char *

    def SetUINT8(self, y):
        return self._SetUINT8(self.handle,y) # int

    def SetBooL(self, b):
        return self._SetBooL(self.handle,b) # int

    def SetInT16(self, n):
        return self._SetInT16(self.handle,n) # int

    def SetUINT16(self, q):
        return self._SetUINT16(self.handle,q) # int

    def SetInT32(self, i):
        return self._SetInT32(self.handle,i) # int

    def SetUINT32(self, u):
        return self._SetUINT32(self.handle,u) # int

    def SetInT64(self, x):
        return self._SetInT64(self.handle,x) # int

    def SetUINT64(self, t):
        return self._SetUINT64(self.handle,t) # int

    def SetDouble(self, d):
        return self._SetDouble(self.handle,d) # double

    def SetString(self, s):
        return self._SetString(self.handle,s) # const char *

    def SetObjectPath(self, o):
        return self._SetObjectPath(self.handle,o) # const char *

    def SetSignature(self, g):
        return self._SetSignature(self.handle,g) # const char *

    def GetUINT8(self, y):
        return self._GetUINT8(self.handle,y) # int *

    def GetBooL(self, b):
        return self._GetBooL(self.handle,b) # int *

    def GetInT16(self, n):
        return self._GetInT16(self.handle,n) # int *

    def GetUINT16(self, q):
        return self._GetUINT16(self.handle,q) # int *

    def GetInT32(self, i):
        return self._GetInT32(self.handle,i) # int *

    def GetUINT32(self, u):
        return self._GetUINT32(self.handle,u) # int *

    def GetInT64(self, x):
        return self._GetInT64(self.handle,x) # int *

    def GetUINT64(self, t):
        return self._GetUINT64(self.handle,t) # int *

    def GetDouble(self, d):
        return self._GetDouble(self.handle,d) # double *

    def GetString(self, s):
        return self._GetString(self.handle,s) # char **

    def GetObjectPath(self, o):
        return self._GetObjectPath(self.handle,o) # char **

    def GetSignature(self, g):
        return self._GetSignature(self.handle,g) # char **

    def GetVariant(self, v):
        return self._GetVariant(self.handle,v) # alljoyn_msgarg

    def SetUINT8ARRAY(self, length,ay):
        return self._SetUINT8ARRAY(self.handle,length,ay) # int,int *

    def SetBooLARRAY(self, length,ab):
        return self._SetBooLARRAY(self.handle,length,ab) # int,int *

    def SetInT16ARRAY(self, length,an):
        return self._SetInT16ARRAY(self.handle,length,an) # int,int *

    def SetUINT16ARRAY(self, length,aq):
        return self._SetUINT16ARRAY(self.handle,length,aq) # int,int *

    def SetInT32ARRAY(self, length,ai):
        return self._SetInT32ARRAY(self.handle,length,ai) # int,int *

    def SetUINT32ARRAY(self, length,au):
        return self._SetUINT32ARRAY(self.handle,length,au) # int,int *

    def SetInT64ARRAY(self, length,ax):
        return self._SetInT64ARRAY(self.handle,length,ax) # int,int *

    def SetUINT64ARRAY(self, length,at):
        return self._SetUINT64ARRAY(self.handle,length,at) # int,int *

    def SetDoubleArray(self, length,ad):
        return self._SetDoubleArray(self.handle,length,ad) # int,double *

    def SetStringArray(self, length,as):
        return self._SetStringArray(self.handle,length,as) # int,const char **

    def SetObjectPathArray(self, length,ao):
        return self._SetObjectPathArray(self.handle,length,ao) # int,const char **

    def SetSignatureArray(self, length,ag):
        return self._SetSignatureArray(self.handle,length,ag) # int,const char **

    def GetUINT8ARRAY(self, length,ay):
        return self._GetUINT8ARRAY(self.handle,length,ay) # int *,int *

    def GetBooLARRAY(self, length,ab):
        return self._GetBooLARRAY(self.handle,length,ab) # int *,int *

    def GetInT16ARRAY(self, length,an):
        return self._GetInT16ARRAY(self.handle,length,an) # int *,int *

    def GetUINT16ARRAY(self, length,aq):
        return self._GetUINT16ARRAY(self.handle,length,aq) # int *,int *

    def GetInT32ARRAY(self, length,ai):
        return self._GetInT32ARRAY(self.handle,length,ai) # int *,int *

    def GetUINT32ARRAY(self, length,au):
        return self._GetUINT32ARRAY(self.handle,length,au) # int *,int *

    def GetInT64ARRAY(self, length,ax):
        return self._GetInT64ARRAY(self.handle,length,ax) # int *,int *

    def GetUINT64ARRAY(self, length,at):
        return self._GetUINT64ARRAY(self.handle,length,at) # int *,int *

    def GetDoubleArray(self, length,ad):
        return self._GetDoubleArray(self.handle,length,ad) # int *,double *

    def GetVariantArray(self, signature,length,av):
        return self._GetVariantArray(self.handle,signature,length,av) # const char *,int *,alljoyn_msgarg *

    def GetArrayNumberOfElements(self):
        return self._GetArrayNumberOfElements(self.handle)

    def GetArrayElement(self, index,element):
        return self._GetArrayElement(self.handle,index,element) # int,alljoyn_msgarg *

    def GetArrayElementSignature(self, index):
        return self._GetArrayElementSignature(self.handle,index) # int

    def GetKey(self):
        return self._GetKey(self.handle)

    def GetValue(self):
        return self._GetValue(self.handle)

    def SetDICTENTRY(self, key,value):
        return self._SetDICTENTRY(self.handle,key,value) # alljoyn_msgarg,alljoyn_msgarg

    def SetsTRUCT(self, struct_members,num_members):
        return self._SetsTRUCT(self.handle,struct_members,num_members) # alljoyn_msgarg,int

    def GetNuMMEMBERS(self):
        return self._GetNuMMEMBERS(self.handle)

    def GetMember(self, index):
        return self._GetMember(self.handle,index) # int

