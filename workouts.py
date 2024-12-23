import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

def workouts():
    # Title 
    st.title("Workout Assistant")
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