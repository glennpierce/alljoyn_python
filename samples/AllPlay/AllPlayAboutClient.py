#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message
import signal
import time
import sys

timeout = 10

#INTERFACE_NAME = "net.allplay.MediaPlayer"
INTERFACE_NAMES = ["net.allplay.MediaPlayer", 'net.allplay.MCU', "net.allplay.ZoneManager"]


def signal_handler(signal, frame):
    s_interrupt = True


class MySessionListener(SessionListener.SessionListener):
    def __init__(self, callback_data=None):
        super(MySessionListener, self).__init__()

    def OnSessionLostCallBack(self, context, sessionId, reason):
        print "SessionLost sessionId = %u, Reason = %s" % (sessionId, reason)


class MyAboutListener(AboutListener.AboutListener):
    def __init__(self, bus_attachment, context=None):
        super(MyAboutListener, self).__init__(context=context)
        self.bus_attachment = bus_attachment
        self.sessionListener = MySessionListener()

    # Print out the fields found in the AboutData. Only fields with known signatures
    # are printed out.  All others will be treated as an unknown field.
    def printAboutData(self, aboutData, language, tabNum):
        for field in aboutData.GetFields():
            print "\t" * tabNum, "Key:", field,

            tmp = aboutData.GetField(field, language=language)

            print "Signature", tmp.Signature()

            if tmp.Signature().startswith("ay"):
                print "\t", ' '.join(["%02x " % v for v in tmp.GetSingleCompleteValue()])
            elif tmp.Signature().startswith("as"):
                print "\t",  ' '.join([v for v in tmp.GetSingleCompleteValue()])
            elif tmp.Signature().startswith("s"):
                print "\t", tmp.GetSingleCompleteValue()
            else:
                print "User Defined Value\tSignature: ", tmp.Signature()

    def OnAboutListenerCallBack(self, context, busName, version, port, objectDescriptionArg, aboutDataArg):        
        objectDescription = AboutObjectDescription.AboutObjectDescription(objectDescriptionArg)

        aboutData = AboutData.AboutData(aboutDataArg, language="en")

        print "Device Name", aboutData.GetDeviceName()

        opts = Session.SessionOpts(Session.ALLJOYN_TRAFFIC_TYPE_MESSAGES,
                                   False,
                                   Session.ALLJOYN_PROXIMITY_ANY,
                                   TransportMask.ALLJOYN_TRANSPORT_ANY)

        g_bus.EnableConcurrentCallBacks()
        sessionId = g_bus.JoinSession(busName, port, self.sessionListener, opts)

        aboutProxy = AboutProxy.AboutProxy(g_bus, busName, sessionId)

        objArg = aboutProxy.GetObjectDescription()

        aboutObjectDescription = AboutObjectDescription.AboutObjectDescription(objArg)

        for path in aboutObjectDescription.GetPaths():
            print "\t ObjectPath: ", path
            for interface in aboutObjectDescription.GetInterfaces(path):
                print "\t\t", interface

        proxyBusObject = ProxyBusObject.ProxyBusObject(g_bus, busName, '/About', sessionId)
           
        try:
            proxyBusObject.IntrospectRemoteObject()
            iface = proxyBusObject.GetInterface("org.alljoyn.About")
            print iface.Introspect()
        except QStatusException, ex:
            print "Failed to introspect remote object."


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

    print g_bus.GetUniqueName()

    aboutListener = MyAboutListener(g_bus)

    g_bus.RegisterAboutListener(aboutListener)

    #g_bus.WhoImplementsInterfaces([INTERFACE_NAME])
    g_bus.WhoImplementsInterfaces(INTERFACE_NAMES)

    s_interrupt = False
    t = 0
    while s_interrupt is False:
        time.sleep(0.1)
        t += 0.1

        if t >= timeout:
            break


#    try:
#    while True:
#        time.sleep(10)
#except KeyboardInterrupt:
#    print 'interrupted!'


    g_bus.Stop()
    g_bus.Join()

    alljoyn.RouterShutdown()
