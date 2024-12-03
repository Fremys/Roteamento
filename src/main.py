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
    
    def get_node_list(self):
        return list(self.graph.nodes)
    
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
        # if(self.graph.has_edge(origin, dest)):
        #     print(f"Aresta: {origin} - {dest} | Valor = {self.graph.get_edge_data(origin, dest).get("weight")}")
        # else:
        #     print(f"Aresta: {origin} - {dest} | Valor = N/A")     
            
    def print_edges_and_weight(self):
        
        nodes = list(self.graph.nodes) #resgatar lista de nos do grafo
        
        for origin in nodes:
            for dest in nodes:
                if(origin != dest):
                    self.print_edges_info(origin, dest)
    
def build_random_example_route(centerNode="D"):
    #definir dados
    exampleGraph = nx.Graph() 
    listNode = ["A", "B", "C", "D", "E", "F"]
    listEdge = build_edges_with_center_node(listNode, centerNode)
    
    exampleGraph.add_nodes_from(listNode) #adicionando os nos ao grafo
    exampleGraph.add_weighted_edges_from(listEdge) #adicionando as arestas ao grafo 
    
    return exampleGraph

def build_example_route(listNodes=["A", "B", "C", "D", "E", "F"]):
    centerNode = 'D'  # Nó central
    exampleGraph = nx.Graph()
    
    # Adicionar nós ao grafo
    for node in listNodes:
        exampleGraph.add_node(node)
    
    # Adicionar arestas entre o nó central e todos os outros
    for node in listNodes:
        if node != centerNode:
            weight = random.randint(1, 10)  # Peso aleatório entre 1 e 10
            exampleGraph.add_edge(centerNode, node, weight=weight)
    
    # Adicionar algumas conexões adicionais (não exaustivo)
    extra_edges = [
        ("A", "B", 8),
        ("A", "C", 12),
        ("B", "E", 3),
        ("C", "F", 7),
        # Adicione mais arestas se necessário
    ]
    for edge in extra_edges:
        exampleGraph.add_edge(edge[0], edge[1], weight=edge[2])
    
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

def calc_economy(firstNode, secondNode, route):
    
    if(not(exist_economy_calculate(firstNode, secondNode, route))):
        return (-1) * sys.maxsize
    
    firstToOriginD =  get_edge_value(route.graph, route.centerNode, firstNode)
    secondToOriginD = get_edge_value(route.graph, route.centerNode, secondNode)
    firstToSecondD =  get_edge_value(route.graph, firstNode, secondNode)
        
    return firstToOriginD + secondToOriginD - firstToSecondD 

def get_edge_value(graph, originNode, destNode):
    return graph.get_edge_data(originNode, destNode).get("weight")

def select_key_for_sort(dict):
    return dict['Value']

def exist_economy_calculate(firstNode, secondNode, route):
    #verificar se existe uma rota entres os nós intermediarios e se nenhum deles é o nó central
    return route.graph.has_edge(firstNode, secondNode) and ( firstNode != route.centerNode) and (secondNode != route.centerNode)

def build_economic_dict(route):
    economicDict = [] #dicionario a ser desenvolvido
    nodeList = route.get_node_list()
    
    for i in range(0, (len(nodeList)-1)):
        for j in range(i+1, (len(nodeList))):
            economicDict.append(
                {
                    'SubRoute': [nodeList[i], nodeList[j]],
                    'Value': calc_economy(nodeList[i], nodeList[j], route) 
                    
                }
            )
    return economicDict

def buildGraphNodesFromTXT (graphPath):
    G = nx.Graph()
    with open(graphPath, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
        
        # Atribuindo os centros de distribuicao que estao na primeira linha destacada
        nodes = linhas[0].strip().split()
        for node in nodes:
            G.add_node(node)
    return G

def connectGraphNodesFromTXT (graphPath, G):
    with open(graphPath, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
    
        # Outras linhas: conexões entre os nodulos
        for linha in linhas[1:]:
            origem, destino, peso = linha.strip().split()
            G.add_edge(origem, destino, weight=int(peso))
    return G

def buildFullGraphFromTXT (graphPath):
    # Grafo apenas com os nodes
    rawGraph = buildGraphNodesFromTXT(graphPath)

    # Preencher grafo com as ligações
    fullGraph = connectGraphNodesFromTXT(graphPath, rawGraph)

    return fullGraph


def main():
    
    # route = Route(build_example_route(), "D")
    route = Route(buildFullGraphFromTXT('grafo.txt'), "D")
    print(route.centerNode)
    # route.graph.
    # route = Route(nx.graph_atlas(), 3)
    # listNodes = list(route.graph.nodes)
    
    # route.graph.get_edge_data(listNodes[0], listNodes[1]).get("weight")
    # print(listNodes)
    # economicCalc = build_economic_dict(route)
    # economicCalc.sort(key=select_key_for_sort, reverse=True)
    
    # route.print_edges_and_weight()
    
    # print(economicCalc[0]['Value'])
    
    # route.print_graph()

main()
# # Exibe as arestas com os pesos
# print("Arestas e pesos:")
# for origem, destino, dados in graph.edges(data=True):
#     print(f"{origem} -> {destino}, peso: {dados['weight']}")

# # Desenha o grafo
# pos = nx.spring_layout(graph)  # Layout do grafo
# nx.draw(graph, pos, with_labels=True, node_color='lightblue', font_weight='bold')
# labels = nx.get_edge_attributes(graph, 'weight')
# nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
# plt.show()