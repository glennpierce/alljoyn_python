#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message, BusListener, BusAttachment, InterfaceDescription, MessageReceiver
import signal
import time
import sys

import ctypes as C

import threading

lock = threading.Lock()

#SERVICE_NAME = "net.allplay.MediaPlayer.i51e73778-31f3-4dc8-a33d-9237295005ae.rv2HiHStz"
#SERVICE_NAME = "net.allplay.MediaPlayer.i4a360b3d-95c5-4b67-9728-c2f74b875625.rX6nDdAbA"
#SERVICE_NAME = "net.allplay.MediaPlayer.i9f5cf275-d33a-4ae6-8c57-c39d0487be3f.rUIe75rBf"
SERVICE_NAME = "net.allplay.MediaPlayer"
SERVICE_PATH = "/net/allplay/MediaPlayer";
SERVICE_PORT = 1


# Email feed back from Daniel Tai AllPlay Click Wireless Home Audio SDK mailinglist
# Since you are controlling speakers, you do not need to implement SetZoneLead,
# this is for player only, but you are on the right track to implement
# CreateZone.

# You are half right on putting the device id for slaves, and what you need to
# do is to put in the format of net.allplay.MediaPlayer.i<deviceID>.  Sorry
# for the lack of doc here.

# Do you need to keep in mind of CreateZone's timestamp, as you don't need to
# parse the output slaves if the timetamp is older than the latest.  You will
# get a signal onZoneChanged from lead player session, which contains the same
# data.  This is sent to all sessions connected to the lead player.  So if
# you have another instance of an app somewhere, itself can also update
# according to the data.    

class AllPlayer(object):

    interfaces_created = False

    def __init__(self, bus_attachment, bus_name, session_id, device_name, device_id):
        self.bus = bus_attachment
        self.session_id = session_id
        self.bus_name = bus_name

        print "AllPlayer session_id", self.session_id, "bus_name", self.bus_name

        self.device_name = device_name
        self.device_id = device_id
        self.full_device_id = "net.allplay.MediaPlayer.i" + self.device_id

        self.CreateInterfaces()

    def __repr__(self):
        return self.device_name + " (" + self.device_id + ")"

    def CreateInterfaces(self):

        if AllPlayer.interfaces_created:
            return

        print "CreateInterfaces", self.bus, self.bus_name
        print self.session_id
        self.proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, self.bus_name, SERVICE_PATH, self.session_id)
        print self.proxyBusObject.IntrospectRemoteObject()

        #AddMember(self, message_type, name, inputSig, outSig, argNames, annotation):

        # iface = self.bus.CreateInterface("net.allplay.MCU")
        # iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "GetCurrentItemUrl", None,  "s", None, 0)
        # iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "PlayItem", "ssssxss", None, None, 0)
        # iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "AdvanceLoopMode", None, None, None, 0)
        # iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "ToggleShuffleMode", None, None, None, 0)
        # iface.Activate()

        # iface = self.bus.CreateInterface("net.allplay.MediaPlayer")
        # iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "Stop", None,  None, None, 0)
        # iface.Activate()

        # iface = self.bus.CreateInterface("org.alljoyn.Control.Volume")
        # iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "AdjustVolumePercent", "d", None, None, 0)
        # iface.AddProperty('Mute', 'b', InterfaceDescription.ALLJOYN_PROP_ACCESS_RW)
        # iface.Activate()

        # iface = self.bus.CreateInterface("net.allplay.ZoneManager")
        # iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "CreateZone", "as", "sia{si}", "slaves,zoneId,timestamp,slaves", 0)
        # iface.AddSignal("OnZoneChanged", "sia{si}", "zoneId,timestamp,slaves", 0, None)
        # iface.Activate()

        # proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        # iface = self.bus.GetInterface("net.allplay.ZoneManager")
        # proxyBusObject.AddInterface(iface)

        # interfaceMember = iface.GetSignal('OnZoneChanged')

        # self.bus.RegisterSignalHandler(MessageReceiver.MessageReceiverSignalHandlerFuncType(AllPlayer.OnZoneChanged), interfaceMember, None)
        
        AllPlayer.interfaces_created = True

    def CreateZone(self, device_ids):
        #     <method name="CreateZone">
        #       <arg name="slaves" type="as" direction="in"/>
        #       <arg name="zoneId" type="s" direction="out"/>
        #       <arg name="timestamp" type="i" direction="out"/>
        #       <arg name="slaves" type="a{si}" direction="out"/>
        #     </method>

        # We must remove the dice id that this player is as the speaker does not accept it.
        self.device_ids = [d for d in device_ids if d != self.full_device_id]
        #device_ids = [d for d in device_ids if d != self.device_id]

        #proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        #proxyBusObject.IntrospectRemoteObject()
        # u'IntrospectRemoteObject': (u'alljoyn_proxybusobject_introspectremoteobject',
        #                                      (u'QStatus', C.c_uint),
        #                                      ((u'alljoyn_proxybusobject', ProxyBusHandle),)),

        #iface = self.bus.GetInterface("net.allplay.ZoneManager")      
        #proxyBusObject.AddInterface(iface)
  
        self.arg = MsgArg.MsgArg()
        size = len(self.device_ids)

        self.array = (C.c_char_p * size)()
        self.array[:] = self.device_ids
        self.arg.Set("as", [C.c_int, C.POINTER(C.c_char_p)], [size, self.array])
        
        print "device_ids", self.device_ids

        replyMsg = Message.Message(self.bus)
        try:
            self.proxyBusObject.MethodCall('net.allplay.ZoneManager', "CreateZone", self.arg, 1, replyMsg, 100000, 0)
            # callback = MessageReceiver.MessageReceiverReplyHandlerFuncType(AllPlayer.OnReplyMessageCallback)
            # proxyBusObject.MethodCallAsync('net.allplay.ZoneManager', "CreateZone", callback, self.arg, 1, None, 55000, 0)
 
        except QStatusException as ex:
            print replyMsg
            print replyMsg.Description()
            print replyMsg.GetErrorName()
            raise

        

    @staticmethod
    def OnReplyMessageCallback(message, context):
        print "reply message", message, context
        print Message.Message.FromHandle(message)

    @staticmethod
    def OnZoneChanged(member, srcpath, message):
        #     <signal name="OnZoneChanged">
        #       <arg name="zoneId" type="s" direction="out"/>
        #       <arg name="timestamp" type="i" direction="out"/>
        #       <arg name="slaves" type="a{si}" direction="out"/>
        #     </signal>

        print "OnZoneChanged"
        print member, srcpath, message
        print vars(member)
        message = Message.Message.FromHandle(message)
        print "message", message.GetSignature()

        slaves = message.GetArg(2)

        print "slaves", slaves.Signature()

        # Todo Tidy up MsgArg code. Could there be a way to dynamically create types based on the dbus signature ?
        num = C.c_uint()
        entries = MsgArg.MsgArg()

        slaves.Get("a{si}", [C.POINTER(C.c_uint), C.POINTER(MsgArg.MsgArgHandle)], [C.byref(num), C.byref(entries.handle)])
       
        for i in range(num.value):
            print "i", i
            key = C.c_char_p()
            value = C.c_int()
            element = entries.ArrayElement(i)
            
            element.Get("{si}", [C.POINTER(C.c_char_p), C.c_int_p], [C.byref(key), C.byref(value)])
            print key.value, ":", value.value

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

    def Next(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.MediaPlayer")
        proxyBusObject.AddInterface(iface)
        proxyBusObject.MethodCallNoReply('net.allplay.MCU', "Next", None, 0, 0)

    def Pause(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.MediaPlayer")
        proxyBusObject.AddInterface(iface)
        proxyBusObject.MethodCallNoReply('net.allplay.MCU', "Pause", None, 0, 0)

    def Play(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.MediaPlayer")
        proxyBusObject.AddInterface(iface)
        proxyBusObject.MethodCallNoReply('net.allplay.MCU', "Play", None, 0, 0)

    def Previous(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.MediaPlayer")
        proxyBusObject.AddInterface(iface)
        proxyBusObject.MethodCallNoReply('net.allplay.MCU', "Previous", None, 0, 0)

    def Resume(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.MediaPlayer")
        proxyBusObject.AddInterface(iface)
        proxyBusObject.MethodCallNoReply('net.allplay.MCU', "Resume", None, 0, 0)


    def Stop(self):
        #proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        #iface = self.bus.GetInterface("net.allplay.MediaPlayer")
        #proxyBusObject.AddInterface(iface)
        self.proxyBusObject.MethodCallNoReply('net.allplay.MediaPlayer', "Stop", None, 0, 0)
        # try:
        #     replyMsg = Message.Message(self.bus)
        #     self.proxyBusObject.MethodCall('net.allplay.MediaPlayer', "Stop", None, 0, replyMsg, 100000, 0)
        # except QStatusException as ex:
        #     print replyMsg

    def SetPosition(self, position):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, "SERVICE_NAME", SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.MediaPlayer")      
        proxyBusObject.AddInterface(iface)
        param = MsgArg.MsgArg()
        param.SetInt64(position)
        proxyBusObject.MethodCallNoReply("net.allplay.MediaPlayer", "SetPosition", param, 1, 0)

    def PlayUrl(self):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("net.allplay.MCU")      
        proxyBusObject.AddInterface(iface)
  
        inputs = MsgArg.MsgArg.ArrayCreate(7)
        inputs.ArraySet(7, "ssssxss", [C.c_char_p, C.c_char_p, C.c_char_p, C.c_char_p,  C.c_longlong, C.c_char_p, C.c_char_p],
                            ['http://192.168.1.149:8000/test.mp3', 'Dummy', 'Dummy', 'Dummy', 200, 'Dummy', 'Dummy'])
        
        proxyBusObject.MethodCallNoReply('net.allplay.MCU', "PlayItem", inputs, 7, 0)

    def AdjustVolumePercent(self, percent):
        proxyBusObject = ProxyBusObject.ProxyBusObject(self.bus, SERVICE_NAME, SERVICE_PATH, self.session_id)
        iface = self.bus.GetInterface("org.alljoyn.Control.Volume")      
        proxyBusObject.AddInterface(iface)
  
        percent = min(max(0.0, percent), 100.0)

        param = MsgArg.MsgArg()
        param.SetDouble(percent)

        proxyBusObject.MethodCallNoReply("org.alljoyn.Control.Volume", "AdjustVolumePercent", param, 1, 0)


class MySessionListener(SessionListener.SessionListener):
    def __init__(self, callback_data=None):
        super(MySessionListener, self).__init__()

    def OnSessionLostCallBack(self, context, sessionId, reason):
        print "SessionLost sessionId = %u, Reason = %s" % (sessionId, reason)


class MyAboutListener(AboutListener.AboutListener):

    mySessionListener = None
    session_id = None

    def __init__(self, bus_attachment, context=None):
        super(MyAboutListener, self).__init__(context=context)
        self.bus_attachment = bus_attachment
        self.devices = []

    def OnAboutListenerCallBack(self, context, busName, version, port, objectDescriptionArg, aboutDataArg): 

        #

        objectDescription = AboutObjectDescription.AboutObjectDescription(objectDescriptionArg)
        aboutData = AboutData.AboutData(aboutDataArg, language="en")
 
        opts = Session.SessionOpts(Session.ALLJOYN_TRAFFIC_TYPE_MESSAGES,
                                        False,
                                        Session.ALLJOYN_PROXIMITY_ANY,
                                        TransportMask.ALLJOYN_TRANSPORT_ANY)
        
        # alljoyn_busattachment_joinsession might block for a while, so allow other callbacks to run in parallel with it 
        self.bus_attachment.EnableConcurrentCallBacks()

        lock.acquire()  # We seem to need this. Not sure why. EnableConcurrentCallBacks cause weird effects
                        # Guess the list and session listener need to be thread safe. 
                        # Note we need mySessionListener constructed after EnableConcurrentCallBacks

        if not MyAboutListener.mySessionListener:
            
            MyAboutListener.mySessionListener = MySessionListener(self.bus_attachment)
            # Bus name of attachment that is hosting the session to be joined.
            MyAboutListener.session_id = self.bus_attachment.JoinSession(busName, SERVICE_PORT, MyAboutListener.mySessionListener, opts)
            print "Join Session Complete", MyAboutListener.session_id
        
        self.devices.append((busName, aboutData.GetDeviceName(), aboutData.GetDeviceId()))
        lock.release()
        


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
    
    aboutListener = MyAboutListener(g_bus)
    g_bus.RegisterAboutListener(aboutListener)
    g_bus.WhoImplementsInterfaces([SERVICE_NAME])

    # Wait for join session to complete 
    t=0
    while t < 10.0:
        if len(aboutListener.devices) >= 3:
            break
        time.sleep(0.1)
        t+=0.1   

    allplayers = []
    for bus_name, device_name, device_id in aboutListener.devices:
        allplayers.append(AllPlayer(g_bus, bus_name, MyAboutListener.session_id, device_name, device_id))

    player = allplayers[0]
    print "using: ", player.device_name, "speaker", player.device_id

    player.Stop()
    #print "Mute:", player.GetMuteStatus()
    #player.AdjustVolumePercent(20.0)

    player.CreateZone([p.full_device_id for p in allplayers])
    #player.PlayUrl()

    g_bus.Stop()
    g_bus.Join()

    #print allplayer.GetMuteStatus()

    #while True:
    #    time.sleep(0.5)

        #allplayer.AdjustVolumePercent(0.0)
        #allplayer.PlayUrl()
        #allplayer.AdjustVolumePercent(0.0)
        #for i in range(10):
        #    allplayer.AdjustVolumePercent(10.0*i)


#AdjustVolumePercent(self, percent)

