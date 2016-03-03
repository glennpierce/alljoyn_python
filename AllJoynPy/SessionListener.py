import sys, types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject

# Wrapper for file SessionListener.h

@unique
class SessionLostReason(Enum):
    ALLJOYN_SESSIONLOST_INVALID = 0
    ALLJOYN_SESSIONLOST_REMOTE_END_LEFT_SESSION = 1
    ALLJOYN_SESSIONLOST_REMOTE_END_CLOSED_ABRUPTLY = 2
    ALLJOYN_SESSIONLOST_REMOVED_BY_BINDER = 3
    ALLJOYN_SESSIONLOST_LINK_TIMEOUT = 4
    ALLJOYN_SESSIONLOST_REASON_OTHER = 5

# Typedefs
# enum alljoyn_sessionlostreason alljoyn_sessionlostreason
# struct _alljoyn_sessionlistener_handle * alljoyn_sessionlistener
# void (*)(const void *, int, alljoyn_sessionlostreason) alljoyn_sessionlistener_sessionlost_ptr
# void (*)(const void *, int, const char *) alljoyn_sessionlistener_sessionmemberadded_ptr
# void (*)(const void *, int, const char *) alljoyn_sessionlistener_sessionmemberremoved_ptr
# struct alljoyn_sessionlistener_callbacks alljoyn_sessionlistener_callbacks

if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE
    
#typedef void (AJ_CALL * alljoyn_sessionlistener_sessionlost_ptr)(const void* context, alljoyn_sessionid sessionId, alljoyn_sessionlostreason reason);
SessionListenerSessionLostFuncType = CallbackType(None, C.c_void_p, C.c_int, C.c_int) # context sessionId reason

#typedef void (AJ_CALL * alljoyn_sessionlistener_sessionmemberadded_ptr)(const void* context, alljoyn_sessionid sessionId, const char* uniqueName);
SessionListenerSessionMemberAddedFuncType = CallbackType(None, C.c_void_p, C.c_int, C.c_char_p) # context sessionId uniqueName

#typedef void (AJ_CALL * alljoyn_sessionlistener_sessionmemberremoved_ptr)(const void* context, alljoyn_sessionid sessionId, const char* uniqueName);
SessionListenerSessionMemberRemovedFuncType = CallbackType(None, C.c_void_p, C.c_int, C.c_char_p) # context sessionId uniqueName


class SessionListenerCallBacks(C.Structure):
    _fields_ = [
                ("SessionLost", SessionListenerSessionLostFuncType),
                ("SessionMemberAdded", SessionListenerSessionMemberAddedFuncType),
                ("SessionMemberRemoved", SessionListenerSessionMemberRemovedFuncType)
               ]


class SessionListener(AllJoynObject):
    
    __metaclass__ = AllJoynMeta
    
    _cmethods = {u'Create': (u'alljoyn_sessionlistener_create', (u'alljoyn_sessionlistener', C.c_void_p), 
                                                                   ((u'const alljoyn_sessionlistener_callbacks *', POINTER(SessionListenerCallBacks)),
                                                                    (u'const void *', C.c_void_p))),
                 
                 u'Destroy': (u'alljoyn_sessionlistener_destroy', (u'void', None), ((u'alljoyn_sessionlistener', C.c_void_p),))}


    def __init__(self, callback_data=None):
        
        super(SessionListener, self).__init__()
        
        #print "init  self", self, id(self)
        
        self.callback_structure = SessionListenerCallBacks()
    
        #print "callback_structure",  self.callback_structure, id(self.callback_structure)
        
        self.callback_data = callback_data

        self.callback_structure.SessionLost = SessionListenerSessionLostFuncType(SessionListener._OnSessionLostCallBack)
        self.callback_structure.SessionMemberAdded = SessionListenerSessionMemberAddedFuncType(SessionListener._OnSessionMemberAddedCallback)
        self.callback_structure.SessionMemberRemoved = SessionListenerSessionMemberRemovedFuncType(SessionListener._OnSessionMemberRemovedCallBack)
        
        print "self.callback_structure", self.callback_structure
        
        # We pass the id of self tothe callback here as the context so we can get self in the callback.
        # Usuall ctypes would handle the self magic but in this case the ptr is stuck into a structure
        # and ctypes does not then do the magic
        # print ctypes.cast(ctypes.c_longlong(id(a)).value, ctypes.py_object).value
        
        # alljoyn_sessionlistener_create(const alljoyn_sessionlistener_callbacks* callbacks, const void* context);

        #print "dddd", self, id(self)
        
        
        #self.unique_id = AllJoynObject.unique_id_count
        #AllJoynObject.unique_id_count += 1
        #unique_instances[self.unique_id] = self
        
        print "unqiue id", self.unique_id
        self.unique = C.c_int(self.unique_id)
        self.handle = self._Create(C.byref(self.callback_structure), C.byref(self.unique))
        
        #self.handle = self._Create(C.byref(self.callback_structure), C.c_void_p(id(self)))
        #self.handle = self._Create(None, C.c_void_p(id(self)))
     
    def __del__(self):
        print "In del"
        if self.handle:
            return self._Destroy(self.handle)

    @staticmethod
    def  _OnSessionLostCallBack(context, sessionId, reason):  # const void* context, alljoyn_sessionid sessionId, alljoyn_sessionlostreason reason)
        #print "harley", C.cast(context, C.c_int).value
        print "OHH", type(context), context
        #self = C.cast(context, C.py_object).value
        self = AllJoynObject.unique_instances[context]
        print "selfy", self, id(self)
        self.OnSessionLostCallBack(self.callback_data, sessionId, reason)
        
    @staticmethod
    def _OnSessionMemberAddedCallback(context, sessionId, uniqueName):
        print "_OnSessionMemberRemovedCallBack"
        self = C.cast(context, C.py_object).value
        self.OnSessionMemberAddedCallback(self.callback_data, sessionId, uniqueName)
        
    @staticmethod
    def _OnSessionMemberRemovedCallBack(context, sessionId, uniqueName):
        print "_OnSessionLostCallBack"
        self = C.cast(context, C.py_object).value
        self.OnSessionMemberRemovedCallBack(self.callback_data, sessionId, uniqueName)
        
        
    def OnSessionLostCallBack(self, context, sessionId, reason):
        pass
    
    def OnSessionMemberAddedCallback(self, context, sessionId, uniqueName):
        pass
    
    def OnSessionMemberRemovedCallBack(self, context, sessionId, uniqueName):
        pass
    
SessionListener.bind_functions_to_cls()
