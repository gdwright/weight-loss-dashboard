import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from openai import OpenAI
from progress_dashboard import progress_dashboard 
from data import load_data, generate_target_data
from meals import meals
from workouts import workouts

# Set the OpenAI API key
client = OpenAI(api_key=st.secrets['OPENAI_KEY'])

# Load existing data
logged_data = load_data()
target_data = generate_target_data()

# Streamlit app
st.title("Weight Loss Dashboard")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Progress Visualization", "Data Logging", "Meals", "Workouts","About the Dashboard"])

# Tab 1: Progress Visualization
with tab1:
    progress_dashboard()

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

# Tab 3 Meals
with tab3:
    meals()

# Tab 4: Workouts
with tab4:
    st.header("Workouts")

    # workouts()


# Tab 5: About the Dashboard
with tab5:
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
