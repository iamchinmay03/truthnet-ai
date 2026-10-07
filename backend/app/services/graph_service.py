from __future__ import annotations

import networkx as nx


def build_graph_from_dataset(entries: list[dict[str, object]]) -> nx.Graph:
    graph = nx.Graph()
    for entry in entries:
        user_id = str(entry.get("user_id", "anonymous"))
        post_id = str(entry.get("post_id", "post"))
        graph.add_node(user_id, type="user")
        graph.add_node(post_id, type="post")
        graph.add_edge(user_id, post_id, relation="shares")
    return graph


def graph_metrics(graph: nx.Graph) -> dict[str, float | int]:
    centrality = nx.degree_centrality(graph)
    nodes = list(graph.nodes())
    return {
        "node_count": graph.number_of_nodes(),
        "edge_count": graph.number_of_edges(),
        "avg_degree": round(sum(dict(graph.degree()).values()) / max(len(nodes), 1), 2),
        "max_degree_centrality": round(max(centrality.values(), default=0), 2),
        "connected_components": nx.number_connected_components(graph),
    }
