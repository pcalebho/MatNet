import pandas as pd
import gspread
import json
import pymongo
from pathlib import Path

gc = gspread.service_account(Path('google_auth.json'))

def gsheet_to_json(sheet_key: str, material_name: str):
    #Open Spreadsheet
    sheet = gc.open_by_key(sheet_key)
    graph_sheet = sheet.worksheet('Graph Data')
    mat_prop_sheet = sheet.worksheet('Material Properties')
    equation_sheet = sheet.worksheet('Equivalent Stress Equation')

    graph_values = graph_sheet.get_all_values()

    graph_df = pd.DataFrame(graph_values[1:])
    graph_df.columns= graph_values[0]

    mat_name = mat_prop_sheet.acell('G2').value
    product_form = mat_prop_sheet.acell('E2').value
    k_value = mat_prop_sheet.acell('D2').value
    tus = mat_prop_sheet.acell('A2').value
    tys = mat_prop_sheet.acell('B2').value

    rmax = equation_sheet.acell('B1').value
    rmin = equation_sheet.acell('B2').value
    a1 = equation_sheet.acell('B3').value
    b1 = equation_sheet.acell('B4').value
    c1 = equation_sheet.acell('B5').value
    d1 = equation_sheet.acell('B6').value
    e1 = equation_sheet.acell('B7').value
    std = equation_sheet.acell('B9').value
    rsq = equation_sheet.acell('B10').value
    std2 = equation_sheet.acell('B12').value
    rsq2 = equation_sheet.acell('B13').value
    m1 = equation_sheet.acell('D1').value
    a2 = equation_sheet.acell('D2').value
    b2 = equation_sheet.acell('D3').value
    c2 = equation_sheet.acell('D4').value
    a3 = equation_sheet.acell('D5').value
    b3 = equation_sheet.acell('D6').value
    c3 = equation_sheet.acell('D7').value
    r1 = equation_sheet.acell('D8').value
    r2 = equation_sheet.acell('D9').value
    r3 = equation_sheet.acell('D10').value
    n1 = equation_sheet.acell('H1').value
    d2 = equation_sheet.acell('H2').value
    m2 = equation_sheet.acell('H3').value
    m3 = equation_sheet.acell('H4').value

    return graph_df


def main():
    loc_sheet = pd.read_csv('data_location_sheet.csv')
    
    graph_data = gsheet_to_json(loc_sheet.at[0, 'ID'], loc_sheet.at[0, "Material Name"])
    print(graph_data)
    # master_sheet = gc.open_by_key('1GKv5Vv4dpARDjjm-7iSrrHhIKdNinnM5EzZVDhqnpVM')

    # # Get the worksheet
    # worksheet = mastersheet.worksheet('Sheet1')

    # # Get the values in the worksheet
    # values = worksheet.get_all_values()

if __name__ == '__main__':
    main()