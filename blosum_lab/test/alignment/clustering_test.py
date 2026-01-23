from alignment.clustering import build_identity_graph, connected_components


class TestClustering:

    def test_build_identity_graph(self):
        pairwise_identity = [
            ("pfam1", "id1", "id2", 0),
            ("pfam1","id1", "id3", 75),
            ("pfam1","id2", "id3", 60),
        ]

        graph_build = build_identity_graph(pairwise_identity, 60)
        expected_graph = {
            "id1": set(["id3"]),
            "id2": set(["id3"]),
            "id3": set(["id1", "id2"]),
        }
        assert graph_build == expected_graph

    
    def test_conntected_components(self):
        graph = {
            'id1': {'id2', 'id3'}, 
            'id2': {'id1', 'id3'}, 
            'id3': {'id2'},
            'id4': {'id5'},
            'id5': {'id4'}
            }
        clusters = connected_components(graph)
        expected_clusters = [{"id1", "id2", "id3"}, {"id4", "id5"}]
        assert clusters == expected_clusters

        