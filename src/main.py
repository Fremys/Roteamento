import pandas as pd 
import networkx as nx
import matplotlib.pyplot as plt
import random

class Route:
    graph = nx.cubical_graph()
            
    def __init__(self, graph):
        self.graph = graph
    
    def printGraph(self):
        nx.draw(self.graph, with_labels=True, pos=nx.circular_layout(self.graph), node_color='r', edge_color='b', font_weight='bold')
        plt.show()
    

def build_example_route():
    #definir dados
    exampleGraph = nx.Graph() 
    listNode = ["A", "B", "C", "D", "E", "F"]
    listEdge = build_edges_with_center_node(listNode, "D")
    
    exampleGraph.add_nodes_from(listNode) #adicionando os nos ao grafo
    exampleGraph.add_weighted_edges_from(listEdge) #adicionando as arestas ao grafo 
    
    return exampleGraph
    
    
def build_edges_with_center_node(listNode, centerNode):
    
    listEdgeResult = []
    
    for nodeOrigin in listNode:
        for nodeDest in listNode:
            weight = random.randint(1, 20)
            if(nodeDest != nodeOrigin): #nao construir rotas para o mesmo lugar
                if(nodeOrigin == centerNode):
                    listEdgeResult.append((nodeOrigin, nodeDest, weight)) #construir rota do central para todos os outros no da rede
                else:
                    if(random.choice([True, False])):
                        listEdgeResult.append((nodeOrigin, nodeDest, weight)) #construir as outras rotas da rede
                    
    return listEdgeResult


def main():
    
    graph = Route(build_example_route())
    graph.printGraph()
    
    print("ola mundo")

main()