#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, QStatusException
import signal, time
import sys

#Note the removal of almost all Error handling to make the sample code more
#straight forward to read.  This is only used here for demonstration actual
#programs should check the return values of all method calls.
 

timeout = 10

INTERFACE_NAME = "net.allplay.MediaPlayer";


def signal_handler(signal, frame):
    QCC_UNUSED(sig);
    s_interrupt = True;

"""

# Print out the fields found in the AboutData. Only fields with known signatures
# are printed out.  All others will be treated as an unknown field.
def printAboutData(aboutData, language, tabNum:
    size_t count = alljoyn.AboutdataGetfields(aboutData, None, 0) 
    fields = C.create_string_buffer(count)            # sould be arrary of arrays
    aboutData.GetFields(fields, count)
    
    for i in range(count):
        for j in range(tabNum):
            print "\t"
        }
        print "Key: %s" % (fields[i],)

        tmp = aboutData.GetField(fields[i], language)
        
        print "\t"
        
        tmp = 
        signature = C.create_string_buffer(256)  
        tmp.Signature(signature, tmp, 16)
        
        if signature[0] == "s":
            tmp_s = C.create_string_buffer(256)  
            tmp.GetString(tmp_s)
            print tmp_s
        #elif 
        
        
        #} else if (!strncmp(signature, "as", 2)) {
        #    size_t las;
        #    alljoyn_msgarg as_arg = alljoyn_msgarg_create();
        #    alljoyn_msgarg_get(tmp, "as", &las, &as_arg);

        #    for (size_t j = 0; j < las; ++j) {
        #        const char* tmp_s;
        #        alljoyn_msgarg_get(alljoyn_msgarg_array_element(as_arg, j), "s", &tmp_s);
        #        printf("%s ", tmp_s);
        #    }
        #} else if (!strncmp(signature, "ay", 2)) {
        #    size_t lay;
        #    uint8_t* pay;
        #    alljoyn_msgarg_get(tmp, "ay", &lay, &pay);
        #    for (k = 0; k < lay; ++k) {
        #        printf("%02x ", pay[k]);
        #    }
        #} else {
        #    printf("User Defined Value\tSignature: %s", signature);
        #}
        #printf("\n");
    #}
    #free((void*)fields);
#}
    
    
#def BusListenerLostAdvertisedNameFuncT(context, name, transport, namePrefix):
    

    
    
typedef struct my_about_listener_t {
    alljoyn_sessionlistener sessionlistener;
    alljoyn_aboutlistener aboutlistener;
}my_about_listener;

static void alljoyn_sessionlistener_connect_lost_cb(const void* context,
                                                    alljoyn_sessionid sessionId,
                                                    alljoyn_sessionlostreason reason)
{
    QCC_UNUSED(context);
    printf("SessionLost sessionId = %u, Reason = %d\n", sessionId, reason);
}






class MyAboutListener(object):
    def __init__(self):
        self.aboutListener = alljoyn.AboutListener(callback, result)



def my_about_listener create_my_alljoyn_aboutlistener():
    callback->about_listener_announced = announced_cb;

    result->aboutlistener = alljoyn_aboutlistener_create(callback, result);

    result->sessionlistener = create_my_alljoyn_sessionlistener();

    return result;







def announced_cb(context, busName, version, port, objectDescriptionArg, aboutDataArg)
{
    my_about_listener* mylistener = (my_about_listener*) context;
        
    objectDescription = AboutObjectDescription();
    objectDescription.CreateFromMsgArg(objectDescription, objectDescriptionArg)

    print "*********************************************************************************"
    print "Announce signal discovered"
    print "\tFrom bus %s", busName
    print "\tAbout version %hu", version
    print "\tSessionPort %hu", port
    print "\tObjectDescription"

    aod = AboutObjectDescription();
    aod.CreateFromMsgArg(aod, objectDescriptionArg)

    path_num = aod.Getpaths(None, 0)

    paths = C.create_string_buffer(path_num)  
    aod.Getpaths(paths, path_num)


    print "\tAboutData:"
    alljoyn_aboutdata aboutData = AboutData("en", aboutDataArg)



  #  printf("\tAboutData:\n");
  #  alljoyn_aboutdata aboutData = alljoyn_aboutdata_create_full(aboutDataArg, "en");
    
    printAboutData(aboutData, NULL, 2);
    printf("*********************************************************************************\n");
    QStatus status;
    if (g_bus != NULL) {
        alljoyn_sessionid sessionId;
        alljoyn_sessionopts sessionOpts =
            alljoyn_sessionopts_create(ALLJOYN_TRAFFIC_TYPE_MESSAGES,
                                       QCC_FALSE, ALLJOYN_PROXIMITY_ANY,
                                       ALLJOYN_TRANSPORT_ANY);

        alljoyn_busattachment_enableconcurrentcallbacks(g_bus);
        status =
            alljoyn_busattachment_joinsession(g_bus, busName, port,
                                              mylistener->sessionlistener,
                                              &sessionId, sessionOpts);
        if (ER_OK == status && 0 != sessionId) {
            alljoyn_aboutproxy aboutProxy =
                alljoyn_aboutproxy_create(g_bus, busName, sessionId);
            alljoyn_msgarg objArg = alljoyn_msgarg_create();
            alljoyn_aboutproxy_getobjectdescription(aboutProxy, objArg);
            printf("*********************************************************************************\n");
            printf("AboutProxy.GetObjectDescription:\n");
            alljoyn_aboutobjectdescription aod2 =
                alljoyn_aboutobjectdescription_create();
            alljoyn_aboutobjectdescription_createfrommsgarg(aod2, objArg);

            path_num = alljoyn_aboutobjectdescription_getpaths(aod2, NULL, 0);
            paths = (const char**) malloc(sizeof(const char*) * path_num);
            alljoyn_aboutobjectdescription_getpaths(aod2, paths, path_num);

            for (size_t i = 0; i < path_num; ++i) {
                printf("\t\t%s\n", paths[i]);
                size_t intf_num =
                    alljoyn_aboutobjectdescription_getinterfaces(aod2,
                                                                 paths[i],
                                                                 NULL, 0);
                const char** intfs =
                    (const char**) malloc(sizeof(const char*) * intf_num);
                alljoyn_aboutobjectdescription_getinterfaces(aod2, paths[i],
                                                             intfs, intf_num);

                for (size_t j = 0; j < intf_num; ++j) {
                    printf("\t\t\t%s\n", intfs[j]);
                }
                free((void*)intfs);
                intfs = NULL;
            }
            free((void*) paths);
            paths = NULL;

            alljoyn_msgarg aArg = alljoyn_msgarg_create();
            alljoyn_aboutproxy_getaboutdata(aboutProxy, "en", aArg);
            printf("*********************************************************************************\n");
            printf("AboutProxy.GetAboutData: (Default Language)\n");
            aboutData = alljoyn_aboutdata_create("en");
            alljoyn_aboutdata_createfrommsgarg(aboutData, aArg, "en");
            printAboutData(aboutData, NULL, 1);
            size_t lang_num =
                alljoyn_aboutdata_getsupportedlanguages(aboutData, NULL, 0);
            if (lang_num > 1) {
                const char** langs =
                    (const char**) malloc(sizeof(char*) * lang_num);
                alljoyn_aboutdata_getsupportedlanguages(aboutData,
                                                        langs,
                                                        lang_num);
                char* defaultLanguage;
                alljoyn_aboutdata_getdefaultlanguage(aboutData,
                                                     &defaultLanguage);
                /*
                 * Print out the AboutData for every language but the
                 * default it has already been printed.
                 */
                for (size_t i = 0; i < lang_num; ++i) {
                    if (strcmp(defaultLanguage, langs[i]) != 0) {
                        status = alljoyn_aboutproxy_getaboutdata(aboutProxy,
                                                                 langs[i],
                                                                 aArg);
                        if (ER_OK == status) {
                            alljoyn_aboutdata_createfrommsgarg(aboutData,
                                                               aArg,
                                                               langs[i]);
                            printAboutData(aboutData, langs[i], 1);
                        }
                    }
                }
                free((void*)langs);
                langs = NULL;
                uint16_t ver;
                alljoyn_aboutproxy_getversion(aboutProxy, &ver);
                printf("*********************************************************************************\n");
                printf("AboutProxy.GetVersion %hd\n", ver);
                printf("*********************************************************************************\n");

                const char* path;
                alljoyn_aboutobjectdescription_getinterfacepaths(objectDescription,
                                                                 INTERFACE_NAME,
                                                                 &path, 1);

                alljoyn_proxybusobject proxyObject =
                    alljoyn_proxybusobject_create(g_bus, busName,
                                                  path, sessionId);

                status =
                    alljoyn_proxybusobject_introspectremoteobject(proxyObject);

                if (status != ER_OK) {
                    printf("Failed to introspect remote object.\n");
                }
                alljoyn_msgarg arg =
                    alljoyn_msgarg_create_and_set("s", "ECHO Echo echo...\n");
                alljoyn_message replyMsg = alljoyn_message_create(g_bus);

                alljoyn_proxybusobject_methodcall(proxyObject,
                                                  INTERFACE_NAME,
                                                  "Echo", arg,
                                                  1, replyMsg,
                                                  25000, 0);
                if (status != ER_OK) {
                    printf("Failed to call Echo method.\n");
                    return;
                }

                char* echoReply;
                alljoyn_msgarg reply_msgarg =
                    alljoyn_message_getarg(replyMsg, 0);
                status = alljoyn_msgarg_get(reply_msgarg, "s", &echoReply);
                if (status != ER_OK) {
                    printf("Failed to read Echo method reply.\n");
                }
                printf("Echo method reply: %s\n", echoReply);
                alljoyn_message_destroy(replyMsg);
                alljoyn_msgarg_destroy(arg);
                alljoyn_proxybusobject_destroy(proxyObject);
            }

            alljoyn_msgarg_destroy(aArg);
            alljoyn_aboutobjectdescription_destroy(aod2);
            alljoyn_msgarg_destroy(objArg);
            alljoyn_aboutproxy_destroy(aboutProxy);
        }
        alljoyn_sessionopts_destroy(sessionOpts);
    } else {
        printf("BusAttachment is NULL\n");
    }
    alljoyn_aboutdata_destroy(aboutData);
    alljoyn_aboutobjectdescription_destroy(aod);
    alljoyn_aboutobjectdescription_destroy(objectDescription);




def BusListenerBusPropertyChangedFunc(context, prop_name, prop_value):
    pass
     

callback = AllJoynPy.AboutListenerCallback()
callback.AboutListenerAnnouncedFuncType = AllJoynPy.AboutListenerAnnouncedFuncType(announced_cb)

"""

#aboutlistener = AuthListener(callback, result)


class MyAboutListener(AboutListener.AboutListener):
    def __init__(self):
        super(MyAboutListener, self).__init__()
        
    def OnAboutListenerCallBack(self, context, busName, version, port, objectDescriptionArg, aboutDataArg):
        print "Harley    GLENN !!!!!!!!!!!!!!!!!!!", busName, version, port, objectDescriptionArg, aboutDataArg


        #objectDescription = AboutObjectDescription();
        #objectDescription.CreateFromMsgArg(objectDescription, objectDescriptionArg)

        #print "*********************************************************************************"
        #print "Announce signal discovered"
        #print "\tFrom bus %s", busName
        #print "\tAbout version %hu", version
        #print "\tSessionPort %hu", port
        #print "\tObjectDescription"

        #aod = AboutObjectDescription();
        #aod.CreateFromMsgArg(aod, objectDescriptionArg)

        #path_num = aod.Getpaths(None, 0)

        #paths = C.create_string_buffer(path_num)  
        #aod.Getpaths(paths, path_num)


        #print "\tAboutData:"
        #alljoyn_aboutdata aboutData = AboutData("en", aboutDataArg)



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
    
    aboutListener = MyAboutListener()
   
    g_bus.RegisterAboutListener(aboutListener)
   
    g_bus.WhoImplementsInterfaces([INTERFACE_NAME])

    s_interrupt = False
    t=0
    while s_interrupt == False:
        time.sleep(0.1)
        t += 0.1
        
        if t >= timeout:
            break


"""
    

    destroy_my_alljoyn_aboutlistener(listener);

    alljoyn_busattachment_stop(g_bus);
    alljoyn_busattachment_join(g_bus);

    alljoyn_busattachment_destroy(g_bus);


    alljoyn_shutdown();
"""

