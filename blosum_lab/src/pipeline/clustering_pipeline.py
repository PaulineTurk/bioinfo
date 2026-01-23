from storage.sqlite import DatabaseBlosumStore
from tqdm import tqdm
from alignment.clustering import build_identity_graph, connected_components, compute_weights

def run(threshold: int, db_path: str):
    store = DatabaseBlosumStore(db_path)
    store.init_cluster(threshold)
    pfams = store.get_all_pfam()
    pfams_count = len(pfams)
    for pfam in tqdm(pfams, total=pfams_count, desc=f"Clustering {threshold}%"):
        pairwise_identity = store.get_all_pairwise_identity(pfam)
        graph = build_identity_graph(pairwise_identity, threshold)
        clusters = connected_components(graph)
        weights = compute_weights(clusters)
        store.save_cluster(pfam, threshold, clusters, weights)