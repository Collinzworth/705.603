import math
import numpy as np
from fast_crossing import FastCrossing

class Bi_Graph:

    def __init__(self, network):
        
        self.network = network

        self.max_xpos = -math.inf
        self.max_level = -math.inf
        self.max_ypos = -math.inf

        self.set_segments()
        self.set_node_dict_attr()
        self.calc_line_crossings()

    def fc_create(self):

        network = self.network
        fc = FastCrossing()
    
        for edge in network.edges():
            node1 = network.nodes()[edge[0]]
            node2 = network.nodes()[edge[1]]

            pos1 = node1["pos"]
            pos2 = node2["pos"]

            fc.add_polyline(np.array([[pos1[0], pos1[1]], [pos2[0], pos2[1]]]))
            
        fc.finish()

        self.fc = fc

        return

    def calc_line_crossings(self):
        self.crossings = self.fast_cross()
        self.num_line_crossings = len(self.crossings)
        return

    def set_node_dict_attr(self):
        network = self.network
        xpos_dict = {}
        ypos_dict = {}
        level_dict = {}

        self.max_xpos = -math.inf
        self.max_level = -math.inf
        self.max_ypos = -math.inf

        node_coordinates = []

        for node_num in network.nodes():
            node = network.nodes()[node_num]
            node_coordinates.append(node["pos"])

            try:
                xpos_dict[node["x_pos"]].append(node_num)
            except KeyError:
                xpos_dict[node["x_pos"]] = [node_num]

            try:
                ypos_dict[node["y_pos"]].append(node_num)    
            except KeyError:
                ypos_dict[node["y_pos"]] = [node_num]

            try:            
                level_dict[node["level"]].append(node_num)
            except KeyError:
                level_dict[node["level"]] = [node_num]

            self.set_max_pos(node)

        self.xpos_dict = xpos_dict
        self.ypos_dict = ypos_dict
        self.level_dict = level_dict
        self.node_coordinates = node_coordinates

        return

    def set_max_pos(self, node):
        
        if node["x_pos"] > self.max_xpos:
            self.max_xpos = node["x_pos"]
            
        if node["y_pos"] > self.max_ypos:
            self.max_ypos = node["y_pos"]

        if node["level"] > self.max_level:
            self.max_level = node["level"]

    def get_nodes_by_xcoord(self):
        return self.xpos_dict
    

    def set_segments(self):
        network = self.network
        segment_positions = []
        for edge in network.edges():
            position_tuple = []
            for insert_node_name in edge:
                insert_node = network.nodes()[insert_node_name]
                position_tuple.append(insert_node["pos"])

            position_tuple = sorted(position_tuple, key=lambda x: x[0])
            position_tuple = tuple(position_tuple)
            segment_positions.append(position_tuple)

        self.segments =  sorted(segment_positions, key=lambda x: x[0][0])

        return



    """

    Fast Crossing Test: https://github.com/cubao/fast-crossing

    """

    def fast_cross(self):

        network = self.network

        fc = FastCrossing()

        for edge in network.edges():
            node1 = network.nodes()[edge[0]]
            node2 = network.nodes()[edge[1]]

            pos1 = node1["pos"]
            pos2 = node2["pos"]

            fc.add_polyline(np.array([[pos1[0], pos1[1]], [pos2[0], pos2[1]]]))

        fc.finish()

        return fc.intersections()