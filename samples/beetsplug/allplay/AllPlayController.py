#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message, BusListener, BusAttachment, InterfaceDescription, MessageReceiver, MsgArgHandle

import logging
import time
import sys

import ctypes as C

import threading

from beets import config

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

        self.proxyBusObject = ProxyBusObject.ProxyBusObject(
            self.bus, self.bus_name, SERVICE_PATH, self.session_id)
        self.proxyBusObject.IntrospectRemoteObject()

        iface = self.proxyBusObject.GetInterface('net.allplay.ZoneManager')
        success, zoneChangedSignal = iface.GetSignal('OnZoneChanged')
        self.bus.RegisterSignalHandler(MessageReceiver.MessageReceiverSignalHandlerFuncType(
             AllPlayer.OnZoneChanged), zoneChangedSignal, None)

        iface = self.proxyBusObject.GetInterface('net.allplay.MediaPlayer')

        # success, playStateChangedSignal = iface.GetSignal('PlayStateChanged')
        # self.playStateChangedFuncPtr = MessageReceiver.MessageReceiverSignalHandlerFuncType(self._OnPlayStateChanged())
        # self.bus.RegisterSignalHandler(self.playStateChangedFuncPtr, playStateChangedSignal, None)

        # Not present. Think it may be internal
        success, endOfPlaybackSignal = iface.GetSignal('EndOfPlayback')
        self.endOfPlaybackFuncPtr = MessageReceiver.MessageReceiverSignalHandlerFuncType(self._OnEndOfPlayback())
        self.bus.RegisterSignalHandler(self.endOfPlaybackFuncPtr, endOfPlaybackSignal, None)

        # success, loopModeChangedSignal = iface.GetSignal('LoopModeChanged')
        # self.loopModeChangedFuncPtr = MessageReceiver.MessageReceiverSignalHandlerFuncType(AllPlayer.OnLoopModeChanged)
        # self.bus.RegisterSignalHandler(self.loopModeChangedFuncPtr, loopModeChangedSignal, None)

        # success, shuffleModeChangedSignal = iface.GetSignal('ShuffleModeChanged')
        # self. shuffleModeChangeFuncPtr = MessageReceiver.MessageReceiverSignalHandlerFuncType(AllPlayer.OnShuffleModeChanged)
        # self.bus.RegisterSignalHandler(self. shuffleModeChangeFuncPtr, shuffleModeChangedSignal, None)

    def __repr__(self):
        return self.device_name + " (" + self.device_id + ")"

    def CreateZone(self, device_ids):
        # We must remove the id that this player is as the speaker does
        # not accept it.
        self.device_ids = [d for d in device_ids if d != self.device_id]

        self.arg = MsgArg.MsgArg()
        size = len(self.device_ids)

        self.array = (C.c_char_p * size)()

        print "CreateZone", self.device_ids

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

    @staticmethod
    def OnLoopModeChanged(member, srcpath, message):
        """
        <signal name="LoopModeChanged">
         <arg name="loopMode" type="s" direction="out"/>
        </signal>
        """
        message = Message.Message.FromHandle(message)

    @staticmethod
    def OnShuffleModeChanged(member, srcpath, message):
        """
        <signal name="ShuffleModeChanged">
          <arg name="shuffleMode" type="s" direction="out"/>
        </signal>
        """
        message = Message.Message.FromHandle(message)

    @staticmethod
    def OnZoneChanged(member, srcpath, message):
        """
        <signal name="OnZoneChanged">
          <arg name="zoneId" type="s" direction="out"/>
          <arg name="timestamp" type="i" direction="out"/>
          <arg name="slaves" type="a{si}" direction="out"/>
        </signal>
        """
        print "OnZoneChanged"
        print member, srcpath, message
        args = Message.Message.FromHandle(message).GetArgs()
        slaves = args[2]

        # Todo Tidy up MsgArg code. Could there be a way to dynamically create
        # types based on the dbus signature ?
        num = C.c_uint()
        entries = MsgArg.MsgArg()
        slaves.Get("a{si}", [C.POINTER(C.c_uint), C.POINTER(MsgArg.MsgArgHandle)], [
                   C.byref(num), C.byref(entries.handle)])

        for i in range(num.value):
            key = C.c_char_p()
            value = C.c_int()
            element = entries.ArrayElement(i)

            try:
                element.Get(
                    "{si}", [C.POINTER(C.c_char_p), C.c_int_p], [C.byref(key), C.byref(value)])
                print key.value, ":", value.value
            except QStatusException as ex:
                print ex


    def _OnEndOfPlayback(self):
        def func(member, srcpath, message):
            self.OnEndOfPlayback(member, srcpath, message, self.device_id)
        return MessageReceiver.MessageReceiverSignalHandlerFuncType(func)

    def OnEndOfPlayback(self, member, srcpath, message, device_id):
        pass

    def _OnPlayStateChanged(self):
        def func(member, srcpath, message):
            self.OnPlayStateChanged(member, srcpath, message)
        return MessageReceiver.MessageReceiverSignalHandlerFuncType(func)

    def OnPlayStateChanged(self, member, srcpath, message):
        """
        (sxuuuiia(ssssxsssa{ss}a{sv}v))
        """
        message = Message.Message.FromHandle(message)
        arg =  message.GetArg(0)

        play_state = C.c_char_p()
        position = C.c_int64()
        current_sample_rate = C.c_uint32()
        audio_channels = C.c_uint32()
        bits_per_sample = C.c_uint32()
        index_current_item = C.c_int32()
        index_next_item = C.c_int32()

        num = C.c_size_t()
        entries = MsgArg.MsgArg()

        arg.Get("(sxuuuii*)",
                  [C.POINTER(C.c_char_p),
                   C.POINTER(C.c_int64),
                   C.POINTER(C.c_uint32),
                   C.POINTER(C.c_uint32),
                   C.POINTER(C.c_uint32),
                   C.POINTER(C.c_int32),
                   C.POINTER(C.c_int32),
                   C.POINTER(C.c_size_t),
                   C.POINTER(MsgArgHandle)
                   ],
                  [C.byref(play_state),
                   C.byref(position),
                   C.byref(current_sample_rate),
                   C.byref(audio_channels),
                   C.byref(bits_per_sample),
                   C.byref(index_current_item),
                   C.byref(index_next_item),
                   C.byref(num),
                   C.byref(entries.handle)])

        print  play_state.value

    def SetLoopMode(self, value):
        """
        <property name="LoopMode" type="s" access="readwrite"/>
        ONE, ALL, NONE
        """
        param = MsgArg.MsgArg()
        param.SetString(value)
        self.proxyBusObject.SetProperty("net.allplay.MediaPlayer", "LoopMode", param)

    def GetLoopMode(self):
        param = MsgArg.MsgArg()
        self.proxyBusObject.GetProperty("net.allplay.MediaPlayer", "LoopMode", param)
        return param.GetString()

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
        logging.info("setting volume for device %s (%s) to %s",
                     self.device_name, self.device_id, volume)

    def UpdatePlaylist(self, tracks):
        number_of_tracks = len(tracks)

        arg = MsgArg.MsgArg()

        entries = MsgArg.MsgArg.ArrayCreate(number_of_tracks)

        for i, track in enumerate(tracks):

            url = C.c_char_p(track['url'])
            title = C.c_char_p(track.get('title', 'None'))
            artist = C.c_char_p(track.get('artist', 'None'))
            thumbnail_url = C.c_char_p(track.get('thumbnail_url', 'None'))
            duration = C.c_int64(track.get('duration', 'None',))
            media_type = C.c_char_p(track.get('media_type', 'None'))
            album = C.c_char_p(track.get('album', 'None'))
            genre = C.c_char_p(track.get('genre', 'None'))

            num = C.c_size_t(0)
            #  a{ss}: other data
            other_data  = MsgArg.MsgArg.ArrayCreate(0)

            # a{sv}: medium description (codec, container, protocol,
            medium_data =  MsgArg.MsgArg.ArrayCreate(0)

            user_data = MsgArg.MsgArg()

            element = entries.ArrayElement(i)

            # (ssssxsssa{ss}a{sv}v)
            element.Set(
                "(ssssxsssa{ss}a{sv}v)", [C.POINTER(C.c_char_p),
                                          C.POINTER(C.c_char_p),
                                          C.POINTER(C.c_char_p),
                                          C.POINTER(C.c_char_p),
                                          C.POINTER(C.c_int64),
                                          C.POINTER(C.c_char_p),
                                          C.POINTER(C.c_char_p),
                                          C.POINTER(C.c_char_p),
                                          C.POINTER(C.c_size_t),
                                          C.POINTER(MsgArgHandle),
                                          C.POINTER(C.c_size_t),
                                          C.POINTER(MsgArgHandle),
                                          C.POINTER(MsgArgHandle)],
                [C.byref(url),
                 C.byref(title),
                 C.byref(artist),
                 C.byref(thumbnail_url),
                 C.byref(duration),
                 C.byref(mediaType),
                 C.byref(album),
                 C.byref(genre),
                 C.byref(num),
                 C.byref(other_data.handle),
                 C.byref(num),
                 C.byref(medium_data.handle),
                 C.byref(user_data.handle)])

        arg.Set("a(ssssxsssa{ss}a{sv}v)", number_of_tracks, entries)


    def GetPlaylist(self):
        """
        <method name="GetPlaylist">
        <arg name="items" type="a(ssssxsssa{ss}a{sv}v)" direction="out"/>
        <!-- see UpdatePlaylist -->
        <arg name="controllerType" type="s" direction="out"/>
        <arg name="playlistUserData" type="s" direction="out"/>
        </method>
        """
        replyMsg = Message.Message(self.bus)

        try:
            self.proxyBusObject.MethodCall(
                'net.allplay.MediaPlayer', "GetPlaylist", None, 0, replyMsg, 25000, 0)
        except QStatusException:
            return []

        arg = replyMsg.GetArg(0)

        num = C.c_size_t()
        entries = MsgArg.MsgArg()
        arg.Get("a(ssssxsssa{ss}a{sv}v)", [C.POINTER(C.c_size_t), C.POINTER(MsgArgHandle)], [
            C.byref(num), C.byref(entries.handle)])

        items = []

        for i in range(num.value):
            url = C.c_char_p()
            title = C.c_char_p()
            artist = C.c_char_p()
            thumbnail_url = C.c_char_p()
            duration = C.c_int64()
            mediaType = C.c_char_p()
            album = C.c_char_p()
            genre = C.c_char_p()

            #  a{ss}: other data
            other_data_num = C.c_size_t()
            other_data = MsgArg.MsgArg()

            # a{sv}: medium description (codec, container, protocol,
            medium_data_num = C.c_size_t()
            medium_data = MsgArg.MsgArg()

            user_data = MsgArg.MsgArg()

            element = entries.ArrayElement(i)

            try:
                # (ssssxsssa{ss}a{sv}v)
                element.Get(
                    "(ssssxsssa{ss}a{sv}v)", [C.POINTER(C.c_char_p),
                                              C.POINTER(C.c_char_p),
                                              C.POINTER(C.c_char_p),
                                              C.POINTER(C.c_char_p),
                                              C.POINTER(C.c_int64),
                                              C.POINTER(C.c_char_p),
                                              C.POINTER(C.c_char_p),
                                              C.POINTER(C.c_char_p),
                                              C.POINTER(C.c_size_t),
                                              C.POINTER(MsgArgHandle),
                                              C.POINTER(C.c_size_t),
                                              C.POINTER(MsgArgHandle),
                                              C.POINTER(MsgArgHandle)],
                    [C.byref(url),
                     C.byref(title),
                     C.byref(artist),
                     C.byref(thumbnail_url),
                     C.byref(duration),
                     C.byref(mediaType),
                     C.byref(album),
                     C.byref(genre),
                     C.byref(other_data_num),
                     C.byref(other_data.handle),
                     C.byref(medium_data_num),
                     C.byref(medium_data.handle),
                     C.byref(user_data.handle)])

                items.append({'url': url.value,
                                        'title': title.value,
                                        'artist': artist.value,
                                        'thumbnail_url': thumbnail_url.value,
                                        'duration': duration.value,
                                        'media_type': mediaType.value,
                                        'album': album.value,
                                        'genre': genre.value})

            except QStatusException, ex:
                print ex

        return items

    def GetPlayingState(self):
        param = MsgArg.MsgArg()
        self.proxyBusObject.GetProperty(
            "net.allplay.MediaPlayer", "PlayState", param)

        play_state = C.c_char_p()
        position = C.c_int64()
        current_sample_rate = C.c_uint32()
        audio_channels = C.c_uint32()
        bits_per_sample = C.c_uint32()
        index_current_item = C.c_int32()
        index_next_item = C.c_int32()

        num = C.c_size_t()
        entries = MsgArg.MsgArg()

        # (sxuuuiia(ssssxsssa{ss}a{sv}v))
        param.Get("(sxuuuii*)",
                  [C.POINTER(C.c_char_p),
                   C.POINTER(C.c_int64),
                   C.POINTER(C.c_uint32),
                   C.POINTER(C.c_uint32),
                   C.POINTER(C.c_uint32),
                   C.POINTER(C.c_int32),
                   C.POINTER(C.c_int32),
                   C.POINTER(C.c_size_t),
                   C.POINTER(MsgArgHandle)
                   ],
                  [C.byref(play_state),
                   C.byref(position),
                   C.byref(current_sample_rate),
                   C.byref(audio_channels),
                   C.byref(bits_per_sample),
                   C.byref(index_current_item),
                   C.byref(index_next_item),
                   C.byref(num),
                   C.byref(entries.handle)])

        return play_state.value, position.value

    def GetCurrentItemUrl(self):
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
        self.proxyBusObject.MethodCallNoReply(
            'net.allplay.MediaPlayer', "Pause", None, 0, 0)
        logging.info(
            "pausing for device %s (%s)", self.device_name, self.device_id)

    def Play(self):
        """
        Start playing the item at the index
        at the specified start position. If
        Play() is called while the playlist
        is playing, it will restart playback
        from the start of the current track.

        itemIndex yes i N/A in Index in the playlist of the item to play.

        startPositionMsecs yes x N/A in Start position in milliseconds.

        pauseStateOnly yes Indicates whether to start streaming (false) or just pause at
        the specific position (true). This is used for transferring of playlists.
        """

	state = self.GetPlayingState()

        if state.lower() == "paused":
            self.proxyBusObject.MethodCallNoReply(
                'net.allplay.MediaPlayer', "Resume", None, 0, 0)
            logging.info(
                "resuming for device %s (%s)", self.device_name, self.device_id)
	    return

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
        print "playing: %s" % (uri,)

    def AdjustVolumePercent(self, percent):
        """
        Not interested in this at this time. Left for future
        The change has floating point values between -1.0 and 1.0 to represent volume
        changes between -100% to 100%.
        A positive value (respectively negative), will increase (respectively decrease) the volume
        by the percentage of the "remaining range" towards the maximum (respectively
        minimum) value, i.e. difference between the current volume and the maximum
        (respectively minimum) volume.
        For example, when the volume range is [0-100] and we want to adjust by +50%:

        If the current volume is 25, the increment will be:
        "(100-25)*50%=75*0.5=38" (once rounded) so the new volume will be 63.

        Another adjustment by +50% will be "(100-63)*0.5=19" to a volume of 82.
        If we want instead to adjust by -50%, the decrement would be "(25-0)*0.5=13" to a
        volume of 12, and another adjustment by -50% would be "(12-0)*0.5=6" to a volume of 6.
        """

        percent = min(max(0.0, percent), 100.0)
        param = MsgArg.MsgArg()
        param.SetDouble(percent)
        self.proxyBusObject.MethodCallNoReply(
            "org.alljoyn.Control.Volume", "AdjustVolumePercent", param, 1, 0)
        logging.info(
            "adjust volume for %s (%s) to %s", self.device_name, self.device_id, percent)


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
        alljoyn.RouterInit() 
        self.player = None
        self.queue = []

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
            self.allplayers[p['id']] = AllPlayer(
                self.g_bus, p['busname'], p['session_id'], p['name'], p['id'])

    def SetQueue(self, queue):
        self.queue = queue

    @staticmethod
    def item_url(item_id):
        host = config['allplay']['host'].get(unicode)
        return "http://%s:8337/trackfile/%s" % (host, item_id,)

    def OnEndOfPlayback(self, member, srcpath, message, device_id):
        print "EndOfPlayback2", self.player.device_name, device_id

        if self.player.device_id != device_id:
            return 

        self.PlayQueue()

    def PlayQueue(self):
        if len(self.queue) == 0:
            return

        item = self.queue.pop(0)
        print "item popped from queue", item
        url = AllPlayController.item_url(item['id'])
        self.player.PlayUrl(url)

    def PlayTrack(self, item_id):
        url = AllPlayController.item_url(item_id)
        self.player.PlayUrl(url)

    def __del__(self):
        print "Shutting Down"
        self.g_bus.Stop()
        self.g_bus.Join()
        alljoyn.RouterShutdown() 

    def CreateZone(self, device_ids):

        if not device_ids:
            self.player.Stop()  # Stop playing as all devices disconnected
            return

        devices = []
        state = 'stopped'
        position = 0
        current_url = None

        # We stop the current playing before changing.
        # However we save the current uri and position if playing.
        if self.player:
            state, position = self.player.GetPlayingState()
            print "state", state
            print "position", position
            current_url = self.player.GetCurrentItemUrl()
            self.player.Stop()

            # check if current player is in list. If so keep that one current
            if self.player.device_id in device_ids:
                devices = [
                    p for p in self.allplayers.values() if p.device_id != self.player.device_id]

        if not devices:
            # Use the first device _id as the player
            devices = [
                p for p in self.allplayers.values() if p.device_id in device_ids]
            self.player = devices.pop(0)

        print "using: ", self.player.device_name, "speaker", self.player.device_id
        self.player.OnEndOfPlayback = self.OnEndOfPlayback
        self.player.CreateZone(device_ids)

        # restart playing if needed
        if state.lower() == 'playing':
            self.player.PlayUrl(current_url)
            print "resetting position", position
            self.player.SetPosition(position)

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
            state, position = p.GetPlayingState()
            players.append({'id': p.device_id,
                            'name': p.device_name,
                            'state': state.lower(),
                            'volume': p.GetVolume()})

        print players
        return players

    def GetPlayer(self):
        return self.player


if __name__ == "__main__":
    controller = AllPlayController()

    tracks = []
    for t in range(5):
        tmp = {'url':'url'+ str(t),
                     'title': 'title' + str(t)
                    }
        tracks.append(tmp)

    for p in controller.allplayers.values():
        if "kitchen" in p.device_name.lower():
            print "Device", p.device_name
            # print p.GetPlayingState()

            #p.UpdatePlaylist(tracks)

            print p.GetPlaylist()
            print p.GetLoopMode()
            p.SetLoopMode("None")

    while True:
        time.sleep(0.1)
