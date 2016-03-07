import sys, types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject
# Wrapper for file Message.h


#define ALLJOYN_MESSAGE_FLAG_NO_REPLY_EXPECTED  0x01
#define ALLJOYN_MESSAGE_FLAG_AUTO_START         0x02
#define ALLJOYN_MESSAGE_FLAG_ALLOW_REMOTE_MSG   0x04
#define ALLJOYN_MESSAGE_FLAG_SESSIONLESS        0x10
#define ALLJOYN_MESSAGE_FLAG_GLOBAL_BROADCAST   0x20
#define ALLJOYN_MESSAGE_FLAG_COMPRESSED         (attempted_use_of_deprecated_definition = 0x40)
#define ALLJOYN_MESSAGE_FLAG_ENCRYPTED          0x80


#define ALLJOYN_MESSAGE_FLAG_NO_REPLY_EXPECTED  0x01
#define ALLJOYN_MESSAGE_FLAG_AUTO_START         0x02
#define ALLJOYN_MESSAGE_FLAG_ALLOW_REMOTE_MSG   0x04
#define ALLJOYN_MESSAGE_FLAG_SESSIONLESS        0x10
#define ALLJOYN_MESSAGE_FLAG_GLOBAL_BROADCAST   0x20
#define ALLJOYN_MESSAGE_FLAG_COMPRESSED         (attempted_use_of_deprecated_definition = 0x40)
#define ALLJOYN_MESSAGE_FLAG_ENCRYPTED          0x80


@unique
class MessageType(Enum):
    ALLJOYN_MESSAGE_INVALID = 0
    ALLJOYN_MESSAGE_METHOD_CALL = 1
    ALLJOYN_MESSAGE_METHOD_RET = 2
    ALLJOYN_MESSAGE_ERROR = 3
    ALLJOYN_MESSAGE_SIGNAL = 4


# Typedefs
# struct _alljoyn_message_handle * alljoyn_message
# struct _alljoyn_busattachment_handle * alljoyn_busattachment
# enum alljoyn_messagetype alljoyn_messagetype

class Message(AllJoynObject):
    
    __metaclass__ = AllJoynMeta
    
    _cmethods = {u'Create': (u'alljoyn_message_create',
             (u'alljoyn_message', C.c_void_p),
             ((u'alljoyn_busattachment', C.c_void_p),)),
             u'Description': (u'alljoyn_message_description',
                              (u'int', C.c_int),
                              ((u'alljoyn_message', C.c_void_p),
                               (u'char *', C.c_char_p),
                               (u'int', C.c_int))),
             u'Destroy': (u'alljoyn_message_destroy',
                          (u'void', None),
                          ((u'alljoyn_message', C.c_void_p),)),
             u'Eql': (u'alljoyn_message_eql',
                      (u'int', C.c_int),
                      ((u'const alljoyn_message', C.c_void_p),
                       (u'const alljoyn_message', C.c_void_p))),
             u'GetArg': (u'alljoyn_message_getarg',
                         (u'const int', C.c_int),
                         ((u'alljoyn_message', C.c_void_p), (u'int', C.c_int))),
             u'GetArgs': (u'alljoyn_message_getargs',
                          (u'void', None),
                          ((u'alljoyn_message', C.c_void_p),
                           (u'int *', POINTER(C.c_int)),
                           (u'int *', POINTER(C.c_int)))),
             u'GetAuthMechanism': (u'alljoyn_message_getauthmechanism',
                                   (u'const char *', C.c_char_p),
                                   ((u'alljoyn_message', C.c_void_p),)),
             u'GetCallSerial': (u'alljoyn_message_getcallserial',
                                (u'int', C.c_int),
                                ((u'alljoyn_message', C.c_void_p),)),
             u'GetDestination': (u'alljoyn_message_getdestination',
                                 (u'const char *', C.c_char_p),
                                 ((u'alljoyn_message', C.c_void_p),)),
             u'GetErrorName': (u'alljoyn_message_geterrorname',
                               (u'const char *', C.c_char_p),
                               ((u'alljoyn_message', C.c_void_p),
                                (u'char *', C.c_char_p),
                                (u'int *', POINTER(C.c_int)))),
             u'GetFlags': (u'alljoyn_message_getflags',
                           (u'int', C.c_int),
                           ((u'alljoyn_message', C.c_void_p),)),
             u'GetInterface': (u'alljoyn_message_getinterface',
                               (u'const char *', C.c_char_p),
                               ((u'alljoyn_message', C.c_void_p),)),
             u'GetMemberName': (u'alljoyn_message_getmembername',
                                (u'const char *', C.c_char_p),
                                ((u'alljoyn_message', C.c_void_p),)),
             u'GetObjectPath': (u'alljoyn_message_getobjectpath',
                                (u'const char *', C.c_char_p),
                                ((u'alljoyn_message', C.c_void_p),)),
             u'GetReceiveEndPointName': (u'alljoyn_message_getreceiveendpointname',
                                         (u'const char *', C.c_char_p),
                                         ((u'alljoyn_message', C.c_void_p),)),
             u'GetReplySerial': (u'alljoyn_message_getreplyserial',
                                 (u'int', C.c_int),
                                 ((u'alljoyn_message', C.c_void_p),)),
             u'GetSender': (u'alljoyn_message_getsender',
                            (u'const char *', C.c_char_p),
                            ((u'alljoyn_message', C.c_void_p),)),
             u'GetSessionId': (u'alljoyn_message_getsessionid',
                               (u'int', C.c_int),
                               ((u'alljoyn_message', C.c_void_p),)),
             u'GetSignature': (u'alljoyn_message_getsignature',
                               (u'const char *', C.c_char_p),
                               ((u'alljoyn_message', C.c_void_p),)),
             u'GetTimesTamp': (u'alljoyn_message_gettimestamp',
                               (u'int', C.c_int),
                               ((u'alljoyn_message', C.c_void_p),)),
             u'GetType': (u'alljoyn_message_gettype',
                          (u'alljoyn_messagetype', C.c_void_p),
                          ((u'alljoyn_message', C.c_void_p),)),
             u'IsBroadcastSignal': (u'alljoyn_message_isbroadcastsignal',
                                    (u'int', C.c_int),
                                    ((u'alljoyn_message', C.c_void_p),)),
             u'IsEncrypted': (u'alljoyn_message_isencrypted',
                              (u'int', C.c_int),
                              ((u'alljoyn_message', C.c_void_p),)),
             u'IsExpired': (u'alljoyn_message_isexpired',
                            (u'int', C.c_int),
                            ((u'alljoyn_message', C.c_void_p),
                             (u'int *', POINTER(C.c_int)))),
             u'IsGlobalBroadcast': (u'alljoyn_message_isglobalbroadcast',
                                    (u'int', C.c_int),
                                    ((u'alljoyn_message', C.c_void_p),)),
             u'IsSessionLess': (u'alljoyn_message_issessionless',
                                (u'int', C.c_int),
                                ((u'alljoyn_message', C.c_void_p),)),
             u'IsUnreliable': (u'alljoyn_message_isunreliable',
                               (u'int', C.c_int),
                               ((u'alljoyn_message', C.c_void_p),)),
             u'ParseArgs': (u'alljoyn_message_parseargs',
                            (u'QStatus', C.c_uint),
                            ((u'alljoyn_message', C.c_void_p),
                             (u'const char *', C.c_char_p))),
             u'SetEndianess': (u'alljoyn_message_setendianess',
                               (u'void', None),
                               ((u'const char', C.c_byte),)),
             u'ToString': (u'alljoyn_message_tostring',
                           (u'int', C.c_int),
                           ((u'alljoyn_message', C.c_void_p),
                            (u'char *', C.c_char_p),
                            (u'int', C.c_int)))}

    def __init__(self, bus_attachment):
        self.handle = self._Create(bus_attachment.handle)
        
    def __del__(self):
        self._Destroy(self.handle)

    # Wrapper Methods

    def IsBroadcastSignal(self):
        return self._IsBroadcastSignal(self.handle)

    def IsGlobalBroadcast(self):
        return self._IsGlobalBroadcast(self.handle)

    def IsSessionLess(self):
        return self._IsSessionLess(self.handle)

    def GetFlags(self):
        return self._GetFlags(self.handle)

    def IsExpired(self, tillExpireMS):
        return self._IsExpired(self.handle,tillExpireMS) # int *

    def IsUnreliable(self):
        return self._IsUnreliable(self.handle)

    def IsEncrypted(self):
        return self._IsEncrypted(self.handle)

    def GetAUTHMECHANISM(self):
        return self._GetAUTHMECHANISM(self.handle)

    def GetType(self):
        return self._GetType(self.handle)

    def GetARGS(self, numArgs,args):
        return self._GetARGS(self.handle,numArgs,args) # int *,int *

    def GetARG(self, argN):
        return self._GetARG(self.handle,argN) # int

    def ParSearGS(self, signature):
        return self._ParSearGS(self.handle,signature) # const char *

    def GetCallSerial(self):
        return self._GetCallSerial(self.handle)

    def GetSignature(self):
        return self._GetSignature(self.handle)

    def GetObjectPath(self):
        return self._GetObjectPath(self.handle)

    def GetInterface(self):
        return self._GetInterface(self.handle)

    def GetMemberName(self):
        return self._GetMemberName(self.handle)

    def GetReplySerial(self):
        return self._GetReplySerial(self.handle)

    def GetSender(self):
        return self._GetSender(self.handle)

    def GetReceiveEndPointName(self):
        return self._GetReceiveEndPointName(self.handle)

    def GetDestination(self):
        return self._GetDestination(self.handle)

    def GetSessionId(self):
        return self._GetSessionId(self.handle)

    def GetErrorName(self, errorMessage,errorMessage_size):
        return self._GetErrorName(self.handle,errorMessage,errorMessage_size) # char *,int *

    def ToString(self, str,buf):
        return self._ToString(self.handle,str,buf) # char *,int

    def Description(self, str,buf):
        return self._Description(self.handle,str,buf) # char *,int

    def GetTimesTamp(self):
        return self._GetTimesTamp(self.handle)

    def EQL(self, other):
        return self._EQL(self.handle,other) # const alljoyn_message

    def SetEndIANESS(self):
        return self._SetEndIANESS(self.handle)

    

Message.bind_functions_to_cls()