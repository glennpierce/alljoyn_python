#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message
import signal
import time
import sys

timeout = 5

INTERFACE_NAME = "net.allplay.MediaPlayer"

# /About
#             org.alljoyn.About
#         /net/allplay/MediaPlayer
#             net.allplay.MCU
#             net.allplay.MediaPlayer
#             net.allplay.ZoneManager
#             org.alljoyn.Control.Volume


def signal_handler(signal, frame):
    global s_interrupt
    s_interrupt = True


class MySessionListener(SessionListener.SessionListener):
    def __init__(self, callback_data=None):
        super(MySessionListener, self).__init__()

    def OnSessionLostCallBack(self, context, sessionId, reason):
        print "SessionLost sessionId = %u, Reason = %s" % (sessionId, reason)


class MyAboutListener(AboutListener.AboutListener):
    def __init__(self, bus_attachment, context=None):
        super(MyAboutListener, self).__init__(context=context)
        self.bus = bus_attachment
        self.sessionListener = MySessionListener()

   

    def OnAboutListenerCallBack(self, context, busName, version, port, objectDescriptionArg, aboutDataArg):

        global s_interrupt

        objectDescription = AboutObjectDescription.AboutObjectDescription(objectDescriptionArg)

        print objectDescription.GetPaths()

        aboutData = AboutData.AboutData(aboutDataArg, language="en")

        print {f:aboutData.GetField(f).GetSingleCompleteValue() for f in aboutData.GetFields()}

        #self.printAboutData(aboutData, None, 2)

        print "*********************************************************************************"

        opts = Session.SessionOpts(Session.ALLJOYN_TRAFFIC_TYPE_MESSAGES,
                                   False,
                                   Session.ALLJOYN_PROXIMITY_ANY,
                                   TransportMask.ALLJOYN_TRANSPORT_ANY)

        self.bus.EnableConcurrentCallBacks()
        sessionId = self.bus.JoinSession(busName, port, self.sessionListener, opts)

        aboutProxy = AboutProxy.AboutProxy(self.bus, busName, sessionId)

        objArg = aboutProxy.GetObjectDescription()

        aboutObjectDescription = AboutObjectDescription.AboutObjectDescription(objArg)

        for path in aboutObjectDescription.GetPaths():
            print "\t", path
            for interface in aboutObjectDescription.GetInterfaces(path):
                print "\t\t", interface

        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, busName, '/net/allplay/MediaPlayer', sessionId)
           
        try:
            proxyBusObject.IntrospectRemoteObject()
        except QStatusException, ex:
            print "Failed to introspect remote object."
                

        replyMsg = Message.Message(self.bus)
        proxyBusObject.MethodCall('net.allplay.MCU', "GetCurrentItemUrl", None, 0, replyMsg, 25000, 0)
        print "GetCurrentItemUrl:", replyMsg.GetArg(0).GetString()

            # arg = MsgArg.MsgArg()
            # arg.SetString("ECHO Echo echo...")
            
        #replyMsg = Message.Message(self.bus)    
        #proxyBusObject.MethodCall('net.allplay.MCU', "GetCurrentItemUrl", arg, 1, replyMsg, 25000, 0)
        #print "GetCurrentItemUrl:", replyMsg.GetArg(0).GetString()


if __name__ == "__main__":

    # Install SIGINT handler so Ctrl + C deallocates memory properly
    alljoyn = AllJoyn()

    print "AllJoyn Library version:", alljoyn.Version
    print "AllJoyn Library build info:", alljoyn.BuildInfo

    alljoyn.RouterInit()

    signal.signal(signal.SIGINT, signal_handler)

    # Create message bus
    g_bus = alljoyn.BusAttachment.BusAttachment("AboutServiceTest", True)

    # Start the msg bus
    g_bus.Start()

    try:
        g_bus.Connect(None)
    except QStatusException as ex:
        print "Have you got the daemon running ?"
        sys.exit(1)

    aboutListener = MyAboutListener(g_bus)

    g_bus.RegisterAboutListener(aboutListener)

    g_bus.WhoImplementsInterfaces([INTERFACE_NAME])

    s_interrupt = False
    t = 0
    while s_interrupt is False:
        time.sleep(0.1)
        t += 0.1

        if t >= timeout:
            break

    g_bus.Stop()
    g_bus.Join()

    alljoyn.RouterShutdown()
    time.sleep(2)
