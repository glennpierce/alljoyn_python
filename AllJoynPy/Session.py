import sys, types
import ctypes as C
from ctypes import POINTER
from enum import Enum, unique
from . import AllJoynMeta, AllJoynObject
# Wrapper for file Session.h


#define ALLJOYN_SESSION_PORT_ANY (alljoyn_sessionport)0
#define ALLJOYN_SESSION_ID_ALL_HOSTED ((alljoyn_sessionid)(-1))
#define ALLJOYN_TRAFFIC_TYPE_MESSAGES        0x01   /**< Session carries message traffic */
#define ALLJOYN_TRAFFIC_TYPE_RAW_UNRELIABLE  0x02   /**< Session carries an unreliable (lossy) byte stream */
#define ALLJOYN_TRAFFIC_TYPE_RAW_RELIABLE    0x04   /**< Session carries a reliable byte stream */
#define ALLJOYN_PROXIMITY_ANY       0xFF /**< Accept any proximity options */
#define ALLJOYN_PROXIMITY_PHYSICAL  0x01 /**< Limit the session to the same physical device */
#define ALLJOYN_PROXIMITY_NETWORK   0x02 /**< Limit the session to network proximity */


#define ALLJOYN_SESSION_PORT_ANY (alljoyn_sessionport)0
#define ALLJOYN_SESSION_ID_ALL_HOSTED ((alljoyn_sessionid)(-1))
#define ALLJOYN_TRAFFIC_TYPE_MESSAGES        0x01   /**< Session carries message traffic */
#define ALLJOYN_TRAFFIC_TYPE_RAW_UNRELIABLE  0x02   /**< Session carries an unreliable (lossy) byte stream */
#define ALLJOYN_TRAFFIC_TYPE_RAW_RELIABLE    0x04   /**< Session carries a reliable byte stream */
#define ALLJOYN_PROXIMITY_ANY       0xFF /**< Accept any proximity options */
#define ALLJOYN_PROXIMITY_PHYSICAL  0x01 /**< Limit the session to the same physical device */
#define ALLJOYN_PROXIMITY_NETWORK   0x02 /**< Limit the session to network proximity */



# Typedefs
# struct _alljoyn_sessionopts_handle * alljoyn_sessionopts
# int alljoyn_sessionport
# int alljoyn_sessionid


if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE
    




class SessionOpts(AllJoynObject):
    
    __metaclass__ = AllJoynMeta
    
    _cmethods = {u'CMP': (u'alljoyn_sessionopts_cmp',
          (u'int', C.c_int),
          ((u'const alljoyn_sessionopts', C.c_void_p),
           (u'const alljoyn_sessionopts', C.c_void_p))),
 u'Create': (u'alljoyn_sessionopts_create',
             (u'alljoyn_sessionopts', C.c_void_p),
             ((u'int', C.c_int),
              (u'int', C.c_int),
              (u'int', C.c_int),
              (u'int', C.c_int))),
 u'Destroy': (u'alljoyn_sessionopts_destroy',
              (u'void', None),
              ((u'alljoyn_sessionopts', C.c_void_p),)),
 u'GetMuLTIPOINT': (u'alljoyn_sessionopts_get_multipoint',
                    (u'int', C.c_int),
                    ((u'const alljoyn_sessionopts', C.c_void_p),)),
 u'GetProximity': (u'alljoyn_sessionopts_get_proximity',
                   (u'int', C.c_int),
                   ((u'const alljoyn_sessionopts', C.c_void_p),)),
 u'GetTraffic': (u'alljoyn_sessionopts_get_traffic',
                 (u'int', C.c_int),
                 ((u'const alljoyn_sessionopts', C.c_void_p),)),
 u'GetTransports': (u'alljoyn_sessionopts_get_transports',
                    (u'int', C.c_int),
                    ((u'const alljoyn_sessionopts', C.c_void_p),)),
 u'IsCompatible': (u'alljoyn_sessionopts_iscompatible',
                   (u'int', C.c_int),
                   ((u'const alljoyn_sessionopts', C.c_void_p),
                    (u'const alljoyn_sessionopts', C.c_void_p))),
 u'SetMuLTIPOINT': (u'alljoyn_sessionopts_set_multipoint',
                    (u'void', None),
                    ((u'alljoyn_sessionopts', C.c_void_p),
                     (u'int', C.c_int))),
 u'SetProximity': (u'alljoyn_sessionopts_set_proximity',
                   (u'void', None),
                   ((u'alljoyn_sessionopts', C.c_void_p),
                    (u'int', C.c_int))),
 u'SetTraffic': (u'alljoyn_sessionopts_set_traffic',
                 (u'void', None),
                 ((u'alljoyn_sessionopts', C.c_void_p),
                  (u'int', C.c_int))),
 u'SetTransports': (u'alljoyn_sessionopts_set_transports',
                    (u'void', None),
                    ((u'alljoyn_sessionopts', C.c_void_p),
                     (u'int', C.c_int)))}
    
    def __init__(self):
        pass
        
    def __del__(self):
        #self.SessionOptsDestroy(self.handle)
        pass

    # Wrapper Methods

    def Create(self, isMultipoint,proximity,transports):
        return self._Create(self.handle,isMultipoint,proximity,transports) # int,int,int

    def Destroy(self):
        return self._Destroy(self.handle)

    def GetTraffic(self):
        return self._GetTraffic(self.handle)

    def SetTraffic(self, traffic):
        return self._SetTraffic(self.handle,traffic) # int

    def GetMuLTIPOINT(self):
        return self._GetMuLTIPOINT(self.handle)

    def SetMuLTIPOINT(self, isMultipoint):
        return self._SetMuLTIPOINT(self.handle,isMultipoint) # int

    def GetProximity(self):
        return self._GetProximity(self.handle)

    def SetProximity(self, proximity):
        return self._SetProximity(self.handle,proximity) # int

    def GetTransports(self):
        return self._GetTransports(self.handle)

    def SetTransports(self, transports):
        return self._SetTransports(self.handle,transports) # int

    def IsCompatible(self, other):
        return self._IsCompatible(self.handle,other) # const alljoyn_sessionopts

    def CMP(self, other):
        return self._CMP(self.handle,other) # const alljoyn_sessionopts

    


Session.bind_functions_to_cls()