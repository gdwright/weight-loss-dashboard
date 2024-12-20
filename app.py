import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# File to store logged data
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

# Load existing data
logged_data = load_data()
target_data = generate_target_data()

# Ensure "Date" column is datetime
if not logged_data.empty:
    logged_data['Date'] = pd.to_datetime(logged_data['Date'], dayfirst=True)

# Streamlit app
st.title("Weight Loss Dashboard")

# Create tabs
tab1, tab2, tab3 = st.tabs(["Progress Visualization", "Data Logging", "About the Dashboard"])

# Tab 1: Progress Visualization
with tab1:
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

# Tab 2: Data Logging
with tab2:
    # st.header("Log Your Data")

    # # Input fields for logging data
    # date = st.date_input("Date", value=datetime.today())
    # weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
    # calories = st.number_input("Calories Consumed", min_value=0, step=1)
    # deficit = st.number_input("Calorie Deficit", step=1)
    # steps = st.number_input("Steps", min_value=0, step=1)
    # workout = st.text_area("Workout Description")

    # Add new entry
    # if st.button("Add Entry"):
    #     new_row = pd.DataFrame({
    #         'Date': [date],
    #         'Weight': [weight],
    #         'Calories': [calories],
    #         'Deficit': [deficit],
    #         'Steps': [steps],
    #         'Workout': [workout]
    #     })
    #     logged_data = pd.concat([logged_data, new_row], ignore_index=True)
    #     save_data(logged_data)
    #     st.success("Entry added successfully!")

    # Display logged data
    st.subheader("Logged Data")
    st.dataframe(logged_data)

# Tab 3: About the Dashboard
with tab3:
    st.header("About the Dashboard")
    st.markdown("""
    This dashboard is designed to help you track your weight loss progress. It allows you to:
    
    - Visualize your actual weight against your target weight.
    - Track daily calorie deficits.
    - Log data such as weight, calorie intake, steps, and workouts.

    ### How It Works
    1. Use the **Data Logging** tab to input your daily stats.
    2. View your progress in the **Progress Visualization** tab.
    3. Use the plots to identify trends and make adjustments to meet your goals.

    Stay consistent with logging for the most accurate insights!
    """)
