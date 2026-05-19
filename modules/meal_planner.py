import pandas as pd


def generate_meal_plan(target_calories, target_protein, target_carbs, target_fat):
    """
    Placeholder meal plan generator.

    Later, this function will use the genetic algorithm output
    to generate an optimized daily meal plan.

    Parameters:
        target_calories (float): Daily calorie target.
        target_protein (float): Daily protein target.
        target_carbs (float): Daily carbohydrate target.
        target_fat (float): Daily fat target.

    Returns:
        pandas.DataFrame: Generated meal plan.
    """

    meal_plan = pd.DataFrame([
        {
            "Meal": "Breakfast",
            "Food": "Oatmeal",
            "Calories": 370,
            "Protein": 13,
            "Carbs": 60,
            "Fat": 7
        },
        {
            "Meal": "Lunch",
            "Food": "Chicken Breast + Rice",
            "Calories": 520,
            "Protein": 38,
            "Carbs": 55,
            "Fat": 8
        },
        {
            "Meal": "Dinner",
            "Food": "Salmon + Potato",
            "Calories": 600,
            "Protein": 42,
            "Carbs": 45,
            "Fat": 22
        },
        {
            "Meal": "Snack",
            "Food": "Yogurt + Banana",
            "Calories": 250,
            "Protein": 10,
            "Carbs": 40,
            "Fat": 5
        }
    ])

    return meal_plan