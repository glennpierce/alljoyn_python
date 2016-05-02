#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message, BusListener, BusAttachment
import signal
import time
import sys


INTERFACE_NAME = "net.allplay.MediaPlayer"
OBJECT_NAME = "net.allplay.MediaPlayer.i51e73778-31f3-4dc8-a33d-9237295005ae.rVeY693N7"
OBJECT_PATH = "/net/allplay/MediaPlayer"


class MyBusListener(BusListener.BusListener):
    def __init__(self, context=None):
        super(MyBusListener, self).__init__()

    def OnListenerRegisteredCallBack(self, context, bus):
        print "Registered"

    def OnFoundAdvertisedNameCallBack(self, context, name, transport, name_prefix):
        print "AwesomeSauce", context, name, transport, name_prefix

    def OnNameOwnerChangedCallBack(self, context, bus_name, previous_owner, new_owner):
        print "AwesomeSauce", contexPt, bus_name, previous_owner, new_owner


def signal_handler(signal, frame):
    global s_interrupt
    s_interrupt = True


if __name__ == "__main__":
    alljoyn = AllJoyn()

    alljoyn.RouterInit()

    signal.signal(signal.SIGINT, signal_handler)

    g_bus = BusAttachment.BusAttachment("BasicApp", True)

    iface = g_bus.CreateInterface(INTERFACE_NAME)
    iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "cat", "ss", "s", "inStr1,inStr2,outStr", 0)
    iface.Activate()

    g_bus.Start()

    try:
        g_bus.Connect(None)
    except QStatusException as ex:
        print "Have you got the daemon running ?"
        sys.exit(1)

    busListener = MyBusListener()
    g_bus.RegisterBusListener(busListener)

    g_bus.FindAdvertisedName(OBJECT_NAME)

    # Wait for join session to complete
    t = 0
    while t < 10:
        time.sleep(0.5)
        t += 0.5

    alljoyn.RouterShutdown()
