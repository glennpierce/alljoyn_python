#!/usr/bin/env python

import sys, json, re
from itertools import groupby
import ctypes as C
from ctypes import POINTER
import StringIO
import pprint

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
            'sessionportlistener' : 'SessionPortListener',
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
           
type_map = {'char':'C.c_byte',
            'char*':'C.c_char_p',
            'void*':'C.c_void_p',
            'bool':'C.c_ubyte',                                  
            'size_t':'C.c_size_t',
            'int':'C.c_int',
            'uint8_t':'C.c_ubyte',    
            'int16_t':'C.c_short',    
            'uint16_t':'C.c_ushort',    
            'int32_t':'C.c_int',    
            'uint32_t':'C.c_uint',   
            'int64_t':'C.c_longlong',        
            'uint64_t':'C.c_ulonglong',   
            'double':'C.c_double',           
            'QCC_BOOL':'C.c_int',   
            'QStatus':'C.c_uint',    
            'QCC_BOOL*':'POINTER(C.c_int)',
            'int*':'POINTER(C.c_int)', 
            'int**':'POINTER(POINTER(C.c_int))', 
            'uint8_t*':'POINTER(C.c_ubyte)',          
            'uint8_t**':'POINTER(C.c_ubyte)',            
            'int16_t*':'POINTER(C.c_short)', 
            'uint16_t*':'POINTER(C.c_ushort)', 
            'int32_t*':'POINTER(C.c_int)', 
            'uint32_t*':'POINTER(C.c_uint)', 
            'int64_t*':'POINTER(C.c_longlong)', 
            'uint64_t*':'POINTER(C.c_ulonglong)',     
            'double*':'POINTER(C.c_double)', 
            'char**':'POINTER(C.c_char_p)', 
            'size_t*':'POINTER(C.c_size_t)', 
            'alljoyn_messagetype':'C.c_void_p',
            'alljoyn_transportmask':'C.c_ushort',
            'alljoyn_proxybusobject':'C.c_void_p',
            'alljoyn_proxybusobject*':'POINTER(C.c_void_p)',
            'alljoyn_aboutdata':'C.c_void_p',
            'alljoyn_aboutdata*':'POINTER(C.c_void_p)',
            'alljoyn_abouticon':'C.c_void_p',
            'alljoyn_abouticon*':'POINTER(C.c_void_p)',
            'alljoyn_abouticonproxy':'C.c_void_p',
            'alljoyn_abouticonproxy*':'POINTER(C.c_void_p)',
            'alljoyn_aboutobjectdescription':'C.c_void_p',
            'alljoyn_aboutobjectdescription*':'POINTER(C.c_void_p)',
            'alljoyn_aboutobj':'C.c_void_p',
            'alljoyn_aboutobj*':'POINTER(C.c_void_p)',
            'alljoyn_busattachment':'C.c_void_p',
            'alljoyn_busattachment*':'POINTER(C.c_void_p)',
            'alljoyn_authlistener':'C.c_void_p',
            'alljoyn_authlistener*':'POINTER(C.c_void_p)',
            'alljoyn_credentials':'C.c_void_p',
            'alljoyn_credentials*':'POINTER(C.c_void_p)',
            'alljoyn_autopinger':'C.c_void_p',
            'alljoyn_autopinger*':'POINTER(C.c_void_p)',
            'alljoyn_busobject':'C.c_void_p',
            'alljoyn_busobject*':'POINTER(C.c_void_p)',
            'alljoyn_interfacedescription':'C.c_void_p',
            'alljoyn_interfacedescription*':'POINTER(C.c_void_p)',
            'alljoyn_message':'C.c_void_p',
            'alljoyn_message*':'POINTER(C.c_void_p)',
            'alljoyn_msgarg':'C.c_void_p',
            'alljoyn_sessionportlistener':'C.c_void_p',
            'alljoyn_msgarg*':'POINTER(C.c_void_p)',
            'alljoyn_sessionlostreason': 'C.c_uint',
            'const alljoyn_interfacedescription_member':'C.c_void_p',
            'alljoyn_interfacedescription_member *':'POINTER(C.c_void_p)',
            'const uint8_t *':'POINTER(C.c_ubyte)',
            'uint8_t *':'POINTER(C.c_ubyte)',
            'interfacedescription_securitypolicy': 'C.uint',
            'alljoyn_interfacedescription_securitypolicy': 'C.uint',
            'const alljoyn_msgarg':'C.c_void_p',
            'alljoyn_typeid': 'C.c_uint',
            'alljoyn_msgarg':'C.c_void_p',
            'alljoyn_sessionopts':'C.c_void_p',
            'alljoyn_aboutdatalistener':'C.c_void_p',
            'alljoyn_msgarg*':'POINTER(C.c_void_p)',
            'alljoyn_sessionid':'C.c_uint',
            'alljoyn_buslistener':'C.c_void_p',
            'alljoyn_sessionport':'C.c_ushort',
            'alljoyn_sessionport *':'POINTER(C.c_ushort)',
            'const alljoyn_credentials':'C.c_void_p',
            'const alljoyn_interfacedescription':'C.c_void_p',
            'alljoyn_aboutlistener':'C.c_void_p',
            'alljoyn_aboutproxy':'C.c_void_p',
            'alljoyn_interfacedescription *':'POINTER(C.c_void_p)',
            'alljoyn_interfacedescription_member':'C.c_void_p',
            'alljoyn_interfacedescription_member*':'POINTER(C.c_void_p)',
            'alljoyn_pinglistener':'C.c_void_p',
            'alljoyn_sessionlistener':'C.c_void_p',
            'const alljoyn_sessionopts':'C.c_void_p',
            'alljoyn_observer':'C.c_void_p',
            'alljoyn_observerlistener':'C.c_void_p',
            'alljoyn_keystorelistener':'C.c_void_p',
            'void': None,  
            'const alljoyn_busattachment':'C.c_void_p',
            'alljoyn_keystore':'C.c_void_p',
            }
            
                       
file_objects = {'enums':[],
                'typefeds': [],
                'structs': [],
                'functions': []
               }
           
CallbackPtrToPythonNameMap = {}

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
    
    #print "word", words
    
    end = ''.join([x.capitalize() for x in words[0]])
    
    return python_name, end
    
           

def process_file(filepath, of):
    file_description = json.loads(get_json(filepath))
 
    f = open('class_template.txt', 'r')
    class_template = f.read()
    f.close()
 
    import_string = "import sys, types\n"
    import_string += "import ctypes as C\n"
    import_string += "from ctypes import POINTER\n"
    import_string += "from enum import Enum, unique\n"
    import_string += "from . import AllJoynMeta, AllJoynObject\n"
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
    
    
    function_pointers_string = ""
    # function_pointers
    # BusListenerRegisteredFuncType = CallbackType(None, C.c_void_p, C.c_void_p)                 # const void* context, alljoyn_busattachment bus
    # alljoyn_busattachment_joinsessioncb_ptr
   
    
    for function_pointer_name, function_pointer in file_description['function_pointers'].items():
            #function_pointer_name = function_pointer_name.replace('ptr', 'functype')
            python_name_start, python_name_end = spelling_to_python_name(function_pointer_name)
            callbackName = python_name_start + python_name_end
            callbackName = callbackName.replace('PTR', 'FuncType')
            CallbackPtrToPythonNameMap[function_pointer_name] = callbackName
            type_map[function_pointer_name.strip()] = 'POINTER(' + callbackName + ')'
            
            #print function_pointer_name,  type_map[function_pointer_name.strip()]
            
            arg_names = [a[2] for a in function_pointer]
            arg_types = [a[0] for a in function_pointer]
            carg_types = [type_map[a.replace('const', '').replace(' ', '')] for a in arg_types]
            
            #print "Adding", type_map[a.replace('const', '').replace(' ', ''), CallbackPtrTpPythonNameMap[parsed['name']] 
            function_pointers_string += callbackName  + " = CallbackType(None, " + ', '.join(carg_types) + ') # ' + ' '.join(arg_names) + '\n'
           
    class_template = class_template.replace('__FUNCTION_POINTER_TYPES__', function_pointers_string)
    
    
    #_fields_ = [("AboutListenerAnnounced",
    #                POINTER(AboutListenerAnnouncedFuncType))
    #           ]
    struct_string = ""
    for struct_name, fields in file_description['structs'].items():
        python_name_start, python_name_end = spelling_to_python_name(struct_name)
        CallbackClassName = python_name_start + python_name_end
        type_map[struct_name] = CallbackClassName   # Add the name to the class map
        type_map[struct_name + "*"] = "POINTER(" + CallbackClassName + ")"
        struct_string += "class " + CallbackClassName + "(C.Structure):\n"
        struct_string += "    _fields_ = [\n"

        for field in fields:
            field_type = field[0]
            field_name = field[1]
            real_field_type = CallbackPtrToPythonNameMap.get(field_type,field_type+"unknown_fix")
            struct_string += "                (\"%s\", POINTER(%s))," % (field_name, real_field_type)
  
        struct_string += "                ]\n\n"
 
    class_template = class_template.replace('__STRUCTS__', struct_string)
    
            
    methods = {}
    
    done_name = False
    
    # functions
    for function in file_description['functions']:
        functionname = function['name']

        if 'deprecated' in functionname.lower() or 'router' in functionname.lower():
            continue
    
        python_name_start, python_name_end = spelling_to_python_name(functionname)

        if not done_name:
            class_template = class_template.replace('__NAME__', python_name_start)
            done_name = True
        
        parameter_types = []
        parameter_names = []
        parameter_ctypes = []
        
        for param in function['params']:
            parameter_names.append(param['name'])
            parameter_types.append(param['type'])
            
            param_name = param['type'].replace(' ', '').replace('const', '').strip()

            try:
                param_ctype = None
                #if '_ptr' in param_name:  # callback pointer. fill will junk and manually correct
                #    param_ctype = "POINTER(CallbackFuncType)"
                #else:
                param_ctype = type_map[param_name]
                parameter_ctypes.append(param_ctype)
            except Exception as ex:
                print str(ex)
                raise
            
        list_of_params = zip(parameter_types, parameter_ctypes)

        ctype_return_type = type_map[function['return_type'].replace('const', '').replace(' ', '').strip()]

        tmp = [functionname, (function['return_type'], ctype_return_type), 
               tuple(list_of_params)]
               
        methods[python_name_end] = (tuple(tmp)) 
    
    
    methods_string = pprint.pformat(methods)
 
    class_template = class_template.replace('__METHODS__', str(methods_string))
    
    # Wrappers
    
    wrapper_string = ""
    # functions
    for function in file_description['functions']:
        functionname = function['name']

        if 'deprecated' in functionname.lower() or 'router' in functionname.lower():
            continue
    
        python_name_start, python_name_end = spelling_to_python_name(functionname)
        parameter_types = []
        parameter_names = []
        
        for param in function['params']:
            parameter_names.append(param['name'])
            parameter_types.append(param['type'])
        
        parameter_names = parameter_names[1:]
        parameter_types = parameter_types[1:]
        
        if parameter_names:
            wrapper_string += "def %s(self, %s):\n    " % (python_name_end, ','.join(parameter_names))
            wrapper_string += "    return self._" + python_name_end + "(self.handle," + ','.join(parameter_names) + ") # " + ','.join(parameter_types) + '\n\n    '
        else:
            wrapper_string += "def %s(self):\n    " % (python_name_end,)
            wrapper_string += "    return self._" + python_name_end + "(self.handle)\n\n    "
        
    
    class_template = class_template.replace('__WRAPPERS__', wrapper_string)
    
    of.write(class_template)
    
if __name__ == '__main__':
    process_file(sys.argv[1], sys.stdout)

