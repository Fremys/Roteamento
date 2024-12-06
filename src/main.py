import pandas as pd 
import networkx as nx
import matplotlib.pyplot as plt
import random
import sys
#teste

class NodeDemand():
    Node = ""
    Demand = ""
    
    def __init__(self, node, demand):
        self.Node = node
        self.Demand = demand
class Route:
    graph = nx.null_graph
    centerNode = ""
    qMax = 0
            
    def __init__(self, graph, centerNode, qMax):
        self.graph = graph
        self.centerNode=centerNode
        self.qMax = qMax
    
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

def get_node_demand(node, demandList):
    for nodeDemand in demandList:
        if(nodeDemand.Node == node):
            return nodeDemand.Demand
    return 0

def build_demand_list(nodesGraph, demandList):
    nodeDemandList = []
    
    if(len(nodesGraph) == len(demandList)):
        for i in range(0, len(nodesGraph)):
            nodeDemandList.append(
                NodeDemand(nodesGraph[i], demandList[i])
                )
            
    return nodeDemandList  
    
def build_fix_demand(value, numbersNode):
    listFixDemand = []
    
    for i in range(0, numbersNode):
          listFixDemand.append(value)
          
    return listFixDemand
 
def build_random_example_route(centerNode="D"):
    #definir dados
    exampleGraph = nx.Graph() 
    listNode = ["A", "B", "C", "D", "E", "F"]
    listEdge = build_edges_with_center_node(listNode, centerNode)
    
    exampleGraph.add_nodes_from(listNode) #adicionando os nos ao grafo
    exampleGraph.add_weighted_edges_from(listEdge) #adicionando as arestas ao grafo 
    
    return exampleGraph

def build_example_route(listNodes=["A", "B", "C", "D", "E", "F"], center="D"):
    centerNode = center  # Nó central
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

def calc_init_economy(firstNode, secondNode, route):
    """_summary_
    Esse método realiza o calculo da economia inicial
    para a primeiro iteração do método

    Args:
        firstNode (Dictionary<string:Node, List:Path>): dicionario com o nó e a lista do menor caminho dele para o centro
        secondNode (Dictionary<string:Node, List:Path>): dicionario com o nó e a lista do menor caminho dele para o centro
        route (Route): rota do problema

    Returns:
        int: valor do calculo inicial da economia
    """

    firstToOriginD =  get_value_path(route.graph, firstNode["Path"])
    secondToOriginD = get_value_path(route.graph, secondNode["Path"])
    pathFirstToSecond = nx.dijkstra_path(route.graph, firstNode["Node"], secondNode["Node"]) #resgatar menor caminho entre os dois nós
    firstToSecondD = get_value_path(route.graph, pathFirstToSecond) 
        
    return firstToOriginD + secondToOriginD - firstToSecondD 

def get_value_path(graph, nodeList):
    result = 0
    
    for i in range(0, len(nodeList) - 1 ):
        result = result + graph.get_edge_data(nodeList[i], nodeList[i+1]).get("weight")
    
    return result

def select_key_for_sort(dict):
    return dict["Economics"]

def exist_economy_calculate(firstNode, secondNode, route):
    #verificar se existe uma rota entres os nós intermediarios e se nenhum deles é o nó central
    return route.graph.has_edge(firstNode, secondNode) and ( firstNode != route.centerNode) and (secondNode != route.centerNode)

def build_graph_nodes_from_TXT (graphPath):
    G = nx.Graph()
    with open(graphPath, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
        
        # Atribuindo os centros de distribuicao que estao na primeira linha destacada
        nodes = linhas[0].strip().split()
        for node in nodes:
            G.add_node(node)
    return G

def connect_graph_nodes_from_TXT (graphPath, G):
    with open(graphPath, 'r', encoding='utf-8') as file:
        linhas = file.readlines()
    
        # Outras linhas: conexões entre os nodulos
        for linha in linhas[1:]:
            origem, destino, peso = linha.strip().split()
            G.add_edge(origem, destino, weight=int(peso))
    return G

def build_full_graph_from_TXT (graphPath):
    # Grafo apenas com os nodes
    rawGraph = build_graph_nodes_from_TXT(graphPath)

    # Preencher grafo com as ligações
    fullGraph = connect_graph_nodes_from_TXT(graphPath, rawGraph)

    return fullGraph

def get_min_path_for_center(route): 
    """_summary_

    Usa dijkstra para calcular o caminho minimo de cada
    nó do grafo da rota para o centro

    Args:
        route (Rute): rota do problema

    Returns:
        Dictionary<Node:string, Path:List>: lista do menor caminho do nó para o centro
    """
     
    listNode = route.get_node_list()
    minPaths = []
    
    for node in listNode:
        if(node != route.centerNode):
            pathForCenter = nx.dijkstra_path(route.graph, node, route.centerNode, weight='weight') #buscar o menor caminho do nó para o centro
            minPaths.append(
                    {
                        "Node": node,
                        "Path": pathForCenter
                    }
                )
            
    return minPaths

def demand_calculate(listNode, demandList):
    result = 0
    for node in listNode:
        result = result + get_node_demand(node, demandList)
    return result

def group_init_paths(minPathForCenter, demandList, route):
    """_summary_

    Args:
        minPathForCenter (Dictionary<Node:string, Path:List> : List ): lista de caminhos minimos de cada no para o centro
        route (Route): a rota do problema

    Returns:
        Dictionary<Nodes:List, Economics:int>:List : lista de pares dos nós é suas respectivas economias 
    """
    
    newTableRoute = []
    
    for i in range(0, (len(minPathForCenter)-1)):
        for j in range(i+1, (len(minPathForCenter))):
            
            listNodes = [minPathForCenter[i]["Node"], minPathForCenter[j]["Node"]]
            newTableRoute.append(
                {
                    "Nodes": listNodes, 
                    "Economics":  calc_init_economy(minPathForCenter[i], minPathForCenter[j], route),
                    "Demand" : demand_calculate(listNodes, demandList)
                }
            )
            
    return newTableRoute          
            
def fusion_routes(economicsList):
    """_summary_
        Método que realiza a fusão entre as rotas

        Args:
            economicsList (Dictionary<Nodes: List, Economics:int>:List  ): Lista das economias dos nós ordenadas
        Returns:

    """
    newTableRoute = []
    
    for i in range(0, len(economicsList)-1 ):
        for j in range(0, len(economicsList)):
            print("teste")
            
def clark_and_wrigth(route, demandList):
    
    minPathsForCenter = get_min_path_for_center(route)
    
    economicList = group_init_paths(minPathsForCenter, demandList, route)
    
    economicList.sort(key=select_key_for_sort, reverse=True)
    
    print("finish")
    
    # economicCalc = build_economic_dict(route) #calculo da economia
    # economicCalc.sort(key=select_key_for_sort, reverse=True)

def main():
    
    # route = Route(build_example_route(), "D")
    route = Route(build_full_graph_from_TXT('data/grafo.txt'), "D", 50)
    
    #resgatar a demanda
    fixDemand = build_fix_demand(40, len(route.get_node_list()) )
    demandList = build_demand_list(route.get_node_list(), fixDemand)
    
    # route.graph.get_edge_data
    # route.print_graph()
    clark_and_wrigth(route, demandList)
    
    # route = Route(nx.graph_atlas(), 3)
    
    # route.graph.get_edge_data(listNodes[0], listNodes[1]).get("weight")
    # print(listNodes)
    # economicCalc = build_economic_dict(route)
    # economicCalc.sort(key=select_key_for_sort, reverse=True)
    
    # route.print_edges_and_weight()
    
    # print(economicCalc[0]['Value'])
    
    # route.print_graph()

main()