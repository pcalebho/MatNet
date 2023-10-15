import pandas as pd
import gspread
import json
import pymongo
from pathlib import Path

gc = gspread.service_account(Path('google_auth.json'))

def parse_gsheet(sheet_key: str, material_name: str):
    output = {}

    #Open Spreadsheet
    sheet = gc.open_by_key(sheet_key)
    output['description'] = sheet.title

    graph_sheet = sheet.worksheet('Graph Data')
    mat_prop_sheet = sheet.worksheet('Material Properties')
    equation_sheet = sheet.worksheet('Equivalent Stress Equation')

    graph_raw = graph_sheet.get_all_values()

    #raw values
    graph_values = graph_raw[1:]

    #Material properties
    output['material_name'] = mat_prop_sheet.acell('G2').value
    output['product_form'] = mat_prop_sheet.acell('E2').value
    output['k_value'] = mat_prop_sheet.acell('D2').value

    #Other properties
    output['tus_ksi'] = mat_prop_sheet.acell('A2').value
    output['tys_ksi'] = mat_prop_sheet.acell('B2').value
    output['temp_F'] = mat_prop_sheet.acell('C2').value

    #equation stress equations
    coefficients = {}
    coefficients['rmax'] = equation_sheet.acell('B1').value
    coefficients['rmin'] = equation_sheet.acell('B2').value
    coefficients['a1'] = equation_sheet.acell('B3').value
    coefficients['b1'] = equation_sheet.acell('B4').value
    coefficients['c1'] = equation_sheet.acell('B5').value
    coefficients['d1'] = equation_sheet.acell('B6').value
    coefficients['e1'] = equation_sheet.acell('B7').value
    coefficients['std'] = equation_sheet.acell('B9').value
    coefficients['rsq'] = equation_sheet.acell('B10').value
    coefficients['std2'] = equation_sheet.acell('B12').value
    coefficients['rsq2'] = equation_sheet.acell('B13').value
    coefficients['m1'] = equation_sheet.acell('D1').value
    coefficients['a2'] = equation_sheet.acell('D2').value
    coefficients['b2'] = equation_sheet.acell('D3').value
    coefficients['c2'] = equation_sheet.acell('D4').value
    coefficients['a3'] = equation_sheet.acell('D5').value
    coefficients['b3'] = equation_sheet.acell('D6').value
    coefficients['c3'] = equation_sheet.acell('D7').value
    coefficients['r1'] = equation_sheet.acell('D8').value
    coefficients['r2'] = equation_sheet.acell('D9').value
    coefficients['r3'] = equation_sheet.acell('D10').value
    coefficients['n1'] = equation_sheet.acell('H1').value
    coefficients['d2'] = equation_sheet.acell('H2').value
    coefficients['m2'] = equation_sheet.acell('H3').value
    coefficients['m3'] = equation_sheet.acell('H4').value
    
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
    export = map(parse_gsheet,loc_sheet['ID'], loc_sheet["Material Name"])
    export_to_json(list(export), 'output.json')
    

if __name__ == '__main__':
    main()