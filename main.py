import random

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from scipy.interpolate import interp1d


# Функція для апроксимації кривої
def interpolate_curve(x_points, y_points, num_points=100):
    t = np.linspace(0, 1, len(x_points))
    interp_x = interp1d(t, x_points, kind='linear')
    interp_y = interp1d(t, y_points, kind='linear')
    
    t_new = np.linspace(0, 1, num_points)
    x_new = interp_x(t_new)
    y_new = interp_y(t_new)
    
    return x_new, y_new

# Функція для розрахунку довжини кривої
def curve_length(x_points, y_points):
    length = 0
    for i in range(1, len(x_points)):
        dx = x_points[i] - x_points[i-1]
        dy = y_points[i] - y_points[i-1]
        length += np.sqrt(dx**2 + dy**2)
    return length

# Функція для рівномірного розміщення вершин на кривій
def generate_uniform_curve_positions(nodes, x_points, y_points):
    x_new, y_new = interpolate_curve(x_points, y_points)
    total_length = curve_length(x_new, y_new)
    distances = np.linspace(0, total_length, len(nodes))
    
    positions = {}
    accumulated_length = 0
    current_index = 0
    
    for i, node in enumerate(nodes):
        while current_index < len(x_new) - 1 and accumulated_length < distances[i]:
            dx = x_new[current_index + 1] - x_new[current_index]
            dy = y_new[current_index + 1] - y_new[current_index]
            accumulated_length += np.sqrt(dx**2 + dy**2)
            current_index += 1
        positions[node] = np.array([x_new[current_index], y_new[current_index]])
    
    return positions

# Створення графа
G = nx.Graph()

# Додавання вершин до графа
stations = [
    "110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127",
    "210", "211", "212", "213", "214", "215", "216", "217", "218", "219", "220", "221", "222", "223", "224", "225", "226", "227",
    "310", "311", "312", "313", "314", "315", "316", "317", "318", "319", "320", "321", "322", "323", "324", "325"
]
G.add_nodes_from(stations)

# Визначення контрольних точок для кривих (приблизні координати)
red_line_x = [-2,  6, 15, 17, 20, 25]
red_line_y = [16, 11, 11,  9,  9, 12]
blue_line_x = [13, 13, 11, 9, 4, -4]
blue_line_y = [30, 10, 8, 5, 1, 1]
green_line_x = [4, 10, 10, 13, 13, 17, 24, 30]
green_line_y = [18, 14, 10, 8,  5,  1,  1,  3]

# Генерація позицій для кожної лінії
red_line_positions = generate_uniform_curve_positions(["110", "111", "112", "113", "114", "115", "116", "117", "118", "119", "120", "121", "122", "123", "124", "125", "126", "127"], red_line_x, red_line_y)
blue_line_positions = generate_uniform_curve_positions(["210", "211", "212", "213", "214", "215", "216", "217", "218", "219", "220", "221", "222", "223", "224", "225", "226", "227"], blue_line_x, blue_line_y)
green_line_positions = generate_uniform_curve_positions(["310", "311", "312", "313", "314", "315", "316", "317", "318", "319", "320", "321", "322", "323", "324", "325"], green_line_x, green_line_y)

# Об'єднання позицій
positions = {**red_line_positions, **blue_line_positions, **green_line_positions}

# Додавання ребер (зв'язків)
edges = [
    ("110", "111"), ("111", "112"), ("112", "113"), ("113", "114"), ("114", "115"), ("115", "116"),
    ("116", "117"), ("117", "118"), ("118", "119"), ("119", "120"), ("120", "121"), ("121", "122"),
    ("122", "123"), ("123", "124"), ("124", "125"), ("125", "126"), ("126", "127"),
    ("210", "211"), ("211", "212"), ("212", "213"), ("213", "214"), ("214", "215"), ("215", "216"),
    ("216", "217"), ("217", "218"), ("218", "219"), ("219", "220"), ("220", "221"), ("221", "222"),
    ("222", "223"), ("223", "224"), ("224", "225"), ("225", "226"), ("226", "227"),
    ("310", "311"), ("311", "312"), ("312", "313"), ("313", "314"), ("314", "315"), ("315", "316"),
    ("316", "317"), ("317", "318"), ("318", "319"), ("319", "320"), ("320", "321"), ("321", "322"),
    ("322", "323"), ("323", "324"), ("324", "325"),
    ("119", "314"), ("315", "218"), ("120", "217")
]

random.seed(42)

# Додавання ребер до графа з атрибутами
for edge in edges:
    random_weight = round(random.uniform(0.5, 2), 1)
    if edge[0] in red_line_positions and edge[1] in red_line_positions:
        G.add_edge(edge[0], edge[1], color='red', weight=random_weight)
    if edge[0] in blue_line_positions and edge[1] in blue_line_positions:
        G.add_edge(edge[0], edge[1], color='blue', weight=random_weight)
    if edge[0] in green_line_positions and edge[1] in green_line_positions:
        G.add_edge(edge[0], edge[1], color='green', weight=random_weight)

# Додавання ребер переходів між лініями до графа з атрибутами
connections = [("119", "314", 'purple', 5), ("315", "218", 'purple', 7), ("120", "217", 'purple', 4)]
for c in connections:
    G.add_edge(c[0], c[1], color=c[2], weight=c[3])


# Отримання кольорів та ваг ребер
edge_colors = [G[u][v]['color'] for u, v in G.edges()]
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

# Візуалізація графа
plt.figure(figsize=(10, 7))
nx.draw(G, pos=positions, with_labels=True, node_color='skyblue', node_size=500, font_size=10, font_color='black', edge_color=edge_colors, width=edge_weights)


# Аналіз основних характеристик
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
degrees = dict(G.degree())
degree_centrality = nx.degree_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

print(f"К-ть вершин: {num_nodes}")
print(f"К-ть ребер: {num_edges}")
print(f"max та min ступені вершин: {max(degrees.values())}, {min(degrees.values())}")
print(f"Ступінь центральності top10: {sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]}")
print(f"Близькість вузла top10: {sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]}")
print(f"Посередництво вузла top10: {sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]}")

# Відображення кривих ліній для debug
#plt.plot(red_line_x, red_line_y, 'r--', alpha=0.5)
#plt.plot(blue_line_x, blue_line_y, 'b--', alpha=0.5)
#plt.plot(green_line_x, green_line_y, 'g--', alpha=0.5)

plt.show()
