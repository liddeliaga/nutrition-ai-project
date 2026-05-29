from pathlib import Path

BASE_DIR = Path(__file__).parent

FOODS_DATA_PATH = BASE_DIR / "data/foods.csv"
USER_WEIGHT_DATA_PATH = BASE_DIR / "data/user_weight_data.csv"

MODEL_PATH = BASE_DIR / "models/best_weight_model.pkl"

MODEL_RESULTS_PATH = BASE_DIR / "outputs/model_results.csv"
OPTIMIZATION_RESULTS_PATH = BASE_DIR / "outputs/optimization_results.csv"
GENERATED_MEAL_PLAN_PATH = BASE_DIR / "outputs/generated_meal_plan.csv"

DEFAULT_TARGET_DAYS = 7