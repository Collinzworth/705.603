import math
import random
from copy import deepcopy
import matplotlib.pyplot as plt

import Optimize_Layout.Bi_Graph as big
import Optimize_Layout.Genetic_Operators as go
import Optimize_Layout.GA_Visualization as gv

import Optimize_Layout.GA_Operator_Plot as ga_oper_p

plot_ga_operators = False

class Population:

    def __init__(self, bi_graph_nx, pop_size):
        
        self.population = []
        self.bi_graph_nx = bi_graph_nx
        self.pop_size = pop_size
        self.fitness_dict = {}
        self.explored_graphs = {} # Keeps track of all calculated graph fitnesses

        # Init Plot settings
        self.operator_plot = None

        self.initialize_population()

        return

    def initialize_population(self):

        bi_graph_nx = self.bi_graph_nx

        print("Initializing Population")

        population = self.population

        init_fitness = bi_graph_nx.num_line_crossings
        population.append((init_fitness, bi_graph_nx))

        self.max_ypos = -math.inf
        
        for ind_num in range(1, self.pop_size):

            bi_graph_nx_copy = deepcopy(bi_graph_nx)
            bi_graph_nx_copy = scramble_network(bi_graph_nx_copy)
            bigraph_new = big.Bi_Graph(bi_graph_nx_copy.network)

            population.append((bigraph_new.num_line_crossings, bigraph_new))
            
            if bigraph_new.max_ypos > self.max_ypos:
                self.max_ypos = bigraph_new.max_ypos

            # print("Individual num {} has {} # of crossings".format(ind_num, bigraph_new.num_line_crossings))
            self.pop_fitness_dict(bigraph_new)

        population = sorted(population, key=lambda x: x[0])

        print("Population Initialized")


        return

    def pop_fitness_dict(self, individual):

        if self.fitness_dict.get(individual.num_line_crossings):
            self.fitness_dict[individual.num_line_crossings].append(individual)
        else:
            self.fitness_dict[individual.num_line_crossings] = [individual]

        return
    
    def repopulate(self, tournament_size, num_elite, crossover_rate, mutation_rate):

        # Initialiaze GA Operator Plot
        if not self.operator_plot and plot_ga_operators:
            self.operator_plot = ga_oper_p.GA_Operator_Plot()

        pop_copy = deepcopy(self.population)
        self.population = self.population[0:num_elite]

        iterations = 0
        while len(self.population) < self.pop_size:

            parents = go.selection(pop_copy, tournament_size)

            individuals = go.crossover(parents, crossover_rate)

            parents_only = (parents[0][1], parents[1][1])

            if plot_ga_operators:
                self.operator_plot = self.operator_plot.update_plot(parents_only, individuals)

            for individual in individuals:
                random_draw = random.uniform(0, 1)
                individual = go.mutate(individual, mutation_rate, random_draw, self.max_ypos)
                if iterations > 3*len(self.population) or not self.check_if_ind_exists(individual):
                    self.population.append((individual.num_line_crossings, individual))

            iterations = iterations + 1

        self.population = sorted(self.population, key=lambda x: x[0])

        return

    """
    check_if_ind_exits: checks the yposition dictionary of the reproduced offspring and current population to make sure duplicates are not repopulated
    into the population.
    
    
    """
    def check_if_ind_exists(self, individual):
        for pop_ind in self.population:
            if self.dict_compare(pop_ind[1].ypos_dict, individual.ypos_dict):
                return True
        return False

    def dict_compare(self, d1, d2):
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        shared_keys = d1_keys.intersection(d2_keys)

        for key in shared_keys:
            try:
                if d1[key] == d2[key]:
                    continue
                else:
                    return False
            except:
                return False

            
        return True

        # added = d1_keys - d2_keys
        # removed = d2_keys - d1_keys
        # modified = {o : (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
        # same = set(o for o in shared_keys if d1[o] == d2[o])



        # return added, removed, modified, same


def scramble_network(bi_graph_nx):
    # randomize y coordinates of each individual's nodes
    for key in bi_graph_nx.xpos_dict:
        level_nodes = bi_graph_nx.xpos_dict[key]
        bi_graph_nx = randomize_y_level_coords(bi_graph_nx, level_nodes)

    return bi_graph_nx


def randomize_y_level_coords(bi_graph_nx, level_nodes):

    network = bi_graph_nx.network
    
    if len(level_nodes) > 1:

        y_coords =  [network.nodes()[node_name]["y_pos"] for node_name in level_nodes]
        random.shuffle(y_coords)
        random.shuffle(level_nodes)
        for node_name in level_nodes:

            node = network.nodes()[node_name]

            node["y_pos"] = y_coords.pop(0)
            node["pos"] = (node["x_pos"], node["y_pos"])

    else:

        node_name = level_nodes[0]
        node = network.nodes()[node_name]

        minimum = min([network.nodes()[node_name]['y_pos'] for node_name in network.nodes()])
        maximum = max([network.nodes()[node_name]['y_pos'] for node_name in network.nodes()])

        node["y_pos"] = random.randint(int(minimum), int(maximum))

    return bi_graph_nx



def get_limits(individual_list):

    max_x = -math.inf
    max_y = -math.inf

    for individual in individual_list:

        ind = individual[0][1]

        ind_max_x = ind.max_xpos
        ind_max_y = ind.max_ypos

        if ind_max_x > max_x:
            max_x = ind_max_x

        if ind_max_y > max_y:
            max_y = ind_max_y

    return max_x, max_y