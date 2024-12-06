import networkx as nx
import random
import matplotlib.pyplot as plt

def save_routes_to_txt(graph, filename="rotas.txt"):
    with open(filename, "w") as file:
        file.write("1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31\n")
        for u, v, data in graph.edges(data=True):
            file.write(f"{u}, {v}, {data['weight']}\n")
    print(f"Rotas registradas no arquivo: {filename}")

def save_results_to_txt(routes, filename="resultados.txt"):
    with open(filename, "w") as file:
        file.write("Rotas Otimizadas (Clarke-Wright)\n")
        for route in routes:
            file.write(f" -> ".join(map(str, route)) + "\n")
    print(f"Resultados registrados no arquivo: {filename}")

def generate_graph(num_nodes=31):
    # Cria um grafo vazio
    G = nx.Graph()
    
    # Adiciona os nós
    G.add_nodes_from(range(1, num_nodes + 1))
    
    # Atribui demandas aleatórias (exceto ao depósito)
    demands = {node: random.randint(1, 10) for node in G.nodes}
    demands[1] = 0  # Depósito tem demanda 0
    nx.set_node_attributes(G, demands, "demand")
    
    # Garante que cada nó tenha pelo menos uma aresta conectada
    for node in G.nodes:
        target = random.choice([n for n in G.nodes if n != node])
        weight = random.randint(1, 100)  # Peso aleatório
        G.add_edge(node, target, weight=weight)
    
    # Adiciona arestas adicionais aleatórias
    for _ in range(num_nodes * 2):  # Ajuste para maior conectividade
        u, v = random.sample(G.nodes, 2)
        if not G.has_edge(u, v):
            weight = random.randint(1, 100)
            G.add_edge(u, v, weight=weight)
    
    return G

def clarke_wright_algorithm(G, depot=1, vehicle_capacity=50):
    # Inicializa rotas individuais para cada nó
    demands = nx.get_node_attributes(G, "demand")
    routes = {node: ([depot, node, depot], demands[node]) for node in G.nodes if node != depot}
    savings = []
    
    # Calcula as economias entre cada par de nós
    for i in G.nodes:
        for j in G.nodes:
            if i < j and i != depot and j != depot:
                cost_direct = nx.shortest_path_length(G, depot, i, weight='weight') + \
                              nx.shortest_path_length(G, depot, j, weight='weight')
                cost_savings = cost_direct - nx.shortest_path_length(G, i, j, weight='weight')
                savings.append((cost_savings, i, j))
    
    # Ordena as economias em ordem decrescente
    savings.sort(reverse=True, key=lambda x: x[0])
    
    # Aplica o algoritmo de Clarke-Wright para otimizar as rotas
    for _, i, j in savings:
        route_i = next((r for r in routes.values() if i in r[0]), None)
        route_j = next((r for r in routes.values() if j in r[0]), None)
        
        if route_i and route_j and route_i != route_j:
            route_nodes_i, load_i = route_i
            route_nodes_j, load_j = route_j
            
            # Verifica a capacidade do veículo
            if load_i + load_j <= vehicle_capacity:
                if route_nodes_i[-2] == i and route_nodes_j[1] == j:
                    # Une as rotas i e j
                    new_route = route_nodes_i[:-1] + route_nodes_j[1:]
                    new_load = load_i + load_j
                    for node in new_route[1:-1]:
                        routes.pop(node, None)
                    routes[i] = (new_route, new_load)
    
    return [route[0] for route in routes.values()]

# Gera o grafo
graph = generate_graph()

save_routes_to_txt(graph)

# Desenha o grafo
pos = nx.spring_layout(graph)
nx.draw(graph, pos, with_labels=True, node_color="lightblue", font_weight="bold")
labels = nx.get_edge_attributes(graph, 'weight')
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
plt.title("Grafo Gerado")
plt.show()

# Mostra demandas
demands = nx.get_node_attributes(graph, "demand")
print("Demandas dos nós:", demands)

# Executa o algoritmo de Clarke-Wright
vehicle_capacity = 50
best_routes = clarke_wright_algorithm(graph, vehicle_capacity=vehicle_capacity)

# Salva os resultados das rotas otimizadas no arquivo TXT
save_results_to_txt(best_routes)

print("\nMelhores Rotas Geradas pelo Algoritmo Clarke-Wright:")
for route in best_routes:
    print(route)