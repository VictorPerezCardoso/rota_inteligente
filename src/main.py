
import os
from src.grafo import build_graph, visualize_graph
from src.clustering_kmeans import run_kmeans
from src.algoritmo_a_star import a_star

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = os.path.join(ROOT, 'data')
OUT = os.path.join(ROOT, 'outputs')

def main():
    pontos = os.path.join(DATA, 'pontos_entrega.csv')
    matriz = os.path.join(DATA, 'matriz_distancias.csv')
    G = build_graph(pontos, matriz)
    visualize_graph(G, os.path.join(OUT, 'grafo_visualizado.png'))
    # run clustering
    csv_clusters, img_clusters = run_kmeans(pontos, k=3)
    # load clusters to plan simple routes: for each cluster, pick node closest to center as start (depot ~ node 1)
    import pandas as pd
    pts = pd.read_csv(csv_clusters)
    report = []
    depot = 1
    clusters = sorted(pts['cluster'].unique())
    for c in clusters:
        nodes = pts[pts['cluster']==c]['id'].tolist()
        # simple route: start from depot, go to each node sequentially using A*
        current = depot
        total = 0
        seq = []
        for n in nodes:
            path, cost = a_star(G, current, int(n))
            if path is None:
                continue
            seq.append({'from': current, 'to': n, 'path': path, 'cost_min': cost})
            total += cost
            current = int(n)
        report.append({'cluster': int(c), 'visitas': len(nodes), 'tempo_total_min': round(total,2), 'detalhe': seq})
    # save report
    import json
    with open(os.path.join(OUT,'relatorio_rotas.json'),'w') as f:
        json.dump(report, f, indent=2)
    print('Processo concluído. Outputs gerados em', OUT)

if __name__ == '__main__':
    main()
