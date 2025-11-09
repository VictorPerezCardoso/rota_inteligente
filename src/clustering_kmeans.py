
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = os.path.join(ROOT, 'data')
OUT = os.path.join(ROOT, 'outputs')

def run_kmeans(pontos_csv, k=3):
    pts = pd.read_csv(pontos_csv)
    coords = pts[['lat','lon']].values
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10).fit(coords)
    pts['cluster'] = kmeans.labels_
    out_img = os.path.join(OUT, 'clusters_entregas.png')
    plt.figure(figsize=(6,6))
    for c in range(k):
        subset = pts[pts['cluster']==c]
        plt.scatter(subset['lon'], subset['lat'], label=f'Cluster {c}')
        for _, r in subset.iterrows():
            plt.text(r['lon'], r['lat'], r['local'], fontsize=8)
    plt.legend()
    plt.title(f'Clusters de Entregas (k={k})')
    plt.tight_layout()
    plt.savefig(out_img)
    plt.close()
    out_csv = os.path.join(DATA, 'pontos_com_cluster.csv')
    pts.to_csv(out_csv, index=False)
    return out_csv, out_img

if __name__ == '__main__':
    run_kmeans(os.path.join(DATA,'pontos_entrega.csv'), k=3)
    print('K-Means executado. Saídas em pasta outputs/ e data/.')
