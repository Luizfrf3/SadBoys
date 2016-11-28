#!/usr/bin/python2
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import jsonify, json, Response

from graph import generate_graph, generate_edges, generate_nodes, initial_graph, user_graph
from map import states_heatmap, tweets_heatmap

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/graph")
def graph():
    return render_template('graph.html')

@app.route("/graph/data/initial")
def graph_complete():
    n, e = initial_graph()
    return jsonify(nodes = n, edges = e)

# To acess a certain node date just go to graph
@app.route("/graph/data/<int:user_id>")
def graph_complete_user(user_id):
    n, e = user_graph(int(user_id))
    return jsonify(nodes = n, edges = e)

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/map/data/states")
def map_states():
    s = states_heatmap()
    return jsonify(s)

@app.route("/map/data/tweets")
def map_tweets():
    t = tweets_heatmap()
    return jsonify(t)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
