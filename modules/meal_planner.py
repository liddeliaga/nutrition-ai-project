import pandas as pd

from config import FOODS_DATA_PATH


def generate_meal_plan(
    target_calories,
    target_protein,
    target_carbs,
    target_fat,
    diet_recommendation="Balanced",
    allergies=None,
    preferred_cuisine="Any"
):
    """
    Generates a simple meal plan from foods.csv.

    This is still a placeholder version.
    Later, the genetic algorithm will optimize the food selection.

    Parameters:
        target_calories (float): Daily calorie target.
        target_protein (float): Daily protein target.
        target_carbs (float): Daily carbohydrate target.
        target_fat (float): Daily fat target.
        diet_recommendation (str): Predicted or selected diet type.
        allergies (list): User allergies.
        preferred_cuisine (str): User cuisine preference.

    Returns:
        pandas.DataFrame: Generated meal plan.
    """

    if allergies is None:
        allergies = []

    foods = pd.read_csv(FOODS_DATA_PATH)

    foods["not_suitable_for"] = foods["not_suitable_for"].fillna("None")
    foods["allergens"] = foods["allergens"].fillna("None")

    filtered_foods = foods[
        foods["suitable_diets"].str.contains(diet_recommendation, na=False)
    ]

    if filtered_foods.empty:
        filtered_foods = foods[
            foods["suitable_diets"].str.contains("Balanced", na=False)
        ]

    for allergy in allergies:
        filtered_foods = filtered_foods[
            ~filtered_foods["allergens"].str.contains(allergy, na=False)
        ]

    if preferred_cuisine != "Any":
        cuisine_filtered = filtered_foods[
            (filtered_foods["cuisine"] == preferred_cuisine)
            | (filtered_foods["cuisine"] == "Any")
        ]

        if not cuisine_filtered.empty:
            filtered_foods = cuisine_filtered

    breakfast_options = filtered_foods[
        filtered_foods["meal_type"].isin(["breakfast", "any"])
    ]

    lunch_options = filtered_foods[
        filtered_foods["meal_type"].isin(["lunch", "lunch_dinner", "any"])
    ]

    dinner_options = filtered_foods[
        filtered_foods["meal_type"].isin(["dinner", "lunch_dinner", "any"])
    ]

    snack_options = filtered_foods[
        filtered_foods["meal_type"].isin(["snack", "any"])
    ]

    selected_meals = []

    if not breakfast_options.empty:
        selected_meals.append(("Breakfast", breakfast_options.sample(1).iloc[0]))

    if not lunch_options.empty:
        selected_meals.append(("Lunch", lunch_options.sample(1).iloc[0]))

    if not dinner_options.empty:
        selected_meals.append(("Dinner", dinner_options.sample(1).iloc[0]))

    if not snack_options.empty:
        selected_meals.append(("Snack", snack_options.sample(1).iloc[0]))

    meal_plan_rows = []

    for meal_name, food in selected_meals:
        meal_plan_rows.append({
            "Meal": meal_name,
            "Food": food["food_name"],
            "Calories": food["calories"],
            "Protein": food["protein"],
            "Carbs": food["carbs"],
            "Fat": food["fat"],
            "Serving Size": food["serving_size"],
            "Category": food["category"],
            "Cuisine": food["cuisine"]
        })

    return pd.DataFrame(meal_plan_rows)