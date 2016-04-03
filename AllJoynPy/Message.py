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


import ctypes as C
from ctypes import POINTER
from enum import Enum, unique

from . import *
import MsgArg
import BusAttachment
# Wrapper for file Message.h


ALLJOYN_MESSAGE_FLAG_NO_REPLY_EXPECTED = 0x01
ALLJOYN_MESSAGE_FLAG_AUTO_START = 0x02
ALLJOYN_MESSAGE_FLAG_ALLOW_REMOTE_MSG = 0x04
ALLJOYN_MESSAGE_FLAG_SESSIONLESS = 0x10
ALLJOYN_MESSAGE_FLAG_GLOBAL_BROADCAST = 0x20
ALLJOYN_MESSAGE_FLAG_COMPRESSED = ("attempted_use_of_deprecated_definition", 0x40)
ALLJOYN_MESSAGE_FLAG_ENCRYPTED = 0x80


@unique
class MessageType(Enum):
    ALLJOYN_MESSAGE_INVALID = 0
    ALLJOYN_MESSAGE_METHOD_CALL = 1
    ALLJOYN_MESSAGE_METHOD_RET = 2
    ALLJOYN_MESSAGE_ERROR = 3
    ALLJOYN_MESSAGE_SIGNAL = 4


class Message(AllJoynObject):

    __metaclass__ = AllJoynMeta

    _cmethods = {u'Create': (u'alljoyn_message_create',
                             (u'alljoyn_message', MessageHandle),
                             ((u'alljoyn_busattachment', BusAttachment.BusAttachmentHandle),)),

                 u'Description': (u'alljoyn_message_description',
                                  (u'int', C.c_int),
                                  ((u'alljoyn_message', MessageHandle),
                                      (u'char *', C.c_char_p),
                                      (u'size_t', C.c_size_t))),

                 u'Destroy': (u'alljoyn_message_destroy',
                              (u'void', None),
                              ((u'alljoyn_message', MessageHandle),)),

                 u'Eql': (u'alljoyn_message_eql',
                          (u'int', C.c_int),
                          ((u'const alljoyn_message', MessageHandle),
                              (u'const alljoyn_message', MessageHandle))),

                 u'GetArg': (u'alljoyn_message_getarg',
                             (u'const int', MsgArg.MsgArgHandle),
                             ((u'alljoyn_message', MessageHandle), (u'int', C.c_int))),

                 u'GetArgs': (u'alljoyn_message_getargs',
                              (u'void', None),
                              ((u'alljoyn_message', MessageHandle),
                                  (u'size_t *', POINTER(C.c_size_t)),
                                  (u'int *', POINTER(MsgArgHandle)))),

                 u'GetAuthMechanism': (u'alljoyn_message_getauthmechanism',
                                       (u'const char *', C.c_char_p),
                                       ((u'alljoyn_message', MessageHandle),)),

                 u'GetCallSerial': (u'alljoyn_message_getcallserial',
                                    (u'int', C.c_int),
                                    ((u'alljoyn_message', MessageHandle),)),

                 u'GetDestination': (u'alljoyn_message_getdestination',
                                     (u'const char *', C.c_char_p),
                                     ((u'alljoyn_message', MessageHandle),)),

                 u'GetErrorName': (u'alljoyn_message_geterrorname',
                                   (u'const char *', C.c_char_p),
                                   ((u'alljoyn_message', MessageHandle),
                                       (u'char *', C.c_char_p),
                                       (u'size_t *', POINTER(C.c_size_t)))),

                 u'GetFlags': (u'alljoyn_message_getflags',
                               (u'int', C.c_int),
                               ((u'alljoyn_message', MessageHandle),)),

                 u'GetInterface': (u'alljoyn_message_getinterface',
                                   (u'const char *', C.c_char_p),
                                   ((u'alljoyn_message', MessageHandle),)),

                 u'GetMemberName': (u'alljoyn_message_getmembername',
                                    (u'const char *', C.c_char_p),
                                    ((u'alljoyn_message', MessageHandle),)),

                 u'GetObjectPath': (u'alljoyn_message_getobjectpath',
                                    (u'const char *', C.c_char_p),
                                    ((u'alljoyn_message', MessageHandle),)),

                 u'GetReceiveEndPointName': (u'alljoyn_message_getreceiveendpointname',
                                             (u'const char *', C.c_char_p),
                                             ((u'alljoyn_message', MessageHandle),)),

                 u'GetReplySerial': (u'alljoyn_message_getreplyserial',
                                     (u'int', C.c_int),
                                     ((u'alljoyn_message', MessageHandle),)),

                 u'GetSender': (u'alljoyn_message_getsender',
                                (u'const char *', C.c_char_p),
                                ((u'alljoyn_message', MessageHandle),)),

                 u'GetSessionId': (u'alljoyn_message_getsessionid',
                                   (u'int', C.c_int),
                                   ((u'alljoyn_message', MessageHandle),)),

                 u'GetSignature': (u'alljoyn_message_getsignature',
                                   (u'const char *', C.c_char_p),
                                   ((u'alljoyn_message', MessageHandle),)),

                 u'GetTimesTamp': (u'alljoyn_message_gettimestamp',
                                   (u'int', C.c_int),
                                   ((u'alljoyn_message', MessageHandle),)),

                 u'GetType': (u'alljoyn_message_gettype',
                              (u'alljoyn_messagetype', C.c_void_p),
                              ((u'alljoyn_message', MessageHandle),)),

                 u'IsBroadcastSignal': (u'alljoyn_message_isbroadcastsignal',
                                        (u'int', C.c_int),
                                        ((u'alljoyn_message', MessageHandle),)),

                 u'IsEncrypted': (u'alljoyn_message_isencrypted',
                                  (u'int', C.c_int),
                                  ((u'alljoyn_message', MessageHandle),)),

                 u'IsExpired': (u'alljoyn_message_isexpired',
                                (u'int', C.c_int),
                                ((u'alljoyn_message', MessageHandle),
                                    (u'int *', POINTER(C.c_int)))),

                 u'IsGlobalBroadcast': (u'alljoyn_message_isglobalbroadcast',
                                        (u'int', C.c_int),
                                        ((u'alljoyn_message', MessageHandle),)),

                 u'IsSessionLess': (u'alljoyn_message_issessionless',
                                    (u'int', C.c_int),
                                    ((u'alljoyn_message', MessageHandle),)),

                 u'IsUnreliable': (u'alljoyn_message_isunreliable',
                                   (u'int', C.c_int),
                                   ((u'alljoyn_message', MessageHandle),)),

                 u'ParseArgs': (u'alljoyn_message_parseargs',
                                (u'QStatus', C.c_uint),
                                ((u'alljoyn_message', MessageHandle),
                                    (u'const char *', C.c_char_p))),

                 u'SetEndianess': (u'alljoyn_message_setendianess',
                                   (u'void', None),
                                   ((u'const char', C.c_byte),)),

                 u'ToString': (u'alljoyn_message_tostring',
                               (u'int', C.c_int),
                               ((u'alljoyn_message', MessageHandle),
                                   (u'char *', C.c_char_p),
                                   (u'size_t', C.c_size_t)))}

    def __init__(self, bus_attachment=None):
        if bus_attachment:
            assert type(bus_attachment.handle) == BusAttachment.BusAttachmentHandle
            self.handle = self._Create(bus_attachment.handle)

    def __del__(self):
        # Todo Getting seg fault with Destroy
        # print "Message __del__ called"
        # self._Destroy(self.handle)
        pass

    @classmethod
    def FromHandle(cls, handle):
        assert type(handle) == MessageHandle
        instance = cls()
        instance.handle = handle
        return instance

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
        return self._IsExpired(self.handle, tillExpireMS)  # int *

    def IsUnreliable(self):
        return self._IsUnreliable(self.handle)

    def IsEncrypted(self):
        return self._IsEncrypted(self.handle)

    def GetAuthMechanism(self):
        return self._GetAuthMechanism(self.handle)

    def GetType(self):
        return MessageType(self._GetType(self.handle))

    def GetArgs(self):
        size = C.c_size_t()
        arg = MsgArgHandle()
        self._GetArgs(self.handle, C.byref(size), C.byref(arg))
        args = MsgArg.MsgArg.FromHandle(arg)
        return [args.ArrayElement(i) for i in range(size.value)]

    def GetArg(self, arg_index):
        return MsgArg.MsgArg.FromHandle(self._GetArg(self.handle, arg_index))  # int

    def ParSearGS(self, signature):
        return self._ParSearGS(self.handle, signature)  # const char *

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

    def GetErrorName(self):
        error_message = C.create_string_buffer(1024)
        size = C.c_size_t(1024)
        error_name = self._GetErrorName(self.handle, error_message, C.byref(size))  # char *,int *
        return (error_name, error_message.value)

    def ToString(self):
        buf = C.create_string_buffer(1024)
        size = C.c_size_t(1024)
        self._ToString(self.handle, buf, size)  # char *,int
        return buf.value

    def __repr__(self):
        return self.ToString()

    def Description(self):
        buf = C.create_string_buffer(1024)
        size = C.c_size_t(1024)
        self._Description(self.handle, buf, size)  # char *,int
        return buf.value

    def GetTimesTamp(self):
        return self._GetTimesTamp(self.handle)

    def Eql(self, other):
        return self._Eql(self.handle, other)  # const alljoyn_message

    def SetEndianess(self):
        return self._SetEndianess(self.handle)


Message.bind_functions_to_cls()
