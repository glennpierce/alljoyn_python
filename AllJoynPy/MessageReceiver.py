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
    
import sys, types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject, InterfaceDescription, Message

# Wrapper for file MessageReceiver.h

# Typedefs
# struct _alljoyn_busobject_handle * alljoyn_busobject
# void (*)(alljoyn_busobject, const int *, int) alljoyn_messagereceiver_methodhandler_ptr
# void (*)(int, void *) alljoyn_messagereceiver_replyhandler_ptr
# void (*)(const int *, const char *, int) alljoyn_messagereceiver_signalhandler_ptr


if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE
    
MessageReceiverMethodHandlerFuncType = CallbackType(None, C.c_void_p, POINTER(InterfaceDescription.InterfaceDescriptionMember), C.c_void_p) # bus member message
MessageReceiverSignalHandlerFuncType = CallbackType(None, POINTER(InterfaceDescription.InterfaceDescriptionMember), C.c_char_p, C.c_void_p) # member srcPath message
MessageReceiverReplyHandlerFuncType = CallbackType(None, C.c_void_p, C.c_void_p) # message context

