#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message, BusListener, BusAttachment, InterfaceDescription, MessageReceiver
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


class AllPlayer(object):

    def __init__(self, bus, name, session_id):
        self.bus = bus
        self.name = name
        self.session_id = session_id
        self.device_details = {}

        self.CreateInterfaces()

        self.GetAboutData()

    def __repr__(self):
        return self.name

    def CreateInterfaces(self):
        #AddMember(self, message_type, name, inputSig, outSig, argNames, annotation):

        iface = self.bus.CreateInterface("net.allplay.MCU")
        iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "GetCurrentItemUrl", None,  "s", None, 0)
        iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "PlayItem", "ssssxss", None, None, 0)
        iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "AdvanceLoopMode", None, None, None, 0)
        iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "ToggleShuffleMode", None, None, None, 0)
        iface.Activate()

        iface = self.bus.CreateInterface("org.alljoyn.Control.Volume")
        
        iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "AdjustVolumePercent", "d", None, None, 0)
        
        iface.AddProperty('Mute', 'b', InterfaceDescription.ALLJOYN_PROP_ACCESS_RW)

        iface.Activate()


        iface = self.bus.CreateInterface("net.allplay.ZoneManager")
        iface.AddSignal("OnZoneChanged", "sia{si}", "zoneId,timestamp,slaves", 0, None)
        iface.Activate()


        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.ZoneManager")
        proxyBusObject.AddInterface(iface)

        interfaceMember = iface.GetSignal('OnZoneChanged')
 
        print "interfaceMember", interfaceMember.Signature

        # u'GetSignal': (u'alljoyn_interfacedescription_getsignal',
        #                         (u'int', C.c_int),
        #                         ((u'alljoyn_interfacedescription', InterfaceDescriptionHandle),
        #                          (u'const char *', C.c_char_p),
        #                          (u'alljoyn_interfacedescription_member *', POINTER(InterfaceDescriptionMember)))),



        self.bus.RegisterSignalHandler(MessageReceiver.MessageReceiverSignalHandlerFuncType(AllPlayer.OnZoneChanged), interfaceMember, None)
        

#<signal name="OnZoneChanged">
#       <arg name="zoneId" type="s" direction="out"/>
#       <arg name="timestamp" type="i" direction="out"/>
#       <arg name="slaves" type="a{si}" direction="out"/>
#     </signal>


    @staticmethod
    def OnZoneChanged(member, srcpath, message):
        print "OnZoneChanged"
        print member, srcpath, message
        print vars(member)
        args = Message.Message.FromHandle(message).GetArgs()
        print "args", args
        slaves = args[2]

        # Todo Tidy up MsgArg code. Could there be a way to dynamically create types based on the dbus signature ?
        num = C.c_uint()
        entries = MsgArg.MsgArg()
        slaves.Get("a{si}", [C.POINTER(C.c_uint), C.POINTER(MsgArg.MsgArgHandle)], [C.byref(num), C.byref(entries.handle)])
       
        for i in range(num.value):
            key = C.c_char_p()
            value = C.c_int()
            element = entries.ArrayElement(i)
            
            try:
                element.Get("{si}", [C.POINTER(C.c_char_p), C.c_int_p], [C.byref(key), C.byref(value)])
                print key.value, ":", value.value
            except QStatusException as ex:
                pass


        #print [a.GetString() for a in args if a.Signature() == 's']


    def GetMuteStatus(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("org.alljoyn.Control.Volume")
        proxyBusObject.AddInterface(iface)
        param = MsgArg.MsgArg()
        proxyBusObject.GetProperty("org.alljoyn.Control.Volume", "Mute", param)
        return bool(param.GetBool())

    def SetMute(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("org.alljoyn.Control.Volume")
        proxyBusObject.AddInterface(iface)
        param = MsgArg.MsgArg()
        param.SetBool(True)
        proxyBusObject.GetProperty("org.alljoyn.Control.Volume", "Mute", param)

    def CallGetCurrentItemUrl(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.MCU")
        proxyBusObject.AddInterface(iface)
        replyMsg = Message.Message(g_bus)
        proxyBusObject.MethodCall('net.allplay.MCU', "GetCurrentItemUrl", None, 0, replyMsg, 25000, 0)
        return replyMsg.GetArg(0).GetString()

    def ToggleAdvanceLoopMode(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.MCU")
        proxyBusObject.AddInterface(iface)
        proxyBusObject.MethodCallNoReply('net.allplay.MCU', "AdvanceLoopMode", None, 0, 0)


    def ToggleShuffleMode(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.MCU")
        proxyBusObject.AddInterface(iface)
        proxyBusObject.MethodCallNoReply('net.allplay.MCU', "ToggleShuffleMode", None, 0, 0)


    def PlayUrl(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.MCU")      
        proxyBusObject.AddInterface(iface)
  
        inputs = MsgArg.MsgArg.ArrayCreate(7)
        inputs.ArraySet(7, "ssssxss", [C.c_char_p, C.c_char_p, C.c_char_p, C.c_char_p,  C.c_longlong, C.c_char_p, C.c_char_p],
                            ['http://192.168.1.149:8000/test.mp3', 'Dummy', 'Dummy', 'Dummy', 200, 'Dummy', 'Dummy'])
        
        proxyBusObject.MethodCallNoReply('net.allplay.MCU', "PlayItem", inputs, 7, 0)


    def AdjustVolumePercent(self, percent):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, "SERVICE_NAME", SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("org.alljoyn.Control.Volume")      
        proxyBusObject.AddInterface(iface)
  
        percent = min(max(0.0, percent), 100.0)

        param = MsgArg.MsgArg()
        param.SetDouble(percent)

        proxyBusObject.MethodCallNoReply("org.alljoyn.Control.Volume", "AdjustVolumePercent", param, 1, 0)


    def GetAboutData(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, "/About", self.session_id)
        iface = self.bus.GetInterface("org.alljoyn.About")
        proxyBusObject.AddInterface(iface)

        #     <method name="GetAboutData">
        #       <arg name="languageTag" type="s" direction="in"/>
        #       <arg name="aboutData" type="a{sv}" direction="out"/>
        #     </method>

        languageTag = MsgArg.MsgArg()
        languageTag.SetString("en")
        replyMsg = Message.Message(g_bus)
        proxyBusObject.MethodCall('org.alljoyn.About', "GetAboutData", languageTag, 1, replyMsg, 25000, 0)
        arg = replyMsg.GetArg(0)

        # Todo Tidy up MsgArg code. Could there be a way to dynamically create types based on the dbus signature ?
        num = C.c_uint()
        entries = MsgArg.MsgArg()
        arg.Get("a{sv}", [C.POINTER(C.c_uint), C.POINTER(MsgArg.MsgArgHandle)], [C.byref(num), C.byref(entries.handle)])
       
        for i in range(num.value):
            key = C.c_char_p()
            value_string = C.c_char_p()
            element = entries.ArrayElement(i)
            
            try:
                element.Get("{ss}", [C.POINTER(C.c_char_p), C.POINTER(C.c_char_p)], [C.byref(key), C.byref(value_string)])
                self.device_details[key.value] = value_string.value
            except QStatusException as ex:
                pass

         
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

    alljoyn.RouterInit()

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
        #print allplayer.CallGetCurrentItemUrl() #, allplayer.device_details.items()
        print allplayer.device_details.items()
        print allplayer.GetMuteStatus()




    while True:
        time.sleep(0.5)

        #allplayer.AdjustVolumePercent(0.0)
        #allplayer.PlayUrl()
        #allplayer.AdjustVolumePercent(0.0)
        #for i in range(10):
        #    allplayer.AdjustVolumePercent(10.0*i)

	alljoyn.RouterShutdown()	

#AdjustVolumePercent(self, percent)



# <interface name="net.allplay.ZoneManager">
#     <method name="CreateZone">
#       <arg name="slaves" type="as" direction="in"/>
#       <arg name="zoneId" type="s" direction="out"/>
#       <arg name="timestamp" type="i" direction="out"/>
#       <arg name="slaves" type="a{si}" direction="out"/>
#     </method>
#     <signal name="EnabledChanged">
#       <arg name="enabled" type="b" direction="out"/>
#     </signal>
#     <signal name="OnZoneChanged">
#       <arg name="zoneId" type="s" direction="out"/>
#       <arg name="timestamp" type="i" direction="out"/>
#       <arg name="slaves" type="a{si}" direction="out"/>
#     </signal>
#     <signal name="PlayerReady">
#       <arg name="resumeLatency" type="t" direction="out"/>
#     </signal>
#     <method name="SetZoneLead">
#       <arg name="zoneId" type="s" direction="in"/>
#       <arg name="timeServerIp" type="s" direction="in"/>
#       <arg name="timeServerPort" type="q" direction="in"/>
#       <arg name="timestamp" type="i" direction="out"/>
#     </method>
#     <signal name="SlaveOutOfData">
#     </signal>
#     <signal name="SlaveState">
#       <arg name="timestamp" type="i" direction="out"/>
#       <arg name="state" type="s" direction="out"/>
#       <arg name="url" type="s" direction="out"/>
#       <arg name="startTime" type="t" direction="out"/>
#       <arg name="currentPosition" type="t" direction="out"/>
#       <arg name="nextStream" type="s" direction="out"/>
#     </signal>
#     <property name="Enabled" type="b" access="read"/>
#     <property name="Version" type="q" access="read"/>
#   </interface>
