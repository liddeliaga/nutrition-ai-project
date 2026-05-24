import os
import joblib
import pandas as pd

from config import MODEL_PATH


def _fallback_weight_change_prediction(user_data):
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


def _build_model_input(user_data):
    gender = user_data.get("gender", "male")
    activity_level = user_data.get("activity_level", "sedentary")

    gender = "Male" if gender == "male" else "Female"

    activity_map = {
        "sedentary":  "Sedentary",
        "light":      "Light",
        "moderate":   "Moderate",
        "active":     "Active",
        "very_active": "Very Active",
    }
    activity_level = activity_map.get(activity_level, "Sedentary")

    return pd.DataFrame([{
        "Age":                              user_data.get("age", 25),
        "Gender":                           gender,
        "Weight_kg":                        user_data.get("current_weight", 70),
        "Height_cm":                        user_data.get("height", 170),
        "BMI":                              user_data.get("bmi", 24),
        "Physical_Activity_Level":          activity_level,
        "Daily_Caloric_Intake":             user_data.get("daily_calories", 2000),
        "Weekly_Exercise_Hours":            user_data.get("weekly_exercise_hours", 3),
        "Adherence_to_Diet_Plan":           user_data.get("adherence_to_diet_plan", 80),
        "Dietary_Nutrient_Imbalance_Score": user_data.get("dietary_nutrient_imbalance_score", 3),
    }])


def predict_weight_change(user_data):
    if not os.path.exists(MODEL_PATH):
        return _fallback_weight_change_prediction(user_data)
    try:
        model = joblib.load(MODEL_PATH)
        prediction = model.predict(_build_model_input(user_data))[0]
        return round(float(prediction), 2)
    except Exception:
        return _fallback_weight_change_prediction(user_data)


def predict_diet_recommendation(user_data):
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
