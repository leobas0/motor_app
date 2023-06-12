import streamlit as st
import pandas as pd
import sqlite3

### streamlit run /Users/macbookpro/Desktop/LABS/motor_app/main.py

# Set up the function to execute SQL queries
def run_query(query):
    with sqlite3.connect('my_database.db') as conn:
        return pd.read_sql_query(query, conn)

# Function to get policy details
def get_policy_details(user_id):
    df = run_query(f'SELECT * FROM user_data WHERE User_ID = {user_id}')
    return df

# Function to get tow truck and workshop details
def get_tow_truck_and_workshop_details(area_code):
    tow_truck_df = run_query(f'SELECT * FROM tow_truck WHERE Area_Code = {area_code}')
    workshop_df = run_query(f'SELECT * FROM workshop WHERE Area_Code = {area_code}')
    return tow_truck_df, workshop_df

# Title
st.title('Insurance Claim Tracker')

# User inputs
user_id = st.text_input('Enter your User ID (from QR code):')
location = st.selectbox('Select Your Location:', ['Kuala Lumpur', 'Ipoh', 'Georgetown', 'Alor Setar', 'Johor Bahru'])

# Fetch area code for the selected location
area_code_df = run_query(f'SELECT * FROM accident_location WHERE Location = "{location}"')
area_code = area_code_df['Area_Code'].values[0] if not area_code_df.empty else None

if user_id and location:
    # Fetch policy details
    policy_df = get_policy_details(user_id)
    
    # Fetch tow truck and workshop details
    tow_truck_df, workshop_df = get_tow_truck_and_workshop_details(area_code)
    
    # Display policy details
    st.subheader('Your Policy Details:')
    st.dataframe(policy_df)

    # Display tow truck details
    st.subheader('Nearby Tow Trucks:')
    st.dataframe(tow_truck_df)

    # Display workshop details
    st.subheader('Nearby Workshops:')
    st.dataframe(workshop_df)
