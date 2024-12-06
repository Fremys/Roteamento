import tkinter.filedialog as fd
import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Funções do problema
def generate_graph(num_nodes=31):
    G = nx.Graph()
    G.add_nodes_from(range(1, num_nodes + 1))
    demands = {node: random.randint(1, 10) for node in G.nodes}
    demands[1] = 0  # Depósito tem demanda 0
    nx.set_node_attributes(G, demands, "demand")
    
    for node in G.nodes:
        target = random.choice([n for n in G.nodes if n != node])
        weight = random.randint(1, 100)
        G.add_edge(node, target, weight=weight)
    
    for _ in range(num_nodes * 2):
        u, v = random.sample(G.nodes, 2)
        if not G.has_edge(u, v):
            weight = random.randint(1, 100)
            G.add_edge(u, v, weight=weight)
    
    return G

def clarke_wright_algorithm(G, depot=1, vehicle_capacity=50):
    demands = nx.get_node_attributes(G, "demand")
    print(vehicle_capacity)
    routes = {node: ([depot, node, depot], demands[node]) for node in G.nodes if node != depot}
    savings = []
    
    for i in G.nodes:
        for j in G.nodes:
            if i < j and i != depot and j != depot:
                cost_direct = nx.shortest_path_length(G, depot, i, weight='weight') + \
                              nx.shortest_path_length(G, depot, j, weight='weight')
                cost_savings = cost_direct - nx.shortest_path_length(G, i, j, weight='weight')
                savings.append((cost_savings, i, j))
    
    savings.sort(reverse=True, key=lambda x: x[0])
    
    for _, i, j in savings:
        route_i = next((r for r in routes.values() if i in r[0]), None)
        route_j = next((r for r in routes.values() if j in r[0]), None)
        
        if route_i and route_j and route_i != route_j:
            route_nodes_i, load_i = route_i
            route_nodes_j, load_j = route_j
            
            if load_i + load_j <= vehicle_capacity:
                if route_nodes_i[-2] == i and route_nodes_j[1] == j:
                    new_route = route_nodes_i[:-1] + route_nodes_j[1:]
                    new_load = load_i + load_j
                    for node in new_route[1:-1]:
                        routes.pop(node, None)
                    routes[i] = (new_route, new_load)
    
    return [route[0] for route in routes.values()]

def load_graph_from_txt(filepath):
    with open(filepath, "r") as file:
        lines = file.readlines()
    
    num_nodes = int(lines[0].strip())
    vehicle_capacity = int(lines[1].strip())
    demands = list(map(int, lines[2].strip().split()))

    G = nx.Graph()
    G.add_nodes_from(range(1, num_nodes + 1))
    nx.set_node_attributes(G, {i + 1: demand for i, demand in enumerate(demands)}, "demand")
    
    for line in lines[3:]:
        node1, node2, weight = map(int, line.strip().split())
        G.add_edge(node1, node2, weight=weight)
    
    return G, vehicle_capacity

class GraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clarke-Wright Algorithm")
        self.geometry("1200x800")
        
        self.graph = None
        self.original_xlim = None
        self.original_ylim = None
        
        # Botão para gerar grafo
        self.generate_btn = ttk.Button(self, text="Gerar Grafo", command=self.generate_graph)
        self.generate_btn.pack(pady=10)

        # Botão para carregar grafo de um TXT
        self.load_btn = ttk.Button(self, text="Carregar Grafo de TXT", command=self.load_graph)
        self.load_btn.pack(pady=10)
        
        # Área para visualização do grafo
        self.figure = plt.Figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack()
        
        # Botão para aplicar o algoritmo
        self.apply_btn = ttk.Button(self, text="Aplicar Clarke-Wright", command=self.apply_algorithm)
        self.apply_btn.pack(pady=10)
        
        # Botão para resetar o zoom
        self.reset_zoom_btn = ttk.Button(self, text="Resetar Zoom", command=self.reset_zoom)
        self.reset_zoom_btn.pack(pady=10)
        
        # Área para mostrar resultados
        self.result_label = ttk.Label(self, text="Resultados:", anchor="w")
        self.result_label.pack(fill="x", pady=5)
        self.result_text = tk.Text(self, height=10)
        self.result_text.pack(fill="both", expand=True)
    
    def generate_graph(self):
        self.graph = generate_graph()
        self.display_graph()
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "Grafo gerado com sucesso!\n")
    
    def load_graph(self):
        filepath = fd.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not filepath:
            return
        
        try:
            self.graph, self.vehicle_capacity = load_graph_from_txt(filepath)
            self.display_graph()
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Grafo carregado com sucesso de {filepath}!\n")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar o arquivo: {e}")
    
    def display_graph(self):
        self.figure.clear()
        pos = nx.spring_layout(self.graph, k=0.4, seed=42)
        ax = self.figure.add_subplot(111)
        nx.draw(
            self.graph,
            pos,
            ax=ax,
            with_labels=True,
            node_color="lightblue",
            font_weight="bold",
            node_size=800
        )
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, ax=ax)
        
        # Salvar limites originais para resetar o zoom
        self.original_xlim = ax.get_xlim()
        self.original_ylim = ax.get_ylim()
        
        # Permite interatividade com o zoom
        self.canvas.mpl_connect("scroll_event", lambda event: self.zoom(event, ax))
        self.canvas.draw()

    def zoom(self, event, ax):
        base_scale = 1.1
        scale_factor = base_scale if event.button == "up" else 1 / base_scale
        
        # Coordenadas do mouse em relação ao gráfico
        xdata = event.xdata
        ydata = event.ydata

        # Obter limites atuais
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()

        # Calcular as distâncias relativas ao centro do zoom
        x_left = xdata - cur_xlim[0]
        x_right = cur_xlim[1] - xdata
        y_bottom = ydata - cur_ylim[0]
        y_top = cur_ylim[1] - ydata

        # Ajustar os limites com base no fator de escala
        new_xlim = [xdata - x_left * scale_factor, xdata + x_right * scale_factor]
        new_ylim = [ydata - y_bottom * scale_factor, ydata + y_top * scale_factor]

        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)

        # Redesenhar o gráfico
        self.canvas.draw()
    
    def reset_zoom(self):
        if self.original_xlim and self.original_ylim:
            ax = self.figure.axes[0]  # Pega o primeiro (e único) eixo do gráfico
            ax.set_xlim(self.original_xlim)
            ax.set_ylim(self.original_ylim)
            self.canvas.draw()
    
    def apply_algorithm(self):
        if self.graph is None:
            messagebox.showerror("Erro", "Gere um grafo primeiro!")
            return
        
        best_routes = clarke_wright_algorithm(self.graph,vehicle_capacity=self.vehicle_capacity)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, "Rotas Otimizadas:\n")
        for route in best_routes:
            self.result_text.insert(tk.END, f"{' -> '.join(map(str, route))}\n")
        self.result_text.insert(tk.END, "\nAlgoritmo concluído com sucesso!")


# Inicializa o aplicativo
if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()