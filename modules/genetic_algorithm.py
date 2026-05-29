import os
import random
import pandas as pd

from config import FOODS_DATA_PATH, GENERATED_MEAL_PLAN_PATH, OPTIMIZATION_RESULTS_PATH


def _contains_value(cell_value, target):
    if pd.isna(cell_value):
        return False
    values = [str(v).strip().lower() for v in str(cell_value).split("|")]
    return str(target).strip().lower() in values


def filter_foods_for_ga(foods, diet_recommendation, allergies, preferred_cuisine):
    foods = foods.copy()

    foods["suitable_diets"] = foods["suitable_diets"].fillna("Balanced")
    foods["not_suitable_for"] = foods["not_suitable_for"].fillna("None")
    foods["allergens"] = foods["allergens"].fillna("None")
    foods["cuisine"] = foods["cuisine"].fillna("Any")

    filtered_foods = foods[
        foods["suitable_diets"].apply(lambda x: _contains_value(x, diet_recommendation))
    ]

    if filtered_foods.empty:
        filtered_foods = foods[
            foods["suitable_diets"].apply(lambda x: _contains_value(x, "Balanced"))
        ]

    if filtered_foods.empty:
        filtered_foods = foods.copy()

    for allergy in allergies:
        filtered_foods = filtered_foods[
            ~filtered_foods["allergens"].apply(lambda x: _contains_value(x, allergy))
        ]

    if preferred_cuisine != "Any":
        cuisine_filtered = filtered_foods[
            (filtered_foods["cuisine"].str.lower() == preferred_cuisine.lower())
            | (filtered_foods["cuisine"].str.lower() == "any")
        ]
        if not cuisine_filtered.empty:
            filtered_foods = cuisine_filtered

    return filtered_foods.reset_index(drop=True)


def get_options_by_meal_type(foods):
    return {
        "Breakfast": foods[foods["meal_type"].isin(["breakfast", "any"])].reset_index(drop=True),
        "Lunch":     foods[foods["meal_type"].isin(["lunch", "lunch_dinner", "any"])].reset_index(drop=True),
        "Dinner":    foods[foods["meal_type"].isin(["dinner", "lunch_dinner", "any"])].reset_index(drop=True),
        "Snack":     foods[foods["meal_type"].isin(["snack", "any"])].reset_index(drop=True),
    }


def create_random_individual(meal_options):
    return {meal: random.randint(0, len(opts) - 1) for meal, opts in meal_options.items()}


def individual_to_dataframe(individual, meal_options):
    rows = []
    for meal_name, food_index in individual.items():
        food = meal_options[meal_name].iloc[food_index]
        rows.append({
            "Meal Type": meal_name,
            "Food":      food["food_name"],
            "Calories":  food["calories"],
            "Protein":   food["protein"],
            "Carbs":     food["carbs"],
            "Fat":       food["fat"],
            "Serving Size": food["serving_size"],
            "Category":  food["category"],
            "Cuisine":   food["cuisine"],
        })
    return pd.DataFrame(rows)


def calculate_plan_error(plan_df, targets):
    calorie_error = abs(targets["calories"] - plan_df["Calories"].sum())
    protein_error = abs(targets["protein"] - plan_df["Protein"].sum())
    carbs_error   = abs(targets["carbs"]   - plan_df["Carbs"].sum())
    fat_error     = abs(targets["fat"]     - plan_df["Fat"].sum())
    return calorie_error * 2 + protein_error * 5 + carbs_error * 2 + fat_error * 3


def calculate_fitness(plan_df, targets):
    return 1 / (1 + calculate_plan_error(plan_df, targets))


def crossover(parent1, parent2):
    return {
        meal: parent1[meal] if random.random() < 0.5 else parent2[meal]
        for meal in parent1
    }


def mutate(individual, meal_options, mutation_rate):
    mutated = individual.copy()
    for meal, opts in meal_options.items():
        if random.random() < mutation_rate:
            mutated[meal] = random.randint(0, len(opts) - 1)
    return mutated


def run_genetic_algorithm(
    targets,
    diet_recommendation="Balanced",
    allergies=None,
    preferred_cuisine="Any",
    population_size=100,
    generation_count=50,
    mutation_rate=0.10,
    elite_ratio=0.2,
):
    if allergies is None:
        allergies = []

    foods = pd.read_csv(FOODS_DATA_PATH)
    filtered_foods = filter_foods_for_ga(foods, diet_recommendation, allergies, preferred_cuisine)
    meal_options = get_options_by_meal_type(filtered_foods)

    for meal_name, opts in meal_options.items():
        if opts.empty:
            return pd.DataFrame(), {
                "best_fitness": 0,
                "best_error": None,
                "mutation_rate": mutation_rate,
                "population_size": population_size,
                "generation_count": generation_count,
                "message": f"No suitable food found for {meal_name}",
            }

    population = [create_random_individual(meal_options) for _ in range(population_size)]

    best_individual = None
    best_fitness = -1
    best_error = None
    history = []
    elite_count = max(2, int(population_size * elite_ratio))

    for generation in range(generation_count):
        scored = []
        for ind in population:
            plan_df = individual_to_dataframe(ind, meal_options)
            scored.append({
                "individual": ind,
                "fitness": calculate_fitness(plan_df, targets),
                "error":   calculate_plan_error(plan_df, targets),
            })

        scored.sort(key=lambda x: x["fitness"], reverse=True)

        if scored[0]["fitness"] > best_fitness:
            best_fitness   = scored[0]["fitness"]
            best_error     = scored[0]["error"]
            best_individual = scored[0]["individual"]

        history.append({"generation": generation + 1, "best_fitness": best_fitness, "best_error": best_error})

        elites = [s["individual"] for s in scored[:elite_count]]
        new_population = elites.copy()
        while len(new_population) < population_size:
            child = crossover(random.choice(elites), random.choice(elites))
            child = mutate(child, meal_options, mutation_rate)
            new_population.append(child)
        population = new_population

    best_plan_df = individual_to_dataframe(best_individual, meal_options)

    ga_result = {
        "best_fitness":    round(best_fitness, 6),
        "best_error":      round(best_error, 2),
        "mutation_rate":   mutation_rate,
        "population_size": population_size,
        "generation_count": generation_count,
        "plan_totals": {
            "calories": round(best_plan_df["Calories"].sum(), 2),
            "protein":  round(best_plan_df["Protein"].sum(),  2),
            "carbs":    round(best_plan_df["Carbs"].sum(),    2),
            "fat":      round(best_plan_df["Fat"].sum(),      2),
        },
        "message": "Genetic algorithm completed successfully",
    }

    os.makedirs(GENERATED_MEAL_PLAN_PATH.parent, exist_ok=True)
    best_plan_df.to_csv(GENERATED_MEAL_PLAN_PATH, index=False)
    pd.DataFrame(history).to_csv(OPTIMIZATION_RESULTS_PATH, index=False)

    return best_plan_df, ga_result
