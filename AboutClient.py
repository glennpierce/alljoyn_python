#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy
import signal
import time
import sys

timeout = 10

INTERFACE_NAME = "net.allplay.MediaPlayer"


def signal_handler(signal, frame):
    # QCC_UNUSED(sig);
    s_interrupt = True


class MySessionListener(SessionListener.SessionListener):
    def __init__(self, callback_data=None):
        super(MySessionListener, self).__init__()

    def OnSessionLostCallBack(self, context, sessionId, reason):
        print "SessionLost sessionId = %u, Reason = %d" % (sessionId, reason)


class MyAboutListener(AboutListener.AboutListener):
    def __init__(self, callback_data=None):
        super(MyAboutListener, self).__init__(callback_data=callback_data)
        print "MyAboutListener __init__", id(self)
        self.sessionListener = MySessionListener()

    # Print out the fields found in the AboutData. Only fields with known signatures
    # are printed out.  All others will be treated as an unknown field.
    def printAboutData(self, aboutData, language, tabNum):
        for field in aboutData.GetFields():
            print "\t" * tabNum, "Key:", field,

            tmp = aboutData.GetField(field)

            if tmp.Signature().startswith("ay"):
                print "\t", ' '.join(["%02x " % v for v in tmp.GetSingleCompleteValue()])
            elif tmp.Signature().startswith("as"):
                print "\t", [v for v in tmp.GetSingleCompleteValue()]
            elif tmp.Signature().startswith("s"):
                print "\t", tmp.GetSingleCompleteValue()
            else:
                print "User Defined Value\tSignature: ", tmp.Signature()

    def OnAboutListenerCallBack(self, context, busName, version, port, objectDescriptionArg, aboutDataArg):

        g_bus = context

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

        # print "*********************************************************************************"

        # opts = Session.SessionOpts(Session.ALLJOYN_TRAFFIC_TYPE_MESSAGES,
        #                            False,
        #                            Session.ALLJOYN_PROXIMITY_ANY,
        #                            TransportMask.ALLJOYN_TRANSPORT_ANY)

        # print g_bus
        # g_bus.EnableConcurrentCallBacks()
        # sessionId = g_bus.JoinSession(busName, port, self.sessionListener, opts)
        # print "SessionJoined sessionId = ", sessionId

        # aboutProxy = AboutProxy.AboutProxy(g_bus, busName, sessionId)

        # objArg = aboutProxy.GetObjectDescription()
        # print "*********************************************************************************"
        # print "AboutProxy.GetObjectDescription:"
        # #AboutObjectDescription.AboutObjectDescription(objArg)

        # aboutObjectDescription = AboutObjectDescription.AboutObjectDescription(objArg)





    
               
                
                # 
                # AboutObjectDescription aboutObjectDescription(objArg);
                #path_num = aboutObjectDescription.GetPaths(NULL, 0);
                # paths = new const char*[path_num];
                #aboutObjectDescription.GetPaths(paths, path_num);
                # for (size_t i = 0; i < path_num; ++i) {
                    #printf("\t%s\n", paths[i]);
                    # size_t intf_num = aboutObjectDescription.GetInterfaces(paths[i], NULL, 0);
                    # const char** intfs = new const char*[intf_num];
                    #aboutObjectDescription.GetInterfaces(paths[i], intfs, intf_num);
                    # for (size_t j = 0; j < intf_num; ++j) {
                        #printf("\t\t%s\n", intfs[j]);
                    #}
                    # delete [] intfs;
                #}
                # delete [] paths;

                # MsgArg aArg;
                #aboutProxy.GetAboutData("en", aArg);
                # printf("*********************************************************************************\n");
                #printf("AboutProxy.GetAboutData: (Default Language)\n");
                # AboutData defaultLangAboutData(aArg);
                #printAboutData(defaultLangAboutData, NULL, 1);
                # size_t lang_num;
                #lang_num = defaultLangAboutData.GetSupportedLanguages();
                #// If the lang_num == 1 we only have a default language
                # if (lang_num > 1) {
                    # const char** langs = new const char*[lang_num];
                    #defaultLangAboutData.GetSupportedLanguages(langs, lang_num);
                    #char* defaultLanguage;
                    # defaultLangAboutData.GetDefaultLanguage(&defaultLanguage);
                    #// print out the AboutData for every language but the
                    #// default it has already been printed.
                    # for (size_t i = 0; i < lang_num; ++i) {
                        # if (strcmp(defaultLanguage, langs[i]) != 0) {
                            #status = aboutProxy.GetAboutData(langs[i], aArg);
                            # if (ER_OK == status) {
                                #defaultLangAboutData.CreatefromMsgArg(aArg, langs[i]);
                                #printf("AboutProxy.GetAboutData: (%s)\n", langs[i]);
                                #printAboutData(defaultLangAboutData, langs[i], 1);
                            #}
                        #}
                    #}
                    # delete [] langs;
                #}

                # uint16_t ver;
                # aboutProxy.GetVersion(ver);
                # printf("*********************************************************************************\n");
                #printf("AboutProxy.GetVersion %hd\n", ver);
                # printf("*********************************************************************************\n");

                # const char* path;
                # objectDescription.GetInterfacePaths(INTERFACE_NAME, &path, 1);
                #printf("Calling %s/%s\n", path, INTERFACE_NAME);
                # ProxyBusObject proxyObject(*g_bus, busName, path, sessionId);
                #status = proxyObject.IntrospectRemoteObject();
                # if (status != ER_OK) {
                    #printf("Failed to introspect remote object.\n");
                #}
                # MsgArg arg("s", "ECHO Echo echo...\n");
                # Message replyMsg(*g_bus);
                # status = proxyObject.MethodCall(INTERFACE_NAME, "Echo", &arg, 1, replyMsg);
                # if (status != ER_OK) {
                    #printf("Failed to call Echo method.\n");
                    # return;
                #}
                #char* echoReply;
                # status = replyMsg->GetArg(0)->Get("s", &echoReply);
                # if (status != ER_OK) {
                    #printf("Failed to read Echo method reply.\n");
                #}
                #printf("Echo method reply: %s\n", echoReply);
            #}
        #} else {
            #printf("BusAttachment is NULL\n");
        #}
    #}
    # MySessionListener sessionListener;

        pass

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
