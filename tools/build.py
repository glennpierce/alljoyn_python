import os, os.path, re
import CppHeaderParser
from glob import glob, iglob

name_map = {
            'authlistener': 'AuthListener',
            'busobject': 'BusObject',
            'proxybusobject': 'ProxyBusObject',
            'observerlistener': 'ObserverListener',
            'observer_object': 'PbserverObject',
            'observer': 'Observer',
            'sessionportlistener': 'SessionPortListener',
            'aboutdatalistener': 'AboutDataListener',
            'aboutdata': 'AboutData',
            'aboutobj': 'AboutObject',
            'msgarg': 'MsgArg',
            'aboutobjectdescription': 'AboutObjectDescription',
            'proxybusobject_listener': 'ProxyBusObjectListener',
            'proxybusobject': 'ProxyBusObject',
            'messagereceiver': 'MessageReceiver',
            'autopinger': 'AutoPinger',
            'sessionlistener': 'SessionListener',
            'abouticonobj': 'AboutIconObj',
            'abouticon': 'AboutIcon',
            'sessionopts': 'SessionOpts',
            'passwordmanager': 'PasswordManager',
            'interfacedescription_member': 'InterfaceDescriptionMember',
            'interfacedescription_property': 'InterfaceDescriptionProperty',
            'interfacedescription': 'InterfaceDescription',
            'abouticonproxy': 'AboutIconProxy',
            'permissionconfigurationlistener': 'PermissionConfigurationListener',
            'keystorelistener': 'KeyStoreListener',
            'busattachment': 'BusAttachment',
            'buslistener_listener': 'BusListenerListener',
            'buslistener': 'BusListener',
            'aboutproxy': 'AboutProxy',
            'message': 'Message',
            'aboutlistener': 'AboutListener',
            'alljoyn': 'AllJoyn',
            'pinglistener': 'PingListener',
            'authlistenerasync': 'AuthListenerAsync',
            'credentials': 'Credentials',
            'unity': 'Unity',
            'about': 'About'
           }

type_map = {'char': 'C.c_int8',
            'char*': 'C.c_char_p',
            'void*': 'C.c_void_p',
            'bool': 'C.c_uint8',                                  
            'size_t':'C.csize_t',
            'uint8_t': 'C.c_uint8',    
            'int16_t': 'C.c_int16',    
            'uint16_t': 'C.c_uint16',    
            'int32_t': 'C.c_int32',    
            'uint32_t': 'C.uint32_t',   
            'int64_t':'C.c_int64',        
            'uint64_t':'C.c_uint64',   
            'double':'C.c_double',           
            'QCC_BOOL':'C.c_int32',   
            'QStatus':  'C.c_uint32',    
            'QCC_BOOL*':'POINTER(C.c_int32)',
            'uint8_t*':'POINTER(C.c_uint8_t)',          
            'uint8_t**': 'POINTER(C.c_uint8)',            
            'int16_t*':'POINTER(C.c_int16)', 
            'uint16_t*':'POINTER(C.c_uint16)', 
            'int32_t*':'POINTER(C.c_int32)', 
            'uint32_t*':'POINTER(C.c_uint32)', 
            'int64_t*':'POINTER(C.c_int64)', 
            'uint64_t*':'POINTER(C.c_uint64_t)',     
            'double*':'POINTER(C.c_double)', 
            'char**':'POINTER(C.c_char_p)', 
            'size_t*':'POINTER(C.csize_t)', 

            'alljoyn_transportmask': 'C.uint16_t',
            
            'alljoyn_proxybusobject': 'C.c_void_p',
            'alljoyn_aboutdata': 'C.c_void_p',
            'alljoyn_abouticon': 'C.c_void_p',
            'alljoyn_abouticonproxy': 'C.c_void_p',
            'alljoyn_aboutobjectdescription': 'C.c_void_p',
            'alljoyn_aboutobj': 'C.c_void_p',
            'alljoyn_busattachment': 'C.c_void_p',
            'alljoyn_authlistener': 'C.c_void_p',
            'alljoyn_credentials': 'C.c_void_p',
            'alljoyn_autopinger': 'C.c_void_p',
            'alljoyn_busobject': 'C.c_void_p',
            'alljoyn_interfacedescription': 'C.c_void_p',
            'alljoyn_message': 'C.c_void_p',
            'alljoyn_msgarg': 'C.c_void_p',
            'const alljoyn_interfacedescription_member': 'C.c_void_p',
            'alljoyn_interfacedescription_member *': 'POINTER(C.c_void_p)',
            'const uint8_t *': 'POINTER(C.c_uint8_t)',
            'uint8_t *': 'POINTER(C.c_uint8_t)',
            'const alljoyn_msgarg': 'C.c_void_p',
            'alljoyn_msgarg': 'C.c_void_p',
            'alljoyn_sessionopts': 'C.c_void_p',
            
            'alljoyn_sessionid': 'C.c_uint32',
            'alljoyn_buslistener': 'C.c_void_p',
            'alljoyn_sessionport': 'C.c_uint16',
            'alljoyn_sessionport *': 'POINTER(C.c_uint16)',
            'const alljoyn_credentials': 'C.c_void_p',
            'const alljoyn_interfacedescription': 'C.c_void_p',
            'alljoyn_aboutlistener': 'C.c_void_p',
            'alljoyn_aboutproxy': 'C.c_void_p',
            'alljoyn_interfacedescription *': 'POINTER(C.c_void_p)',
            'alljoyn_pinglistener': 'C.c_void_p',
            'alljoyn_sessionlistener': 'C.c_void_p',
            'const alljoyn_sessionopts': 'C.c_void_p',
            'alljoyn_observer': 'C.c_void_p',
            'alljoyn_observerlistener': 'C.c_void_p',
            'alljoyn_keystorelistener': 'C.c_void_p',
            'void': 'as',  # Python keyword to flag error
            'const alljoyn_busattachment': 'C.c_void_p',
            'alljoyn_keystore': 'C.c_void_p',
            }


f = open('class_template.txt', 'r')
class_template = f.read()
f.close()
    
    
CallbackPtrTpPythonNameMap = {}
    
def underscore_to_camelcase(value):
    return ''.join([x.capitalize() for x in value.lower().split('_')])
    
def pass_function_name(func):
    name_parts = func['name'].split('_')
    name_end = []
    
    if 'DEPRECATED' in name_parts:
        raise

    try:
        if len(name_parts) == 2:
            python_name = name_map[name_parts[0]]
            name_end = name_parts[1:]
        elif len(name_parts) >= 3:
            python_name = name_map[name_parts[1]]
            name_end = name_parts[2:]
    except KeyError as ex:
        print str(ex)
        print header
        print name_parts
        raise
    
    return python_name, underscore_to_camelcase('_'.join(name_end))
    
def process_function_pointer_typedef(typedefs):
    for name, value in typedefs.items():
        
        if 'AJ_CALL *' in value:  # We have a function pointer typedef defined
            function_pointer_text = value
            pre_parsed = function_pointer_text.replace('AJ_CALL *', '') + ');' # play havoc with parser. Also parser leaves of ); on original typedef
            parts = pre_parsed.split(')')
            pre_parsed = 'extern ' + parts[0].replace('(','') + ')'.join(parts[1:])  # Nasty removeing () around name of function. Hope its robust enough
            print pre_parsed
            parsed = CppHeaderParser.CppHeader(pre_parsed, argType="string")
            
            
            for func in parsed.functions:  
                #print "name", func['name']
                try:
                    python_name_start, python_name_end = pass_function_name(func)
                    print python_name_start, python_name_end
                except:
                    continue
                
                parameter_types = []
                parameter_names = []
                parameter_ctypes = []
                
                #print func
                for param in func['parameters']:
                    parameter_names.append(param['name'])
                    parameter_types.append(param['type'])
                    parameter_ctypes.append(type_map[param['type'].replace(' ', '').replace('const', '')])
                
                callbackName = python_name_start + python_name_end
                CallbackPtrTpPythonNameMap[callbackName] = callbackName.replace('Ptr', 'FuncType')
                print CallbackPtrTpPythonNameMap[callbackName]  + " = CallbackType(None, " + ', '.join(parameter_ctypes) + ') # ' + ' '.join(parameter_names)
   
            
        
   
def process_structures(typedefs):
        
        #class BusListenerCallbacks(C.Structure):
    #_fields_ = [("BusListenerRegistered",
                    #POINTER(BusListenerRegisteredFuncType)),                 # const void* context, alljoyn_busattachment bus
                #("BusListenerUnRegistered",
                    #POINTER(BusListenerUnRegisteredFuncType)),                             # const void* context
                #("BusListenerFoundAdvertisedName", 
                    #POINTER(BusListenerFoundAdvertisedNameFuncType)), # const void* context, const char* name, alljoyn_transportmask transport, const char* namePrefix
                #("BusListenerLostAdvertisedName", 
                    #POINTER(BusListenerLostAdvertisedNameFuncType)), # const void* context, const char* name, alljoyn_transportmask transport, const char* namePrefix
                #("BusListenerNameOwnerChanged", 
                    #POINTER(BusListenerNameOwnerChangedFuncType)), # const void* context, const char* busName, const char* previousOwner, const char* newOwner
                #("BusListenerBusStopping", 
                    #POINTER(BusListenerBusStoppingFuncType)),                                     # const void* context
                #("BusListenerBusDisconnected", 
                    #POINTER(BusListenerBusDisconnectedFuncType)),                                     # const void* context
                #("BusListenerBusPropertyChanged", 
                    #POINTER(BusListenerBusPropertyChangedFuncType))             # const void* context, const char* prop_name, alljoyn_msgarg prop_value
               #]
               
               
    
def create_python_file(header, cpp_header):
    
    
    
    
    #print "class Constants(object):"
    #for name, value in cpp_header.typedefs.items():
    #    print "    #%s=%s" % (name,value)
    #print

    #for d in cpp_header.defines:
    #    print '    #', d
    
    
    #for t in cpp_header.typedefs:
    #    print '    #', d
    
    
    process_function_pointer_typedef(cpp_header.typedefs)
    
    for name, value in cpp_header.typedefs.items():
        
        if not 'AJ_CALL *' in value:  # We have a function pointer typedef defined allready dealt with
            print "name", name
            print "value", value 
            print "\n\n"
    
    # build class
    for func in cpp_header.functions:
        python_name_start, python_name_end = pass_function_name(func)
        
        name_parts = func['name'].split('_')
        name_end = []
        
        if 'DEPRECATED' in name_parts:
            continue

        try:
            if len(name_parts) == 2:
                python_name = name_map[name_parts[0]]
                name_end = name_parts[1:]
            elif len(name_parts) >= 3:
                python_name = name_map[name_parts[1]]
                name_end = name_parts[2:]
        except KeyError as ex:
            print str(ex)
            print header
            print name_parts
            raise
        
        
        
        
        #print "# wrapper for", original_name, "returns", func['rtnType']
    #method_text = "def " + new_name + '(self, ' + ', '.join(parameter_names) + '):  # ' + ', '.join(parameter_types) + '\n'
    
        #    BusListenerRegisteredFuncType = CallbackType(None, C.c_void_p, C.c_void_p)                 # const void* context, alljoyn_busattachment bus
    
        parameter_types = []
        parameter_names = []
    
        for param in func['parameters']:
            parameter_names.append(param['name'])
            parameter_types.append(param['type'])
        
        if func.has_key('pointer') and func['pointer'] == 1:  # Build callback types
            python_name_end = underscore_to_camelcase(name_end)
            print python_name + python_name_end + " = CallbackType(None, " + ', '.join(parameter_types) + ') #' + ''.join(parameter_names)
            #return

        print func, "\n\n\n"
        continue
        
        
        
        
        class_template_replaced = class_template.replace('__NAME__', python_name)
        print class_template_replaced
        

    
#for header in iglob('/home/glenn/Devel/alljoyn-15.09.00a-src/alljoyn_c/inc/alljoyn_c/*.h'):
for header in iglob('*.h'):

    try:
        print "processing", header
        cpp_header = CppHeaderParser.CppHeader(header)
        create_python_file(header, cpp_header)
    except CppHeaderParser.CppParseError as e:
        print(e)
        sys.exit(1)
        
       






#missing = 0

#for func in cppHeader.functions:
    #method_text = ""
    
    #original_name = func['name']

    ##if original_name != "alljoyn_aboutdata_createfromxml":
    ##    continue

    #new_name = underscore_to_camelcase(original_name)

    ##print original_name
    ##print new_name

    #new_return_type = None

    #allowed_return_types = {
                             #'const char *': 'C.c_char_p',
                             #'const char*': 'C.c_char_p',
                             #'QStatus': 'C.c_uint',
                             #'const char': 'C.c_int8',
                             #'void': '',
                             #'int':'C.c_uint',
                             #'int32_t': 'C.c_int32',
                             #'uint32_t': 'C.c_uint32',
                             #'uint8_t': 'C.c_uint8',
                             #'uint16_t': 'C.c_uint16',
                             #'bool': 'C.c_uint',
                             #'size_t': 'C.c_size_t',
                             #'QCC_BOOL': 'C.c_int32',
                             #'alljoyn_busattachment': 'C.c_void_p',
                             #'alljoyn_proxybusobject': 'C.c_void_p',
                             #'alljoyn_aboutdata': 'C.c_void_p',
                             #'alljoyn_aboutdatalistener': 'C.c_void_p',
                             #'alljoyn_abouticonproxy': 'C.c_void_p',
                             #'alljoyn_authlistener': 'C.c_void_p',
                             #'const alljoyn_interfacedescription': 'C.c_void_p',
                             #'alljoyn_sessionid': 'C.c_uint32',
                             #'alljoyn_msgarg': 'C.c_void_p',
                             #'alljoyn_aboutobjectdescription': 'C.c_void_p',
                             #'alljoyn_abouticonobj': 'C.c_void_p',
                             #'alljoyn_aboutlistener': 'C.c_void_p',
                             #'alljoyn_buslistener': 'C.c_void_p',
                             #'alljoyn_busobject': 'C.c_void_p',
                             #'const alljoyn_proxybusobject': 'C.c_void_p',
                             #'alljoyn_abouticon': 'C.c_void_p',
                             #'alljoyn_aboutobj': 'C.c_void_p',
                             #'alljoyn_aboutproxy': 'C.c_void_p',
                             #'alljoyn_credentials': 'C.c_void_p',
                             #'alljoyn_pinglistener': 'C.c_void_p',
                             #'alljoyn_sessionopts': 'C.c_void_p',
                             #'alljoyn_transportmask': 'C.c_void_p',
                             #'alljoyn_sessionlistener': 'C.c_void_p',
                             #'alljoyn_sessionportlistener': 'C.c_void_p',
                             #'const alljoyn_busattachment': 'C.c_void_p',
                             #'alljoyn_observerlistener': 'C.c_void_p',
                             #'alljoyn_observer': 'C.c_void_p',
                             #'alljoyn_messagetype': 'C.c_uint32',
                             #'alljoyn_message': 'C.c_void_p',
                             #'alljoyn_typeid': 'C.c_int32',
                             #'alljoyn_autopinger': 'C.c_int32',
                              #'alljoyn_interfacedescription_securitypolicy': 'C.c_int32',
                        

                                
                           #}

    #new_return_type = ''
    #try:
        #new_return_type = allowed_return_types[func['rtnType']]
    #except Exception as ex:
        #missing+=1
     ##   print original_name, str(ex)
        #continue
    
    
    #allowed_parameter_types = { 'const char *': 'C.c_char_p',
                                #'const char*': 'C.c_char_p',
                                #'char *': 'C.c_char_p',
                                #'void *': 'C.c_void_p',
                                #'bool': 'C.c_uint8',                                  
                                #'const uint8_t * *': 'POINTER(C.c_uint8)',
                                #'void *': 'C.c_void_p',
                                
                                #'size_t':'C.csize_t',
                                #'uint8_t': 'C.c_uint8',    
                                #'uint32_t': 'C.uint32_t',
                                #'uint32_t': 'C.uint32_t',           
                                #'int16_t': 'C.c_int16',    
                                #'uint16_t': 'C.c_uint16',    
                                #'int32_t': 'C.c_int32',            
                                #'QCC_BOOL':'C.c_int32',   
                                #'QStatus':  'C.c_uint32',    
                                #'const char': 'C.c_int8',
                                #'uint8_t *':'POINTER(C.c_uint8_t)',          
                                #'uint64_t *':'POINTER(C.c_uint64_t)',          
                                #'QCC_BOOL *':'POINTER(C.c_int32)',            
                                #'int16_t *':'POINTER(C.c_int16)', 
                                #'uint16_t *':'POINTER(C.c_uint16)', 
                                #'int32_t *':'POINTER(C.c_int32)', 
                                #'uint32_t *':'POINTER(C.c_uint32)', 
                                #'int64_t *':'POINTER(C.c_int64)', 
                                #'double *':'POINTER(C.c_double)', 
                                #'const char * *':'POINTER(C.c_char_p)', 
                                #'char * *':'POINTER(C.c_char_p)', 
                                #'size_t *':'POINTER(C.csize_t)', 
                                #'int64_t':'C.c_int64',        
                                #'uint64_t':'C.c_uint64',        
                                #'double':'C.c_double',        
                                #'const size_t': 'C.csize_t',
                                
                                
                                #'alljoyn_proxybusobject': 'C.c_void_p',
                                #'alljoyn_aboutdata': 'C.c_void_p',
                                #'alljoyn_abouticon': 'C.c_void_p',
                                #'alljoyn_abouticonproxy': 'C.c_void_p',
                                #'alljoyn_aboutobjectdescription': 'C.c_void_p',
                                #'alljoyn_aboutobj': 'C.c_void_p',
                                #'alljoyn_busattachment': 'C.c_void_p',
                                #'alljoyn_authlistener': 'C.c_void_p',
                                #'alljoyn_credentials': 'C.c_void_p',
                                #'alljoyn_autopinger': 'C.c_void_p',
                                #'alljoyn_busobject': 'C.c_void_p',
                                #'alljoyn_interfacedescription': 'C.c_void_p',
                                #'alljoyn_message': 'C.c_void_p',
                                #'alljoyn_msgarg': 'C.c_void_p',
                                #'const alljoyn_interfacedescription_member': 'C.c_void_p',
                                #'alljoyn_interfacedescription_member *': 'POINTER(C.c_void_p)',
                                #'const uint8_t *': 'POINTER(C.c_uint8_t)',
                                #'uint8_t *': 'POINTER(C.c_uint8_t)',
                                #'const alljoyn_msgarg': 'C.c_void_p',
                                #'alljoyn_msgarg': 'C.c_void_p',
                                #'alljoyn_sessionopts': 'C.c_void_p',
                                #'alljoyn_transportmask': 'C.c_void_p',
                                #'alljoyn_sessionid': 'C.c_uint32',
                                #'alljoyn_buslistener': 'C.c_void_p',
                                #'alljoyn_sessionport': 'C.c_uint16',
                                #'alljoyn_sessionport *': 'POINTER(C.c_uint16)',
                                #'const alljoyn_credentials': 'C.c_void_p',
                                #'const alljoyn_interfacedescription': 'C.c_void_p',
                                #'alljoyn_aboutlistener': 'C.c_void_p',
                                #'alljoyn_aboutproxy': 'C.c_void_p',
                                #'alljoyn_interfacedescription *': 'POINTER(C.c_void_p)',
                                #'alljoyn_pinglistener': 'C.c_void_p',
                                #'alljoyn_sessionlistener': 'C.c_void_p',
                                #'const alljoyn_sessionopts': 'C.c_void_p',
                                #'alljoyn_observer': 'C.c_void_p',
                                #'alljoyn_observerlistener': 'C.c_void_p',
                                #'alljoyn_keystorelistener': 'C.c_void_p',
                                #'void': 'as',  # Python keyword to flag error
                                #'const alljoyn_busattachment': 'C.c_void_p',
                                #'alljoyn_keystore': 'C.c_void_p',
                                #}

    #parameter_names = []
    #parameter_types = []
    
    #for param in func['parameters']:
        #parameter_names.append(param['name'])
        #parameter_types.append(param['type'])

    
    ##print "\n\n\n-----------------------------------\n"
    ##print "parameter_types", parameter_types
    ##print "\n\n"
    ##print "allowed_parameter_types", allowed_parameter_types.keys()
    ##print "\n\n\n-----------------------------------\n"
    
    
    #if not bool(set(parameter_types) & set(allowed_parameter_types.keys())):
        #missing+=1
    ##    print original_name, parameter_types
        #continue
    
    #try:
        #new_args_types = [allowed_parameter_types[p] for p in parameter_types]
    #except Exception as ex:
        #missing+=1
        
    ##    print original_name, str(ex)
        
        #continue
    
    ##print original_name
    ##continue
    
    
    #print "# wrapper for", original_name, "returns", func['rtnType']
    #method_text = "def " + new_name + '(self, ' + ', '.join(parameter_names) + '):  # ' + ', '.join(parameter_types) + '\n'
    #if new_return_type != '':
        #method_text += '    self.__lib.' + original_name + '.restype = ' + new_return_type + '\n';
    #method_text += '    self.__lib.' + original_name + '.argtypes = ' + '[' + ', '.join(new_args_types) + ']' + '\n';
    
    #if new_return_type != '':
        #if func['rtnType'] == 'QStatus':
            #method_text += '    return QStatus(self.__lib.' + original_name + '(' + ', '.join(parameter_names) + '))'
        #else:
            #method_text += '    return self.__lib.' + original_name + '(' + ', '.join(parameter_names) + ')'
    #else:
        #method_text += '    self.__lib.' + original_name + '(' + ', '.join(parameter_names) + ')'
    
    #print method_text, '\n\n'



#print "missing", missing
