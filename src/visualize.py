from mcst import MCST_Node

def generate_gjgf(node:MCST_Node, levels, parent_id=None, graph:dict=None):
    if graph == None:
        graph = {
            'graph': {
                'directed':False,
                'nodes':{},
                'edges':[],
            }
        }
    
    id = len(graph['graph']['nodes'])
    color = '#ff8888' if node.player == 1 else '#8888ff' if node.player == -1 else '#88ff88'
    graph['graph']['nodes'][id] = {'metadata': {'label': get_meta(node), 'color':color}}
    if parent_id != None:
        graph['graph']['edges'].append({'source': parent_id, 'target':id, 'metadata':{'move': node.move}})
    
    levels -= 1
    if levels > 0:
        for child in node.children:
            graph = generate_gjgf(child, levels, id, graph)
        
    return graph
    
    
    
def get_meta(node:MCST_Node) -> str:
       return f'w: {node.w}\nn: {node.n}\nw/n: {node.w/node.n if node.n > 0 else -1}\n UCT: {node.UCT():.2f}'