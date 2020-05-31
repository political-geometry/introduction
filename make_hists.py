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
c1, c2 = [x/255 for x in [166,206,227]], [x/255 for x in [31,120,180]]

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
    seatsPRES = list(pd.read_csv("{}/rundata_{}.csv".format(s, "PRES16"))["PRES16_Dseats"])
    seatsSEN = list(pd.read_csv("{}/rundata_{}.csv".format(s, "SEN16"))["SEN16_Dseats"])
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(8,4))
    ax1.hist(
        seatsPRES,
        bins = [
            x-0.5 for x in range(min(seatsSEN+seatsPRES), max(seatsSEN+seatsPRES)+2)
        ],
        color=c1,
        density=True
    )
    ax1.axvline(
        statwideD[s][0]/100*num_districts[s],
        c='g',
        linestyle='--'
    )
    ax1.set_xticks([
        x for x in range(min(seatsSEN+seatsPRES), max(seatsSEN+seatsPRES)+1)
    ])
    ax1.set_title("{} in {} ({})".format("PRES16",s, num_districts[s]))

    ax2.hist(
        seatsSEN,
        bins = [
            x-0.5 for x in range(min(seatsSEN+seatsPRES), max(seatsSEN+seatsPRES)+2)
        ],
        color=c2,
        density=True
    )
    ax2.axvline(
        statwideD[s][1]/100*num_districts[s],
        c='g',
        linestyle='--'
    )
    ax2.set_xticks([
        x for x in range(min(seatsSEN+seatsPRES), max(seatsSEN+seatsPRES)+1)
    ])
    ax2.set_title("{} in {} ({})".format("SEN16",s, num_districts[s]))

    fig.savefig(
        "{}.png".format(s),
        dpi=150,
        bbox_inches="tight"
    )
    plt.close()

for s in states12:
    seatsPRES = list(pd.read_csv("{}/rundata_{}.csv".format(s, "PRES12"))["PRES12_Dseats"])
    seatsSEN = list(pd.read_csv("{}/rundata_{}.csv".format(s, "SEN12"))["SEN12_Dseats"])
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(8,4))
    ax1.hist(
        seatsPRES,
        bins = [
            x-0.5 for x in range(min(seatsSEN+seatsPRES), max(seatsSEN+seatsPRES)+2)
        ],
        color=c1,
        density=True
    )
    ax1.axvline(
        statwideD[s][0]/100*num_districts[s],
        c='g',
        linestyle='--'
    )
    ax1.set_xticks([
        x for x in range(min(seatsSEN+seatsPRES), max(seatsSEN+seatsPRES)+1)
    ])
    ax1.set_title("{} in {} ({})".format("PRES12",s, num_districts[s]))

    ax2.hist(
        seatsSEN,
        bins = [
            x-0.5 for x in range(min(seatsSEN+seatsPRES), max(seatsSEN+seatsPRES)+2)
        ],
        color=c2,
        density=True
    )
    ax2.axvline(
        statwideD[s][1]/100*num_districts[s],
        c='g',
        linestyle='--'
    )
    ax2.set_xticks([
        x for x in range(min(seatsSEN+seatsPRES), max(seatsSEN+seatsPRES)+1)
    ])
    ax2.set_title("{} in {} ({})".format("SEN12",s, num_districts[s]))

    fig.savefig(
        "{}.png".format(s),
        dpi=150,
        bbox_inches="tight"
    )
    plt.close()
