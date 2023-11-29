import Optimize_Layout.Bi_Graph as big
import Optimize_Layout.GA_Visualization as gv
import Optimize_Layout.Gen_Bipartite_Graph as gbg
import Optimize_Layout.Optimize_Line_Crossings as olc

plot_network = False

min_left = 30
max_left = 30
min_right = 30
max_right = 30
num_edges = 20

def main():

    genetic_args = {}
    genetic_args["pop_size"] = 20
    genetic_args["max_gen"] = 500
    genetic_args["tourny_perc"] = 0.2
    genetic_args["elite_perc"] =  0.1
    genetic_args["crossover_rate"] = 0.9
    genetic_args["mutation_rate"] = 0.2

    network = gbg.gen_bipartite_graph(min_left, max_left, min_right, max_right, num_edges)

    bipartite_graph = big.Bi_Graph(network)
    bipartite_graph.set_node_dict_attr()

    best_individuals = olc.opt_line_crossings(bipartite_graph, plot_network, **genetic_args)
    
    gv.plot_fitness_evolution(best_individuals)

    gv.animate_evolution(best_individuals)

    best_individual = best_individuals[-1]
    best_graph = best_individual[0][1]
    best_generation = best_individuals[-1][1]
    gv.compare_plots(bipartite_graph, "Original Graph", best_graph, "Optimized Graph", best_generation)
    
    input("Press Enter to continue...")

    return


if __name__ == '__main__':
    main()