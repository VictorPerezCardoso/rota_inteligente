import heapq
import networkx as nx
import math

def heuristic(u, v, G):
    """
    Calcula a distância heurística entre dois nós.
    Usa lat/lon se disponíveis; caso contrário, usa coordenadas do layout salvo no grafo.
    """
    # Tenta usar coordenadas reais (lat/lon)
    if all(k in G.nodes[u] for k in ('lat', 'lon')) and all(k in G.nodes[v] for k in ('lat', 'lon')):
        lat_u, lon_u = G.nodes[u]['lat'], G.nodes[u]['lon']
        lat_v, lon_v = G.nodes[v]['lat'], G.nodes[v]['lon']

        if None not in (lat_u, lon_u, lat_v, lon_v):
            # Distância euclidiana aproximada em quilômetros
            return math.hypot(lon_u - lon_v, lat_u - lat_v) * 111

    # Caso contrário, usa coordenadas virtuais do layout
    pos = G.graph.get('pos', nx.spring_layout(G, seed=42))
    ux, uy = pos[u]
    vx, vy = pos[v]
    return math.hypot(ux - vx, uy - vy)


def a_star(G, start, goal):
    """
    Implementação do algoritmo A* (A-Star) para encontrar o caminho mais curto.
    Usa o tempo ('tempo') como peso das arestas.
    """
    open_set = [(0, start)]
    came_from = {}
    gscore = {n: float('inf') for n in G.nodes()}
    gscore[start] = 0
    fscore = {n: float('inf') for n in G.nodes()}
    fscore[start] = heuristic(start, goal, G)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstrói o caminho
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            return path, gscore[goal]

        for neighbor in G.neighbors(current):
            tentative = gscore[current] + G.edges[current, neighbor]['tempo']
            if tentative < gscore[neighbor]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative
                fscore[neighbor] = tentative + heuristic(neighbor, goal, G)
                heapq.heappush(open_set, (fscore[neighbor], neighbor))

    return None, float('inf')

                gscore[neighbor] = tentative
                fscore[neighbor] = tentative + heuristic(neighbor, goal, G)
                heapq.heappush(open_set, (fscore[neighbor], neighbor))
    return None, float('inf')
