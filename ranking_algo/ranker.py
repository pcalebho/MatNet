import pandas as pd
import skcriteria as skc
import numpy as np
import yaml
from skcriteria.preprocessing import invert_objectives, scalers
from skcriteria.madm import simple

CRITERION_KEY = {
    "Density(g/cc)": 'density',
    "Yield Strength(MPa)": 'tensile_strength_yield',
    "Ultimate Strength(MPa)": 'tensile_strength_ultimate',
    "Elastic Modulus(GPa)": 'modulus_of_elasticity',
    "Brinell Hardness": 'hardness_brinell',
    "Machinability(%)": 'machinability',
    "Specific Heat Capacity(J/g-°C)": 'specific_heat_capacity',
    "*Cost": 'cost'
}

def get_id(key):
    if type(key) == list:
        result = [CRITERION_KEY.get(k) for k in key]
        result = [x for x in result if x != None]
        return result

    return CRITERION_KEY.get(key)

def get_key(label):
    KEY = {
        "Density(g/cc)": 'physical_properties.density',
        "Yield Strength(MPa)": 'mechanical_properties.tensile_strength_yield',
        "Ultimate Strength(MPa)": 'mechanical_properties.tensile_strength_ultimate',
        "Elastic Modulus(GPa)": 'mechanical_properties.modulus_of_elasticity',
        "Brinell Hardness": 'mechanical_properties.hardness_brinell',
        "Machinability(%)": 'mechanical_properties.machinability',
        "Specific Heat Capacity(J/g-°C)": 'thermal_properties.specific_heat_capacity',
        "*Cost": 'cost'
    }

    # if type(label) == list:
    #     result = [CRITERION_KEY.get(k) for k in key]
    #     result = [x for x in result if x != None]
    #     return result

    return KEY.get(label)

def rank_materials(criterions, weights, raw_data):
    raw_dataframe = pd.DataFrame(raw_data)

    #Filter out inconsequential data
    formData = {}
    for i in range(len(weights)):
        if weights[i] != 0:
            formData[criterions[i]] = weights[i]  
    
    if formData == {}:
        return raw_dataframe

    #Reformat and normalize weights
    np_weights = np.asarray(list(formData.values()))
    np_weights = np.divide(np_weights,10)

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
        weights= np_weights.tolist(),
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

if __name__ == '__main__':
    #for unit testing
    with open('C:/Users/ttrol/CodingProjects/MatNet/webscraper/results_files/AISI_steels_fakedata.yaml','r') as stream:
        try:
            raw_data = yaml.safe_load(stream)
        except FileNotFoundError:
            raise FileNotFoundError
        
    criterions = [ 'Yield Strength', 'Cost', 'Machineability', 'Elastic Modulus', 'Ultimate Strength']
    raw_weights = [10, -10, 3, 0, 0]
    
    df = rank_materials(criterions, raw_weights, raw_data)
    print(df)