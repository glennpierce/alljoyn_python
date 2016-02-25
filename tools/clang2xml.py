#!/usr/bin/env python

import sys
import clang.cindex
import clang.enumerations
import hashlib

           
def no_system_includes(cursor, level):
    '''filter predicate for show_ast: filter out verbose stuff from system include files'''
    return (level!= 1) or (cursor.location.file is not None and not cursor.location.file.name.startswith('/usr/include'))
 

# A function show(level, *args) would have been simpler but less fun
# and you'd need a separate parameter for the AST walkers if you want it to be exchangeable.
class Level(int):
    '''represent currently visited level of a tree'''
    def show(self, *args):
        '''pretty print an indented line'''
        print '\t'*self + ' '.join(map(str, args))
    def __add__(self, inc):
        '''increase level'''
        return Level(super(Level, self).__add__(inc))
    def open(self, type, location, **kwargs):
        '''Opens an XML tag'''
        attributes = {
            "file" : location.file,
            "line" : location.line,
            "column" : location.column,
            }
        attributes.update(kwargs)
        print '\t'*self + '<%s %s>' % (type, ' '.join(['%s="%s"' % (key, value) for key, value in attributes.items()]))

        attributes['type'] = type
        #print attributes

    def close(self, type):
        '''Closes an XML tag'''
        print '\t'*self + '</%s>' % type
    def openclose(self, type, **kwargs):
        ret = self.open(type, **kwargs)
        self.close(type)
        return ret

def is_valid_type(t):
    '''used to check if a cursor has a type'''
    return t.kind != clang.cindex.TypeKind.INVALID
    
def qualifiers(t):
    '''set of qualifiers of a type'''
    q = set()

    if t.is_const_qualified(): q.add('const')
    if t.is_volatile_qualified(): q.add('volatile')
    if t.is_restrict_qualified(): q.add('restrict')
    #if t.is_function_variadic(): q.add('variadic')
    return q
 
def is_definition(cursor):
    ''' Returns true if the cursor is the definition '''
    return (
        (cursor.is_definition() and not cursor.kind in (
   #         clang.cindex.CursorKind.CXX_ACCESS_SPEC_DECL,
   #         clang.cindex.CursorKind.TEMPLATE_TYPE_PARAMETER,
            clang.cindex.CursorKind.UNEXPOSED_DECL,
            )) or
        cursor.kind in (
            clang.cindex.CursorKind.FUNCTION_DECL,
    #        clang.cindex.CursorKind.CXX_METHOD,
    #        clang.cindex.CursorKind.FUNCTION_TEMPLATE,
            ))

def is_named_scope(cursor):
    ''' Returns true if the cursor is a name declaration   '''
    return cursor.kind in (
        clang.cindex.CursorKind.STRUCT_DECL,
        clang.cindex.CursorKind.UNION_DECL,
        clang.cindex.CursorKind.ENUM_DECL,
        clang.cindex.CursorKind.INTEGER_LITERAL,
        )

def semantic_parents(cursor):
    import collections
    p = collections.deque()
    c = cursor.semantic_parent
    while c and is_named_scope(c):
        p.appendleft(c.displayname)
        c = c.semantic_parent
    return list(p)

def retrieve_type(t):
    
    #print "t", vars(t['_tu'])
    
    '''retrieve actual type'''
    if is_valid_type(t.get_pointee()):
        
        
        
        pointee = ""
        if t.kind == clang.cindex.TypeKind.POINTER:
            pointee = "*"
        if t.kind == clang.cindex.TypeKind.LVALUEREFERENCE:
            pointee = "&"
        if t.kind == clang.cindex.TypeKind.RVALUEREFERENCE:
            pointee = "&&"
        return retrieve_type(t.get_pointee()) + pointee + ' '.join(qualifiers(t))
    else:
        cursor = t.get_declaration()
        
        print "t.kind", t.kind
        
        if t.kind == clang.cindex.TypeKind.INT:
            print "\n\n\n\n-------------------------"
            print t #.get_tokens().next().spelling
            print dir(t)
            
            print "result", t.get_result()
            #'data', 'element_count', 'element_type', 'from_result', 'get_align', 'get_array_element_type', 'get_array_size', 'get_canonical', 'get_class_type', 'get_declaration', 'get_offset', 'get_pointee', 'get_ref_qualifier', 'get_result', 'get_size', 'is_const_qualified', 'is_function_variadic', 'is_pod', 'is_restrict_qualified', 'is_volatile_qualified', 'kind', 'spelling', 'translation_unit']
#result <clang.cindex.Type object at 0x7fe6cae6bf80>

            print "\n\n-----------------------------"
            
        parents = semantic_parents(cursor)
        if cursor.displayname != "":
            return ' '.join(qualifiers(t)) + " " + "::".join(parents + [cursor.displayname])
        else:
            return ' '.join(qualifiers(t)) + " " + "::".join(parents + [str(t.kind).split(".")[-1]])


def show_ast(cursor, filter_pred=None, level=Level(), inherited_attributes={}):
    '''pretty print cursor AST'''
    if filter_pred(cursor, level):

        #print "-------------------------"
        #print vars(cursor)
        #print "-------------------------"

        type = str(cursor.kind).split(".")[-1].strip()
        level1 = level+1

        level.open(type, spelling=cursor.spelling, displayname=cursor.displayname, location=cursor.location, **inherited_attributes)
        if is_valid_type(cursor.type):
            level1.openclose("type", displayname=retrieve_type(cursor.type.get_canonical()), location=cursor.location)
            
        attributes = {}
        for c in cursor.get_children():
            show_ast(c, filter_pred, level1, attributes)

        #print attributes

        level.close(type)
 
if __name__ == '__main__':
    index = clang.cindex.Index.create()
    tu = index.parse(sys.argv[1], ["-xc"])
    show_ast(tu.cursor, no_system_includes)

