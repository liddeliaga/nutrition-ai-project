def predict_weight_change(user_data):
    """
    Placeholder regression function.

    Later, this function will predict estimated weekly weight change
    by using a trained regression model.

    Parameters:
        user_data (dict): User information and nutrition targets.

    Returns:
        float: Estimated weekly weight change in kg.
    """

    goal = user_data.get("goal", "maintain_weight")
    daily_calories = user_data.get("daily_calories", 2000)
    tdee = user_data.get("tdee", 2000)

    calorie_balance = daily_calories - tdee

    estimated_weekly_change = (calorie_balance * 7) / 7700

    if goal == "lose_weight":
        return round(min(estimated_weekly_change, -0.1), 2)

    if goal == "gain_weight":
        return round(max(estimated_weekly_change, 0.1), 2)

    return round(estimated_weekly_change, 2)


def predict_diet_recommendation(user_data):
    """
    Placeholder classification function.

    Later, this function will predict diet recommendation
    by using a trained classification model.

    Parameters:
        user_data (dict): User information.

    Returns:
        str: Diet recommendation category.
    """

    goal = user_data.get("goal", "maintain_weight")
    activity_level = user_data.get("activity_level", "sedentary")
    bmi = user_data.get("bmi", 25)

    if bmi >= 30:
        return "Low_Calorie"

    if goal == "lose_weight":
        return "Low_Carb"

    if goal == "gain_weight":
        return "High_Protein"

    if activity_level in ["active", "very_active"]:
        return "High_Protein"

    return "Balanced"