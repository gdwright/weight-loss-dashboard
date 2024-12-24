import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from openai import OpenAI
from data import load_data, generate_target_data

# Set the OpenAI API key
client = OpenAI(api_key=st.secrets['OPENAI_KEY'])

# File to store logged data (need to change to a DB)
# DATA_FILE = "data.csv"

# # Constants for target weight data
# TARGET_START_DATE = datetime(2024, 12, 9)
# TARGET_END_DATE = TARGET_START_DATE + pd.Timedelta(days=120)
# START_WEIGHT = 101.3
# TARGET_WEIGHT = 91.3

# # Generate target weight data
# def generate_target_data():
#     target_dates = pd.date_range(TARGET_START_DATE, TARGET_END_DATE)
#     target_weights = [START_WEIGHT - (START_WEIGHT - TARGET_WEIGHT) * (i / len(target_dates)) for i in range(len(target_dates))]
#     return pd.DataFrame({"Date": target_dates, "Target Weight": target_weights})

# # Load or create the data file
# def load_data():
#     try:
#         return pd.read_csv(DATA_FILE, parse_dates=['Date'])
#     except FileNotFoundError:
#         return pd.DataFrame(columns=['Date', 'Weight', 'Calories', 'Deficit', 'Steps', 'Workout'])

# Load existing data
logged_data = load_data()
target_data = generate_target_data()

# Ensure "Date" column is datetime
if not logged_data.empty:
    logged_data['Date'] = pd.to_datetime(logged_data['Date'], dayfirst=True)

def progress_dashboard():
    st.header("Progress Visualization")
    # Merge target and logged data
    if not logged_data.empty:
        merged_data = pd.merge(target_data, logged_data, on='Date', how='left')

        # Weight vs Target Weight plot
        fig, ax = plt.subplots()
        ax.plot(
            merged_data['Date'],
            merged_data['Target Weight'],
            label='Target Weight',
            linestyle='--',
            color='blue'
        )
        ax.plot(merged_data['Date'], merged_data['Weight'], label='Actual Weight', color='red')
        ax.set_xlabel("Date")
        ax.tick_params(axis='x', labelrotation=90)
        ax.set_ylabel("Weight (kg)")
        ax.set_title("Weight vs. Target Weight Over Time")
        ax.legend()
        st.pyplot(fig)

        # Calorie Deficit bar chart
        fig, ax = plt.subplots()
        ax.bar(
            merged_data['Date'],
            merged_data['Deficit'],
            label='Calorie Deficit',
            color=np.where(merged_data['Deficit'] < 0, 'crimson', 'deepskyblue')
        )
        ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
        ax.set_xlabel("Date")
        ax.tick_params(axis='x', labelrotation=90)
        ax.set_ylabel("Calorie Deficit (kcal)")
        ax.set_title("Daily Calorie Deficit")
        ax.legend()
        st.pyplot(fig)
    else:
        st.info("No data to display. Please log your progress in the Data Logging tab.")