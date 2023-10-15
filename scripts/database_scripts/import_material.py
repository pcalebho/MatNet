import pandas as pd
import gspread
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