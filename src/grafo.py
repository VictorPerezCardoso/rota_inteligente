
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = os.path.join(ROOT, 'data')
OUT = os.path.join(ROOT, 'outputs')

def build_graph(pontos_csv, matriz_csv):
    pts = pd.read_csv(pontos_csv)
    mat = pd.read_csv(matriz_csv)
    G = nx.Graph()
    for _, r in pts.iterrows():
        G.add_node(int(r['id']), local=r['local'], lat=float(r['lat']), lon=float(r['lon']))
    for _, r in mat.iterrows():
        u = int(r['origem']); v = int(r['destino']); w = float(r['tempo_min'])
        G.add_edge(u, v, tempo=w)
    return G

def visualize_graph(G, out_path):
    pos = {n:(G.nodes[n]['lon'], G.nodes[n]['lat']) for n in G.nodes()}
    labels = {n: G.nodes[n]['local'] for n in G.nodes()}
    plt.figure(figsize=(6,6))
    nx.draw(G, pos, with_labels=False, node_size=300)
    for n, (x,y) in pos.items():
        plt.text(x, y, labels[n], fontsize=8, horizontalalignment='left', verticalalignment='bottom')
    # annotate edges with weight
    edge_labels = {(u,v): f"{d['tempo']}" for u,v,d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    plt.title('Grafo de Entregas (nós = bairros)')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

if __name__ == '__main__':
    pontos = os.path.join(DATA, 'pontos_entrega.csv')
    matriz = os.path.join(DATA, 'matriz_distancias.csv')
    out_img = os.path.join(OUT, 'grafo_visualizado.png')
    G = build_graph(pontos, matriz)
    visualize_graph(G, out_img)
    print('Grafo gerado em', out_img)
