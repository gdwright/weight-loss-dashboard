import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from openai import OpenAI
import os
# from config import OPENAI_KEY

# Set your OpenAI API key
os.environ['OPENAI_KEY'] = st.secrets['OPENAI_KEY']

client = OpenAI(api_key=os.getenv('OPENAI_KEY'))

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
tab1, tab2, tab3, tab4 = st.tabs(["Progress Visualization", "Data Logging", "Meal & Workout Planning","About the Dashboard"])

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
with tab3:
    # Title
    st.title("Fitness Assistant")
    st.write("I can help you with meal plans, workout plans, and feedback on your progress.")

    # Input values for the chat GPT prompt
    cols = st.columns(3)
    with cols[0]:
        deficit_input = st.number_input("Daily target calorie deficit (kCal)", max_value=1200)
    with cols[1]:
        weight_input = st.number_input("Weight (kg)", max_value=500, min_value=2, value=None)
        age_input = st.number_input("Age (years)", value=None)
        height_input = st.number_input("Height (cm)", value=None)
    with cols[2]:
        gender_input = st.radio("Gender", ["Female", "Male", "Prefer not to say"])
    dietry_input = st.pills(
        "Dietry requirements",
        ["Gluten-free", "Vegetarian", "Vegan", "Nut allergy", "Non-dairy", "Kosher", "Other"],
        selection_mode="multi"
    )
    orr_dietry_bool = "Other" in dietry_input
    if orr_dietry_bool:
        orr_dietry_input = st.text_area("Other dietry requirements")
    workout_bool = st.toggle("Include a workout plan")
    workout_input = st.pills(
        "Workout days:",
        ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
        selection_mode = "multi",
        disabled=not(workout_bool)
    )
    shopping_list_bool = st.toggle("Include a shopping list")

    if deficit_input > 0:
        deficit_text = f"a daily calorie deficit of {deficit_input}kCal"
    elif deficit_input < 0:
        deficit_text = f"a daily calorie surplus of {deficit_input}kCal"
    else:
        deficit_text = "no calorie deficit/surplus"

    if (gender_input == "Female") or (gender_input == "Male"):
        gender_text = f" for a {gender_input}"
    else:
        gender_text = " for a person"

    if age_input is not None:
        age_text = f" aged {age_input}."
    else:
        age_text = "."

    if len(dietry_input)>0:
        if orr_dietry_bool:
            dietry_text = f" Please consider the following dietry requirements{dietry_input} and also {orr_dietry_input}"
        else:
            dietry_text = f" Please consider the following dietry requirements{dietry_input}"
    else:
        dietry_text = " There are no particular dietry needs."

    if workout_bool:
        workout_text = f" Please include workout instructions for the following days: {workout_input}"
    else:
        workout_text = ""

    if shopping_list_bool:
        shopping_list_text = " Please also include a shopping list with the quantities/weights of the ingredients required for the meal plan."
    else:
        shopping_list_text = ""

    user_input = (
        "Please create a week long meal-plan (including snacks) with " + deficit_text + gender_text + age_text + dietry_text + workout_text + shopping_list_text +
        "Please include the estimated calories next to the name of each meal. " +
        "Also put the shopping list in the order of supermarket sections"
    )

    # Function to interact with ChatGPT
    def chat_with_gpt(prompt):
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a fitness assistant. Provide meal plans, workout plans, and feedback based on the user's goals. Avoid unrelated topics."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    },
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"An error occurred: {e}"

    # Display GPT response
    if st.button("Submit"):
        if user_input:
            st.write("Your request: " + f"***{user_input}***")
            with st.spinner("Processing..."):
                response = chat_with_gpt(user_input)
            st.write(response)
        else:
            st.warning("Please enter a query.")

    # Footer
    st.write("---")
    st.write("Powered by OpenAI GPT")


# Tab 4: About the Dashboard
with tab4:
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
