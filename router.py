import networkx as nx

def calculate_safety_weighted_cost(length, safety_score, safety_weight=0.8):
    """
    Custom cost function balancing physical distance and safety score.
    Lower cost = preferred route.
    If safety_weight is high, roads with low safety scores become extremely 'expensive' to cross.
    """
    normalized_safety = safety_score / 100.0 # 0 to 1
    # Cost formula: Distance penalized by lack of safety
    cost = length * (1 + (safety_weight * (1 - normalized_safety)))
    return cost

def find_safest_path(G, source_node, target_node, safety_weight=0.8):
    # Custom weight assignment on graph edges
    for u, v, data in G.edges(data=True):
        length = data.get('length', 1.0)
        # Mocking or fetching predicted safety score for the edge (default to 75 if missing)
        safety_score = data.get('safety_score', 75.0) 
        data['custom_cost'] = calculate_safety_weighted_cost(length, safety_score, safety_weight)
        
    # Find shortest path using Dijkstra with our custom safety cost
    path = nx.shortest_path(G, source=source_node, target=target_node, weight='custom_cost')
    return path