import pandas as pd
import skcriteria as skc
import numpy as np
from skcriteria.preprocessing import invert_objectives, scalers
from skcriteria.madm import simple

def get_id(key):
    criterion_key = {
        'Name' : 'name',
        'Elastic Modulus' : 'elastic_mod',
        'Yield Strength' : 'yield_strength',
        'Cost' : 'cost',
        'Ultimate Strength': 'ult_strength',
        'Machineability' : 'machineability'
    }

    if type(key) == list:
        result = [criterion_key.get(k) for k in key]
        result = [x for x in result if x != None]
        return result

    return criterion_key.get(key)

def rank_materials(criterions, weights, raw_data):
    raw_dataframe = pd.DataFrame(raw_data)

    #Filter out inconsequential data
    formData = {}
    for i in range(5):
        if criterions[i] != '' and weights[i] != 0:
            formData[criterions[i]] = weights[i]  

    #Reformat and normalize weights
    np_weights = np.asarray(list(formData.values()))
    np_weights = np.divide(weights,10)

    #get objectives from weights
    objectives = []
    for weight in np_weights:
        if weight < 0:
            objectives.append(min)
        elif weight > 0:
            objectives.append(max)


    criterion_ids = get_id(list(formData.keys()))

    df = raw_dataframe.loc[:, criterion_ids]        #type: ignore

    # we use the built-in function as aliases
    row_id =  list(raw_dataframe.loc[:, 'name'])
    dm = skc.mkdm(
        df.to_numpy(),
        objectives= objectives,
        weights= weights,
        alternatives = row_id,
        criteria= list(formData.keys())
    )

    #SKC handles maximization or minimization only best , so we invert the third row to be a maximization problem 
    #maximization is preferable to minimizationm
    inverter = invert_objectives.InvertMinimize()
    dmt = inverter.transform(dm)

    #normalizes values
    scaler = scalers.SumScaler(target="both")
    dmt = scaler.transform(dmt)

    #Get rank
    dec = simple.WeightedSumModel()
    rank = dec.evaluate(dmt)  # we use the tansformed version of the data

    df_with_score = raw_dataframe.assign(Score = rank.e_.score).assign(Rank = rank.rank_)
    SortedDF = df_with_score.sort_values(by = 'Score', ascending = False)

    return SortedDF
