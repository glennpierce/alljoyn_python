#!/usr/bin/env python

import sys, json, re
from itertools import groupby

from clang2json import get_json

def viterbi_segment(text):
    probs, lasts = [1.0], [0]
    for i in range(1, len(text) + 1):
        prob_k, k = max((probs[j] * word_prob(text[j:i]), j)
                        for j in range(max(0, i - max_word_length), i))
        probs.append(prob_k)
        lasts.append(k)
    words = []
    i = len(text)
    while 0 < i:
        words.append(text[lasts[i]:i])
        i = lasts[i]
    words.reverse()
    return words, probs[-1]

def word_prob(word): return dictionary.get(word, 0) / total
def words(text): return re.findall('[a-z]+', text.lower()) 
dictionary = dict((w, len(list(ws)))
                  for w, ws in groupby(sorted(words(open('big.txt').read()))))
max_word_length = max(map(len, dictionary))
total = float(sum(dictionary.values()))

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
            'messagetype': 'MessageType',
            'aboutlistener': 'AboutListener',
            'alljoyn': 'AllJoyn',
            'pinglistener': 'PingListener',
            'authlistenerasync': 'AuthListenerAsync',
            'credentials': 'Credentials',
            'unity': 'Unity',
            'about': 'About',
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
            
                       
file_objects = {'enums':[],
                'typefeds': [],
                'structs': [],
                'functions': []
               }
           
def underscore_to_camelcase(value):
    return ''.join([x.capitalize() for x in value.lower().split('_')])
    
def spelling_to_python_name(spelling):
    name_parts = spelling.split('_')
    name_end = []
    
    if 'DEPRECATED' in name_parts:
        raise

    try:
        if len(name_parts) == 2:
            python_name = name_map[name_parts[0]]
            name_end = ''.join(name_parts[1:])
        elif len(name_parts) >= 3:
            python_name = name_map[name_parts[1]]
            name_end = ''.join(name_parts[2:])
    except KeyError as ex:
        print str(ex)
        print spelling
        print name_parts
        raise
    

    words = viterbi_segment(name_end)  # splits srings by words
    end = ''.join([x.capitalize() for x in words[0]])
    
    return python_name, end
    
           

def process_file(filepath, of):
    file_description = json.loads(get_json(filepath))
 
    f = open('class_template.txt', 'r')
    class_template = f.read()
    f.close()
 
    import_string = "import types\n"
    import_string += "import ctypes as C\n"
    import_string += "from ctypes import POINTER\n"
    import_string += "from enum import Enum, unique\n"
    import_string += "from AllJoyn import AllJoynObject\n"
    import_string += "# Wrapper for file %s\n\n" % (file_description['doc'],)
    
    class_template = class_template.replace('__IMPORTS__', import_string)
    
    define_string = ""
    for define in file_description['defines']:
        define_string += "%s\n" % (define,)
        
    class_template = class_template.replace('__DEFINES__', define_string)
        
    variables_string = ""
    for type, name, value in file_description['variables']:
        variables_string += "%s = %s   # %s\n" % (name, value, type)
        
    class_template = class_template.replace('__VARIABLES__', define_string)
    
    enum_string = ""
    for enum_name, enum in file_description['enums'].items():
        enum_string += "@unique\n"
        enum_string += "class %s(Enum):\n" % (spelling_to_python_name(enum_name)[1],)
        for enum_constant in enum:
            enum_string += "    %s = %s\n" % (enum_constant[0], enum_constant[1])
 
    class_template = class_template.replace('__ENUMS__', enum_string)
    
    typedef_string = "# Typedefs\n"
    for type, name in file_description['typedefs']:
        typedef_string += "# %s %s\n" % (type, name)
        
    class_template = class_template.replace('__TYPEDEFS__', typedef_string)
    
    struct_string = ""
    for struct_name, struct in file_description['structs'].items():
        python_name_start, python_name_end = spelling_to_python_name(cls['name'])
        CallbackClassName = python_name_start + python_name_end
        type_map[struct_name] = CallbackClassName   # Add the name to the class map
        type_map[struct_name + "*"] = "POINTER(" + CallbackClassName + ")"
        struct_string += "class " + CallbackClassName + "(C.Structure):\n"
        struct_string += "    _fields_ = [\n"
  
        #for prop in cls['properties']['public']:
        #    of.write("            (\"%s\", POINTER(%s))," % (underscore_to_camelcase(prop['name']), CallbackPtrTpPythonNameMap[prop['type'].strip()]))
  
        #of.write( "              ]\n\n")
 
    class_template = class_template.replace('__STRUCTS__', enum_string)
    
    # function_pointers
    #print func
            #for param in parsed['parameters']:
                #parameter_names.append(param['name'])
                #parameter_types.append(param['type'])
                #parameter_ctypes.append(type_map[param['type'].replace(' ', '').replace('const', '')])
            
            #callbackName = python_name_start + python_name_end
            #CallbackPtrTpPythonNameMap[parsed['name'].strip()] = callbackName.replace('Ptr', 'FuncType')
            #type_map[parsed['name'].strip()] = 'POINTER(' + callbackName.replace('Ptr', 'FuncType') + ')'
            #print "Adding", parsed['name'], CallbackPtrTpPythonNameMap[parsed['name']] 
            
 
    
    methods = []
    
    # functions
    for function in file_description['functions']:
        functionname = function['name']
        
        python_name_start, python_name_end = spelling_to_python_name(functionname)

        if 'DEPRECATED' in functionname:
            continue
    
        parameter_types = []
        parameter_names = []
        parameter_ctypes = []
        
        for param in function['params']:
            parameter_names.append(param['name'])
            parameter_types.append(param['type'])
            
            param_name = param['type'].replace(' ', '').replace('const', '').strip()

            try:
                parameter_ctypes.append(type_map[param_name])
            except Exception as ex:
                print str(ex)
                raise
 
            list_of_params = zip(parameter_types, parameter_ctypes)

            tmp = [func['name'], (function['return_type'], type_map[return_type.replace(' ', '').replace('const', '')]), tuple(list_of_params)]
               
            methods.append(tuple(tmp)) 
    
 
    class_template = class_template.replace('__METHODS__', str(methods))
    
    of.write(class_template)
    
if __name__ == '__main__':
    process_file(sys.argv[1], sys.stdout)

