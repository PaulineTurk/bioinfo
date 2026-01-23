from typing import Dict, Set

def build_identity_graph(
    pairwise_identity: list,
    threshold: int
) -> Dict[str, Set[str]]:
    graph: Dict[str, Set[str]] = {}

    for _, id1, id2, identity in pairwise_identity:
        if id1 not in graph: graph[id1] = set()
        if id2 not in graph: graph[id2] = set()
        if identity >= threshold:
            graph[id1].add(id2)
            graph[id2].add(id1)
    return graph


def connected_components(
    graph: Dict[str, Set[str]]
)-> list[set[str]]:
    visited = set()
    clusters = []

    for node in graph:
        if node in visited:
            continue
        stack = [node]
        cluster = set()

        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            cluster.add(current)
            stack.extend(graph[current] - visited)

        clusters.append(cluster)
    return clusters

#TODO: test
def compute_weights(clusters):
    sequence_weights = {}
    for cluster in clusters:
        cluster_size = len(cluster)
        weight_per_sequence = 1.0 / cluster_size
        
        for seq_id in cluster:
            sequence_weights[seq_id] = weight_per_sequence
    return sequence_weights