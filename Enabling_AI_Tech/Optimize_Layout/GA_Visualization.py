import math
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt
from matplotlib import collections as mc
from IPython import display

import Optimize_Layout.Population as pop

def plot_fitness_evolution(best_individuals):

    fitnesses = []
    generations = []

    for individual in best_individuals:
        fitnesses.append(individual[0][0])
        generations.append(individual[1])

    fig, ax = pl.subplots()
    ax.set_title("Fitness vs Generations")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness (# Line Crossings)")
    plt.plot(generations, fitnesses)
    return

def compare_plots(original_graph, title_left, optimized_graph, title_right, generation):

    c = np.array([(0, 0, 1, 1)])

    combo_fig, sub_axes = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=True)

    combo_fig.suptitle(title_left + ' vs ' + title_right, fontsize=24)
    combo_fig.supxlabel('X Coordinate')
    combo_fig.supylabel('Y Coordinate')

    exp_x_limits, exp_y_limits = expand_limits(original_graph.max_xpos, original_graph.max_ypos)
    
    generation_left = get_left_generation(title_left, generation)

    set_plot_axis(sub_axes[0], original_graph, title_left, generation_left, c, exp_x_limits, exp_y_limits)
    set_plot_axis(sub_axes[1], optimized_graph, title_right, generation, c, exp_x_limits, exp_y_limits)

    combo_fig.show()

    return

def get_left_generation(title_left, generation):
    if "Original" in title_left:
        return 0
    else:
        return generation

def set_plot_axis(axis, graph, title, generation, c, x_limits, y_limits):

    # Plot line collections
    line_collection = mc.LineCollection(graph.segments, colors=c, linewidths=2)
    graph_node_coords = graph.node_coordinates

    axis.set_title(title, fontsize=14)
    axis.margins(0.1)
    axis.add_collection(line_collection)
    axis.set_xlim(x_limits[0], x_limits[1])
    axis.set_ylim(y_limits[0], y_limits[1])

    # Set annotations
    # Node Circles
    add_circles(axis, graph_node_coords)
    annotate_nodes(axis, graph)
    # axis.autoscale()

    annotate_text = "Fitness: " + str(graph.num_line_crossings) + " Crossings"
    axis.annotate(annotate_text, (int(x_limits[1]/2), y_limits[1]-5))

    if generation >= 0:
        annotate_text = "Generation: " + str(generation)
        axis.annotate(annotate_text, (int(x_limits[1]/5), y_limits[1]-5))

    return


def animate_evolution(evolution_diagrams):

    max_x, max_y = pop.get_limits(evolution_diagrams)

    fig, ax = pl.subplots()
    for frame in evolution_diagrams:

        diagram_to_plot = frame[0][1]
        generation = frame[1]
        fig, ax = plot_segments(fig, ax, diagram_to_plot, max_x, max_y, generation)

        plt.draw()
        plt.pause(0.35)

    return

def expand_limits(max_x, max_y):
    # Add ten percent to max/min for x and y maximum graph node positions
    X_MIN = 0 - int(0.1*max_x)
    X_MAX = max_x + int(0.1*max_x)

    Y_MIN = 0 - int(0.1*max_y)
    Y_MAX = max_y + int(0.1*max_y)

    x_limits = (X_MIN, X_MAX)
    #y_limits = (Y_MIN, Y_MAX)
    y_limits = (Y_MIN, Y_MAX)

    return x_limits, y_limits

def plot_segments(fig, ax, graph, max_x, max_y, generation):

    c = np.array([(0, 0, 1, 1)])

    ax.clear()
    plt.title("Network Graph Generations")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")

    x_limits, y_limits = expand_limits(max_x, max_y)

    set_plot_axis(ax, graph, "Network Graph Generations", generation, c, x_limits, y_limits)

    return fig, ax




def plot_graph(graph):

    fig, ax = pl.subplots()

    net_segments = graph.segments
    node_coordinates = graph.node_coordinates

    c = np.array([(0, 0, 1, 1)])
    lc = mc.LineCollection(net_segments, colors=c, linewidths=2)

    plt.title("Bipartite Graph")

    ax.add_collection(lc)
    add_circles(ax, node_coordinates)
    ax.set_title("Bipartite Graph")
    ax.set_xlabel("X Coordinate")
    ax.set_ylabel("Y Coordinate")

    ax.autoscale()
    ax.margins(0.1)

    annotate_nodes(ax, graph)
    
    return


def add_circles(ax, node_coordinates):
    for node_coordinate in node_coordinates:
        add_circle = plt.Circle(node_coordinate, 2, color='blue', )
        ax.add_patch(add_circle)
    return

def annotate_nodes(ax, bigraph):
    annotation_shift = 3
    level_dict = bigraph.level_dict
    graph_network = bigraph.network
    for level in level_dict.keys():
        for node_number in level_dict[level]:
            node = graph_network.nodes()[node_number]
            if level == 0:
                node_pos = (node["x_pos"]-annotation_shift, node["y_pos"])
            else:
                node_pos = (node["x_pos"]+annotation_shift, node["y_pos"])

            ax.annotate(str(node_number), node_pos, color='green', weight='bold')

    return


def print_fitnesses(population):
    for i, ind in enumerate(population.population):
        print("Ind: {}  Fitness: {}  ".format(i, ind[0]))
    return