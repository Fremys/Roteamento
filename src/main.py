import pandas as pd 
import networkx as nx
import matplotlib.pyplot as plt
import random
import sys

class Route:
    graph = nx.null_graph
    centerNode = ""
            
    def __init__(self, graph, centerNode):
        self.graph = graph
        self.centerNode=centerNode
    
    def print_graph(self):
        nx.draw(self.graph, with_labels=True, pos=nx.circular_layout(self.graph), node_color='r', edge_color='b', font_weight='bold')
        # Obtendo os pesos das arestas
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')  # Extrai os pesos das arestas
        nx.draw_networkx_edge_labels(self.graph, nx.circular_layout(self.graph), edge_labels=edge_labels, font_color='red')
        plt.show()
             
    def print_edges_info(self, origin, dest):
        """_summary_

        CUIDADO!
        ESSE MÉTODO É DE USO INTERNO DA CLASSE
        
        Esse metodo mostra na tela a aresta e seu
        respectivo peso
        
        Args:
            origin (string): nó de origem da aresta
            dest (string): nó de destino da aresta
        """
        if(self.graph.has_edge(origin, dest)):
            print(f"Aresta: {origin} - {dest} | Valor = {self.graph.get_edge_data(origin, dest).get("weight")}") 
        else:
            print(f"Aresta: {origin} - {dest} | Valor = N/A")     
            
    def print_edges_and_weight(self):
        
        nodes = list(self.graph.nodes) #resgatar lista de nos do grafo
        
        for origin in nodes:
            for dest in nodes:
                if(origin != dest):
                    self.print_edges_info(origin, dest)
    
        
    
def build_example_route(centerNode="D"):
    #definir dados
    exampleGraph = nx.Graph() 
    listNode = ["A", "B", "C", "D", "E", "F"]
    listEdge = build_edges_with_center_node(listNode, centerNode)
    
    exampleGraph.add_nodes_from(listNode) #adicionando os nos ao grafo
    exampleGraph.add_weighted_edges_from(listEdge) #adicionando as arestas ao grafo 
    
    return exampleGraph

def add_edge_to_nodes(originNode, destNode, weight, centerNode, listEdgeResult):
    if(originNode == centerNode):
        listEdgeResult.append((originNode, destNode, weight)) #construir rota do central para todos os outros no da rede
    else:
        if(random.choice([True, False])):
            listEdgeResult.append((originNode, destNode, weight)) #construir as outras rotas da rede
    
def build_edges_with_center_node(listNode, centerNode):
    
    listEdgeResult = []
    
    for originNode in listNode:
        for destNode in listNode:
            weight = random.randint(1, 20)
            if(destNode != originNode): #nao construir loops no grafo
                add_edge_to_nodes(originNode, destNode, weight, centerNode, listEdgeResult)
                    
    return listEdgeResult

def calc_economic(firstNode, secondNode, centerNode, graph):
    
    if(not(graph.has_edge(firstNode, secondNode))):
        return (-1) * sys.maxsize
    
    firstToOriginD =  get_edge_value(graph, centerNode, firstNode)
    secondToOriginD = get_edge_value(graph, centerNode, secondNode)
    firstToSecondD =  get_edge_value(graph, firstNode, secondNode)
        
    return firstToOriginD + secondToOriginD - firstToSecondD 

def get_edge_value(graph, originNode, destNode):
    return graph.get_edge_data(originNode, destNode).get("weight")

def main():
    
    route = Route(build_example_route("D"), "D")
    # route.graph.
    # route = Route(nx.graph_atlas(), 3)
    listNodes = list(route.graph.nodes)
    
    # route.graph.get_edge_data(listNodes[0], listNodes[1]).get("weight")
    # print(listNodes)
    dist = calc_economic(listNodes[0], listNodes[1], route.centerNode, route.graph)
    print(f"distancia : {dist}")
    
    route.print_edges_and_weight()
    
    route.print_graph()

#Executar funcao principal
main()