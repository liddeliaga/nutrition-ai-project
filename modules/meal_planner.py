import pandas as pd

from config import FOODS_DATA_PATH


def filter_foods(foods, diet_recommendation, allergies, preferred_cuisine):
    foods["suitable_diets"] = foods["suitable_diets"].fillna("Balanced")
    foods["not_suitable_for"] = foods["not_suitable_for"].fillna("None")
    foods["allergens"] = foods["allergens"].fillna("None")
    foods["cuisine"] = foods["cuisine"].fillna("Any")

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

    return filtered_foods


def get_meal_options(filtered_foods, meal_types):
    return filtered_foods[
        filtered_foods["meal_type"].isin(meal_types)
    ]


def calculate_plan_score(plan, target_calories, target_protein, target_carbs, target_fat):
    plan_calories = plan["Calories"].sum()
    plan_protein = plan["Protein"].sum()
    plan_carbs = plan["Carbs"].sum()
    plan_fat = plan["Fat"].sum()

    calorie_error = abs(target_calories - plan_calories)
    protein_error = abs(target_protein - plan_protein)
    carbs_error = abs(target_carbs - plan_carbs)
    fat_error = abs(target_fat - plan_fat)

    score = (
        calorie_error * 2
        + protein_error * 5
        + carbs_error * 2
        + fat_error * 3
    )

    return score


def create_plan_from_foods(breakfast, lunch, dinner, snack):
    rows = [
        ("Breakfast", breakfast),
        ("Lunch", lunch),
        ("Dinner", dinner),
        ("Snack", snack)
    ]

    meal_plan_rows = []

    for meal_name, food in rows:
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


def generate_meal_plan(
    target_calories,
    target_protein,
    target_carbs,
    target_fat,
    diet_recommendation="Balanced",
    allergies=None,
    preferred_cuisine="Any",
    trial_count=300
):
    """
    Generates a meal plan from foods.csv.

    This version uses repeated random search to select the best plan.
    Later, this will be replaced by a genetic algorithm.
    """

    if allergies is None:
        allergies = []

    foods = pd.read_csv(FOODS_DATA_PATH)

    filtered_foods = filter_foods(
        foods,
        diet_recommendation,
        allergies,
        preferred_cuisine
    )

    breakfast_options = get_meal_options(filtered_foods, ["breakfast", "any"])
    lunch_options = get_meal_options(filtered_foods, ["lunch", "lunch_dinner", "any"])
    dinner_options = get_meal_options(filtered_foods, ["dinner", "lunch_dinner", "any"])
    snack_options = get_meal_options(filtered_foods, ["snack", "any"])

    if (
        breakfast_options.empty
        or lunch_options.empty
        or dinner_options.empty
        or snack_options.empty
    ):
        return pd.DataFrame()

    best_plan = None
    best_score = float("inf")

    for _ in range(trial_count):
        breakfast = breakfast_options.sample(1).iloc[0]
        lunch = lunch_options.sample(1).iloc[0]
        dinner = dinner_options.sample(1).iloc[0]
        snack = snack_options.sample(1).iloc[0]

        candidate_plan = create_plan_from_foods(
            breakfast,
            lunch,
            dinner,
            snack
        )

        score = calculate_plan_score(
            candidate_plan,
            target_calories,
            target_protein,
            target_carbs,
            target_fat
        )

        if score < best_score:
            best_score = score
            best_plan = candidate_plan

    return best_plan