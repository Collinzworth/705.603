import math
import random
import networkx as nx

from copy import copy, deepcopy

import Optimize_Layout.Bi_Graph as big
import Optimize_Layout.GA_Visualization as gv

fitness_func_name = "line_crossings"


"""
Selection: Performs tournament selection. A select sample size "tournament size" is taken from the population. 
With the selected sample size, the individual with the largest fitness is selected.

Inputs
    population list(digraph): population of current generation
    tournament_size (int): size of the sample to perform tournament on.

Outputs
    parents Tuple(digraph): Tuple containing selected parents.

"""

def selection(population, tournament_size):

    selected_pop = random.sample(population, tournament_size)
    selected_pop_sorted = sorted(selected_pop, key=lambda x: x[0])

    return selected_pop_sorted[0], selected_pop_sorted[1]


def crossover(parents, crossover_rate):
    cross_chance = random.uniform(0, 1)
    if cross_chance < crossover_rate:
        individuals = cross_parents(parents)
    else:
        individuals = (parents[0][1], parents[1][1])

    return individuals

"""
Cross_Parents: 

Inputs
    parents Tuple(digraph): Tuple containing selected parents.

Outputs

"""

def cross_parents(parents):

    parent1_net_obj_copy = parents[0][1]
    parent2_net_obj_copy = parents[1][1]

    parent1_network = parents[0][1].network
    parent2_network = parents[1][1].network

    parent1_network_copy = copy_network(parent1_network)
    parent2_network_copy = copy_network(parent2_network)

    max_level = parent1_net_obj_copy.max_level

    split_level = random.randint(0, max_level) # At minimum need to split off level 0

    parent1_nodes_from_parent2 = parent1_net_obj_copy.level_dict[split_level]

    for node_name in parent1_nodes_from_parent2:

        parent1_node = parent1_network_copy.nodes()[node_name]
        parent2_node = parent2_network.nodes()[node_name]

        parent1_node["y_pos"] = parent2_node["y_pos"]
        parent1_node["pos"] = (parent1_node["x_pos"], parent1_node["y_pos"])

    for node_name in parent1_nodes_from_parent2:

        parent2_node = parent2_network_copy.nodes()[node_name]
        parent1_node = parent1_network.nodes()[node_name]

        parent2_node["y_pos"] = parent1_node["y_pos"]
        parent2_node["pos"] = (parent2_node["x_pos"], parent2_node["y_pos"])

    parent1 = big.Bi_Graph(parent1_network_copy)
    parent2 = big.Bi_Graph(parent2_network_copy)

    return parent1, parent2

def copy_network(network):
    new_network = nx.DiGraph()
    for node_number in network.nodes():
        
        network_node = network.nodes()[node_number]
        new_network.add_node(node_number)

        new_node = new_network.nodes()[node_number]
        new_node["x_pos"] = network_node["x_pos"]
        new_node["y_pos"] = network_node["y_pos"]
        new_node["pos"] = network_node["pos"]
        new_node["level"] = network_node["level"]
        
    for edge in network.edges():
        new_network.add_edge(edge[0], edge[1])

    return new_network

"""
Mutation: 

Inputs
    

Outputs
    

"""
def mutation(population, num_elite, mutation_rate, max_ypos):
    for individual in population[num_elite:len(population)]:
        random_draw = random.uniform(0, 1)
        individual = mutate(individual, mutation_rate, random_draw, max_ypos)
    return population

"""
Mutate: 

Inputs
    

Outputs

"""

def mutate(individual, mutation_rate, random_draw, max_ypos):
    if random_draw < mutation_rate:
        level_dict = individual.level_dict
        mutation_level = random.randint(0, individual.max_level)
        level_nodes = level_dict[mutation_level]
        individual = swap_level_y_coords(individual, level_nodes, max_ypos)
        individual.set_segments()
        individual.set_node_dict_attr()
        individual.calc_line_crossings()

    return individual



def swap_level_y_coords(individual, level_nodes, max_ypos):
    if len(level_nodes) > 1:
        multi_node_level_case(individual, level_nodes, max_ypos)
    else:
        single_node_level_case(individual, level_nodes, max_ypos)

    return individual

def multi_node_level_case(individual, level_nodes, max_ypos):

    network = individual.network
    
    random_node_num = random.sample(level_nodes, 1)
    random_node = network.nodes()[random_node_num[0]]

    ten_percent = int(0.1*max_ypos)

    random_lb = math.ceil((0 - ten_percent)/10)*10
    random_ub = math.ceil( (max_ypos + ten_percent)/10)*10
    random_ycoord = random.randrange(random_lb, random_ub, 10)
    node_present = False
    for node_number in level_nodes:
        node = network.nodes()[node_number]
        if node["y_pos"] == random_ycoord:
            swap_two_nodes_y_coords(random_node, node)
            node_present = True

    if not node_present:
        random_node["y_pos"] = random_ycoord
        random_node["pos"] = (random_node["x_pos"], random_node["y_pos"])

    return

def swap_two_nodes_y_coords(random_node_1, random_node_2):

    random_node_ypos_1 = random_node_1["y_pos"]
    random_node_ypos_2 = random_node_2["y_pos"]

    random_node_1["y_pos"] = random_node_ypos_2
    random_node_1["pos"] = (random_node_1["x_pos"], random_node_1["y_pos"])

    random_node_2["y_pos"] = random_node_ypos_1
    random_node_2["pos"] = (random_node_2["x_pos"], random_node_2["y_pos"])

    return


def single_node_level_case(individual, level_nodes, max_ypos):

    network = individual.network
    
    # Select node from level
    node_name = level_nodes[0]
    node = network.nodes()[node_name]

    # Select random position between min/max
    node["y_pos"] = random.randint(int(-max_ypos), int(max_ypos))
    node["pos"] = (node["x_pos"], node["y_pos"])

    return


def retrieve_nodes_from_list(level_dict, level):
    node_list = level_dict[1]
    for i in range(2, level+1):
        node_list.extend(level_dict[i])
    return node_list

def retrieve_split_list(level_dict, level):
    node_list1 = []
    node_list2 = []
    for i in list(level_dict.keys()):
        if i < level:
            try:
                node_list1.extend(level_dict[i])
            except:
                node_list1 = level_dict[i]
        else:
            try:
                node_list2.extend(level_dict[i])
            except:
                node_list2 = level_dict[i]

    return node_list1, node_list2

