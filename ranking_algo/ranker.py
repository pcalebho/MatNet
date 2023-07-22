import pandas as pd
import skcriteria as skc
import numpy as np
import matplotlib.pyplot as plt
import json
import yaml

from skcriteria.preprocessing import invert_objectives, scalers
from skcriteria.madm import simple

with open('webscraper/results_files/AISI_steels_fakedata.yaml','r') as stream:
    try:
        raw_data = yaml.safe_load(stream)
    except FileNotFoundError:
        raise FileNotFoundError

df = pd.DataFrame(raw_data)
print(df)

# 2 alternatives by 3 criteria
matrix = [
    [1, 2, 3],  # alternative 1
    [4, 5, 6],  # alternative 2
]

# let's says the first two alternatives are
# for maximization and the last one for minimization
objectives = [max, max, min]

# we use the built-in function as aliases
dm = skc.mkdm(
    matrix,
    objectives,
    alternatives=["car 0", "car 1"],
    weights=[0.5, 0.05, 0.45],
    criteria=["autonomy", "comfort", "price"],
)
dm = dm.copy(alternatives=["VW", "Ford"])


#SKC handles maximization or minimization only best , so we invert the third row to be a maximization problem 
#maximization is preferable to minimizationm
inverter = invert_objectives.InvertMinimize()
dmt = inverter.transform(dm)
print(dmt)

#normalizes values
scaler = scalers.SumScaler(target="both")
dmt = scaler.transform(dmt)

dec = simple.WeightedSumModel()
rank = dec.evaluate(dmt)  # we use the tansformed version of the data