
import math
from copy import deepcopy

import Optimize_Layout.Bi_Graph as big
import Optimize_Layout.Population as olp

def random_search(graph, max_gen, pop_size):

    best_random_ind = None
    best_random_fitness = math.inf

    num_evals = max_gen*pop_size

    for i in range(0, num_evals):

        new_random_bigraph = olp.scramble_network(graph)
        new_random_bigraph = big.Bi_Graph(new_random_bigraph.network)
        new_random_bigraph_fitness = new_random_bigraph.num_line_crossings

        if new_random_bigraph_fitness < best_random_fitness:
            best_random_ind = new_random_bigraph
            best_random_fitness = new_random_bigraph_fitness
            print("Best Fitness: {} crossings".format(best_random_fitness))

    return best_random_ind, best_random_fitness

