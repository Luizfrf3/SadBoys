#!/usr/bin/python2
# -*- coding: utf-8 -*-
# Module to deal with the graph data
# Authors: Henrique
#          Thiago

import random, json, sys

sys.path.insert(0, '../')
from BD.heatmap_dataset import heatmap_dataset

state_names = [
    "Alabama",
    "Alaska",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "District of Columbia",
    "Florida",
    "Georgia",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
]

def states_heatmap():
    db = heatmap_dataset()
    states = []
    for state in state_names:
        s_rates = db.getStateData(state)
        states.append(create_state_rates(state, s_rates['avg_l'],
                                         s_rates['suicide_rate'], s_rates['depressive_percentage'],
                                         s_rates['suicide_percentage']))

    return states


def states_heatmap_complete():
    db = heatmap_dataset()
    states = []
    for state in state_names:
        s_rates = db.getStateData(state)
        states.append(s_rates)

    return states

def tweets_heatmap():
    # Creates a new object to deal with bd
    db = heatmap_dataset()
    initial_tweets = db.getTweets()
    tweets = []

    for tweet in initial_tweets:
        tweets.append(create_tweets(tweet['coordinates'], tweet['label']))

    return tweets

def tweets_heatmap_happy():
    # Creates a new object to deal with bd
    db = heatmap_dataset()
    initial_tweets = db.getTweetsPositive()
    tweets = []

    for tweet in initial_tweets:
        tweets.append(create_tweets(tweet['coordinates'], tweet['label']))

    return tweets

def tweets_heatmap_sad():
    # Creates a new object to deal with bd
    db = heatmap_dataset()
    initial_tweets = db.getTweetsNegative()
    tweets = []

    for tweet in initial_tweets:
        tweets.append(create_tweets(tweet['coordinates'], tweet['label']))

    return tweets




# Creates states_rates
def create_state_rates(name, avg_label, suicide_rate, depressive_percentage, suicide_percentage):
    state_rates = dict()

    state_rates['name'] = str(name)
    state_rates['id_help'] = str(name.replace(" ", ""))
    state_rates['avg_label'] = float(avg_label)
    state_rates['suicide_rate'] = float(suicide_rate)
    state_rates['depressive_percentage'] = float(depressive_percentage)
    state_rates['suicide_percentage'] = float(suicide_percentage)

    return state_rates

# Creates tweets
def create_tweets(coord, label):
    tweets = dict()

    tweets['lat'] = float(coord[0])
    tweets['long'] = float(coord[1])
    tweets['label'] = float(label)

    return tweets
