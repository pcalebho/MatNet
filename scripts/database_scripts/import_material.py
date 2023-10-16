import pandas as pd
import gspread
from gspread.exceptions import APIError
import json
import time
import random
from tqdm import tqdm
from pathlib import Path

gc = gspread.service_account(Path('google_auth.json'))

def exponential_backoff(func):
    max_backoff = 64    #seconds
    max_retries = 1000

    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    def inner(*args, **kwargs):
        retries = 0
 
        # storing time before function execution
        while retries <= max_retries:
            try:
                func(*args, **kwargs)
            except APIError:
                retries += 1
                backoff = min((2**retries) + random.random(), max_backoff)
                time.sleep(backoff)
            else:
                break
        
        if retries != 0:
            print(retries)
 
    return inner

def parse_gsheet(sheet_key: str, material_name: str):
    output = {}


    @exponential_backoff
    def open_sheet():
        global sheet
        sheet = gc.open_by_key(sheet_key)
        output['description'] = sheet.title
    
    open_sheet()
    
    @exponential_backoff
    def instantiate_sheets():
        global graph_sheet, mat_prop_sheet, equation_sheet, graph_raw, graph_sheet
        graph_sheet = sheet.worksheet('Graph Data')
        mat_prop_sheet = sheet.worksheet('Material Properties')
        equation_sheet = sheet.worksheet('Equivalent Stress Equation')
        graph_raw = graph_sheet.get_all_values()
    
    instantiate_sheets()

    #raw values
    graph_values = graph_raw[1:]

    #Material properties
    @exponential_backoff
    def get_propcell():
        output['material_name'] = mat_prop_sheet.acell('G2').value
        output['product_form'] = mat_prop_sheet.acell('E2').value
        output['k_value'] = mat_prop_sheet.acell('D2').value
    get_propcell()

    #Other properties
    @exponential_backoff
    def get_other_propcell():
        output['tus_ksi'] = mat_prop_sheet.acell('A2').value
        output['tys_ksi'] = mat_prop_sheet.acell('B2').value
        output['temp_F'] = mat_prop_sheet.acell('C2').value
    get_other_propcell()

    #equation stress equations
    coefficients = {}

    @exponential_backoff
    def get_cell_1():
        coefficients['rmax'] = equation_sheet.acell('B1').value
        coefficients['rmin'] = equation_sheet.acell('B2').value
        coefficients['a1'] = equation_sheet.acell('B3').value
    get_cell_1()


    @exponential_backoff
    def get_cell_2():
        coefficients['b1'] = equation_sheet.acell('B4').value
        coefficients['c1'] = equation_sheet.acell('B5').value
        coefficients['d1'] = equation_sheet.acell('B6').value
        coefficients['e1'] = equation_sheet.acell('B7').value
    get_cell_2()
        
    @exponential_backoff
    def get_cell_3():
        coefficients['std'] = equation_sheet.acell('B9').value
        coefficients['rsq'] = equation_sheet.acell('B10').value
        coefficients['std2'] = equation_sheet.acell('B12').value
        coefficients['rsq2'] = equation_sheet.acell('B13').value
    get_cell_3()

    @exponential_backoff
    def get_cell_4():
        coefficients['m1'] = equation_sheet.acell('D1').value
        coefficients['a2'] = equation_sheet.acell('D2').value
        coefficients['b2'] = equation_sheet.acell('D3').value
        coefficients['c2'] = equation_sheet.acell('D4').value
    get_cell_4()
        
    @exponential_backoff
    def get_cell_5():
        coefficients['a3'] = equation_sheet.acell('D5').value
        coefficients['b3'] = equation_sheet.acell('D6').value
        coefficients['c3'] = equation_sheet.acell('D7').value
        coefficients['r1'] = equation_sheet.acell('D8').value
    get_cell_5()
        
    @exponential_backoff
    def get_cell_6():
        coefficients['r2'] = equation_sheet.acell('D9').value
        coefficients['r3'] = equation_sheet.acell('D10').value
        coefficients['n1'] = equation_sheet.acell('H1').value
        coefficients['d2'] = equation_sheet.acell('H2').value
        coefficients['m2'] = equation_sheet.acell('H3').value
        coefficients['m3'] = equation_sheet.acell('H4').value
    get_cell_6()

        
    output['equivalent_stress_equations'] = coefficients
    output['graph'] = graph_values

    return output

def export_to_json(output, filename):
    # Open the file in write mode
    filepath = f'results_files/{filename}'
    with open(filepath, "w") as f:
        # Write the JSON string to the file
        json.dump(output, f, indent=2)
    

def main():
    loc_sheet = pd.read_csv('data_location_sheet.csv')
    iter = tqdm(loc_sheet['Material Name'])
    export = map(parse_gsheet,loc_sheet['ID'], iter)
    export_to_json(list(export), 'output.json')
    

if __name__ == '__main__':
    main()