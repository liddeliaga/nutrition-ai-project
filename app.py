import streamlit as st

from modules.calorie_calculator import (
    calculate_bmr,
    calculate_tdee,
    calculate_target_calories,
    calculate_macros
)


st.set_page_config(
    page_title="AI Nutrition Planner",
    page_icon="🥗",
    layout="wide"
)


st.title("AI Based Personalized Nutrition Planner")
st.write(
    "Machine Learning and Genetic Algorithm based personalized nutrition planning system."
)


st.sidebar.header("User Information")

age = st.sidebar.number_input(
    "Age",
    min_value=10,
    max_value=100,
    value=22
)

gender = st.sidebar.selectbox(
    "Gender",
    ["male", "female"]
)

height = st.sidebar.number_input(
    "Height (cm)",
    min_value=100,
    max_value=230,
    value=175
)

weight = st.sidebar.number_input(
    "Current Weight (kg)",
    min_value=30,
    max_value=200,
    value=75
)

activity_level = st.sidebar.selectbox(
    "Activity Level",
    ["sedentary", "light", "moderate", "active", "very_active"]
)

goal = st.sidebar.selectbox(
    "Goal",
    ["lose_weight", "maintain_weight", "gain_weight"]
)


if st.sidebar.button("Generate Plan"):
    bmr = calculate_bmr(gender, weight, height, age)
    tdee = calculate_tdee(bmr, activity_level)
    target_calories = calculate_target_calories(tdee, goal)
    macros = calculate_macros(target_calories, weight)

    st.subheader("Calorie and Macro Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("BMR", f"{bmr:.0f} kcal")

    with col2:
        st.metric("TDEE", f"{tdee:.0f} kcal")

    with col3:
        st.metric("Target Calories", f"{target_calories:.0f} kcal")

    st.subheader("Macro Targets")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("Protein", f"{macros['protein']} g")

    with col5:
        st.metric("Carbohydrate", f"{macros['carbs']} g")

    with col6:
        st.metric("Fat", f"{macros['fat']} g")

else:
    st.info("Enter user information from the sidebar and click Generate Plan.")