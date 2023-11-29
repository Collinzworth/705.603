
import pylab as pl
from copy import copy, deepcopy
import matplotlib.pyplot as plt

import Optimize_Layout.Population as pop
import Optimize_Layout.GA_Visualization as gv

plot_ga_operators = False

def opt_line_crossings(tsn_net, plot_network, pop_size, max_gen, tourny_perc, 
                       elite_perc, crossover_rate, mutation_rate):

    tournament_size = calc_num_tournament(tourny_perc, pop_size)
    num_elite = calc_num_elite(elite_perc, pop_size)

    genetic_args = {}
    genetic_args["crossover_rate"] = crossover_rate
    genetic_args["mutation_rate"] = mutation_rate
    genetic_args["tournament_size"] = tournament_size
    genetic_args["num_elite"] = num_elite

    if plot_network:
        fig, ax = pl.subplots()

    print("Initial Fitness: {} crossings".format(tsn_net.num_line_crossings))
    population = pop.Population(tsn_net, pop_size)

    best_inds = []
    generation = 0
    while generation <= max_gen:

        print("Generation {}!".format(str(generation)))

        population.repopulate(**genetic_args)

        best_ind = population.population[0]
        best_fitness = best_ind[0]

        best_inds = update_best_inds(best_inds, best_ind, best_fitness, generation)

        print("Best Fitness: {} crossings".format(best_fitness))

        generation = generation + 1

    return best_inds

def update_best_inds(best_inds, best_ind, best_fitness, generation):
    if best_inds and best_inds[-1][0][0] != best_fitness:
        best_inds.append((best_ind, generation))
    elif not best_inds:
        best_inds.append((best_ind, generation))
    return best_inds


def print_level_y_coords(network, level_nodes):
    for level_node_name in level_nodes:
        level_node = network.nodes()[level_node_name]
        y_pos = level_node["y_pos"]
        print("{}  {}".format(level_node_name, y_pos))
    return


def calc_num_tournament(tournament_percent, pop_size):
    tournament_size = int(tournament_percent*pop_size)
    if tournament_size < 2:
        raise Exception("Tournament Size is too small (< 2), increase tournament percentage")
    return tournament_size

def calc_num_elite(elite_percent, pop_size):
    num_elite = int(elite_percent*pop_size)
    if num_elite < 1:
        raise Exception("Elitism pool too small (< 1), increase elite percentage")
    return num_elite




# def get_edge_linestring(network, edge):

#     node1 = network.nodes()[edge[0]]
#     node2 = network.nodes()[edge[1]]

#     node1_coords = (node1["x_pos"], node1["y_pos"])
#     node2_coords = (node2["x_pos"], node2["y_pos"])

#     linestring = LineString([node1_coords, node2_coords])

#     return linestring


# if __name__ == "__main__":
#     main()