def calculate_bmr(gender, weight, height, age):
    """
    Calculates Basal Metabolic Rate using the Mifflin-St Jeor formula.
    weight: kg
    height: cm
    age: years
    """

    if gender == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5

    return 10 * weight + 6.25 * height - 5 * age - 161


def calculate_tdee(bmr, activity_level):
    """
    Calculates Total Daily Energy Expenditure.
    """

    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }

    return bmr * activity_multipliers.get(activity_level, 1.2)


def calculate_target_calories(tdee, goal):
    """
    Adjusts daily calories according to user's goal.
    """

    if goal == "lose_weight":
        return tdee - 500

    if goal == "gain_weight":
        return tdee + 300

    return tdee


def calculate_macros(target_calories, weight):
    """
    Calculates daily protein, carbohydrate and fat targets.
    """

    protein = weight * 1.8
    fat = weight * 0.8

    protein_calories = protein * 4
    fat_calories = fat * 9

    remaining_calories = target_calories - protein_calories - fat_calories
    carbs = max(0, remaining_calories) / 4

    return {
        "protein": round(protein, 1),
        "carbs": round(carbs, 1),
        "fat": round(fat, 1)
    }