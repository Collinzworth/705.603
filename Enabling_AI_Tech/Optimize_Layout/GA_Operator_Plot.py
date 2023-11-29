import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import Optimize_Layout.GA_Visualization as gv

class GA_Operator_Plot:

    def __init__(self, title, title_1, title_2, title_3, title_4):
        self.title = title
        self.title_1 = title_1
        self.title_2 = title_2
        self.title_3 = title_3
        self.title_4 = title_4
        self.init_ga_operator_plot()


    def update_plot(self, parents, offspring):

        c = np.array([(0, 0, 1, 1)])

        parent1 = parents[0]
        parent2 = parents[1]

        parent1_lc = mc.LineCollection(parent1.segments, colors=c, linewidths=2)
        parent2_lc = mc.LineCollection(parent2.segments, colors=c, linewidths=2)

        parent1_nodes = parent1.node_coordinates
        parent2_nodes = parent2.node_coordinates

        offspring1 = offspring[0]
        offspring2 = offspring[1]

        offspring1_lc = mc.LineCollection(offspring1.segments, colors=c, linewidths=2)
        offspring2_lc = mc.LineCollection(offspring2.segments, colors=c, linewidths=2)

        offspring1_nodes = parent1.node_coordinates
        offspring2_nodes = parent2.node_coordinates

        self.sub_axes[0][0].clear()
        self.sub_axes[0][0].set_title(self.title_1, fontsize=14)
        self.sub_axes[0][0].add_collection(parent1_lc)
        gv.add_circles(self.sub_axes[0][0], parent1_nodes)
        gv.annotate_nodes(self.sub_axes[0][0], parent1)
        self.sub_axes[0][0].autoscale()

        self.sub_axes[0][1].clear()
        self.sub_axes[0][1].set_title(self.title_2, fontsize=14)
        self.sub_axes[0][1].add_collection(parent2_lc)
        gv.add_circles(self.sub_axes[0][1], parent2_nodes)
        gv.annotate_nodes(self.sub_axes[0][1], parent2)

        self.sub_axes[1][0].clear()
        self.sub_axes[1][0].set_title(self.title_3, fontsize=14)
        self.sub_axes[1][0].add_collection(offspring1_lc)
        gv.add_circles(self.sub_axes[1][0], offspring1_nodes)
        gv.annotate_nodes(self.sub_axes[1][0], offspring1)

        self.sub_axes[1][1].clear()
        self.sub_axes[1][1].set_title(self.title_4, fontsize=14)
        self.sub_axes[1][1].add_collection(offspring2_lc)
        gv.add_circles(self.sub_axes[1][1], offspring2_nodes)
        gv.annotate_nodes(self.sub_axes[1][1], offspring2)

        return self

    def init_ga_operator_plot(self):

        self.combo_fig, self.sub_axes = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)

        self.combo_fig.suptitle(self.title, fontsize=24)
        self.combo_fig.supxlabel('X Coordinate')
        self.combo_fig.supylabel('Y Coordinate')

        self.sub_axes[0][0].set_title(self.title_1, fontsize=14)
        self.sub_axes[0][0].margins(0.1)

        self.sub_axes[0][1].set_title(self.title_2, fontsize=14)
        self.sub_axes[0][1].margins(0.1)

        self.sub_axes[1][0].set_title(self.title_3, fontsize=14)
        self.sub_axes[1][0].margins(0.1)

        self.sub_axes[1][1].set_title(self.title_4, fontsize=14)
        self.sub_axes[1][1].margins(0.1)

        self.combo_fig.show()

        return