
import Optimize_Layout.Gen_Bipartite_Graph as gbg
import Optimize_Layout.Optimize_Line_Crossings as olc
import Optimize_Layout.Random_Search as rs
import Optimize_Layout.Bi_Graph as big

plot_network = False

def compare_random(genetic_args, num_iterations, min_left_nodes, max_left_nodes, min_right_nodes, max_right_nodes, num_edges):
    best_ga_fitnesses = []
    best_random_fitnesses = []

    for iteration in range(0, num_iterations):
        network = gbg.gen_bipartite_graph(min_left_nodes, max_left_nodes, min_right_nodes, max_right_nodes, num_edges)
        bipartite_graph = big.Bi_Graph(network)
        bipartite_graph.set_node_dict_attr()

        best_individuals = olc.opt_line_crossings(bipartite_graph, plot_network, **genetic_args)
        best_ga_fitnesses.append(best_individuals[-1][0][0])

        best_random_ind, best_random_fitness = rs.random_search(bipartite_graph, genetic_args["max_gen"], genetic_args["pop_size"])
        best_random_fitnesses.append(best_random_fitness)

        print("Iteration {} Completed".format(iteration))

    return best_ga_fitnesses, best_random_fitnesses