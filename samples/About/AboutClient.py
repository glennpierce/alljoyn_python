#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message
import signal
import time
import sys

timeout = 10

#INTERFACE_NAME = "com.example.about.feature.interface.sample"
INTERFACE_NAME = "net.allplay.MediaPlayer"

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
        self.sessionListener = MySessionListener()
        self.bus_attachment = bus_attachment

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

        print "BusName", busName

        print "objectDescriptionArg", objectDescriptionArg, type(objectDescriptionArg)
        print "aboutDataArg", aboutDataArg, type(aboutDataArg)
        
        objectDescription = AboutObjectDescription.AboutObjectDescription(objectDescriptionArg)

        print "*********************************************************************************"
        print "Announce signal discovered"
        print "\tFrom bus", busName
        print "\tAbout version", version
        print "\tSessionPort", port
        print "\tObjectDescription:"
        print "*********************************************************************************"
        print "Announce signal discovered"

        for path in objectDescription.GetPaths():
            print "\t\t", path
            for interface in objectDescription.GetInterfaces(path):
                print "\t\t\t", interface

        print "\tAboutData:"
        aboutData = AboutData.AboutData(aboutDataArg, language="en")

        self.printAboutData(aboutData, None, 2)

        print "*********************************************************************************"

        opts = Session.SessionOpts(Session.ALLJOYN_TRAFFIC_TYPE_MESSAGES,
                                    False,
                                    Session.ALLJOYN_PROXIMITY_ANY,
                                    TransportMask.ALLJOYN_TRANSPORT_ANY)

        self.bus_attachment.EnableConcurrentCallBacks()

        print "JoiningSession", "busName", busName, "port", port, "opts", opts
        sessionId = self.bus_attachment.JoinSession(busName, port, self.sessionListener, opts)
        print "SessionJoined sessionId = ", sessionId

        aboutProxy = AboutProxy.AboutProxy(self.bus_attachment, busName, sessionId)

        objArg = aboutProxy.GetObjectDescription()
        print "*********************************************************************************"
        print "AboutProxy.GetObjectDescription:"

        aboutObjectDescription = AboutObjectDescription.AboutObjectDescription(objArg)

        for path in aboutObjectDescription.GetPaths():
            print "\t", path
            for interface in aboutObjectDescription.GetInterfaces(path):
                print "\t\t", interface

        aArg = aboutProxy.GetAboutData()
        print "*********************************************************************************"
        print "AboutProxy.GetAboutData: (Default Language)"

        defaultLangAboutData = AboutData.AboutData()
        self.printAboutData(defaultLangAboutData, None, 1)
        
        defaultLanguage = defaultLangAboutData.GetDefaultLanguage()
        # Print out the AboutData for every language but the default it has already been printed.
        
        for lang in defaultLangAboutData.GetSupportedLanguages():
            if lang != defaultLanguage:
                aArg = aboutProxy.GetAboutData(language=lang)
                printAboutData(aArg, lang, 1);
            ver = aboutProxy.GetVersion()
            print "*********************************************************************************"
            print "AboutProxy.GetVersion %hd" % (ver,)
            print "*********************************************************************************"
            path = objectDescription.GetInterfacePaths(INTERFACE_NAME)[0];
            print "Calling %s/%s" % (path, INTERFACE_NAME)
            print "busName", busName, type(busName)
            print "path", path, type(path)
            print "sessionId", sessionId, type(sessionId)
            proxyBusObject = ProxyBusObject.ProxyBusObject(g_bus, busName, path, sessionId)
           
            print "proxyBusObject", proxyBusObject
            try:
                proxyBusObject.IntrospectRemoteObject()
            except QStatusException, ex:
                print "Failed to introspect remote object."
                
            arg = MsgArg.MsgArg()
            arg.SetString("ECHO Echo echo...")
            
            replyMsg = Message.Message(self.bus_attachment)
            
            proxyBusObject.MethodCall(INTERFACE_NAME, "Echo", arg, 1, replyMsg, 25000, 0)
    
            print "Echo method reply:", replyMsg.GetArg(0).GetString()


if __name__ == "__main__":

    # Install SIGINT handler so Ctrl + C deallocates memory properly
    alljoyn = AllJoyn()

    alljoyn.RouterInit()

    print "AllJoyn Library version:", alljoyn.Version
    print "AllJoyn Library build info:", alljoyn.BuildInfo

    signal.signal(signal.SIGINT, signal_handler)

    # Create message bus
    g_bus = alljoyn.BusAttachment.BusAttachment("AboutServiceTest", True)

    # Start the msg bus
    g_bus.Start()

    print "Bus started"

    try:
        g_bus.Connect(None)
    except QStatusException as ex:
        print "Have you got the daemon running ?"
        sys.exit(1)

    print g_bus.GetUniqueName()

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
