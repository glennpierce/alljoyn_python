#!/usr/bin/env python

from AllJoynPy import AllJoyn, AboutListener, AboutData, QStatusException, AboutObjectDescription, MsgArg
import signal, time
import sys

timeout = 10

INTERFACE_NAME = "net.allplay.MediaPlayer";


def signal_handler(signal, frame):
    QCC_UNUSED(sig);
    s_interrupt = True;

"""
    
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


"""
void printAboutData(AboutData& aboutData, const char* language, int tabNum):
    for field in aboutData.GetFields():
        for (int j = 0; j < tabNum; ++j) {
            printf("\t");
        }
        printf("Key: %s", field);

        MsgArg* tmp;
        aboutData.GetField(fields[i], tmp, language);
        printf("\t");
        if (tmp->Signature() == "s") {
            const char* tmp_s;
            tmp->Get("s", &tmp_s);
            printf("%s", tmp_s);
        } else if (tmp->Signature() == "as") {
            size_t las;
            MsgArg* as_arg;
            tmp->Get("as", &las, &as_arg);
            for (size_t j = 0; j < las; ++j) {
                const char* tmp_s;
                as_arg[j].Get("s", &tmp_s);
                printf("%s ", tmp_s);
            }
        } else if (tmp->Signature() == "ay") {
            size_t lay;
            uint8_t* pay;
            tmp->Get("ay", &lay, &pay);
            for (size_t j = 0; j < lay; ++j) {
                printf("%02x ", pay[j]);
            }
        } else {
            printf("User Defined Value\tSignature: %s", tmp->Signature().c_str());
        }
        printf("\n");
    }
    delete [] fields;
}
"""

class MyAboutListener(AboutListener.AboutListener):
    def __init__(self):
        super(MyAboutListener, self).__init__()
        
    # Print out the fields found in the AboutData. Only fields with known signatures
    # are printed out.  All others will be treated as an unknown field.
    def printAboutData(self, aboutData, language, tabNum):
        for field in aboutData.GetFields():
            print "\t" * tabNum, "Key:", field
   
            tmp = aboutData.GetField(field)
            #print "\t"
            
            #print tmp
            
            #here
            #signature = tmp.Signature()
            #print "signature", signature
           
            #if signature and signature[0] == "s":
            #    print tmp.GetString()
                
                
                
                
            ##lse if (tmp->Signature() == "as") {
            #size_t las;
            #MsgArg* as_arg;
            #tmp->Get("as", &las, &as_arg);
            #for (size_t j = 0; j < las; ++j) {
                #const char* tmp_s;
                #as_arg[j].Get("s", &tmp_s);
                #printf("%s ", tmp_s);
            #}
        #} else if (tmp->Signature() == "ay") {
            #size_t lay;
            #uint8_t* pay;
            #tmp->Get("ay", &lay, &pay);
            #for (size_t j = 0; j < lay; ++j) {
                #printf("%02x ", pay[j]);
            #}
        #} else {
            #printf("User Defined Value\tSignature: %s", tmp->Signature().c_str());
        #}
        #printf("\n");
     

    def OnAboutListenerCallBack(self, context, busName, version, port, objectDescriptionArg, aboutDataArg):
        
        objectDescription = AboutObjectDescription.AboutObjectDescription(objectDescriptionArg)

        print "*********************************************************************************"
        print "Announce signal discovered"
        print "\tFrom bus",  busName
        print "\tAbout version", version
        print "\tSessionPort", port
        print "\tObjectDescription:"
        print "*********************************************************************************"
        print "Announce signal discovered"
        
        for path in objectDescription.GetPaths():
            print "\t\t", path
            for interface in objectDescription.GetInterfaces(path):
                print "\t\t\t", interface
         
        print "\tAboutData:"
        aboutData = AboutData.AboutData(aboutDataArg)
        
        self.printAboutData(aboutData, None, 2);
        
        print "*********************************************************************************"
        
        #QStatus status;

        #if (g_bus != NULL) {
            #SessionId sessionId;
            #SessionOpts opts(SessionOpts::TRAFFIC_MESSAGES, false, SessionOpts::PROXIMITY_ANY, TRANSPORT_ANY);
            #g_bus->EnableConcurrentCallbacks();
            #status = g_bus->JoinSession(busName, port, &sessionListener, sessionId, opts);
            #printf("SessionJoined sessionId = %u, status = %s\n", sessionId, QCC_StatusText(status));
            #if (ER_OK == status && 0 != sessionId) {
                #AboutProxy aboutProxy(*g_bus, busName, sessionId);

                #MsgArg objArg;
                #aboutProxy.GetObjectDescription(objArg);
                #printf("*********************************************************************************\n");
                #printf("AboutProxy.GetObjectDescription:\n");
                #AboutObjectDescription aboutObjectDescription(objArg);
                #path_num = aboutObjectDescription.GetPaths(NULL, 0);
                #paths = new const char*[path_num];
                #aboutObjectDescription.GetPaths(paths, path_num);
                #for (size_t i = 0; i < path_num; ++i) {
                    #printf("\t%s\n", paths[i]);
                    #size_t intf_num = aboutObjectDescription.GetInterfaces(paths[i], NULL, 0);
                    #const char** intfs = new const char*[intf_num];
                    #aboutObjectDescription.GetInterfaces(paths[i], intfs, intf_num);
                    #for (size_t j = 0; j < intf_num; ++j) {
                        #printf("\t\t%s\n", intfs[j]);
                    #}
                    #delete [] intfs;
                #}
                #delete [] paths;

                #MsgArg aArg;
                #aboutProxy.GetAboutData("en", aArg);
                #printf("*********************************************************************************\n");
                #printf("AboutProxy.GetAboutData: (Default Language)\n");
                #AboutData defaultLangAboutData(aArg);
                #printAboutData(defaultLangAboutData, NULL, 1);
                #size_t lang_num;
                #lang_num = defaultLangAboutData.GetSupportedLanguages();
                #// If the lang_num == 1 we only have a default language
                #if (lang_num > 1) {
                    #const char** langs = new const char*[lang_num];
                    #defaultLangAboutData.GetSupportedLanguages(langs, lang_num);
                    #char* defaultLanguage;
                    #defaultLangAboutData.GetDefaultLanguage(&defaultLanguage);
                    #// print out the AboutData for every language but the
                    #// default it has already been printed.
                    #for (size_t i = 0; i < lang_num; ++i) {
                        #if (strcmp(defaultLanguage, langs[i]) != 0) {
                            #status = aboutProxy.GetAboutData(langs[i], aArg);
                            #if (ER_OK == status) {
                                #defaultLangAboutData.CreatefromMsgArg(aArg, langs[i]);
                                #printf("AboutProxy.GetAboutData: (%s)\n", langs[i]);
                                #printAboutData(defaultLangAboutData, langs[i], 1);
                            #}
                        #}
                    #}
                    #delete [] langs;
                #}

                #uint16_t ver;
                #aboutProxy.GetVersion(ver);
                #printf("*********************************************************************************\n");
                #printf("AboutProxy.GetVersion %hd\n", ver);
                #printf("*********************************************************************************\n");

                #const char* path;
                #objectDescription.GetInterfacePaths(INTERFACE_NAME, &path, 1);
                #printf("Calling %s/%s\n", path, INTERFACE_NAME);
                #ProxyBusObject proxyObject(*g_bus, busName, path, sessionId);
                #status = proxyObject.IntrospectRemoteObject();
                #if (status != ER_OK) {
                    #printf("Failed to introspect remote object.\n");
                #}
                #MsgArg arg("s", "ECHO Echo echo...\n");
                #Message replyMsg(*g_bus);
                #status = proxyObject.MethodCall(INTERFACE_NAME, "Echo", &arg, 1, replyMsg);
                #if (status != ER_OK) {
                    #printf("Failed to call Echo method.\n");
                    #return;
                #}
                #char* echoReply;
                #status = replyMsg->GetArg(0)->Get("s", &echoReply);
                #if (status != ER_OK) {
                    #printf("Failed to read Echo method reply.\n");
                #}
                #printf("Echo method reply: %s\n", echoReply);
            #}
        #} else {
            #printf("BusAttachment is NULL\n");
        #}
    #}
    #MySessionListener sessionListener;



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


    g_bus.Stop()
    g_bus.Join()
    
