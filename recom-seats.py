from gerrychain import Graph, Election, updaters, Partition, constraints, MarkovChain
from gerrychain.updaters import cut_edges
from gerrychain.proposals import recom
from gerrychain.tree import recursive_tree_part
from gerrychain.accept import always_accept
import numpy as np
from functools import partial
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import math
import pickle
import sys, os, datetime
from datetime import datetime
import networkx as nx
from itertools import product

#User entered parameters for the run
steps = int(sys.argv[1]) #recom steps
INTERVAL = int(sys.argv[2]) #sampling interval
outputfolder = sys.argv[3] #outputfolder
os.makedirs(outputfolder, exist_ok=True)
file = open("{}/specs.txt".format(outputfolder),"w") #dump specs to file
file.write("{} \n".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
for x in sys.argv:
    file.write("{} \n".format(x))
file.close()

#State and district level parameters -- change these for a new state
num_districts = int(sys.argv[4])
election_names = [sys.argv[5]]
election_columns = [
    [sys.argv[6], sys.argv[7]],
] #DEM, REP
pop_tol = 0.02
pop_col = sys.argv[8]
pre_file_shape = sys.argv[9]

if pre_file_shape.endswith(".shp"):
    graph = Graph.from_file(pre_file_shape)
else:
    graph = Graph.from_json(pre_file_shape)


#Set up and start the chain
print("Shapefile loaded, graph created and islands fixed...")
print("Connected components: {}, graph size: {}".format(nx.number_connected_components(graph), len(graph)))
print("Sample node from graph:\n", graph.nodes[np.random.choice(graph.nodes)])
total_population = sum([graph.nodes[n][pop_col] for n in graph.nodes()])
print("Shapefiles loaded and ready to run ReCom...")
for x in graph.nodes: #fix NaN
    for index, e in enumerate(election_names):
        for k in election_columns[index]:
            if isinstance(graph.nodes[x][k], str):
                graph.nodes[x][k] = float(graph.nodes[x][k].replace(',',''))
            if math.isnan(graph.nodes[x][k]):
                graph.nodes[x][k] = 0
                print("Fixed NaN in ", k, "at ", x)
for k in [num_districts]:
    rundata = pd.DataFrame()
    seats = []
    percents = []

    pop_target = total_population/k
    myproposal = partial(recom, pop_col=pop_col, pop_target=pop_target, epsilon=pop_tol, node_repeats=10)

    #updaters
    myupdaters = {
        "population": updaters.Tally(pop_col, alias="population"),
        "cut_edges": cut_edges,
    }
    elections = [
        Election(
            election_names[i],
            {"Democratic": election_columns[i][0], "Republican": election_columns[i][1]},
        )
        for i in range(len(election_names))
    ]
    election_updaters = {election.name: election for election in elections}
    myupdaters.update(election_updaters)

    #initial partition
    print("Creating seed with", k, "districts.")
    dev = pop_tol*pop_target + 1
    while dev > pop_tol*pop_target:
        print(".", end="")
        initial_ass = recursive_tree_part(graph, range(k), pop_target, pop_col, pop_tol, node_repeats=10)
        initial_partition = Partition(graph, initial_ass, myupdaters)
        dev = max([np.abs(initial_partition["population"][d] - pop_target) for d in initial_partition.parts])
    dev = max([np.abs(initial_partition["population"][d] - pop_target) for d in initial_partition.parts])
    print(" Using initial", k, "districts with population deviation = ", 100*dev/pop_target, "% of ideal.")

    #chain
    compactness_bound = constraints.UpperBound(
        lambda p: len(p["cut_edges"]),
        2*len(initial_partition["cut_edges"])
    )
    myconstraints = [
        constraints.within_percent_of_ideal_population(initial_partition, pop_tol),
        compactness_bound
    ]
    chain = MarkovChain(
        proposal=myproposal,
        constraints=myconstraints,
        accept=always_accept,
        initial_state=initial_partition,
        total_steps=steps
    )

    #run ReCom
    for index, step in enumerate(chain):
        #store some plans
        if index%INTERVAL == 0:
            print(index, end=" ")
            #record seats
            for e in election_names:
                seats.append(step[e].seats("Democratic"))
            #record percents
            for e in election_names:
                percents.append(sorted(step[e].percents("Democratic")))

rundata["{}_Dseats".format(election_names[0])] = seats
for i in range(len(percents[0])):
    rundata["{}_Dperc{}".format(election_names[0],i)] = [x[i] for x in percents]
rundata.to_csv("{}/rundata_{}.csv".format(outputfolder, election_names[0]))
