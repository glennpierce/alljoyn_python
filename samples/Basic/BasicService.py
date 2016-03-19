#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message, BusListener, BusAttachment, DBusDefines, BusObject,  \
    SessionPortListener, AjAPI, MessageReceiver, SessionBusListener
import signal
import time
import sys


INTERFACE_NAME = "org.alljoyn.Bus.sample"
SERVICE_NAME = "org.alljoyn.Bus.sample"
SERVICE_PATH = "/sample";
SERVICE_PORT = 25;

s_interrupt = False

def signal_handler(signal, frame):
    global s_interrupt
    s_interrupt = True


class BasicServiceObject(BusObject.BusObject):
    def __init__(self, bus_attachment, path):
        super(BasicServiceObject, self).__init__(path)

        iface = bus_attachment.GetInterface(INTERFACE_NAME)

        self.AddInterface(iface)
        self.SetAnnounceFlag(iface, AjAPI.AnnounceFlag.Announced)

        methodEntryStruct = BusObject.BusObjectMethodEntry()
        methodEntryStruct.Member = iface.GetMember("cat")
        methodEntryStruct.MethodHandler = MessageReceiver.MessageReceiverMethodHandlerFuncType(BasicServiceObject.cat)
        self.AddMethodHandlers([methodEntryStruct])

    @staticmethod
    def cat(busobject_handle, member, msg):

        # Concatenate the two input strings and reply with the result.
        message = Message.Message.FromHandle(msg)
        output = message.GetArg(0).GetString() + message.GetArg(1).GetString()
        
        replyArg = MsgArg.MsgArg()
        replyArg.SetString(output)

        BusObject.BusObject.FromHandle(busobject_handle).MethodReplyArgs(message, replyArg, 1)

        replyArg.Destroy()


class MyListener(SessionBusListener.SessionBusListener):
    def __init__(self, context=None):
        super(MyListener, self).__init__(context=context)

    def OnAcceptSessionJoinerCallBack(self, context, session_port, joiner, opts):
        if session_port != SERVICE_PORT:
            print "Rejecting join attempt on unexpected session port", session_port
            return False
        return True

    def OnNameOwnerChangedCallBack(self, context, bus_name, previous_owner, new_owner):
        if new_owner and bus_name == SERVICE_NAME:
            print "NameOwnerChanged: name=%s, oldOwner=%s, newOwner=%s." % (bus_name, previous_owner, new_owner)


def CreateBasicServiceInterface(bus_attachment):
    iface = bus_attachment.CreateInterface(INTERFACE_NAME)
    ##AddMember(self, message_type, name, inputSig, outSig, argNames, annotation):
    #iface.AddMember(Message.MessageType.ALLJOYN_MESSAGE_METHOD_CALL, "GetCurrentItemUrl", None,  "s", None, 0)
    iface.AddMethod("cat", "ss",  "s", "inStr1,inStr2,outStr", 0, None)
    iface.Activate()


if __name__ == "__main__":
    alljoyn = AllJoyn()

    signal.signal(signal.SIGINT, signal_handler)

    myListener = MyListener()

    g_bus = BusAttachment.BusAttachment("myApp", True) 

    g_bus.RegisterBusListener(myListener.busListener)
    
    CreateBasicServiceInterface(g_bus)

    basicServiceObject = BasicServiceObject(g_bus, SERVICE_PATH)
         
    g_bus.RegisterBusObject(basicServiceObject)

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


    g_bus.BindSessionPort(SERVICE_PORT, opts, myListener.sessionPortListener)
    

    # Advertise this service on the bus.
    # There are three steps to advertising this service on the bus.
    # 1) Request a well-known name that will be used by the client to discover
    #    this service.
    # 2) Create a session.
    # 3) Advertise the well-known name.
    flags = DBusDefines.DBUS_NAME_FLAG_REPLACE_EXISTING | DBusDefines.DBUS_NAME_FLAG_DO_NOT_QUEUE
    g_bus.RequestName(SERVICE_NAME, flags)

    g_bus.AdvertiseName(SERVICE_NAME, TransportMask.ALLJOYN_TRANSPORT_ANY)

    while s_interrupt is False:
        time.sleep(0.1)