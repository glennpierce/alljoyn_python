#!/usr/bin/python

import shutil
import clang.cindex
import sys, os
import fileinput
import json

from collections import defaultdict

def get_ts(source_path):
    index = clang.cindex.Index.create()
    return index.parse(source_path, ["-xc", "-ansi"])


doc = None
typedefs = defaultdict(list)
enums = defaultdict(list)
structs = defaultdict(list)
functions = defaultdict(list)


def get_parent_with_type(node, type):
    while node and node.kind != type:
        node = node.parent_node
    return node

def print_node(node, parent_node):
    node.parent_node = parent_node
    
    #underlying_typedef_type
    
    #if node.kind == clang.cindex.CursorKind.INTEGER_LITERAL:
        ## Could maybe use enum_value and enum_type. I did not know about it when I wrote below
        #typedef_node = get_parent_with_type(node, clang.cindex.CursorKind.TYPEDEF_DECL)
        #if typedef_node:
            #container = enums[typedef_node.spelling]
            #container.append({'enum_name' : node.parent_node.spelling,
                              #'enum_type' : node.semantic_parent.enum_type.spelling,
                              #'enum_value' : node.enum_value})

    if node.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
        # Could maybe use enum_value and enum_type. I did not know about it when I wrote below
        typedef_node = get_parent_with_type(node, clang.cindex.CursorKind.TYPEDEF_DECL)
        if typedef_node:
            container = enums[typedef_node.spelling]
            container.append(node.enum_value)

    #if node.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
    #    if node.semantic_parent.kind == clang.cindex.CursorKind.ENUM_DECL:
    #        container = enums[node.semantic_parent.spelling]
    #        container.append({'enum_name' : node.parent_node.spelling,
    #                          'enum_type' : node.semantic_parent.enum_type.spelling,
    #                          'enum_value' : node.enum_value})


    elif node.kind == clang.cindex.CursorKind.FIELD_DECL:
        typedef_node = get_parent_with_type(node, clang.cindex.CursorKind.TYPEDEF_DECL)
        if typedef_node:
            container = structs[typedef_node.spelling]
            container.append((node.get_tokens().next().spelling, node.spelling))
 
    elif node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        container = functions[node.spelling]
        
        #print node.type.get_result().spelling
        #print node.type.get_ref_qualifier
        params = [(arg.type.spelling, arg.spelling) for arg in node.get_arguments()]
        
        variadic = False
        
        if node.type.kind == clang.cindex.TypeKind.FUNCTIONPROTO:
            variadic = node.type.is_function_variadic()
        
        #print [n.spelling for n in node.get_tokens()]
        container.append({'displayname':node.displayname, 'return_type': node.get_tokens().next().spelling,
                          'params':params, 'is_variadic':variadic})
        
    elif node.kind == clang.cindex.CursorKind.PARM_DECL:
        typedef_node = get_parent_with_type(node, clang.cindex.CursorKind.TYPEDEF_DECL)
       
        if typedef_node:
            container = typedefs[typedef_node.spelling]
            container.append((node.type.spelling, str(node.type.kind).split(".")[1], node.spelling))
    else:
        #print node.kind
        #print node.spelling, node.location
        pass

   
    [print_node(n, node) for n in node.get_children()]


if __name__ == "__main__":
    
    filepath = sys.argv[1]
    junk, filename = os.path.split(filepath)
    tmp_filename = '/tmp/' + filename
    
    # Preprocess file remove AJ_CALL, AJ_API, extern
    with open(filepath, 'r') as f:
        filedata = f.read()
        filedata = filedata.replace('AJ_CALL', '')
        filedata = filedata.replace('AJ_API', '')
        filedata = filedata.replace('extern', '')

        # Write the file out again
        with open(tmp_filename, 'w') as fo:
            fo.write(filedata)

    ts = get_ts(tmp_filename)
    
    [print_node(n, None) for n in ts.cursor.get_children()]

    print json.dumps({
            'doc': os.path.split(ts.spelling)[1],
            'enums': dict(enums),
            'structs': dict(structs),
            'typedefs': dict(typedefs),
            'functions': dict(functions)
          }, indent=4)
    
