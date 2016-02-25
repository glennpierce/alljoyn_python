#!/usr/bin/python

import sys

from xml.dom import minidom

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
           
           
file_objects = {'enums':[],
                'typefeds': [],
                'structs': [],
                'functions': []
               }
           
def underscore_to_camelcase(value):
    return ''.join([x.capitalize() for x in value.lower().split('_')])
    
def spelling_to_python_name(spelling):
    
    print spelling
    
    name_parts = spelling.split('_')
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
        print spelling
        print name_parts
        raise
    
    return python_name, underscore_to_camelcase('_'.join(name_end))
    

doc = minidom.parse(sys.argv[1])

name = doc.getElementsByTagName("TRANSLATION_UNIT")[0]

print "import types"
print "import ctypes as C"
print "from ctypes import POINTER"
print "from enum import Enum, unique\n\n"
            
print "# Wrapper for file", name.getAttribute("spelling")

def getParentTypedefNode(node):
    while node.parentNode:
        node = node.parentNode
        if node.nodeName == "TYPEDEF_DECL":
            return node


# doc.getElementsByTagName returns NodeList
enums = doc.getElementsByTagName("ENUM_DECL")

for enum in enums:
    typedefNode = getParentTypedefNode(enum)
    
    if typedefNode != None:
        typedef_spelling = typedefNode.getAttribute("spelling")
        python_spelling = spelling_to_python_name(typedef_spelling)[0]
        print "@unique"
        print "class " + python_spelling + "(Enum):"
    
    constants = enum.getElementsByTagName("ENUM_CONSTANT_DECL")
    
    for constant in constants:
        print "    " + constant.
    
    
    #print vars(enum.parentNode)
    #if enum.parentNode.nodeName == "TRANSLATION_UNIT":
    #    continue
    #enum_typedef = enum.parentNode #doc.getElementsByTagName("parentNode")
    #print vars(enum_typedef)
    
    #print vars(enum)
#staffs = doc.getElementsByTagName("staff")
#for staff in staffs:
 #       sid = staff.getAttribute("id")
 #       nickname = staff.getElementsByTagName("nickname")[0]
 #       salary = staff.getElementsByTagName("salary")[0]
 #       print("id:%s, nickname:%s, salary:%s" %
 #             (sid, nickname.firstChild.data, salary.firstChild.data))
              
        
