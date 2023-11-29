import random
import networkx as nx

# Sets the coordinates of the graph layout
Y_SCALE_FACTOR = 100
SHIFT_AMOUNT = 10

def gen_bipartite_graph(min_level1_nodes, max_level1_nodes, min_level2_nodes, max_level2_nodes, num_edges):
    
    # Generate random number set by specified intervals. Use number to generate number of nodes 
    num_level_1_nodes = random.randint(min_level1_nodes, max_level1_nodes)
    num_level_2_nodes = random.randint(min_level2_nodes, max_level2_nodes)

    # generate set of y positions to assign to nodes
    # y_pos_level1_list = random.sample(range(num_level_1_nodes*Y_SCALE_FACTOR), num_level_1_nodes)
    # y_pos_level2_list = random.sample(range(num_level_2_nodes*Y_SCALE_FACTOR), num_level_2_nodes)

    X_SHIFT = max(num_level_1_nodes, num_level_2_nodes)*SHIFT_AMOUNT

    y_pos_level1_list = random.sample(range(0, X_SHIFT, SHIFT_AMOUNT), num_level_1_nodes)
    y_pos_level2_list = random.sample(range(0, X_SHIFT, SHIFT_AMOUNT), num_level_2_nodes)

    # Generate networkx digraph from randomly generated nodes
    network = nx.DiGraph()
    network = generate_nodes(network, y_pos_level1_list, y_pos_level2_list, X_SHIFT)

    level1_range = len(y_pos_level1_list)
    level2_range = level1_range + len(y_pos_level2_list)

    node_list1 = list(range(0, level1_range))
    node_list2 = list(range(level1_range, level2_range))

    network = add_edges(network, node_list1, node_list2, num_edges)

    # Remove nodes that do not have have attached edges
    network.remove_nodes_from(list(nx.isolates(network)))

    return network

def generate_nodes(network, y_pos_level1_list, y_pos_level2_list, x_shift):

    x_coord = 0
    level_num = 0
    node_count = 0
    # Loop over both y_coordinate lists, create node with corresponding xy coordinate
    for y_coord_list in [y_pos_level1_list, y_pos_level2_list]:
        for y_coord in y_coord_list:
            network.add_node(node_count, x_pos=x_coord, y_pos=y_coord, pos=(x_coord, y_coord), level=level_num)
            node_count = node_count + 1
        x_coord = x_coord + x_shift
        level_num = level_num + 1

    return network

def add_edges(network, node_list1, node_list2, num_edges):
 
    for edge_num in range(0, num_edges):
        left_node = random.sample(node_list1, 1)[0]
        right_node = random.sample(node_list2, 1)[0]
        if not network.has_edge(left_node, right_node):
            network.add_edge(left_node, right_node)

    return network