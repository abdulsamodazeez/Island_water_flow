import streamlit as st
import pandas as pd
import gspread
import os
from dotenv import load_dotenv
from algo import find_water_flow  

load_dotenv()

# Function to fetch grid data from Google Sheets
def get_grid_data(sheet_url, tab_name):
    """
    Fetches grid data from a specific Google Sheets tab and converts it into a NumPy array.

    Args:
        sheet_url (str): The URL of the Google Sheet.
        tab_name (str): The tab (worksheet) name within the sheet.

    Returns:
        np.ndarray: A NumPy array of the grid data in float format.
    """
    json_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON_PATH')
    gc = gspread.service_account(filename=json_path)
    
    try:
        sheet = gc.open_by_url(sheet_url)
        worksheet = sheet.worksheet(tab_name)
        data = worksheet.get_all_values()
        df = pd.DataFrame(data)
        return df.astype(float).values
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

# Streamlit app definition
def app():
    """
    Streamlit app to visualize island water flow analysis using data from Google Sheets.
    Allows the user to select a scenario from multiple tabs and applies the `find_water_flow` algorithm
    to determine the cells where water flows to both Pacific and Atlantic oceans.
    """
    st.title("Island Water Flow Analysis")

    sheet_url = 'https://docs.google.com/spreadsheets/d/1guE4DI4wQpBXPlXRKXVEeb3nH84Phq6YqgYK9M4NUT0'

    # Load tab names (scenarios) from the Google Sheets
    json_path = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON_PATH')
    gc = gspread.service_account(filename=json_path)
    sheet = gc.open_by_url(sheet_url)
    tabs = [ws.title for ws in sheet.worksheets()]

    tab_name = st.selectbox("Select a Scenario", tabs)

    grid = get_grid_data(sheet_url, tab_name)
    
    if grid is not None:
        st.write("Grid Data:")
        st.dataframe(pd.DataFrame(grid))

        grid = grid.tolist()  
        coordinates = find_water_flow(grid) 

        if coordinates:
            st.write(f"Number of cells that flow to both oceans: {len(coordinates)}")
            st.write("Coordinates of qualifying cells:")
            for coord in coordinates:
                st.write(f"({coord[0]}, {coord[1]})")  
        else:
            st.write("No cells flow to both oceans.")

if __name__ == '__main__':
    app()
