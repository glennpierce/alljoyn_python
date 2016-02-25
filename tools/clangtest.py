import clang.cindex
import sys
from collections import defaultdict

def get_ts(source_path):
    index = clang.cindex.Index.create()
    return index.parse(source_path, ["-xc"])


doc = None
typedefs = []
enums = defaultdict(list)
structs = []
functions = []


"""
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

def qualifiers(t):
    '''set of qualifiers of a type'''
    q = set()

    if t.is_const_qualified(): q.add('const')
    if t.is_volatile_qualified(): q.add('volatile')
    if t.is_restrict_qualified(): q.add('restrict')
    #if t.is_function_variadic(): q.add('variadic')
    return q
    
def retrieve_type(t):
    '''retrieve actual type'''
    if t.get_pointee().kind != clang.cindex.TypeKind.INVALID:
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
        parents = semantic_parents(cursor)
        if cursor.displayname != "":
            return ' '.join(qualifiers(t)) + " " + "::".join(parents + [cursor.displayname])
        else:
            return ' '.join(qualifiers(t)) + " " + "::".join(parents + [str(t.kind).split(".")[-1]])
"""


def get_parent_with_type(node, type):
    while node and node.kind != type:
        node = node.parent_node
    return node

def print_node(node, parent_node):
    node.parent_node = parent_node
    
    #print node.spelling

    #if node.kind == clang.cindex.CursorKind.TRANSLATION_UNIT:
    #    doc = node
    #el
    
    if node.kind == clang.cindex.CursorKind.INTEGER_LITERAL:
        
        typedef_node = get_parent_with_type(node, clang.cindex.CursorKind.TYPEDEF_DECL)
        if typedef_node:
            container = enums[typedef_node.spelling]
            container.append(node.parent_node.spelling + " = " + node.get_tokens().next().spelling)
    elif node.kind == clang.cindex.CursorKind.TYPEDEF_DECL:
        print node.spelling, node.location
        pass
    elif node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        #print node.spelling, node.location,"\n"   
        pass
    
        #if parent_node and parent_node.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL: # and parent_node.parent_node and parent_node.parent_node.kind == clang.cindex.CursorKind.TYPEDEF_DECL:
        #    print parent_node.spelling, parent_node.location
        #    print node.type.kind, node.get_tokens() #.next().spelling
        #pass
        #print node.type.kind, node.get_tokens().next().spelling
    #elif node.kind == clang.cindex.CursorKind.ENUM_DECL:
    #    if parent_node and parent_node.kind == clang.cindex.CursorKind.TYPEDEF_DECL:
    #        enums.append(node)
    #    #print node.type.kind, node.get_tokens().next().spelling
    #elif node.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL:
    #    if parent_node and parent_node.kind == clang.cindex.CursorKind.ENUM_DECL:
    #        print "here", node.
    #        #enums.append(node)
    #    #print node.type.kind, node.get_tokens().next().spelling
    elif node.kind == clang.cindex.CursorKind.STRUCT_DECL:
        #print "what", node, retrieve_type(node.type.get_canonical()), "\n\n"
        structs.append(node)
        
    [print_node(n, node) for n in node.get_children()]

ts = get_ts(sys.argv[1])
[print_node(n, None) for n in ts.cursor.get_children()]




print enums

#print doc
#print [(e.spelling, e.location, e.location.column) for e in enums]
#print [(s.spelling, s.location, s.location.column) for s in structs]


#print [(s.spelling, s.location, s.location.column) for s in structs]
