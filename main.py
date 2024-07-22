import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

# Функція для апроксимації та розрахунку довжини кривої
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
red_line_x = [1,  6, 15, 17, 19, 21]
red_line_y = [16, 11, 11,  9,  9, 12]
blue_line_x = [13, 13, 11, 9, 5, 0]
blue_line_y = [25, 10, 8, 5, 1, 1]
green_line_x = [6, 11, 11, 13, 13, 17, 21, 25]
green_line_y = [17, 14, 10, 8,  5,  1,  1,  3]

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

G.add_edges_from(edges)

# Візуалізація графа
plt.figure(figsize=(10, 7))
nx.draw(G, pos=positions, with_labels=True, node_color='skyblue', node_size=500, font_size=10, font_color='black', edge_color='gray')

# Відображення кривих ліній для наочності (debug)
#plt.plot(red_line_x, red_line_y, 'r--', alpha=0.5)
#plt.plot(blue_line_x, blue_line_y, 'b--', alpha=0.5)
#plt.plot(green_line_x, green_line_y, 'g--', alpha=0.5)

plt.show()
