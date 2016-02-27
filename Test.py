#!/usr/bin/env python

from AllJoynPy import AllJoyn
import signal, time
import sys


INTERFACE_NAME = "com.example.about.feature.interface.sample"


def signal_handler(signal, frame):
    QCC_UNUSED(sig);
    s_interrupt = QCC_TRUE;


if __name__ == "__main__":
    # Install SIGINT handler so Ctrl + C deallocates memory properly
    alljoyn = AllJoyn()

    print "AllJoyn Library version:", alljoyn.Version
    print "AllJoyn Library build info:", alljoyn.BuildInfo

    signal.signal(signal.SIGINT, signal_handler)

    # Create message bus 
    g_bus = alljoyn.BusAttachment.BusAttachment("AboutServiceTest", True)

    # Start the msg bus 
    g_bus.Start()
    
    g_bus.Connect(None)

    print g_bus.GetUniqueName()
