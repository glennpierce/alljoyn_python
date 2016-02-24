import os, os.path, re
import CppHeaderParser
from glob import glob, iglob

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


def underscore_to_camelcase(value):
    return ''.join([x.capitalize() for x in value.lower().split('_')])
    
    
    
def create_python_file(cpp_header):
    print "class Constants(object):"
    for name, value in cpp_header.typedefs.items():
        print "    #%s=%s" % (name,value)
    print

    for d in cpp_header.defines:
        print '    #', d
    
    print 
    
    # build class
    for func in cppHeader.functions:
        print "class __NAME__(object):"
        
        print "    __metaclass__ = AllJoynMeta"
        
        def __init__(self, defaultLanguage, arg=None):
            if not arg:
                self.handle = self.AboutdataCreate(defaultLanguage)
            else:
                self.handle = self.AboutdataCreateFull(arg, defaultLanguage)
        
        def __del__(self):
            self.AboutdataDestroy(self.handle)
        
    
for header in iglob('/home/glenn/devel/alljoyn-15.09.00a-src/alljoyn_c/inc/alljoyn_c/*.h'):

    try:
        print "processing", header
        cpp_header = CppHeaderParser.CppHeader(header)
        create_python_file(cpp_header)
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
