#!/usr/bin/env python

import AllJoynPy
from AllJoynPy import AllJoyn, Constants, QStatus
from callbacks import *
import ctypes as C
import signal, time
import sys
from ctypes import POINTER


if sys.platform == 'win32':
    CallbackType = C.WINFUNCTYPE
else:
    CallbackType = C.CFUNCTYPE


#Note the removal of almost all Error handling to make the sample code more
#straight forward to read.  This is only used here for demonstration actual
#programs should check the return values of all method calls.
 

INTERFACE_NAME = "com.example.about.feature.interface.sample"
#INTERFACE_NAME = "net.allplay.MediaPlayer";


def signal_handler(signal, frame):
    QCC_UNUSED(sig);
    s_interrupt = QCC_TRUE;


if __name__ == "__main__":
    # Install SIGINT handler so Ctrl + C deallocates memory properly
    alljoyn = AllJoyn('alljoyn_c')

    print alljoyn.Init()

    print "AllJoyn Library version:", alljoyn.GetVersion()
    print "AllJoyn Library build info:", alljoyn.GetBuildInfo()

    signal.signal(signal.SIGINT, signal_handler)


    # Create message bus 
    g_bus = BusAttachment("AboutServiceTest", Constants.QCC_TRUE)

    # Start the msg bus 
    g_bus.Start()
    
    status = gbus.Connect(None)

    if status == QStatus.ER_OK:
        print "BusAttachment connect succeeded. BusName", alljoyn.BusattachmentGetuniquename(g_bus)
