import json
import jenkspy
import random
import bisect


def add_node(name, weight, avg_moods):
    global network, moods_to_break
    id = len(network["nodes"])
    network["nodes"].append(
        {"name": name, "weight": weight, "avg_mood": avg_moods[name]}
    )
    moods_to_break.append(avg_moods[name])


def add_edge(source, target, weight):
    global network
    network["links"].append({"source": source, "target": target, "weight": weight})


def build_network(nodes, edges, avg_moods, n=100):

    global network, moods_to_break, nodes_to_input

    ## build edges
    i = 0
    for key in edges:

        source, target = key.split("_")
        add_edge(source, target, edges[key])

        nodes_to_input[source] = nodes[source]
        nodes_to_input[target] = nodes[target]

        ## i must be > 2 for jenkyspy to work
        i += 1
        if i == n:
            break

    ## build nodes
    for key in nodes_to_input:
        add_node(key, nodes_to_input[key], avg_moods)

    ## build moods
    breaks = jenkspy.jenks_breaks(moods_to_break, nb_class=4)

    for node in network["nodes"]:
        m = node["avg_mood"]
        i = bisect.bisect_left(breaks, m)
        node["mood"] = i

    return network


def init_network():
    global network, moods_to_break, nodes_to_input

    network = {}
    network["nodes"] = []
    network["links"] = []

    moods_to_break = []
    nodes_to_input = {}


network = {}
moods_to_break = []
nodes_to_input = {}
