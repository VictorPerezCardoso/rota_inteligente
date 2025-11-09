
import heapq
import networkx as nx
import math

def heuristic(u, v, G):
    # euclidean on lat/lon as rough estimate (longitude, latitude)
    ux, uy = G.nodes[u]['lon'], G.nodes[u]['lat']
    vx, vy = G.nodes[v]['lon'], G.nodes[v]['lat']
    return math.hypot(ux - vx, uy - vy) * 111000 / 1000  # scaled roughly to km -> not exact, fine as heuristic

def a_star(G, start, goal):
    # G edges have attribute 'tempo' as weight (minutes)
    open_set = [(0, start)]
    came_from = {}
    gscore = {n: float('inf') for n in G.nodes()}
    gscore[start] = 0
    fscore = {n: float('inf') for n in G.nodes()}
    fscore[start] = heuristic(start, goal, G)
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            # reconstruct path
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
