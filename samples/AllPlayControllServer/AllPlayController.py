#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message, BusListener, BusAttachment, InterfaceDescription, MessageReceiver

import logging
import time
import sys

import ctypes as C

import threading

lock = threading.Lock()

SERVICE_NAME = "net.allplay.MediaPlayer"
SERVICE_PATH = "/net/allplay/MediaPlayer"
SERVICE_PORT = 1


class AllPlayer(object):

    def __init__(self, bus_attachment, bus_name, session_id, device_name, device_id):
        self.bus = bus_attachment
        self.bus_name = bus_name
        self.session_id = session_id
        self.device_name = device_name
        self.device_id = device_id
        self.paused = False

        self.proxyBusObject = ProxyBusObject.ProxyBusObject(
            self.bus, self.bus_name, SERVICE_PATH, self.session_id)
        self.proxyBusObject.IntrospectRemoteObject()

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
            self.proxyBusObject.MethodCall(
                'net.allplay.ZoneManager', "CreateZone", self.arg, 1, replyMsg, 100000, 0)
        except QStatusException:
            print replyMsg
            raise

    @staticmethod
    def OnReplyMessageCallback(message, context):
        print Message.Message.FromHandle(message)

    def GetMute(self):
        param = MsgArg.MsgArg()
        self.proxyBusObject.GetProperty(
            "org.alljoyn.Control.Volume", "Mute", param)
        return bool(param.GetBool())

    def SetMute(self):
        param = MsgArg.MsgArg()
        param.SetBool(True)
        self.proxyBusObject.SetProperty(
            "org.alljoyn.Control.Volume", "Mute", param)

    def GetVolume(self):
        param = MsgArg.MsgArg()
        self.proxyBusObject.GetProperty(
            "org.alljoyn.Control.Volume", "Volume", param)
        return param.GetInt16()

    def SetVolume(self, volume):
        param = MsgArg.MsgArg()
        param.SetInt16(volume)
        self.proxyBusObject.SetProperty(
            "org.alljoyn.Control.Volume", "Volume", param)
        logging.info("setting volume for device %s (%s) to %s", self.device_name, self.device_id, volume)

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
            'net.allplay.MediaPlayer', "Next", None, 0, 0)

    def Pause(self):
        self.paused = True
        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MediaPlayer', "Pause", None, 0, 0)
        logging.info("pausing for device %s (%s)", self.device_name, self.device_id)

    def Play(self):
        if self.paused:
            self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MediaPlayer', "Resume", None, 0, 0)
            self.paused = False
            logging.info("resuming for device %s (%s)", self.device_name, self.device_id)

        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MediaPlayer', "Play", None, 0, 0)

    def Previous(self):
        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MediaPlayer', "Previous", None, 0, 0)

    def Resume(self):
        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MediaPlayer', "Resume", None, 0, 0)

    def Stop(self):
        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MediaPlayer', "Stop", None, 0, 0)
        logging.info("stopping")

    def SetPosition(self, position):
        param = MsgArg.MsgArg()
        param.SetInt64(position)
        self.proxyBusObject.MethodCallNoReply(
            "net.allplay.MediaPlayer", "SetPosition", param, 1, 0)

    def PlayUrl(self, uri):
        inputs = MsgArg.MsgArg.ArrayCreate(7)
        inputs.ArraySet(7, "ssssxss",
                        [C.c_char_p, C.c_char_p, C.c_char_p, C.c_char_p,
                            C.c_longlong, C.c_char_p, C.c_char_p],
                        [uri, 'Dummy', 'Dummy', 'Dummy', 200, 'Dummy', 'Dummy'])
        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MCU', "PlayItem", inputs, 7, 0)
        logging.info("playing: %s", uri)

    def AdjustVolumePercent(self, percent):
        percent = min(max(0.0, percent), 100.0)
        param = MsgArg.MsgArg()
        param.SetDouble(percent)
        self.proxyBusObject.MethodCallNoReply(
            "org.alljoyn.Control.Volume", "AdjustVolumePercent", param, 1, 0)
        logging.info("adjust volume for %s (%s) to %s", self.device_name, self.device_id, percent)

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
        self.player = None

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

        self.allplayers = {}
        for p in self.aboutListener.devices.values():
            print "session_id", MyAboutListener.session_id
            self.allplayers[p['id']] = AllPlayer(self.g_bus, p['busname'], p['session_id'], p['name'], p['id'])

    def __del__(self):
        print "Shutting Down"
        self.g_bus.Stop()
        self.g_bus.Join()

    def CreateZone(self, device_ids):
        # Find the player with the first device _id
        if not device_ids:
            return
        devices = [p for p in self.allplayers.values() if p.device_id == device_ids[0]]
        self.player = devices[0]
        print "using: ", self.player.device_name, "speaker", self.player.device_id
        self.player.CreateZone(device_ids)

    def GetVolume(self, device_id):
        player = self.allplayers[device_id]
        return player.GetVolume()

    def SetVolume(self, device_id, volume):
        player = self.allplayers[device_id]
        return player.SetVolume(volume)

    # def SetVolume(self, device_id, volume):
    #     player = self.allplayers[device_id]
    #     return player.AdjustVolumePercent(volume)

    def GetPlayers(self):
        players = []
        for p in self.allplayers.values():
            players.append({'id': p.device_id,
                            'name': p.device_name,
                            'volume': p.GetVolume()})
        return players

    def GetPlayer(self):
        return self.player
