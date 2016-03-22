#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message, BusListener, BusAttachment, InterfaceDescription, MessageReceiver

import time
import sys

import ctypes as C

import threading

lock = threading.Lock()

SERVICE_NAME = "net.allplay.MediaPlayer"
SERVICE_PATH = "/net/allplay/MediaPlayer"
SERVICE_PORT = 1


class AllPlayer(object):

    proxyBusObject = None

    def __init__(self, bus_attachment, bus_name, session_id, device_name, device_id):
        self.bus = bus_attachment
        self.bus_name = bus_name
        self.session_id = session_id
        self.device_name = device_name
        self.device_id = device_id

        if not AllPlayer.proxyBusObject:
            AllPlayer.proxyBusObject = ProxyBusObject.ProxyBusObject(
                self.bus, self.bus_name, SERVICE_PATH, self.session_id)
            AllPlayer.proxyBusObject.IntrospectRemoteObject()

    def __repr__(self):
        return self.device_name + " (" + self.device_id + ")"

    def CreateZone(self, device_ids):
        # We must remove the id that this player is as the speaker does
        # not accept it.
        self.device_ids = [d for d in device_ids if d != self.device_id]

        self.arg = MsgArg.MsgArg()
        size = len(self.device_ids)

        self.array = (C.c_char_p * size)()
        self.array[:] = self.device_ids
        self.arg.Set(
            "as", [C.c_int, C.POINTER(C.c_char_p)], [size, self.array])

        replyMsg = Message.Message(self.bus)
        try:
            AllPlayer.proxyBusObject.MethodCall(
                'net.allplay.ZoneManager', "CreateZone", self.arg, 1, replyMsg, 100000, 0)
        except QStatusException:
            print replyMsg
            raise

    @staticmethod
    def OnReplyMessageCallback(message, context):
        print Message.Message.FromHandle(message)

    def GetMuteStatus(self):
        param = MsgArg.MsgArg()
        self.proxyBusObject.GetProperty(
            "org.alljoyn.Control.Volume", "Mute", param)
        return bool(param.GetBool())

    def SetMute(self):
        param = MsgArg.MsgArg()
        param.SetBool(True)
        self.proxyBusObject.GetProperty(
            "org.alljoyn.Control.Volume", "Mute", param)

    def CallGetCurrentItemUrl(self):
        replyMsg = Message.Message(self.bus)
        self.proxyBusObject.MethodCall(
            'net.allplay.MCU', "GetCurrentItemUrl", None, 0, replyMsg, 25000, 0)
        return replyMsg.GetArg(0).GetString()

    def ToggleAdvanceLoopMode(self):
        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MCU', "AdvanceLoopMode", None, 0, 0)

    def ToggleShuffleMode(self):
        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MCU', "ToggleShuffleMode", None, 0, 0)

    def Next(self):
        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MCU', "Next", None, 0, 0)

    def Pause(self):
        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MCU', "Pause", None, 0, 0)

    def Play(self):
        AllPlayer.proxyBusObject.MethodCallNoReply(
            'net.allplay.MCU', "Play", None, 0, 0)

    def Previous(self):
        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MCU', "Previous", None, 0, 0)

    def Resume(self):
        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MCU', "Resume", None, 0, 0)

    def Stop(self):
        AllPlayer.proxyBusObject.MethodCallNoReply(
            'net.allplay.MediaPlayer', "Stop", None, 0, 0)

    def SetPosition(self, position):
        param = MsgArg.MsgArg()
        param.SetInt64(position)
        self.proxyBusObject.MethodCallNoReply(
            "net.allplay.MediaPlayer", "SetPosition", param, 1, 0)

    def PlayUrl(self, uri):
        inputs = MsgArg.MsgArg.ArrayCreate(7)
        inputs.ArraySet(7, "ssssxss",
                        [C.c_char_p, C.c_char_p, C.c_char_p, C.c_char_p, C.c_longlong, C.c_char_p, C.c_char_p],
                        [uri, 'Dummy', 'Dummy', 'Dummy', 200, 'Dummy', 'Dummy'])
        AllPlayer.proxyBusObject.MethodCallNoReply(
            'net.allplay.MCU', "PlayItem", inputs, 7, 0)

    def AdjustVolumePercent(self, percent):
        percent = min(max(0.0, percent), 100.0)
        param = MsgArg.MsgArg()
        param.SetDouble(percent)
        AllPlayer.proxyBusObject.MethodCallNoReply(
            "org.alljoyn.Control.Volume", "AdjustVolumePercent", param, 1, 0)


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
        self.devices = {}

    def OnAboutListenerCallBack(self, context, busName, version, port, objectDescriptionArg, aboutDataArg):

        # alljoyn_busattachment_joinsession might block for a while, so allow
        # other callbacks to run in parallel with it
        self.bus_attachment.EnableConcurrentCallBacks()

        # We seem to need this. Not sure why. EnableConcurrentCallBacks cause
        # weird effects
        # Guess the list and session listener need to be thread safe.
        # Note we need mySessionListener constructed after
        # EnableConcurrentCallBacks
        lock.acquire()

        aboutData = AboutData.AboutData(aboutDataArg, language="en")

        opts = Session.SessionOpts(Session.ALLJOYN_TRAFFIC_TYPE_MESSAGES,
                                   False,
                                   Session.ALLJOYN_PROXIMITY_ANY,
                                   TransportMask.ALLJOYN_TRANSPORT_ANY)

        if not MyAboutListener.mySessionListener:

            MyAboutListener.mySessionListener = MySessionListener(
                self.bus_attachment)

        # Bus name of attachment that is hosting the session to be joined.
        session_id = self.bus_attachment.JoinSession(
            busName, SERVICE_PORT, MyAboutListener.mySessionListener, opts)

        full_device_id = "net.allplay.MediaPlayer.i" + aboutData.GetDeviceId()
        self.devices[full_device_id] = {'busname': busName,
                                        'session_id': session_id,
                                        'name': aboutData.GetDeviceName(),
                                        'id': full_device_id}
        lock.release()


class AllPlayController(object):

    def __init__(self):
        super(AllPlayController, self).__init__()
        self.alljoyn = AllJoyn()

        self.g_bus = BusAttachment.BusAttachment("AllPlayerApp", True)
        self.g_bus.Start()

        try:
            self.g_bus.Connect(None)
        except QStatusException:
            print "Have you got the daemon running ?"
            sys.exit(1)

        self.aboutListener = MyAboutListener(self.g_bus)
        self.g_bus.RegisterAboutListener(self.aboutListener)
        self.g_bus.WhoImplementsInterfaces([SERVICE_NAME])

        # Wait for join session to complete
        t = 0
        while t < 10.0:
            if len(self.aboutListener.devices) >= 3:
                break
            time.sleep(0.1)
            t += 0.1

        allplayers = []
        for p in self.aboutListener.devices.values():
            print "session_id", MyAboutListener.session_id
            allplayers.append(AllPlayer(self.g_bus, p['busname'], p['session_id'], p['name'], p['id']))

        player = allplayers[0]
        print "using: ", player.device_name, "speaker", player.device_id
        player.Stop()

    def __del__(self):
        print "Shutting Down"
        self.g_bus.Stop()
        self.g_bus.Join()

    def GetPlayers(self):
        return self.aboutListener.devices.values()

    def GetAllPlayer(self):
        first = self.aboutListener.devices.values()[0]
        return AllPlayer(self.g_bus, first['busname'], first['session_id'], first['name'], first['id'])
