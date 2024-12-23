import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np


# File to store logged data (need to change to a DB)
DATA_FILE = "data.csv"

# Constants for target weight data
TARGET_START_DATE = datetime(2024, 12, 9)
TARGET_END_DATE = TARGET_START_DATE + pd.Timedelta(days=120)
START_WEIGHT = 101.3
TARGET_WEIGHT = 91.3

# Generate target weight data
def generate_target_data():
    target_dates = pd.date_range(TARGET_START_DATE, TARGET_END_DATE)
    target_weights = [START_WEIGHT - (START_WEIGHT - TARGET_WEIGHT) * (i / len(target_dates)) for i in range(len(target_dates))]
    return pd.DataFrame({"Date": target_dates, "Target Weight": target_weights})

# Load or create the data file
def load_data():
    try:
        return pd.read_csv(DATA_FILE, parse_dates=['Date'])
    except FileNotFoundError:
        return pd.DataFrame(columns=['Date', 'Weight', 'Calories', 'Deficit', 'Steps', 'Workout'])

# Save data back to the file
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

