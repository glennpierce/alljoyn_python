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

import BusObject, Message, InterfaceDescription

# Wrapper for file MessageReceiver.h

if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE



# typedef void (AJ_CALL * alljoyn_messagereceiver_methodhandler_ptr)(alljoyn_busobject bus,
#                                                                    const alljoyn_interfacedescription_member* member,
#                                                                    alljoyn_message message);
MessageReceiverMethodHandlerFuncType = CallbackType(
    None, BusObject.BusObjectHandle, POINTER(InterfaceDescription.InterfaceDescriptionMember), Message.MessageHandle)  # bus member message


# typedef void (AJ_CALL * alljoyn_messagereceiver_signalhandler_ptr)(const alljoyn_interfacedescription_member* member,
#                                                                    const char* srcPath, alljoyn_message message);
MessageReceiverSignalHandlerFuncType = CallbackType(
    None, POINTER(InterfaceDescription.InterfaceDescriptionMember), C.c_char_p, Message.MessageHandle)  # member srcPath message


# typedef void (AJ_CALL * alljoyn_messagereceiver_replyhandler_ptr)(alljoyn_message message, void* context);
MessageReceiverReplyHandlerFuncType = CallbackType(None, Message.MessageHandle, C.c_void_p)  # message context







