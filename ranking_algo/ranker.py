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
    "*Cost": 'cost',
    "Score (Rank)": "Score-rank"
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

    return KEY.get(label)



def rank_materials(form_data, raw_data):
    raw_dataframe = pd.DataFrame(raw_data)

    #Filter out inconsequential data           
    criterion_ids = get_id(list(form_data.keys()))
    objectives = []
    weights = []
    criterion_ids = []
    for key in form_data.keys():
        if form_data[key]['importance'] != 0:
            criterion_ids.append(get_id(key))
            objectives.append(form_data[key]['objective'])
            weights.append(form_data[key]['importance']/10)

    if not any(weights):
        return raw_dataframe


    df = raw_dataframe.loc[:, criterion_ids]      

    # we use the built-in function as aliases
    row_id =  list(raw_dataframe.loc[:, 'name'])
    dm = skc.mkdm(
        df.to_numpy(),
        objectives= objectives,
        weights= weights,
        alternatives = row_id,
        criteria= df.columns.tolist()
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
    
    array_x = rank.rank_ 
    array_y = [round(num*1000,3) for num in rank.e_.score]
    
    formatted_ranking = [f"{y} ({x})" for x, y in zip(array_x, array_y)]

    # df_with_score = raw_dataframe.assign(Rank = formatted_ranking)
    df_with_score = raw_dataframe.assign(Score_rank = formatted_ranking).assign(Score = array_y)
    SortedDF = df_with_score.sort_values(by = 'Score_rank', ascending = False)

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
    
    # df = rank_materials(criterions, raw_weights, raw_data)
    # print(df)