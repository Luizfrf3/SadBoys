#!/usr/bin/python2
# -*- coding: utf-8 -*-
import random, json

# These are the colors for the nodes (we can change then)
# i thought about using the groups to add colors to the nodes
colors = {
    0: "rgb(0, 28, 247)",
    1: "rgb(0, 94, 247)",
    3: "rgb(0, 140, 247)",
    2: "rgb(0, 164, 247)",
    4: "rgb(0, 189, 247)",
    5: "rgb(247, 247, 0)",
    6: "rgb(247, 197, 0)",
    7: "rgb(247, 156, 0)",
    8: "rgb(247, 119, 0)",
    9: "rgb(247, 65, 0)",
}

## The functions below are just for generating simulated graphs ##

# generates n_nodes for a graph
# returns a list of dict containing nodes, and a node is:
# node:
# {
# "color": rgb()
# "group": a int,
# "id": an id,
# "label": a name
# "attributes": {...}
# "size": a size (int)
# }
def generate_nodes(n_id ,n_nodes):
    nodes = []
    for i in range(n_nodes):
        node = dict()
        color = dict()
        highlight = dict()
        hover = dict()

        # Creating node
        group = i%10
        node['id'] = str(i)
        node['label'] = str(i)
        if(n_id == i):
            node['size'] = 15
        else:
            node['size'] = group
        node['group'] = group
        node['attributes'] = {}

        # Defining the color based on the group
        node['color'] = colors[group]

        #append the node on the list
        nodes.append(node)
    return nodes


# generates "random" edges for a n_nodes
# returns a list of edges:
# edge {
#   source: n_id
#   target: node
#   size: a size (int)
#   attributes: any atributes wanted (must be a dict)
# }
def generate_edges(n_id, n_nodes):
    edges = []
    # conect all the nodes on the centered (n_id)
    for j in range(n_nodes):
        edge = dict()
        if j != 0:
            edge['source'] = str(n_id)
            if j != n_id:
                edge['target'] = str(j)
                edge['size'] = 1
                edge['attributes'] = {}
                edges.append(edge)

    return edges

# generates a graph with n_nodes
def generate_graph(n_id, n_nodes):
    nodes = generate_nodes(n_id, n_nodes)
    edges = generate_edges(n_id, n_nodes)
    return nodes, edges
