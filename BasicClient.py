#!/usr/bin/env python

from AllJoynPy import AllJoyn, Constants, QStatus
import ctypes as C
import signal
import sys


INTERFACE_NAME = "net.allplay.MediaPlayer";
OBJECT_NAME = "net.allplay.MediaPlayer.i51e73778-31f3-4dc8-a33d-9237295005ae.rVeY693N7";
OBJECT_PATH = "/net/allplay/MediaPlayer";

ROUTER = True

#static const alljoyn_sessionport SERVICE_PORT = 25;

#static QCC_BOOL s_joinInitiated = QCC_FALSE;
#static volatile QCC_BOOL s_joinComplete = QCC_FALSE;
#static alljoyn_sessionid s_sessionId = 0;

#/* Static BusListener */
#static alljoyn_buslistener s_busListener = NULL;

#static volatile QCC_BOOL s_interrupt = QCC_FALSE;


status = QStatus.ER_OK;

#    char* connectArgs = NULL;
#    alljoyn_interfacedescription testIntf = NULL;
#    unsigned long timeoutMs = ULONG_MAX;
#    unsigned long timeMs = 0;

#    /* Create a bus listener */
#    alljoyn_buslistener_callbacks callbacks = {
#        NULL,
#        NULL,
#        &found_advertised_name,
#        NULL,
#        &name_owner_changed,
#        NULL,
#        NULL,
#        NULL
#    };

#    if (alljoyn_init() != ER_OK) {
#        return 1;
#    }


def signal_handler(signal, frame):
    pass
    #QCC_UNUSED(sig);
    #s_interrupt = QCC_TRUE;
    #print('You pressed Ctrl+C!')
    #sys.exit(0)

alljoyn = AllJoyn('alljoyn_c')

print alljoyn.Init()

if ROUTER:
    if alljoyn.Routerinit() != ER_OK:
        alljoyn.Shutdown();
        sys.exit(1)
   

print "AllJoyn Library version:", alljoyn.GetVersion()
print "AllJoyn Library build info:", alljoyn.GetBuildInfo()

signal.signal(signal.SIGINT, signal_handler)

# Create message bus 
if status == QStatus.ER_OK:
    s_msgBus = alljoyn.BusattachmentCreate("myApp", Constants.QCC_TRUE) 
    
    print type(C.c_void_p())
    print s_msgBus, type(s_msgBus)

    testIntf = C.c_void_p()
    status = alljoyn.BusattachmentCreateinterface(s_msgBus, INTERFACE_NAME, C.byref(testIntf));
    
    if status == QStatus.ER_OK:
        print "Interface Created"
        print alljoyn.InterfaceDescriptionAddMember(testIntf, Constants.ALLJOYN_MESSAGE_METHOD_CALL, "cat", "ss",  "s", "inStr1,inStr2,outStr", 0)
        print alljoyn.InterfacedescriptionActivate(testIntf)
    else:
        print "Failed to create interface 'org.alljoyn.Bus.method_sample"
    
    
    # Start the msg bus 
    if status == QStatus.ER_OK:
        status = alljoyn.BusattachmentStart(s_msgBus);
        print "status BusattachmentStart", status
        if status != QStatus.ER_OK:
            print "alljoyn_busattachment_start failed"
        else:
            print "alljoyn_busattachment started."
        
    
    #print "Bus Attachment is started", alljoyn.BusattachmentIsstarted(s_msgBus)
    
    
    
    #connectArgs = C.c_char_p();
    #print "s_msgBus", s_msgBus
    # Connect to the bus 
    if status == QStatus.ER_OK:
        print "done0"
        status = alljoyn.BusattachmentConnect(s_msgBus, None)
        print "done"
        
        print status
        if status != QStatus.ER_OK:
            #if not connectArgs:
            #    connectArgs = "NULL"
            print "alljoyn_busattachment_connect(NULL) failed"
        else:
            print "alljoyn_busattachment connected to \"%s\"" % (alljoyn.BusattachmentGetconnectspec(s_msgBus),)
        
  
    
"""
    


   
"""
