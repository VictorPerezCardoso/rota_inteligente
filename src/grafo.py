import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import os

# Caminhos padrão
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = os.path.join(ROOT, 'data')
OUT = os.path.join(ROOT, 'outputs')

def build_graph(pontos_csv, matriz_csv):
    """
    Constrói o grafo de entregas a partir dos arquivos CSV.
    Funciona mesmo que os pontos não tenham coordenadas (usa layout automático).
    """
    pts = pd.read_csv(pontos_csv)
    mat = pd.read_csv(matriz_csv)

    G = nx.Graph()

    # Adiciona os nós (pode ser numérico ou nomeado)
    for _, r in pts.iterrows():
        node_id = r.get('id', None)
        if node_id is None:
            node_id = r.get('local', str(len(G.nodes()) + 1))
        G.add_node(node_id,
                   local=r.get('local', str(node_id)),
                   lat=r.get('lat', None),
                   lon=r.get('lon', None))

    # Adiciona as arestas com o tempo de deslocamento
    for _, r in mat.iterrows():
        u = r['origem']
        v = r['destino']
        w = r['tempo_min']
        G.add_edge(u, v, tempo=w)

    # Gera layout automático e armazena no grafo (caso não tenha lat/lon)
    G.graph['pos'] = nx.spring_layout(G, seed=42)

    return G


def visualize_graph(G, out_path):
    """
    Mostra e salva o grafo com nomes, pesos e visualização interativa.
    """
    # Usa layout salvo no grafo
    pos = G.graph.get('pos', nx.spring_layout(G, seed=42))

    # Define rótulos (funciona com nome ou número)
    labels = {}
    for n in G.nodes():
        labels[n] = G.nodes[n].get('local', str(n))

    plt.figure(figsize=(7, 7))
    nx.draw(G, pos,
            with_labels=True,
            labels=labels,
            node_size=1200,
            node_color='lightblue',
            font_size=10,
            font_weight='bold',
            edge_color='gray')

    # Mostra os pesos das arestas
    edge_labels = nx.get_edge_attributes(G, 'tempo')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9)

    plt.title('📍 Grafo de Entregas - Rota Inteligente', fontsize=13)
    plt.tight_layout()

    # Salva a imagem no diretório outputs
    if out_path:
        plt.savefig(out_path)
        print(f"✅ Gráfico salvo em: {out_path}")

    # Exibe o gráfico em uma nova janela
    plt.show()


if __name__ == '__main__':
    pontos = os.path.join(DATA, 'pontos_entrega.csv')
    matriz = os.path.join(DATA, 'matriz_distancias.csv')
    out_img = os.path.join(OUT, 'grafo_visualizado.png')
    G = build_graph(pontos, matriz)
    visualize_graph(G, out_img)
    print('Grafo gerado em', out_img)

    out_img = os.path.join(OUT, 'grafo_visualizado.png')
    G = build_graph(pontos, matriz)
    visualize_graph(G, out_img)
    print('Grafo gerado em', out_img)
