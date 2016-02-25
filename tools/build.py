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
            'alljoyn_proxybusobject*': 'POINTER(C.c_void_p)',
            'alljoyn_aboutdata': 'C.c_void_p',
            'alljoyn_aboutdata*': 'POINTER(C.c_void_p)',
            'alljoyn_abouticon': 'C.c_void_p',
            'alljoyn_abouticon*': 'POINTER(C.c_void_p)',
            'alljoyn_abouticonproxy': 'C.c_void_p',
            'alljoyn_abouticonproxy*': 'POINTER(C.c_void_p)',
            'alljoyn_aboutobjectdescription': 'C.c_void_p',
            'alljoyn_aboutobjectdescription*': 'POINTER(C.c_void_p)',
            'alljoyn_aboutobj': 'C.c_void_p',
            'alljoyn_aboutobj*': 'POINTER(C.c_void_p)',
            'alljoyn_busattachment': 'C.c_void_p',
            'alljoyn_busattachment*': 'POINTER(C.c_void_p)',
            'alljoyn_authlistener': 'C.c_void_p',
            'alljoyn_authlistener*': 'POINTER(C.c_void_p)',
            'alljoyn_credentials': 'C.c_void_p',
            'alljoyn_credentials*': 'POINTER(C.c_void_p)',
            'alljoyn_autopinger': 'C.c_void_p',
            'alljoyn_autopinger*': 'POINTER(C.c_void_p)',
            'alljoyn_busobject': 'C.c_void_p',
            'alljoyn_busobject*': 'POINTER(C.c_void_p)',
            'alljoyn_interfacedescription': 'C.c_void_p',
            'alljoyn_interfacedescription*': 'POINTER(C.c_void_p)',
            'alljoyn_message': 'C.c_void_p',
            'alljoyn_message*': 'POINTER(C.c_void_p)',
            'alljoyn_msgarg': 'C.c_void_p',
            'alljoyn_msgarg*': 'POINTER(C.c_void_p)',
            'const alljoyn_interfacedescription_member': 'C.c_void_p',
            'alljoyn_interfacedescription_member *': 'POINTER(C.c_void_p)',
            'const uint8_t *': 'POINTER(C.c_uint8_t)',
            'uint8_t *': 'POINTER(C.c_uint8_t)',
            'const alljoyn_msgarg': 'C.c_void_p',
            'alljoyn_msgarg': 'C.c_void_p',
            'alljoyn_sessionopts': 'C.c_void_p',
            'alljoyn_aboutdatalistener': 'C.c_void_p',
            'alljoyn_msgarg*': 'POINTER(C.c_void_p)',
            'alljoyn_sessionid': 'C.c_uint32',
            'alljoyn_buslistener': 'C.c_void_p',
            'alljoyn_sessionport': 'C.c_uint16',
            'alljoyn_sessionport *': 'POINTER(C.c_uint16)',
            'const alljoyn_credentials': 'C.c_void_p',
            'const alljoyn_interfacedescription': 'C.c_void_p',
            'alljoyn_aboutlistener': 'C.c_void_p',
            'alljoyn_aboutproxy': 'C.c_void_p',
            'alljoyn_interfacedescription *': 'POINTER(C.c_void_p)',
            'alljoyn_interfacedescription_member': 'C.c_void_p',
            'alljoyn_interfacedescription_member*': 'POINTER(C.c_void_p)',
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
    
    
CallbackPtrTpPythonNameMap = {}
   
def underscore_to_camelcase(value):
    return ''.join([x.capitalize() for x in value.lower().split('_')])
    
def pass_function_name(name):
    name_parts = name.split('_')
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
    
    
def pass_function_pointer_typedef(line):
    # Probably could use re but I couldn't be bothered
    # typedef void (AJ_CALL * alljoyn_buslistener_bus_prop_changed_ptr)(const void* context, const char* prop_name, alljoyn_msgarg prop_value);
    #print line
    line = ''.join(line.split('*', 1)[1:])
    parts = line.split(')')
    name = parts[0]
    params = ''.join(parts[1:]).replace('(', '').replace(')', '').replace(';', '')
    parsed = {}
    parsed['name'] = name.strip()
    parsed['parameters'] = []
    
    for param in params.split(','):
        param = param.strip()
        parts = param.split(' ')
        parsed['parameters'].append(
                                  {
                                    'type': ' '.join(parts[0:-1]).strip(),
                                    'name': parts[-1].strip(),
                                  }
                                   )
    
    
    #print parsed
    return parsed
    
def process_function_pointer_typedef(typedefs, of):    
    for typedef_line in typedefs:
        
        if 'AJ_CALL *' in typedef_line:  # We have a function pointer typedef defined
            
            parsed = pass_function_pointer_typedef(typedef_line)
            
            try:
                python_name_start, python_name_end = pass_function_name(parsed['name'])
            except Exception as ex:
                print str(ex)
                raise
            
            parameter_types = []
            parameter_names = []
            parameter_ctypes = []
            
            #print func
            for param in parsed['parameters']:
                parameter_names.append(param['name'])
                parameter_types.append(param['type'])
                parameter_ctypes.append(type_map[param['type'].replace(' ', '').replace('const', '')])
            
            callbackName = python_name_start + python_name_end
            CallbackPtrTpPythonNameMap[parsed['name'].strip()] = callbackName.replace('Ptr', 'FuncType')
            type_map[parsed['name'].strip()] = 'POINTER(' + callbackName.replace('Ptr', 'FuncType') + ')'
            print "Adding", parsed['name'], CallbackPtrTpPythonNameMap[parsed['name']] 
            
            of.write(CallbackPtrTpPythonNameMap[parsed['name'].strip()]  + " = CallbackType(None, " + ', '.join(parameter_ctypes) + ') # ' + ' '.join(parameter_names) + '\n\n')


import pprint
   
def process_structures(cpp_header, of):

    for cls_name, cls in cpp_header.classes.items():
        python_name_start, python_name_end = pass_function_name(cls['name'])
        CallbackClassName = python_name_start + python_name_end
        type_map[cls['name']] = CallbackClassName
        type_map[cls['name'] + "*"] = "POINTER(" + CallbackClassName + ")"
        of.write("class " + CallbackClassName + "(C.Structure):\n")
        of.write("    _fields_ = [\n")
  
        for prop in cls['properties']['public']:
            of.write("            (\"%s\", POINTER(%s))," % (underscore_to_camelcase(prop['name']), CallbackPtrTpPythonNameMap[prop['type'].strip()]))
  
        of.write( "              ]\n\n")
  
    
def create_python_file(header, cpp_header, typedef_lines, of):
    f = open('class_template.txt', 'r')
    class_template = f.read()
    f.close()
    
    for name, value in cpp_header.typedefs.items():
        
        print "here", name, value
        
        if not 'AJ_CALL *' in value:  # We have a function pointer typedef defined allready dealt with
            of.write("#" + value) 
            of.write('\n')
    
    
    
    process_structures(cpp_header, of)
    
    process_function_pointer_typedef(typedef_lines, of)
    
    methods = []
    
    python_name_start = None
    # build class
    for func in cpp_header.functions:
        python_name_start, python_name_end = pass_function_name(func['name'])
        
        if 'DEPRECATED' in func['name']:
            continue

        parameter_types = []
        parameter_names = []
        parameter_ctypes = []
        
        for param in func['parameters']:
            parameter_names.append(param['name'])
            parameter_types.append(param['type'])
            
            
            param_name = param['type'].replace(' ', '').replace('const', '').strip()
            #if param_name not in type_map and param_name.endswith('_ptr'):
            #    type_map[type_map] = "POINTER(" + CallbackClassName + ")"
            
            try:
                parameter_ctypes.append(type_map[param_name])
            except:
                return False;
 
            list_of_params = zip(parameter_types, parameter_ctypes)

            return_type = func['rtnType'].replace('extern AJ_API', '').replace('AJ_CALL', '').strip()

            tmp = [func['name'], (return_type, type_map[return_type.replace(' ', '').replace('const', '')]), tuple(list_of_params)]
               
            methods.append(tuple(tmp)) 
        
        #__METHODS__
        
        
    #process_function_pointer_typedef(typedef_lines, of)
        
    if python_name_start == None:
        return True
        
    class_template_replaced = class_template.replace('__METHODS__', str(methods)) 
    class_template_replaced = class_template_replaced.replace('__NAME__', python_name_start)
    of.write(class_template_replaced + '\n\n')
    return True
        

    
headers = list(iglob('/home/glenn/devel/alljoyn-15.09.00a-src/alljoyn_c/inc/alljoyn_c/*.h'))
headers = list(iglob('./*.h'))
    
for header in headers:

    #print header
    
    try:
        dummy, filename = os.path.split(header)
        filename_withext, ext = os.path.splitext(filename)
        with open('./tmp/' + filename_withext + ".py", 'w') as of:

            typedef_lines = []
            
            with open(header, 'r') as f:
                file_contents = ', '.join([l.strip() for l in f.read().split(',\n')])
                
                for line in file_contents.split('\n'):
                    if '(AJ_CALL *' in line:
                        typedef_lines.append(line.strip())

            of.write("import types\n")
            of.write("import ctypes as C\n")
            of.write("from ctypes import POINTER\n")
            of.write("from enum import Enum, unique\n\n")
            
            cpp_header = CppHeaderParser.CppHeader(header)
            if not create_python_file(header, cpp_header, typedef_lines, of):
                headers.append(header)
                
    except CppHeaderParser.CppParseError as e:
        print(e)
        print header
        sys.exit(1)
