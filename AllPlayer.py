#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message, BusListener, BusAttachment
import signal
import time
import sys

import ctypes as C

#SERVICE_NAME = "net.allplay.MediaPlayer.i51e73778-31f3-4dc8-a33d-9237295005ae.rH9ArLLIX"
#SERVICE_NAME = "net.allplay.MediaPlayer.i4a360b3d-95c5-4b67-9728-c2f74b875625.rX6nDdAbA"
SERVICE_NAME = "net.allplay.MediaPlayer.i9f5cf275-d33a-4ae6-8c57-c39d0487be3f.rUIe75rBf"
#SERVICE_NAME = "net.allplay.MediaPlayer"

SERVICE_PATH = "/net/allplay/MediaPlayer";
SERVICE_PORT = 1



# QStatus MakeMethodCall(void)
# {
#     ProxyBusObject remoteObj(*g_msgBus, SERVICE_NAME, SERVICE_PATH, s_sessionId);
#     const InterfaceDescription* alljoynTestIntf = g_msgBus->GetInterface(INTERFACE_NAME);

#     assert(alljoynTestIntf);
#     remoteObj.AddInterface(*alljoynTestIntf);

#     Message reply(*g_msgBus);
#     MsgArg inputs[2];

#     inputs[0].Set("s", "Hello ");
#     inputs[1].Set("s", "World!");

#     QStatus status = remoteObj.MethodCall(INTERFACE_NAME, "cat", inputs, 2, reply, 5000);

#     if (ER_OK == status) {
#         printf("'%s.%s' (path='%s') returned '%s'.\n", SERVICE_NAME, "cat",
#                SERVICE_PATH, reply->GetArg(0)->v_string.str);
#     } else {
#         printf("MethodCall on '%s.%s' failed.", SERVICE_NAME, "cat");
#     }

#     return status;
# }


class AllPlayer(object):

    def __init__(self, bus, name, session_id):
        self.bus = bus
        self.name = name
        self.session_id = session_id

        
        self.CreateInterfaces()
    
    def __repr__(self):
        return self.name

    def CreateInterfaces(self):
        pass
        iface = self.bus.CreateInterface("net.allplay.MCU")
        iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "GetCurrentItemUrl", None,  "s", None, 0)
     

        iface = self.bus.CreateInterface("net.allplay.MCU")
        ###AddMember(self, message_type, name, inputSig, outSig, argNames, annotation):
        iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "PlayItem", "ssssxss", None, None, 0)
        iface.Activate()


        
    #     <method name="GetAboutData">
    #   <arg name="languageTag" type="s" direction="in"/>
    #   <arg name="aboutData" type="a{sv}" direction="out"/>
    # </method>

    def CallGetCurrentItemUrl(self):

        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)

        iface = self.bus.GetInterface("net.allplay.MCU")
        proxyBusObject.AddInterface(iface)

        replyMsg = Message.Message(g_bus)

        proxyBusObject.MethodCall('net.allplay.MCU', "GetCurrentItemUrl", None, 0, replyMsg, 25000, 0)
        return replyMsg.GetArg(0).GetString()


    def CallInterface(self):
        
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.MCU")
        
        proxyBusObject.AddInterface(iface)
        # iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "PlayItem", None,  "ssssxss", None, 0)
        # iface.Activate()


        inputs = MsgArg.MsgArg.ArrayCreate(7)
        inputs.ArraySet(7, "ssssxss", [C.c_char_p, C.c_char_p, C.c_char_p, C.c_char_p,  C.c_longlong, C.c_char_p, C.c_char_p],
                            ['http://192.168.1.149:8000/test.mp3', 'Dummy', 'Dummy', 'Dummy', 200, 'Dummy', 'Dummy'])
        
        print "hmm", inputs.Signature()

        proxyBusObject.MethodCallNoReply('net.allplay.MCU', "PlayItem", inputs, 7, 0)


    
    # def GetAboutData(self):
    #     proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, "About", self.session_id)
    #     iface = self.bus.GetInterface("org.alljoyn.About")
    #     proxyBusObject.AddInterface(iface)


    #     arg = MsgArg.MsgArg()
    #     arg.SetString("en")

    #     replyMsg = Message.Message(g_bus)

    #     proxyBusObject.MethodCall('org.alljoyn.About', "GetAboutData", arg, 1, replyMsg, 25000, 0)
    #     print "here"

    #     print "net.allplay.MediaPlayer:", replyMsg.GetArg(0).GetSingleCompleteValue()


class MySessionListener(SessionListener.SessionListener):
    def __init__(self, callback_data=None):
        super(MySessionListener, self).__init__()

    def OnSessionLostCallBack(self, context, sessionId, reason):
        print "SessionLost sessionId = %u, Reason = %s" % (sessionId, reason)


class MyBusListener(BusListener.BusListener):
    def __init__(self, gbus):
        super(MyBusListener, self).__init__()
        self.g_bus = gbus
        self.sessionListener = MySessionListener()
        self.names = []

    def OnFoundAdvertisedNameCallBack(self, context, name, transport, name_prefix):

        if name.endswith('quiet'):
            return

        opts = Session.SessionOpts(Session.ALLJOYN_TRAFFIC_TYPE_MESSAGES,
                                        False,
                                        Session.ALLJOYN_PROXIMITY_ANY,
                                        TransportMask.ALLJOYN_TRANSPORT_ANY)
        # We found a remote bus that is advertising basic service's well-known name so connect to it.
        # Since we are in a callback we must enable concurrent callbacks before calling a synchronous method. 
        self.g_bus.EnableConcurrentCallBacks()

        # Bus name of attachment that is hosting the session to be joined.
        session_id = self.g_bus.JoinSession(name, SERVICE_PORT, self.sessionListener, opts)

        self.names.append(AllPlayer(self.g_bus, name, session_id))

    def OnNameOwnerChangedCallBack(self, context, bus_name, previous_owner, new_owner):
        print "NameOwnerChanged", context, bus_name, previous_owner, new_owner


def signal_handler(signal, frame):
    global s_interrupt
    s_interrupt = True;


if __name__ == "__main__":
    alljoyn = AllJoyn()

    signal.signal(signal.SIGINT, signal_handler)

    g_bus = BusAttachment.BusAttachment("AllPlayerApp", True) 
    g_bus.Start()

    try:
        g_bus.Connect(None)
    except QStatusException as ex:
        print "Have you got the daemon running ?"
        sys.exit(1)  
    
    busListener = MyBusListener(g_bus)
    g_bus.RegisterBusListener(busListener)
       
    g_bus.FindAdvertisedName(SERVICE_NAME)
        
    # Wait for join session to complete 
    t=0
    while t < 2.5:
        time.sleep(0.5)
        t+=0.5    

    for allplayer in busListener.names:
        print allplayer.CallGetCurrentItemUrl()
        allplayer.CallInterface()
        
