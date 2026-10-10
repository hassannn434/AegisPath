import osmnx as ox
import networkx as nx

def build_city_road_graph(place_name="Mumbai, India"):
    print(f"Downloading street network for {place_name}...")
    # Download walkable street networks
    G = ox.graph_from_place(place_name, network_type="walk")
    
    # Project graph to UTM for metric distance calculations (meters)
    G_projected = ox.project_graph(G)
    
    print(f"Graph loaded successfully with {len(G_projected.nodes)} nodes and {len(G_projected.edges)} edges.")
    return G_projected

if __name__ == "__main__":
    graph = build_city_road_graph()