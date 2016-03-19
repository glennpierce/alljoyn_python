#!/usr/bin/env python
# -*- coding: utf-8 -*-

from AllJoynPy import *

from AllJoynPy import AboutListener, MsgArg, AboutData, \
    AboutObjectDescription, Session, BusObject, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, MessageReceiver, \
    Message, SessionPortListener, AboutObj, AjAPI, InterfaceDescription

import signal
import time
import sys

ASSIGNED_SESSION_PORT = 900
INTERFACE_NAME = "com.example.about.feature.interface.sample"

s_interrupt = False


def signal_handler(signal, frame):
    s_interrupt = True


class MySessionPortListener(SessionPortListener.SessionPortListener):
    def __init__(self, context=None):
        super(MySessionPortListener, self).__init__(context=context)

    def OnAcceptSessionJoinerCallBack(self, context, session_port, joiner, opts):
        if session_port != ASSIGNED_SESSION_PORT:
            print "Rejecting join attempt on unexpected session port", session_port
            return False
        return True

    def OnSessionJoinedCallback(self, context, session_port, session_id, joiner):
        print "Session Joined SessionId", session_id


class MyBusObject(BusObject.BusObject):
    def __init__(self, bus_attachment, path, is_place_holder=False):
        super(MyBusObject, self).__init__(path, is_place_holder)

        iface = bus_attachment.GetInterface(INTERFACE_NAME)

        self.AddInterface(iface)

        self.SetAnnounceFlag(iface, AjAPI.AnnounceFlag.Announced)

        methodEntryStruct = BusObject.BusObjectMethodEntry()
        methodEntryStruct.Member = iface.GetMember("Echo")

        methodEntryStruct.MethodHandler = MessageReceiver.MessageReceiverMethodHandlerFuncType(MyBusObject.Echo)

        self.AddMethodHandlers([methodEntryStruct])

    @staticmethod
    def Echo(busobject_handle, member, msg):
        # Respond to remote method call `Echo` by returning the string back to the
        # sender.
        message = Message.Message.FromHandle(msg)
        msgarg = message.GetArg(0)

        text = msgarg.GetString()
        print "Server Echo method recieved:", text

        replyArg = MsgArg.MsgArg()
        replyArg.SetString("Echoing back:" + text)

        print BusObject.BusObject.FromHandle(busobject_handle).MethodReplyArgs(message, replyArg, 1)

if __name__ == "__main__":

    # Install SIGINT handler so Ctrl + C deallocates memory properly
    alljoyn = AllJoyn()

    print "AllJoyn Library version:", alljoyn.Version
    print "AllJoyn Library build info:", alljoyn.BuildInfo

    signal.signal(signal.SIGINT, signal_handler)

    # Create message bus
    g_bus = alljoyn.BusAttachment.BusAttachment("About Service Example", True)

    # Start the msg bus
    g_bus.Start()

    try:
        g_bus.Connect(None)
    except QStatusException as ex:
        print "Have you got the daemon running ?"
        sys.exit(1)

    opts = Session.SessionOpts(Session.ALLJOYN_TRAFFIC_TYPE_MESSAGES,
                               False,
                               Session.ALLJOYN_PROXIMITY_ANY,
                               TransportMask.ALLJOYN_TRANSPORT_ANY)

    listener = MySessionPortListener()

    sessionPort = g_bus.BindSessionPort(ASSIGNED_SESSION_PORT, opts, listener)

    aboutData = AboutData.AboutData(language="en")

    appId = [0x01, 0xB3, 0xBA, 0x14, 0x1E, 0x82, 0x11, 0xE4, 0x86, 0x51, 0xD1, 0x56, 0x1D, 0x5D, 0x46, 0xB0]

    aboutData.SetAppId(appId)
    aboutData.SetDeviceName("My Device Name", "en")

    # DeviceId is a string encoded 128bit UUID
    aboutData.SetDeviceId("93c06771-c725-48c2-b1ff-6a2a59d445b8")
    aboutData.SetAppName("Application", "en")
    aboutData.SetManufacturer("Manufacturer", "en")
    aboutData.SetModelNumber("123456")
    aboutData.SetDescription("A poetic description of this application", "en")
    aboutData.SetDateOfManufacture("2014-03-24")
    aboutData.SetSoftwareVersion("0.1.2")
    aboutData.SetHardwareVersion("0.0.1")
    aboutData.SetSupportURL("http://www.example.org")

    # The default language is automatically added to the `SupportedLanguages`
    # Users don't have to specify the AJSoftwareVersion its automatically added
    # to the AboutData/
    # Adding Spanish Localization values to the AboutData. All strings MUST be
    # UTF-8 encoded.

    aboutData.SetDeviceName("Mi dispositivo Nombre", "es")
    aboutData.SetAppName("aplicación", "es")
    aboutData.SetManufacturer("fabricante", "es")
    aboutData.SetDescription("Una descripción poética de esta aplicación", "es")

    # Check to see if the aboutData is valid before sending the About Announcement
    if not aboutData.IsValid("en"):
        print "failed to setup about data."

    interface = """
<node>
  <interface name='%s'>
    <method name='Echo'>
      <arg name='out_arg' type='s' direction='in' />
      <arg name='return_arg' type='s' direction='out' />
    </method>
  </interface>
</node>
""" % (INTERFACE_NAME,)

    print "Interface =", interface

    g_bus.CreateInterfacesFromXML(interface)

    myBusObject = MyBusObject(g_bus, "/example/path")

    g_bus.RegisterBusObject(myBusObject)

    # Announce about signal */

    aboutObj = AboutObj.AboutObject(g_bus, AjAPI.AnnounceFlag.UnAnnounced)

    # Note the ObjectDescription that is part of the Announce signal is found
    # automatically by introspecting the BusObjects registered with the bus
    # attachment.

    try:
        aboutObj.Announce(sessionPort, aboutData)
        print "AboutObj Announce Succeeded."
    except QStatusException as ex:
        print str(ex)

    # Perform the service asynchronously until the user signals for an exit
    while s_interrupt is False:
        time.sleep(0.1)

    print "HERE .................................."

    aboutObj.UnAnnounce()

    g_bus.Stop()
    g_bus.Join()
