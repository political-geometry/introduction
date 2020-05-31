import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import math
import sys, os
from itertools import product

states16 = ["GA",  "MD", "NC",  "OH",  "OR",  "PA",   "WI"]
states12 = ["TX", "MA"]

statwideD = {
        "GA": [47.33, 42.82],
        "MD": [57.82, 56.96],
        "NC": [48.02, 46.98],
        "OH": [45.74, 39.04],
        "OR": [56.16, 62.93],
        "PA": [49.65, 49.28],
        "WI": [49.59, 48.27],
        "TX": [41.99, 41.85],
        "MA": [61.79, 53.78],
}

num_districts = {
    "GA": 14,
    "MD": 8,
    "NC": 13,
    "OH": 16,
    "OR": 5,
    "PA": 18,
    "WI": 8,
    "TX": 36,
    "MA": 9,
}

for s in states16:
    seats = list(pd.read_csv("{}/rundata_{}.csv".format(s, "PRES16"))["PRES16_Dseats"])
    print("{}_PRES16_mean = ".format(s), np.mean(seats))
    v = [len([x for x in seats if x == i]) for i in range(num_districts[s]+1)]
    print("{}_{} = np.array({})".format(s, "PRES16", v))
    seats = list(pd.read_csv("{}/rundata_{}.csv".format(s, "SEN16"))["SEN16_Dseats"])
    v = [len([x for x in seats if x == i]) for i in range(num_districts[s]+1)]
    print("{}_{} = np.array({})".format(s, "SEN16", v))

for s in states12:
    seats = list(pd.read_csv("{}/rundata_{}.csv".format(s, "PRES12"))["PRES12_Dseats"])
    v = [len([x for x in seats if x == i]) for i in range(num_districts[s]+1)]
    print("{}_{} = np.array({})".format(s, "PRES12", v))
    seats = list(pd.read_csv("{}/rundata_{}.csv".format(s, "SEN12"))["SEN12_Dseats"])
    v = [len([x for x in seats if x == i]) for i in range(num_districts[s]+1)]
    print("{}_{} = np.array({})".format(s, "SEN12", v))
