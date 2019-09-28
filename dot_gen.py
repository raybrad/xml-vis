from graphviz import Digraph

def genDAG(dot,root):
    if isinstance(root, str):
        return dot 
    for node, child in root.items():
        dot.node(node)  
        if isinstance(child,dict):
            for k,v in child.items():
                dot.edge(node,k)
                dot.node(k)  
                dot.edge(k,v)
                dot=genDAG(dot,v)
        else:
            dot.node(child)  
            dot.edge(node,child)
    
    return dot 

def genDAG2(dot,node,child):
    dot.node(node)  
    #s.attr(rank = 'same')                                                                                                                                                                   
    if isinstance(child, str):
        dot.node(child)  
        dot.edge(node,child)
        return dot 
    for subnode, subchild in child.items():
        dot.node(subnode)  
        dot.edge(node,subnode)
        dot=genDAG2(dot,subnode,subchild)
    return dot 

def dict2dag(dag):
    dot = Digraph(comment='DAG')
    dot=genDAG2(dot,'section_inspect',dag['section_inspect'])
    # print(dot.source)  
    # dot.render('dag.gv', view=True)  # doctest: +SKIP

    return



