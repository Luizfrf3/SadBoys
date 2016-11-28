#!/usr/bin/python2
# -*- coding: utf-8 -*-
import sys

from flask import Flask
from flask import render_template
from flask import jsonify, json, Response, request

from graph import initial_graph, user_graph, user_tweet_graph
from map import states_heatmap, tweets_heatmap

sys.path.insert(0, '../')
import sent_analysis.apply_demo as apde


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def view_analysis():
    if request.method == 'POST':
        search = str(request.form['search'])
        av = apde.analyse(str(request.form['search']))
        print(str(av))
        return render_template("index.html", av = av, search = search)
    if request.method == 'GET':
        return render_template("index.html")

@app.route("/graph")
def graph():
    return render_template('graph.html')

@app.route("/graph/data/initial")
def graph_complete():
    n, e = initial_graph()
    return jsonify(nodes = n, edges = e)

# To acess a certain node date just go to graph
@app.route("/graph/data/follows/<int:user_id>")
def graph_complete_user_f(user_id):
    n, e = user_graph(int(user_id))
    return jsonify(nodes = n, edges = e)

# To acess a certain node date just go to graph
@app.route("/graph/data/tweets/<int:user_id>")
def graph_complete_user_t(user_id):
    n, e = user_tweet_graph(int(user_id))
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

@app.route("/map/data/tweets/happy")
def map_tweets_happy():
    t = tweets_heatmap()
    return jsonify(t)

@app.route("/map/data/tweets/sad")
def map_tweets_sad():
    t = tweets_heatmap()
    return jsonify(t)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
