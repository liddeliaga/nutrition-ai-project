import streamlit as st

from modules.calorie_calculator import (
    calculate_bmr,
    calculate_tdee,
    calculate_target_calories,
    calculate_macros
)

from modules.ml_model import predict_weight_change, predict_diet_recommendation
from modules.meal_planner import generate_meal_plan
from modules.genetic_algorithm import run_genetic_algorithm
from modules.visualization import (
    plot_macro_distribution,
    plot_target_vs_plan
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

allergies = st.sidebar.multiselect(
    "Allergies",
    ["Milk", "Gluten", "Egg", "Nuts", "Fish", "Soy"]
)

preferred_cuisine = st.sidebar.selectbox(
    "Preferred Cuisine",
    ["Any", "Turkish", "Mediterranean", "Asian", "Western"]
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

    bmi = weight / ((height / 100) ** 2)

    user_data = {
        "age": age,
        "gender": gender,
        "height": height,
        "current_weight": weight,
        "bmi": bmi,
        "bmr": bmr,
        "tdee": tdee,
        "daily_calories": target_calories,
        "activity_level": activity_level,
        "protein": macros["protein"],
        "carbs": macros["carbs"],
        "fat": macros["fat"],
        "goal": goal
    }

    predicted_weight_change = predict_weight_change(user_data)
    diet_recommendation = predict_diet_recommendation(user_data)

    meal_plan = generate_meal_plan(
        target_calories,
        macros["protein"],
        macros["carbs"],
        macros["fat"],
        diet_recommendation=diet_recommendation,
        allergies=allergies,
        preferred_cuisine=preferred_cuisine
    )

    if meal_plan.empty:
        st.error("No suitable meal plan found for selected filters.")
        st.stop()

    plan_calories = meal_plan["Calories"].sum()
    plan_protein = meal_plan["Protein"].sum()
    plan_carbs = meal_plan["Carbs"].sum()
    plan_fat = meal_plan["Fat"].sum()

    targets = {
        "calories": target_calories,
        "protein": macros["protein"],
        "carbs": macros["carbs"],
        "fat": macros["fat"]
    }

    plan_totals = {
        "calories": plan_calories,
        "protein": plan_protein,
        "carbs": plan_carbs,
        "fat": plan_fat
    }

    ga_result = run_genetic_algorithm(targets)

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

        



    st.subheader("Machine Learning Predictions")

    col_ml1, col_ml2, col_ml3 = st.columns(3)

    with col_ml1:
        st.metric(
            "Predicted Weekly Weight Change",
            f"{predicted_weight_change:.2f} kg"
        )

    with col_ml2:
        st.metric(
            "Diet Recommendation",
            diet_recommendation
        )

    with col_ml3:
        st.metric(
            "BMI",
            f"{bmi:.1f}"
        )

    st.subheader("Genetic Algorithm Result")

    col7, col8, col9 = st.columns(3)

    with col7:
        st.metric("Best Fitness", ga_result["best_fitness"])

    with col8:
        st.metric("Mutation Rate", ga_result["mutation_rate"])

    with col9:
        st.metric("Population Size", ga_result["population_size"])

    st.subheader("Generated Meal Plan")
    st.dataframe(meal_plan, use_container_width=True)

    st.subheader("Generated Plan Totals")

    col10, col11, col12, col13 = st.columns(4)

    with col10:
        st.metric("Plan Calories", f"{plan_calories:.0f} kcal")

    with col11:
        st.metric("Plan Protein", f"{plan_protein:.1f} g")

    with col12:
        st.metric("Plan Carbs", f"{plan_carbs:.1f} g")

    with col13:
        st.metric("Plan Fat", f"{plan_fat:.1f} g")

    st.subheader("Graphs")

    macro_fig = plot_macro_distribution(
        macros["protein"],
        macros["carbs"],
        macros["fat"]
    )

    st.pyplot(macro_fig)

    calories_fig = plot_target_vs_plan(
        target_calories,
        plan_calories
    )

    st.pyplot(calories_fig)

else:
    st.info("Enter user information from the sidebar and click Generate Plan.")