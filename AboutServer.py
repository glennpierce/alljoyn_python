#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, MsgArg, AboutData, \
    QStatusException, AboutObjectDescription, Session, \
    TransportMask, SessionListener, AboutProxy, ProxyBusObject, \
    Message, SessionPortListener, AboutObject, AjAPI, InterfaceDescription
import signal
import time
import sys

timeout = 10
ASSIGNED_SESSION_PORT = 900
INTERFACE_NAME = "com.example.about.feature.interface.sample"


def signal_handler(signal, frame):
    s_interrupt = True


/**
 * Respond to remote method call `Echo` by returning the string back to the sender
 */
static void echo_cb(alljoyn_busobject object,
                    const alljoyn_interfacedescription_member* member,
                    alljoyn_message msg) {
    alljoyn_msgarg arg = alljoyn_message_getarg(msg, 0);
    QCC_UNUSED(member);
    printf("Echo method called %s\n", ((ajn::MsgArg*)arg)->v_string.str);

    QStatus status = alljoyn_busobject_methodreply_args(object, msg, arg, 1);
    if (status != ER_OK) {
        printf("Failed to created MethodReply.\n");
    }
}



class MySessionPortListener(SessionPortListener.SessionPortListener):
    def __init__(self, callback_data=None):
        super(MySessionPortListener, self).__init__(callback_data=callback_data)
        self.sessionListener = MySessionListener()
        
    def OnAcceptSessionJoinerCallBack(self, callback_data, session_port, joiner, opts):
        QCC_UNUSED(joiner);
        QCC_UNUSED(opts);

        if (sessionPort != ASSIGNED_SESSION_PORT) {
            printf("Rejecting join attempt on unexpected session port %d\n", sessionPort);
            return false;
        }
        return true;

    def OnSessionJoinedCallback(self, callback_data, session_port, session_id, joiner):
        QCC_UNUSED(sessionPort);
        QCC_UNUSED(joiner);

        printf("Session Joined SessionId = %u\n", id);
    
     
        
class MyBusObject(BusObject.BusObject):
    def __init__(self, bus_attachment, path, is_place_holder):
        super(MyBusObject, self).__init__(path, False)   
        self.iface = bus_attachment.GetInterface(INTERFACE_NAME)
        self.AddInterface(self.iface)
        self.SetAnnounceFlag(self.iface, AjAPI.AnnounceFlag.ANNOUNCED);
        
        methodEntryStruct = BusObjectMethodEntry()
        methodEntryStruct.Member = self.iface.GetMember("Echo")
        methodEntryStruct.MethodHandler = MessageReceiver.MessageReceiverMethodHandlerFuncType(MyBusObject.Echo)
        
        self.AddMethodHandlers(self, [methodEntryStruct]):
    
    @staticmethod
    def Echo(member, msg):
        # Respond to remote method call `Echo` by returning the string back to the
        # sender.
        text = msg.GetArg(0).GetString()
        print "Echo method called:", text
        replyMsg = MsgArg.MsgArg()
        replyMsg.SetString("Echoing ... " + text)


#void Echo(const InterfaceDescription::Member* member, Message& msg) {
#        QCC_UNUSED(member);

#        printf("Echo method called: %s", msg->GetArg(0)->v_string.str);
#        const MsgArg* arg((msg->GetArg(0)));
#        QStatus status = MethodReply(msg, arg, 1);
#        if (status != ER_OK) {
#            printf("Failed to created MethodReply.\n");
#        }
#    }
    
        
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

        
        
    opts = Session.SessionOpts(ALLJOYN_TRAFFIC_TYPE_MESSAGES,
                                    False,
                                    ALLJOYN_PROXIMITY_ANY,
                                    ALLJOYN_TRANSPORT_ANY)
    

    alljoyn_sessionport sessionPort = ASSIGNED_SESSION_PORT;
    
    listener = MySessionPortListener()
    
    g_bus.BindSessionPort(session_port, opts, listener)
    
 
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
    

    busObject = MyBusObject(gbus, "/example/path")

    g_bus.RegisterBusObject(busObject)
    
    # Announce about signal */
    
    aboutObj = AboutObject.AboutObject(g_bus, AjAPI.AnnounceFlag.UNANNOUNCED)

    # Note the ObjectDescription that is part of the Announce signal is found
    # automatically by introspecting the BusObjects registered with the bus
    # attachment.
   
    try:
        aboutObj.Announce(sessionPort, aboutData)
        print "AboutObj Announce Succeeded."
    except AlljoynPy.QStatusException ex:
        print str(ex)

    # Perform the service asynchronously until the user signals for an exit 
    while s_interrupt is False:
        time.sleep(0.1)
        t += 0.1

        if t >= timeout:
            break

    alljoyn_aboutobj_unannounce(aboutObj);
    alljoyn_sessionportlistener_destroy(listener);

    g_bus.Stop()
    g_bus.Join()