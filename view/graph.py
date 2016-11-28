#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Module to deal with the graph data
# Authors: Henrique
#          Thiago
import random, json, sys

sys.path.insert(0, '../')
from BD.graph_dataset import graph_dataset

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

def initial_graph():
    # Creates a new object to deal with bd
    db = graph_dataset()
    initial_user_id = db.getUserID('justinbieber')
    user_info, user_follows = db.getFollows(initial_user_id)

    nodes = []
    edges = []

    att = dict()
    att['tw_name'] = str(user_info['screen_name']);
    att['img_url'] = str(user_info['profile_image']);
    att['total_follows'] = int(len(user_follows))
    # Contar todos os usuarios que essa pessoa segue que sao de tal jeito
    att['0'] = int(1)
    att['1'] = int(1)
    att['2'] = int(1)
    att['3'] = int(1)
    att['4'] = int(1)
    att['5'] = int(1)
    att['6'] = int(1)
    att['7'] = int(1)
    att['8'] = int(1)
    att['9'] = int(1)

    # Creates the nodes
    main_user = create_node(user_info['id'], user_info['screen_name'],
                            user_info['label'], 16, att)

    nodes.append(main_user)
    for user in user_follows:
        att = dict()
        att['tw_name'] = str(user['screen_name']);
        nodes.append(create_node(user['id'], user['screen_name'],
                                 user['label'], 6 ,att))
    # Creates the edges
    for node in nodes[1:]:
        edges.append(create_edge(nodes[0]['id'], node['id']))

    for user in user_follows:
        edges_aux = []
        nodes_aux = []
        user_info, user_follows2 = db.getFollows(user['id'])
        for user2 in user_follows2:
            att = dict()
            att['tw_name'] = str(user['screen_name']);
            node2 = create_node(user2['id'], user2['screen_name'],
                                user2['label'], 6, att)

            # Verifica para não entrar em loop
            flag = 0
            for node_aux in nodes_aux:
                if node_aux['id'] == node2['id']:
                    flag = 1
            for node_aux in nodes:
                if node_aux['id'] == node2['id']:
                    flag = 1
            if flag == 0:
                nodes_aux.append(node2)

        nodes = nodes + nodes_aux

        for node in nodes_aux:
            edges.append(create_edge(user_info['id'], node['id']))


    return nodes, edges


def user_graph(user_id):
    # Creates a new object to deal with bd
    db = graph_dataset()
    user_info, user_follows = db.getFollows(user_id)

    att = dict()
    att['tw_name'] = str(user_info['screen_name']);
    att['img_url'] = str(user_info['profile_image']);
    att['total_follows'] = int(len(user_follows))
    # Contar todos os usuarios que essa pessoa segue que sao de tal jeito
    att['0'] = int(1)
    att['1'] = int(1)
    att['2'] = int(1)
    att['3'] = int(1)
    att['4'] = int(1)
    att['5'] = int(1)
    att['6'] = int(1)
    att['7'] = int(1)
    att['8'] = int(1)
    att['9'] = int(1)
    # Creates the nodes
    main_user = create_node(user_info['id'], user_info['screen_name'],
                            user_info['label'], 16, att)

    nodes = []
    edges = []
    nodes.append(main_user)


    for user in user_follows:
        att = dict()
        att['tw_name'] = str(user['screen_name']);
        nodes.append(create_node(user['id'], user['screen_name'],
                                 user['label'], 6 ,att))
    # Creates the edges
    for node in nodes[1:]:
        edges.append(create_edge(nodes[0]['id'], node['id']))

    # Adiciona os usuário que os usuario que ele segue seguem
    for user in user_follows:
        edges_aux = []
        nodes_aux = []
        user_info, user_follows2 = db.getFollows(user['id'])
        for user2 in user_follows2:
            att = dict()
            att['tw_name'] = str(user['screen_name']);
            node2 = create_node(user2['id'], user2['screen_name'],
                                user2['label'], 6, att)

            # Verifica para não entrar em loop
            flag = 0
            for node_aux in nodes_aux:
                if node_aux['id'] == node2['id']:
                    flag = 1
            for node_aux in nodes:
                if node_aux['id'] == node2['id']:
                    flag = 1
            if flag == 0:
                nodes_aux.append(node2)

        nodes = nodes + nodes_aux

        for node in nodes_aux:
            edges.append(create_edge(user_info['id'], node['id']))


    return nodes, edges

# Retorna um grafo contendo um usuário no centro e os tweets dele ao lado
def user_tweet_graph(user_id):
    nodes = []
    edges = []

    # Creates a new object to deal with bd
    db = graph_dataset()
    user_info, user_follows = db.getFollows(user_id)
    tweets = db.getTweets(user_id)

    att = dict()
    att['tw_name'] = str(user_info['screen_name']);
    att['img_url'] = str(user_info['profile_image']);
    att['dcrp']= str(user_info['description']);
    #att['total_follows'] = int(size(user_follows))
    # Contar todos os usuarios que essa pessoa segue que sao de tal jeito
    att['0'] = int(1)
    att['1'] = int(1)
    att['2'] = int(1)
    att['3'] = int(1)
    att['4'] = int(1)
    att['5'] = int(1)
    att['6'] = int(1)
    att['7'] = int(1)
    att['8'] = int(1)
    att['9'] = int(1)

    # Creates the primary node
    main_user = create_node(user_info['id'], user_info['screen_name'],
                            user_info['label'], 16, att)

    nodes.append(main_user);

    # now we create the tweets nodes and edges
    i=0
    for tweet in tweets:
        # We should add att (the tweet text) to this
        #att = dict()
        #att['tw_name'] = str(user['screen_name']);
        nodes.append(create_node(i, str(i), tweet['label'], 3))
        i = i + 1

    for node in nodes[1:]:
        edges.append(create_edge(nodes[0]['id'], node['id']))

    return nodes, edges


# Creates a node containing the information below
def create_node(id, label, depression, size = 6, att = {}):
    node = dict()

    group = int(depression*10)
    node['id'] = str(id)
    node['label'] = str(label)
    node['size'] = int(size)
    node['group'] = group
    node['attributes'] = att
    # Defining the color based on the group
    node['color'] = colors[group]

    return node

# Creates an edge from -> to
def create_edge(fr, to, size = 1, att = {}):
    edge = dict()

    edge['source'] = str(fr)
    edge['target'] = str(to)
    edge['size'] = int(1)
    edge['attributes'] = att

    return edge
